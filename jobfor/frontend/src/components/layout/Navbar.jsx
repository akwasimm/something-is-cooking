import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Search, Bell, Menu, UserCircle, LogOut, Settings } from 'lucide-react';
import styles from './Navbar.module.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);

  // Generate page title via regex parsing strictly routing endpoints
  const getPageTitle = () => {
    const path = location.pathname.split('/')[1];
    if (!path) return 'Welcome';
    return path.charAt(0).toUpperCase() + path.slice(1).replace('-', ' ');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className={styles.navbar}>
      <div className={styles.leftSection}>
        <h1 className={styles.pageTitle}>{getPageTitle()}</h1>
      </div>

      <div className={styles.rightSection}>
        <div className={styles.searchContainer}>
          <Search size={18} className={styles.searchIcon} />
          <input 
            type="text" 
            placeholder="Search roles, companies..." 
            className={styles.searchInput}
          />
        </div>
        
        <button className={styles.iconBtn} aria-label="Notifications">
          <Bell size={20} />
          <span className={styles.badge}>3</span>
        </button>

        <div className={styles.userMenu}>
          <button 
            className={styles.avatarBtn} 
            onClick={() => setShowDropdown(!showDropdown)}
          >
            {user?.profile?.avatar_url ? (
               <img src={user.profile.avatar_url} alt="Profile" className={styles.avatar} />
            ) : (
               <UserCircle size={28} className={styles.avatarPlaceholder} />
            )}
            <span className={styles.userName}>{user?.firstName || 'Candidate'}</span>
          </button>

          {showDropdown && (
            <div className={styles.dropdown}>
              <button onClick={() => { setShowDropdown(false); navigate('/profile'); }} className={styles.dropdownItem}>
                <Settings size={16} />
                <span>Settings</span>
              </button>
              <button onClick={handleLogout} className={`${styles.dropdownItem} ${styles.danger}`}>
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
