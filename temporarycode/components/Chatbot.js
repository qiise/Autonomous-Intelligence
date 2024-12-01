// import React, { useState } from 'react';

// function Chatbot() {
//   const [messages, setMessages] = useState([]);
//   const [inputText, setInputText] = useState('');

//   const sendMessage = async () => {
//     if (inputText.trim() === '') return;

//     const userMessage = { sender: 'user', text: inputText };
//     setMessages([...messages, userMessage]);

//     // Call backend API
//     const response = await fetch('http://localhost:5000/api/chat', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ message: inputText }),
//     });
//     const data = await response.json();

//     const botMessage = { sender: 'bot', text: data.reply };
//     setMessages((msgs) => [...msgs, botMessage]);
//     setInputText('');
//   };

//   return (
//     <div className="flex flex-col h-screen">
//         <h2 className="text-xl font-bold mb-4">Chat</h2>
//       <div className="flex-1 p-4 overflow-y-auto">
//         {messages.map((msg, idx) => (
//           <div key={idx} className={`mb-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
//             <span className={`inline-block px-4 py-2 rounded-lg ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
//               {msg.text}
//             </span>
//           </div>
//         ))}
//       </div>
//       <div className="p-4 flex">
//         <input
//           className="flex-1 border rounded-l-lg p-2"
//           type="text"
//           value={inputText}
//           onChange={(e) => setInputText(e.target.value)}
//           onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
//         />
//         <button className="bg-blue-500 text-white px-4 py-2 rounded-r-lg" onClick={sendMessage}>
//           Send
//         </button>
//       </div>
//     </div>
//   );
// }

// export default Chatbot;

import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [logs, setLogs] = useState('');
  const [activeAgent, setActiveAgent] = useState('');

  useEffect(() => {
    // Set up WebSocket connection for real-time logs
    const socket = io('http://localhost:5000');
    socket.on('log', (msg) => {
      setLogs((prevLogs) => prevLogs + '\n' + msg.data);
    });
    return () => socket.disconnect();
  }, []);

  const sendMessage = async () => {
    if (inputText.trim() === '') return;

    const userMessage = { sender: 'user', text: inputText };
    setMessages([...messages, userMessage]);
    setActiveAgent('Processing...');

    // Call backend API
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: inputText }),
    });
    const data = await response.json();

    const botMessage = { sender: 'bot', text: data.reply };
    setMessages((msgs) => [...msgs, botMessage]);
    setInputText('');
    setActiveAgent('');
  };

  return (
    <div className="flex">
      <div className="flex-1 flex flex-col h-screen">
        <div className="flex-1 p-4 overflow-y-auto">
          {messages.map((msg, idx) => (
            <div key={idx} className={`mb-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}>
              <span className={`inline-block px-4 py-2 rounded-lg ${msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>
                {msg.text}
              </span>
            </div>
          ))}
        </div>
        <div className="p-4 flex">
          <input
            className="flex-1 border rounded-l-lg p-2"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded-r-lg" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
      <div className="w-1/3 border-l p-4 overflow-y-auto">
        <h3 className="font-bold mb-2">Active Agent: {activeAgent}</h3>
        <h3 className="font-bold mb-2">Logs</h3>
        <pre className="text-sm">{logs}</pre>
      </div>
    </div>
  );
}

export default Chatbot;
