import React, { useState } from "react";

// ─── Data ────────────────────────────────────────────────────────────────────

const sideNavItems = [
  { icon: "dashboard", label: "Dashboard" },
  { icon: "work", label: "Jobs" },
  { icon: "analytics", label: "Insights" },
  { icon: "rocket_launch", label: "Big Opps" },
  { icon: "bookmark", label: "Saved" },
  { icon: "check_circle", label: "Applied" },
  { icon: "psychology", label: "AI Coach" },
];

const topNavLinks = [
  { label: "Jobs", active: false },
  { label: "Companies", active: false },
  { label: "Profile", active: true },
];

const initialSkills = [
  { id: 1, name: "Kubernetes", level: "Expert" },
  { id: 2, name: "AWS Ecosystem", level: "Advanced" },
  { id: 3, name: "Terraform", level: "Expert" },
  { id: 4, name: "Python / Go", level: "Advanced" },
  { id: 5, name: "CI/CD Pipeline Design", level: "Expert" },
];

const workExperience = [
  {
    id: 1, current: true,
    title: "Principal Cloud Architect", company: "SkyNet Global Infrastructure",
    period: "Jan 2021 — Present (3 years)",
    bullets: [
      "Led the migration of legacy monolithic systems to a multi-cloud Kubernetes environment, reducing operational costs by 45%.",
      "Designed and maintained 50+ Terraform modules used across the entire engineering organization of 200+ developers.",
    ],
  },
  {
    id: 2, current: false,
    title: "Senior Systems Engineer", company: "Nexus Data Systems",
    period: "Mar 2018 — Dec 2020 (2 years 10 months)",
    bullets: [
      "Automated deployment pipelines using Jenkins and GitLab CI, increasing deployment frequency from weekly to 10+ times daily.",
      "Implemented comprehensive monitoring and alerting using Prometheus and Grafana for high-traffic retail platforms.",
    ],
  },
];

const education = [
  { id: 1, degree: "Master's Degree", field: "Computer Science", school: "Stanford University", info: "Class of 2018 • GPA 3.9/4.0" },
  { id: 2, degree: "Bachelor's Degree", field: "Software Engineering", school: "UC Berkeley", info: "Class of 2016 • Magna Cum Laude" },
];

const targetRoles = [
  { label: "Solutions Architect", selected: true },
  { label: "Infrastructure Lead", selected: true },
  { label: "VP Engineering", selected: false },
  { label: "CTO", selected: false },
];

const locationOptions = [
  { label: "Fully Remote", selected: true },
  { label: "Hybrid (SF)", selected: false },
  { label: "Hybrid (NYC)", selected: false },
  { label: "On-Site", selected: false },
];

const resumes = [
  { id: 1, name: "Alex_Chen_Cloud_Arch_2024.pdf", isDefault: true, date: null },
  { id: 2, name: "Alex_Chen_CTO_Tailored.pdf", isDefault: false, date: "Uploaded Oct 2023" },
];

// ─── Component ────────────────────────────────────────────────────────────────

export default function EditProfile() {
  const [skills, setSkills] = useState(initialSkills);
  const [roles, setRoles] = useState(targetRoles);
  const [locations, setLocations] = useState(locationOptions);
  const [form, setForm] = useState({
    name: "Alex Chen",
    location: "San Francisco, CA",
    headline: "Senior Cloud Architect | Scalable Infrastructure Specialist",
    linkedin: "alexchen-cloud",
    portfolio: "https://alexchen.dev",
  });

  const [saveHover, setSaveHover] = useState(false);
  const [saveActive, setSaveActive] = useState(false);
  const [discardHover, setDiscardHover] = useState(false);
  const [addRoleHover, setAddRoleHover] = useState(false);
  const [postJobHover, setPostJobHover] = useState(false);

  const removeSkill = (id) => setSkills((prev) => prev.filter((s) => s.id !== id));
  const toggleRole = (idx) => setRoles((prev) => prev.map((r, i) => (i === idx ? { ...r, selected: !r.selected } : r)));
  const toggleLocation = (idx) => setLocations((prev) => prev.map((l, i) => ({ ...l, selected: i === idx })));
  const handleChange = (field) => (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const inputStyle = {
    backgroundColor: "#ffffff", border: "4px solid #1a1c1c", padding: "12px",
    fontWeight: 700, outline: "none", fontFamily: "'Inter', sans-serif",
    fontSize: "1rem", color: "#1a1c1c", width: "100%", borderRadius: 0,
    transition: "box-shadow 0.15s ease",
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700;900&family=Inter:wght@400;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body { font-family: 'Inter', sans-serif; background-color: #f9f9f9; color: #1a1c1c; }
        h1, h2, h3 { font-family: 'Lexend', sans-serif; }

        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-size: 24px; line-height: 1; display: inline-block; direction: ltr;
        }

        ::selection { background-color: #2d5bff; color: #fff; }

        .neo-input:focus { box-shadow: 4px 4px 0px 0px #2D5BFF; }

        .sidebar-link {
          display: flex; align-items: center; gap: 16px; padding: 12px;
          font-family: 'Lexend', sans-serif; font-weight: 700; font-size: 0.875rem;
          text-transform: uppercase; letter-spacing: 0.1em; color: #1a1c1c;
          text-decoration: none; transition: all 0.1s ease; cursor: pointer;
          border: none; background: none; width: 100%;
        }
        .sidebar-link:hover { background-color: #D4BFFF; transform: translateX(4px); }
        .sidebar-link:active { transform: scale(0.95); }

        .section-card { background-color: #f9f9f9; border: 4px solid #1a1c1c; padding: 32px; box-shadow: 8px 8px 0px 0px rgba(0,0,0,1); }

        .skill-tag {
          display: flex; align-items: center; justify-content: space-between;
          background-color: #eaddff; border: 4px solid #1a1c1c;
          padding: 16px; box-shadow: 4px 4px 0px 0px rgba(0,0,0,1);
        }

        .icon-btn {
          padding: 8px; border: 2px solid #1a1c1c; background: transparent;
          cursor: pointer; display: flex; align-items: center; justify-content: center;
          transition: background-color 0.15s ease;
        }
        .icon-btn:hover { background-color: #e8e8e8; }
        .icon-btn-danger:hover { background-color: #ffdad6; color: #ba1a1a; }

        .top-link {
          font-weight: 700; text-decoration: none; padding: 4px 12px;
          transition: background-color 0.15s ease; font-family: 'Inter', sans-serif;
        }
        .top-link:hover { background-color: #D4BFFF; }

        @media (max-width: 1024px) {
          .sidebar { display: none !important; }
          .main-content { margin-left: 0 !important; }
          .bottom-bar { left: 0 !important; }
        }

        @media (max-width: 768px) {
          .top-nav-links { display: none !important; }
          .section-grid-2 { grid-template-columns: 1fr !important; }
          .section-grid-3 { grid-template-columns: 1fr !important; }
          .basic-grid { grid-template-columns: 1fr !important; }
          .resume-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>

      {/* ── Top Header ── */}
      <header style={{ position: "fixed", top: 0, width: "100%", zIndex: 50, display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 32px", height: "80px", backgroundColor: "#ffffff", borderBottom: "4px solid #1a1c1c", boxShadow: "4px 4px 0px 0px rgba(0,0,0,1)" }}>
        <div style={{ fontSize: "1.5rem", fontWeight: 900, textTransform: "uppercase", letterSpacing: "-0.05em", color: "#1B3D2F", fontFamily: "'Lexend', sans-serif" }}>
          Career Manifesto
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
          <div className="top-nav-links" style={{ display: "flex", gap: "32px" }}>
            {topNavLinks.map((link) => (
              <a key={link.label} href="#" className="top-link" style={{ color: link.active ? "#2D5BFF" : "#1a1c1c", fontWeight: link.active ? 900 : 700, textDecoration: link.active ? "underline" : "none", textDecorationThickness: link.active ? "4px" : undefined }}>
                {link.label}
              </a>
            ))}
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <span className="material-symbols-outlined" style={{ fontSize: "2rem", cursor: "pointer" }}>search</span>
            <span className="material-symbols-outlined" style={{ fontSize: "2rem", cursor: "pointer" }}>notifications</span>
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBVDul7LZBkrrNeh-RW3pF2jxqrYFulpgFY700jl_r6-zpGSccec5jLkR7kb8AvhksbPpLHAgU2h363mSxfO53pS4E35pON8YQH2B83nUhWx_evJLWN8Mh1R9owp8ODuahL-FIqqngd24rjCj1VobYl0B38PGy36rw_fIWL_v-k6PMJwt-U7FVPD86V8XJ9kurEsNAaSGwCCpIhagKJQ5LUkZZp_5wSePdRPua5n-yUR4VcOi6otqrZ1py70S3G_chcHLXrYLayQiU" alt="User" style={{ width: 40, height: 40, border: "2px solid #1a1c1c", objectFit: "cover" }} />
          </div>
        </div>
      </header>

      <div style={{ display: "flex", paddingTop: "80px", minHeight: "100vh" }}>
        {/* ── Sidebar ── */}
        <aside className="sidebar" style={{ position: "fixed", left: 0, top: "80px", width: "288px", height: "calc(100vh - 80px)", display: "flex", flexDirection: "column", padding: "24px", gap: "8px", backgroundColor: "#f9f9f9", borderRight: "4px solid #1a1c1c", overflowY: "auto", zIndex: 40 }}>
          {/* User info */}
          <div style={{ marginBottom: "32px", display: "flex", alignItems: "center", gap: "16px" }}>
            <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuALjzLqlPmSkGYDdF1k9NwmrsCAIswWocv3NrpGYGy5rGy9PBBbhxuCyGqge_pxRP7NchIxGcyhf6dwQQC495SeoYy0Gb6HZczRDnsR4jQrt15A8Wn3F5uGiBVbFKEXXMV86b7p1a0SaIT_ahRTFhxJyNIHiVCvFBnbeovDdFbWlX9IA3j5Eht_p6gEHTdJw_bkCZKLiewAoALNLzB7mPtz48X3pljhngpK14yRCKxdFVnc90XaFwoJDVaGfApiub7R9Ug62mXkz60" alt="User" style={{ width: 48, height: 48, border: "2px solid #1a1c1c", objectFit: "cover" }} />
            <div>
              <h3 style={{ fontFamily: "'Lexend', sans-serif", fontWeight: 900, fontSize: "0.875rem", color: "#1a1c1c" }}>Alex Chen</h3>
              <p style={{ fontSize: "0.75rem", opacity: 0.6 }}>Senior Architect</p>
            </div>
          </div>

          <nav style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {sideNavItems.map((item) => (
              <button key={item.label} className="sidebar-link">
                <span className="material-symbols-outlined">{item.icon}</span>
                {item.label}
              </button>
            ))}
            <button className="sidebar-link" style={{ backgroundColor: "#2D5BFF", color: "#ffffff", border: "2px solid #1a1c1c", boxShadow: "4px 4px 0px 0px rgba(0,0,0,1)" }}>
              <span className="material-symbols-outlined">settings</span>
              Settings
            </button>
          </nav>

          <button
            onMouseEnter={() => setPostJobHover(true)}
            onMouseLeave={() => setPostJobHover(false)}
            style={{ marginTop: "auto", backgroundColor: "#03271a", color: "#ffffff", border: "4px solid #1a1c1c", padding: "16px", fontFamily: "'Lexend', sans-serif", fontWeight: 900, textTransform: "uppercase", cursor: "pointer", boxShadow: postJobHover ? "none" : "4px 4px 0px 0px rgba(0,0,0,1)", transform: postJobHover ? "translate(2px,2px)" : "translate(0,0)", transition: "all 0.15s ease", fontSize: "0.875rem" }}
          >
            Post a Job
          </button>
        </aside>

        {/* ── Main ── */}
        <main className="main-content" style={{ flex: 1, marginLeft: "288px", padding: "48px", backgroundColor: "#f9f9f9", paddingBottom: "160px" }}>
          <div style={{ maxWidth: "1024px", margin: "0 auto" }}>
            {/* Page Header */}
            <div style={{ marginBottom: "48px" }}>
              <h1 style={{ fontSize: "3rem", fontWeight: 900, color: "#03271a", lineHeight: 1.1, marginBottom: "24px", fontFamily: "'Lexend', sans-serif" }}>
                Edit Your Professional Profile
              </h1>
              <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
                <div style={{ flex: 1, height: "32px", backgroundColor: "#e2e2e2", border: "4px solid #1a1c1c", position: "relative", overflow: "hidden" }}>
                  <div style={{ position: "absolute", inset: 0, backgroundColor: "#D4BFFF", width: "78%", borderRight: "4px solid #1a1c1c" }} />
                </div>
                <span style={{ fontSize: "1.5rem", fontWeight: 900, fontFamily: "'Lexend', sans-serif", whiteSpace: "nowrap" }}>78% Complete</span>
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "64px" }}>

              {/* ── 01. Basic Information ── */}
              <section className="section-card">
                <h2 style={{ fontSize: "1.5rem", fontWeight: 900, marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px", display: "inline-block", fontFamily: "'Lexend', sans-serif" }}>
                  01. Basic Information
                </h2>
                <div className="basic-grid" style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: "32px" }}>
                  {/* Photo */}
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                    <div style={{ width: "192px", height: "192px", border: "4px solid #1a1c1c", position: "relative", marginBottom: "16px" }}>
                      <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBLf0NqjGey0Cx1zDVZ_FTgTMQH9xH08saHy0Mk6qONEOEaZBbroTlR5UQZ1KhbK0hHqyt5xAaHxGba2fwWKs54FWEyjxIgFcmPF7hGmU6IL6R-AY5-cVjkHS5eWyr-fhbBO45B48WhQBjPwK1fftKJgm6hJ60L-lNGZ4oyh6k5YA3EChIJJL8fwS2i2PD8MYEkxEgkaMZfBIolIrzaHi5__KuZb_JJJkQoNUwODmfDDRHkryX1zefWBz3VOmNsaPSRnu4eTeyC_ZQ" alt="Profile" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                      <button style={{ position: "absolute", bottom: "-16px", right: "-16px", backgroundColor: "#2d5bff", color: "#ffffff", border: "4px solid #1a1c1c", padding: "12px", boxShadow: "4px 4px 0px 0px rgba(0,0,0,1)", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>
                        <span className="material-symbols-outlined">edit</span>
                      </button>
                    </div>
                    <p style={{ fontSize: "0.75rem", fontWeight: 700, textTransform: "uppercase", opacity: 0.6 }}>Upload new photo</p>
                  </div>

                  {/* Fields */}
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
                    {[
                      { label: "Full Name", field: "name", span: false },
                      { label: "Location", field: "location", span: false },
                      { label: "Professional Headline", field: "headline", span: true },
                    ].map(({ label, field, span }) => (
                      <div key={field} style={{ gridColumn: span ? "span 2" : undefined, display: "flex", flexDirection: "column", gap: "8px" }}>
                        <label style={{ fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", fontFamily: "'Lexend', sans-serif" }}>{label}</label>
                        <input className="neo-input" style={inputStyle} value={form[field]} onChange={handleChange(field)} />
                      </div>
                    ))}

                    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                      <label style={{ fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", fontFamily: "'Lexend', sans-serif" }}>LinkedIn URL</label>
                      <div style={{ display: "flex" }}>
                        <span style={{ backgroundColor: "#e2e2e2", borderTop: "4px solid #1a1c1c", borderBottom: "4px solid #1a1c1c", borderLeft: "4px solid #1a1c1c", padding: "12px", fontWeight: 700 }}>in/</span>
                        <input className="neo-input" style={inputStyle} value={form.linkedin} onChange={handleChange("linkedin")} />
                      </div>
                    </div>

                    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                      <label style={{ fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", fontFamily: "'Lexend', sans-serif" }}>Portfolio URL</label>
                      <input className="neo-input" style={inputStyle} value={form.portfolio} onChange={handleChange("portfolio")} />
                    </div>
                  </div>
                </div>
              </section>

              {/* ── 02. Expert Skills ── */}
              <section className="section-card">
                <h2 style={{ fontSize: "1.5rem", fontWeight: 900, marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px", display: "inline-block", fontFamily: "'Lexend', sans-serif" }}>
                  02. Expert Skills
                </h2>
                <div className="section-grid-3" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
                  {skills.map((skill) => (
                    <div key={skill.id} className="skill-tag">
                      <div>
                        <span style={{ fontWeight: 900, display: "block", textTransform: "uppercase", fontSize: "0.875rem", fontFamily: "'Lexend', sans-serif" }}>{skill.name}</span>
                        <span style={{ fontSize: "0.625rem", backgroundColor: "#1a1c1c", color: "#ffffff", padding: "2px 8px", fontWeight: 700, textTransform: "uppercase" }}>{skill.level}</span>
                      </div>
                      <button onClick={() => removeSkill(skill.id)} style={{ background: "none", border: "none", cursor: "pointer", padding: 0 }}>
                        <span className="material-symbols-outlined">close</span>
                      </button>
                    </div>
                  ))}
                  <button
                    style={{ border: "4px dashed #1a1c1c", padding: "16px", fontWeight: 900, display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", cursor: "pointer", backgroundColor: "transparent", fontFamily: "'Inter', sans-serif", fontSize: "0.875rem", transition: "background-color 0.15s ease" }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#e8e8e8")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                  >
                    <span className="material-symbols-outlined">add_circle</span>
                    Add More
                  </button>
                </div>
              </section>

              {/* ── 03. Work Experience ── */}
              <section className="section-card">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px" }}>
                  <h2 style={{ fontSize: "1.5rem", fontWeight: 900, fontFamily: "'Lexend', sans-serif" }}>03. Work Experience</h2>
                  <button
                    onMouseEnter={() => setAddRoleHover(true)}
                    onMouseLeave={() => setAddRoleHover(false)}
                    style={{ backgroundColor: "#2d5bff", color: "#ffffff", border: "4px solid #1a1c1c", padding: "8px 16px", fontWeight: 900, boxShadow: addRoleHover ? "none" : "4px 4px 0px 0px rgba(0,0,0,1)", transform: addRoleHover ? "translate(2px,2px)" : "translate(0,0)", fontSize: "0.875rem", textTransform: "uppercase", display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", transition: "all 0.15s ease", fontFamily: "'Lexend', sans-serif" }}
                  >
                    <span className="material-symbols-outlined" style={{ fontSize: "18px" }}>add</span>
                    Add Role
                  </button>
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
                  {workExperience.map((role) => (
                    <div key={role.id} style={{ border: "4px solid #1a1c1c", padding: "24px", backgroundColor: "#ffffff", position: "relative" }}>
                      {role.current && (
                        <div style={{ position: "absolute", top: "-12px", left: "-12px", backgroundColor: "#03271a", color: "#ffffff", padding: "4px 12px", fontWeight: 900, fontSize: "0.75rem", textTransform: "uppercase", border: "2px solid #1a1c1c", fontFamily: "'Lexend', sans-serif" }}>
                          Current
                        </div>
                      )}
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
                        <div>
                          <h3 style={{ fontSize: "1.25rem", fontWeight: 900, textTransform: "uppercase", fontFamily: "'Lexend', sans-serif", marginBottom: "4px" }}>{role.title}</h3>
                          <p style={{ fontWeight: 700, color: "#0040df" }}>{role.company}</p>
                          <p style={{ fontSize: "0.875rem", fontWeight: 700, opacity: 0.6, textTransform: "uppercase", marginTop: "4px" }}>{role.period}</p>
                        </div>
                        <div style={{ display: "flex", gap: "8px" }}>
                          <button className="icon-btn"><span className="material-symbols-outlined" style={{ fontSize: "20px" }}>edit</span></button>
                          <button className="icon-btn icon-btn-danger"><span className="material-symbols-outlined" style={{ fontSize: "20px" }}>delete</span></button>
                        </div>
                      </div>
                      <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "12px" }}>
                        {role.bullets.map((b, i) => (
                          <li key={i} style={{ display: "flex", gap: "12px", fontWeight: 500 }}>
                            <span style={{ color: "#03271a", fontWeight: 900, marginTop: "4px" }}>→</span>
                            <span>{b}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </section>

              {/* ── 04. Education ── */}
              <section className="section-card">
                <h2 style={{ fontSize: "1.5rem", fontWeight: 900, marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px", display: "inline-block", fontFamily: "'Lexend', sans-serif" }}>
                  04. Education
                </h2>
                <div className="section-grid-2" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px" }}>
                  {education.map((edu) => (
                    <div key={edu.id} style={{ border: "4px solid #1a1c1c", padding: "24px", backgroundColor: "#f4f3f3", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                      <div>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "16px" }}>
                          <span style={{ backgroundColor: "#1a1c1c", color: "#fff", padding: "4px 12px", fontWeight: 900, fontSize: "0.75rem", textTransform: "uppercase" }}>{edu.degree}</span>
                          <button style={{ background: "none", border: "none", cursor: "pointer" }}><span className="material-symbols-outlined" style={{ fontSize: "20px" }}>edit</span></button>
                        </div>
                        <h3 style={{ fontSize: "1.25rem", fontWeight: 900, textTransform: "uppercase", fontFamily: "'Lexend', sans-serif" }}>{edu.field}</h3>
                        <p style={{ fontWeight: 700 }}>{edu.school}</p>
                      </div>
                      <p style={{ fontSize: "0.875rem", fontWeight: 900, opacity: 0.6, textTransform: "uppercase", marginTop: "24px", letterSpacing: "0.05em" }}>{edu.info}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* ── 05. Preferences ── */}
              <section className="section-card">
                <h2 style={{ fontSize: "1.5rem", fontWeight: 900, marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px", display: "inline-block", fontFamily: "'Lexend', sans-serif" }}>
                  05. Preferences
                </h2>
                <div style={{ display: "flex", flexDirection: "column", gap: "40px" }}>
                  {/* Target Roles */}
                  <div>
                    <label style={{ display: "block", fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", marginBottom: "16px", fontFamily: "'Lexend', sans-serif" }}>Target Job Roles</label>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
                      {roles.map((role, i) => (
                        <button key={role.label} onClick={() => toggleRole(i)} style={{ padding: "8px 24px", border: "2px solid #1a1c1c", backgroundColor: role.selected ? "#D4BFFF" : "#ffffff", fontWeight: role.selected ? 900 : 700, boxShadow: role.selected ? "4px 4px 0px 0px rgba(0,0,0,1)" : "none", cursor: "pointer", transition: "all 0.15s ease", fontFamily: "'Inter', sans-serif", fontSize: "0.875rem" }}>
                          {role.label}
                        </button>
                      ))}
                      <button style={{ padding: "8px 24px", border: "2px solid #1a1c1c", backgroundColor: "#ffffff", fontWeight: 700, cursor: "pointer", fontFamily: "'Inter', sans-serif", fontSize: "0.875rem" }}>+ Add more</button>
                    </div>
                  </div>

                  <div className="section-grid-2" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "48px" }}>
                    {/* Location */}
                    <div>
                      <label style={{ display: "block", fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", marginBottom: "16px", fontFamily: "'Lexend', sans-serif" }}>Preferred Location</label>
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                        {locations.map((loc, i) => (
                          <div key={loc.label} onClick={() => toggleLocation(i)} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "16px", border: "4px solid #1a1c1c", backgroundColor: loc.selected ? "#ffffff" : "#f9f9f9", cursor: "pointer" }}>
                            <div style={{ width: "24px", height: "24px", border: "4px solid #1a1c1c", backgroundColor: loc.selected ? "#2d5bff" : "#ffffff", flexShrink: 0 }} />
                            <span style={{ fontWeight: 700, textTransform: "uppercase", fontSize: "0.75rem", opacity: loc.selected ? 1 : 0.6 }}>{loc.label}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Salary */}
                    <div>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
                        <label style={{ fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem", fontFamily: "'Lexend', sans-serif" }}>Target Annual Salary</label>
                        <span style={{ fontWeight: 900, color: "#0040df", fontSize: "1.5rem", fontFamily: "'Lexend', sans-serif" }}>₹185k - ₹240k+</span>
                      </div>
                      <div style={{ position: "relative", height: "16px", backgroundColor: "#e2e2e2", border: "2px solid #1a1c1c", marginBottom: "16px" }}>
                        <div style={{ position: "absolute", top: 0, bottom: 0, left: "25%", right: "20%", backgroundColor: "#0040df", borderLeft: "2px solid #1a1c1c", borderRight: "2px solid #1a1c1c" }} />
                        {[25, 80].map((pos) => (
                          <div key={pos} style={{ position: "absolute", top: "50%", left: `${pos}%`, transform: "translate(-50%, -50%)", width: "32px", height: "32px", backgroundColor: "#ffffff", border: "4px solid #1a1c1c", boxShadow: "2px 2px 0px 0px rgba(0,0,0,1)", cursor: "pointer" }} />
                        ))}
                      </div>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.625rem", fontWeight: 900, textTransform: "uppercase", opacity: 0.6 }}>
                        {["₹80k", "₹150k", "₹220k", "₹300k+"].map((v) => <span key={v}>{v}</span>)}
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              {/* ── 06. Resumes ── */}
              <section className="section-card">
                <h2 style={{ fontSize: "1.5rem", fontWeight: 900, marginBottom: "32px", borderBottom: "4px solid #1a1c1c", paddingBottom: "8px", display: "inline-block", fontFamily: "'Lexend', sans-serif" }}>
                  06. Resumes
                </h2>
                <div className="resume-grid" style={{ display: "grid", gridTemplateColumns: "5fr 7fr", gap: "32px" }}>
                  {/* Upload zone */}
                  <div
                    style={{ border: "4px dashed #1a1c1c", backgroundColor: "#f4f3f3", padding: "32px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", cursor: "pointer", transition: "background-color 0.15s ease" }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#ffffff")}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#f4f3f3")}
                  >
                    <span className="material-symbols-outlined" style={{ fontSize: "3rem", marginBottom: "16px" }}>cloud_upload</span>
                    <p style={{ fontWeight: 900, textTransform: "uppercase", marginBottom: "8px" }}>Drop your new CV here</p>
                    <p style={{ fontSize: "0.75rem", fontWeight: 700, opacity: 0.6, textTransform: "uppercase" }}>PDF, DOCX up to 10MB</p>
                    <button style={{ marginTop: "24px", padding: "8px 24px", backgroundColor: "#03271a", color: "#ffffff", fontWeight: 900, border: "4px solid #1a1c1c", boxShadow: "4px 4px 0px 0px rgba(0,0,0,1)", fontSize: "0.75rem", textTransform: "uppercase", cursor: "pointer", fontFamily: "'Lexend', sans-serif" }}>
                      Choose File
                    </button>
                  </div>

                  {/* Resume list */}
                  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                    {resumes.map((resume) => (
                      <div key={resume.id} style={{ border: "4px solid #1a1c1c", padding: "16px", backgroundColor: resume.isDefault ? "#ffffff" : "#f9f9f9", display: "flex", alignItems: "center", justifyContent: "space-between", boxShadow: resume.isDefault ? "4px 4px 0px 0px rgba(0,0,0,1)" : "none" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "16px", opacity: resume.isDefault ? 1 : 0.7 }}>
                          <span className="material-symbols-outlined" style={{ fontSize: "2rem", color: resume.isDefault ? "#03271a" : "#1a1c1c" }}>description</span>
                          <div>
                            <p style={{ fontWeight: 900, textTransform: "uppercase", fontSize: "0.875rem" }}>{resume.name}</p>
                            <p style={{ fontSize: "0.625rem", fontWeight: 700, textTransform: "uppercase", color: resume.isDefault ? "#0040df" : "#1a1c1c" }}>{resume.isDefault ? "Default Resume" : resume.date}</p>
                          </div>
                        </div>
                        <div style={{ display: "flex", gap: "8px" }}>
                          {resume.isDefault ? (
                            <button className="icon-btn"><span className="material-symbols-outlined" style={{ fontSize: "18px" }}>download</span></button>
                          ) : (
                            <button style={{ padding: "4px 12px", border: "2px solid #1a1c1c", fontWeight: 900, fontSize: "0.625rem", textTransform: "uppercase", background: "transparent", cursor: "pointer", fontFamily: "'Lexend', sans-serif" }}>Set Default</button>
                          )}
                          <button className="icon-btn icon-btn-danger"><span className="material-symbols-outlined" style={{ fontSize: "18px" }}>delete</span></button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </section>
            </div>
          </div>
        </main>
      </div>

      {/* ── Bottom Action Bar ── */}
      <div className="bottom-bar" style={{ position: "fixed", bottom: 0, left: "288px", right: 0, backgroundColor: "#ffffff", borderTop: "4px solid #1a1c1c", padding: "24px", display: "flex", justifyContent: "flex-end", gap: "24px", zIndex: 40 }}>
        <button
          onMouseEnter={() => setDiscardHover(true)}
          onMouseLeave={() => setDiscardHover(false)}
          style={{ padding: "16px 40px", fontWeight: 900, textTransform: "uppercase", letterSpacing: "0.1em", border: "4px solid #1a1c1c", backgroundColor: discardHover ? "#f4f3f3" : "transparent", cursor: "pointer", fontFamily: "'Lexend', sans-serif", fontSize: "0.875rem", transition: "background-color 0.15s ease" }}
        >
          Discard Changes
        </button>
        <button
          onMouseEnter={() => setSaveHover(true)}
          onMouseLeave={() => { setSaveHover(false); setSaveActive(false); }}
          onMouseDown={() => setSaveActive(true)}
          onMouseUp={() => setSaveActive(false)}
          style={{ padding: "16px 40px", fontWeight: 900, textTransform: "uppercase", letterSpacing: "0.1em", backgroundColor: "#03271a", color: "#ffffff", border: "4px solid #1a1c1c", boxShadow: saveActive ? "none" : "4px 4px 0px 0px rgba(0,0,0,1)", transform: saveActive ? "translate(4px,4px)" : "translate(0,0)", cursor: "pointer", fontFamily: "'Lexend', sans-serif", fontSize: "0.875rem", transition: "all 0.15s ease" }}
        >
          Save Profile
        </button>
      </div>
    </>
  );
}
