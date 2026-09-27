# Data Directory

This directory holds datasets for the Smart City Big Data Traffic Analytics Platform.

## Structure
- `raw/` - Raw, unprocessed datasets (currently unused).
- `generated/` - Synthetic data produced by the Python traffic generator. 
- `processed/` - Cleaned/aggregated data processed by Spark or MapReduce (planned).
- `samples/` - Small sample files for testing purposes.

**IMPORTANT NOTE ON GENERATED DATA:**
All traffic events inside the `generated/` directory are synthetic and intended purely for Big Data pipeline experimentation. They are generated using statistical probabilities and do not represent actual real-world sensor deployments.
