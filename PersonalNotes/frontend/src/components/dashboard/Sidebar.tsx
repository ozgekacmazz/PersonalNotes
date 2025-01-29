import React from 'react';
import { Link } from 'react-router-dom';

interface SidebarProps {
    isAdmin: boolean; // Kullanıcının admin olup olmadığını kontrol eden prop
}

const Sidebar: React.FC<SidebarProps> = ({ isAdmin }) => {
    return (
        <div style={{ width: '200px', backgroundColor: '#fadadd', padding: '10px' }}>
            <h3>Dashboard</h3>
            <ul>
                <li><Link to="/dashboard/notes">Notes</Link></li>
                <li><Link to="/dashboard/tasks">Tasks</Link></li>
                {/* Eğer kullanıcı adminse "Admin" tuşu göster */}
                {isAdmin && <li><Link to="/admin">Admin</Link></li>}
            </ul>
        </div>
    );
};

export default Sidebar;
