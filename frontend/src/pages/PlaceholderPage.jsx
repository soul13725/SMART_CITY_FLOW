import React from 'react';

const PlaceholderPage = ({ title }) => {
  return (
    <div>
      <div className="page-header">
        <h1>{title}</h1>
        <p>This module is planned for a future development phase.</p>
      </div>
      <div className="content-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4rem 2rem', textAlign: 'center' }}>
        <h2 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Module Not Implemented</h2>
        <p style={{ color: 'var(--text-muted)', maxWidth: '500px' }}>
          The <strong>{title}</strong> features require the Big Data ingestion and processing pipelines (Kafka, Spark, Hadoop, etc.) which will be introduced in subsequent phases.
        </p>
      </div>
    </div>
  );
};

export default PlaceholderPage;
