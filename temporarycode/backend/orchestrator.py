import os
import asyncio
import logging
from agent_base import AgentBase
from utils import parse_agent_markdown, parse_workflow_markdown, load_json

class Orchestrator:
    def __init__(self, workflow_config_path):
        self.workflow = self.load_workflow(workflow_config_path)
        self.agents = self.initialize_agents()
        self.data_store = {}  # Stores outputs from agents

    def load_agents(self):
        # Re-initialize agents based on the updated workflow
        self.agents = self.initialize_agents()

    # def load_workflow(self, config_path):
    #     workflow = parse_workflow_markdown(config_path)
    #     if 'agents' not in workflow:
    #         raise KeyError("'agents' section is missing from the workflow configuration")
    #     logging.info(f"Workflow '{workflow['workflow_name']}' loaded with agents: {[agent['agent_name'] for agent in workflow['agents']]}")
    #     return workflow

    def load_workflow(self, config_path):
        workflow = load_json(config_path)
        if 'workflow_name' not in workflow:
            raise KeyError("Workflow configuration missing 'workflow_name'.")
        if 'agents' not in workflow or not isinstance(workflow['agents'], list):
            raise KeyError("Workflow configuration missing or invalid 'agents' section.")
        if 'execution_flow' not in workflow or not isinstance(workflow['execution_flow'], list):
            raise KeyError("Workflow configuration missing or invalid 'execution_flow' section.")
        return workflow

    def initialize_agents(self):
        agents = {}
        for agent_info in self.workflow['agents']:
            config_path = agent_info.get('config_path')
            if not config_path:
                raise ValueError(f"Agent configuration missing 'config_path': {agent_info}")
            agent_config = load_json(config_path)
            agent = AgentBase(agent_config)
            agents[agent_info['agent_name']] = agent
        return agents

    # def initialize_agents(self):
    #     agents = {}
    #     for agent_info in self.workflow['agents']:
    #         config_path = agent_info['config_path']
    #         config = parse_agent_markdown(config_path)
    #         agent = AgentBase(config)
    #         agents[agent_info['agent_name']] = agent
    #     return agents

    async def run(self, initial_input):
        self.data_store['user_input'] = initial_input
        for step in self.workflow['execution_flow']:
            if step.get('parallel', False):
                tasks = []
                for parallel_step in step['steps']:
                    tasks.append(self.execute_step(parallel_step))
                await asyncio.gather(*tasks)
            else:
                await self.execute_step(step)
        final_output = self.collect_final_output()
        return final_output

    async def execute_step(self, step):
        try:
            agent_name = step['agent']
            agent = self.agents[agent_name]
            inputs = self.collect_inputs(step['inputs'])
            logging.info(f"Step: {step['step_name']} - Agent: {agent_name} - Inputs: {inputs}")
            outputs = await agent.execute(inputs)
            logging.info(f"Step: {step['step_name']} - Outputs: {outputs}")
            self.store_outputs(step['outputs'], outputs)
        except Exception as e:
            logging.error(f"Error executing step '{step['step_name']}': {e}")

    def collect_inputs(self, input_sources):
        inputs = {}
        for source in input_sources:
            if source == 'user_input':
                inputs.update(self.data_store['user_input'])
            else:
                inputs.update(self.data_store.get(source, {}))
        return inputs

    def store_outputs(self, destinations, outputs):
        for dest in destinations:
            self.data_store[dest] = outputs

    def collect_final_output(self):
        return self.data_store.get('Final_Output', {})

    def get_next_step(self, current_step):
        # Determine the next step based on the current step
        execution_flow = self.workflow['execution_flow']
        current_index = execution_flow.index(current_step)
        if current_index + 1 < len(execution_flow):
            next_step = execution_flow[current_index + 1]
            return next_step['step_name']
        else:
            return 'Workflow completed.'

    def get_agent_list(self):
        return list(self.agents.keys())

    def get_agent_config(self, agent_name):
        agent = self.agents.get(agent_name)
        if agent:
            return agent.get_config()
        else:
            return None

    def update_agent_config(self, agent_name, new_config):
        agent = self.agents.get(agent_name)
        if agent:
            agent.update_config(new_config)
            return True
        else:
            return False

    def get_workflow(self, workflow_name):
        if self.workflow['workflow_name'] == workflow_name:
            return self.workflow
        else:
            return None

    async def run_workflow(self, workflow, initial_input):
        self.workflow = workflow
        self.agents = self.initialize_agents()
        self.data_store = {}
        return await self.run(initial_input)
