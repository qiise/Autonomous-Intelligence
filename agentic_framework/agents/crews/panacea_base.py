# agents/crews/panacea_base.py

from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Type

from panacea_ai_framework.agents.base_agent import Agent
from panacea_ai_framework.tasks.task import Task
from panacea_ai_framework.lm.llm_service import LLM
from panacea_ai_framework.tools.custom_tool import MyCustomTool

class PanaceaBase(BaseModel):
    """Base class for Panacea crews."""
    pass
