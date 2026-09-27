# Smart City MongoDB NoSQL Persistence and Analytics

## Overview
This module introduces MongoDB as the NoSQL document persistence and analytical layer for the Smart City platform. 
While HDFS is used for massive offline distributed file storage, MongoDB provides rapid, indexed document querying and advanced aggregation pipelines (e.g. `$group`, `$match`, `$project`) to answer questions about traffic flow, weather impacts, and junction congestion.

## Architecture
- **Database**: `smart_city`
- **Collection**: `traffic_events`
- **Document**: A single traffic event containing canonical Phase 2 fields.
- **Indexes**: Used to rapidly filter events (e.g., by `junction_id`, `timestamp`).
- **Aggregation Pipeline**: MongoDB's native analytical engine which performs multi-stage calculations (grouping, summing, averaging) entirely within the database without needing to transfer all records to Python first.

## Execution
If MongoDB is installed and running locally on `localhost:27017`:

1. **Install dependencies**: `uv pip install -r mongodb/requirements.txt`
2. **Ingest Phase 2 Data**: 
   `python -m mongodb.ingestion.import_traffic --input data/generated/traffic_events.csv`
3. **Run Analytics**:
   `python -m mongodb.scripts.run_analytics`

## Duplicate Handling
The ingestion pipeline enforces a unique index on `event_id`. Duplicate events from multiple imports are gracefully trapped using bulk write error handling, ensuring data integrity without aborting the batch.
