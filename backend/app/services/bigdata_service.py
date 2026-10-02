"""
Big Data component runtime-status service.

Each check probes whether the underlying runtime dependency is actually
available in the current environment. Source-code existence is tracked
separately from runtime availability.

Rules:
  - implemented=True  → source files exist in the project
  - runtime_available → the runtime dependency is actually reachable/executable
  - reason            → human-readable explanation for unavailability
"""
import shutil
import subprocess
import sys
import logging
from pathlib import Path

logger = logging.getLogger("smart-city-backend")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


# ─────────────────────────────────────────────────────────────────────────────
# Individual component checks
# ─────────────────────────────────────────────────────────────────────────────

def _check_kafka() -> dict:
    """Check Kafka broker connectivity."""
    # Source check
    implemented = (_PROJECT_ROOT / "kafka").exists()

    # Try to import confluent_kafka without connecting
    try:
        from confluent_kafka.admin import AdminClient  # noqa: F401

        # Try a very short connect attempt to the default broker
        try:
            from kafka.config.settings import settings as kafka_settings  # type: ignore
            bootstrap = kafka_settings.KAFKA_BOOTSTRAP_SERVERS
        except Exception:
            bootstrap = "localhost:9092"

        try:
            admin = AdminClient({"bootstrap.servers": bootstrap, "socket.timeout.ms": 2000})
            meta = admin.list_topics(timeout=2.0)
            return {"implemented": implemented, "runtime_available": True, "reason": None}
        except Exception as exc:
            return {
                "implemented": implemented,
                "runtime_available": False,
                "reason": f"Kafka broker unreachable: {exc}",
            }
    except ImportError:
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": "confluent_kafka Python package not installed in this environment",
        }


def _check_spark() -> dict:
    """Check PySpark availability."""
    implemented = (_PROJECT_ROOT / "spark").exists()
    try:
        import pyspark  # noqa: F401
        # pyspark imports fine but JAVA_HOME may be missing at runtime
        import os
        java_home = os.environ.get("JAVA_HOME") or shutil.which("java")
        if java_home:
            return {"implemented": implemented, "runtime_available": True, "reason": None}
        else:
            return {
                "implemented": implemented,
                "runtime_available": False,
                "reason": "Java runtime not found (JAVA_HOME not set, java not on PATH)",
            }
    except ImportError:
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": "PySpark not installed in this environment",
        }


def _check_hadoop() -> dict:
    """Check Hadoop/HDFS availability."""
    implemented = (_PROJECT_ROOT / "hadoop").exists()
    hadoop_bin = shutil.which("hadoop")
    hdfs_bin = shutil.which("hdfs")
    if hadoop_bin or hdfs_bin:
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    # Also check HADOOP_HOME
    import os
    hadoop_home = os.environ.get("HADOOP_HOME")
    if hadoop_home and Path(hadoop_home).exists():
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    return {
        "implemented": implemented,
        "runtime_available": False,
        "reason": "Hadoop/HDFS binaries not found on PATH and HADOOP_HOME not set",
    }


def _check_mongodb() -> dict:
    """Check MongoDB connectivity."""
    implemented = (_PROJECT_ROOT / "mongodb").exists()
    try:
        import pymongo  # noqa: F401
        try:
            from mongodb.config.settings import settings as mongo_settings  # type: ignore
            uri = mongo_settings.MONGO_URI
        except Exception:
            uri = "mongodb://localhost:27017"

        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        client.close()
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    except ImportError:
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": "pymongo not installed in this environment",
        }
    except Exception as exc:
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": f"MongoDB unreachable: {exc}",
        }


def _check_hive() -> dict:
    """Check Apache Hive/HiveServer2 availability."""
    implemented = (_PROJECT_ROOT / "hive").exists()
    # Hive is typically accessed via JDBC / beeline; check for beeline or hive on PATH
    beeline = shutil.which("beeline")
    hive_bin = shutil.which("hive")
    if beeline or hive_bin:
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    # Also try PyHive import
    try:
        from pyhive import hive  # noqa: F401
        # Even if PyHive is installed, HiveServer2 may not be running
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": "PyHive installed but HiveServer2 runtime not reachable on localhost",
        }
    except ImportError:
        pass
    return {
        "implemented": implemented,
        "runtime_available": False,
        "reason": "Hive binaries not on PATH and PyHive not installed",
    }


def _check_pig() -> dict:
    """Check Apache Pig availability."""
    implemented = (_PROJECT_ROOT / "pig").exists()
    pig_bin = shutil.which("pig")
    if pig_bin:
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    import os
    pig_home = os.environ.get("PIG_HOME")
    if pig_home and (Path(pig_home) / "bin" / "pig").exists():
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    return {
        "implemented": implemented,
        "runtime_available": False,
        "reason": "Pig binary not found on PATH and PIG_HOME not set",
    }


def _check_bloom_filter() -> dict:
    """Check Bloom Filter implementation availability (pure Python, always local)."""
    implemented = (_PROJECT_ROOT / "bloom_filter").exists()
    try:
        # Attempt to import the bloom filter module
        sys.path.insert(0, str(_PROJECT_ROOT))
        from bloom_filter.implementation.bloom_filter import BloomFilter  # noqa: F401
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    except ImportError as exc:
        return {
            "implemented": implemented,
            "runtime_available": False,
            "reason": f"Bloom Filter import failed: {exc}",
        }


def _check_r() -> dict:
    """Check R runtime availability."""
    implemented = (_PROJECT_ROOT / "r_analytics").exists()
    rscript = shutil.which("Rscript")
    r_exe = shutil.which("R")
    if rscript or r_exe:
        return {"implemented": implemented, "runtime_available": True, "reason": None}
    # Windows: try common install paths
    common_r_paths = [
        r"C:\Program Files\R",
        r"C:\Program Files (x86)\R",
    ]
    for base in common_r_paths:
        base_path = Path(base)
        if base_path.exists():
            matches = list(base_path.glob("R-*/bin/Rscript.exe"))
            if matches:
                return {"implemented": implemented, "runtime_available": True, "reason": None}
    return {
        "implemented": implemented,
        "runtime_available": False,
        "reason": "Rscript executable not available on PATH and not found in common install locations",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Public interface
# ─────────────────────────────────────────────────────────────────────────────

def get_component_status() -> dict:
    """
    Return runtime status of all Big Data components.

    Each check is isolated in a try/except so one failing check never
    prevents the others from running.
    """
    checks = {
        "kafka": _check_kafka,
        "spark": _check_spark,
        "hadoop": _check_hadoop,
        "mongodb": _check_mongodb,
        "hive": _check_hive,
        "pig": _check_pig,
        "bloom_filter": _check_bloom_filter,
        "r": _check_r,
    }

    results = {}
    for name, check_fn in checks.items():
        try:
            results[name] = check_fn()
        except Exception as exc:
            logger.error(f"Unexpected error checking {name}: {exc}")
            results[name] = {
                "implemented": True,
                "runtime_available": False,
                "reason": f"Check raised unexpected error: {exc}",
            }

    return results


def get_r_status() -> dict:
    """Return detailed R runtime status."""
    info = _check_r()
    return {
        "implemented": info["implemented"],
        "runtime_available": info["runtime_available"],
        "reason": info.get("reason") or "R runtime is available",
    }
