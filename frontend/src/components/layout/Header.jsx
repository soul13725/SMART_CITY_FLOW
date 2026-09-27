import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { User, Bell } from 'lucide-react';
import { getHealth } from '../../services/api';

const Header = () => {
  const location = useLocation();
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    const checkBackend = async () => {
      const { data } = await getHealth();
      if (data && data.status === 'ok') {
        setStatus('online');
      } else {
        setStatus('offline');
      }
    };
    checkBackend();
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []);

  const getPageTitle = (pathname) => {
    const path = pathname.substring(1);
    if (!path) return 'Dashboard';
    return path.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <header className="top-header">
      <div className="header-title">
        {getPageTitle(location.pathname)}
      </div>
      <div className="header-actions">
        <div className="status-badge" title={`Backend is ${status}`}>
          <div className={`status-dot ${status}`}></div>
          <span style={{ textTransform: 'capitalize' }}>API: {status}</span>
        </div>
        <Bell size={20} style={{ cursor: 'pointer', color: 'var(--text-muted)' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
          <User size={20} />
          <span style={{ fontSize: '0.875rem' }}>Admin</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
