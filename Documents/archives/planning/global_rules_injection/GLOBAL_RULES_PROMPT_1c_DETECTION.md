# Worker Task 1c: Add Compliance Detection
**Worker Model:** DeepSeek-R1
**Objective:** Add the `check_compliance` function to `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `check_compliance(cursorrules_path: pathlib.Path) -> dict`
- [ ] **Logic:** Reads file content.
- [ ] **Detection:** Returns dict with `has_trash_rule` (if "Trash, Don't Delete" in content) and `has_silent_rule` (if "Silent Failures" in content).

### CONSTRAINTS (READ FIRST)
- DO NOT change existing functions.
- ONLY add the requested function.

### Reference Code Snippet
```python
def check_compliance(cursorrules_path: pathlib.Path) -> dict:
    """Check if a .cursorrules file has the required safety rules."""
    content = cursorrules_path.read_text()
    return {
        'path': cursorrules_path,
        'project': cursorrules_path.parent.name,
        'has_trash_rule': "Trash, Don't Delete" in content,
        'has_silent_rule': "Silent Failures" in content,
    }
```
