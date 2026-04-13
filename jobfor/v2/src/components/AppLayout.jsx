import React from "react";
import AppHeader from "./AppHeader";
import AppSidebar from "./AppSidebar";

export default function AppLayout({ children }) {
  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f9f9f9" }}>
      <AppHeader />
      <AppSidebar />
      <div style={{
        paddingTop: 80,
        marginLeft: 288,
        minHeight: "100vh",
      }}>
        {children}
      </div>
    </div>
  );
}
