import React from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

const Dashboard = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        navigate("/");
    };

    const rooms = ["Room1", "Room2", "Room3"]; // Danh sách phòng chat mẫu

    return (
        <div className="container mt-5 dashboard-container">
            <h1>Welcome to Dashboard</h1>
            <p>Select a chat room to join:</p>
            <div className="list-group">
                {rooms.map((room, index) => (
                    <button
                        key={index}
                        className="list-group-item list-group-item-action"
                        onClick={() => navigate(`/chat/${room}`)} // Truyền roomName qua URL
                    >
                        {room}
                    </button>
                ))}
            </div>
            <button className="btn btn-danger mt-3" onClick={handleLogout}>
                Logout
            </button>
        </div>
    );
};

export default Dashboard;
