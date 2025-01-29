import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Notes: React.FC = () => {
    const [notes, setNotes] = useState<{ id: number; title: string; content: string; username: string }[]>([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    // Notları getir
    const fetchNotes = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/notes/', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setNotes(response.data);
        } catch (error) {
            console.error('Error fetching notes:', error);
        }
    };

    useEffect(() => {
        fetchNotes();
    }, []);

    // Yeni not ekle
    const handleAddNote = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post(
                'http://localhost:5000/notes/',
                { title, content },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Note added successfully!');
            fetchNotes();
            setTitle('');
            setContent('');
        } catch (error) {
            console.error('Error adding note:', error);
            alert(error.response?.data?.message || 'Failed to add note.');
        }
    };

    // Notu sil
    const handleDeleteNote = async (id: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/admin/notes/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Note deleted successfully!');
            fetchNotes();
        } catch (error) {
            console.error('Error deleting note:', error);
            alert(error.response?.data?.message || 'Failed to delete note.');
        }
    };

    return (
        <div style={{ backgroundColor: '#ffe4e1', minHeight: '100vh', padding: '20px' }}>
            <div className="container mt-5">
                <h2 className="text-center mb-4">Notes</h2>
                <form onSubmit={handleAddNote} className="mb-4">
                    <div className="mb-3">
                        <label htmlFor="title" className="form-label">Title</label>
                        <input
                            type="text"
                            id="title"
                            className="form-control"
                            placeholder="Enter note title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="content" className="form-label">Content</label>
                        <textarea
                            id="content"
                            className="form-control"
                            placeholder="Enter note content"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            required
                        ></textarea>
                    </div>
                    {/* Mor buton */}
                    <button type="submit" className="btn" style={{ backgroundColor: '#6a0dad', color: 'white' }}>
                        Add Note
                    </button>
                </form>

                <h3 className="mb-3">All Notes</h3>
                <div className="row">
                    {notes.map((note) => (
                        <div key={note.id} className="col-md-4">
                            <div className="card mb-3">
                                <div className="card-body">
                                    <h5 className="card-title">{note.title}</h5>
                                    <p className="card-text">{note.content}</p>
                                    <p className="card-text">
                                        <small className="text-muted">Created by: {note.username}</small>
                                    </p>
                                    {/* Mor buton */}
                                    <button
                                        className="btn"
                                        style={{ backgroundColor: '#6a0dad', color: 'white' }}
                                        onClick={() => handleDeleteNote(note.id)}
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

export default Notes;
