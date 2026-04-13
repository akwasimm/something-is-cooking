import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Layout components
import PublicLayout from './components/PublicLayout';
import AppLayout from './components/AppLayout';

// Public pages
import JobForLanding from './JobForLanding';
import BigOpportunities from './BigOpportunities';
import MarketInsights from './MarketInsights';
import SkillGapAnalysis from './SkillGapAnalysis';
import CareerCoach from './CareerCoach';
import JobDetail from './JobDetail';
import JoinCommunity from './JoinCommunity';
import NotFound from './NotFound';

// Standalone auth pages (no layout)
import LoginPage from './LoginPage';
import ResetPassword from './ResetPassword';

// App pages
import UserDashboard from './UserDashboard';
import JobForDashboard from './JobForDashboard';
import SavedJobs from './SavedJobs';
import SettingsPage from './SettingsPage';
import ResumeAnalyzer from './ResumeAnalyzer';
import AIRecommendations from './AIRecommendations';
import JobDiscovery from './JobDiscovery';
import EditProfile from './EditProfile';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ── Public pages ── */}
        <Route path="/" element={<PublicLayout><JobForLanding /></PublicLayout>} />
        <Route path="/opportunities" element={<PublicLayout><BigOpportunities /></PublicLayout>} />
        <Route path="/insights" element={<AppLayout><MarketInsights /></AppLayout>} />
        <Route path="/skill-gap" element={<PublicLayout><SkillGapAnalysis /></PublicLayout>} />
        <Route path="/coach" element={<AppLayout><CareerCoach /></AppLayout>} />
        <Route path="/job" element={<PublicLayout><JobDetail /></PublicLayout>} />
        <Route path="/join" element={<JoinCommunity />} />
        <Route path="*" element={<PublicLayout><NotFound /></PublicLayout>} />

        {/* ── Standalone auth pages ── */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/reset" element={<ResetPassword />} />

        {/* ── App pages (sidebar + header) ── */}
        <Route path="/user" element={<AppLayout><UserDashboard /></AppLayout>} />
        <Route path="/applied" element={<AppLayout><JobForDashboard /></AppLayout>} />
        <Route path="/saved" element={<AppLayout><SavedJobs /></AppLayout>} />
        <Route path="/ai" element={<AppLayout><AIRecommendations /></AppLayout>} />
        <Route path="/discover" element={<AppLayout><JobDiscovery /></AppLayout>} />
        <Route path="/profile" element={<AppLayout><EditProfile /></AppLayout>} />
        <Route path="/settings" element={<AppLayout><SettingsPage /></AppLayout>} />
        <Route path="/analyzer" element={<AppLayout><ResumeAnalyzer /></AppLayout>} />
      </Routes>
    </BrowserRouter>
  );
}
