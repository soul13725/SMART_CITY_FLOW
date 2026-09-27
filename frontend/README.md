# Smart City Big Data Traffic Analytics Platform - Frontend

## Overview
This is the React frontend for the Smart City platform, built with Vite. Currently in Phase 1, it provides the application shell, routing, a professional sidebar and header, and placeholder pages for all future big data analytics modules. It gracefully handles API connectivity state.

## Quick Start
```bash
npm install
npm run dev
```
The application will be accessible at `http://localhost:5173`.

## Architecture
- `src/components/layout/` - Core layout components (Sidebar, Header, MainLayout)
- `src/pages/` - Application routes (Dashboard, SystemStatus, etc.)
- `src/services/` - Centralized API communication (Axios)

## Environment Variables
- `VITE_API_BASE_URL` - Base URL for the backend API (Defaults to `http://localhost:8000/api`)

## Current Limitations
- Traffic data is not real. It is stubbed with "N/A" or "Not Connected" until Phase 2 provides the data pipeline.
- Authentication is not implemented.

## Future Phases
The placeholders in `Live Traffic`, `Historical Analytics`, `Junction Analytics`, etc., will be connected to live WebSocket/REST data feeds from the FastAPI backend as the Kafka/Spark/Hadoop architecture is built.
