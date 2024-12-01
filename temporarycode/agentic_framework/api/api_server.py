# api/api_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from orchestrator.orchestrator import Orchestrator
from utils.logger import logger
from utils.cache_manager import CacheManager
from memory.memory_manager import MemoryManager
from utils.rbac_manager import RBACManager
from agents.registry import agent_registry
from tools.search_api import SearchAPI
from lm.llm_service import LLMService
import yaml

app = FastAPI()

# Load configurations
def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Initialize tools
tools = {}
for tool_name, tool_class_path in config['tools'].items():
    module_name, class_name = tool_class_path.rsplit('.', 1)
    module = __import__(module_name, fromlist=[class_name])
    tool_class = getattr(module, class_name)
    tools[tool_name] = tool_class()

# Initialize memory manager and RBAC manager
memory_manager = MemoryManager()
cache_manager = CacheManager()
rbac_manager = RBACManager('config/rbac.yaml')

# Initialize orchestrator
orchestrator = Orchestrator(agent_registry, tools, memory_manager, rbac_manager)

# Pydantic model for request
class QueryRequest(BaseModel):
    query: str
    user_role: str = 'user'

@app.on_event("startup")
async def startup_event():
    await memory_manager.connect()
    logger.info("API server started and memory manager connected.")

@app.on_event("shutdown")
async def shutdown_event():
    await memory_manager.close()
    logger.info("API server shutdown and memory manager disconnected.")

@app.post("/process_query/")
async def process_query(request: QueryRequest):
    query = request.query
    user_role = request.user_role
    try:
        response = await orchestrator.process_query(query, user_role=user_role)
        return {"query": query, "response": response}
    except Exception as e:
        logger.error(f"Error processing query '{query}': {e}")
        raise HTTPException(status_code=500, detail=str(e))
