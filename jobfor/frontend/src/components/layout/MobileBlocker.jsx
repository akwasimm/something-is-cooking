import { useState, useEffect } from 'react';

const styles = {
    container: {
        position: 'fixed',
        inset: 0,
        backgroundColor: '#0d6634', // JobFor green
        color: '#fff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px',
        textAlign: 'center',
        zIndex: 999999, // Ensure it's on top of everything
        fontFamily: "'Inter', sans-serif"
    },
    iconWrapper: {
        width: '80px',
        height: '80px',
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: '24px'
    },
    icon: {
        fontSize: '40px',
        color: '#fff' // Wait, I'll use material-symbols-outlined
    },
    title: {
        fontSize: '24px',
        fontWeight: '800',
        marginBottom: '16px',
        lineHeight: 1.2
    },
    message: {
        fontSize: '16px',
        color: 'rgba(255,255,255,0.85)',
        maxWidth: '320px',
        lineHeight: 1.5,
        marginBottom: '32px'
    },
    brand: {
        position: 'absolute',
        bottom: '32px',
        fontSize: '18px',
        fontWeight: '900',
        color: 'rgba(255,255,255,0.5)',
        letterSpacing: '-0.5px'
    }
};

export default function MobileBlocker({ children }) {
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    if (isMobile) {
        return (
            <div style={styles.container}>
                <div style={styles.iconWrapper}>
                    <span className="material-symbols-outlined" style={styles.icon}>desktop_mac</span>
                </div>
                <h1 style={styles.title}>Desktop Experience Required</h1>
                <p style={styles.message}>
                    Hold up! JobFor's advanced AI matching and dashboard tools are optimized exclusively for desktop screens.
                </p>
                <p style={{...styles.message, marginBottom: '0'}}>
                    Please switch to a laptop or increase your browser width to access the platform.
                </p>
                <div style={styles.brand}>JobFor.</div>
            </div>
        );
    }

    return children;
}
