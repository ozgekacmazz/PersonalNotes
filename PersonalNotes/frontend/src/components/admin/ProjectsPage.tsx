import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const ProjectsPage: React.FC = () => {
    const [projects, setProjects] = useState<
        { id: number; name: string; description: string; title: string }[]
    >([]);
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [title, setTitle] = useState('');

    // Fetch projects
    const fetchProjects = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/admin/projects', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setProjects(response.data);
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
    };

    useEffect(() => {
        fetchProjects();
    }, []);

    // Add a new project
    const handleAddProject = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post(
                'http://localhost:5000/admin/projects',
                { name, description, title },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Project added successfully!');
            fetchProjects(); // Reload projects
            setName('');
            setDescription('');
            setTitle('');
        } catch (error) {
            console.error('Error adding project:', error);
        }
    };

    // Delete a project
    const handleDeleteProject = async (projectId: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/admin/projects/${projectId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Project deleted successfully!');
            fetchProjects(); // Reload projects
        } catch (error) {
            console.error('Error deleting project:', error);
        }
    };

    return (
        <div style={{ backgroundColor: '#ffe4e1', minHeight: '100vh', padding: '20px' }}>
            <div className="container mt-4">
                <h2 className="text-center text-dark mb-4">Projects</h2>
                <form onSubmit={handleAddProject} className="mb-4">
                    <div className="mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Project Name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>
                    {/* Add Project button */}
                    <button
                        type="submit"
                        className="btn w-100"
                        style={{ backgroundColor: '#6a0dad', color: 'white' }}
                    >
                        Add Project
                    </button>
                </form>
                <div className="row">
                    {projects.map((project) => (
                        <div key={project.id} className="col-md-4 mb-4">
                            <div className="card h-100 shadow-sm">
                                <div className="card-body">
                                    <h5 className="card-title text-dark">{project.name}</h5>
                                    <p className="card-text text-secondary">{project.description}</p>
                                    <p className="text-muted">Title: {project.title}</p>
                                    {/* Delete button */}
                                    <button
                                        className="btn btn-sm"
                                        style={{ backgroundColor: '#6a0dad', color: 'white' }}
                                        onClick={() => handleDeleteProject(project.id)}
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

export default ProjectsPage;
