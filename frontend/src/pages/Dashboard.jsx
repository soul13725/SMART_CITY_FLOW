import React from 'react';

const Dashboard = () => {
  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Smart City Traffic Overview (Awaiting Phase 2 Data Pipeline)</p>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-card-header">
            <span>Traffic Status</span>
          </div>
          <div className="metric-card-value">N/A</div>
          <div className="metric-card-footer">Not Connected</div>
        </div>
        <div className="metric-card">
          <div className="metric-card-header">
            <span>Active Sensors</span>
          </div>
          <div className="metric-card-value">N/A</div>
          <div className="metric-card-footer">Waiting for Data</div>
        </div>
        <div className="metric-card">
          <div className="metric-card-header">
            <span>Monitored Junctions</span>
          </div>
          <div className="metric-card-value">N/A</div>
          <div className="metric-card-footer">Not Connected</div>
        </div>
        <div className="metric-card">
          <div className="metric-card-header">
            <span>Events Processed</span>
          </div>
          <div className="metric-card-value">N/A</div>
          <div className="metric-card-footer">Waiting for Data</div>
        </div>
      </div>

      <div className="content-grid">
        <div className="content-card">
          <h3>Traffic Overview</h3>
          <p style={{ color: 'var(--text-muted)' }}>Demo / Not Connected - Awaiting future data pipeline to render traffic charts.</p>
        </div>
        <div className="content-card">
          <h3>Traffic Density</h3>
          <p style={{ color: 'var(--text-muted)' }}>Demo / Not Connected - Awaiting future data pipeline.</p>
        </div>
        <div className="content-card">
          <h3>Vehicle Distribution</h3>
          <p style={{ color: 'var(--text-muted)' }}>Demo / Not Connected - Awaiting future data pipeline.</p>
        </div>
        <div className="content-card">
          <h3>Recent Events</h3>
          <p style={{ color: 'var(--text-muted)' }}>Demo / Not Connected - Awaiting future data pipeline.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
