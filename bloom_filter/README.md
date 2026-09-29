# Phase 9 — Bloom Filter Duplicate Event Detection

This directory contains a custom Bloom Filter implementation and a Duplicate Detector to identify redundant traffic events.

## What is a Bloom Filter?

A Bloom Filter is a space-efficient probabilistic data structure that is used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not. This makes it highly suitable for big data streams where exact membership checking would require too much memory.

## Why is it useful for Traffic Analytics?

In a high-throughput smart city traffic stream, duplicate events might be ingested due to sensor retries or network anomalies. 
Checking duplicates against a traditional database (like MongoDB or Postgres) is extremely slow and resource-intensive. A Bloom Filter allows the pipeline to drop duplicates in memory at ultra-high speed before they even reach downstream processors, preserving exact counts for analytics.

## Implementation Details

- **Bit Array**: Memory is allocated continuously using Python's `bytearray`.
- **Hash Functions**: We use deterministic double hashing combining MD5 and SHA-256 for uniform distribution.
- **No False Negatives**: Guaranteed by the bitwise operations (if bits are 0, it definitively wasn't added).
- **False Positives**: Probabilistic. Configurable via `BLOOM_FALSE_POSITIVE_RATE`.
- **Parameter Calculation**: Automatically calculates optimal bit array size ($m$) and hash function count ($k$) based on expected items and target false-positive rate.
- **Duplicate Detection**: The `DuplicateDetector` class tracks incoming events and yields analytical metrics on repetition rates.

## Future Integration Point

While implemented as a standalone package in this phase, it is designed to eventually integrate into the Kafka consumer or Spark Structured Streaming pipeline:

```
Kafka Consumer -> Bloom Filter (Check) -> [Drop if Duplicate] -> [Process if New] -> Downstream Storage (MongoDB/HDFS)
```

## Memory Efficiency

A Bloom Filter tracking 1,000,000 items with a 1% false positive rate requires less than 1.2 MB of memory, compared to hundreds of megabytes for a traditional hash set of UUID strings.
