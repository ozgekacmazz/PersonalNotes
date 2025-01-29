import React, { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Notes from '../components/dashboard/Notes';
import Tasks from '../components/dashboard/Tasks';
import Sidebar from '../components/dashboard/Sidebar';

const DashboardPage: React.FC = () => {
    const [isAdmin, setIsAdmin] = useState<boolean>(false);

    useEffect(() => {
        const checkAdminStatus = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error('Token bulunamadı');
                return;
            }

            try {
                const response = await axios.get('http://localhost:5000/admin/check-admin', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                console.log('Admin durumu:', response.data.is_admin);
                setIsAdmin(response.data.is_admin);
            } catch (error: any) {
                console.error('Admin kontrolü hatası:', error.response?.data || error);
            }
        };

        checkAdminStatus();
    }, []);

    return (
        <div className="d-flex justify-content-center align-items-center" style={styles.container}>
            <div className="row w-100" style={styles.dashboardWrapper}>
                {/* Sidebar */}
                <div className="col-md-3 p-4" style={styles.sidebar}>
                    <Sidebar isAdmin={isAdmin} />
                </div>
                {/* Content */}
                <div className="col-md-9 p-4 d-flex flex-column justify-content-center align-items-center" style={styles.content}>
                    <h1 style={styles.motivationalText}>Dream it, plan it, and make it happen.</h1>
                    <p style={styles.subtitle}>Your Dashboard at a glance: Simplify, track, and achieve!</p>
                    <Routes>
                        <Route path="/dashboard/notes" element={<Notes />} />
                        <Route path="/dashboard/tasks" element={<Tasks />} />
                    </Routes>
                </div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        minHeight: '100vh',
        backgroundColor: '#ffe4e1', // Açık pembe arka plan
    },
    dashboardWrapper: {
        maxWidth: '1200px',
        margin: 'auto',
        borderRadius: '12px',
        boxShadow: '0 6px 8px rgba(0, 0, 0, 0.1)',
        overflow: 'hidden',
    },
    sidebar: {
        backgroundColor: '#fadadd', // Toz pembe sidebar
        color: 'black',
        borderRight: '2px solid #ba55d3', // Açık mor kenar
        borderRadius: '8px 0 0 8px',
    },
    content: {
        backgroundColor: '#ba55d3', // İçerik kısmı açık mor
        color: 'white',
        borderRadius: '0 8px 8px 0',
        textAlign: 'center' as const,
    },
    motivationalText: {
        fontSize: '2rem',
        fontWeight: 'bold' as const,
        color: 'white',
        marginBottom: '1rem',
    },
    subtitle: {
        fontSize: '1rem',
        color: '#white',
        marginBottom: '2rem',
    },
};

export default DashboardPage;
