import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const AdminUsers: React.FC = () => {
    const [users, setUsers] = useState<{ id: number; username: string; role: string }[]>([]);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('user');

    // Fetch all users
    const fetchAllUsers = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/admin/users', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    useEffect(() => {
        fetchAllUsers();
    }, []);

    // Add user
    const handleAddUser = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post(
                'http://localhost:5000/admin/users',
                { username, password, role },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('User added successfully!');
            fetchAllUsers();
            setUsername('');
            setPassword('');
            setRole('user');
        } catch (error) {
            console.error('Error adding user:', error);
        }
    };

    // Delete user
    const handleDeleteUser = async (id: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/admin/users/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('User deleted successfully!');
            fetchAllUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    return (
        <div style={{ backgroundColor: '#ffe4e1', minHeight: '100vh', padding: '20px' }}>
            <div className="container mt-5">
                <h2 className="text-center text-dark mb-4">Users</h2>
                <form onSubmit={handleAddUser} className="mb-4">
                    <div className="mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <input
                            type="password"
                            className="form-control"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <select
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            className="form-select"
                            required
                        >
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>
                    <button
                        type="submit"
                        className="btn w-100"
                        style={{ backgroundColor: '#6a0dad', color: 'white' }}
                    >
                        Add User
                    </button>
                </form>
                <div className="row">
                    {users.map((user) => (
                        <div key={user.id} className="col-md-4 mb-4">
                            <div className="card shadow-sm border-0">
                                <div className="card-body bg-light">
                                    <h5 className="card-title text-dark">{user.username}</h5>
                                    <p className="card-text">
                                        <strong>Role:</strong> <span className="text-secondary">{user.role}</span>
                                    </p>
                                    <button
                                        className="btn"
                                        style={{ backgroundColor: '#6a0dad', color: 'white' }}
                                        onClick={() => handleDeleteUser(user.id)}
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdminUsers;
