rkdown
# Crews

A **Crew** is a group of Agents executing one or more Tasks in a coordinated manner.

## 1. Structure

Crews can be composed of:
- Multiple **Agents** (e.g., marketing agent, finance agent, research agent)
- One or more **Tasks** (e.g., "Conduct market research," "Prepare financial analysis")

## 2. Example Creation

```python
from anote_agents import Crew

team_crew = Crew(
    agents=[marketing_agent, finance_agent],
    tasks=[research_task, analysis_task],
    verbose=True
)

# Kick off the tasks
results = team_crew.kickoff(inputs={"industry": "Renewable Energy"})
```
Parameters
agents (list): Agents that can collaborate or work on different tasks.
tasks (list): Tasks, each assigned to a specific Agent.
verbose (bool): Enables additional logging.
3. Execution Flow
Initialization: The Crew binds each Task to the correct Agent.
kickoff: Passes input data (if any) into tasks that contain placeholders.
Orchestration: Tasks may run sequentially or in parallel, depending on workflow.
Results: The Crew collects outputs from each Task.
4. Key Benefits
Centralized management for complex multi-agent workflows.
Clear separation of responsibilities among Agents.
Reusability of Agents and Tasks across different Crews if desired.