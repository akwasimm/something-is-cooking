import React from 'react';

export default function Footer({ 
  description, 
  cols, 
  copyright, 
  maxWidthClass = "max-w-7xl", 
  mtClass = "mt-20" 
}) {
  return (
    <footer style={{ borderTop: "3px solid #000000", backgroundColor: "#ffffff" }}>
      <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "24px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px" }}>
        <a href="/" style={{ fontSize: "1.5rem", fontWeight: 800, fontFamily: "'Syne', sans-serif", letterSpacing: "-0.05em", color: "#1A4D2E", textDecoration: "none" }}>
          JOBFOR<span style={{ color: "#D8B4FE" }}>.</span>
        </a>
        <div style={{ color: "#000000", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.1em", fontFamily: "'Space Grotesk', sans-serif" }}>
          {copyright || "© 2026 Jobfor. All rights reserved. Made in India with ❤️"}
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
  );
}
