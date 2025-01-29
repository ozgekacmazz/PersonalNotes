import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import PrivateRoute from './components/common/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Notes from './components/dashboard/Notes';
import Tasks from './components/dashboard/Tasks';
import AdminPage from './components/admin/AdminPage';

const App: React.FC = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route
                        path="/dashboard/*"
                        element={<PrivateRoute component={DashboardPage} />}

                    />
                    <Route path="/admin/*" element={<PrivateRoute component={AdminPage} />} />
                    <Route path="/dashboard/notes" element={<Notes />} />
                    <Route path="/dashboard/tasks" element={<Tasks />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
