import React, { useState } from "react";

// ─── Data ────────────────────────────────────────────────────────────────────

const billingHistory = [
  { date: "Sep 24, 2026", invoiceId: "INV-88210-JF", amount: "₹29.00", status: "Paid" },
  { date: "Aug 24, 2026", invoiceId: "INV-77102-JF", amount: "₹29.00", status: "Paid" },
  { date: "Jul 24, 2026", invoiceId: "INV-66044-JF", amount: "₹29.00", status: "Paid" },
];

const languages = ["English (US)", "German", "French"];

const digestOptions = [
  { id: "daily", label: "Daily Updates" },
  { id: "weekly", label: "Weekly Summary" },
];

// ─── Component ────────────────────────────────────────────────────────────────

export default function SettingsPage() {
  const [form, setForm] = useState({
    fullName: "Alexander Sterling",
    username: "asterling_dev",
    email: "alexander.s@jobfor.tech",
  });
  const [twoFactor, setTwoFactor] = useState(true);
  const [theme, setTheme] = useState("light");
  const [language, setLanguage] = useState("English (US)");
  const [digest, setDigest] = useState("daily");

  const [saveHover, setSaveHover] = useState(false);
  const [changePhotoHover, setChangePhotoHover] = useState(false);
  const [manageBillingHover, setManageBillingHover] = useState(false);
  const [cancelHover, setCancelHover] = useState(false);

  const handleChange = (field) => (e) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const inputStyle = {
    width: "100%",
    padding: "16px",
    border: "2px solid #000000",
    backgroundColor: "#ffffff",
    fontFamily: "'Inter', sans-serif",
    fontSize: "1rem",
    fontWeight: 600,
    outline: "none",
    transition: "border-color 0.15s ease",
    borderRadius: 0,
  };

  return (
    <>
      <style>{`
        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-size: 24px; line-height: 1; display: inline-block; direction: ltr;
          flex-shrink: 0;
        }

        .toggle-track {
          width: 64px;
          height: 32px;
          background-color: #000000;
          border: 2px solid #000000;
          display: flex;
          align-items: center;
          padding: 4px;
          cursor: pointer;
          transition: background-color 0.2s ease;
        }

        .toggle-thumb {
          width: 24px;
          height: 24px;
          background-color: #D8B4FE;
          border: 2px solid #000000;
          transition: transform 0.2s ease;
        }

        .toggle-track.off .toggle-thumb {
          background-color: #e2e2e2;
        }

        .toggle-track.on .toggle-thumb {
          transform: translateX(32px);
        }

        .theme-btn {
          flex: 1;
          padding: 8px;
          font-weight: 900;
          cursor: pointer;
          transition: all 0.15s ease;
          border: none;
          font-family: 'Lexend', sans-serif;
        }

        .theme-btn.active {
          background-color: #1A4D2E;
          color: #ffffff;
        }

        .theme-btn:not(.active) {
          background-color: #e2e2e2;
          color: #000000;
          border-left: 2px solid #000000;
        }

        .radio-custom {
          width: 20px;
          height: 20px;
          border: 2px solid #000000;
          appearance: none;
          -webkit-appearance: none;
          cursor: pointer;
          border-radius: 0;
          background: #ffffff;
          flex-shrink: 0;
        }

        .radio-custom:checked {
          background-color: #1A4D2E;
        }

        @media (max-width: 1024px) {
          .bento-grid { grid-template-columns: 1fr !important; }
          .security-membership { grid-template-columns: 1fr !important; }
          .preferences-grid { grid-template-columns: 1fr !important; }
        }

        @media (max-width: 768px) {
          .form-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>


      <main
          style={{
            flex: 1,
            padding: "32px",
          }}
        >
          <div style={{ maxWidth: "1024px", margin: "0 auto", display: "flex", flexDirection: "column", gap: "48px" }}>

            {/* ── Account Settings Section ── */}
            <section>
              <header style={{ marginBottom: "24px" }}>
                <h2
                  style={{
                    fontSize: "2rem",
                    fontWeight: 900,
                    textTransform: "uppercase",
                    letterSpacing: "-0.025em",
                    fontFamily: "'Syne', sans-serif",
                  }}
                >
                  Account Settings
                </h2>
                <div style={{ height: "6px", width: "128px", backgroundColor: "#D8B4FE", marginTop: "8px" }} />
              </header>

              <div
                className="bento-grid"
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 2fr",
                  gap: "24px",
                }}
              >
                {/* Profile Photo Card */}
                <div
                  style={{
                    backgroundColor: "#ffffff",
                    border: "2px solid #000000",
                    padding: "24px",
                    boxShadow: "4px 4px 0px 0px #000000",
                    position: "relative",
                  }}
                >
                  <div
                    style={{
                      width: "128px",
                      height: "128px",
                      border: "2px solid #000000",
                      margin: "0 auto 24px auto",
                      backgroundColor: "#eeeeed",
                      overflow: "hidden",
                    }}
                  >
                    <img
                      src="https://lh3.googleusercontent.com/aida-public/AB6AXuALjzLqlPmSkGYDdF1k9NwmrsCAIswWocv3NrpGYGy5rGy9PBBbhxuCyGqge_pxRP7NchIxGcyhf6dwQQC495SeoYy0Gb6HZczRDnsR4jQrt15A8Wn3F5uGiBVbFKEXXMV86b7p1a0SaIT_ahRTFhxJyNIHiVCvFBnbeovDdFbWlX9IA3j5Eht_p6gEHTdJw_bkCZKLiewAoALNLzB7mPtz48X3pljhngpK14yRCKxdFVnc90XaFwoJDVaGfApiub7R9Ug62mXkz60"
                      alt="Profile"
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>

                  <button
                    onMouseEnter={() => setChangePhotoHover(true)}
                    onMouseLeave={() => setChangePhotoHover(false)}
                    style={{
                      width: "100%",
                      backgroundColor: "#D8B4FE",
                      color: "#000000",
                      fontWeight: 900,
                      padding: "12px",
                      border: "2px solid #000000",
                      boxShadow: changePhotoHover ? "none" : "4px 4px 0px 0px #000000",
                      transform: changePhotoHover ? "translate(2px,2px)" : "translate(0,0)",
                      cursor: "pointer",
                      textTransform: "uppercase",
                      transition: "all 0.15s ease",
                      fontFamily: "'Space Grotesk', sans-serif",
                      fontSize: "0.875rem",
                    }}
                  >
                    Change Photo
                  </button>

                  <p
                    style={{
                      textAlign: "center",
                      fontSize: "0.75rem",
                      marginTop: "16px",
                      fontWeight: 700,
                      textTransform: "uppercase",
                      letterSpacing: "0.1em",
                      color: "#414844",
                    }}
                  >
                    JPG, PNG or GIF. Max 5MB.
                  </p>
                </div>

                {/* Form Card */}
                <div
                  style={{
                    backgroundColor: "#ffffff",
                    border: "2px solid #000000",
                    padding: "24px",
                    boxShadow: "4px 4px 0px 0px #000000"
                  }}
                >
                  <div
                    className="form-grid"
                    style={{
                      display: "grid",
                      gridTemplateColumns: "1fr 1fr",
                      gap: "24px",
                    }}
                  >
                    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                      <label
                        style={{
                          fontWeight: 900,
                          textTransform: "uppercase",
                          fontSize: "0.875rem",
                          fontFamily: "'Syne', sans-serif",
                        }}
                      >
                        Full Name
                      </label>
                      <input
                        style={inputStyle}
                        value={form.fullName}
                        onChange={handleChange("fullName")}
                      />
                    </div>

                    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                      <label
                        style={{
                          fontWeight: 900,
                          textTransform: "uppercase",
                          fontSize: "0.875rem",
                          fontFamily: "'Syne', sans-serif",
                        }}
                      >
                        Username
                      </label>
                      <input
                        style={inputStyle}
                        value={form.username}
                        onChange={handleChange("username")}
                      />
                    </div>

                    <div style={{ gridColumn: "span 2", display: "flex", flexDirection: "column", gap: "8px" }}>
                      <label
                        style={{
                          fontWeight: 900,
                          textTransform: "uppercase",
                          fontSize: "0.875rem",
                          fontFamily: "'Syne', sans-serif",
                        }}
                      >
                        Email Address
                      </label>
                      <input
                        type="email"
                        style={inputStyle}
                        value={form.email}
                        onChange={handleChange("email")}
                      />
                    </div>
                  </div>

                  <div style={{ marginTop: "32px", display: "flex", justifyContent: "flex-end" }}>
                    <button
                      onMouseEnter={() => setSaveHover(true)}
                      onMouseLeave={() => setSaveHover(false)}
                      style={{
                        padding: "12px 32px",
                        backgroundColor: "#1A4D2E",
                        color: "#ffffff",
                        fontWeight: 900,
                        border: "2px solid #000000",
                        boxShadow: saveHover ? "none" : "4px 4px 0px 0px #000000",
                        transform: saveHover ? "translate(2px,2px)" : "translate(0,0)",
                        cursor: "pointer",
                        textTransform: "uppercase",
                        transition: "all 0.15s ease",
                        fontFamily: "'Space Grotesk', sans-serif",
                        fontSize: "0.875rem",
                      }}
                    >
                      Save Changes
                    </button>
                  </div>
                </div>
              </div>
            </section>

            {/* ── Security & Membership ── */}
            <div
              className="security-membership"
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "24px",
              }}
            >
              {/* Security Card */}
              <section style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                <h2
                  style={{
                    fontSize: "1.5rem",
                    fontWeight: 900,
                    textTransform: "uppercase",
                    letterSpacing: "-0.025em",
                    fontFamily: "'Syne', sans-serif",
                  }}
                >
                  Security & Privacy
                </h2>

                <div
                  style={{
                    backgroundColor: "#f4f3f3",
                    border: "2px solid #000000",
                    padding: "24px",
                    boxShadow: "4px 4px 0px 0px #000000",
                    display: "flex",
                    flexDirection: "column",
                    gap: "24px",
                  }}
                >
                  {/* Two Factor */}
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <div>
                      <h3
                        style={{
                          fontWeight: 900,
                          textTransform: "uppercase",
                          fontSize: "1rem",
                          fontFamily: "'Syne', sans-serif",
                        }}
                      >
                        Two-Factor Auth
                      </h3>
                      <p style={{ fontSize: "0.875rem", color: "#414844", fontFamily: "'Space Grotesk', sans-serif" }}>Add an extra layer of security</p>
                    </div>

                    <div
                      className={`toggle-track ${twoFactor ? "on" : "off"}`}
                      onClick={() => setTwoFactor(!twoFactor)}
                    >
                      <div className="toggle-thumb" />
                    </div>
                  </div>

                  {/* Change Password */}
                  <div style={{ borderTop: "2px solid #000000", paddingTop: "24px" }}>
                    <button
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        fontWeight: 900,
                        textTransform: "uppercase",
                        fontSize: "0.875rem",
                        background: "none",
                        border: "none",
                        cursor: "pointer",
                        fontFamily: "'Space Grotesk', sans-serif",
                        color: "#000000",
                        transition: "color 0.15s ease",
                      }}
                      onMouseEnter={(e) => (e.currentTarget.style.color = "#1A4D2E")}
                      onMouseLeave={(e) => (e.currentTarget.style.color = "#000000")}
                    >
                      <span className="material-symbols-outlined">key</span>
                      Change Password
                    </button>
                  </div>

                  {/* Active Sessions */}
                  <div style={{ borderTop: "2px solid #000000", paddingTop: "24px" }}>
                    <h4
                      style={{
                        fontWeight: 900,
                        textTransform: "uppercase",
                        fontSize: "0.75rem",
                        marginBottom: "16px",
                        color: "#414844",
                        fontFamily: "'Space Grotesk', sans-serif",
                      }}
                    >
                      Active Sessions
                    </h4>

                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        backgroundColor: "#ffffff",
                        padding: "16px",
                        border: "2px solid #000000",
                      }}
                    >
                      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                        <span className="material-symbols-outlined">desktop_windows</span>
                        <div style={{ fontSize: "0.875rem", fontFamily: "'Space Grotesk', sans-serif" }}>
                          <p style={{ fontWeight: 700 }}>Chrome on MacOS</p>
                          <p style={{ fontSize: "0.75rem", color: "#414844" }}>London, UK • Active Now</p>
                        </div>
                      </div>
                      <button
                        style={{
                          fontSize: "0.75rem",
                          fontWeight: 900,
                          textTransform: "uppercase",
                          color: "#ba1a1a",
                          background: "none",
                          border: "none",
                          cursor: "pointer",
                          fontFamily: "'Syne', sans-serif",
                        }}
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </section>

              {/* Membership Card */}
              <section style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
                <h2
                  style={{
                    fontSize: "1.5rem",
                    fontWeight: 900,
                    textTransform: "uppercase",
                    letterSpacing: "-0.025em",
                    fontFamily: "'Syne', sans-serif",
                  }}
                >
                  Membership
                </h2>

                <div
                  style={{
                    backgroundColor: "#1A4D2E",
                    border: "2px solid #000000",
                    padding: "24px",
                    position: "relative",
                    overflow: "hidden",
                    boxShadow: "4px 4px 0px 0px #000000",
                  }}
                >
                  {/* Pro badge */}
                  <div
                    style={{
                      position: "absolute",
                      right: "-16px",
                      top: "-16px",
                      width: "100px",
                      height: "100px",
                      backgroundColor: "#D8B4FE",
                      border: "2px solid #000000",
                      transform: "rotate(12deg)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <span
                      style={{
                        fontWeight: 900,
                        color: "#000000",
                        transform: "rotate(-12deg)",
                        fontFamily: "'Syne', sans-serif",
                        textTransform: "uppercase",
                      }}
                    >
                      PRO
                    </span>
                  </div>

                  <h3
                    style={{
                      color: "#ffffff",
                      fontWeight: 900,
                      fontSize: "1.25rem",
                      textTransform: "uppercase",
                      marginBottom: "8px",
                      fontFamily: "'Syne', sans-serif",
                    }}
                  >
                    Architect Plan
                  </h3>
                  <p style={{ color: "#e5e7eb", fontSize: "0.875rem", marginBottom: "32px", fontFamily: "'Space Grotesk', sans-serif" }}>
                    Next billing cycle: Oct 24, 2026
                  </p>

                  <div style={{ display: "flex", flexDirection: "column", gap: "16px", fontFamily: "'Space Grotesk', sans-serif" }}>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        color: "#ffffff",
                        borderBottom: "2px solid #e5e7eb",
                        paddingBottom: "8px",
                      }}
                    >
                      <span style={{ fontWeight: 500 }}>Monthly Charge</span>
                      <span style={{ fontWeight: 900 }}>₹29.00</span>
                    </div>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        color: "#ffffff",
                        borderBottom: "2px solid #e5e7eb",
                        paddingBottom: "8px",
                      }}
                    >
                      <span style={{ fontWeight: 500 }}>Total Storage</span>
                      <span style={{ fontWeight: 900 }}>50GB</span>
                    </div>
                  </div>

                  <div style={{ marginTop: "48px", display: "flex", gap: "16px" }}>
                    <button
                      onMouseEnter={() => setManageBillingHover(true)}
                      onMouseLeave={() => setManageBillingHover(false)}
                      style={{
                        flex: 1,
                        padding: "10px",
                        backgroundColor: "#ffffff",
                        color: "#000000",
                        fontWeight: 900,
                        border: "2px solid #000000",
                        boxShadow: manageBillingHover ? "none" : "4px 4px 0px 0px #000000",
                        transform: manageBillingHover ? "translate(2px,2px)" : "translate(0,0)",
                        cursor: "pointer",
                        transition: "all 0.15s ease",
                        textTransform: "uppercase",
                        fontFamily: "'Space Grotesk', sans-serif",
                        fontSize: "0.875rem",
                      }}
                    >
                      Manage Billing
                    </button>

                    <button
                      onMouseEnter={() => setCancelHover(true)}
                      onMouseLeave={() => setCancelHover(false)}
                      style={{
                        padding: "10px",
                        backgroundColor: "#ba1a1a",
                        color: "#ffffff",
                        border: "2px solid #000000",
                        boxShadow: cancelHover ? "none" : "4px 4px 0px 0px #000000",
                        transform: cancelHover ? "translate(2px,2px)" : "translate(0,0)",
                        cursor: "pointer",
                        transition: "all 0.15s ease",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <span className="material-symbols-outlined">cancel</span>
                    </button>
                  </div>
                </div>
              </section>
            </div>

            {/* ── Preferences Section ── */}
            <section style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
              <h2
                style={{
                  fontSize: "1.5rem",
                  fontWeight: 900,
                  textTransform: "uppercase",
                  letterSpacing: "-0.025em",
                  fontFamily: "'Syne', sans-serif",
                }}
              >
                Preferences
              </h2>

              <div
                className="preferences-grid"
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(3, 1fr)",
                  gap: "24px",
                }}
              >
                {/* Language */}
                <div
                  style={{
                    backgroundColor: "#eaddff",
                    border: "2px solid #000000",
                    padding: "24px",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    textAlign: "center",
                    boxShadow: "4px 4px 0px 0px #000000"
                  }}
                >
                  <span className="material-symbols-outlined" style={{ fontSize: "2rem", marginBottom: "16px" }}>
                    language
                  </span>
                  <h3 style={{ fontWeight: 900, textTransform: "uppercase", fontFamily: "'Syne', sans-serif", fontSize: "1rem" }}>
                    Language
                  </h3>
                  <p style={{ fontSize: "0.875rem", marginTop: "8px", marginBottom: "24px", fontFamily: "'Space Grotesk', sans-serif" }}>
                    Set your interface language
                  </p>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    style={{
                      width: "100%",
                      backgroundColor: "#ffffff",
                      border: "2px solid #000000",
                      fontWeight: 700,
                      padding: "8px",
                      fontFamily: "'Space Grotesk', sans-serif",
                      fontSize: "0.875rem",
                      cursor: "pointer",
                      outline: "none",
                    }}
                  >
                    {languages.map((lang) => (
                      <option key={lang}>{lang}</option>
                    ))}
                  </select>
                </div>

                {/* Theme */}
                <div
                  style={{
                    backgroundColor: "#ffffff",
                    border: "2px solid #000000",
                    padding: "24px",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    textAlign: "center",
                    boxShadow: "4px 4px 0px 0px #000000"
                  }}
                >
                  <span className="material-symbols-outlined" style={{ fontSize: "2rem", marginBottom: "16px" }}>
                    dark_mode
                  </span>
                  <h3 style={{ fontWeight: 900, textTransform: "uppercase", fontFamily: "'Syne', sans-serif", fontSize: "1rem" }}>
                    Interface Theme
                  </h3>
                  <p style={{ fontSize: "0.875rem", marginTop: "8px", marginBottom: "24px", fontFamily: "'Space Grotesk', sans-serif" }}>
                    Choose how JobFor looks
                  </p>
                  <div style={{ display: "flex", border: "2px solid #000000", width: "100%", overflow: "hidden" }}>
                    <button
                      className={`theme-btn ${theme === "light" ? "active" : ""}`}
                      onClick={() => setTheme("light")}
                      style={{ borderLeft: "none" }}
                    >
                      Light
                    </button>
                    <button
                      className={`theme-btn ${theme === "dark" ? "active" : ""}`}
                      onClick={() => setTheme("dark")}
                    >
                      Dark
                    </button>
                  </div>
                </div>

                {/* Email Digests */}
                <div
                  style={{
                    backgroundColor: "#dde1ff",
                    border: "2px solid #000000",
                    padding: "24px",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    textAlign: "center",
                    boxShadow: "4px 4px 0px 0px #000000"
                  }}
                >
                  <span className="material-symbols-outlined" style={{ fontSize: "2rem", marginBottom: "16px" }}>
                    mail
                  </span>
                  <h3 style={{ fontWeight: 900, textTransform: "uppercase", fontFamily: "'Syne', sans-serif", fontSize: "1rem" }}>
                    Email Digests
                  </h3>
                  <p style={{ fontSize: "0.875rem", marginTop: "8px", marginBottom: "24px", fontFamily: "'Space Grotesk', sans-serif" }}>
                    How often we ping you
                  </p>
                  <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "100%", textAlign: "left" }}>
                    {digestOptions.map((opt) => (
                      <label
                        key={opt.id}
                        style={{ display: "flex", alignItems: "center", gap: "12px", cursor: "pointer", fontFamily: "'Space Grotesk', sans-serif" }}
                      >
                        <input
                          type="radio"
                          name="digest"
                          className="radio-custom"
                          checked={digest === opt.id}
                          onChange={() => setDigest(opt.id)}
                        />
                        <span style={{ fontWeight: 700, fontSize: "0.875rem" }}>{opt.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </section>

            {/* ── Billing History ── */}
            <section style={{ display: "flex", flexDirection: "column", gap: "24px", paddingBottom: "80px" }}>
              <h2
                style={{
                  fontSize: "1.5rem",
                  fontWeight: 900,
                  textTransform: "uppercase",
                  letterSpacing: "-0.025em",
                  fontFamily: "'Syne', sans-serif",
                }}
              >
                Billing History
              </h2>

              <div
                style={{
                  border: "2px solid #000000",
                  overflow: "hidden",
                  boxShadow: "4px 4px 0px 0px #000000"
                }}
              >
                <table style={{ width: "100%", textAlign: "left", borderCollapse: "collapse" }}>
                  <thead>
                    <tr
                      style={{
                        backgroundColor: "#000000",
                        color: "#ffffff",
                        fontFamily: "'Space Grotesk', sans-serif",
                        textTransform: "uppercase",
                        fontSize: "0.75rem",
                        letterSpacing: "0.1em",
                      }}
                    >
                      <th style={{ padding: "16px", borderRight: "1px solid rgba(255,255,255,0.2)" }}>Date</th>
                      <th style={{ padding: "16px", borderRight: "1px solid rgba(255,255,255,0.2)" }}>Invoice ID</th>
                      <th style={{ padding: "16px", borderRight: "1px solid rgba(255,255,255,0.2)" }}>Amount</th>
                      <th style={{ padding: "16px" }}>Status</th>
                    </tr>
                  </thead>
                  <tbody style={{ backgroundColor: "#ffffff", fontFamily: "'Space Grotesk', sans-serif" }}>
                    {billingHistory.map((row, i) => (
                      <tr
                        key={i}
                        style={{
                          borderBottom: i < billingHistory.length - 1 ? "2px solid #000000" : "none",
                          transition: "background-color 0.15s ease",
                        }}
                        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#f4f3f3")}
                        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#ffffff")}
                      >
                        <td style={{ padding: "16px", fontWeight: 700, borderRight: "2px solid #000000" }}>
                          {row.date}
                        </td>
                        <td
                          style={{
                            padding: "16px",
                            color: "#414844",
                            fontFamily: "monospace",
                            borderRight: "2px solid #000000",
                          }}
                        >
                          {row.invoiceId}
                        </td>
                        <td style={{ padding: "16px", fontWeight: 900, borderRight: "2px solid #000000" }}>
                          {row.amount}
                        </td>
                        <td style={{ padding: "16px" }}>
                          <span
                            style={{
                              backgroundColor: "#D8B4FE",
                              color: "#000000",
                              fontSize: "0.625rem",
                              fontWeight: 900,
                              padding: "4px 8px",
                              textTransform: "uppercase",
                              border: "1px solid #000000",
                            }}
                          >
                            {row.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </div>
        </main>
    </>
  );
}
