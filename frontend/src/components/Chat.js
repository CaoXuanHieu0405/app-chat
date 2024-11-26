import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom"; // Import useParams
import "./Chat.css";

const Chat = () => {
    const { roomName } = useParams(); // Lấy roomName từ URL
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState("");
    const socket = useRef(null);
    const navigate = useNavigate();

    // Kết nối WebSocket
    useEffect(() => {
        if (!roomName) {
            console.error("Room name is undefined!");
            return;
        }

        socket.current = new WebSocket(`ws://127.0.0.1:8080/ws/chat/${roomName}/`);

        socket.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prev) => [...prev, data.message]);
        };

        return () => {
            if (socket.current) {
                socket.current.close();
            }
        };
    }, [roomName]);

    // Gửi tin nhắn
    const sendMessage = () => {
        if (socket.current && message.trim()) {
            socket.current.send(JSON.stringify({ message }));
            setMessage("");
        }
    };

    return (
        <div className="container mt-5">
            <button className="btn btn-secondary mb-3" onClick={() => navigate("/dashboard")}>
                Back to Dashboard
            </button>
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <div className="card">
                        <div className="card-header text-center">
                            <h3>Chat Room: {roomName}</h3>
                        </div>
                        <div className="card-body chat-box">
                            <ul className="list-group">
                                {messages.map((msg, index) => (
                                    <li className="list-group-item" key={index}>
                                        {msg}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="card-footer">
                            <div className="input-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Enter message"
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                />
                                <button className="btn btn-primary" onClick={sendMessage}>
                                    Send
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chat;
