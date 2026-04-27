from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# =====================================================
# STATE DEFINITION
# =====================================================

class State(TypedDict):
    user_request: str
    plan: str
    tool_result: str
    final_answer: str
    validation: str
    retries: int


# =====================================================
# LLM CONFIGURATION (Groq - Free)
# =====================================================

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.2
)


# =====================================================
# TOOL (REAL ACTION)
# =====================================================

def calculate_sum(a: int, b: int) -> int:
    """Simple deterministic tool for demonstration"""
    return a + b


# =====================================================
# PLANNER NODE
# =====================================================

def planner_node(state: State) -> State:
    plan = llm.invoke(
        f"""
User request:
{state['user_request']}

Create a clear step-by-step plan.
If calculation is required, mention using the calculate_sum tool.
"""
    ).content

    return {
        "user_request": state["user_request"],
        "plan": plan,
        "tool_result": "",
        "final_answer": "",
        "validation": "",
        "retries": 0
    }


# =====================================================
# EXECUTOR NODE (USES TOOL)
# =====================================================

def executor_node(state: State) -> State:
    # Hard-coded for demo; can be made dynamic later
    a, b = 5, 7
    result = calculate_sum(a, b)

    final_answer = f"Computed result using tool evidence: {a} + {b} = {result}"

    return {
        **state,
        "tool_result": f"calculate_sum({a}, {b}) = {result}",
        "final_answer": final_answer,
    }


# =====================================================
# VALIDATOR NODE
# =====================================================

def validator_node(state: State) -> State:
    validation = llm.invoke(
        f"""
Validate the following result.

User request:
{state['user_request']}

Answer:
{state['final_answer']}

Reply ONLY with VALID or INVALID.
"""
    ).content.strip()

    return {
        **state,
        "validation": validation,
        "retries": state["retries"] + 1
    }


# =====================================================
# RETRY LOGIC
# =====================================================

MAX_RETRIES = 2

def retry_router(state: State):
    if "VALID" in state["validation"].upper():
        return END
    if state["retries"] >= MAX_RETRIES:
        return END
    return "executor"


# =====================================================
# BUILD LANGGRAPH
# =====================================================

graph = StateGraph(State)

graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("validator", validator_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "validator")

graph.add_conditional_edges(
    "validator",
    retry_router,
    {
        "executor": "executor",
        END: END,
    }
)

app = graph.compile()


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    output = app.invoke({
        "user_request": "Calculate the sum of 5 and 7"
    })

    print("\n--- PLAN ---")
    print(output["plan"])

    print("\n--- TOOL RESULT ---")
    print(output["tool_result"])

    print("\n--- FINAL ANSWER ---")
    print(output["final_answer"])

    print("\n--- VALIDATION ---")
    print(output["validation"])

    print("\n--- RETRIES ---")
    print(output["retries"])
``
