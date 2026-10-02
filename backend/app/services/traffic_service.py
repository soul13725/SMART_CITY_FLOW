"""
Traffic analytics service.

Reads the Phase 2 CSV dataset and computes aggregated analytics on demand.
External Big Data services (Kafka, Spark, MongoDB, etc.) are checked separately
via bigdata_service. This service works purely from the local CSV file and
therefore runs without any external infrastructure.
"""
import os
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("smart-city-backend")

# ─────────────────────────────────────────────────────────────────────────────
# Dataset location
# ─────────────────────────────────────────────────────────────────────────────

# Resolve path relative to this file's location so that the service works
# regardless of the current working directory.
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
_PROJECT_ROOT = _BACKEND_DIR.parent                            # project root
_CSV_PATH = _PROJECT_ROOT / "data" / "generated" / "traffic_events.csv"

# Alternative: large dataset (if it exists and is preferred)
_CSV_PATH_LARGE = _PROJECT_ROOT / "data" / "generated" / "traffic_events_large.csv"


def _get_csv_path() -> Optional[Path]:
    """Return the first available dataset path, or None if neither exists."""
    if _CSV_PATH.exists():
        return _CSV_PATH
    if _CSV_PATH_LARGE.exists():
        return _CSV_PATH_LARGE
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Lazy-loaded DataFrame (simple in-process cache)
# ─────────────────────────────────────────────────────────────────────────────

_df_cache = None


def _load_df():
    """Load and cache the traffic dataset. Returns None if unavailable."""
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    csv_path = _get_csv_path()
    if csv_path is None:
        logger.warning("Traffic dataset CSV not found. Analytics will be unavailable.")
        return None

    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        # Ensure timestamp is parsed
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        _df_cache = df
        logger.info(f"Loaded traffic dataset: {len(df)} rows from {csv_path}")
        return _df_cache
    except Exception as exc:
        logger.error(f"Failed to load traffic dataset: {exc}")
        return None


def reload_df():
    """Force reload of the cached DataFrame (useful for testing)."""
    global _df_cache
    _df_cache = None
    return _load_df()


# ─────────────────────────────────────────────────────────────────────────────
# Public analytics functions
# ─────────────────────────────────────────────────────────────────────────────

def get_traffic_summary() -> Optional[dict]:
    """
    Return a high-level summary of all traffic events.
    Returns None if the dataset is unavailable.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        return {
            "total_events": int(len(df)),
            "total_vehicle_count": int(df["vehicle_count"].sum()),
            "average_speed": round(float(df["average_speed"].mean()), 2),
            "average_occupancy": round(float(df["occupancy_rate"].mean()), 4),
            "junction_count": int(df["junction_id"].nunique()),
            "sensor_count": int(df["sensor_id"].nunique()),
        }
    except Exception as exc:
        logger.error(f"Error computing traffic summary: {exc}")
        return None


def get_vehicle_analytics(vehicle_type: Optional[str] = None) -> Optional[list[dict]]:
    """
    Return analytics grouped by vehicle type.
    Optionally filter to a single vehicle_type.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        if vehicle_type:
            df = df[df["vehicle_type"] == vehicle_type]

        grouped = (
            df.groupby("vehicle_type", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                total_vehicle_count=("vehicle_count", "sum"),
                average_speed=("average_speed", "mean"),
            )
            .sort_values("event_count", ascending=False)
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "vehicle_type": str(row["vehicle_type"]),
                "event_count": int(row["event_count"]),
                "total_vehicle_count": int(row["total_vehicle_count"]),
                "average_speed": round(float(row["average_speed"]), 2),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing vehicle analytics: {exc}")
        return None


def get_junction_analytics(junction_id: Optional[str] = None) -> Optional[list[dict]]:
    """
    Return analytics grouped by junction.
    Optionally filter to a single junction_id.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        if junction_id:
            df = df[df["junction_id"] == junction_id]

        grouped = (
            df.groupby("junction_id", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                total_vehicle_count=("vehicle_count", "sum"),
                average_speed=("average_speed", "mean"),
                average_occupancy=("occupancy_rate", "mean"),
            )
            .sort_values("junction_id")
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "junction_id": str(row["junction_id"]),
                "event_count": int(row["event_count"]),
                "total_vehicle_count": int(row["total_vehicle_count"]),
                "average_speed": round(float(row["average_speed"]), 2),
                "average_occupancy": round(float(row["average_occupancy"]), 4),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing junction analytics: {exc}")
        return None


def get_sensor_analytics(sensor_id: Optional[str] = None) -> Optional[list[dict]]:
    """
    Return analytics grouped by sensor.
    Optionally filter to a single sensor_id.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        if sensor_id:
            df = df[df["sensor_id"] == sensor_id]

        grouped = (
            df.groupby("sensor_id", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                total_vehicle_count=("vehicle_count", "sum"),
                average_speed=("average_speed", "mean"),
                average_occupancy=("occupancy_rate", "mean"),
            )
            .sort_values("sensor_id")
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "sensor_id": str(row["sensor_id"]),
                "event_count": int(row["event_count"]),
                "total_vehicle_count": int(row["total_vehicle_count"]),
                "average_speed": round(float(row["average_speed"]), 2),
                "average_occupancy": round(float(row["average_occupancy"]), 4),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing sensor analytics: {exc}")
        return None


def get_density_analytics(traffic_density: Optional[str] = None) -> Optional[list[dict]]:
    """
    Return analytics grouped by traffic density level.
    Density values are detected from actual dataset (not assumed).
    """
    df = _load_df()
    if df is None:
        return None

    try:
        if traffic_density:
            df = df[df["traffic_density"] == traffic_density]

        total = len(df)
        grouped = (
            df.groupby("traffic_density", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                average_vehicle_count=("vehicle_count", "mean"),
                average_speed=("average_speed", "mean"),
            )
            .sort_values("event_count", ascending=False)
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "traffic_density": str(row["traffic_density"]),
                "event_count": int(row["event_count"]),
                "percentage": round(float(row["event_count"]) / total * 100, 2) if total > 0 else 0.0,
                "average_vehicle_count": round(float(row["average_vehicle_count"]), 2),
                "average_speed": round(float(row["average_speed"]), 2),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing density analytics: {exc}")
        return None


def get_weather_analytics(weather_condition: Optional[str] = None) -> Optional[list[dict]]:
    """
    Return analytics grouped by weather condition.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        if weather_condition:
            df = df[df["weather_condition"] == weather_condition]

        total = len(df)
        grouped = (
            df.groupby("weather_condition", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                average_speed=("average_speed", "mean"),
                average_vehicle_count=("vehicle_count", "mean"),
            )
            .sort_values("event_count", ascending=False)
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "weather_condition": str(row["weather_condition"]),
                "event_count": int(row["event_count"]),
                "percentage": round(float(row["event_count"]) / total * 100, 2) if total > 0 else 0.0,
                "average_speed": round(float(row["average_speed"]), 2),
                "average_vehicle_count": round(float(row["average_vehicle_count"]), 2),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing weather analytics: {exc}")
        return None


def get_incident_analytics() -> Optional[list[dict]]:
    """
    Return analytics grouped by incident status.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        total = len(df)
        grouped = (
            df.groupby("incident_status", as_index=False)
            .agg(event_count=("event_id", "count"))
            .sort_values("event_count", ascending=False)
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "incident_status": str(row["incident_status"]),
                "event_count": int(row["event_count"]),
                "percentage": round(float(row["event_count"]) / total * 100, 2) if total > 0 else 0.0,
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing incident analytics: {exc}")
        return None


def get_hourly_analytics() -> Optional[list[dict]]:
    """
    Return analytics aggregated by hour-of-day (0–23).
    """
    df = _load_df()
    if df is None:
        return None

    try:
        df = df.copy()
        df["hour"] = df["timestamp"].dt.hour

        grouped = (
            df.groupby("hour", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                total_vehicle_count=("vehicle_count", "sum"),
                average_speed=("average_speed", "mean"),
            )
            .sort_values("hour")
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "hour": int(row["hour"]),
                "event_count": int(row["event_count"]),
                "total_vehicle_count": int(row["total_vehicle_count"]),
                "average_speed": round(float(row["average_speed"]), 2),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing hourly analytics: {exc}")
        return None


def get_daily_analytics() -> Optional[list[dict]]:
    """
    Return analytics aggregated by calendar date.
    """
    df = _load_df()
    if df is None:
        return None

    try:
        df = df.copy()
        df["date"] = df["timestamp"].dt.date.astype(str)

        grouped = (
            df.groupby("date", as_index=False)
            .agg(
                event_count=("event_id", "count"),
                total_vehicle_count=("vehicle_count", "sum"),
                average_speed=("average_speed", "mean"),
            )
            .sort_values("date")
        )

        result = []
        for _, row in grouped.iterrows():
            result.append({
                "date": str(row["date"]),
                "event_count": int(row["event_count"]),
                "total_vehicle_count": int(row["total_vehicle_count"]),
                "average_speed": round(float(row["average_speed"]), 2),
            })
        return result
    except Exception as exc:
        logger.error(f"Error computing daily analytics: {exc}")
        return None


def dataset_info() -> dict:
    """Return basic info about the dataset availability."""
    csv_path = _get_csv_path()
    if csv_path is None:
        return {"available": False, "path": None, "rows": None}
    df = _load_df()
    return {
        "available": df is not None,
        "path": str(csv_path),
        "rows": len(df) if df is not None else None,
    }
