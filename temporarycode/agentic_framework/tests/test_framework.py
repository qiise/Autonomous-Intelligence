# # tests/test_framework.py
# import pytest
# import asyncio
# from agents.registry import agent_registry
# from tools.search_api import SearchAPI
# from lm.llm_service import LLMService
# from orchestrator.orchestrator import Orchestrator
# from memory.memory_manager import MemoryManager
# from utils.rbac_manager import RBACManager

# @pytest.fixture
# async def setup_orchestrator():
#     # Load configuration
#     config = {
#         'agents': [
#             {"name": "SearchAgent", "class": "agents.search_agent.SearchAgent"},
#             {"name": "AnalysisAgent", "class": "agents.analysis_agent.AnalysisAgent"},
#             {"name": "CommunicationAgent", "class": "agents.communication_agent.CommunicationAgent"}
#         ],
#         'tools': {
#             "search_api": SearchAPI(),
#             "language_model": LLMService(config_path='config/config.yaml')
#         }
#     }
#     rbac_manager = RBACManager('config/rbac.yaml')
#     memory_manager = MemoryManager(':memory:')
#     await memory_manager.connect()
#     orchestrator = Orchestrator(agent_registry, config['tools'], memory_manager, rbac_manager)
#     return orchestrator

# @pytest.mark.asyncio
# async def test_process_query(setup_orchestrator):
#     orchestrator = setup_orchestrator
#     query = "Get the latest AI news and summarize it"
#     response = await orchestrator.process_query(query, user_role='user')
#     assert "SearchAgent" in response
#     assert "AnalysisAgent" in response
#     assert "Summary of content" in response

# tests/test_framework.py

import unittest
from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.tasks.task import Task
from panacea_ai_framework.crews.crew import Crew
from panacea_ai_framework.tools.custom_tool import MyCustomTool
from panacea_ai_framework.lm.llm_service import LLM

class TestAgentExecution(unittest.TestCase):

    def setUp(self):
        self.llm = LLM(model="gpt-4o-mini")
        self.agent = Agent(
            role="AI Researcher",
            goal="Uncover cutting-edge developments in AI",
            backstory="You're a seasoned researcher with expertise in AI.",
            llm=self.llm,
            verbose=True
        )
        self.tool = MyCustomTool()
        self.agent.tools.append(self.tool)

    def test_task_execution(self):
        task = Task(
            description="Research the latest in AI",
            expected_output="A summary of recent AI developments.",
            agent=self.agent
        )
        result = task.execute()
        self.assertIsInstance(result, str)
        self.assertIn("AI", result)

class TestCrewExecution(unittest.TestCase):

    def setUp(self):
        self.llm = LLM(model="gpt-4o-mini")
        self.agent1 = Agent(
            role="AI Researcher",
            goal="Uncover cutting-edge developments in AI",
            backstory="You're a seasoned researcher with expertise in AI.",
            llm=self.llm,
            verbose=True
        )
        self.agent2 = Agent(
            role="AI Reporting Analyst",
            goal="Create detailed reports based on AI data analysis and research findings",
            backstory="You're a meticulous analyst specializing in AI reports.",
            llm=self.llm,
            verbose=True
        )
        self.task1 = Task(
            description="Research the latest in AI",
            expected_output="A summary of recent AI developments.",
            agent=self.agent1
        )
        self.task2 = Task(
            description="Compile the research into a report",
            expected_output="A comprehensive AI research report.",
            agent=self.agent2
        )
        self.crew = Crew(
            agents=[self.agent1, self.agent2],
            tasks=[self.task1, self.task2],
            process="sequential",
            verbose=True
        )

    def test_crew_kickoff(self):
        inputs = {"context": "AI advancements in 2024"}
        results = self.crew.kickoff(inputs=inputs)
        self.assertIsInstance(results, dict)
        self.assertIn(self.task1.description, results)
        self.assertIn(self.task2.description, results)

if __name__ == '__main__':
    unittest.main()
