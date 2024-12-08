import React, { useEffect, useState } from 'react';

const SocketComponent = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    let socket;

    useEffect(() => {
        // Initialize WebSocket connection
        socket = new WebSocket('ws://localhost:5000');

        // Handle incoming messages
        socket.onmessage = (event) => {
            console.log('Message from server:', event.data);
            setMessages((prevMessages) => [...prevMessages, event.data]);
        };

        // Handle connection errors
        socket.onerror = (error) => {
            console.error('WebSocket Error:', error);
        };

        // Cleanup on component unmount
        return () => {
            if (socket) {
                socket.close();
            }
        };
    }, []);

    // Send message to WebSocket server
    const sendMessage = () => {
        if (socket && input.trim()) {
            socket.send(input);
            setInput('');
        }
    };

    return (
        <div>
            <h2>WebSocket Demo</h2>
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

export default SocketComponent;
