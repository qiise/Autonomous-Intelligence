import React, { useState, useEffect } from 'react';
import AgentForm from './AgentForm';

function AgentUI() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentConfig, setAgentConfig] = useState(null);
  const [creatingAgent, setCreatingAgent] = useState(false);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch('/api/agents');
      if (!response.ok) throw new Error('Failed to fetch agents');
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Error fetching agents:', error);
      setAgents([]);
    }
  };

  const selectAgent = async (agentName) => {
    setCreatingAgent(false);
    setSelectedAgent(agentName);
    try {
      const response = await fetch(`/api/agents/${agentName}`);
      if (!response.ok) throw new Error('Failed to fetch agent details');
      const data = await response.json();
      setAgentConfig(data);
    } catch (error) {
      console.error('Error selecting agent:', error);
      setAgentConfig(null);
    }
  };

  const handleConfigChange = (field, value, isTaskField = false) => {
    if (isTaskField) {
      setAgentConfig({
        ...agentConfig,
        Task: { ...agentConfig?.Task, [field]: value },
      });
    } else {
      setAgentConfig({ ...agentConfig, [field]: value });
    }
  };

  const saveAgentConfig = async (newAgentConfig) => {
    try {
      const response = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAgentConfig),
      });
      if (!response.ok) throw new Error('Failed to save agent configuration');
      alert('Agent configuration saved successfully.');
      setCreatingAgent(false);
      fetchAgents();
    } catch (error) {
      console.error('Error saving agent configuration:', error);
      alert('Failed to save agent configuration.');
    }
  };

  const createAgent = () => {
    setCreatingAgent(true);
    setSelectedAgent(null);
    setAgentConfig({
      'Agent Name': '',
      'System Prompt': '',
      'Task': {
        'Task Description': '',
        Subtasks: [],
      },
      Tools: [],
      Output: { Format: '' },
    });
  };

  return (
    <div className="flex">
      <div className="w-1/3 border-r p-4">
        <h2 className="text-xl font-bold mb-4">Agents</h2>
        <button
          className="bg-green-500 text-white px-4 py-2 mb-4"
          onClick={createAgent}
        >
          Create New Agent
        </button>
        <ul>
          {agents.length > 0 ? (
            agents.map((agent, index) => (
              <li key={agent || index} className="mb-2">
                <button
                  className="text-blue-500"
                  onClick={() => selectAgent(agent)}
                >
                  {agent}
                </button>
              </li>
            ))
          ) : (
            <p className="text-gray-500">No agents found. Create one to get started!</p>
          )}
        </ul>
      </div>
      <div className="w-2/3 p-4">
        {creatingAgent && (
          <AgentForm
            onSave={(newAgentConfig) => saveAgentConfig(newAgentConfig)}
          />
        )}
        {agentConfig && !creatingAgent && (
          <div>
            <h2 className="text-xl font-bold mb-4">{selectedAgent}</h2>
            <div className="mb-4">
              <label className="block font-bold mb-2">Agent Name</label>
              <input
                name="Agent Name"
                className="w-full border p-2"
                value={agentConfig['Agent Name'] || ''}
                onChange={(e) =>
                  handleConfigChange('Agent Name', e.target.value)
                }
              />
            </div>
            <div className="mb-4">
              <label className="block font-bold mb-2">System Prompt</label>
              <textarea
                name="System Prompt"
                className="w-full border p-2"
                value={agentConfig['System Prompt'] || ''}
                onChange={(e) =>
                  handleConfigChange('System Prompt', e.target.value)
                }
              ></textarea>
            </div>
            <div className="mb-4">
              <label className="block font-bold mb-2">Task Description</label>
              <textarea
                name="Task Description"
                className="w-full border p-2"
                value={agentConfig.Task?.['Task Description'] || ''}
                onChange={(e) =>
                  handleConfigChange('Task Description', e.target.value, true)
                }
              ></textarea>
            </div>
            <button
              className="bg-blue-500 text-white px-4 py-2"
              onClick={() => saveAgentConfig(agentConfig)}
            >
              Save Configuration
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default AgentUI;
