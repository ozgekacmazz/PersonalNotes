import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminTasks: React.FC = () => {
    const [tasks, setTasks] = useState<
        { id: number; title: string; description: string; project_name: string; tag_name: string; assigned_by: string }[]
    >([]);

    // Görevleri yükle
    const fetchTasks = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/admin/tasks', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setTasks(response.data);
        } catch (error) {
            console.error('Error fetching tasks:', error);
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    // Görev silme işlemi
    const handleDeleteTask = async (id: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/admin/tasks/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Task deleted successfully!');
            fetchTasks(); // Görevleri yeniden yükle
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    };

    return (
        <div style={{ backgroundColor: '#ffe4e1', minHeight: '100vh', padding: '20px', color: 'black' }}>
            <h2 className="text-center mb-4">Tasks</h2>
            <h3 className="mb-3">All Tasks</h3>
            <div className="row">
                {tasks.map((task) => (
                    <div key={task.id} className="col-md-4">
                        <div
                            className="card mb-3"
                            style={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }}
                        >
                            <div className="card-body">
                                <h4 className="card-title">{task.title}</h4>
                                <p className="card-text">{task.description}</p>
                                <p className="card-text">
                                    <strong>Project:</strong> {task.project_name || 'No Project'}
                                </p>
                                <p className="card-text">
                                    <strong>Tag:</strong> {task.tag_name || 'No Tags'}
                                </p>
                                <p className="card-text">
                                    <strong>Assigned by:</strong> {task.assigned_by}
                                </p>
                                <button
                                    onClick={() => handleDeleteTask(task.id)}
                                    style={styles.deleteButton}
                                    className="btn btn-danger"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const styles = {
    deleteButton: {
        backgroundColor: '#ba55d3',
        color: '#ffffff',
        border: 'none',
        padding: '10px 15px',
        cursor: 'pointer',
        borderRadius: '5px',
        width: '100%',
    },
};

export default AdminTasks;
