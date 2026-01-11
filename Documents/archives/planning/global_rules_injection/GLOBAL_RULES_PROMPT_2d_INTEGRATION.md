# Worker Task 2d: Integration
**Worker Model:** DeepSeek-R1
**Objective:** Add `run_update` and update `main()` in `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `run_update(projects_root: pathlib.Path, backup_dir: pathlib.Path, execute: bool = False) -> bool`
- [ ] **Logic:** Orchestrates the full scan and update process.
- [ ] **Integration:** `main()` now calls `run_update`.

### CONSTRAINTS (READ FIRST)
- REMOVE `run_dry_run` if it becomes redundant (it should be replaced by `run_update`).

### Reference Code Snippet
```python
def run_update(projects_root: pathlib.Path, backup_dir: pathlib.Path, execute: bool = False) -> bool:
    cursorrules_files = find_cursorrules_files(projects_root)
    if not cursorrules_files:
        logger.warning("No .cursorrules files found")
        return True
    stats = {'ok': 0, 'updated': 0}
    for cr_path in cursorrules_files:
        result = update_cursorrules(cr_path, backup_dir, execute)
        stats[result] += 1
    logger.info("-" * 60)
    logger.info(f"Summary: {stats['ok']} OK, {stats['updated']} {'updated' if execute else 'would update'}")
    return True

# In main():
backup_dir = args.backup_dir.resolve()
success = run_update(args.root, backup_dir, execute=args.execute)
```
