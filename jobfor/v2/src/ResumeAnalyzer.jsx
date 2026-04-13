import React, { useState } from "react";

// ─── Data ────────────────────────────────────────────────────────────────────

const strongKeywords = [
  "Strategic Architecture",
  "Scalability",
  "Technical Lead",
  "Cloud Native",
];

const missingKeywords = ["Neo-brutalism", "SASS", "System Design"];

const enhancements = [
  {
    id: 1,
    iconBg: "#2d5bff",
    icon: "bolt",
    title: "Impact Verbs",
    subtitle: "Upgrade passive voice to power actions",
    priority: "High",
    priorityBg: "#eaddff",
    before:
      '"Responsible for managing a team of developers and overseeing the deployment process."',
    after:
      '"Architected and engineered large-scale deployments while mentoring a high-performance team of 12."',
  },
  {
    id: 2,
    iconBg: "#03271a",
    icon: "bar_chart",
    title: "Quantify Results",
    subtitle: "Adding data increases interview rate by 40%",
    priority: "Medium",
    priorityBg: "#e2e2e2",
    before:
      '"Improved the application load speed for better user experience."',
    after:
      '"Reduced frontend latency by 65% across core modules, resulting in a 22% uplift in user retention."',
  },
];

// ─── Radial Progress ──────────────────────────────────────────────────────────

function RadialProgress({ percent = 75 }) {
  const r = 80;
  const circ = 2 * Math.PI * r;
  const offset = circ - (circ * percent) / 100;

  return (
    <div style={{ position: "relative", width: "192px", height: "192px" }}>
      <svg
        width="192"
        height="192"
        viewBox="0 0 192 192"
        style={{ transform: "rotate(-90deg)" }}
      >
        <circle cx="96" cy="96" r={r} fill="transparent" stroke="#e2e2e2" strokeWidth="20" />
        <circle
          cx="96"
          cy="96"
          r={r}
          fill="transparent"
          stroke="#03271a"
          strokeWidth="20"
          strokeDasharray={circ}
          strokeDashoffset={offset}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <span
          style={{
            fontSize: "3rem",
            fontWeight: 900,
            fontFamily: "'Syne', sans-serif",
            lineHeight: 1,
          }}
        >
          {percent}%
        </span>
        <span
          style={{
            fontSize: "0.625rem",
            fontWeight: 900,
            textTransform: "uppercase",
            color: "#6b7280",
          }}
        >
          Optimized
        </span>
      </div>
    </div>
  );
}

// ─── Enhancement Card ─────────────────────────────────────────────────────────

function EnhancementCard({ item }) {
  const [hovered, setHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        backgroundColor: "#ffffff",
        border: "2px solid #000000",
        padding: "32px",
        boxShadow: hovered ? "4px 4px 0px 0px rgba(0,0,0,1)" : "8px 8px 0px 0px rgba(0,0,0,1)",
        transform: hovered ? "translateY(2px)" : "translateY(0)",
        transition: "all 0.15s ease",
      }}
    >
      {/* Card Header */}
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          marginBottom: "24px",
          flexWrap: "wrap",
          gap: "12px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div
            style={{
              backgroundColor: item.iconBg,
              padding: "12px",
              color: "#ffffff",
              border: "2px solid #000000",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <span className="material-symbols-outlined">{item.icon}</span>
          </div>
          <div>
            <h4
              style={{
                fontSize: "1.125rem",
                fontWeight: 900,
                lineHeight: 1.2,
                fontFamily: "'Syne', sans-serif",
                textTransform: "uppercase",
              }}
            >
              {item.title}
            </h4>
            <p
              style={{
                fontSize: "0.75rem",
                fontWeight: 700,
                color: "#6b7280",
                textTransform: "uppercase",
              }}
            >
              {item.subtitle}
            </p>
          </div>
        </div>

        <span
          style={{
            fontSize: "0.625rem",
            fontWeight: 900,
            textTransform: "uppercase",
            padding: "4px 8px",
            backgroundColor: item.priorityBg,
            border: "2px solid #000000",
            fontFamily: "'Space Grotesk', sans-serif",
            whiteSpace: "nowrap",
          }}
        >
          Priority: {item.priority}
        </span>
      </div>

      {/* Before / After */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "24px",
        }}
        className="before-after-grid"
      >
        <div
          style={{
            padding: "24px",
            backgroundColor: "#f4f3f3",
            border: "2px solid #000000",
          }}
        >
          <p
            style={{
              fontSize: "0.625rem",
              fontWeight: 900,
              textTransform: "uppercase",
              color: "#6b7280",
              marginBottom: "8px",
            }}
          >
            Before
          </p>
          <p
            style={{
              fontStyle: "italic",
              color: "#414844",
              fontWeight: 500,
              lineHeight: 1.6,
            }}
          >
            {item.before}
          </p>
        </div>

        <div
          style={{
            padding: "24px",
            backgroundColor: "#c5ebd7",
            border: "2px solid #000000",
          }}
        >
          <p
            style={{
              fontSize: "0.625rem",
              fontWeight: 900,
              textTransform: "uppercase",
              color: "#2c4d3f",
              marginBottom: "8px",
            }}
          >
            After
          </p>
          <p
            style={{
              fontWeight: 700,
              color: "#03271a",
              lineHeight: 1.6,
            }}
          >
            {item.after}
          </p>
        </div>
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function ResumeAnalyzer() {
  const [browseHover, setBrowseHover] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [fabHover, setFabHover] = useState(false);

  return (
    <>
      <style>{`
        .keyword-tag-strong {
          background-color: #c5ebd7;
          color: #002115;
          border: 2px solid #000000;
          padding: 4px 12px;
          font-weight: 700;
          font-size: 0.75rem;
          text-transform: uppercase;
          font-family: 'Space Grotesk', sans-serif;
        }

        .keyword-tag-missing {
          background-color: #eaddff;
          color: #221045;
          border: 2px solid #000000;
          padding: 4px 12px;
          font-weight: 700;
          font-size: 0.75rem;
          text-transform: uppercase;
          font-family: 'Space Grotesk', sans-serif;
        }

        @media (max-width: 1024px) {
          .bento-grid { grid-template-columns: 1fr !important; }
          .hero-grid { grid-template-columns: 1fr !important; }
        }

        @media (max-width: 768px) {
          .keyword-grid { grid-template-columns: 1fr !important; }
          .before-after-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>


      {/* ── Main Content ── */}
      <main
        className="main-canvas"
        style={{
          flex: 1,
          padding: "32px",
        }}
      >
        <div style={{ maxWidth: "1200px", margin: "0 auto" }}>

          {/* ── Hero Section ── */}
          <section
            className="hero-grid"
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "40px",
              alignItems: "center",
              marginBottom: "48px",
            }}
          >
            <div>
              <h1
                style={{
                  fontSize: "3.5rem",
                  fontWeight: 900,
                  marginBottom: "24px",
                  lineHeight: 0.9,
                  letterSpacing: "-0.05em",
                  fontFamily: "'Syne', sans-serif",
                  textTransform: "uppercase"
                }}
              >
                Resume
                <br />
                <span style={{ color: "#0040df" }}>Intelligence</span>
              </h1>
              <p
                style={{
                  fontSize: "1.125rem",
                  fontWeight: 500,
                  color: "#414844",
                  maxWidth: "512px",
                  lineHeight: 1.6,
                  fontFamily: "'Space Grotesk', sans-serif",
                }}
              >
                Deconstruct your career architecture. Our ATS-optimized neural
                engine analyzes your blueprint for high-impact market fit.
              </p>
            </div>

            {/* Upload Zone */}
            <div style={{ position: "relative" }}>
              <div
                style={{
                  position: "absolute",
                  inset: "-8px",
                  backgroundColor: "#eaddff",
                  border: "2px solid #000000",
                  zIndex: 0,
                  transition: "transform 0.15s ease",
                  transform: dragOver ? "translate(8px,8px)" : "translate(0,0)",
                }}
              />
              <div
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => { e.preventDefault(); setDragOver(false); }}
                style={{
                  position: "relative",
                  zIndex: 1,
                  backgroundColor: "#ffffff",
                  border: "2px dashed #000000",
                  padding: "48px",
                  textAlign: "center",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  minHeight: "300px",
                }}
              >
                <span
                  className="material-symbols-outlined"
                  style={{ fontSize: "4rem", marginBottom: "16px", color: "#000000" }}
                >
                  upload_file
                </span>
                <h2
                  style={{
                    fontSize: "1.5rem",
                    fontWeight: 900,
                    marginBottom: "8px",
                    fontFamily: "'Syne', sans-serif",
                    textTransform: "uppercase"
                  }}
                >
                  Drop Your Blueprint
                </h2>
                <p
                  style={{
                    fontSize: "0.875rem",
                    fontWeight: 700,
                    textTransform: "uppercase",
                    letterSpacing: "0.1em",
                    color: "#9ca3af",
                  }}
                >
                  PDF, DOCX (Max 10MB)
                </p>
                <button
                  onMouseEnter={() => setBrowseHover(true)}
                  onMouseLeave={() => setBrowseHover(false)}
                  style={{
                    marginTop: "24px",
                    backgroundColor: "#0040df",
                    color: "#ffffff",
                    border: "2px solid #000000",
                    padding: "12px 32px",
                    fontWeight: 900,
                    boxShadow: browseHover ? "none" : "4px 4px 0px 0px rgba(0,0,0,1)",
                    transform: browseHover ? "translateY(2px)" : "translateY(0)",
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                    fontFamily: "'Syne', sans-serif",
                    fontSize: "0.875rem",
                    letterSpacing: "0.05em",
                    textTransform: "uppercase"
                  }}
                >
                  BROWSE FILES
                </button>
              </div>
            </div>
          </section>

          {/* ── Bento Grid Stats ── */}
          <div
            className="bento-grid"
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "32px",
              marginBottom: "48px",
            }}
          >
            {/* ATS Compatibility */}
            <div
              style={{
                backgroundColor: "#ffffff",
                border: "2px solid #000000",
                padding: "32px",
                boxShadow: "4px 4px 0px 0px #000000",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <h3
                style={{
                  fontSize: "1.25rem",
                  marginBottom: "32px",
                  alignSelf: "flex-start",
                  fontFamily: "'Syne', sans-serif",
                  textTransform: "uppercase",
                  fontWeight: 900,
                }}
              >
                ATS Compatibility
              </h3>

              <RadialProgress percent={75} />

              <p
                style={{
                  marginTop: "32px",
                  textAlign: "center",
                  fontWeight: 700,
                  fontSize: "0.875rem",
                  color: "#414844",
                  lineHeight: 1.6,
                  fontFamily: "'Space Grotesk', sans-serif",
                }}
              >
                Your resume is highly readable but lacks 3 core architectural
                keywords found in the job description.
              </p>
            </div>

            {/* Keyword Deep Dive */}
            <div
              style={{
                backgroundColor: "#ffffff",
                border: "2px solid #000000",
                padding: "32px",
                boxShadow: "4px 4px 0px 0px #000000",
              }}
            >
              <h3
                style={{
                  fontSize: "1.25rem",
                  marginBottom: "32px",
                  fontFamily: "'Syne', sans-serif",
                  textTransform: "uppercase",
                  fontWeight: 900,
                }}
              >
                Keyword Deep Dive
              </h3>

              <div
                className="keyword-grid"
                style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px" }}
              >
                <div>
                  <p
                    style={{
                      fontSize: "0.75rem",
                      fontWeight: 900,
                      textTransform: "uppercase",
                      color: "#9ca3af",
                      marginBottom: "16px",
                      letterSpacing: "0.1em",
                    }}
                  >
                    Strong Keywords
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
                    {strongKeywords.map((kw) => (
                      <span key={kw} className="keyword-tag-strong">{kw}</span>
                    ))}
                  </div>
                </div>

                <div>
                  <p
                    style={{
                      fontSize: "0.75rem",
                      fontWeight: 900,
                      textTransform: "uppercase",
                      color: "#9ca3af",
                      marginBottom: "16px",
                      letterSpacing: "0.1em",
                    }}
                  >
                    Missing Keywords
                  </p>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
                    {missingKeywords.map((kw) => (
                      <span key={kw} className="keyword-tag-missing">{kw}</span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Pro Tip */}
              <div
                style={{
                  marginTop: "40px",
                  padding: "24px",
                  backgroundColor: "#f4f3f3",
                  border: "2px dashed #000000",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                  <span className="material-symbols-outlined" style={{ color: "#0040df", flexShrink: 0 }}>
                    info
                  </span>
                  <p style={{ fontSize: "0.875rem", fontWeight: 700, lineHeight: 1.6, fontFamily: "'Space Grotesk', sans-serif" }}>
                    Pro Tip: Integrate "System Design" into your Experience section to
                    boost ranking by 12%.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* ── Actionable Intelligence ── */}
          <section>
            <div
              style={{
                display: "flex",
                alignItems: "flex-end",
                justifyContent: "space-between",
                marginBottom: "32px",
                borderBottom: "2px solid #000000",
                paddingBottom: "16px",
              }}
            >
              <h2
                style={{
                  fontSize: "2rem",
                  fontWeight: 900,
                  fontFamily: "'Syne', sans-serif",
                  textTransform: "uppercase",
                }}
              >
                Actionable Intelligence
              </h2>
              <span
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 900,
                  textTransform: "uppercase",
                  backgroundColor: "#000000",
                  color: "#ffffff",
                  padding: "4px 12px",
                  fontFamily: "'Space Grotesk', sans-serif",
                }}
              >
                3 Enhancements Found
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "32px" }}>
              {enhancements.map((item) => (
                <EnhancementCard key={item.id} item={item} />
              ))}
            </div>
          </section>
        </div>
      </main>

      {/* ── Floating Action Button ── */}
      <div style={{ position: "fixed", bottom: "40px", right: "40px", zIndex: 50 }}>
        <button
          onMouseEnter={() => setFabHover(true)}
          onMouseLeave={() => setFabHover(false)}
          style={{
            backgroundColor: "#0040df",
            color: "#ffffff",
            width: "64px",
            height: "64px",
            border: "2px solid #000000",
            boxShadow: fabHover ? "none" : "4px 4px 0px 0px rgba(0,0,0,1)",
            transform: fabHover ? "translateY(2px)" : "translateY(0)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            transition: "all 0.15s ease",
          }}
        >
          <span
            className="material-symbols-outlined"
            style={{ fontSize: "2rem", fontVariationSettings: "'FILL' 1" }}
          >
            description
          </span>
        </button>
      </div>
    </>
  );
}
