// import React, { useState, useEffect } from 'react';
// import ReactFlow, { addEdge, MiniMap, Controls } from 'react-flow-renderer';

// function WorkflowEditor() {
//   const [elements, setElements] = useState([]);
//   const [workflowName, setWorkflowName] = useState('');
//   const [agents, setAgents] = useState([]);

//   useEffect(() => {
//     fetchWorkflow();
//     fetchAgents();
//   }, []);

//   const fetchWorkflow = async () => {
//     // Fetch the workflow configuration from the backend
//     const response = await fetch('/api/workflows/Sample_Workflow');
//     const data = await response.json();
//     if (data.workflow) {
//       setWorkflowName(data.workflow.workflow_name);
//       // Process the workflow data to create nodes and edges
//       const newElements = [];
//       data.workflow.agents.forEach((agent, index) => {
//         newElements.push({
//           id: agent.agent_name,
//           type: 'default',
//           data: { label: agent.agent_name },
//           position: { x: 250 * index, y: 100 },
//         });
//       });
//       data.workflow.execution_flow.forEach((step) => {
//         // Assuming linear flow for simplicity
//         newElements.push({
//           id: `e${step.agent}`,
//           source: step.inputs[0],
//           target: step.agent,
//           animated: true,
//         });
//       });
//       setElements(newElements);
//     }
//   };

//   const fetchAgents = async () => {
//     const response = await fetch('/api/agents');
//     const data = await response.json();
//     setAgents(data.agents);
//   };

//   const onElementsRemove = (elementsToRemove) => {
//     setElements((els) => els.filter((el) => !elementsToRemove.includes(el)));
//   };

//   const onConnect = (params) => setElements((els) => addEdge(params, els));

//   return (
//     <div style={{ height: '80vh' }}>
//       <h2 className="text-xl font-bold mb-4">Workflow Editor: {workflowName}</h2>
//       <ReactFlow elements={elements} onElementsRemove={onElementsRemove} onConnect={onConnect}>
//         <MiniMap />
//         <Controls />
//       </ReactFlow>
//       {/* Add functionality to save the workflow */}
//     </div>
//   );
// }

// export default WorkflowEditor;

import React, { useState, useEffect } from 'react';
import ReactFlow, { addEdge, MiniMap, Controls } from 'react-flow-renderer';

function WorkflowEditor() {
  const [elements, setElements] = useState([]);
  const [workflowName, setWorkflowName] = useState('Sample_Workflow');
  const [agents, setAgents] = useState([]);
  const [workflowConfig, setWorkflowConfig] = useState(null);

  useEffect(() => {
    fetchAgents();
    fetchWorkflow(workflowName);
  }, []);

  const fetchAgents = async () => {
    const response = await fetch('/api/agents');
    const data = await response.json();
    setAgents(data.agents);
  };

  const fetchWorkflow = async (name) => {
    const response = await fetch(`/api/workflows/${name}`);
    const data = await response.json();
    if (data.workflow) {
      setWorkflowConfig(data.workflow);
      // Process the workflow data to create nodes and edges
      const newElements = [];
      data.workflow.agents.forEach((agent, index) => {
        newElements.push({
          id: agent.agent_name,
          type: 'default',
          data: { label: agent.agent_name },
          position: { x: 250 * index, y: 100 },
        });
      });
      data.workflow.execution_flow.forEach((step, index) => {
        newElements.push({
          id: `e${index}`,
          source: step.inputs[0] === 'user_input' ? 'user_input' : step.inputs[0],
          target: step.agent,
          animated: true,
        });
      });
      setElements(newElements);
    } else {
      // Handle workflow not found
    }
  };

  const onElementsRemove = (elementsToRemove) => {
    setElements((els) => els.filter((el) => !elementsToRemove.includes(el)));
  };

  const onConnect = (params) => setElements((els) => addEdge(params, els));

  const saveWorkflow = async () => {
    // Convert elements back to workflow configuration
    const workflow = {
      workflow_name: workflowName,
      agents: agents.map((agentName) => ({
        agent_name: agentName,
        config_path: `agents/${agentName}.md`,
      })),
      execution_flow: elements
        .filter((el) => el.source && el.target)
        .map((el, index) => ({
          step_name: `Step ${index + 1}`,
          agent: el.target,
          inputs: [el.source],
          outputs: [`Output_${el.target}`],
        })),
    };

    const response = await fetch('/api/workflows', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workflow),
    });
    const data = await response.json();
    if (data.status === 'success') {
      alert('Workflow saved successfully.');
    } else {
      alert('Failed to save workflow.');
    }
  };

  return (
    <div style={{ height: '80vh' }}>
      <h2 className="text-xl font-bold mb-4">Workflow Editor: {workflowName}</h2>
      <ReactFlow elements={elements} onElementsRemove={onElementsRemove} onConnect={onConnect}>
        <MiniMap />
        <Controls />
      </ReactFlow>
      <button className="bg-blue-500 text-white px-4 py-2 mt-4" onClick={saveWorkflow}>
        Save Workflow
      </button>
    </div>
  );
}

export default WorkflowEditor;
