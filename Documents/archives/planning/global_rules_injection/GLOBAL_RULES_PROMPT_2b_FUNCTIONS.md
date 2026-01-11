# Worker Task 2b: Add Backup & Inject Functions
**Worker Model:** DeepSeek-R1
**Objective:** Add `create_backup` and `inject_safety_rules` to `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `create_backup(cursorrules_path: pathlib.Path, backup_dir: pathlib.Path) -> pathlib.Path`
- [ ] **Logic:** Creates timestamped subdirectory, copies file using `shutil.copy2`.
- [ ] **Function added:** `inject_safety_rules(content: str, has_trash: bool, has_silent: bool) -> str`
- [ ] **Logic:** Appends `SAFETY_RULES_SECTION` to content if rules missing.

### CONSTRAINTS (READ FIRST)
- DO NOT change existing functions.
- USE `shutil` and `datetime` (import them if missing).

### Reference Code Snippet
```python
import shutil
from datetime import datetime

def create_backup(cursorrules_path: pathlib.Path, backup_dir: pathlib.Path) -> pathlib.Path:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_subdir = backup_dir / timestamp / cursorrules_path.parent.name
    backup_subdir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_subdir / ".cursorrules"
    shutil.copy2(cursorrules_path, backup_path)
    logger.info(f"  Backed up to: {backup_path}")
    return backup_path

def inject_safety_rules(content: str, has_trash: bool, has_silent: bool) -> str:
    if has_trash and has_silent: return content
    if not content.endswith('\n'): content += '\n'
    content += SAFETY_RULES_SECTION
    return content
```
