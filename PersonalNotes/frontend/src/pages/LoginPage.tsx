import React from 'react';
import Login from '../components/auth/Login';

const LoginPage: React.FC = () => {
    return (
        <div style={styles.container}>
            <h1 style={styles.title}>Login</h1>
            <div style={styles.loginBox}>
                <Login />
            </div>
        </div>
    );
};

const styles = {
    container: {
        textAlign: 'center',
        backgroundColor: '#ffe4e1', // Toz pembe arka plan
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
    loginBox: {
        padding: '30px',
        backgroundColor: '#ffe4e1', // Kutunun arka planını açık pembe yapıyoruz
        borderRadius: '10px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '400px',
    },
    button: {
        backgroundColor: '#ba55d3', // Açık mor buton rengi
        color: '#fff',
        border: 'none',
        padding: '10px 20px',
        borderRadius: '5px',
        cursor: 'pointer',
        width: '100%',
        marginTop: '10px',
    },
};

export default LoginPage;
