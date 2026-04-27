# langgraph-task-automation-agent

# AI Task Automation Agent (LangGraph)
A production-style agentic AI workflow that plans tasks, executes actions using tools, validates results, and retries automatically on failure.

## Why this project?
Most LLM applications respond to prompts but do not behave like reliable systems.
This project demonstrates how to convert LLM reasoning into a controlled execution workflow with:
- explicit planning
- tool-based execution
- output validation
- automatic retry logic

``
## Architecture
START
 → Planner
 → Executor (uses tools)
 → Validator
   → VALID → END
   → INVALID → Retry Executor
   
## What this project demonstrates
- Planner–Executor–Validator pattern
- Tool-driven execution (Python functions)
- Validation before trusting AI output
- Retry logic for self-healing workflows
- Deterministic AI system design using LangGraph

## Example
Input:
"Calculate the sum of 5 and 7"

Flow:
Planner → identifies calculation
Executor → calls calculate_sum tool
Validator → verifies correctness
Final validated result returned

## Tech Stack
- Python
- LangGraph
- Groq LLM
``
