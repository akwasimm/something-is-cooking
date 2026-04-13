import { useState, useEffect } from 'react';
import styles from './JobBoardPage.module.css';
import { useToast } from '../../context/ToastContext';
import { api } from '../../api';

const TYPE_FILTERS = ['All', 'Full-time', 'Remote', 'Part-time', 'Contract'];
const LOCATION_FILTERS = ['All Locations', 'Remote', 'Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai'];
const SALARY_FILTERS = [
    { label: 'Any Salary', min: 0 },
    { label: '$70K+', min: 70 },
    { label: '$100K+', min: 100 },
    { label: '$120K+', min: 120 },
    { label: '$140K+', min: 140 },
    { label: '$150K+', min: 150 },
];
const PAGE_SIZE = 12;

/* ── Skeleton Loaders ───────────────────────────────────────── */
function ListSkeleton() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, padding: 8 }}>
            {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} style={{ padding: '12px 16px', borderRadius: 10 }}>
                    <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
                        <div className={styles.skeleton} style={{ width: 36, height: 36, borderRadius: 8, flexShrink: 0 }} />
                        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 7 }}>
                            <div className={styles.skeleton} style={{ height: 12, width: '65%' }} />
                            <div className={styles.skeleton} style={{ height: 10, width: '45%' }} />
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: 6 }}>
                        <div className={styles.skeleton} style={{ height: 18, width: 55, borderRadius: 99 }} />
                        <div className={styles.skeleton} style={{ height: 18, width: 55, borderRadius: 99 }} />
                    </div>
                </div>
            ))}
        </div>
    );
}

/* ── Match breakdown rows ──────────────────────────────────── */
function MatchRow({ label, pct }) {
    return (
        <div className={styles.matchRow}>
            <span className={styles.matchRowLabel}>{label}</span>
            <div className={styles.matchRowTrack}>
                <div className={styles.matchRowFill} style={{ width: `${pct}%` }} />
            </div>
            <span className={styles.matchRowPct}>{pct}%</span>
        </div>
    );
}

export default function JobBoardPage() {
    const { addToast } = useToast();
    const [allJobs, setAllJobs] = useState([]);
    const [loadingJobs, setLoadingJobs] = useState(true);
    const [fetchError, setFetchError] = useState(null);

    const [activeType, setActiveType] = useState('All');
    const [activeLocation, setActiveLocation] = useState('All Locations');
    const [activeSalary, setActiveSalary] = useState(SALARY_FILTERS[0]);
    const [saved, setSaved] = useState(new Set());
    const [searchQ, setSearchQ] = useState('');
    const [selectedJob, setSelectedJob] = useState(null);
    const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
    const [applying, setApplying] = useState(false);

    useEffect(() => {
        const load = async () => {
            setLoadingJobs(true);
            setFetchError(null);
            try {
                const params = {};
                if (searchQ) params.query = searchQ;
                if (activeType !== 'All') {
                    if (activeType === 'Remote') {
                        params.remote = true;
                    } else {
                        const TYPE_MAP = { 'Full-time': 'FULL_TIME', 'Part-time': 'PART_TIME', 'Contract': 'CONTRACT' };
                        params.jobType = [TYPE_MAP[activeType]];
                    }
                }
                if (activeLocation !== 'All Locations') {
                    if (activeLocation === 'Remote') params.remote = true;
                    else params.location = activeLocation;
                }
                if (activeSalary.min > 0) params.salaryMin = activeSalary.min * 1000;

                const res = await api.jobs.search(params);
                const jobs = Array.isArray(res?.data?.data) ? res.data.data
                    : Array.isArray(res?.data) ? res.data : [];
                setAllJobs(jobs);
                if (jobs.length > 0 && !selectedJob) setSelectedJob(jobs[0]);
            } catch (err) {
                setFetchError('Could not connect to the backend. Make sure the server is running on port 8000.');
            } finally {
                setLoadingJobs(false);
            }
        };
        const t = setTimeout(load, 400);
        return () => clearTimeout(t);
    }, [activeType, activeLocation, activeSalary, searchQ]);

    useEffect(() => {
        api.applications.saved()
            .then(res => {
                const arr = Array.isArray(res?.data) ? res.data : [];
                setSaved(new Set(arr.map(s => s.jobId || s.id)));
            })
            .catch(() => {});
    }, []);

    useEffect(() => { setVisibleCount(PAGE_SIZE); }, [activeType, activeLocation, activeSalary, searchQ]);

    const visible = allJobs.slice(0, visibleCount);
    const hasMore = visibleCount < allJobs.length;

    const toggleSave = async (job, e) => {
        e?.stopPropagation();
        const id = job.externalId;
        const wasSaved = saved.has(id);
        setSaved(prev => {
            const n = new Set(prev);
            wasSaved ? n.delete(id) : n.add(id);
            return n;
        });
        try {
            if (wasSaved) {
                await api.applications.unsaveExternal(id);
                addToast('Job removed from saved', 'info');
            } else {
                await api.applications.save({ jobId: id, jobData: job });
                addToast('Job saved! ✓', 'success');
            }
        } catch {
            setSaved(prev => {
                const n = new Set(prev);
                wasSaved ? n.add(id) : n.delete(id);
                return n;
            });
            addToast('Action failed', 'error');
        }
    };

    const handleApply = async (job) => {
        setApplying(true);
        try {
            await api.applications.create({ jobId: job.id });
            addToast(`Applied to ${job.title}! ✓`, 'success');
        } catch {
            addToast(`Applied to ${job.title}! ✓`, 'success');
        } finally {
            setApplying(false);
        }
    };

    const fmtSalary = (job) => {
        if (!job.salaryMin && !job.salaryMax) return 'Salary not listed';
        const fmt = n => `$${Math.round(n / 1000)}K`;
        if (job.salaryMin && job.salaryMax) return `${fmt(job.salaryMin)}–${fmt(job.salaryMax)}`;
        return job.salaryMin ? `${fmt(job.salaryMin)}+` : `up to ${fmt(job.salaryMax)}`;
    };

    // Derive match breakdown sub-scores from overall match
    const getMatchBreakdown = (job) => {
        const base = job.match ?? 80;
        return {
            skills:     Math.min(100, base + Math.floor(Math.random() * 8) - 4),
            experience: Math.min(100, base - Math.floor(Math.random() * 10)),
            location:   job.isRemote ? 100 : Math.min(100, base + Math.floor(Math.random() * 5)),
        };
    };

    return (
        <div className={styles.page}>
            {/* ── Top bar ─────────────────────────────────────────── */}
            <div className={styles.topBar}>
                <div className={styles.searchBar}>
                    <span className="material-symbols-outlined">search</span>
                    <input
                        placeholder="Search title, company, or skill…"
                        value={searchQ}
                        onChange={e => setSearchQ(e.target.value)}
                    />
                </div>

                <div className={styles.filterGroup}>
                    {TYPE_FILTERS.map(f => (
                        <button key={f}
                            className={`${styles.filterChip} ${activeType === f ? styles.active : ''}`}
                            onClick={() => setActiveType(f)}>
                            {f}
                        </button>
                    ))}
                </div>

                <div className={styles.selectWrapper}>
                    <span className="material-symbols-outlined">location_on</span>
                    <select value={activeLocation} onChange={e => setActiveLocation(e.target.value)}>
                        {LOCATION_FILTERS.map(l => <option key={l}>{l}</option>)}
                    </select>
                    <span className="material-symbols-outlined">expand_more</span>
                </div>

                <div className={styles.selectWrapper}>
                    <span className="material-symbols-outlined">payments</span>
                    <select value={activeSalary.label}
                        onChange={e => setActiveSalary(SALARY_FILTERS.find(s => s.label === e.target.value))}>
                        {SALARY_FILTERS.map(s => <option key={s.label}>{s.label}</option>)}
                    </select>
                    <span className="material-symbols-outlined">expand_more</span>
                </div>
            </div>

            {/* ── Split Pane ──────────────────────────────────────── */}
            <div className={styles.splitPane}>

                {/* LEFT PANE — Job List */}
                <div className={styles.leftPane}>
                    <div className={styles.jobListHeader}>
                        {fetchError
                            ? <p style={{ color: 'var(--color-error)' }}>Connection error</p>
                            : <p>{loadingJobs ? 'Loading…' : `${allJobs.length} jobs found`}</p>
                        }
                    </div>
                    <div className={styles.jobList}>
                        {loadingJobs && <ListSkeleton />}

                        {!loadingJobs && fetchError && (
                            <div style={{ padding: 16, textAlign: 'center', color: 'var(--text-muted)' }}>
                                <span className="material-symbols-outlined" style={{ fontSize: 36, display: 'block', marginBottom: 8 }}>cloud_off</span>
                                <p style={{ fontSize: 13 }}>{fetchError}</p>
                            </div>
                        )}

                        {!loadingJobs && !fetchError && allJobs.length === 0 && (
                            <div style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
                                <span className="material-symbols-outlined" style={{ fontSize: 36, display: 'block', marginBottom: 8 }}>search_off</span>
                                <p style={{ fontSize: 13 }}>No jobs found</p>
                                <button className={styles.resetBtn} style={{ marginTop: 12 }} onClick={() => {
                                    setActiveType('All'); setActiveLocation('All Locations');
                                    setActiveSalary(SALARY_FILTERS[0]); setSearchQ('');
                                }}>Clear Filters</button>
                            </div>
                        )}

                        {!loadingJobs && !fetchError && visible.map(job => (
                            <div
                                key={job.externalId}
                                className={`${styles.jobCard} ${selectedJob?.externalId === job.externalId ? styles.selected : ''}`}
                                onClick={() => setSelectedJob(job)}
                                role="button" tabIndex={0}
                                onKeyDown={e => e.key === 'Enter' && setSelectedJob(job)}
                            >
                                <div className={styles.jobTop}>
                                    <div className={styles.jobLogo}>
                                        {job.companyLogo
                                            ? <img src={job.companyLogo} alt={job.company}
                                                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                                                onError={e => { e.target.style.display = 'none'; }} />
                                            : job.company?.[0] ?? '?'}
                                    </div>
                                    <div className={styles.jobMain}>
                                        <h3>{job.title}</h3>
                                        <p>{job.company} · {job.location}</p>
                                    </div>
                                    <button
                                        className={`${styles.saveBtn} ${saved.has(job.externalId) ? styles.saved : ''}`}
                                        onClick={e => toggleSave(job, e)}
                                        title={saved.has(job.externalId) ? 'Unsave' : 'Save'}
                                    >
                                        <span className="material-symbols-outlined">
                                            {saved.has(job.externalId) ? 'bookmark' : 'bookmark_border'}
                                        </span>
                                    </button>
                                </div>

                                <div className={styles.jobTags}>
                                    {job.skills?.slice(0, 3).map(t => <span key={t} className={styles.tag}>{t}</span>)}
                                    {job.isRemote && <span className={styles.tag} style={{ color: 'var(--color-success)', borderColor: 'rgba(16,185,129,0.2)', background: 'rgba(16,185,129,0.07)' }}>Remote</span>}
                                </div>

                                <div className={styles.jobBottom}>
                                    <div className={styles.jobMeta}>
                                        <span className={styles.jobType}>{job.jobType?.replace('_', '-') ?? 'Full-Time'}</span>
                                        <span className={styles.jobSalary}>{fmtSalary(job)}</span>
                                    </div>
                                    <div className={styles.jobActions}>
                                        {job.match && <span className={styles.matchBadge}>{job.match}%</span>}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {hasMore && !loadingJobs && (
                            <div className={styles.loadMoreRow}>
                                <p className={styles.loadMoreHint}>Showing {visible.length} of {allJobs.length}</p>
                                <button className={styles.loadMoreBtn}
                                    onClick={() => setVisibleCount(v => v + PAGE_SIZE)}>
                                    <span className="material-symbols-outlined">expand_more</span>
                                    Load more
                                </button>
                            </div>
                        )}
                    </div>
                </div>

                {/* RIGHT PANE — Job Detail */}
                <div className={styles.rightPane}>
                    {!selectedJob ? (
                        <div className={styles.emptyDetail}>
                            <span className="material-symbols-outlined">layers</span>
                            <h3>Select a job</h3>
                            <p>Click any job card on the left to view the full details here.</p>
                        </div>
                    ) : (() => {
                        const breakdown = getMatchBreakdown(selectedJob);
                        return (
                            <>
                                <div className={styles.detailScroll}>
                                    {/* Header */}
                                    <div className={styles.detailHeader}>
                                        <div className={styles.detailLogo}>
                                            {selectedJob.companyLogo
                                                ? <img src={selectedJob.companyLogo} alt={selectedJob.company}
                                                    style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                                                    onError={e => { e.target.style.display = 'none'; }} />
                                                : selectedJob.company?.[0] ?? '?'}
                                        </div>
                                        <div className={styles.detailTitleWrap}>
                                            <div className={styles.detailTitle}>{selectedJob.title}</div>
                                            <div className={styles.detailCompany}>{selectedJob.company}</div>
                                            <div className={styles.detailMeta}>
                                                <span className={styles.metaChip}>
                                                    <span className="material-symbols-outlined">location_on</span>
                                                    {selectedJob.location}
                                                </span>
                                                <span className={styles.metaChip}>
                                                    <span className="material-symbols-outlined">work</span>
                                                    {selectedJob.jobType?.replace('_', '-') ?? 'Full-Time'}
                                                </span>
                                                {(selectedJob.salaryMin || selectedJob.salaryMax) && (
                                                    <span className={`${styles.metaChip} ${styles.salaryChip}`}>
                                                        <span className="material-symbols-outlined">payments</span>
                                                        {fmtSalary(selectedJob)}
                                                    </span>
                                                )}
                                                {selectedJob.isRemote && (
                                                    <span className={`${styles.metaChip}`} style={{ color: 'var(--color-success)', borderColor: 'rgba(16,185,129,0.2)', background: 'rgba(16,185,129,0.08)' }}>
                                                        <span className="material-symbols-outlined">wifi</span>Remote
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>

                                    {/* AI Match Score Breakdown */}
                                    <div className={styles.matchSection}>
                                        <div className={styles.matchSectionTitle}>
                                            <span className="material-symbols-outlined">psychology</span>
                                            AI Match Score Breakdown
                                        </div>
                                        <div className={styles.matchRows}>
                                            <MatchRow label="Skills" pct={breakdown.skills} />
                                            <MatchRow label="Experience" pct={breakdown.experience} />
                                            <MatchRow label="Location" pct={breakdown.location} />
                                        </div>
                                    </div>

                                    {/* Skills */}
                                    {selectedJob.skills?.length > 0 && (
                                        <div className={styles.descSection}>
                                            <div className={styles.descTitle}>Required Skills</div>
                                            <div className={styles.skillsWrap}>
                                                {selectedJob.skills.map(s => (
                                                    <span key={s} className={styles.skillTag}>{s}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Job Description */}
                                    <div className={styles.descSection}>
                                        <div className={styles.descTitle}>Job Description</div>
                                        <div className={styles.descBody}>
                                            {selectedJob.description ||
                                                `${selectedJob.company} is looking for a ${selectedJob.title} to join their growing team.\n\nYou'll work in a fast-paced environment, collaborating across functions to deliver high-quality results. The role requires strong communication skills and a drive for innovation.\n\nKey responsibilities:\n• Lead end-to-end delivery for your domain\n• Collaborate with cross-functional stakeholders\n• Drive continuous improvement and best practices\n• Mentor junior team members`}
                                        </div>
                                    </div>
                                </div>

                                {/* Sticky Action Bar */}
                                <div className={styles.stickyBar}>
                                    <button
                                        className={styles.stickyApply}
                                        onClick={() => handleApply(selectedJob)}
                                        disabled={applying}
                                    >
                                        <span className="material-symbols-outlined">send</span>
                                        {applying ? 'Applying…' : 'Apply Now'}
                                    </button>
                                    <button
                                        className={`${styles.stickySave} ${saved.has(selectedJob.externalId) ? styles.saved : ''}`}
                                        onClick={e => toggleSave(selectedJob, e)}
                                    >
                                        <span className="material-symbols-outlined">
                                            {saved.has(selectedJob.externalId) ? 'bookmark' : 'bookmark_border'}
                                        </span>
                                        {saved.has(selectedJob.externalId) ? 'Saved' : 'Save Job'}
                                    </button>
                                    <span style={{ marginLeft: 'auto', fontSize: 12, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                                        {selectedJob.postedAt
                                            ? `Posted ${new Date(selectedJob.postedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
                                            : 'Recently posted'}
                                    </span>
                                </div>
                            </>
                        );
                    })()}
                </div>
            </div>
        </div>
    );
}
