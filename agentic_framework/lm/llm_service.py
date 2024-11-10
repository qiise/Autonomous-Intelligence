# lm/llm_service.py
import openai
import asyncio
import yaml
import json
from utils.logger import logger

class LLMService:
    def __init__(self, config_path='config/config.yaml'):
        self.config = self.load_config(config_path)
        self.api_key = self.config['api_keys']['openai']
        openai.api_key = self.api_key

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    async def generate_task_plan(self, query):
        try:
            prompt = f"""
            You are an intelligent orchestrator for a multi-agent AI system. Given a user query, generate a JSON task plan with the following structure:
            {{
                "tasks": [
                    {{
                        "agent_type": "AgentType",
                        "parameters": {{"param1": "value1", "param2": "value2"}}
                    }}
                ],
                "synthesis_instructions": "Instructions for synthesizing the response."
            }}
            The task plan should include all necessary agents to fulfill the query.

            Query: {query}

            Task Plan:
            """
            response = await openai.Completion.acreate(
                engine="gpt-4",
                prompt=prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.5,
            )
            task_plan_text = response.choices[0].text.strip()
            # Try to parse JSON
            try:
                task_plan = json.loads(task_plan_text)
                return task_plan
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse task plan JSON: {e}")
                return {"tasks": [], "synthesis_instructions": ""}
        except Exception as e:
            logger.error(f"LLM Service Error: {e}")
            return {"tasks": [], "synthesis_instructions": ""}
