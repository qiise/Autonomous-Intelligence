# agents/base_agent.py

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union

from panacea_ai_framework.tools.base_tool import BaseTool
from panacea_ai_framework.lm.llm_service import LLM

class Agent(BaseModel):
    """Represents an agent in the Panacea system."""

    role: str
    goal: str
    backstory: str
    llm: Union[str, LLM, Any] = None
    tools: Optional[List[BaseTool]] = Field(default_factory=list)
    verbose: bool = False

    def execute_task(
        self,
        task: "Task",
        context: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
    ) -> str:
        """Execute a given task using the agent's LLM and tools."""
        # Implement task execution logic using the LLM
        # For example:
        prompt = f"{self.backstory}\nTask: {task.description}\nContext: {context}\n"
        if tools:
            for tool in tools:
                prompt += f"Tool {tool.name}: {tool.description}\n"
        response = self.llm.call([{"role": "user", "content": prompt}])
        return response
