import React, { useState, useEffect } from 'react';
import socket from '../services/socket';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Listen for incoming messages
    socket.on('chat_message', (data) => {
      setMessages((prevMessages) => [...prevMessages, data.message]);
    });

    return () => {
      socket.off('chat_message'); // Clean up on component unmount
    };
  }, []);

  const sendMessage = () => {
    if (message.trim()) {
      socket.emit('chat_message', { message });
      setMessage(''); // Clear the input field
    }
  };

  return (
    <div>
      <h2>Real-Time Chat</h2>
      <div style={{ border: '1px solid black', padding: '10px', height: '300px', overflowY: 'scroll' }}>
        {messages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default Chat;
