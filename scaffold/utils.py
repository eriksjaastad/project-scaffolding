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

    return slug
