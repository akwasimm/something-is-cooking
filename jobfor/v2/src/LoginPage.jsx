import React, { useState } from "react";

const footerLinks = ["Privacy Policy", "Terms of Service", "Accessibility"];

function NeoButton({ children, type = "button", onClick, bg, color = "#ffffff", fullWidth = false, large = false, shadowSize = "sm", style = {} }) {
  const [hovered, setHovered] = useState(false);
  const [active, setActive] = useState(false);

  const shadows = {
    sm: "4px 4px 0px 0px #1A1C1C",
    md: "8px 8px 0px 0px #1A1C1C",
    lg: "10px 10px 0px 0px #1A1C1C",
  };

  const getTransform = () => {
    if (active) return "translate(0,0)";
    if (hovered) return "translate(-2px,-2px)";
    return "translate(0,0)";
  };

  const getBoxShadow = () => {
    if (active) return "none";
    if (hovered) return shadowSize === "sm" ? "6px 6px 0px 0px #1A1C1C" : "10px 10px 0px 0px #1A1C1C";
    return shadows[shadowSize];
  };

  return (
    <button
      type={type}
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => { setHovered(false); setActive(false); }}
      onMouseDown={() => setActive(true)}
      onMouseUp={() => setActive(false)}
      style={{
        width: fullWidth ? "100%" : "auto",
        backgroundColor: bg,
        color,
        fontFamily: "'Lexend', sans-serif",
        fontWeight: 900,
        fontSize: large ? "1.25rem" : "0.875rem",
        textTransform: "uppercase",
        letterSpacing: large ? "0.1em" : "-0.025em",
        padding: large ? "20px 24px" : "16px 24px",
        border: "4px solid #1a1c1c",
        boxShadow: getBoxShadow(),
        transform: getTransform(),
        transition: "all 0.15s ease",
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: "12px",
        ...style,
      }}
    >
      {children}
    </button>
  );
}

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login:", { email, password });
  };

  const inputStyle = (focused) => ({
    width: "100%",
    backgroundColor: focused ? "#e8e8e8" : "#ffffff",
    border: "4px solid #1a1c1c",
    padding: "16px",
    fontWeight: 700,
    outline: "none",
    color: "#1a1c1c",
    fontFamily: "'Inter', sans-serif",
    fontSize: "1rem",
    transition: "background-color 0.15s ease",
    borderRadius: 0,
  });

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Inter:wght@100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: 'Inter', sans-serif;
          background-color: #f9f9f9;
          color: #1a1c1c;
          overflow: hidden;
        }

        ::selection { background-color: #2d5bff; color: #ffffff; }

        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-size: 24px;
          line-height: 1;
          display: inline-block;
          direction: ltr;
        }

        .input-field::placeholder { color: #c1c8c2; font-weight: 700; }

        .forgot-link {
          color: #0040df;
          font-family: 'Lexend', sans-serif;
          font-weight: 800;
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: -0.025em;
          text-decoration: none;
        }
        .forgot-link:hover { text-decoration: underline; text-underline-offset: 4px; }

        .signup-link {
          font-family: 'Lexend', sans-serif;
          font-weight: 900;
          color: #1a1c1c;
          text-decoration: underline;
          text-decoration-thickness: 4px;
          text-decoration-color: #d1bcfc;
          text-underline-offset: 4px;
          padding: 0 4px;
          transition: background-color 0.15s ease;
        }
        .signup-link:hover { background-color: #d1bcfc; }

        .footer-link {
          color: rgba(255,255,255,0.8);
          font-family: 'Lexend', sans-serif;
          text-transform: uppercase;
          font-size: 0.75rem;
          font-weight: 700;
          letter-spacing: 0.1em;
          text-decoration: none;
          transition: color 0.15s ease;
        }
        .footer-link:hover { color: #dde1ff; }

        .dot-pattern {
          background-image: radial-gradient(#1a1c1c 2px, transparent 2px);
          background-size: 24px 24px;
        }

        @media (max-width: 768px) {
          .left-panel { display: none !important; }
          .right-panel { width: 100% !important; padding: 24px !important; }
          .mobile-brand { display: block !important; }
          .footer-bar { flex-direction: column !important; text-align: center; }
        }
      `}</style>

      <div style={{ display: "flex", flexDirection: "column", minHeight: "100vh", overflow: "hidden" }}>
        <main style={{ display: "flex", flex: 1 }}>

          {/* ── Left Panel ── */}
          <section
            className="left-panel"
            style={{ width: "50%", backgroundColor: "#eaddff", borderRight: "4px solid #1a1c1c", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "48px", position: "relative", overflow: "hidden" }}
          >
            <div className="dot-pattern" style={{ position: "absolute", inset: 0, opacity: 0.1, pointerEvents: "none" }} />

            <div style={{ position: "absolute", top: 40, left: 40, width: 128, height: 128, border: "4px solid #1a1c1c", backgroundColor: "#2d5bff", boxShadow: "8px 8px 0px 0px #1A1C1C", transform: "rotate(-6deg)" }} />
            <div style={{ position: "absolute", bottom: 40, right: 40, width: 192, height: 192, border: "4px solid #1a1c1c", backgroundColor: "#1b3d2f", boxShadow: "8px 8px 0px 0px #1A1C1C", transform: "rotate(12deg)" }} />

            <div style={{ position: "relative", zIndex: 10, textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: 32 }}>
              <h1 style={{ fontFamily: "'Lexend', sans-serif", fontSize: "6rem", fontWeight: 900, color: "#1a1c1c", lineHeight: 1, letterSpacing: "-0.05em", textTransform: "uppercase", fontStyle: "italic" }}>
                Welcome<br />back!
              </h1>

              <div style={{ backgroundColor: "#fff", border: "4px solid #1a1c1c", padding: 24, boxShadow: "8px 8px 0px 0px #1A1C1C", transform: "rotate(2deg)", maxWidth: 384 }}>
                <p style={{ fontFamily: "'Lexend', sans-serif", fontSize: "1.25rem", fontWeight: 700, color: "#1a1c1c", textTransform: "uppercase", letterSpacing: "-0.025em" }}>
                  Your next architectural career move starts here.
                </p>
              </div>

              <div style={{ display: "flex", gap: 16, justifyContent: "center" }}>
                {[
                  { bg: "#1a1c1c", border: false, color: "#fff", icon: "work", fill: true },
                  { bg: "#2d5bff", border: true, color: "#fff", icon: "architecture", fill: false },
                  { bg: "#fff", border: true, color: "#1a1c1c", icon: "rocket_launch", fill: false },
                ].map((item, i) => (
                  <div key={i} style={{ width: 48, height: 48, backgroundColor: item.bg, border: item.border ? "4px solid #1a1c1c" : "none", display: "flex", alignItems: "center", justifyContent: "center", color: item.color }}>
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: item.fill ? "'FILL' 1" : "'FILL' 0" }}>{item.icon}</span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* ── Right Panel ── */}
          <section
            className="right-panel"
            style={{ width: "50%", backgroundColor: "#ffffff", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "32px 96px", position: "relative" }}
          >
            <div className="mobile-brand" style={{ position: "absolute", top: 32, left: 32, display: "none" }}>
              <span style={{ fontFamily: "'Lexend', sans-serif", fontSize: "1.5rem", fontWeight: 900, color: "#1b3d2f", textTransform: "uppercase", letterSpacing: "-0.05em" }}>JobFor</span>
            </div>

            <div style={{ width: "100%", maxWidth: 448 }}>
              <header style={{ marginBottom: 48 }}>
                <h2 style={{ fontFamily: "'Lexend', sans-serif", fontSize: "3rem", fontWeight: 900, color: "#1a1c1c", textTransform: "uppercase", lineHeight: 1.1, marginBottom: 8 }}>Login</h2>
                <p style={{ color: "#414844", fontWeight: 500, fontFamily: "'Inter', sans-serif" }}>Access your professional structure.</p>
              </header>

              <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 24 }}>
                {/* Email */}
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <label htmlFor="login-email" style={{ fontFamily: "'Lexend', sans-serif", fontWeight: 700, fontSize: "0.875rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "#1a1c1c" }}>
                    Email Address
                  </label>
                  <input
                    id="login-email" type="email" required placeholder="name@company.com"
                    className="input-field" value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    onFocus={() => setEmailFocused(true)} onBlur={() => setEmailFocused(false)}
                    style={inputStyle(emailFocused)}
                  />
                </div>

                {/* Password */}
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
                    <label htmlFor="login-password" style={{ fontFamily: "'Lexend', sans-serif", fontWeight: 700, fontSize: "0.875rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "#1a1c1c" }}>
                      Password
                    </label>
                    <a href="#" className="forgot-link">Forgot Password?</a>
                  </div>
                  <div style={{ position: "relative" }}>
                    <input
                      id="login-password" type={showPassword ? "text" : "password"} required placeholder="••••••••"
                      className="input-field" value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      onFocus={() => setPasswordFocused(true)} onBlur={() => setPasswordFocused(false)}
                      style={{ ...inputStyle(passwordFocused), paddingRight: 52 }}
                    />
                    <button
                      type="button" onClick={() => setShowPassword(!showPassword)}
                      style={{ position: "absolute", right: 16, top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", color: "#414844", display: "flex", alignItems: "center", padding: 0 }}
                    >
                      <span className="material-symbols-outlined">{showPassword ? "visibility_off" : "visibility"}</span>
                    </button>
                  </div>
                </div>

                <NeoButton type="submit" bg="#1b3d2f" color="#ffffff" fullWidth large shadowSize="md" style={{ letterSpacing: "0.15em" }}>
                  LOGIN
                </NeoButton>
              </form>

              {/* Divider */}
              <div style={{ display: "flex", alignItems: "center", margin: "40px 0" }}>
                <div style={{ flexGrow: 1, height: 4, backgroundColor: "#1a1c1c" }} />
                <span style={{ padding: "0 16px", fontFamily: "'Lexend', sans-serif", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.1em", color: "#1a1c1c", whiteSpace: "nowrap" }}>
                  OR CONTINUE WITH
                </span>
                <div style={{ flexGrow: 1, height: 4, backgroundColor: "#1a1c1c" }} />
              </div>

              {/* Social */}
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                <NeoButton bg="#ffffff" color="#1a1c1c" fullWidth shadowSize="sm">
                  <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuD4huHyuKusmR7fnSWTTANvnQWbz_bDRCnHzSuU72Tmoi04KjqC68SQGizCKpsIqeL0A198Zsf78HllDA939Is4PGc6K3bopoTPusJIXivHzqVBRZIcsxSKszv23FPchia0PSUrQpC0axbl6CnK9ZEjik1jY2zoGTrWoHVIrQ8JJjPbWgaDYTOSLJcHg2hw_DfuAC9t657cy6QYjnxroVOsgj7S-LFWuwzAgmjT10jJtaKtkQDo6rvbXTNVVSOTyaE1_cJP80AZRUU" alt="Google" style={{ width: 20, height: 20 }} />
                  Google
                </NeoButton>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                  <NeoButton bg="#2d5bff" color="#ffffff" shadowSize="sm" style={{ width: "100%" }}>
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>groups</span>
                    LinkedIn
                  </NeoButton>
                  <NeoButton bg="#1a1c1c" color="#ffffff" shadowSize="sm" style={{ width: "100%" }}>
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>code</span>
                    GitHub
                  </NeoButton>
                </div>
              </div>

              <footer style={{ marginTop: 48, textAlign: "center" }}>
                <p style={{ fontWeight: 500, color: "#414844", fontFamily: "'Inter', sans-serif" }}>
                  Don't have an account?{" "}
                  <a href="#" className="signup-link">Sign Up</a>
                </p>
              </footer>
            </div>
          </section>
        </main>

        {/* ── Footer ── */}
        <footer
          className="footer-bar"
          style={{ width: "100%", padding: "24px 32px", backgroundColor: "#1b3d2f", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 24, borderTop: "4px solid #1a1c1c", flexWrap: "wrap" }}
        >
          <div style={{ color: "#fff", fontFamily: "'Lexend', sans-serif", fontSize: "1.125rem", fontWeight: 900, textTransform: "uppercase", letterSpacing: "-0.025em" }}>JobFor</div>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 24 }}>
            {footerLinks.map((link) => <a key={link} href="#" className="footer-link">{link}</a>)}
          </div>
          <div style={{ color: "rgba(255,255,255,0.6)", fontFamily: "'Lexend', sans-serif", textTransform: "uppercase", fontSize: "0.625rem", fontWeight: 700, letterSpacing: "0.1em" }}>
            © 2026 Jobfor. All rights reserved. Made in India with ❤️
          </div>
        </footer>
      </div>
    </>
  );
}
