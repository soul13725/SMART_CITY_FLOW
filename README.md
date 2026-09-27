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
**PHASE 4: IMPLEMENTED — KAFKA RUNTIME INTEGRATION BLOCKED** - Apache Spark Structured Streaming pipeline has been implemented to parse, validate, transform, and window-aggregate traffic events in real-time. Code logic and unit tests are complete, but live streaming is blocked pending a local Kafka broker and Spark Hadoop environment on the host machine.

**PHASE 5: IMPLEMENTED — HADOOP RUNTIME BLOCKED** - Apache Hadoop HDFS and MapReduce architecture has been created to handle historical batch analytics. Python Hadoop Streaming scripts (Mappers/Reducers) and HDFS management scripts are complete and unit tested, but actual deployment is blocked since Hadoop/HDFS is not installed on the Windows host.

**PHASE 6: IMPLEMENTED — MONGODB RUNTIME BLOCKED** - MongoDB NoSQL analytical persistence and ingestion architecture is complete. Analytical aggregation pipelines, document schemas, and unique index configurations are implemented and unit tested, but live execution is blocked as MongoDB is not installed locally.

**PHASE 7: IMPLEMENTED — HIVE RUNTIME BLOCKED** - Apache Hive SQL-based batch analytical architecture is complete. HQL scripts for schema generation, external HDFS table mapping, internal ORC tables, and full analytical querying (vehicle, junction, sensor, density, weather, incident, time, summary) are created and validated statically. Execution is blocked as Hive and Hadoop are not installed locally.

## Architecture Pipeline
`Traffic Generator` -> `Kafka / Spark` | `HDFS / MapReduce / Hive` | `MongoDB (NoSQL Analytics)`

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
