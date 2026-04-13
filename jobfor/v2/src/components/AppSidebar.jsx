import React from "react";
import { Link, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { icon: "dashboard",      label: "Dashboard",    to: "/user" },
  { icon: "search",         label: "Discover Jobs", to: "/discover" },
  { icon: "analytics",      label: "Insights",     to: "/insights" },
  { icon: "rocket_launch",  label: "Big Opps",     to: "/opportunities" },
  { icon: "bookmark",       label: "Saved Jobs",   to: "/saved" },
  { icon: "psychology",     label: "AI Coach",     to: "/coach" },
  { icon: "analytics",      label: "Resume Analyzer", to: "/analyzer" },
  { icon: "manage_accounts",label: "Profile",      to: "/profile" },
  { icon: "settings",       label: "Settings",     to: "/settings" },
];

const DEFAULT_USER = {
  name: "Alex Chen",
  role: "Senior Architect",
  avatar: "https://lh3.googleusercontent.com/aida-public/AB6AXuALjzLqlPmSkGYDdF1k9NwmrsCAIswWocv3NrpGYGy5rGy9PBBbhxuCyGqge_pxRP7NchIxGcyhf6dwQQC495SeoYy0Gb6HZczRDnsR4jQrt15A8Wn3F5uGiBVbFKEXXMV86b7p1a0SaIT_ahRTFhxJyNIHiVCvFBnbeovDdFbWlX9IA3j5Eht_p6gEHTdJw_bkCZKLiewAoALNLzB7mPtz48X3pljhngpK14yRCKxdFVnc90XaFwoJDVaGfApiub7R9Ug62mXkz60",
};

export default function AppSidebar({ user = DEFAULT_USER }) {
  const { pathname } = useLocation();

  return (
    <>
      <style>{`
        .app-sidebar-link {
          display: flex; align-items: center; gap: 12px;
          padding: 12px 16px;
          font-family: 'Lexend', sans-serif; font-weight: 700; font-size: 0.8rem;
          text-transform: uppercase; letter-spacing: 0.05em;
          color: #1a1c1c; text-decoration: none;
          border: none; background: none; width: 100%; cursor: pointer;
          transition: all 0.12s ease;
          border-left: 4px solid transparent;
        }
        .app-sidebar-link:hover {
          background-color: #ede9fe;
          border-left-color: #D8B4FE;
          transform: translateX(2px);
        }
        .app-sidebar-link.active {
          background-color: #1A4D2E;
          color: #ffffff;
          border-left-color: #1A4D2E;
          box-shadow: inset -4px 0 0 0 #D8B4FE;
        }
        .app-sidebar-link.active:hover {
          background-color: #0f2a1a;
          transform: none;
        }
        .material-symbols-outlined {
          font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
          font-family: 'Material Symbols Outlined';
          font-size: 20px; line-height: 1; display: inline-block; direction: ltr;
          flex-shrink: 0;
        }
        .app-sidebar-link.active .material-symbols-outlined {
          font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
      `}</style>
      <aside style={{
        position: "fixed",
        top: 80, left: 0,
        width: 288,
        height: "calc(100vh - 80px)",
        backgroundColor: "#f9f9f9",
        borderRight: "4px solid #1a1c1c",
        display: "flex",
        flexDirection: "column",
        overflowY: "auto",
        zIndex: 90,
      }}>
        {/* User mini-card */}
        <div style={{
          padding: "24px 16px 16px",
          borderBottom: "2px solid #e5e5e5",
          display: "flex", alignItems: "center", gap: 12,
        }}>
          <img
            src={user.avatar}
            alt={user.name}
            style={{ width: 44, height: 44, objectFit: "cover", border: "2px solid #1a1c1c", flexShrink: 0 }}
          />
          <div style={{ minWidth: 0 }}>
            <p style={{
              fontFamily: "'Lexend', sans-serif", fontWeight: 900, fontSize: "0.8rem",
              color: "#1a1c1c", margin: 0, textTransform: "uppercase", letterSpacing: "0.025em",
              whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
            }}>
              {user.name}
            </p>
            <p style={{ fontFamily: "'Inter', sans-serif", fontSize: "0.7rem", color: "#6b7280", margin: 0 }}>
              {user.role}
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav style={{ padding: "16px 0", flex: 1 }}>
          {NAV_ITEMS.map(({ icon, label, to }) => {
            const active = pathname === to || (to !== "/" && pathname.startsWith(to));
            return (
              <Link
                key={to}
                to={to}
                className={`app-sidebar-link${active ? " active" : ""}`}
              >
                <span className="material-symbols-outlined">{icon}</span>
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Bottom: AI match badge */}
        <div style={{
          margin: 16, padding: 16,
          border: "3px solid #1a1c1c",
          backgroundColor: "#D8B4FE",
          boxShadow: "4px 4px 0 0 #1a1c1c",
        }}>
          <p style={{
            fontFamily: "'Lexend', sans-serif", fontWeight: 900,
            fontSize: "0.75rem", textTransform: "uppercase", color: "#1a1c1c", margin: "0 0 4px",
          }}>
            AI Match Score
          </p>
          <p style={{
            fontFamily: "'Lexend', sans-serif", fontWeight: 900,
            fontSize: "2rem", color: "#1A4D2E", margin: 0, lineHeight: 1,
          }}>
            94%
          </p>
          <p style={{ fontFamily: "'Inter', sans-serif", fontSize: "0.7rem", color: "#1a1c1c", margin: "4px 0 0", opacity: 0.7 }}>
            Profile is 78% complete
          </p>
        </div>
      </aside>
    </>
  );
}
