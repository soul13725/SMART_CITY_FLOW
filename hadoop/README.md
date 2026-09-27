# Smart City Hadoop Big Data Analytics

## Overview
This module introduces historical and batch Big Data analytics for the Smart City platform using Apache Hadoop HDFS and MapReduce. While Spark and Kafka handle real-time streaming, Hadoop stores the canonical historical datasets (CSV/JSONL) durably and computes heavy batch analytics over large time horizons.

## Architecture Pipeline
`Phase 2 Traffic Data (CSV)` -> `HDFS (/smartcity/traffic/raw/)` -> `MapReduce (Python Streaming)` -> `Historical Analytics`

### Storage Concepts
- **HDFS (Hadoop Distributed File System)**: Used to store historical traffic events. HDFS relies on a **NameNode** (which manages filesystem metadata) and **DataNodes** (which store the actual data blocks).
- **Blocks & Replication**: HDFS splits files into large blocks (e.g., 128MB) and replicates them (default 3x) across DataNodes for distributed parallel processing and fault tolerance.
- **Why HDFS?**: The Smart City traffic dataset grows endlessly. HDFS scales horizontally to support massive historical analytics beyond the capabilities of local storage.

*(Note: Local single-node deployments are for development/demo purposes and do not provide real fault tolerance).*

### Processing Concepts
- **MapReduce**: We use Hadoop Streaming with Python scripts.
  - **Mapper**: Reads raw CSV lines, extracts required fields, and emits key/value pairs (e.g., `JunctionID \t VehicleCount`).
  - **Shuffle/Sort**: Hadoop automatically groups all identical keys together behind the scenes.
  - **Reducer**: Receives grouped keys and values, aggregates them, and outputs final analytics (e.g., `Total vehicles per Junction`).

## MapReduce Jobs Implemented
1. **Vehicle Count**: Total vehicles aggregated per junction.
2. **Junction Traffic**: Average speed, average occupancy, total vehicles, and event counts per junction.
3. **Vehicle Type**: Breakdowns by vehicle category.
4. **Density Analysis**: Traffic characteristics grouped by density state (LOW, MEDIUM, HIGH, SEVERE).

## Scripts
PowerShell scripts are available in the `scripts/` directory for lifecycle management:
- `setup_hdfs.ps1`: Initializes the `/smartcity/traffic` hierarchy.
- `upload_data.ps1`: Uploads Phase 2 historical CSV data into HDFS.
- `run_mapreduce.ps1`: Executes Hadoop Streaming jobs.
