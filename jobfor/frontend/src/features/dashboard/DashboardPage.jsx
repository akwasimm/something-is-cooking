import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api';
import { AreaChart, Area, ResponsiveContainer, Tooltip } from 'recharts';
import styles from './DashboardPage.module.css';

const activityData = [
    { day: 'Mon', applications: 0 }, { day: 'Tue', applications: 0 },
    { day: 'Wed', applications: 0 }, { day: 'Thu', applications: 0 },
    { day: 'Fri', applications: 0 }, { day: 'Sat', applications: 0 },
    { day: 'Sun', applications: 0 },
];

const RECENT_ACTIVITY_MOCK = [
    { icon: 'smart_toy', color: 'info', text: 'AI Coach analysed your resume profile', time: 'Just now' },
    { icon: 'stars', color: 'warning', text: '3 new job matches found for you', time: '2h ago' },
    { icon: 'bookmark', color: 'brand', text: 'You saved "Senior Product Designer"', time: 'Yesterday' },
    { icon: 'task_alt', color: 'success', text: 'Application sent to PixelWorks', time: '2d ago' },
];

/* ── Skeleton Loaders ───────────────────────────── */
function PickSkeleton() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
            {[1, 2, 3].map(i => (
                <div key={i} style={{
                    display: 'flex', alignItems: 'flex-start', gap: 12,
                    padding: '16px 0', borderBottom: '1px solid rgba(255,255,255,0.05)'
                }}>
                    <div className={styles.skeleton} style={{ width: 44, height: 44, borderRadius: 10, flexShrink: 0 }} />
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <div className={styles.skeleton} style={{ height: 13, width: '65%' }} />
                        <div className={styles.skeleton} style={{ height: 11, width: '40%' }} />
                        <div className={styles.skeleton} style={{ height: 5, width: '80%', borderRadius: 99 }} />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 6, alignItems: 'flex-end' }}>
                        <div className={styles.skeleton} style={{ height: 20, width: 48 }} />
                        <div className={styles.skeleton} style={{ height: 28, width: 72, borderRadius: 99 }} />
                    </div>
                </div>
            ))}
        </div>
    );
}

function StatSkeleton() {
    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
            {[1, 2, 3, 4].map(i => (
                <div key={i} className={styles.statCard} style={{ gap: 12 }}>
                    <div className={styles.skeleton} style={{ width: 22, height: 22, borderRadius: 6 }} />
                    <div className={styles.skeleton} style={{ width: '50%', height: 28, borderRadius: 8 }} />
                    <div className={styles.skeleton} style={{ width: '70%', height: 11, borderRadius: 6 }} />
                </div>
            ))}
        </div>
    );
}

function JobsError({ onRetry }) {
    return (
        <div style={{
            textAlign: 'center', padding: '2rem 1rem',
            background: 'rgba(239, 68, 68, 0.05)',
            border: '1px solid rgba(239, 68, 68, 0.2)',
            borderRadius: 12
        }}>
            <span className="material-symbols-outlined" style={{ fontSize: 36, color: 'var(--color-error)', display: 'block', marginBottom: 8 }}>
                wifi_off
            </span>
            <p style={{ color: 'var(--color-error)', fontWeight: 600, marginBottom: 4 }}>Couldn't load job recommendations</p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', marginBottom: 12 }}>
                Make sure the backend server is running at <code>localhost:8000</code>
            </p>
            <button onClick={onRetry} style={{
                padding: '6px 16px', borderRadius: 8, border: '1px solid rgba(239,68,68,0.4)',
                background: 'transparent', color: 'var(--color-error)', cursor: 'pointer', fontSize: '0.83rem',
                fontFamily: 'var(--font-body)'
            }}>
                Retry
            </button>
        </div>
    );
}

export default function DashboardPage() {
    const { user } = useAuth();
    const [jobs, setJobs] = useState([]);
    const [applications, setApplications] = useState([]);
    const [loadingJobs, setLoadingJobs] = useState(true);
    const [errorJobs, setErrorJobs] = useState(false);

    const firstName = user?.profile?.firstName || user?.email?.split('@')[0] || 'there';

    const fetchData = async () => {
        setLoadingJobs(true);
        setErrorJobs(false);
        try {
            const [jobsRes, appsRes] = await Promise.allSettled([
                api.jobs.recommendations(),
                api.applications.list(),
            ]);

            if (jobsRes.status === 'fulfilled') {
                const data = jobsRes.value?.data;
                setJobs(Array.isArray(data) ? data.slice(0, 4) : []);
            } else {
                setErrorJobs(true);
            }

            if (appsRes.status === 'fulfilled') {
                const data = appsRes.value?.data;
                setApplications(Array.isArray(data) ? data : []);
            }
        } catch {
            setErrorJobs(true);
        } finally {
            setLoadingJobs(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const appliedCount = applications.length;
    const interviewCount = applications.filter(a =>
        ['INTERVIEWING', 'SCREENING'].includes(a.status)
    ).length;
    const savedCount = applications.filter(a => a.status === 'SAVED').length;
    const profilePct = user?.profile?.profileCompletion ?? 0;

    const fmtSalary = (min, max) => {
        if (!min && !max) return null;
        const fmt = n => `$${Math.round(n / 1000)}K`;
        if (min && max) return `${fmt(min)}–${fmt(max)}`;
        return min ? `from ${fmt(min)}` : `up to ${fmt(max)}`;
    };

    // Build activity from real applications + static fallback
    const activityItems = applications.length > 0
        ? applications.slice(0, 4).map(app => ({
            icon: 'send',
            color: 'brand',
            text: `Applied to "${app.jobData?.title || 'a job'}" at ${app.jobData?.company || 'a company'}`,
            time: new Date(app.appliedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        }))
        : RECENT_ACTIVITY_MOCK;

    return (
        <div className={styles.page}>
            {/* Welcome Banner */}
            <div className={styles.welcome}>
                <div>
                    <h1>Welcome back, {firstName} 👋</h1>
                    <p>
                        You have <strong>{interviewCount} interview{interviewCount !== 1 ? 's' : ''}</strong> in progress and{' '}
                        <strong>{jobs.length} new job match{jobs.length !== 1 ? 'es' : ''}</strong> today.
                    </p>
                </div>
                <Link to="/jobs" className={styles.exploreBtn}>
                    <span className="material-symbols-outlined">explore</span>
                    Explore Jobs
                </Link>
            </div>

            {/* 4 Kanban KPI Cards */}
            {loadingJobs ? <StatSkeleton /> : (
                <div className={styles.statsGrid}>
                    {[
                        { label: 'Applied Jobs',      value: appliedCount,   icon: 'send',          color: 'brand'   },
                        { label: 'Saved Jobs',         value: savedCount,     icon: 'bookmark',      color: 'info'    },
                        { label: 'Interviewing',       value: interviewCount, icon: 'event',         color: 'success' },
                        { label: 'Profile Complete',   value: `${profilePct}%`, icon: 'person',       color: 'warning' },
                    ].map((s) => (
                        <div key={s.label} className={`${styles.statCard} ${styles[s.color]}`}>
                            <span className={`material-symbols-outlined ${styles.statIcon}`}>{s.icon}</span>
                            <div className={styles.statVal}>{s.value}</div>
                            <div className={styles.statLabel}>{s.label}</div>
                        </div>
                    ))}
                </div>
            )}

            {/* Bento Main Grid: Top Picks + Right Column */}
            <div className={styles.mainGrid}>

                {/* Left: Top Picks */}
                <section className={styles.card}>
                    <div className={styles.cardHeader}>
                        <h2>
                            <span className="material-symbols-outlined">stars</span>
                            Top Picks for You
                        </h2>
                        <Link to="/jobs" className={styles.seeAll}>See all →</Link>
                    </div>
                    <div className={styles.picksList}>
                        {loadingJobs && <PickSkeleton />}

                        {!loadingJobs && errorJobs && <JobsError onRetry={fetchData} />}

                        {!loadingJobs && !errorJobs && jobs.length === 0 && (
                            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                                <span className="material-symbols-outlined" style={{ fontSize: 36, display: 'block', marginBottom: 8, color: 'var(--text-muted)' }}>
                                    work_off
                                </span>
                                <p>No job recommendations yet.</p>
                                <Link to="/jobs" style={{ color: 'var(--color-primary)', fontSize: '0.85rem' }}>Browse all jobs →</Link>
                            </div>
                        )}

                        {!loadingJobs && !errorJobs && jobs.map((job) => {
                            const matchPct = job.match ?? Math.floor(75 + Math.random() * 22);
                            const salary = fmtSalary(job.salaryMin, job.salaryMax);
                            return (
                                <div key={job.id} className={styles.pickItem}>
                                    <div className={styles.pickLogo}>
                                        {job.companyLogo
                                            ? <img src={job.companyLogo} alt={job.company}
                                                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                                                onError={e => { e.target.style.display = 'none'; }} />
                                            : job.company?.[0] ?? '?'}
                                    </div>
                                    <div className={styles.pickInfo}>
                                        <h3>{job.title}</h3>
                                        <p>{job.company} · {job.location}</p>
                                        {salary && <span className={styles.salary}>{salary}</span>}
                                        {/* AI Match Progress Bar */}
                                        <div className={styles.matchBarWrap}>
                                            <div className={styles.matchBarTrack}>
                                                <div className={styles.matchBarFill} style={{ width: `${matchPct}%` }} />
                                            </div>
                                            <span className={styles.matchPct}>{matchPct}%</span>
                                        </div>
                                    </div>
                                    <div className={styles.pickRight}>
                                        <Link to="/jobs" className={styles.quickApply}>View</Link>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </section>

                {/* Right Column */}
                <div className={styles.rightCol}>
                    {/* Weekly Chart */}
                    <section className={styles.card}>
                        <div className={styles.cardHeader}>
                            <h2>
                                <span className="material-symbols-outlined">bar_chart</span>
                                This Week
                            </h2>
                        </div>
                        <ResponsiveContainer width="100%" height={90}>
                            <AreaChart data={activityData}>
                                <defs>
                                    <linearGradient id="gradPrimary" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#6366F1" stopOpacity={0.35} />
                                        <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <Area type="monotone" dataKey="applications" stroke="#6366F1"
                                    fill="url(#gradPrimary)" strokeWidth={2} />
                                <Tooltip contentStyle={{
                                    background: 'var(--bg-card)', border: '1px solid var(--border-color)',
                                    borderRadius: '8px', color: 'var(--text-primary)', fontSize: 12
                                }} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </section>

                    {/* Recent Applications */}
                    <section className={`${styles.card} ${styles.interviewCard}`}>
                        <div className={styles.interviewBadge}>
                            <span className="material-symbols-outlined">send</span>
                            Recent Applications
                        </div>
                        {applications.length === 0 ? (
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', margin: '4px 0 12px' }}>
                                No applications yet.{' '}
                                <Link to="/jobs" style={{ color: 'var(--color-primary)' }}>Browse jobs →</Link>
                            </p>
                        ) : (
                            <>
                                <h3>{applications[0]?.jobData?.title || 'Applied Job'}</h3>
                                <p>Status: <strong style={{ color: 'var(--color-success)' }}>{applications[0]?.status}</strong></p>
                            </>
                        )}
                        <Link to="/jobs/applied" className={styles.prepBtn}
                            style={{ display: 'inline-flex', alignItems: 'center', gap: 6, textDecoration: 'none', marginTop: 4 }}>
                            <span className="material-symbols-outlined" style={{ fontSize: 14 }}>list</span>
                            View All
                        </Link>
                    </section>

                    {/* AI Coach Tip */}
                    <section className={`${styles.card} ${styles.aiCard}`}>
                        <div className={styles.aiHeader}>
                            <span className="material-symbols-outlined">lightbulb</span>
                            AI Coach Tip
                        </div>
                        <p>
                            Your profile match for Tech Roles could increase by <strong>15%</strong> if you add{' '}
                            <em>Systems Design</em> to your skills.
                        </p>
                        <Link to="/skill-gap" className={styles.aiLink}>View Skill Gap →</Link>
                    </section>
                </div>
            </div>

            {/* Activity Timeline */}
            <section className={styles.card}>
                <div className={styles.cardHeader}>
                    <h2>
                        <span className="material-symbols-outlined">history</span>
                        Recent Activity
                    </h2>
                </div>
                <div className={styles.activityList}>
                    {activityItems.map((item, i) => (
                        <div key={i} className={styles.activityItem}>
                            <span className={`material-symbols-outlined ${styles.actIcon} ${styles[item.color]}`}>
                                {item.icon}
                            </span>
                            <p dangerouslySetInnerHTML={{ __html: item.text.replace(/"([^"]+)"/g, '"<strong>$1</strong>"') }} />
                            <span className={styles.actTime}>{item.time}</span>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}
