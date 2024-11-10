# agents/base_agent.py
import asyncio

class Agent:
    def __init__(self, tools=None):
        self.tools = tools or {}

    async def perform_task(self, task):
        """
        Perform the assigned task. This method should be overridden by subclasses.
        :param task: A dictionary containing task details and parameters.
        :return: Result of the task execution.
        """
        raise NotImplementedError("Subclasses should implement this method.")
