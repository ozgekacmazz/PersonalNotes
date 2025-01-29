import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AdminSidebar from './AdminSidebar';
import NotesPage from './NotesPage';
import TasksPage from './TasksPage';
import UsersPage from './UsersPage';
import ProjectsPage from './ProjectsPage';
import AdminTags from './AdminTags';

const AdminPage: React.FC = () => {
    return (
        <div style={styles.container}>
            {/* Sidebar */}
            <div style={styles.sidebar}>
                <AdminSidebar />
            </div>
            {/* Main Content */}
            <div style={styles.content}>
                <div style={styles.innerContent}>
                    <div style={styles.header}>
                        <h1 style={styles.title}>Admin Dashboard</h1>
                        <p style={styles.description}>
                            Welcome to the Admin Panel! Manage notes, tasks, users, tags, and projects.
                        </p>
                    </div>
                    <div style={styles.routesContainer}>
                        <Routes>
                            <Route path="/notes" element={<NotesPage />} />
                            <Route path="/tasks" element={<TasksPage />} />
                            <Route path="/users" element={<UsersPage />} />
                            <Route path="/tags" element={<AdminTags />} />
                            <Route path="/projects" element={<ProjectsPage />} />
                        </Routes>
                    </div>
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        minHeight: '100vh',
        backgroundColor: '#ffe4e1',
    },
    sidebar: {
        width: '250px',
        backgroundColor: '#ba55d3',
        color: '#ffe4e1',
        padding: '20px',
        display: 'flex',
        flexDirection: 'column',
    },
    content: {
        flex: 1,
        display: 'flex',
        justifyContent: 'center', // Yatay ortalama
        alignItems: 'center',    // Dikey ortalama
        backgroundColor: '#ffffff',
        padding: '20px',
    },
    innerContent: {
        width: '100%',
        maxWidth: '800px', // İçeriğin genişliğini sınırlandır
        backgroundColor: '#fadadd', // Toz pembe
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        padding: '20px',
    },

    header: {
        marginBottom: '20px',
    },
    title: {
        fontSize: '24px',
        fontWeight: 'bold',
        color: '#34495e',
        textAlign: 'center',
    },
    description: {
        fontSize: '16px',
        color: '#7f8c8d',
        textAlign: 'center',
    },
    routesContainer: {
        marginTop: '20px',
    },
};

export default AdminPage;
