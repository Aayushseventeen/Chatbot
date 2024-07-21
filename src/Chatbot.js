// src/Chatbot.js
import React, { useState } from 'react';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim()) {
            const newMessage = { sender: 'user', text: input };
            setMessages([...messages, newMessage]);
            setInput('');

            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            });

            const data = await response.json();
            setMessages([...messages, newMessage, { sender: 'bot', text: data.response }]);
        }
    };

    return (
        <div className="chatbot">
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Chatbot;
