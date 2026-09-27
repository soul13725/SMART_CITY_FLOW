# Phase 7: Apache Hive Analytics

## Overview
Apache Hive acts as the project's SQL-based batch analytics layer. While MongoDB (Phase 6) operates as a NoSQL document store with aggregation pipelines, Hive operates directly on massive distributed datasets stored in HDFS (Phase 5). Hive uses HiveQL (HQL) which is compiled into MapReduce or Tez jobs to analyze historical data at scale.

## Architecture
- **Kafka** = real-time event transport
- **Spark Structured Streaming** = real-time stream processing
- **HDFS** = distributed historical storage
- **MapReduce** = batch processing
- **MongoDB** = NoSQL document database + aggregation
- **Hive** = SQL-based batch analytics over large datasets

## Implementation Details
Hive operates on the `traffic_events_raw` external table mapped directly to the HDFS directory `/smartcity/traffic/raw`. 
Data is then populated into a managed ORC table `traffic_events` for optimized query execution.

Analytics covered:
- Vehicle Analytics
- Junction Analytics
- Sensor Analytics
- Density Analytics
- Weather Analytics
- Incident Analytics
- Time-Based Analytics
- Summary Metrics

## Runtime Limitations
Currently, **HIVE RUNTIME IS BLOCKED** due to missing Hive and Hadoop installations on the host environment. The queries and scripts are fully implemented, and static structure tests pass, but live execution cannot occur without an active HDFS and Hive Server.
