import React, { useEffect, useState } from 'react';
import socket from '../services/socket';

const WebSocketDemo = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    // Listen for responses from the server
    socket.on('response', (data) => {
      setMessages((prevMessages) => [...prevMessages, data.data]);
    });

    return () => {
      socket.off('response'); // Clean up listener on component unmount
    };
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      socket.emit('message', input); // Send message to the server
      setInput(''); // Clear input field
    }
  };

  return (
    <div>
      <h2>WebSocket Communication</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '200px', overflowY: 'scroll' }}>
        {messages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default WebSocketDemo;
