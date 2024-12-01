from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging
import asyncio
from orchestrator import Orchestrator
import os
from utils import workflow_config_to_markdown, agent_config_to_markdown

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket support

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent_framework.log"),
        logging.StreamHandler()
    ]
)

# Create a custom logging handler to emit logs via WebSocket
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        socketio.emit('log', {'data': msg})

# Add the custom handler to the root logger
socket_handler = SocketIOHandler()
socket_handler.setLevel(logging.INFO)
logging.getLogger('').addHandler(socket_handler)

# Initialize the orchestrator
orchestrator = Orchestrator('examples/workflows/sample_workflow.json')
import json

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    # Process the message using the orchestrator
    response = asyncio.run(process_chat_message(message))
    return jsonify({'reply': response})

async def process_chat_message(message):
    initial_input = {'user_message': message}
    final_output = await orchestrator.run(initial_input)
    return final_output.get('reply', 'Sorry, I did not understand that.')


@app.route('/api/agents/<agent_name>', methods=['GET'])
def get_agent(agent_name):
    agent_config = orchestrator.get_agent_config(agent_name)
    if agent_config:
        return jsonify(agent_config)
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get a list of available agents."""
    agent_files = os.listdir('agents/')
    agents = [file.split('.json')[0] for file in agent_files if file.endswith('.json')]
    return jsonify({'agents': agents})


@app.route('/api/agents/<agent_name>', methods=['POST'])
def update_agent(agent_name):
    data = request.get_json()
    success = orchestrator.update_agent_config(agent_name, data)
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Failed to update agent'}), 400

@app.route('/api/workflows/<workflow_name>/execute', methods=['POST'])
def execute_workflow(workflow_name):
    data = request.get_json()
    initial_input = data.get('input', {})
    workflow = orchestrator.get_workflow(workflow_name)
    if workflow:
        final_output = asyncio.run(orchestrator.run_workflow(workflow, initial_input))
        return jsonify({'output': final_output})
    else:
        return jsonify({'error': 'Workflow not found'}), 404

@app.route('/api/logs', methods=['GET'])
def get_logs():
    with open('agent_framework.log', 'r') as f:
        logs = f.read()
    return jsonify({'logs': logs})

@app.route('/api/agents', methods=['POST'])
def create_agent():
    """Create a new agent and save its configuration."""
    data = request.get_json()
    agent_name = data.get('agent_name')
    if not agent_name:
        return jsonify({'error': 'Agent name is required'}), 400
    file_path = f"agents/{agent_name}.json"
    save_json(file_path, data)
    logging.info(f"Agent '{agent_name}' saved.")
    return jsonify({'status': 'success', 'message': f"Agent '{agent_name}' saved."})

@app.route('/api/workflows', methods=['POST'])
def create_workflow():
    data = request.get_json()
    workflow_name = data.get('workflow_name')
    if not workflow_name:
        return jsonify({'error': 'Workflow name is required'}), 400
    file_path = f"workflows/{workflow_name}.json"
    save_json(file_path, data)
    return jsonify({'status': 'success', 'message': f"Workflow '{workflow_name}' saved."})


# Add functions to save agents and workflows
def save_agent_markdown(file_path, agent_config):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(agent_config_to_markdown(agent_config))

def save_workflow_markdown(file_path, workflow_config):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(workflow_config_to_markdown(workflow_config))


if __name__ == '__main__':
    # Set the OpenAI API key
    import openai
    # openai.api_key = "add key"
    app.run(debug=True)
