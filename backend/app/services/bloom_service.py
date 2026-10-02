"""
Bloom Filter service adapter.

Wraps the existing Phase 9 BloomFilter implementation and exposes
statistics by running it against the local CSV dataset.

This is a stateless adapter — each call re-processes the dataset.
It does NOT integrate with Kafka or any streaming pipeline (Phase 11 scope).
"""
import logging
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger("smart-city-backend")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))


def get_bloom_filter_statistics() -> Optional[dict]:
    """
    Run the Bloom Filter duplicate detector against all event_ids
    in the local CSV dataset and return usage statistics.

    Returns None if either the dataset or the Bloom Filter module is unavailable.
    """
    # 1. Import bloom filter module
    try:
        from bloom_filter.implementation.duplicate_detector import DuplicateDetector
    except ImportError as exc:
        logger.error(f"Cannot import DuplicateDetector: {exc}")
        return None

    # 2. Load dataset
    from app.services.traffic_service import _load_df, _get_csv_path
    df = _load_df()
    if df is None:
        logger.warning("Dataset unavailable; cannot compute Bloom Filter statistics.")
        return None

    # 3. Process event IDs through the filter
    try:
        detector = DuplicateDetector()

        # Process all event_ids
        for event_id in df["event_id"]:
            detector.process(str(event_id))

        stats = detector.statistics()
        stats["dataset_size"] = int(len(df))
        stats["description"] = (
            "Statistics computed by running all dataset event_ids "
            "through the Bloom Filter duplicate detector (no Kafka integration)."
        )
        return stats

    except Exception as exc:
        logger.error(f"Error running Bloom Filter against dataset: {exc}")
        return None
