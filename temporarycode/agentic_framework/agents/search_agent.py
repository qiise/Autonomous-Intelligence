# agents/search_agent.py
from .base_agent import Agent
import asyncio

class SearchAgent(Agent):
    async def perform_task(self, task):
        keywords = task["parameters"].get("keywords", "")
        search_tool = self.tools.get('search_api')
        if search_tool:
            try:
                results = await search_tool.search(keywords)
                return results
            except Exception as e:
                return f"Error during search: {e}"
        else:
            return "Search tool not available."
