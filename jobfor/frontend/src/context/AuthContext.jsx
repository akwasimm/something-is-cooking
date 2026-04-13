/**
 * AuthContext.jsx
 * ================
 * Global authentication context. Uses the shared api.js client so all
 * auth calls share the same Axios instance (interceptors, token injection).
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, setTokens, clearTokens, getToken } from '../api';

// ─────────────────────────────────────────────────────────────
// DEV BYPASS — set to true to skip login and use a mock user
// ─────────────────────────────────────────────────────────────
const DEV_BYPASS = true;
const MOCK_USER = {
    id: 'dev-001',
    email: 'test@jobfor.dev',
    name: 'Test User',
    role: 'Software Engineer',
    avatar: 'T',
    profile: {
        firstName: 'Test',
        lastName: 'User',
        profileCompletion: 72,
    },
};
// ─────────────────────────────────────────────────────────────

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(DEV_BYPASS ? MOCK_USER : null);
    const [loading, setLoading] = useState(false);
    const [initializing, setInitializing] = useState(!DEV_BYPASS);

    // ── Restore session on mount ────────────────────────────────
    useEffect(() => {
        if (DEV_BYPASS) return; // skip real restore in bypass mode
        const restore = async () => {
            if (!getToken()) {
                setInitializing(false);
                return;
            }
            try {
                const res = await api.auth.me();
                setUser(res.data);
            } catch {
                clearTokens();
            } finally {
                setInitializing(false);
            }
        };
        restore();
    }, []);

    // ── Login ───────────────────────────────────────────────────
    const login = async (email, password) => {
        if (DEV_BYPASS) {
            setUser(MOCK_USER);
            return { success: true };
        }
        setLoading(true);
        try {
            const res = await api.auth.login(email, password);
            const { accessToken, refreshToken } = res.data;
            setTokens(accessToken, refreshToken);
            // Fetch full profile after token set
            const profileRes = await api.auth.me();
            setUser(profileRes.data);
            return { success: true };
        } catch (error) {
            const msg = error.response?.data?.error
                || error.response?.data?.detail
                || 'Invalid email or password.';
            return { success: false, error: msg };
        } finally {
            setLoading(false);
        }
    };

    // ── Register ────────────────────────────────────────────────
    const register = async (formData) => {
        setLoading(true);
        try {
            const res = await api.auth.register(formData);
            const { accessToken, refreshToken } = res.data;
            setTokens(accessToken, refreshToken);
            const profileRes = await api.auth.me();
            setUser(profileRes.data);
            return { success: true };
        } catch (error) {
            const detail = error.response?.data?.detail;
            const msg = Array.isArray(detail)
                ? detail.map(d => d.msg || d.message || JSON.stringify(d)).join(', ')
                : detail || error.response?.data?.error || 'Registration failed.';
            return { success: false, error: msg };
        } finally {
            setLoading(false);
        }
    };

    // ── Logout ──────────────────────────────────────────────────
    const logout = async () => {
        try { await api.auth.logout(); } catch { /* ignore 401 on logout */ }
        clearTokens();
        setUser(null);
    };

    // Wait for session restore before rendering anything
    if (initializing) {
        return (
            <div style={{
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                height: '100vh', background: '#0d1117', color: '#888',
                flexDirection: 'column', gap: 16,
            }}>
                <div style={{
                    width: 36, height: 36, borderRadius: '50%',
                    border: '3px solid rgba(255,255,255,0.08)',
                    borderTopColor: '#2b8cee',
                    animation: 'spin 0.7s linear infinite',
                }} />
                <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
                <span style={{ fontSize: '0.85rem' }}>Initializing JobFor…</span>
            </div>
        );
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be inside AuthProvider');
    return ctx;
};
