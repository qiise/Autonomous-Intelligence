# agents/registry.py
from .search_agent import SearchAgent
from .analysis_agent import AnalysisAgent
from .communication_agent import CommunicationAgent

class AgentRegistry:
    def __init__(self):
        self.registry = {}

    def register_agent(self, agent_name, agent_class):
        self.registry[agent_name] = agent_class

    def get_agent(self, agent_name):
        agent_class = self.registry.get(agent_name)
        if agent_class:
            return agent_class()
        else:
            raise ValueError(f"Agent '{agent_name}' not found in registry.")

# Initialize and register agents
agent_registry = AgentRegistry()
agent_registry.register_agent('SearchAgent', SearchAgent)
agent_registry.register_agent('AnalysisAgent', AnalysisAgent)
agent_registry.register_agent('CommunicationAgent', CommunicationAgent)
