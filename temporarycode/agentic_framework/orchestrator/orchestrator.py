# orchestrator/orchestrator.py
import asyncio
from utils.response_synthesizer import synthesize_response
from utils.logger import logger
from utils.cache_manager import CacheManager
from utils.workflow_engine import load_workflow, WorkflowEngine
from memory.memory_manager import MemoryManager
from utils.rbac_manager import RBACManager

class Orchestrator:
    def __init__(self, agent_registry, tools, memory_manager, rbac_manager):
        """
        Initialize the orchestrator with agent registry, tools, memory manager, and RBAC manager.
        :param agent_registry: An instance of AgentRegistry.
        :param tools: A dictionary of tool instances.
        :param memory_manager: An instance of MemoryManager.
        :param rbac_manager: An instance of RBACManager.
        """
        self.agent_registry = agent_registry
        self.tools = tools
        self.memory_manager = memory_manager
        self.rbac_manager = rbac_manager
        self.cache_manager = CacheManager()

    async def execute_task(self, task, user_role='user'):
        agent_type = task.get("agent_type")
        parameters = task.get("parameters", {})

        # RBAC: Check if the agent is allowed for the user role
        if not self.rbac_manager.is_agent_allowed(user_role, agent_type):
            logger.warning(f"User role '{user_role}' is not permitted to use agent '{agent_type}'.")
            return f"Access denied for agent '{agent_type}'."

        # Check cache first
        cache_key = f"{agent_type}_{str(parameters)}"
        cached_result = self.cache_manager.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for key '{cache_key}'.")
            return cached_result

        try:
            agent = self.agent_registry.get_agent(agent_type)
            agent.tools = self.tools  # Inject tools into the agent
            result = await agent.perform_task(task)
            # Store result in cache
            self.cache_manager.set(cache_key, result)
            # Store result in memory
            await self.memory_manager.store(agent_type, result)
            return result
        except Exception as e:
            logger.error(f"Error executing agent '{agent_type}': {e}")
            return f"Error executing agent '{agent_type}': {e}"

    async def process_query(self, query, user_role='user'):
        """
        Process a user query end-to-end.
        :param query: The user's natural language query.
        :param user_role: The role of the user making the query.
        :return: Final synthesized response.
        """
        logger.info(f"Processing query: '{query}' with user role '{user_role}'")

        # Check cache for the entire query
        cached_response = self.cache_manager.get(query)
        if cached_response:
            logger.info(f"Cache hit for query '{query}'.")
            return cached_response

        try:
            task_plan = await self.tools['language_model'].generate_task_plan(query)
            tasks = task_plan.get("tasks", [])
            synthesis_instructions = task_plan.get("synthesis_instructions", "")
            results = {}

            # Execute tasks asynchronously
            task_coroutines = [
                self.execute_task(task, user_role=user_role) for task in tasks
            ]
            task_results = await asyncio.gather(*task_coroutines)
            for task, result in zip(tasks, task_results):
                agent_type = task.get("agent_type")
                results[agent_type] = result

            final_response = synthesize_response(results)

            # Store final response in cache
            self.cache_manager.set(query, final_response)

            logger.info(f"Final response for query '{query}': {final_response}")
            return final_response

        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
            return f"Error processing query: {e}"
