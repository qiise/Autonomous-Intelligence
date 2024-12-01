# agents/crews/research_panacea.py

from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.agents.crews.panacea_base import PanaceaBase, panacea, task
from panacea_ai_framework.tasks.task import Task
from panacea_ai_framework.tools.custom_tool import MyCustomTool
from pydantic import BaseModel

class ResearchReport(BaseModel):
    """Research Report"""
    title: str
    body: str

@panacea
class ResearchPanacea(PanaceaBase):
    """Research Panacea"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @panacea.agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @panacea.agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @panacea.task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @panacea.task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_pydantic=ResearchReport
        )

    @panacea.crew
    def panacea(self) -> Crew:
        """Creates the Research Panacea"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
