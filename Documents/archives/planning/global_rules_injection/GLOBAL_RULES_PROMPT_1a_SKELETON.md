# Worker Task 1a: Create Script Skeleton
**Worker Model:** DeepSeek-R1
**Objective:** Create the basic structure of `scripts/update_cursorrules.py` with imports and argparse.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **File Created:** `scripts/update_cursorrules.py` exists
- [ ] **Imports:** Includes argparse, logging, pathlib, sys
- [ ] **Logging:** Configured using `logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')`
- [ ] **Argparse:** Implements `main()` with `--dry-run` (default=True) and `--root` (default=[USER_HOME]/projects) arguments
- [ ] **Entry Point:** Includes `if __name__ == "__main__": main()` block

### CONSTRAINTS (READ FIRST)
- DO NOT implement any scanning or logic yet.
- DO NOT implement execute/update logic.
- FOLLOW the pattern from `scripts/warden_audit.py` exactly.

### Reference Code Snippet
```python
import argparse
import logging
import pathlib
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Push safety rules to all project .cursorrules files")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Show what would change (default)")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path("[USER_HOME]/projects"), help="Projects root")
    args = parser.parse_args()
    
    if not args.root.exists():
        logger.error(f"Projects root not found: {args.root}")
        sys.exit(1)
    
    logger.info(f"Scanning: {args.root} (Dry-run: {args.dry_run})")
    sys.exit(0)

if __name__ == "__main__":
    main()
```


## Related Documentation

- [[LOCAL_MODEL_LEARNINGS]] - local AI

