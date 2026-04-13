import React, { useState, useEffect } from "react";
import { fetchJobs } from "./api/client";

// ─── Data ────────────────────────────────────────────────────────────────────

const jobTypes = [
  { id: "fulltime", label: "Full-time", defaultChecked: true },
  { id: "contract", label: "Contract", defaultChecked: false },
  { id: "parttime", label: "Part-time", defaultChecked: false },
];

const dateOptions = [
  { id: "24h", label: "Last 24 hours" },
  { id: "7d", label: "Last 7 days" },
  { id: "30d", label: "Last 30 days" },
  { id: "any", label: "Any time" },
];

const experienceLevels = ["Entry Level", "Mid-Senior", "Director", "Executive"];

const footerResources = ["Market Insights", "Career Pathing", "Salary Benchmarks", "Success Stories"];
const footerCompany = ["Our Philosophy", "Contact Support", "Terms of Use", "Privacy Hub"];

// ─── Reusable Components ─────────────────────────────────────────────────────

function MatchBar({ value }) {
  return (
    <div style={{ maxWidth: "384px", marginBottom: "16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.625rem", fontWeight: 900, textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "8px", fontFamily: "'Space Grotesk', sans-serif" }}>
        <span>Match Compatibility</span>
        <span style={{ color: "#1A4D2E" }}>{value}%</span>
      </div>
      <div style={{ width: "100%", height: "12px", backgroundColor: "#f3f4f6", border: "2px solid #000000", overflow: "hidden", padding: "2px" }}>
        <div style={{ backgroundColor: "#1A4D2E", height: "100%", width: `${value}%`, transition: "width 0.6s ease" }} />
      </div>
    </div>
  );
}

function NeoBtn({ children, bg, color = "#000", shadow = true, onClick, style = {} }) {
  const [hovered, setHovered] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        backgroundColor: bg, color, fontWeight: 900, padding: "12px 24px",
        border: shadow ? "3px solid #000" : "2px solid #000",
        boxShadow: shadow ? (hovered ? "none" : "3px 3px 0px 0px #000000") : "none",
        transform: shadow && hovered ? "translate(2px,2px)" : "translate(0,0)",
        transition: "all 0.15s ease", textTransform: "uppercase",
        fontSize: "0.625rem", letterSpacing: "0.2em", cursor: "pointer",
        fontFamily: "'Space Grotesk', sans-serif", ...style,
      }}
    >
      {children}
    </button>
  );
}

// ─── Job Card ─────────────────────────────────────────────────────────────────

function JobCard({ job }) {
  const [saved, setSaved] = useState(job.bookmarked);
  const [cardHover, setCardHover] = useState(false);
  const [saveHover, setSaveHover] = useState(false);

  return (
    <div
      onMouseEnter={() => setCardHover(true)}
      onMouseLeave={() => setCardHover(false)}
      style={{
        backgroundColor: "#ffffff", padding: "16px", border: "2px solid #000000",
        boxShadow: cardHover ? "8px 8px 0px 0px rgba(0,0,0,1)" : "5px 5px 0px 0px #000000",
        transform: cardHover ? "translate(-1px,-1px)" : "translate(0,0)",
        transition: "all 0.15s ease", position: "relative",
      }}
    >
      {/* Bookmark */}
      <div style={{ position: "absolute", top: "16px", right: "16px" }}>
        <button
          onClick={() => setSaved(!saved)}
          onMouseEnter={() => setSaveHover(true)}
          onMouseLeave={() => setSaveHover(false)}
          style={{
            padding: "12px", border: "2px solid #000000",
            backgroundColor: saved ? "#D8B4FE" : saveHover ? "#D8B4FE" : "#ffffff",
            boxShadow: saved ? "none" : "3px 3px 0px 0px #000000",
            cursor: "pointer", transition: "all 0.15s ease",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}
        >
          <span
            className="material-symbols-outlined"
            style={{ fontVariationSettings: saved ? "'FILL' 1, 'wght' 600" : "'FILL' 0, 'wght' 600", display: "block" }}
          >
            {saved ? "bookmark" : "bookmark_border"}
          </span>
        </button>
      </div>

      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
        {/* Logo */}
        <div style={{ width: "64px", height: "64px", border: "2px solid #000000", backgroundColor: job.logoBg, display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden", flexShrink: 0, boxShadow: "3px 3px 0px 0px #000000" }}>
          {job.logoType === "image" ? (
            <img src={job.logo} alt="Company" style={{ width: "56px", height: "56px", objectFit: "contain" }} />
          ) : (
            <span className="material-symbols-outlined" style={{ fontSize: "2.5rem", color: job.logoIconColor }}>{job.logoIcon}</span>
          )}
        </div>

        {/* Content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ marginBottom: "16px" }}>
            <h2 style={{ fontSize: "1.5rem", fontWeight: 800, textTransform: "uppercase", letterSpacing: "-0.025em", marginBottom: "8px", fontFamily: "'Syne', sans-serif", cursor: "pointer" }}>
              {job.title}
            </h2>
            <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "12px", color: "rgba(0,0,0,0.8)", fontWeight: 700, textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em", fontFamily: "'Space Grotesk', sans-serif" }}>
              <span style={{ display: "flex", alignItems: "center" }}>
                <span className="material-symbols-outlined" style={{ fontSize: "16px", marginRight: "4px" }}>business</span>
                {job.company}
              </span>
              <span style={{ color: "rgba(0,0,0,0.3)" }}>•</span>
              {job.location ? (
                <span style={{ display: "flex", alignItems: "center" }}>
                  <span className="material-symbols-outlined" style={{ fontSize: "16px", marginRight: "4px" }}>location_on</span>
                  {job.location}
                </span>
              ) : job.locationBadge ? (
                <span style={{ backgroundColor: "#D8B4FE", color: "#000000", padding: "2px 8px" }}>{job.locationBadge}</span>
              ) : null}
              <span style={{ color: "rgba(0,0,0,0.3)" }}>•</span>
              <span style={{ backgroundColor: "#1A4D2E", color: "#ffffff", padding: "2px 8px" }}>{job.salary}</span>
            </div>
          </div>

          <MatchBar value={job.match} />

          <div style={{ display: "flex", flexWrap: "wrap", gap: "12px", marginBottom: "24px" }}>
            {job.tags.map((tag) => (
              <span key={tag} style={{ backgroundColor: "#f3f4f6", padding: "6px 16px", fontWeight: 900, fontSize: "0.625rem", textTransform: "uppercase", letterSpacing: "0.1em", border: "2px solid #000000", fontFamily: "'Space Grotesk', sans-serif" }}>
                {tag}
              </span>
            ))}
          </div>

          <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
            <NeoBtn bg="#D8B4FE" color="#000000">Quick Apply</NeoBtn>
            <NeoBtn bg="#ffffff" color="#000000" shadow={false} style={{ border: "2px solid #000" }}>View Details</NeoBtn>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Skeleton Card ────────────────────────────────────────────────────────────

function SkeletonCard() {
  return (
    <div style={{ padding: "16px", border: "2px dashed #d1d5db", opacity: 0.6 }}>
      <style>{`
        @keyframes loading {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
        .skeleton {
          background: linear-gradient(90deg, #f8f8f8 25%, #efeff1 50%, #f8f8f8 75%);
          background-size: 200% 100%;
          animation: loading 1.5s infinite;
        }
      `}</style>
      <div style={{ display: "flex", gap: "16px" }}>
        <div className="skeleton" style={{ width: "64px", height: "64px", border: "2px solid #000", flexShrink: 0 }} />
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "16px" }}>
          <div className="skeleton" style={{ height: "24px", width: "40%" }} />
          <div className="skeleton" style={{ height: "16px", width: "30%" }} />
          <div className="skeleton" style={{ height: "12px", width: "50%" }} />
          <div style={{ display: "flex", gap: "16px" }}>
            <div className="skeleton" style={{ height: "40px", width: "140px" }} />
            <div className="skeleton" style={{ height: "40px", width: "140px" }} />
          </div>
        </div>
      </div>
      <p style={{ textAlign: "center", marginTop: "32px", fontWeight: 900, fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.3em", color: "rgba(0,0,0,0.3)", fontFamily: "'Space Grotesk', sans-serif" }}>
        Syncing latest matches...
      </p>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function JobDiscovery() {
  const [searchQuery, setSearchQuery] = useState("");
  const [locationQuery, setLocationQuery] = useState("");
  const [jobTypeChecks, setJobTypeChecks] = useState({ fulltime: true, contract: false, parttime: false });
  const [experience, setExperience] = useState("Mid-Senior");
  const [datePosted, setDatePosted] = useState("any");
  const [remoteOnly, setRemoteOnly] = useState(true);
  const [sortBy, setSortBy] = useState("Newest First");
  const [currentPage, setCurrentPage] = useState(1);
  const [postJobHover, setPostJobHover] = useState(false);
  const [searchBtnHover, setSearchBtnHover] = useState(false);

  // Live Data State
  const [jobListings, setJobListings] = useState([]);
  const [totalJobs, setTotalJobs] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadJobs = async () => {
      setLoading(true);
      try {
        const data = await fetchJobs({
          query: searchQuery,
          location: locationQuery,
          remote_only: remoteOnly
        });
        // Map backend models to UI expected props
        const mappedJobs = (data.items || []).map((j) => ({
          id: j.id,
          logo: j.company_logo_url || null,
          logoType: j.company_logo_url ? "image" : "icon",
          logoIcon: "work",
          logoBg: "#f9fafb",
          logoIconColor: "#1A4D2E",
          title: j.title,
          company: j.company_name,
          location: j.location,
          locationBadge: j.is_remote ? "Remote" : null,
          salary: j.salary_max ? `₹${(j.salary_min/1000).toFixed(0)}k - ₹${(j.salary_max/1000).toFixed(0)}k` : "Not disclosed",
          match: Math.floor(Math.random() * 20) + 80, // mock match score for now
          tags: [j.employment_type || "Full-time", j.experience_level || "Any"],
          bookmarked: false
        }));
        setJobListings(mappedJobs);
        setTotalJobs(data.total || mappedJobs.length);
      } catch (err) {
        console.error("Failed fetching jobs", err);
      } finally {
        setLoading(false);
      }
    };

    // basic debouncing mapping by a 300ms timeout
    const delay = setTimeout(loadJobs, 300);
    return () => clearTimeout(delay);
  }, [searchQuery, locationQuery, remoteOnly, jobTypeChecks]);

  const toggleJobType = (id) =>
    setJobTypeChecks((prev) => ({ ...prev, [id]: !prev[id] }));

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: 'Space Grotesk', sans-serif;
          background-color: #ffffff;
          color: #000000;
          -webkit-font-smoothing: antialiased;
        }

        h1, h2, h3, h4 { font-family: 'Syne', sans-serif; text-transform: uppercase; font-weight: 800; letter-spacing: -0.025em; }

        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 600, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-style: normal; font-size: 24px; line-height: 1;
          letter-spacing: normal; text-transform: none;
          display: inline-block; white-space: nowrap; direction: ltr;
        }

        .filter-checkbox {
          width: 20px; height: 20px; border: 2px solid #000000;
          appearance: none; -webkit-appearance: none; cursor: pointer;
          position: relative; background: #ffffff; flex-shrink: 0;
        }
        .filter-checkbox:checked { background-color: #1A4D2E; }
        .filter-checkbox:checked::after {
          content: '✓'; position: absolute; color: white; font-size: 14px;
          font-weight: 900; top: 50%; left: 50%; transform: translate(-50%, -50%);
        }

        .filter-radio {
          width: 20px; height: 20px; border: 2px solid #000000;
          appearance: none; -webkit-appearance: none; cursor: pointer;
          position: relative; background: #ffffff; border-radius: 0; flex-shrink: 0;
        }
        .filter-radio:checked { background-color: #1A4D2E; }
        .filter-radio:checked::after {
          content: ''; position: absolute; width: 8px; height: 8px;
          background: white; top: 50%; left: 50%; transform: translate(-50%, -50%);
        }

        .neo-select {
          width: 100%; border: 3px solid #000000; font-weight: 900;
          padding: 12px; font-size: 0.75rem; text-transform: uppercase;
          letter-spacing: 0.1em; background: #ffffff;
          font-family: 'Space Grotesk', sans-serif; cursor: pointer;
        }
        .neo-select:focus { outline: none; }

        .search-input {
          width: 100%; border: none; outline: none;
          font-size: 1rem; font-weight: 700; padding: 0;
          font-family: 'Space Grotesk', sans-serif; background: transparent;
        }
        .search-input::placeholder { color: rgba(0,0,0,0.3); }

        .social-icon {
          width: 40px; height: 40px; border: 2px solid #374151;
          display: flex; align-items: center; justify-content: center;
          cursor: pointer; transition: all 0.15s ease; background: transparent; color: #ffffff;
        }
        .social-icon:hover { background-color: #D8B4FE; color: #000000; border-color: #D8B4FE; }

        .page-btn {
          width: 44px; height: 44px; border: 2px solid #000000;
          display: flex; align-items: center; justify-content: center;
          font-weight: 900; cursor: pointer; transition: all 0.15s ease;
          font-family: 'Space Grotesk', sans-serif; font-size: 1rem;
        }

        @media (max-width: 1024px) {
          .main-layout { flex-direction: column !important; }
          .sidebar { width: 100% !important; }
          .search-bar-inner { flex-direction: column !important; }
          .h1-hero { font-size: 3rem !important; }
        }

        @media (max-width: 768px) {
          .nav-links { display: none !important; }
          .footer-grid { grid-template-columns: 1fr !important; }
          .footer-bottom { flex-direction: column !important; text-align: center; }
        }
      `}</style>

      {/* ── Navbar ── */}
      <nav style={{ borderBottom: "3px solid #000000", backgroundColor: "#ffffff", position: "sticky", top: 0, zIndex: 50 }}>
        <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "0 24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", height: "80px", alignItems: "center" }}>
            <a href="/" style={{ fontSize: "1.875rem", fontWeight: 800, fontFamily: "'Syne', sans-serif", letterSpacing: "-0.05em", color: "#1A4D2E", textDecoration: "none", display: "flex", alignItems: "center", gap: "4px" }}>
              JOBFOR<span style={{ color: "#D8B4FE" }}>.</span>
            </a>

            <div className="nav-links" style={{ display: "flex", gap: "40px" }}>
              {["Discover", "Companies", "Pricing"].map((l) => (
                <a key={l} href="#" style={{ color: "#000", fontWeight: 700, textTransform: "uppercase", fontSize: "0.875rem", letterSpacing: "0.1em", textDecoration: "none", fontFamily: "'Space Grotesk', sans-serif" }}>{l}</a>
              ))}
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
              <a
                href="/analyzer"
                onMouseEnter={() => setPostJobHover(true)}
                onMouseLeave={() => setPostJobHover(false)}
                style={{ backgroundColor: "#D8B4FE", color: "#000", fontWeight: 700, padding: "10px 32px", border: "3px solid #000", boxShadow: postJobHover ? "none" : "5px 5px 0px 0px #000", transform: postJobHover ? "translate(1px,1px)" : "translate(0,0)", transition: "all 0.15s ease", textTransform: "uppercase", fontSize: "0.875rem", textDecoration: "none", fontFamily: "'Space Grotesk', sans-serif", display: "flex", alignItems: "center", gap: "8px" }}
              >
                <span className="material-symbols-outlined" style={{ fontSize: "16px" }}>analytics</span>
                Analyze Resume
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* ── Hero / Search ── */}
      <header style={{ backgroundColor: "rgba(216,180,254,0.15)", padding: "40px 0", borderBottom: "3px solid #000000" }}>
        <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "0 24px" }}>
          <h1 className="h1-hero" style={{ fontSize: "2.75rem", fontFamily: "'Syne', sans-serif", marginBottom: "32px", lineHeight: 1 }}>
            Find Your{" "}
            <span style={{ backgroundColor: "#1A4D2E", color: "#ffffff", padding: "4px 16px", display: "inline-block", transform: "rotate(-1deg)" }}>
              Perfect Match
            </span>
          </h1>

          <div className="search-bar-inner" style={{ display: "flex", backgroundColor: "#ffffff", border: "2px solid #000000", boxShadow: "3px 3px 0px 0px #000000", overflow: "hidden" }}>
            <div style={{ flex: 1, display: "flex", alignItems: "center", padding: "10px 16px", borderRight: "2px solid #000000" }}>
              <span className="material-symbols-outlined" style={{ fontSize: "1.5rem", marginRight: "12px" }}>search</span>
              <input className="search-input" type="text" placeholder="Job title, keywords, or company" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
            </div>
            <div style={{ flex: 1, display: "flex", alignItems: "center", padding: "10px 16px" }}>
              <span className="material-symbols-outlined" style={{ fontSize: "1.5rem", marginRight: "12px" }}>location_on</span>
              <input className="search-input" type="text" placeholder="Location or 'Remote'" value={locationQuery} onChange={(e) => setLocationQuery(e.target.value)} />
            </div>
            <button
              onMouseEnter={() => setSearchBtnHover(true)}
              onMouseLeave={() => setSearchBtnHover(false)}
              style={{ backgroundColor: searchBtnHover ? "#000000" : "#1A4D2E", color: "#ffffff", fontWeight: 900, padding: "12px 24px", textTransform: "uppercase", letterSpacing: "0.2em", border: "none", borderLeft: "2px solid #000000", cursor: "pointer", transition: "background-color 0.15s ease", fontFamily: "'Space Grotesk', sans-serif", fontSize: "0.875rem" }}
            >
              Search
            </button>
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main style={{ maxWidth: "1280px", margin: "0 auto", padding: "64px 24px" }}>
        <div className="main-layout" style={{ display: "flex", gap: "48px" }}>

          {/* ── Sidebar Filters ── */}
          <aside className="sidebar" style={{ width: "288px", flexShrink: 0, display: "flex", flexDirection: "column", gap: "40px" }}>

            {/* Job Type */}
            <div style={{ backgroundColor: "#ffffff", padding: "16px", border: "3px solid #000000", boxShadow: "5px 5px 0px 0px #000000" }}>
              <h3 style={{ fontSize: "1.25rem", marginBottom: "24px", borderBottom: "3px solid #000000", paddingBottom: "12px", display: "flex", alignItems: "center", justifyContent: "space-between", fontFamily: "'Syne', sans-serif" }}>
                Job Type <span className="material-symbols-outlined" style={{ fontSize: "18px" }}>expand_more</span>
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                {jobTypes.map((jt) => (
                  <label key={jt.id} style={{ display: "flex", alignItems: "center", cursor: "pointer" }}>
                    <input className="filter-checkbox" type="checkbox" checked={jobTypeChecks[jt.id]} onChange={() => toggleJobType(jt.id)} />
                    <span style={{ marginLeft: "16px", fontWeight: 700, fontSize: "0.875rem", textTransform: "uppercase", fontFamily: "'Space Grotesk', sans-serif" }}>{jt.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Experience */}
            <div style={{ backgroundColor: "#ffffff", padding: "16px", border: "3px solid #000000", boxShadow: "5px 5px 0px 0px #000000" }}>
              <h3 style={{ fontSize: "1.25rem", marginBottom: "24px", borderBottom: "3px solid #000000", paddingBottom: "12px", fontFamily: "'Syne', sans-serif" }}>Experience</h3>
              <select className="neo-select" value={experience} onChange={(e) => setExperience(e.target.value)}>
                {experienceLevels.map((lvl) => <option key={lvl} value={lvl}>{lvl}</option>)}
              </select>
            </div>

            {/* Salary */}
            <div style={{ backgroundColor: "#ffffff", padding: "16px", border: "3px solid #000000", boxShadow: "5px 5px 0px 0px #000000" }}>
              <h3 style={{ fontSize: "1.25rem", marginBottom: "24px", borderBottom: "3px solid #000000", paddingBottom: "12px", fontFamily: "'Syne', sans-serif" }}>Salary</h3>
              <input type="range" min="40000" max="150000" step="5000" defaultValue="150000" style={{ width: "100%", height: "12px", accentColor: "#1A4D2E", cursor: "pointer" }} />
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: "16px", fontWeight: 900, fontSize: "0.75rem", textTransform: "uppercase", fontFamily: "'Space Grotesk', sans-serif" }}>
                <span>₹40k</span>
                <span style={{ backgroundColor: "#D8B4FE", padding: "0 8px" }}>Up to ₹150k+</span>
              </div>
            </div>

            {/* Remote */}
            <div style={{ backgroundColor: "#ffffff", padding: "16px", border: "3px solid #000000", boxShadow: "5px 5px 0px 0px #000000" }}>
              <h3 style={{ fontSize: "1.25rem", marginBottom: "24px", borderBottom: "3px solid #000000", paddingBottom: "12px", fontFamily: "'Syne', sans-serif" }}>Remote</h3>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span style={{ fontWeight: 900, fontSize: "0.875rem", textTransform: "uppercase", fontFamily: "'Space Grotesk', sans-serif" }}>Remote Only</span>
                <button
                  onClick={() => setRemoteOnly(!remoteOnly)}
                  style={{ width: "56px", height: "32px", backgroundColor: remoteOnly ? "#1A4D2E" : "#e5e7eb", border: "3px solid #000000", position: "relative", cursor: "pointer", transition: "background-color 0.2s ease", padding: 0 }}
                >
                  <span style={{ position: "absolute", top: "3px", width: "16px", height: "16px", backgroundColor: "#ffffff", border: "2px solid #000000", transition: "left 0.2s ease, right 0.2s ease", ...(remoteOnly ? { right: "3px", left: "auto" } : { left: "3px", right: "auto" }) }} />
                </button>
              </div>
            </div>

            {/* Date Posted */}
            <div style={{ backgroundColor: "#ffffff", padding: "16px", border: "3px solid #000000", boxShadow: "5px 5px 0px 0px #000000" }}>
              <h3 style={{ fontSize: "1.25rem", marginBottom: "24px", borderBottom: "3px solid #000000", paddingBottom: "12px", display: "flex", alignItems: "center", justifyContent: "space-between", fontFamily: "'Syne', sans-serif" }}>
                Date Posted <span className="material-symbols-outlined" style={{ fontSize: "18px" }}>schedule</span>
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                {dateOptions.map((opt) => (
                  <label key={opt.id} style={{ display: "flex", alignItems: "center", cursor: "pointer" }}>
                    <input className="filter-radio" type="radio" name="date_posted" checked={datePosted === opt.id} onChange={() => setDatePosted(opt.id)} />
                    <span style={{ marginLeft: "16px", fontWeight: 700, fontSize: "0.875rem", textTransform: "uppercase", fontFamily: "'Space Grotesk', sans-serif" }}>{opt.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </aside>

          {/* ── Job Listings ── */}
          <section style={{ flex: 1, minWidth: 0 }}>
            {/* Results header */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "40px", flexWrap: "wrap", gap: "16px" }}>
              <p style={{ fontWeight: 900, fontSize: "1.25rem", fontFamily: "'Space Grotesk', sans-serif" }}>
                Found{" "}
                <span style={{ backgroundColor: "#D8B4FE", padding: "2px 8px", border: "2px solid #000", boxShadow: "3px 3px 0px 0px #000", margin: "0 4px" }}>
                  {loading ? "..." : totalJobs}
                </span>
                {" "}opportunities
              </p>
              <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                <span style={{ fontSize: "0.75rem", fontWeight: 900, textTransform: "uppercase", letterSpacing: "0.1em", fontFamily: "'Space Grotesk', sans-serif" }}>Sort:</span>
                <select className="neo-select" value={sortBy} onChange={(e) => setSortBy(e.target.value)} style={{ width: "auto", padding: "8px 16px" }}>
                  {["Newest First", "Most Relevant", "Salary: High to Low"].map((s) => <option key={s}>{s}</option>)}
                </select>
              </div>
            </div>

            {/* Cards */}
            <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
              {loading ? (
                <>
                   <SkeletonCard />
                   <SkeletonCard />
                </>
              ) : jobListings.length > 0 ? (
                jobListings.map((job) => <JobCard key={job.id} job={job} />)
              ) : (
                <div style={{ padding: "40px", textAlign: "center", border: "2px dashed #000" }}>
                  <h3 style={{ fontSize: "1.25rem", fontWeight: 800, fontFamily: "'Syne', sans-serif" }}>No matches found</h3>
                  <p style={{ marginTop: "8px", fontWeight: 700, opacity: 0.6 }}>Try adjusting your search criteria</p>
                </div>
              )}
            </div>

            {/* Pagination */}
            <div style={{ marginTop: "64px", display: "flex", justifyContent: "center", gap: "16px" }}>
              {[1, 2, 3].map((pg) => (
                <button key={pg} className="page-btn" onClick={() => setCurrentPage(pg)}
                  style={{ backgroundColor: currentPage === pg ? "#D8B4FE" : "#ffffff", boxShadow: currentPage === pg ? "none" : "3px 3px 0px 0px #000000", transform: currentPage === pg ? "translate(1px,1px)" : "translate(0,0)" }}
                >
                  {pg}
                </button>
              ))}
              <span style={{ width: "44px", height: "44px", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 900, fontFamily: "'Space Grotesk', sans-serif" }}>...</span>
              <button className="page-btn" style={{ backgroundColor: "#ffffff", boxShadow: "3px 3px 0px 0px #000000" }}>
                <span className="material-symbols-outlined" style={{ fontWeight: 900 }}>chevron_right</span>
              </button>
            </div>
          </section>
        </div>
      </main>

      {/* ── Footer ── */}
      <footer style={{ borderTop: "3px solid #000000", backgroundColor: "#ffffff" }}>
        <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "24px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px" }}>
          <a href="/" style={{ fontSize: "1.5rem", fontWeight: 800, fontFamily: "'Syne', sans-serif", letterSpacing: "-0.05em", color: "#1A4D2E", textDecoration: "none" }}>
            JOBFOR<span style={{ color: "#D8B4FE" }}>.</span>
          </a>
          <div style={{ color: "#000000", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.1em", fontFamily: "'Space Grotesk', sans-serif" }}>
            © 2026 Jobfor. All rights reserved. Made in India with ❤️
          </div>
          <div style={{ display: "flex", gap: "24px" }}>
            {["Terms", "Privacy", "Security"].map((link) => (
              <a key={link} href="#" style={{ color: "#000000", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.1em", textDecoration: "none" }}>
                {link}
              </a>
            ))}
          </div>
        </div>
      </footer>
    </>
  );
}
