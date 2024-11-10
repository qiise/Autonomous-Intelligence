# main.py
import asyncio
import yaml
from agents.registry import agent_registry
from tools.search_api import SearchAPI
from lm.llm_service import LLMService
from orchestrator.orchestrator import Orchestrator
from utils.logger import logger
from memory.memory_manager import MemoryManager
from utils.rbac_manager import RBACManager
from utils.workflow_engine import load_workflow, WorkflowEngine

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

async def main():
    # Load configuration
    config = load_config('config/config.yaml')
    rbac_config = load_config('config/rbac.yaml')

    # Initialize tools
    tools = {}
    for tool_name, tool_class_path in config['tools'].items():
        module_name, class_name = tool_class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        tool_class = getattr(module, class_name)
        tools[tool_name] = tool_class()

    # Initialize agents with tools
    for agent_config in config['agents']:
        agent_name = agent_config['name']
        agent_class_path = agent_config['class']
        module_name, class_name = agent_class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        agent_class = getattr(module, class_name)
        agent_registry.register_agent(agent_name, agent_class)

    # Initialize memory manager and RBAC manager
    memory_manager = MemoryManager()
    await memory_manager.connect()
    rbac_manager = RBACManager('config/rbac.yaml')

    # Initialize orchestrator with tools, memory manager, and RBAC
    orchestrator = Orchestrator(agent_registry, tools, memory_manager, rbac_manager)

    # Example queries
    queries = [
        {"query": "Get the latest AI news and summarize it", "user_role": "user"},
        {"query": "Summarize recent AI breakthroughs and reach out to experts", "user_role": "admin"}
    ]

    for q in queries:
        logger.info(f"Processing query: '{q['query']}' with role '{q['user_role']}'")
        response = await orchestrator.process_query(q['query'], user_role=q['user_role'])
        logger.info(f"Response: {response}")
        print(f"Query: {q['query']}\nResponse:\n{response}\n{'-'*50}")

    # Example of executing a predefined workflow
    workflow = load_workflow('workflows/example_workflow.yaml')
    workflow_engine = WorkflowEngine(workflow)
    await workflow_engine.execute(orchestrator)

    # Retrieve and print workflow results from memory
    for step in workflow:
        step_key = f"step_{step['step']}"
        result = await memory_manager.retrieve(step_key)
        print(f"Result for {step_key}: {result}")

    # Close memory manager connection
    await memory_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
