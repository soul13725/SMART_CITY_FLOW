import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Dashboard from './pages/Dashboard';
import SystemStatus from './pages/SystemStatus';
import PlaceholderPage from './pages/PlaceholderPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="live-traffic" element={<PlaceholderPage title="Live Traffic" />} />
          <Route path="historical-analytics" element={<PlaceholderPage title="Historical Analytics" />} />
          <Route path="junction-analytics" element={<PlaceholderPage title="Junction Analytics" />} />
          <Route path="sensor-analytics" element={<PlaceholderPage title="Sensor Analytics" />} />
          <Route path="big-data-analytics" element={<PlaceholderPage title="Big Data Analytics" />} />
          <Route path="reports" element={<PlaceholderPage title="Reports" />} />
          <Route path="system-status" element={<SystemStatus />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
