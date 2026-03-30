import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Search, 
  LineChart, 
  Target, 
  Bot, 
  User,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import styles from './Sidebar.module.css';

const NavigationLinks = [
  { path: "/dashboard", name: "Dashboard", icon: <LayoutDashboard size={20} /> },
  { path: "/jobs", name: "Job Search", icon: <Search size={20} /> },
  { path: "/insights", name: "Market Insights", icon: <LineChart size={20} /> },
  { path: "/big-opps", name: "Big Opps", icon: <Target size={20} /> },
  { path: "/ai-coach", name: "AI Coach", icon: <Bot size={20} /> },
  { path: "/profile", name: "Profile", icon: <User size={20} /> }
];

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''}`}>
      <div className={styles.header}>
        {!collapsed && <h2 className={styles.logo}>JOBFOR</h2>}
        <button 
          onClick={() => setCollapsed(!collapsed)} 
          className={styles.toggleBtn}
          aria-label="Toggle Sidebar"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>
      
      <nav className={styles.navContainer}>
        {NavigationLinks.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) => 
              `${styles.navItem} ${isActive ? styles.active : ''}`
            }
          >
            <span className={styles.icon}>{link.icon}</span>
            {!collapsed && <span className={styles.label}>{link.name}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
