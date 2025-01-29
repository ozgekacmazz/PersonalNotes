import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar: React.FC<{ isAdmin: boolean }> = ({ isAdmin }) => {
    return (
        <div className="bg-dark text-light p-3" style={styles.sidebar}>
            <h4>Dashboard</h4>
            <ul className="list-unstyled">
                <li>
                    <Link to="/dashboard/notes" className="text-light text-decoration-none">
                        Notes
                    </Link>
                </li>
                <li>
                    <Link to="/dashboard/tasks" className="text-light text-decoration-none">
                        Tasks
                    </Link>
                </li>
                {isAdmin && (
                    <li>
                        <Link to="/admin" className="text-light text-decoration-none">
                            Admin Panel
                        </Link>
                    </li>
                )}
            </ul>
        </div>
    );
};

const styles = {
    sidebar: {
        width: '250px',
        minHeight: '100vh',
    },
};

export default Sidebar;
