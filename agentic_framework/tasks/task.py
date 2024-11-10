# tasks/task.py

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Type, Union

from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.tools.base_tool import BaseTool

class Task(BaseModel):
    """Defines a task to be executed by an agent."""

    description: str
    expected_output: str
    agent: Optional[Agent] = None
    tools: Optional[List[BaseTool]] = Field(default_factory=list)
    async_execution: bool = False
    output_pydantic: Optional[Type[BaseModel]] = None
    output_json: Optional[Dict[str, Any]] = None
    output_file: Optional[str] = None

    def execute(self, context: Optional[str] = None) -> Any:
        """Execute the task using the assigned agent."""
        if not self.agent:
            raise ValueError("No agent assigned to execute this task.")
        return self.agent.execute_task(task=self, context=context, tools=self.tools)
