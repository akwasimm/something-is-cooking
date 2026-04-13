import React from "react";
import { Link } from "react-router-dom";

// Default user (replace with real auth context later)
const DEFAULT_USER = {
  name: "Alex Chen",
  role: "Senior Architect",
  avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuBVDul7LZBkrrNeh-RW3pF2jxqrYFulpgFY700jl_r6-zpGSccec5jLkR7kb8AvhksbPpLHAgU2h363mSxfO53pS4E35pON8YQH2B83nUhWx_evJLWN8Mh1R9owp8ODuahL-FIqqngd24rjCj1VobYl0B38PGy36rw_fIWL_v-k6PMJwt-U7FVPD86V8XJ9kurEsNAaSGwCCpIhagKJQ5LUkZZp_5wSePdRPua5n-yUR4VcOi6otqrZ1py70S3G_chcHLXrYLayQiU",
};

export default function AppHeader({ user = DEFAULT_USER }) {
  return (
    <>
      <style>{`
        .app-header-icon {
          width: 40px; height: 40px;
          display: flex; align-items: center; justify-content: center;
          border: none; background: none; cursor: pointer;
          transition: background-color 0.15s ease; border-radius: 0;
          position: relative;
        }
        .app-header-icon:hover { background-color: #f3f4f6; }
        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-size: 24px; line-height: 1; display: inline-block; direction: ltr;
        }
      `}</style>
      <header style={{
        position: "fixed", top: 0, left: 0, right: 0, height: 80, zIndex: 100,
        backgroundColor: "#ffffff",
        borderBottom: "4px solid #1a1c1c",
        boxShadow: "0 4px 0 0 #1a1c1c",
        display: "flex", alignItems: "center",
        padding: "0 32px",
        justifyContent: "space-between",
      }}>
        {/* Brand */}
        <Link to="/" style={{
          fontFamily: "'Lexend', sans-serif", fontWeight: 900, fontSize: "1.5rem",
          color: "#1A4D2E", textDecoration: "none", textTransform: "uppercase",
          letterSpacing: "-0.05em",
        }}>
          JobFor<span style={{ color: "#D8B4FE" }}>.</span>
        </Link>

        {/* Right: icons + avatar */}
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <button className="app-header-icon" title="Search">
            <span className="material-symbols-outlined">search</span>
          </button>
          <button className="app-header-icon" title="Notifications">
            <span className="material-symbols-outlined">notifications</span>
          </button>
          <div style={{
            height: 40, width: 1, backgroundColor: "#e5e5e5", margin: "0 8px",
          }} />
          <Link to="/profile" style={{
            display: "flex", alignItems: "center", gap: 10, textDecoration: "none",
          }}>
            <img
              src={user.avatar}
              alt={user.name}
              style={{
                width: 36, height: 36, objectFit: "cover",
                border: "2px solid #1a1c1c",
              }}
            />
            <div>
              <p style={{
                fontFamily: "'Lexend', sans-serif", fontWeight: 900,
                fontSize: "0.75rem", color: "#1a1c1c", margin: 0,
                textTransform: "uppercase", letterSpacing: "0.025em",
              }}>
                {user.name}
              </p>
              <p style={{ fontFamily: "'Inter', sans-serif", fontSize: "0.625rem", color: "#6b7280", margin: 0 }}>
                {user.role}
              </p>
            </div>
          </Link>
        </div>
      </header>
    </>
  );
}
