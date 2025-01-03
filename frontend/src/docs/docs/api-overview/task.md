## 3. `api-overview/task.md`

# Tasks

A **Task** is a discrete assignment or job for an Agent to execute. Tasks contain:
- A description of the work
- Expected output
- Optional input requirements
- References to Tools or data

## 1. Basic Task Definition

```python
from anote_agents import Task

data_analysis_task = Task(
    description="Analyze historical sales data for the past 3 years",
    expected_output="A summary of key sales trends, plus any anomalies found.",
    human_input=False,
    agent=None  # Agent can be assigned later
)
```

Parameters
description (str): What the Task requires.
expected_output (str): Clarifies the form or content of the result.
human_input (bool): If True, indicates user must provide input (e.g., a prompt).
output_json (Optional Pydantic model): Validates output structure.
output_file (Optional str): Saves the Agent’s result to a file.
agent (Agent): The Agent responsible for executing this Task.
2. Examples of Task Usage
Scheduling: “Find the best meeting times with {participant_count} participants.”
Research: “Gather references on quantum computing breakthroughs since 2020.”
3. Tips
Use placeholders ({placeholder_name}) in description to dynamically inject input data at runtime.
If using structured outputs, define a Pydantic model in output_json for validation and type safety.