# tests/test_framework.py
import pytest
import asyncio
from agents.registry import agent_registry
from tools.search_api import SearchAPI
from lm.llm_service import LLMService
from orchestrator.orchestrator import Orchestrator
from memory.memory_manager import MemoryManager
from utils.rbac_manager import RBACManager

@pytest.fixture
async def setup_orchestrator():
    # Load configuration
    config = {
        'agents': [
            {"name": "SearchAgent", "class": "agents.search_agent.SearchAgent"},
            {"name": "AnalysisAgent", "class": "agents.analysis_agent.AnalysisAgent"},
            {"name": "CommunicationAgent", "class": "agents.communication_agent.CommunicationAgent"}
        ],
        'tools': {
            "search_api": SearchAPI(),
            "language_model": LLMService(config_path='config/config.yaml')
        }
    }
    rbac_manager = RBACManager('config/rbac.yaml')
    memory_manager = MemoryManager(':memory:')
    await memory_manager.connect()
    orchestrator = Orchestrator(agent_registry, config['tools'], memory_manager, rbac_manager)
    return orchestrator

@pytest.mark.asyncio
async def test_process_query(setup_orchestrator):
    orchestrator = setup_orchestrator
    query = "Get the latest AI news and summarize it"
    response = await orchestrator.process_query(query, user_role='user')
    assert "SearchAgent" in response
    assert "AnalysisAgent" in response
    assert "Summary of content" in response
