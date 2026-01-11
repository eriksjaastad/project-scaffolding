# Worker Task 2c: Add Update Logic
**Worker Model:** DeepSeek-R1
**Objective:** Add `update_cursorrules` to `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `update_cursorrules(cursorrules_path: pathlib.Path, backup_dir: pathlib.Path, execute: bool = False) -> str`
- [ ] **Logic:** Checks compliance, handles backup if execute is True, writes updated content.
- [ ] **Returns:** 'ok' or 'updated'.

### CONSTRAINTS (READ FIRST)
- DO NOT change existing functions.
- FOLLOW the snippet exactly.

### Reference Code Snippet
```python
def update_cursorrules(cursorrules_path: pathlib.Path, backup_dir: pathlib.Path, execute: bool = False) -> str:
    compliance = check_compliance(cursorrules_path)
    project = compliance['project']
    if compliance['has_trash_rule'] and compliance['has_silent_rule']:
        logger.info(f"OK: {project} - already has safety rules")
        return 'ok'
    content = cursorrules_path.read_text()
    new_content = inject_safety_rules(content, compliance['has_trash_rule'], compliance['has_silent_rule'])
    if execute:
        create_backup(cursorrules_path, backup_dir)
        cursorrules_path.write_text(new_content)
        logger.info(f"UPDATED: {project}")
    else:
        logger.info(f"WOULD UPDATE: {project}")
    return 'updated'
```
