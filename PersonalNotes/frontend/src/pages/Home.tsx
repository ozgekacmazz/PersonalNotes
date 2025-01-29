import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
    const navigate = useNavigate();

    const handleRegister = () => {
        navigate('/register'); // Register sayfasına yönlendir
    };

    const handleLogin = () => {
        navigate('/login'); // Login sayfasına yönlendir
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>Welcome to the Home Page</h1>
            <p>This is the landing page of the application.</p>
            <div style={styles.buttonContainer}>
                <button onClick={handleRegister} style={styles.button}>
                    Register
                </button>
                <button onClick={handleLogin} style={styles.button}>
                    Login
                </button>
            </div>
        </div>
    );
};

const styles = {
    container: {
        textAlign: 'center',
        marginTop: '50px',
        backgroundColor: '#ffe4e1', // Toz pembe
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        fontSize: '2rem',
        color: '#333',
        marginBottom: '20px',
    },
    buttonContainer: {
        marginTop: '20px',
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
    },
    button: {
        padding: '10px 20px',
        backgroundColor: '#ba55d3', // Açık mor
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
        transition: '0.3s',
    },
};

export default Home;
