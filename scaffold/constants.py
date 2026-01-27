"""
Centralized constants for the project scaffolding system.

Reads from scan_config.yaml as the single source of truth.
"""
import os
from pathlib import Path

import yaml

# Load config from shared YAML file
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", Path.home() / "projects"))
CONFIG_PATH = PROJECTS_ROOT / "project-scaffolding" / "config" / "scan_config.yaml"


def _load_config() -> dict:
    """Load scan configuration from YAML file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    return {}


_config = _load_config()

# Projects that should NEVER be modified by scaffolding or automated cleanup
# Combines ignore_projects (don't scan at all) and protected_projects (read-only)
PROTECTED_PROJECTS = set(_config.get("ignore_projects", [])) | set(
    _config.get("protected_projects", [])
)
