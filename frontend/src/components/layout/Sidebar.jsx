import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Activity, Clock, Map, Cpu, Database, FileText, Settings } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/dashboard', name: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { path: '/live-traffic', name: 'Live Traffic', icon: <Activity size={20} /> },
    { path: '/historical-analytics', name: 'Historical Analytics', icon: <Clock size={20} /> },
    { path: '/junction-analytics', name: 'Junction Analytics', icon: <Map size={20} /> },
    { path: '/sensor-analytics', name: 'Sensor Analytics', icon: <Cpu size={20} /> },
    { path: '/big-data-analytics', name: 'Big Data Analytics', icon: <Database size={20} /> },
    { path: '/reports', name: 'Reports', icon: <FileText size={20} /> },
    { path: '/system-status', name: 'System Status', icon: <Settings size={20} /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Smart City</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '0.25rem' }}>Big Data Flow</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
