# Smart City Big Data Traffic Analytics Platform

## Project Description
A comprehensive big data platform designed to process, analyze, and visualize smart city traffic data at scale. The system aims to ingest real-time traffic events and provide actionable insights for city administration.

## Problem Statement
Modern cities generate massive amounts of traffic data through various sensors. Traditional monolithic systems cannot handle the scale, velocity, and variety of this data efficiently, leading to delayed insights and suboptimal traffic management.

## Objectives
- Build a highly scalable big data pipeline.
- Enable real-time traffic monitoring and analytics.
- Provide historical batch analytics for long-term trends.
- Support advanced NoSQL and SQL-based querying on traffic data.
- Offer an intuitive real-time dashboard for city officials.

## Technology Stack
- **Frontend**: React, Vite
- **Backend API**: Python, FastAPI
- **Message Broker**: Apache Kafka
- **Real-Time Processing**: Apache Spark Structured Streaming
- **Batch Storage & Processing**: Hadoop HDFS, MapReduce
- **Data Warehousing**: Apache Hive
- **Data Flow Scripting**: Apache Pig
- **NoSQL Storage**: MongoDB
- **Statistical Analytics**: R
- **Algorithmic Utilities**: Bloom Filter

## Architecture & Planned Data Flow

### Real-Time Flow
Traffic Generator -> Kafka -> Spark Streaming -> Real-Time Analytics -> FastAPI -> React Dashboard

### Batch/Historical Flow
Traffic Data -> Hadoop HDFS -> MapReduce -> Historical Analytics

### Other Flows
- **Hive**: HDFS -> Hive -> SQL Analytics
- **Pig**: Traffic Data -> Apache Pig -> Filtering/Aggregation
- **MongoDB**: Traffic Events -> MongoDB -> Sensor Analytics
- **R**: Historical Data -> R Analytics -> Trend Visualization

## Project Phases
- **PHASE 0**: Project initialization and environment validation (CURRENT)
- **PHASE 1**: Application foundation and core architecture
- **PHASE 2**: Smart-city traffic data generation
- **PHASE 3**: Kafka real-time ingestion
- **PHASE 4**: Spark Structured Streaming
- **PHASE 5**: Hadoop HDFS + MapReduce
- **PHASE 6**: MongoDB analytics
- **PHASE 7**: Hive analytics
- **PHASE 8**: Apache Pig analytics
- **PHASE 9**: Bloom Filter
- **PHASE 10**: R analytics
- **PHASE 11**: FastAPI integration
- **PHASE 12**: React Smart City dashboard
- **PHASE 13**: Full system integration
- **PHASE 14**: Testing, optimization and documentation

*Note: Future advanced modules (E-challan generation, God's Eye, GPS tracking) are planned but not included in these initial phases.*

## Current Phase Status
**PHASE 3: PARTIALLY COMPLETE** - Kafka real-time ingestion architecture implemented (Producer, Consumer, Schema validation). Code logic is fully complete, but runtime validation is blocked pending a local Kafka broker installation.

## Architecture Pipeline
`Traffic Generator` -> `Kafka Producer` -> `Kafka (traffic-events)` -> `Consumer` -> `(Spark Streaming - Planned for Phase 4)`

## Installation Prerequisites
Ensure the following tools are installed:
- Python 3.9+
- Node.js 18+ and npm
- Git
- Java (JDK 8 or 11 required for Hadoop/Spark)
- Apache Hadoop & HDFS
- Apache Kafka
- Apache Spark
- MongoDB
- Apache Hive
- Apache Pig
- R Language

## Development Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
