# Worker Task 1d: Add Output Logic
**Worker Model:** DeepSeek-R1
**Objective:** Add `run_dry_run` and update `main()` to produce the final output.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `run_dry_run(projects_root: pathlib.Path) -> bool`
- [ ] **Logic:** Calls `find_cursorrules_files`, loops through them, calls `check_compliance`, and logs status.
- [ ] **Status Mapping:** Logs "OK" if both rules exist, "NEEDS UPDATE" if any missing.
- [ ] **Summary:** Logs summary of counts (OK, NEEDS UPDATE, Total).
- [ ] **Integration:** `main()` now calls `run_dry_run`.

### CONSTRAINTS (READ FIRST)
- DO NOT implement execute/update logic.
- OUTPUT format must match the reference.

### Reference Code Snippet
```python
def run_dry_run(projects_root: pathlib.Path) -> bool:
    """Show what would be updated without making changes."""
    logger.info("-" * 60)
    cursorrules_files = find_cursorrules_files(projects_root)
    if not cursorrules_files:
        logger.warning("No .cursorrules files found")
        return True
    stats = {'ok': 0, 'needs_update': 0}
    for cr_path in cursorrules_files:
        comp = check_compliance(cr_path)
        if comp['has_trash_rule'] and comp['has_silent_rule']:
            logger.info(f"OK: {comp['project']} - has all safety rules")
            stats['ok'] += 1
        else:
            missing = []
            if not comp['has_trash_rule']: missing.append("Trash rule")
            if not comp['has_silent_rule']: missing.append("Silent Failures rule")
            logger.info(f"NEEDS UPDATE: {comp['project']} - missing: {', '.join(missing)}")
            stats['needs_update'] += 1
    logger.info("-" * 60)
    logger.info(f"Summary: {stats['ok']} OK, {stats['needs_update']} need update, {len(cursorrules_files)} total")
    return True
```
