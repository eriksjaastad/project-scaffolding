import re
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

def safe_slug(text: str, base_path: Optional[Path] = None) -> str:
    """Sanitizes string for use in filenames and prevents path traversal.

    If base_path is provided, the resolved target path must stay within that base.
    """
    # Lowercase and replace non-alphanumeric with underscores
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    
    # Industrial Hardening: Prevent directory traversal attempts
    if ".." in slug or slug.startswith("/") or slug.startswith("~"):
        logger.warning(f"Potential path traversal attempt in slug: {text}")
        slug = slug.replace("..", "").replace("/", "").replace("~", "")

    if base_path:
        base_path = base_path.resolve()
        target_path = (base_path / slug).resolve()
        if not target_path.is_relative_to(base_path):
            raise ValueError("Security Alert: Path Traversal detected.")

    return slug[:255]


def grepai_search(query: str, project: str | None = None, limit: int = 10) -> list[dict]:
    """Wrapper around grepai search that logs every query to grepai-logs/.

    Use this instead of calling grepai directly from Python scripts.
    Never raises — logging failures are silently swallowed.
    """
    import json
    import os
    import subprocess
    from datetime import datetime, timezone

    if project is None:
        project = Path.cwd().name

    result = subprocess.run(
        ["grepai", "search", query, "--json", "--limit", str(limit)],
        capture_output=True,
        text=True,
        timeout=30,
    )

    results = []
    try:
        results = json.loads(result.stdout).get("results", [])
    except (json.JSONDecodeError, AttributeError):
        pass

    try:
        log_dir = (
            Path(os.environ.get("PROJECTS_ROOT", Path.home() / "projects"))
            / "_tools"
            / "grepai-logs"
        )
        log_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "project": project,
            "query": query,
            "results": [r["file"] for r in results],
        }
        with open(log_dir / "ai_search_log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Never let logging break the actual search

    return results
