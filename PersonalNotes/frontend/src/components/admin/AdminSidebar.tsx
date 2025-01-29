import React from 'react';
import { Link } from 'react-router-dom';

const AdminSidebar: React.FC = () => {
    return (
        <div>
            <h2 style={styles.title}>Admin Panel</h2>
            <ul style={styles.navList}>
                <li style={styles.navItem}>
                    <Link to="/admin/notes" style={styles.navLink}>
                        <i className="fas fa-sticky-note" style={styles.icon}></i> Notes
                    </Link>
                </li>
                <li style={styles.navItem}>
                    <Link to="/admin/tasks" style={styles.navLink}>
                        <i className="fas fa-tasks" style={styles.icon}></i> Tasks
                    </Link>
                </li>
                <li style={styles.navItem}>
                    <Link to="/admin/users" style={styles.navLink}>
                        <i className="fas fa-users" style={styles.icon}></i> Users
                    </Link>
                </li>
                <li style={styles.navItem}>
                    <Link to="/admin/tags" style={styles.navLink}>
                        <i className="fas fa-tags" style={styles.icon}></i> Tags
                    </Link>
                </li>
                <li style={styles.navItem}>
                    <Link to="/admin/projects" style={styles.navLink}>
                        <i className="fas fa-project-diagram" style={styles.icon}></i> Projects
                    </Link>
                </li>
            </ul>
        </div>
    );
};

const styles = {
    title: {
        color: '#ecf0f1',
        marginBottom: '20px',
        textAlign: 'center',
        fontSize: '20px',
        fontWeight: 'bold',
    },
    navList: {
        listStyle: 'none',
        padding: 0,
    },
    navItem: {
        marginBottom: '15px',
    },
    navLink: {
        textDecoration: 'none',
        color: '#ecf0f1',
        fontSize: '16px',
        display: 'flex',
        alignItems: 'center',
        padding: '10px',
        borderRadius: '5px',
        transition: 'background-color 0.3s',
    },
    navLinkHover: {
        backgroundColor: '#34495e',
    },
    icon: {
        marginRight: '10px',
    },
};

export default AdminSidebar;
