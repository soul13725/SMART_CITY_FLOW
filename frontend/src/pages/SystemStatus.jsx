import React, { useEffect, useState } from 'react';
import { getSystemInfo, getHealth } from '../services/api';

const SystemStatus = () => {
  const [loading, setLoading] = useState(true);
  const [systemInfo, setSystemInfo] = useState(null);
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const [healthRes, sysRes] = await Promise.all([
        getHealth(),
        getSystemInfo()
      ]);

      if (healthRes.error || sysRes.error) {
        setError(healthRes.error || sysRes.error);
        setHealth(null);
        setSystemInfo(null);
      } else {
        setHealth(healthRes.data);
        setSystemInfo(sysRes.data);
        setError(null);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div>
      <div className="page-header">
        <h1>System Status</h1>
        <p>Infrastructure and API connection details</p>
      </div>

      <div className="content-grid">
        <div className="content-card">
          <h3>Connection Overview</h3>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">Frontend</span>
              <span className="status-value online">Online</span>
            </div>
            <div className="status-item">
              <span className="status-label">Backend</span>
              {loading ? (
                <span className="status-value" style={{ color: 'var(--warning)' }}>Checking backend...</span>
              ) : error || !health ? (
                <span className="status-value offline">Offline</span>
              ) : (
                <span className="status-value online">Online</span>
              )}
            </div>
            <div className="status-item">
              <span className="status-label">API</span>
              {loading ? (
                <span className="status-value" style={{ color: 'var(--warning)' }}>Connecting...</span>
              ) : error || !health ? (
                <span className="status-value offline">Disconnected</span>
              ) : (
                <span className="status-value online">Connected</span>
              )}
            </div>
          </div>
          
          {error && (
            <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', borderRadius: '0.5rem', border: '1px solid var(--danger)' }}>
              <strong>Unable to connect to backend:</strong> {error}
            </div>
          )}
        </div>

        <div className="content-card">
          <h3>Backend Information</h3>
          {loading ? (
            <p style={{ color: 'var(--text-muted)' }}>Loading system info...</p>
          ) : systemInfo ? (
            <div className="status-grid">
              <div className="status-item">
                <span className="status-label">Service Name</span>
                <span className="status-value">{systemInfo.service}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Version</span>
                <span className="status-value">{systemInfo.version}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Environment</span>
                <span className="status-value" style={{ textTransform: 'capitalize' }}>{systemInfo.environment}</span>
              </div>
            </div>
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>Backend information unavailable.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;
