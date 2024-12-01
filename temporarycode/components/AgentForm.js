import React, { useState } from 'react';

function AgentForm({ onSave }) {
  const [agentConfig, setAgentConfig] = useState({
    'Agent Name': '',
    'Model': 'gpt-3.5-turbo',
    'System Prompt': '',
    'Task': {
      'Task Description': '',
      'Subtasks': [],
    },
    'Tools': [],
    'Output': {
      'Format': 'PlainText',
    },
  });

  const handleConfigChange = (field, value) => {
    setAgentConfig({ ...agentConfig, [field]: value });
  };

  const handleTaskChange = (field, value) => {
    setAgentConfig({
      ...agentConfig,
      Task: { ...agentConfig.Task, [field]: value },
    });
  };

  const handleSubtasksChange = (index, value) => {
    const newSubtasks = [...agentConfig.Task.Subtasks];
    newSubtasks[index] = value;
    setAgentConfig({
      ...agentConfig,
      Task: { ...agentConfig.Task, Subtasks: newSubtasks },
    });
  };

  const addSubtask = () => {
    setAgentConfig({
      ...agentConfig,
      Task: { ...agentConfig.Task, Subtasks: [...agentConfig.Task.Subtasks, ''] },
    });
  };

  const handleToolsChange = (index, value) => {
    const newTools = [...agentConfig.Tools];
    newTools[index] = value;
    setAgentConfig({ ...agentConfig, Tools: newTools });
  };

  const addTool = () => {
    setAgentConfig({ ...agentConfig, Tools: [...agentConfig.Tools, ''] });
  };

  const saveAgent = () => {
    onSave(agentConfig);
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Create New Agent</h2>
      <div className="mb-4">
        <label className="block font-bold mb-2">Agent Name</label>
        <input
          className="w-full border p-2"
          value={agentConfig['Agent Name']}
          onChange={(e) => handleConfigChange('Agent Name', e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">Model</label>
        <input
          className="w-full border p-2"
          value={agentConfig['Model']}
          onChange={(e) => handleConfigChange('Model', e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">System Prompt</label>
        <textarea
          className="w-full border p-2"
          value={agentConfig['System Prompt']}
          onChange={(e) => handleConfigChange('System Prompt', e.target.value)}
        ></textarea>
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">Task Description</label>
        <textarea
          className="w-full border p-2"
          value={agentConfig.Task['Task Description']}
          onChange={(e) => handleTaskChange('Task Description', e.target.value)}
        ></textarea>
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">Subtasks</label>
        {agentConfig.Task.Subtasks.map((subtask, index) => (
          <input
            key={index}
            className="w-full border p-2 mb-2"
            value={subtask}
            onChange={(e) => handleSubtasksChange(index, e.target.value)}
          />
        ))}
        <button className="bg-gray-300 px-2 py-1" onClick={addSubtask}>
          Add Subtask
        </button>
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">Tools</label>
        {agentConfig.Tools.map((tool, index) => (
          <input
            key={index}
            className="w-full border p-2 mb-2"
            value={tool}
            onChange={(e) => handleToolsChange(index, e.target.value)}
          />
        ))}
        <button className="bg-gray-300 px-2 py-1" onClick={addTool}>
          Add Tool
        </button>
      </div>
      <div className="mb-4">
        <label className="block font-bold mb-2">Output Format</label>
        <input
          className="w-full border p-2"
          value={agentConfig.Output['Format']}
          onChange={(e) => setAgentConfig({ ...agentConfig, Output: { 'Format': e.target.value } })}
        />
      </div>
      <button className="bg-blue-500 text-white px-4 py-2" onClick={saveAgent}>
        Save Agent
      </button>
    </div>
  );
}

export default AgentForm;
