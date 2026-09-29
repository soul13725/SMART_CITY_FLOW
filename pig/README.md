# Phase 8 — Apache Pig Data-Flow Analytics

This directory contains the Apache Pig implementation for data-flow scripting, ETL, and batch transformation of smart city traffic data.

## Role of Pig in this Project

The Smart City Big Data platform implements multiple distinct analytical layers to demonstrate different Big Data paradigms:

- **MapReduce**: Low-level distributed batch processing (Mapper → Shuffle/Sort → Reducer).
- **Hive**: SQL-based analytical processing, where queries are translated into execution engine plans.
- **Pig**: Data-flow and ETL scripting language (Pig Latin). It focuses on step-by-step transformations:
  `LOAD → FILTER → FOREACH → GROUP → FOREACH aggregation → ORDER → STORE`.

Pig is used here to perform robust ETL operations directly on the canonical dataset without requiring rigid schemas or SQL translation, highlighting its flexibility in data pipelines.

## Project Structure

- `config/`: Settings and configurations.
- `scripts/`: Pig Latin scripts for loading, filtering, grouping, aggregation, and sorting.
- `tests/`: Static tests verifying script integrity and requirements.
- `run_pig.ps1`: Execution script.

## Runtime

Pig execution relies on the local Hadoop/HDFS environment. If Pig or Hadoop is unavailable on the local machine, the implementation acts as blocked (`IMPLEMENTED — PIG RUNTIME BLOCKED`) but all logic and scripts are provided as specified.
