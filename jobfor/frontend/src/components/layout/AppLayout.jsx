import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import styles from './AppLayout.module.css';

const AppLayout = () => {
  const { user, initializing } = useAuth();

  // Suspend hydration mappings resolving dynamically
  if (initializing) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.spinner}></div>
        <p>Verifying secure session tokens...</p>
      </div>
    );
  }

  // Deflect unauthenticated instances securely
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Construct Protected Grid Pipeline Structurally
  return (
    <div className={styles.layoutWrapper}>
      <Sidebar />
      <div className={styles.mainContent}>
        <Navbar />
        <main className={styles.outletContainer}>
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
