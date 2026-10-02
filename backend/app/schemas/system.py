"""
Pydantic response schemas for system and Big Data component status endpoints.
"""
from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    """Basic health check response."""
    status: str
    service: str
    version: str


class ComponentStatus(BaseModel):
    """Runtime status of a single Big Data component."""
    implemented: bool
    runtime_available: bool
    reason: Optional[str] = None


class BigDataStatusResponse(BaseModel):
    """Aggregated status of all Big Data components."""
    components: dict[str, ComponentStatus]


class BloomFilterStatistics(BaseModel):
    """Statistics from the Bloom Filter duplicate detector."""
    total_checked: int
    new_events: int
    duplicates: int
    estimated_duplicate_rate: float
    # Memory / parameter stats
    bit_count: int
    byte_count: int
    hash_count: int
    expected_items: int
    target_false_positive_rate: float
    # Dataset info
    dataset_size: Optional[int] = None
    description: Optional[str] = None


class RStatusResponse(BaseModel):
    """R Analytics runtime status."""
    implemented: bool
    runtime_available: bool
    reason: str


class SystemInfoResponse(BaseModel):
    """System and component availability info."""
    service: str
    version: str
    environment: str
    python_version: str
    backend: str
    components: dict[str, str]
