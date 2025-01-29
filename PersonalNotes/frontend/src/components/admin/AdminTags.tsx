import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminTags: React.FC = () => {
    const [tags, setTags] = useState<{ id: number; name: string }[]>([]);
    const [tagName, setTagName] = useState('');
    const [editingTagId, setEditingTagId] = useState<number | null>(null);

    const fetchTags = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await axios.get('http://localhost:5000/tags/admin/tags', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setTags(response.data);
        } catch (error) {
            console.error('Error fetching tags:', error);
        }
    };

    useEffect(() => {
        fetchTags();
    }, []);

    const handleAddTag = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        try {
            await axios.post(
                'http://localhost:5000/tags/admin/tags',
                { name: tagName },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Tag added successfully!');
            setTagName('');
            fetchTags();
        } catch (error) {
            console.error('Error adding tag:', error);
        }
    };

    const handleEditTag = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!editingTagId) return;
        const token = localStorage.getItem('token');
        try {
            await axios.put(
                `http://localhost:5000/tags/admin/tags/${editingTagId}`,
                { name: tagName },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert('Tag updated successfully!');
            setTagName('');
            setEditingTagId(null);
            fetchTags();
        } catch (error) {
            console.error('Error updating tag:', error);
        }
    };

    const handleDeleteTag = async (id: number) => {
        const token = localStorage.getItem('token');
        try {
            await axios.delete(`http://localhost:5000/tags/admin/tags/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert('Tag deleted successfully!');
            fetchTags();
        } catch (error) {
            console.error('Error deleting tag:', error);
        }
    };

    const startEditing = (tag: { id: number; name: string }) => {
        setEditingTagId(tag.id);
        setTagName(tag.name);
    };

    return (
        <div style={{ backgroundColor: '#ffe4e1', minHeight: '100vh', padding: '20px' }}>
            <div className="container">
                <h2 className="text-center mb-4"> Manage Tags</h2>
                <form
                    onSubmit={editingTagId ? handleEditTag : handleAddTag}
                    className="d-flex justify-content-center align-items-center mb-4"
                >
                    <input
                        type="text"
                        placeholder="Tag Name"
                        value={tagName}
                        onChange={(e) => setTagName(e.target.value)}
                        required
                        className="form-control me-2"
                    />
                    <button
                        type="submit"
                        className="btn"
                        style={{
                            backgroundColor: editingTagId ? '#4b0082' : '#6a0dad',
                            color: 'white',
                        }}
                    >
                        {editingTagId ? 'Update Tag' : 'Add Tag'}
                    </button>
                    {editingTagId && (
                        <button
                            type="button"
                            onClick={() => {
                                setEditingTagId(null);
                                setTagName('');
                            }}
                            className="btn btn-secondary ms-2"
                        >
                            Cancel
                        </button>
                    )}
                </form>
                <ul className="list-group">
                    {tags.map((tag) => (
                        <li
                            key={tag.id}
                            className="list-group-item d-flex justify-content-between align-items-center"
                        >
                            <span>{tag.name}</span>
                            <div>
                                <button
                                    onClick={() => startEditing(tag)}
                                    className="btn btn-sm me-2"
                                    style={{
                                        backgroundColor: '#4b0082', // Koyu mor
                                        color: 'white',
                                    }}
                                >
                                    Edit
                                </button>
                                <button
                                    onClick={() => handleDeleteTag(tag.id)}
                                    className="btn btn-sm"
                                    style={{
                                        backgroundColor: '#dda0dd', // Açık mor
                                        color: 'white',
                                    }}
                                >
                                    Delete
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default AdminTags;
