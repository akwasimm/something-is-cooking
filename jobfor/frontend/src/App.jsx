import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import AppLayout from "./components/layout/AppLayout";
import './index.css';

// ── Placeholder Public Views ────────────────────────────────────────────────
const LoginPlaceholder = () => (
  <div style={{ padding: "4rem", textAlign: "center" }}>
    <h2 style={{ marginBottom: "1rem", color: "var(--color-primary-dark)" }}>Login Gate</h2>
    <p>Please log in securely leveraging the AI Auth Context.</p>
  </div>
);

const RegisterPlaceholder = () => (
    <div style={{ padding: "4rem", textAlign: "center" }}>
      <h2 style={{ marginBottom: "1rem", color: "var(--color-primary)" }}>Join JobFor</h2>
      <p>Register as a new candidate dynamically mapping DB Arrays.</p>
    </div>
);

// ── Placeholder Protected Views ───────────────────────────────────────────────
const DashboardPlaceholder = () => (
  <div className="card">
    <h3 style={{ marginBottom: "1rem" }}>Application Activity</h3>
    <p style={{ color: "var(--text-secondary)" }}>Your saved jobs, active applications, and intelligence bounds evaluate natively here.</p>
  </div>
);

const JobsPlaceholder = () => (
  <div className="card">
    <h3 style={{ marginBottom: "1rem" }}>Opportunity Discovery</h3>
    <p style={{ color: "var(--text-secondary)" }}>The Recommendation AI Engine pushes optimized job roles natively into this viewport.</p>
  </div>
);

const ProfilePlaceholder = () => (
  <div className="card">
    <h3 style={{ marginBottom: "1rem" }}>Candidate Profile</h3>
    <p style={{ color: "var(--text-secondary)" }}>Manage structured `.pdf` NLP resumes natively here tracking intermediate structural proficiencies!</p>
  </div>
);

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Access */}
          <Route path="/login" element={<LoginPlaceholder />} />
          <Route path="/register" element={<RegisterPlaceholder />} />

          {/* Secure Routing Map -> AppLayout protects these endpoints cleanly */}
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPlaceholder />} />
            <Route path="/jobs" element={<JobsPlaceholder />} />
            <Route path="/insights" element={<div className="card">Insights Coming Soon</div>} />
            <Route path="/big-opps" element={<div className="card">Big Opps Module Offline</div>} />
            <Route path="/ai-coach" element={<div className="card">AI Coaching Terminal Loading...</div>} />
            <Route path="/profile" element={<ProfilePlaceholder />} />
          </Route>

          {/* Fallback 404 Route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
