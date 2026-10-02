"""
pytest configuration for the backend test suite.

Ensures the backend directory is on sys.path so that `from app.xxx import yyy`
works regardless of which directory pytest is invoked from.
"""
import sys
import os

# Add the backend directory to the path so 'app' package is importable
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Also add the project root so that 'bloom_filter', 'data_generator', etc. are importable
_project_root = os.path.abspath(os.path.join(_backend_dir, ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
