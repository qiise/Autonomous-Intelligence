# Panacea

## Overview

The Agentic AI Framework enables the creation and orchestration of modular AI agents to perform complex tasks through collaboration. It leverages Large Language Models (LLMs) for dynamic task planning and supports features like asynchronous execution, persistent memory, role-based access control (RBAC), and API integration.

## Directory Structure
```
agentic_ai_framework/
├── README.md
├── main.py
├── config/
│   ├── config.yaml
│   └── rbac.yaml
├── agents/
│   ├── init.py
│   ├── base_agent.py
│   ├── registry.py
│   ├── search_agent.py
│   ├── analysis_agent.py
│   └── communication_agent.py
├── orchestrator/
│   ├── init.py
│   └── orchestrator.py
├── lm/
│   ├── init.py
│   └── llm_service.py
├── tools/
│   ├── init.py
│   └── search_api.py
├── utils/
│   ├── init.py
│   ├── response_synthesizer.py
│   ├── logger.py
│   ├── cache_manager.py
│   ├── workflow_engine.py
│   └── rbac_manager.py
├── memory/
│   ├── init.py
│   └── memory_manager.py
├── api/
│   ├── init.py
│   └── api_server.py
├── workflows/
│   └── example_workflow.yaml
├── docs/
│   └── setup_guide.md
├── tests/
│   ├── init.py
│   └── test_framework.py
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- `pip` package manager

## Installation

#### Clone the Repository
```
git clone [(https://github.com/nv78/Panacea)](https://github.com/nv78/Panacea)
cd agentic_ai_framework
```
#### Create a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```
#### Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```
#### Configure the Framework

```
OpenAI API Key: Replace "your_openai_api_key_here" in config/config.yaml with your actual OpenAI API key.
Search API: Update the search API endpoint in tools/search_api.py with a real API if available.
```

#### Initialize the Database

The MemoryManager uses SQLite by default, which requires no additional setup. It will create a memory.db file upon first run.

## Running the Framework
a. Running the Main Script
Execute main.py to process example queries and workflows.

```
python3 main.py
```

b. Running the API Server
Start the FastAPI server to expose the framework via API endpoints.

```
uvicorn api.api_server:app --reload
```
Access the interactive API documentation at http://127.0.0.1:8000/docs.

#### Using the API
Endpoint: /process_query/
Method: POST

Payload:

```
{
  "query": "Your natural language query here",
  "user_role": "user"  // or "admin"
}
```
Response:

```
{
  "query": "Your natural language query here",
  "response": "Final synthesized response from agents."
}
```

## Adding New Agents

#### Create a New Agent Class

In the agents/ directory, create a new Python file, e.g., new_agent.py.

```
# agents/new_agent.py
from .base_agent import Agent
import asyncio

class NewAgent(Agent):
    async def perform_task(self, task):
        # Implement task logic here
        parameter = task["parameters"].get("param", "")
        result = f"NewAgent processed parameter: '{parameter}'"
        return result
```
#### Register the New Agent

Update agents/registry.py to include the new agent.

```
# agents/registry.py
from .search_agent import SearchAgent
from .analysis_agent import AnalysisAgent
from .communication_agent import CommunicationAgent
from .new_agent import NewAgent  # Import new agent

class AgentRegistry:
    def __init__(self):
        self.registry = {}

    def register_agent(self, agent_name, agent_class):
        self.registry[agent_name] = agent_class

    def get_agent(self, agent_name):
        agent_class = self.registry.get(agent_name)
        if agent_class:
            return agent_class()
        else:
            raise ValueError(f"Agent '{agent_name}' not found in registry.")

# Initialize and register agents
agent_registry = AgentRegistry()
agent_registry.register_agent('SearchAgent', SearchAgent)
agent_registry.register_agent('AnalysisAgent', AnalysisAgent)
agent_registry.register_agent('CommunicationAgent', CommunicationAgent)
agent_registry.register_agent('NewAgent', NewAgent)  # Register new agent
```
#### Update Configuration

Add the new agent to config/config.yaml.

```
# config/config.yaml
agents:
  - name: SearchAgent
    class: agents.search_agent.SearchAgent
  - name: AnalysisAgent
    class: agents.analysis_agent.AnalysisAgent
  - name: CommunicationAgent
    class: agents.communication_agent.CommunicationAgent
  - name: NewAgent
    class: agents.new_agent.NewAgent
```
You can now utilize NewAgent in your queries or define steps in workflows that invoke it.

#### Testing the Framework

Run tests using pytest:

```
pytest
```
Ensure that all tests pass to verify the integrity of the framework.
