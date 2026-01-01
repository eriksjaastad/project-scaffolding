# Code Quality Standards

> **Purpose:** Establish hard rules for code quality across all projects  
> **Last Updated:** December 31, 2025  
> **Status:** MANDATORY - These are not suggestions

---

## 🚨 Critical Rule #0: EVERY PROJECT MUST HAVE AN INDEX FILE

### The Rule

**EVERY project MUST have a `00_Index_[ProjectName].md` file in its root directory.**

### Why This Exists

**Projects without indexes are invisible and forgotten.** We've had:
- Projects started and abandoned without documentation
- Forgotten what a project does 3 months later
- Duplicate work because we didn't know a project existed
- No way to search or organize 36+ projects
- Lost context on tech decisions and architecture

### What the Index Must Contain

#### ✅ REQUIRED: Index File Structure

```markdown
---
tags:
  - map/project
  - p/[project-name]
  - type/[project-type]
  - domain/[domain]
  - status/[active|production|archived]
  - tech/[primary-tech]
created: YYYY-MM-DD
---

# Project Name

[Sentence 1: What this project does.] 
[Sentence 2: Key technologies and approach.] 
[Sentence 3: Current status.]

## Key Components

### [Component Name]
- `directory/` - Description
  - Key files

## Status

**Tags:** #map/project #p/[project-name]
**Status:** #status/[active|archived|production]
**Last Major Update:** [Date]
```

#### Template Location
`project-scaffolding/templates/00_Index_Template.md`

#### Full Documentation
`project-scaffolding/docs/PROJECT_INDEXING_SYSTEM.md`

### When to Create/Update

**CREATE:**
- Day 1 of new project (mandatory)
- Before first commit
- Part of project initialization

**UPDATE:**
- Major feature additions
- Status changes (active → production, active → archived)
- Tech stack changes
- Every 3-6 months minimum

### Enforcement

**Validation Script:**
```bash
# Check if project has index
./project-scaffolding/scripts/validate_project.py [project-name]

# Check all projects
./project-scaffolding/scripts/validate_project.py --all

# Create missing indexes
./project-scaffolding/scripts/reindex_projects.py --missing
```

**Git Pre-Commit Hook (Optional):**
```bash
# .git/hooks/pre-commit
if [ ! -f "00_Index_*.md" ]; then
  echo "ERROR: Missing project index file (00_Index_*.md)"
  echo "Create one using: project-scaffolding/templates/00_Index_Template.md"
  exit 1
fi
```

### The Scar

**We had 36 projects and couldn't find things.** No way to:
- Know what a project does without exploring code
- See which projects use which technologies
- Identify abandoned projects
- Search across projects
- Remember context 6 months later

**The pain:**
- Duplicated work because forgot similar project existed
- Wasted time re-learning what a project does
- No visibility into project health
- Couldn't organize or prioritize effectively

### Non-Negotiable

This is **not optional**. If a project doesn't have an index:
1. It's not a project yet, it's an experiment
2. It shouldn't be committed to the main projects folder
3. It should stay in `_inbox/` until properly documented

**Rule:** No project leaves `_inbox/` without an index file.

---

## 🚨 Critical Rule #1: NO SILENT FAILURES

### The Rule

**NEVER use `except: pass` or `except Exception: pass` without logging.**

### Why This Exists (The Scar)

**Silent failures are UNTRUSTWORTHY failures.** We've had multiple projects where:
- Parsing silently failed → wrong data in database → bad decisions
- File operations silently failed → data loss not discovered until weeks later  
- API calls silently failed → features appeared to work but didn't
- Integration issues silently failed → wasted hours debugging "phantom" problems

**The pain:**
- Hours of debugging to find where data went wrong
- Loss of trust in the entire system
- Can't tell if something broke or if there was never data there
- No way to diagnose production issues

### What to Do Instead

#### ❌ BAD: Silent Failure
```python
def parse_todo(file_path):
    try:
        content = file_path.read_text()
        return extract_status(content)
    except Exception:
        pass  # ❌ SILENT FAILURE - you'll never know it broke
    return None
```

**Why this is bad:**
- Returns `None` whether file doesn't exist, parsing failed, or status is actually None
- No way to tell the difference
- Debugging is impossible
- Trust in the data is destroyed

#### ✅ GOOD: Log and Fail Loudly
```python
import logging

logger = logging.getLogger(__name__)

def parse_todo(file_path):
    try:
        content = file_path.read_text()
        return extract_status(content)
    except FileNotFoundError:
        logger.warning(f"TODO.md not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}", exc_info=True)
        raise  # Re-raise so caller knows it failed
```

**Why this is better:**
- Specific exception handling (FileNotFoundError vs other errors)
- Logged warnings for expected issues (missing file)
- Logged errors with traceback for unexpected issues
- Re-raises unexpected exceptions so system fails visibly

#### ✅ BETTER: Explicit Error Handling with Context
```python
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class TODOParseError(Exception):
    """Raised when TODO.md exists but can't be parsed."""
    pass

def parse_todo(file_path: Path) -> Optional[str]:
    """
    Parse status from TODO.md file.
    
    Returns:
        Status string if found, None if file doesn't exist
        
    Raises:
        TODOParseError: If file exists but parsing fails
    """
    if not file_path.exists():
        logger.debug(f"TODO.md not found (expected): {file_path}")
        return None
    
    try:
        content = file_path.read_text(encoding='utf-8')
        status = extract_status(content)
        
        if status is None:
            logger.warning(
                f"TODO.md exists but no status found: {file_path}. "
                "Check format in file."
            )
        
        return status
        
    except UnicodeDecodeError as e:
        # Specific error for encoding issues
        logger.error(f"TODO.md has encoding issues: {file_path}")
        raise TODOParseError(f"Can't read {file_path}: encoding error") from e
        
    except Exception as e:
        # Unexpected error - log and raise
        logger.error(
            f"Unexpected error parsing {file_path}: {e}",
            exc_info=True
        )
        raise TODOParseError(f"Failed to parse {file_path}") from e
```

**Why this is best:**
- Explicit about what None means (file doesn't exist)
- Specific exception for parsing failures (TODOParseError)
- Different handling for expected vs unexpected errors
- Full context in logs
- Caller can decide how to handle each case

### Acceptable Uses of Silent Failure

There are **VERY FEW** cases where silent failure is acceptable:

#### ✅ Acceptable: Cleanup in finally/except blocks
```python
try:
    process_data()
finally:
    try:
        temp_file.unlink()
    except Exception:
        pass  # OK - cleanup failure shouldn't break main operation
```

#### ✅ Acceptable: Optional features that genuinely don't matter
```python
try:
    send_discord_notification(message)
except Exception:
    pass  # OK - notification failure shouldn't break core function
```

**But even these should be documented:**
```python
except Exception as e:
    # Silent failure OK: Discord notification is optional,
    # shouldn't break core functionality
    logger.debug(f"Discord notification failed (non-critical): {e}")
    pass
```

### Enforcement

**Code review MUST catch:**
- Any `except: pass` without comment explaining why
- Any `except Exception: pass` without logging
- Any broad exception handling without re-raise or log

**If you see this in code review:**
1. Point it out immediately
2. Ask: "What happens when this fails? How will we know?"
3. Require explicit error handling or justification

---

## 🔍 Rule #2: Use Python logging Module

### The Rule

**Use Python's `logging` module, not print() for debugging or errors.**

### Why

- `print()` goes to stdout and gets mixed with program output
- Can't filter or adjust verbosity
- No timestamps, no context
- Disappears in production

### Setup Logging

**In every script:**

```python
import logging

# Configure at module level
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for development
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to file
        logging.StreamHandler()           # Also log to console
    ]
)

logger = logging.getLogger(__name__)
```

**Log levels:**
- `DEBUG`: Detailed diagnostic info (development only)
- `INFO`: Confirmation things are working as expected
- `WARNING`: Something unexpected but handled
- `ERROR`: Error that affected functionality
- `CRITICAL`: Severe error, system may not recover

### When to Log What

```python
# DEBUG: Detailed diagnostic info
logger.debug(f"Processing file: {filename}")
logger.debug(f"Found {len(items)} items")

# INFO: Normal operations
logger.info(f"Scan complete: {count} projects found")
logger.info(f"Dashboard started on port 8000")

# WARNING: Unexpected but handled
logger.warning(f"TODO.md not found: {project_path}")
logger.warning(f"Invalid cron schedule: {schedule}")

# ERROR: Something failed
logger.error(f"Failed to parse {file}: {e}", exc_info=True)
logger.error(f"Database connection failed: {e}")

# CRITICAL: System-level failure
logger.critical(f"Database corrupted, cannot start")
```

---

## 📝 Rule #3: Type Hints for Public Functions

### The Rule

**All public functions must have type hints for parameters and return values.**

### Why

- Makes code self-documenting
- Catches bugs at development time (with mypy/pyright)
- Better IDE autocomplete
- Clearer contracts

### Examples

#### ❌ BAD: No type hints
```python
def parse_todo(file_path):
    # What type is file_path? str? Path?
    # What does this return? dict? str? None?
    pass
```

#### ✅ GOOD: Type hints
```python
from pathlib import Path
from typing import Optional

def parse_todo(file_path: Path) -> Optional[str]:
    """Parse status from TODO.md file."""
    pass
```

#### ✅ BETTER: Complete type hints
```python
from pathlib import Path
from typing import Optional, Dict, List, Any

def parse_todo(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse TODO.md file and extract metadata.
    
    Args:
        file_path: Path to TODO.md file
        
    Returns:
        Dict with keys: status, phase, completion_pct, ai_agents, cron_jobs
        None if file doesn't exist
        
    Raises:
        TODOParseError: If file exists but can't be parsed
    """
    pass
```

### When Type Hints Are Optional

- Private functions (but still encouraged)
- One-off scripts (but encouraged for complex logic)
- Very obvious types (but still better to include)

---

## 🛡️ Rule #4: Validate Inputs

### The Rule

**Validate external inputs before processing.**

### Why

- Prevents SQL injection (parameterized queries)
- Prevents path traversal attacks
- Catches malformed data early
- Clear error messages

### Examples

#### ❌ BAD: SQL Injection Vulnerability
```python
def get_project(order_by: str):
    query = f"SELECT * FROM projects ORDER BY {order_by}"  # ❌ VULNERABLE
    cursor.execute(query)
```

#### ✅ GOOD: Parameterized Query
```python
def get_project(order_by: str):
    # Whitelist allowed values
    allowed = ["name", "last_modified", "status"]
    if order_by not in allowed:
        raise ValueError(f"Invalid order_by: {order_by}")
    
    query = f"SELECT * FROM projects ORDER BY {order_by}"  # Safe - validated
    cursor.execute(query)
```

#### ❌ BAD: Path Traversal
```python
def read_project_file(filename: str):
    path = BASE_DIR / filename  # ❌ Could be "../../../etc/passwd"
    return path.read_text()
```

#### ✅ GOOD: Validated Path
```python
def read_project_file(filename: str) -> str:
    # Validate filename
    if '..' in filename or filename.startswith('/'):
        raise ValueError(f"Invalid filename: {filename}")
    
    path = BASE_DIR / filename
    
    # Ensure it's actually under BASE_DIR
    if not path.resolve().is_relative_to(BASE_DIR.resolve()):
        raise ValueError(f"Path outside base directory: {filename}")
    
    return path.read_text()
```

---

## 📦 Rule #5: Document Assumptions

### The Rule

**If your code assumes something about the environment, data format, or state, document it.**

### Examples

```python
def scan_projects(base_dir: Path = Path("/Users/eriksjaastad/projects")):
    """
    Scan for projects under base_dir.
    
    Assumptions:
    - base_dir exists and is readable
    - Projects have TODO.md or README.md
    - File system supports case-sensitive names (macOS/Linux)
    - User has read permissions for all subdirectories
    
    Note: Hardcoded path makes this non-portable. TODO: make configurable
    """
    pass
```

---

## ✅ Code Quality Checklist

Before committing code, verify:

### Error Handling
- [ ] No `except: pass` without logging and justification
- [ ] Specific exception types caught (not bare `except Exception`)
- [ ] Errors logged with context (`logger.error`)
- [ ] Unexpected errors re-raised or converted to custom exceptions

### Logging
- [ ] Uses `logging` module, not `print()`
- [ ] Appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Includes context in error messages
- [ ] Log files configured in production

### Type Safety
- [ ] Public functions have type hints
- [ ] Complex return types documented
- [ ] Optional vs required parameters clear

### Input Validation
- [ ] External inputs validated
- [ ] SQL queries use parameters, not f-strings
- [ ] File paths validated (no path traversal)
- [ ] User input sanitized

### Documentation
- [ ] Assumptions documented
- [ ] Scar stories included for safety systems
- [ ] Error cases documented
- [ ] Return value meanings clear (what does None mean?)

---

## 🚨 Critical Violations

**These will block code review:**

1. **Silent failures** - Any `except: pass` without clear justification
2. **SQL injection** - Any f-string SQL with user input
3. **No logging** - Production code without logging setup
4. **Hardcoded secrets** - API keys, passwords in code

**These are strongly discouraged:**

1. No type hints on public functions
2. No docstrings on complex functions
3. Print statements for errors/debugging
4. Broad exception catching without re-raise

---

## 📚 References

- **Error Handling:** See `patterns/safety-systems.md` for specific patterns
- **Logging:** Python logging module documentation
- **Type Hints:** PEP 484 (Type Hints), PEP 526 (Variable Annotations)

---

**Version:** 1.0  
**Established:** December 31, 2025  
**Trigger:** project-tracker code review found 7+ files with silent failures

---

*"Silent failures destroy trust. If it can fail, make it fail loudly."*

