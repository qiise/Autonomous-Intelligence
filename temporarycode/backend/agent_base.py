import openai
import json
import logging
import asyncio
from tools import WebSearchTool

class AgentBase:
    def __init__(self, config):
        self.name = config.get('Agent Name', 'Unnamed Agent')
        self.model = config.get('Model', 'gpt-3.5-turbo')
        self.system_prompt = config.get('System Prompt', '')
        task_data = config.get('Task', {})
        self.task_description = task_data.get('Task Description', '')
        self.subtasks = task_data.get('Subtasks', [])
        self.examples = self.parse_examples(task_data.get('Examples', ''))
        self.files_uploaded = task_data.get('Files Uploaded', [])
        self.tools = config.get('Tools', [])
        output_data = config.get('Output', {})
        self.output_format = output_data.get('Format', 'PlainText')
        self.output_content = output_data.get('Content', [])
        self.initialize_tools()

    def parse_examples(self, examples):
        # Assuming examples is a list of dictionaries
        return examples

    def initialize_tools(self):
        self.tool_instances = {}
        for tool in self.tools:
            if tool.lower() == 'web_search':
                self.tool_instances['web_search'] = WebSearchTool()
            # Initialize other tools as needed

    async def execute(self, inputs):
        prompt = self.prepare_prompt(inputs)
        response = await self.call_model(prompt)
        outputs = self.process_response(response)
        # Log the outputs at the agent level
        logging.info(f"Agent '{self.name}' outputs: {outputs}")
        return outputs

    def prepare_prompt(self, inputs):
        prompt = f"{self.system_prompt}\n\nTask: {self.task_description}\n"
        if inputs:
            for key, value in inputs.items():
                prompt += f"\n{key.capitalize()}: {value}\n"
        if self.examples:
            prompt += "\nExamples:\n"
            for example in self.examples:
                prompt += f"Input: {example['input']}\nOutput: {example['output']}\n"
        return prompt

    async def call_model(self, prompt):
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
            )
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Error calling model for agent {self.name}: {e}")
            raise e

    def process_response(self, response):
        if self.output_format.lower() == 'json':
            try:
                output_data = json.loads(response)
                return output_data
            except json.JSONDecodeError:
                logging.error(f"Agent {self.name} expected JSON output but failed to parse.")
                raise
        else:
            return response

    def get_config(self):
        # Return the agent's configuration (for the API)
        return {
            'Agent Name': self.name,
            'Model': self.model,
            'System Prompt': self.system_prompt,
            'Task': {
                'Task Description': self.task_description,
                'Subtasks': self.subtasks,
                'Examples': self.examples,
                'Files Uploaded': self.files_uploaded
            },
            'Tools': self.tools,
            'Output': {
                'Format': self.output_format,
                'Content': self.output_content
            }
        }

    def update_config(self, new_config):
        # Update the agent's configuration with new values
        self.__init__(new_config)
