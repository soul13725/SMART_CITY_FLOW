"""
Phase 11 — FastAPI Integration Tests

Tests cover:
- All new endpoints (traffic, analytics, bigdata)
- HTTP status codes
- Response schema validity
- Graceful handling of (simulated) unavailable services
- Data integrity: summary values cross-checked against raw CSV

Run from the project root:
    .venv/Scripts/python -m pytest backend/tests/ -v
"""
import sys
import os
import time
import csv
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ─────────────────────────────────────────────────────────────────────────────
# Path setup (also handled by conftest.py — kept here for clarity)
# ─────────────────────────────────────────────────────────────────────────────
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_project_root = os.path.abspath(os.path.join(_backend_dir, ".."))
for _p in [_backend_dir, _project_root]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from app.main import app  # noqa: E402

client = TestClient(app)

# ─────────────────────────────────────────────────────────────────────────────
# CSV path helper for cross-checks
# ─────────────────────────────────────────────────────────────────────────────
_CSV = Path(_project_root) / "data" / "generated" / "traffic_events.csv"


def _csv_row_count() -> int:
    """Count data rows (excluding header) in the CSV file."""
    if not _CSV.exists():
        return 0
    with open(_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return max(0, len(rows) - 1)  # subtract header


def _csv_total_vehicles() -> int:
    """Sum vehicle_count column from the CSV file."""
    if not _CSV.exists():
        return 0
    total = 0
    with open(_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                total += int(row["vehicle_count"])
            except (ValueError, KeyError):
                pass
    return total


# ─────────────────────────────────────────────────────────────────────────────
# Phase 1 — Existing endpoints (regression)
# ─────────────────────────────────────────────────────────────────────────────

class TestExistingEndpoints:
    """Phase 1 regression: existing health and system endpoints must still pass."""

    def test_health_check(self):
        """GET /api/health — must return 200 with correct shape."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "smart-city-big-data-backend"
        assert "version" in data

    def test_system_info(self):
        """GET /api/system/info — must return 200 with expected keys."""
        response = client.get("/api/system/info")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "smart-city-big-data-backend"
        assert "version" in data
        assert "environment" in data

    def test_system_info_has_components(self):
        """GET /api/system/info — Phase 11 enhancement: must include components."""
        response = client.get("/api/system/info")
        assert response.status_code == 200
        data = response.json()
        assert "components" in data
        assert "bloom_filter" in data["components"]
        assert "python_version" in data

    def test_system_info_backend_available(self):
        """GET /api/system/info — backend field must be 'available'."""
        response = client.get("/api/system/info")
        assert response.status_code == 200
        assert response.json()["backend"] == "available"


# ─────────────────────────────────────────────────────────────────────────────
# Test 3 — Traffic Summary
# ─────────────────────────────────────────────────────────────────────────────

class TestTrafficSummary:
    def test_traffic_summary_status(self):
        """GET /api/traffic/summary — must return 200 or 503."""
        response = client.get("/api/traffic/summary")
        assert response.status_code in (200, 503)

    def test_traffic_summary_schema_when_available(self):
        """GET /api/traffic/summary — 200 response must have correct schema."""
        response = client.get("/api/traffic/summary")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable in this environment")
        data = response.json()
        assert "total_events" in data
        assert "total_vehicle_count" in data
        assert "average_speed" in data
        assert "average_occupancy" in data
        assert "junction_count" in data
        assert "sensor_count" in data

    def test_traffic_summary_data_integrity(self):
        """total_events must match the actual CSV row count."""
        response = client.get("/api/traffic/summary")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable in this environment")
        data = response.json()
        csv_rows = _csv_row_count()
        assert data["total_events"] == csv_rows, (
            f"API reports {data['total_events']} events but CSV has {csv_rows} rows"
        )

    def test_traffic_summary_vehicle_count_integrity(self):
        """total_vehicle_count must match the sum of vehicle_count in the CSV."""
        response = client.get("/api/traffic/summary")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable in this environment")
        data = response.json()
        csv_total = _csv_total_vehicles()
        assert data["total_vehicle_count"] == csv_total, (
            f"API reports {data['total_vehicle_count']} vehicles but CSV sums to {csv_total}"
        )

    def test_traffic_summary_reasonable_values(self):
        """average_speed must be positive; junction_count and sensor_count must be > 0."""
        response = client.get("/api/traffic/summary")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable in this environment")
        data = response.json()
        assert data["average_speed"] > 0
        assert data["junction_count"] > 0
        assert data["sensor_count"] > 0


# ─────────────────────────────────────────────────────────────────────────────
# Test 4 — Vehicle Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestVehicleAnalytics:
    def test_vehicle_analytics_status(self):
        response = client.get("/api/analytics/vehicles")
        assert response.status_code in (200, 503)

    def test_vehicle_analytics_schema(self):
        response = client.get("/api/analytics/vehicles")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "vehicle_type" in item
        assert "event_count" in item
        assert "total_vehicle_count" in item
        assert "average_speed" in item

    def test_vehicle_analytics_filter(self):
        """Filter by vehicle_type=car must return only car records."""
        response = client.get("/api/analytics/vehicles?vehicle_type=car")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        for item in data["data"]:
            assert item["vehicle_type"] == "car"

    def test_vehicle_analytics_total_consistency(self):
        """Sum of event_count across all vehicle types must equal total CSV rows."""
        response = client.get("/api/analytics/vehicles")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        total = sum(item["event_count"] for item in data["data"])
        csv_rows = _csv_row_count()
        assert total == csv_rows


# ─────────────────────────────────────────────────────────────────────────────
# Test 5 — Junction Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestJunctionAnalytics:
    def test_junction_analytics_status(self):
        response = client.get("/api/analytics/junctions")
        assert response.status_code in (200, 503)

    def test_junction_analytics_schema(self):
        response = client.get("/api/analytics/junctions")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "junction_id" in item
        assert "event_count" in item
        assert "total_vehicle_count" in item
        assert "average_speed" in item
        assert "average_occupancy" in item

    def test_junction_count(self):
        """Number of junctions in analytics must match traffic summary."""
        summary_resp = client.get("/api/traffic/summary")
        junction_resp = client.get("/api/analytics/junctions")
        if summary_resp.status_code == 503 or junction_resp.status_code == 503:
            pytest.skip("Dataset unavailable")
        junction_count = summary_resp.json()["junction_count"]
        assert len(junction_resp.json()["data"]) == junction_count

    def test_junction_filter(self):
        """Filter by junction_id must return at most one record."""
        response = client.get("/api/analytics/junctions")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        junctions = response.json()["data"]
        if not junctions:
            pytest.skip("No junctions in dataset")
        jid = junctions[0]["junction_id"]
        filtered = client.get(f"/api/analytics/junctions?junction_id={jid}")
        assert filtered.status_code == 200
        filtered_data = filtered.json()["data"]
        assert len(filtered_data) == 1
        assert filtered_data[0]["junction_id"] == jid


# ─────────────────────────────────────────────────────────────────────────────
# Test 6 — Sensor Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestSensorAnalytics:
    def test_sensor_analytics_status(self):
        response = client.get("/api/analytics/sensors")
        assert response.status_code in (200, 503)

    def test_sensor_analytics_schema(self):
        response = client.get("/api/analytics/sensors")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "sensor_id" in item
        assert "event_count" in item
        assert "total_vehicle_count" in item
        assert "average_speed" in item
        assert "average_occupancy" in item

    def test_sensor_count(self):
        """Number of sensors in analytics must match traffic summary."""
        summary_resp = client.get("/api/traffic/summary")
        sensor_resp = client.get("/api/analytics/sensors")
        if summary_resp.status_code == 503 or sensor_resp.status_code == 503:
            pytest.skip("Dataset unavailable")
        sensor_count = summary_resp.json()["sensor_count"]
        assert len(sensor_resp.json()["data"]) == sensor_count


# ─────────────────────────────────────────────────────────────────────────────
# Test 7 — Density Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestDensityAnalytics:
    def test_density_analytics_status(self):
        response = client.get("/api/analytics/density")
        assert response.status_code in (200, 503)

    def test_density_analytics_schema(self):
        response = client.get("/api/analytics/density")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "traffic_density" in item
        assert "event_count" in item
        assert "percentage" in item
        assert "average_vehicle_count" in item
        assert "average_speed" in item

    def test_density_percentages_sum_to_100(self):
        """Sum of all percentages must be approximately 100%."""
        response = client.get("/api/analytics/density")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()["data"]
        total_pct = sum(item["percentage"] for item in data)
        assert abs(total_pct - 100.0) < 0.1, f"Percentages sum to {total_pct}, expected ~100"

    def test_density_event_counts_sum(self):
        """Sum of event_counts across density levels must equal CSV row count."""
        response = client.get("/api/analytics/density")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        total = sum(item["event_count"] for item in response.json()["data"])
        assert total == _csv_row_count()


# ─────────────────────────────────────────────────────────────────────────────
# Test 8 — Weather Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestWeatherAnalytics:
    def test_weather_analytics_status(self):
        response = client.get("/api/analytics/weather")
        assert response.status_code in (200, 503)

    def test_weather_analytics_schema(self):
        response = client.get("/api/analytics/weather")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "weather_condition" in item
        assert "event_count" in item
        assert "percentage" in item
        assert "average_speed" in item
        assert "average_vehicle_count" in item

    def test_weather_percentages_sum_to_100(self):
        response = client.get("/api/analytics/weather")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        total_pct = sum(item["percentage"] for item in response.json()["data"])
        assert abs(total_pct - 100.0) < 0.1


# ─────────────────────────────────────────────────────────────────────────────
# Test 9 — Incident Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestIncidentAnalytics:
    def test_incident_analytics_status(self):
        response = client.get("/api/analytics/incidents")
        assert response.status_code in (200, 503)

    def test_incident_analytics_schema(self):
        response = client.get("/api/analytics/incidents")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "incident_status" in item
        assert "event_count" in item
        assert "percentage" in item

    def test_incident_percentages_sum_to_100(self):
        response = client.get("/api/analytics/incidents")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        total_pct = sum(item["percentage"] for item in response.json()["data"])
        assert abs(total_pct - 100.0) < 0.1


# ─────────────────────────────────────────────────────────────────────────────
# Test 10 — Hourly Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestHourlyAnalytics:
    def test_hourly_analytics_status(self):
        response = client.get("/api/analytics/time/hourly")
        assert response.status_code in (200, 503)

    def test_hourly_analytics_schema(self):
        response = client.get("/api/analytics/time/hourly")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "hour" in item
        assert "event_count" in item
        assert "total_vehicle_count" in item
        assert "average_speed" in item

    def test_hourly_hour_range(self):
        """All hour values must be in 0–23."""
        response = client.get("/api/analytics/time/hourly")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        for item in response.json()["data"]:
            assert 0 <= item["hour"] <= 23

    def test_hourly_event_sum(self):
        """Sum of event_count across hours must equal total CSV rows."""
        response = client.get("/api/analytics/time/hourly")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        total = sum(item["event_count"] for item in response.json()["data"])
        assert total == _csv_row_count()


# ─────────────────────────────────────────────────────────────────────────────
# Test 11 — Daily Analytics
# ─────────────────────────────────────────────────────────────────────────────

class TestDailyAnalytics:
    def test_daily_analytics_status(self):
        response = client.get("/api/analytics/time/daily")
        assert response.status_code in (200, 503)

    def test_daily_analytics_schema(self):
        response = client.get("/api/analytics/time/daily")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        item = data["data"][0]
        assert "date" in item
        assert "event_count" in item
        assert "total_vehicle_count" in item
        assert "average_speed" in item

    def test_daily_event_sum(self):
        """Sum of event_count across dates must equal total CSV rows."""
        response = client.get("/api/analytics/time/daily")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        total = sum(item["event_count"] for item in response.json()["data"])
        assert total == _csv_row_count()


# ─────────────────────────────────────────────────────────────────────────────
# Test 12 — Big Data Status
# ─────────────────────────────────────────────────────────────────────────────

class TestBigDataStatus:
    def test_bigdata_status_always_200(self):
        """GET /api/bigdata/status must always return 200."""
        response = client.get("/api/bigdata/status")
        assert response.status_code == 200

    def test_bigdata_status_schema(self):
        response = client.get("/api/bigdata/status")
        data = response.json()
        assert "components" in data
        components = data["components"]
        expected = ["kafka", "spark", "hadoop", "mongodb", "hive", "pig", "bloom_filter", "r"]
        for name in expected:
            assert name in components, f"Missing component: {name}"
            assert "implemented" in components[name]
            assert "runtime_available" in components[name]

    def test_bigdata_status_bloom_filter_implemented(self):
        """Bloom Filter must be reported as implemented (source exists)."""
        response = client.get("/api/bigdata/status")
        data = response.json()
        assert data["components"]["bloom_filter"]["implemented"] is True

    def test_bigdata_status_types(self):
        """implemented and runtime_available must be booleans."""
        response = client.get("/api/bigdata/status")
        data = response.json()
        for name, info in data["components"].items():
            assert isinstance(info["implemented"], bool), f"{name}.implemented not bool"
            assert isinstance(info["runtime_available"], bool), f"{name}.runtime_available not bool"


# ─────────────────────────────────────────────────────────────────────────────
# Test 13 — Bloom Filter
# ─────────────────────────────────────────────────────────────────────────────

class TestBloomFilter:
    def test_bloom_filter_status(self):
        """GET /api/bigdata/bloom-filter — must return 200 or 503."""
        response = client.get("/api/bigdata/bloom-filter")
        assert response.status_code in (200, 503)

    def test_bloom_filter_schema(self):
        response = client.get("/api/bigdata/bloom-filter")
        if response.status_code == 503:
            pytest.skip("Bloom Filter unavailable in this environment")
        data = response.json()
        assert "total_checked" in data
        assert "new_events" in data
        assert "duplicates" in data
        assert "estimated_duplicate_rate" in data
        assert "bit_count" in data
        assert "byte_count" in data
        assert "hash_count" in data
        assert "expected_items" in data
        assert "target_false_positive_rate" in data

    def test_bloom_filter_all_unique(self):
        """
        Since all event_ids in the CSV are UUIDs, duplicates must be 0
        (or very close to 0 allowing for false positives).
        """
        response = client.get("/api/bigdata/bloom-filter")
        if response.status_code == 503:
            pytest.skip("Bloom Filter unavailable")
        data = response.json()
        assert data["total_checked"] == _csv_row_count()
        assert data["duplicates"] == 0, (
            f"Expected 0 duplicates (all event_ids are unique UUIDs) but got {data['duplicates']}"
        )
        assert data["new_events"] == _csv_row_count()

    def test_bloom_filter_dataset_size(self):
        response = client.get("/api/bigdata/bloom-filter")
        if response.status_code == 503:
            pytest.skip("Bloom Filter unavailable")
        data = response.json()
        assert data.get("dataset_size") == _csv_row_count()


# ─────────────────────────────────────────────────────────────────────────────
# Test 14 — R Status
# ─────────────────────────────────────────────────────────────────────────────

class TestRStatus:
    def test_r_status_always_200(self):
        """GET /api/bigdata/r-status must always return 200."""
        response = client.get("/api/bigdata/r-status")
        assert response.status_code == 200

    def test_r_status_schema(self):
        response = client.get("/api/bigdata/r-status")
        data = response.json()
        assert "implemented" in data
        assert "runtime_available" in data
        assert "reason" in data

    def test_r_status_implemented(self):
        """R Analytics source files exist — implemented must be True."""
        response = client.get("/api/bigdata/r-status")
        data = response.json()
        assert data["implemented"] is True

    def test_r_status_reason_non_empty(self):
        """reason field must always be a non-empty string."""
        response = client.get("/api/bigdata/r-status")
        data = response.json()
        assert isinstance(data["reason"], str)
        assert len(data["reason"]) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Performance tests (local dev benchmarks only)
# ─────────────────────────────────────────────────────────────────────────────

class TestPerformance:
    """
    Measure representative API response times.
    These are local development benchmarks only — not production SLAs.
    """

    _ENDPOINTS = [
        "/api/traffic/summary",
        "/api/analytics/vehicles",
        "/api/analytics/junctions",
    ]

    def _time_request(self, url: str) -> tuple:
        start = time.perf_counter()
        response = client.get(url)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return response.status_code, elapsed_ms

    def test_traffic_summary_response_time(self):
        """Traffic summary must respond within 5 seconds (local CSV read)."""
        status, elapsed = self._time_request("/api/traffic/summary")
        print(f"\n  /api/traffic/summary → {status} in {elapsed:.0f}ms")
        assert elapsed < 5000, f"Response too slow: {elapsed:.0f}ms"

    def test_vehicle_analytics_response_time(self):
        """Vehicle analytics must respond within 5 seconds."""
        status, elapsed = self._time_request("/api/analytics/vehicles")
        print(f"\n  /api/analytics/vehicles → {status} in {elapsed:.0f}ms")
        assert elapsed < 5000

    def test_junction_analytics_response_time(self):
        """Junction analytics must respond within 5 seconds."""
        status, elapsed = self._time_request("/api/analytics/junctions")
        print(f"\n  /api/analytics/junctions → {status} in {elapsed:.0f}ms")
        assert elapsed < 5000


# ─────────────────────────────────────────────────────────────────────────────
# Error handling
# ─────────────────────────────────────────────────────────────────────────────

class TestErrorHandling:
    def test_unknown_route_returns_404(self):
        """Unknown routes must return 404 — not crash the app."""
        response = client.get("/api/does_not_exist")
        assert response.status_code == 404

    def test_invalid_vehicle_type_filter_returns_200_empty(self):
        """
        An unknown vehicle_type filter should return 200 with empty data
        (filtered to nothing) rather than an error.
        """
        response = client.get("/api/analytics/vehicles?vehicle_type=__nonexistent__")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        assert response.status_code == 200
        data = response.json()
        assert data["data"] == []

    def test_invalid_junction_filter_returns_200_empty(self):
        response = client.get("/api/analytics/junctions?junction_id=__nonexistent__")
        if response.status_code == 503:
            pytest.skip("Dataset unavailable")
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_503_has_detail_body(self):
        """
        If a 503 is returned, it must carry a JSON detail body with
        status, service, and reason keys.
        """
        # We'll check the bloom filter endpoint since we can verify its 503 structure
        # by mocking — but instead just verify the format if it returns 503.
        response = client.get("/api/bigdata/bloom-filter")
        if response.status_code == 200:
            pytest.skip("Bloom Filter is available — 503 not triggered")
        assert response.status_code == 503
        detail = response.json().get("detail", {})
        assert "status" in detail
        assert "service" in detail
        assert "reason" in detail
