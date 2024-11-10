# tools/custom_tool.py

from panacea_ai_framework.tools.base_tool import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "MyCustomTool"
    description: str = (
        "Processes input arguments to generate meaningful outputs."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implement your tool's functionality here
        return f"Processed argument: {argument}"
