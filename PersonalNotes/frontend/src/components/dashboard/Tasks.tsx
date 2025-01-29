import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Tasks: React.FC = () => {
    const [tasks, setTasks] = useState<
        { id: number; title: string; description: string; project_name: string; tag_name: string }[]
    >([]);
    const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
    const [tags, setTags] = useState<{ id: number; name: string }[]>([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [projectId, setProjectId] = useState<number | null>(null);
    const [selectedTags, setSelectedTags] = useState<number[]>([]);
    const [currentTaskId, setCurrentTaskId] = useState<number | null>(null);

    useEffect(() => {
        fetchTasks();
        fetchProjects();
        fetchTags();
    }, []);

    const fetchTasks = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/tasks/', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setTasks(response.data);
        } catch (error) {
            console.error('Error fetching tasks:', error);
        }
    };

    const fetchProjects = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/projects/', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setProjects(response.data);
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
    };

    const fetchTags = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/tags/', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setTags(response.data);
        } catch (error) {
            console.error('Error fetching tags:', error);
        }
    };

    const handleAddOrUpdateTask = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            if (currentTaskId) {
                await axios.put(
                    `http://localhost:5000/tasks/${currentTaskId}`,
                    {
                        title,
                        description,
                        project_id: projectId,
                        tags_id: selectedTags,
                    },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert('Task updated successfully!');
            } else {
                await axios.post(
                    'http://localhost:5000/tasks/',
                    {
                        title,
                        description,
                        project_id: projectId,
                        tags_id: selectedTags,
                    },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert('Task added successfully!');
            }
            fetchTasks();
            resetForm();
        } catch (error) {
            console.error('Error adding/updating task:', error);
        }
    };

    const handleDeleteTask = async (taskId: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/tasks/${taskId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Task deleted successfully!');
            fetchTasks();
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    };

    const resetForm = () => {
        setCurrentTaskId(null);
        setTitle('');
        setDescription('');
        setProjectId(null);
        setSelectedTags([]);
    };

    const startEditing = (task: {
        id: number;
        title: string;
        description: string;
        project_name: string;
        tag_name: string;
    }) => {
        setCurrentTaskId(task.id);
        setTitle(task.title);
        setDescription(task.description);
        setProjectId(Number(task.project_name));
        setSelectedTags([]); // Tags güncellenebilir
    };

    return (
        <div
            className="container mt-5"
            style={{
                backgroundColor: '#ffe4e1', // Açık pembe arka plan
                padding: '20px',
                borderRadius: '10px',
            }}
        >
            <h2 className="text-center mb-4">Tasks</h2>
            <form onSubmit={handleAddOrUpdateTask} className="mb-5">
                <div className="mb-3">
                    <label htmlFor="title" className="form-label">
                        Title
                    </label>
                    <input
                        type="text"
                        id="title"
                        className="form-control"
                        placeholder="Enter task title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="description" className="form-label">
                        Description
                    </label>
                    <textarea
                        id="description"
                        className="form-control"
                        placeholder="Enter task description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="project" className="form-label">
                        Select Project
                    </label>
                    <select
                        id="project"
                        className="form-select"
                        value={projectId || ''}
                        onChange={(e) => setProjectId(Number(e.target.value))}
                        required
                    >
                        <option value="" disabled>
                            Select Project
                        </option>
                        {projects.map((project) => (
                            <option key={project.id} value={project.id}>
                                {project.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="tags" className="form-label">
                        Select Tags
                    </label>
                    <select
                        id="tags"
                        className="form-select"
                        multiple
                        value={selectedTags}
                        onChange={(e) =>
                            setSelectedTags(Array.from(e.target.selectedOptions, (option) => Number(option.value)))
                        }
                    >
                        {tags.map((tag) => (
                            <option key={tag.id} value={tag.id}>
                                {tag.name}
                            </option>
                        ))}
                    </select>
                </div>
                <button type="submit" className="btn btn-primary">
                    {currentTaskId ? 'Update Task' : 'Add Task'}
                </button>
            </form>
            <div className="row">
                {tasks.map((task) => (
                    <div key={task.id} className="col-md-4">
                        <div
                            className="card mb-3"
                            style={{ backgroundColor: '#ba55d3', color: '#fff', borderRadius: '10px' }}
                        >
                            <div className="card-body">
                                <h5 className="card-title">{task.title}</h5>
                                <p className="card-text">{task.description}</p>
                                <p className="card-text">
                                    <small>Project: {task.project_name}</small>
                                </p>
                                <p className="card-text">
                                    <small>Tags: {task.tag_name || 'No tags'}</small>
                                </p>
                                <button
                                    className="btn btn-sm me-2"
                                    style={{ backgroundColor: '#4b0082', color: 'white' }}
                                    onClick={() => startEditing(task)}
                                >
                                    Edit
                                </button>
                                <button
                                    className="btn btn-sm"
                                    style={{ backgroundColor: '#dda0dd', color: 'white' }}
                                    onClick={() => handleDeleteTask(task.id)}
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

export default Tasks;
