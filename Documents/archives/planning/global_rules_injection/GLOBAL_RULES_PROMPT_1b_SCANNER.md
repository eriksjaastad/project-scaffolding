# Worker Task 1b: Add Project Scanner
**Worker Model:** DeepSeek-R1
**Objective:** Add the `find_cursorrules_files` function to `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Function added:** `find_cursorrules_files(projects_root: pathlib.Path) -> list[pathlib.Path]`
- [ ] **Logic:** Uses `projects_root.iterdir()` to find directories.
- [ ] **Filtering:** Skips files, skips dirs starting with `.` or `_`.
- [ ] **Matching:** Checks for `.cursorrules` in each project directory.
- [ ] **Sorting:** Returns a sorted list of paths.

### CONSTRAINTS (READ FIRST)
- DO NOT use `os.walk`. Use `pathlib.Path.iterdir()` as shown below.
- DO NOT change the existing imports or `main()` function yet.

### Reference Code Snippet
```python
def find_cursorrules_files(projects_root: pathlib.Path) -> list[pathlib.Path]:
    """Find all .cursorrules files in project directories (not nested)."""
    cursorrules_files = []
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir():
            continue
        if project_dir.name.startswith('.') or project_dir.name.startswith('_'):
            continue
        cursorrules = project_dir / ".cursorrules"
        if cursorrules.exists():
            cursorrules_files.append(cursorrules)
    return sorted(cursorrules_files)
```


## Related Documentation

- [[LOCAL_MODEL_LEARNINGS]] - local AI

