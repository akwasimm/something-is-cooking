/**
 * api.js — Real Axios HTTP client for JobFor
 * ============================================
 * Connects to the FastAPI backend at http://localhost:8000/api/v1
 * 
 * Features:
 *  - Automatic Bearer token injection via request interceptor
 *  - snake_case → camelCase response conversion via response interceptor
 *  - Graceful 401 handling (clears tokens + redirects to login)
 *  - SSE streaming helper for AI Coach chat
 */
import axios from 'axios';

// ─── Token Helpers ───────────────────────────────────────────────
export const getToken = () => localStorage.getItem('accessToken');
export const setTokens = (access, refresh) => {
    localStorage.setItem('accessToken', access);
    if (refresh) localStorage.setItem('refreshToken', refresh);
};
export const clearTokens = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
};

// ─── camelCase Converter ─────────────────────────────────────────
/**
 * Recursively converts an object's keys from snake_case to camelCase.
 * Handles nested objects and arrays.
 */
function toCamel(str) {
    return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}
function convertKeys(obj) {
    if (Array.isArray(obj)) return obj.map(convertKeys);
    if (obj !== null && typeof obj === 'object') {
        return Object.fromEntries(
            Object.entries(obj).map(([k, v]) => [toCamel(k), convertKeys(v)])
        );
    }
    return obj;
}

// ─── Axios Instance ──────────────────────────────────────────────
const http = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: { 'Content-Type': 'application/json' },
    timeout: 15000,
});

// Request interceptor — inject auth token
http.interceptors.request.use((config) => {
    const token = getToken();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

// Response interceptor — normalize keys and handle 401
http.interceptors.response.use(
    (response) => {
        if (response.data && typeof response.data === 'object') {
            response.data = convertKeys(response.data);
        }
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            clearTokens();
            // Soft redirect — components will re-render and hit Navigate guard
            if (!window.location.pathname.includes('/auth/')) {
                window.location.href = '/auth/login';
            }
        }
        return Promise.reject(error);
    }
);

// ─── SSE Streaming for AI Coach ─────────────────────────────────
/**
 * Opens a streaming fetch request to /ai-coach/chat and yields
 * text tokens as they arrive from the server-sent event stream.
 *
 * @param {string} message - User's chat message
 * @param {string} [sessionId] - Optional session continuity ID
 * @param {function} onToken - Called with each token string chunk
 * @returns {Promise<void>}
 */
export async function streamAiChat(message, sessionId, onToken) {
    const token = getToken();
    const response = await fetch('http://localhost:8000/api/v1/ai-coach/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
            message,
            session_id: sessionId || null,
            context: 'general',
        }),
    });

    if (!response.ok) {
        throw new Error(`AI Coach responded with ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        // SSE format: "data: <token>\n\n"
        const lines = chunk.split('\n');
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const token = line.slice(6).trim();
                if (token && token !== '[DONE]') onToken(token);
            }
        }
    }
}

// ─── API Surface ─────────────────────────────────────────────────
export const api = {
    // ── Auth ──────────────────────────────────────────────────────
    auth: {
        login: (email, password) =>
            http.post('/auth/login', { email, password }),

        register: (data) =>
            http.post('/auth/register', data),

        me: () =>
            http.get('/auth/me'),

        logout: () =>
            http.post('/auth/logout'),

        forgotPassword: (email) =>
            http.post('/auth/forgot-password', { email }),

        resetPassword: (token, newPassword) =>
            http.post('/auth/reset-password', { token, newPassword }),
    },

    // ── Jobs ──────────────────────────────────────────────────────
    jobs: {
        search: (params = {}) => {
            // Normalize frontend param keys to backend snake_case query params
            const mapped = {};
            if (params.query)    mapped.query            = params.query;
            if (params.location) mapped.location         = params.location;
            if (params.jobType)  mapped.job_type         = params.jobType;
            if (params.remote)   mapped.remote           = params.remote;
            if (params.salaryMin)mapped.salary_min       = params.salaryMin;
            if (params.page)     mapped.page             = params.page;
            if (params.limit)    mapped.limit            = params.limit;
            return http.get('/jobs/search', { params: mapped });
        },

        trending: (limit = 10) =>
            http.get('/jobs/trending', { params: { limit } }),

        getById: (id) =>
            http.get(`/jobs/${id}`),

        getSimilar: (id, limit = 10) =>
            http.get(`/jobs/${id}/similar`, { params: { limit } }),

        recommendations: (limit = 20) =>
            http.get('/jobs/user/recommendations', { params: { limit } }),
    },

    // ── Applications / ATS ────────────────────────────────────────
    applications: {
        list: (status) =>
            http.get('/applications/', { params: status ? { status } : {} }),

        apply: (data) =>
            http.post('/applications/apply', data),

        // Legacy alias kept for backward compat with JobBoardPage
        create: (data) =>
            http.post('/applications/apply', data),

        updateStatus: (appId, status) =>
            http.patch(`/applications/${appId}/status`, { status }),

        stats: () =>
            http.get('/applications/stats'),

        saved: () =>
            http.get('/applications/saved'),

        save: (data) =>
            // Backend expects integer job_id — if we only have externalId, store jobData
            http.post('/applications/saved', data),

        unsave: (jobId) =>
            http.delete(`/applications/saved/${jobId}`),

        // Alias for external (string) job IDs saved from job board
        unsaveExternal: (jobId) =>
            http.delete(`/applications/saved/${jobId}`),
    },

    // ── Profile ───────────────────────────────────────────────────
    profile: {
        get: () =>
            http.get('/profile/'),

        update: (data) =>
            http.put('/profile/', data),

        addSkill: (data) =>
            http.post('/profile/skills', data),

        removeSkill: (id) =>
            http.delete(`/profile/skills/${id}`),

        addExperience: (data) =>
            http.post('/profile/experience', data),

        updateExperience: (id, data) =>
            http.put(`/profile/experience/${id}`, data),

        deleteExperience: (id) =>
            http.delete(`/profile/experience/${id}`),

        addEducation: (data) =>
            http.post('/profile/education', data),

        updateEducation: (id, data) =>
            http.put(`/profile/education/${id}`, data),

        deleteEducation: (id) =>
            http.delete(`/profile/education/${id}`),

        addCertification: (data) =>
            http.post('/profile/certifications', data),

        uploadResume: (file) => {
            const form = new FormData();
            form.append('file', file);
            return http.post('/profile/resume', form, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
        },

        completion: () =>
            // Frontend used this — map to profile get and compute client-side
            http.get('/profile/'),
    },

    // ── AI Coach ─────────────────────────────────────────────────
    // NOTE: chat uses streamAiChat() instead — see above
    aiCoach: {
        chat: (message, sessionId) =>
            // Non-streaming fallback for places that still call the old API
            http.post('/ai-coach/chat', {
                message,
                session_id: sessionId || null,
                context: 'general',
            }),

        resumeReview: (resumeText) =>
            http.post('/ai-coach/resume-review', { resume_text: resumeText }),

        coverLetter: (jobDescription, tone = 'professional') =>
            http.post('/ai-coach/cover-letter', { job_description: jobDescription, tone }),

        interviewPrep: (role, company) =>
            http.post('/ai-coach/interview-prep', { role, company }),

        salaryNegotiation: (data) =>
            http.post('/ai-coach/salary-negotiation', data),

        careerPath: (currentRole, targetRole) =>
            http.post('/ai-coach/career-path', { current_role: currentRole, target_role: targetRole }),

        sessions: () =>
            http.get('/ai-coach/sessions'),

        sessionHistory: (sessionId) =>
            http.get(`/ai-coach/sessions/${sessionId}`),

        deleteSession: (sessionId) =>
            http.delete(`/ai-coach/sessions/${sessionId}`),
    },

    // ── Insights / Analytics ──────────────────────────────────────
    insights: {
        salary: (role = 'Software Engineer', location) =>
            http.get('/insights/salary', { params: { role, ...(location ? { location } : {}) } }),

        skillDemand: (limit = 20) =>
            http.get('/insights/skills/demand', { params: { limit } }),

        skillGap: (role) =>
            http.get('/insights/skill-gap', { params: { role } }),

        companies: (limit = 20) =>
            http.get('/insights/companies', { params: { limit } }),
    },

    // ── Notifications ─────────────────────────────────────────────
    notifications: {
        list: (unreadOnly = false) =>
            http.get('/notifications/', { params: { unread_only: unreadOnly } }),

        markRead: (id) =>
            http.patch(`/notifications/${id}/read`),

        markAllRead: () =>
            http.patch('/notifications/read-all'),

        delete: (id) =>
            http.delete(`/notifications/${id}`),

        createAlert: (data) =>
            http.post('/notifications/alerts', data),
    },
};
