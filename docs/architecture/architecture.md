# Architecture Document

## Overview
The Smart City Big Data Traffic Analytics Platform is designed to ingest, process, store, and analyze traffic data in a distributed and scalable manner.

## Planned Data Flow

### Real-Time Ingestion and Analytics
```text
Python Traffic Generator
↓
Apache Kafka
↓
Spark Structured Streaming
↓
Real-Time Analytics
↓
FastAPI
↓
React Dashboard
```

### Historical Big Data Analytics
```text
Traffic Data
↓
Hadoop HDFS
↓
MapReduce
↓
Historical Analytics
```

### SQL-Style Analytics
```text
HDFS / processed data
↓
Hive
↓
Traffic Analytics
```

### Data Filtration / Grouping
```text
Traffic Data
↓
Apache Pig
↓
Filtering / Grouping / Aggregation
```

### NoSQL Event Analytics
```text
Traffic Events
↓
MongoDB
↓
Sensor/Event Analytics
```

### Duplicate/Presence Detection
```text
Traffic Event
↓
Bloom Filter
↓
Possible duplicate/presence check
```

### Statistical Analysis
```text
Historical Traffic Data
↓
R Analytics
↓
Traffic Trend Visualization
```
