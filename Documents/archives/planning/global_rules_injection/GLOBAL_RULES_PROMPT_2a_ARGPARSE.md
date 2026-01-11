# Worker Task 2a: Update Argparse + Constant
**Worker Model:** DeepSeek-R1
**Objective:** Add the safety rules constant and update argparse in `scripts/update_cursorrules.py`.

### 🎯 [ACCEPTANCE CRITERIA]
- [ ] **Constant Added:** `SAFETY_RULES_SECTION` string constant added at top level.
- [ ] **Argparse Updated:** Added `--execute` (action="store_true") and `--backup-dir` (type=pathlib.Path, default="_cursorrules_backups").

### CONSTRAINTS (READ FIRST)
- DO NOT implement any logic yet.
- KEEP existing functions.

### Reference Code Snippet
```python
SAFETY_RULES_SECTION = '''
---

## Safety Rules

### File Operations
- **Trash, Don't Delete:** NEVER use `rm`, `os.remove`, `os.unlink`, or `shutil.rmtree` for permanent deletion.
- ALWAYS use `send2trash` (Python) or move files to a `_trash/` directory.

### Error Handling
- **No Silent Failures:** NEVER swallow exceptions without logging.
- ALWAYS log errors with context (file path, operation attempted, error message).
'''

# ... in main() ...
parser.add_argument("--execute", action="store_true", help="Actually modify files")
parser.add_argument("--backup-dir", type=pathlib.Path, default=pathlib.Path("_cursorrules_backups"), help="Backup directory")
```
