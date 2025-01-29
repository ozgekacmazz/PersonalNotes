import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Notes: React.FC = () => {
    const [notes, setNotes] = useState<
        { id: number; title: string; content: string; user_id: number; username: string }[]
    >([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [editMode, setEditMode] = useState(false);
    const [editNoteId, setEditNoteId] = useState<number | null>(null);
    const [currentUserId, setCurrentUserId] = useState<number | null>(null);

    // Kullanıcı ID'sini JWT'den çözümleyerek alın
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1])); // JWT payload kısmını çöz
                setCurrentUserId(Number(payload.sub)); // Kullanıcı ID'sini al
                console.log('Current User ID:', payload.sub);
            } catch (error) {
                console.error('Error parsing token:', error);
            }
        }
    }, []);

    // Notları yükle
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

    // Not ekle veya düzenle
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');

        if (editMode && editNoteId !== null) {
            try {
                await axios.put(
                    `http://localhost:5000/notes/${editNoteId}`,
                    { title, content },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert('Note updated successfully!');
                setEditMode(false);
                setEditNoteId(null);
                setTitle('');
                setContent('');
                fetchNotes(); // Notları yeniden yükle
            } catch (error) {
                console.error('Error updating note:', error);
            }
        } else {
            try {
                await axios.post(
                    'http://localhost:5000/notes/',
                    { title, content },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                alert('Note added successfully!');
                fetchNotes(); // Notları yeniden yükle
                setTitle('');
                setContent('');
            } catch (error) {
                console.error('Error adding note:', error);
            }
        }
    };

    // Not sil
    const handleDeleteNote = async (id: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/notes/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Note deleted successfully!');
            fetchNotes(); // Notları yeniden yükle
        } catch (error) {
            console.error('Error deleting note:', error);
        }
    };

    // Düzenleme başlat
    const handleEditNote = (note: { id: number; title: string; content: string }) => {
        setEditMode(true);
        setEditNoteId(note.id);
        setTitle(note.title);
        setContent(note.content);
    };

    return (
        <div className="container mt-5" style={{ backgroundColor: '#ffe4e1', padding: '20px', borderRadius: '10px' }}>
            <h2 className="text-center mb-4">Notes</h2>
            <form className="mb-4" onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="title" className="form-label">
                        Title
                    </label>
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
                    <label htmlFor="content" className="form-label">
                        Content
                    </label>
                    <textarea
                        id="content"
                        className="form-control"
                        placeholder="Enter note content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    {editMode ? 'Update Note' : 'Add Note'}
                </button>
                {editMode && (
                    <button
                        type="button"
                        className="btn btn-secondary ms-2"
                        onClick={() => {
                            setEditMode(false);
                            setEditNoteId(null);
                            setTitle('');
                            setContent('');
                        }}
                    >
                        Cancel
                    </button>
                )}
            </form>
            <h3>Your Notes</h3>
            <div className="row">
                {notes.map((note) => (
                    <div key={note.id} className="col-md-4">
                        <div
                            className="card mb-3"
                            style={{ backgroundColor: '#ba55d3', color: 'white', borderRadius: '10px' }}
                        >
                            <div className="card-body">
                                <h5 className="card-title">{note.title}</h5>
                                <p className="card-text">{note.content}</p>
                                <p className="card-text">
                                    <small>Created by: {note.username}</small>
                                </p>
                                {currentUserId === note.user_id && (
                                    <div>
                                        <button
                                            className="btn btn-warning btn-sm me-2"
                                            onClick={() => handleEditNote(note)}
                                        >
                                            Edit
                                        </button>
                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={() => handleDeleteNote(note.id)}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Notes;
