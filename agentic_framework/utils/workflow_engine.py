# utils/workflow_engine.py
import yaml
import asyncio
from utils.logger import logger

def load_workflow(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

class WorkflowEngine:
    def __init__(self, workflow):
        self.workflow = workflow

    async def execute(self, orchestrator):
        # Sort the workflow steps by 'step' to ensure order
        sorted_workflow = sorted(self.workflow, key=lambda x: x['step'])
        for step in sorted_workflow:
            dependencies = step.get('depends_on', [])
            if dependencies:
                for dep in dependencies:
                    dep_key = f"step_{dep}"
                    dep_result = await orchestrator.memory_manager.retrieve(dep_key)
                    if not dep_result:
                        logger.error(f"Dependency step {dep} not met for step {step['step']}.")
                        continue
            agent_type = step['agent']
            parameters = step.get('parameters', {})
            task = {
                "agent_type": agent_type,
                "parameters": parameters
            }
            result = await orchestrator.execute_task(task)
            await orchestrator.memory_manager.store(f"step_{step['step']}", result)
            logger.info(f"Executed step {step['step']} with agent '{agent_type}'. Result: {result}")
