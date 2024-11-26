import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Dashboard from "./components/Dashboard";
import Chat from "./components/Chat";

const App = () => {
    const [isAuth, setAuth] = useState(false);

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login setAuth={setAuth} />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={isAuth ? <Dashboard /> : <Login setAuth={setAuth} />} />
                <Route path="/chat/:roomName" element={isAuth ? <Chat /> : <Login setAuth={setAuth} />} />
            </Routes>
        </Router>
    );
};

export default App;
