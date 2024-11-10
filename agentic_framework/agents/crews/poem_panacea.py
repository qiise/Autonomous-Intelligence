# agents/crews/poem_panacea.py

from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.agents.crews.panacea_base import PanaceaBase, panacea, task
from panacea_ai_framework.tasks.task import Task
from pydantic import BaseModel

@panacea
class PoemPanacea(PanaceaBase):
    """Poem Panacea"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @panacea.agent
    def poem_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['poem_writer'],
            verbose=True
        )

    @panacea.task
    def write_poem(self) -> Task:
        return Task(
            config=self.tasks_config['write_poem'],
        )

    @panacea.crew
    def panacea(self) -> Crew:
        """Creates the Poem Panacea"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
