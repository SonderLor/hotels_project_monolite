import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LogoutPage = () => {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/login');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <div className="container text-center mt-5">
            <h2>Are you sure you want to log out?</h2>
            <button className="btn btn-danger me-2" onClick={handleLogout}>
                Yes, log out
            </button>
            <button className="btn btn-secondary" onClick={() => navigate(-1)}>
                Cancel
            </button>
        </div>
    );
};

export default LogoutPage;
