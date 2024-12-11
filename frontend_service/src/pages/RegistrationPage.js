import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BackendAPI } from '../api';

const RegistrationPage = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        passwordRepeat: '',
        group_name: 'User',
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.password !== formData.passwordRepeat) {
            setError('Passwords do not match.');
            return;
        }

        const { passwordRepeat, ...dataToSubmit } = formData;

        try {
            await BackendAPI.post('auth/users/', dataToSubmit);
            navigate('/login');
        } catch (err) {
            setError('Registration failed. Please try again.');
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <div className="container mt-5">
            <h2>Registration</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input
                        type="email"
                        name="email"
                        className="form-control"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input
                        type="password"
                        name="password"
                        className="form-control"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Repeat Password</label>
                    <input
                        type="password"
                        name="passwordRepeat"
                        className="form-control"
                        value={formData.passwordRepeat}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Group</label>
                    <select
                        name="group_name"
                        className="form-select"
                        value={formData.group_name}
                        onChange={handleChange}
                    >
                        <option value="User">User</option>
                        <option value="Tenant">Tenant</option>
                    </select>
                </div>
                <button type="submit" className="btn btn-success">
                    Register
                </button>
            </form>
        </div>
    );
};

export default RegistrationPage;
