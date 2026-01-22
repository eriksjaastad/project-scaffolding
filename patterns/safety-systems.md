# Safety Systems Patterns

> **Philosophy:** "Every safety system was a scar"
> **Source:** Extracted from battle-tested projects
> **Last Updated:** December 21, 2025

> **Industry Context:** These patterns align with production AI safety practices. See [Documents/reports/trustworthy_ai_report.md](../Documents/reports/trustworthy_ai_report.md) for how Google DeepMind, Anthropic, and Microsoft implement defense-in-depth safety systems.

---

## Core Philosophy

### Build Protections After Learning What Breaks

**Don't** over-engineer safety systems for theoretical risks.  
**Do** wait until something actually breaks.  
**Then** build the specific protection needed.  
**Always** document WHY the safety system exists (the scar story).

**Benefits:**
- Focused safety systems (not bloated)
- Clear purpose (scar = story = lesson)
- Easier to maintain (you know why it matters)
- Better than guessing what might break

---

## Pattern 1: Append-Only Archives

### What

Critical data files are never modified or deleted, only appended.

### When to Use

- Historical records (logs, journals, transactions)
- User data (memories, entries, sessions)
- Training data (ML datasets)
- Audit trails (who did what when)

### Implementation

**File naming convention:**
```
data/
├── memories/
│   ├── 2025-12-15.json
│   ├── 2025-12-16.json
│   └── 2025-12-17.json
```

**Rules:**
1. One file per time period (day, hour, etc.)
2. Once written, never modify
3. New data = new file
4. Deletion = archive/move, not rm

**Code Pattern:**

```python
import tempfile
import shutil
from pathlib import Path
from datetime import date

def save_append_only(data_dir: Path, data: str, file_date: date) -> None:
    """
    Save data to append-only archive.
    
    Safety guarantees:
    - Won't corrupt if interrupted (atomic write)
    - Won't overwrite existing files (check first)
    - Won't delete data (only creates)
    
    Scar story: Lost 3 days of data to a half-written file
    when script was interrupted. Now we use atomic writes.
    """
    target = data_dir / f"{file_date}.json"
    
    # Never overwrite existing files
    if target.exists():
        raise FileExistsError(
            f"Archive already exists: {target}. "
            "Append-only archives cannot be modified."
        )
    
    # Atomic write: temp file → rename
    temp_fd, temp_path = tempfile.mkstemp(
        suffix='.json',
        dir=data_dir
    )
    
    try:
        with open(temp_fd, 'w') as f:
            f.write(data)
        
        # Atomic rename (POSIX guarantee: won't corrupt)
        shutil.move(temp_path, target)
        
    except Exception:
        # Clean up temp file on failure
        Path(temp_path).unlink(missing_ok=True)
        raise
```

### Evidence from Projects

**Cortana Personal AI:**
- Memory files: `data/memories/daily/YYYY-MM-DD.json`
- 108 days of memories, never modified after creation
- Scar: None yet (built with this pattern from start)

**image-workflow:**
- File operation logs: append-only audit trail
- Session summaries: one file per session, immutable
- Scar: Early version modified files in place, corrupted data during crashes

**trading-copilot:**
- Trade journal: `04_journal/daily/YYYY-MM-DD_journal.md`
- One entry per day, never edited
- Scar: Accidentally overwrote week's worth of notes before this pattern

---

## Pattern 2: Read-Only Source Data

### What

Original source data is NEVER modified by processing pipelines. Only read and transformed elsewhere.

### When to Use

- Raw data from external sources (APIs, files, databases)
- User-provided files (images, documents)
- Historical data (market data, sensor readings)

### Implementation

**Directory structure:**
```
project/
├── source_data/          # READ ONLY - never write here
│   └── raw_files/
├── processed_data/       # Write transformed data here
│   └── cleaned/
└── output/               # Write final results here
```

**Code Pattern:**

```python
from pathlib import Path

class DataProcessor:
    """
    Process data with read-only source guarantee.
    
    Scar story: Accidentally modified source images during
    processing. Couldn't re-run pipeline from original data.
    Lost 2 days re-acquiring the images.
    """
    
    def __init__(self, source_dir: Path, output_dir: Path):
        self.source_dir = source_dir
        self.output_dir = output_dir
        
        # Sanity check: different directories
        if self.source_dir == self.output_dir:
            raise ValueError("Source and output must be different directories")
    
    def process(self) -> None:
        """Process all source files."""
        for source_file in self.source_dir.glob("*.txt"):
            # NEVER modify source_file
            # Read, transform, write to new location
            
            data = source_file.read_text()
            transformed = self._transform(data)
            
            output_file = self.output_dir / source_file.name
            output_file.write_text(transformed)
    
    def _transform(self, data: str) -> str:
        """Transform data (implementation detail)."""
        return data.upper()
```

**OS-level protection (optional):**

```bash
# Make source directory read-only
chmod -R 444 source_data/
chmod +X source_data/  # Keep directory executable

# Now even bugs can't modify it
```

### Evidence from Projects

**image-workflow:**
- Original PNG/YAML files never modified
- Files are moved to new directories, not edited
- Scar: Early version edited metadata in place, corrupted files

**Cortana Personal AI:**
- SuperWhisper database is read-only
- Wispr Flow database is read-only
- All processing writes to separate `data/memories/` directory
- Scar: None (built with this principle from start)

**trading-copilot:**
- Raw market data CSVs never modified
- Paper trading history files read-only
- All analysis writes to separate `data/` directory
- Scar: Accidentally truncated CSV during parsing bug

---

## Pattern 3: Atomic Writes

### What

Critical file writes are atomic - they either complete fully or not at all. No partial/corrupted files.

### When to Use

- Any file where corruption would be disastrous
- Config files
- Database exports
- Data archives
- State files

### Implementation

**Pattern:**
1. Write to temporary file
2. Validate/verify (optional but recommended)
3. Atomic rename to target location

**Why it works:** On POSIX systems (macOS, Linux), `rename()` is atomic. Either the old file exists or the new file exists, never a corrupted in-between state.

**Code Pattern:**

```python
import tempfile
import shutil
import json
from pathlib import Path
from typing import Any

def save_json_atomically(target_path: Path, data: dict[str, Any]) -> None:
    """
    Save JSON with atomic write guarantee.
    
    Guarantees:
    - Won't leave partial files if interrupted
    - Won't corrupt existing file if write fails
    - Either old file or new file exists, never corrupted
    
    Scar story: Script interrupted during write, left
    corrupted JSON. Couldn't parse it, lost the data.
    """
    
    # 1. Write to temp file in same directory
    #    (same filesystem = atomic rename works)
    temp_fd, temp_path = tempfile.mkstemp(
        suffix='.json',
        dir=target_path.parent  # Same dir = same filesystem
    )
    
    try:
        # 2. Write data
        with open(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # 3. Validate (optional but recommended)
        with open(temp_path, 'r') as f:
            loaded = json.load(f)  # Ensure it's valid JSON
        
        # 4. Atomic rename
        #    If this succeeds, file is guaranteed complete
        #    If this fails, old file still intact
        shutil.move(temp_path, target_path)
        
    except Exception as e:
        # Clean up temp file on failure
        Path(temp_path).unlink(missing_ok=True)
        raise RuntimeError(f"Failed to save {target_path}") from e
```

**Alternative: Context Manager**

```python
from contextlib import contextmanager
from typing import Generator
import tempfile
from pathlib import Path

@contextmanager
def atomic_write(target_path: Path) -> Generator[Path, None, None]:
    """
    Context manager for atomic writes.
    
    Usage:
        with atomic_write(Path("config.json")) as temp_path:
            temp_path.write_text(data)
        # File is now atomically written
    """
    temp_fd, temp_path_str = tempfile.mkstemp(
        suffix=target_path.suffix,
        dir=target_path.parent
    )
    temp_path = Path(temp_path_str)
    
    try:
        # Close the fd, just use the path
        import os
        os.close(temp_fd)
        
        yield temp_path
        
        # Atomic rename after context exits successfully
        shutil.move(temp_path, target_path)
        
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
```

### Evidence from Projects

**Cortana Personal AI:**
- Memory files use atomic writes
- Documented in CLAUDE.md as required pattern
- Scar: None (built with this from start, learned from other projects)

**image-workflow:**
- Critical config files use atomic writes
- Session logs use atomic writes
- Scar: Corrupted progress file during system crash, had to reconstruct state

---

## Pattern 4: Move, Don't Modify

### What

For files with metadata/state (images + YAML, data + schema), move entire groups together. Never modify in place.

### When to Use

- Files with companion files (image.png + image.yaml)
- Files with sidecars (data.csv + data.schema.json)
- Files in workflows (raw → processed → reviewed → final)

### Implementation

**Code Pattern:**

```python
from pathlib import Path
import shutil
from typing import List

def move_file_with_companions(
    source: Path,
    dest_dir: Path,
    companion_extensions: List[str] = ['.yaml', '.json', '.txt']
) -> List[Path]:
    """
    Move file and all companion files together.
    
    Safety guarantees:
    - All companions move together (or none move)
    - Preserves file relationships
    - Rollback on failure
    
    Scar story: Moved PNG files but forgot YAML metadata.
    Lost captions for 500 images. Couldn't match them back up.
    """
    
    moved_files: List[Path] = []
    
    try:
        # Find all companions
        companions = [source]
        for ext in companion_extensions:
            companion = source.with_suffix(ext)
            if companion.exists():
                companions.append(companion)
        
        # Move all together
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file in companions:
            dest = dest_dir / file.name
            shutil.move(str(file), str(dest))
            moved_files.append(dest)
        
        return moved_files
        
    except Exception as e:
        # Rollback: move everything back
        for dest in moved_files:
            try:
                shutil.move(str(dest), str(source.parent / dest.name))
            except Exception:
                pass  # Best effort rollback
        
        raise RuntimeError(
            f"Failed to move {source} with companions"
        ) from e
```

**Validation Helper:**

```python
def verify_companions_exist(
    files: List[Path],
    required_extensions: List[str] = ['.yaml']
) -> None:
    """
    Verify all files have required companions.
    
    Raises ValueError if any companions are missing.
    """
    missing = []
    
    for file in files:
        for ext in required_extensions:
            companion = file.with_suffix(ext)
            if not companion.exists():
                missing.append((file, ext))
    
    if missing:
        error_msg = "Missing companion files:\n"
        for file, ext in missing:
            error_msg += f"  {file} missing {ext}\n"
        raise ValueError(error_msg)
```

### Evidence from Projects

**image-workflow:**
- All PNG files have YAML companions
- FileTracker utility moves both together
- Scar: Lost metadata for 500 images by moving only PNGs

---

## Pattern 5: Trash, Don't Delete

### What

Use operating system trash/recycle bin for deletions, not `rm`/`os.remove()`. Allows recovery from mistakes.

### When to Use

- Any user-facing deletion operation
- Cleanup scripts
- File management tools
- Anywhere mistakes are possible

### Implementation

**Python (using send2trash):**

```bash
pip install send2trash
```

```python
from send2trash import send2trash
from pathlib import Path

def delete_safely(path: Path) -> None:
    """
    Delete file using OS trash/recycle bin.
    
    Benefits over os.remove():
    - Recoverable if mistake
    - User can review trash before emptying
    - Familiar to users
    
    Scar story: Accidentally deleted 300 files with
    os.remove(). Gone forever. Now we use trash.
    """
    if not path.exists():
        raise FileNotFoundError(f"Cannot delete: {path}")
    
    send2trash(str(path))
    print(f"Moved to trash: {path}")
```

**Bash alternative:**

```bash
# macOS - trash CLI is built-in at /usr/bin/trash
trash myfile.txt

# Linux (requires trash-cli)
# sudo apt-get install trash-cli
trash-put myfile.txt
```

### Evidence from Projects

**image-workflow:**
- All file deletions use send2trash
- Documented in safety rules: "NEVER use os.remove()"
- Scar: Deleted 300 reviewed images, couldn't recover

---

## Pattern 6: Validate Before Writing

### What

Validate data structure/format before writing to critical files.

### When to Use

- JSON/YAML config files
- Data archives
- State files
- Anything where corruption breaks the system

### Implementation

```python
import json
from pathlib import Path
from typing import Any
from dataclasses import dataclass, asdict

@dataclass
class MemoryEntry:
    """Validated data structure."""
    date: str
    projects: list[str]
    decisions: list[str]
    summary: str
    
    def validate(self) -> None:
        """Validate field constraints."""
        if not self.date:
            raise ValueError("date is required")
        if len(self.summary) > 10000:
            raise ValueError("summary too long (max 10000 chars)")

def save_with_validation(path: Path, entry: MemoryEntry) -> None:
    """
    Save data with validation.
    
    Scar story: Wrote invalid JSON (missing required field).
    Broke the entire system. Now we validate first.
    """
    # 1. Validate structure
    entry.validate()
    
    # 2. Convert to dict
    data = asdict(entry)
    
    # 3. Test serialization (ensure it's JSON-able)
    test_json = json.dumps(data)
    
    # 4. Test deserialization (ensure it round-trips)
    json.loads(test_json)
    
    # 5. Now safe to write (using atomic write from Pattern 3)
    save_json_atomically(path, data)
```

---

## Pattern 7: Sandbox Draft Pattern (V4)

### What

Untrusted agents write to a controlled sandbox directory. A gatekeeper reviews diffs before applying changes to target files.

### When to Use

- Multi-agent systems where workers need to edit files
- AI assistants that generate code
- Any system where untrusted processes need write access
- Workflows where parse failures from code extraction are unacceptable

### Implementation

**Directory structure:**
```
project/
├── _handoff/
│   └── drafts/           # SANDBOX - workers can ONLY write here
│       ├── file.py.task123.draft
│       └── task123.submission.json
├── src/                  # TARGET - workers CANNOT write here directly
│   └── file.py
```

**Security Layers:**

```python
# Layer 1: Path Validation (sandbox.py)
def validate_sandbox_write(path: str) -> ValidationResult:
    """
    SECURITY CRITICAL: Only allow writes to sandbox.

    Checks:
    1. Path must resolve inside _handoff/drafts/
    2. No path traversal (..)
    3. Only .draft or .submission.json extensions
    """
    target = Path(path).resolve()
    sandbox = SANDBOX_DIR.resolve()

    if not target.is_relative_to(sandbox):
        return ValidationResult(valid=False, reason="Outside sandbox")

    if ".." in str(path):
        return ValidationResult(valid=False, reason="Path traversal")

    return ValidationResult(valid=True, resolved_path=target)


# Layer 2: Content Analysis (draft_gate.py)
SECRET_PATTERNS = [
    r'sk-[a-zA-Z0-9]{20,}',           # OpenAI
    r'ANTHROPIC_API_KEY',              # Anthropic
    r'password\s*=\s*["\'][^"\']+["\']' # Hardcoded passwords
]

HARDCODED_PATH_PATTERNS = [
    r'/Users/[a-zA-Z0-9_]+/',          # macOS home dirs
    r'/home/[a-zA-Z0-9_]+/',           # Linux home dirs
]

def analyze_diff(original: str, draft: str) -> SafetyAnalysis:
    """Check diff for security issues."""
    # ... implementation
    return SafetyAnalysis(
        has_secrets=check_patterns(draft, SECRET_PATTERNS),
        has_hardcoded_paths=check_patterns(draft, HARDCODED_PATH_PATTERNS),
        deletion_ratio=calculate_deletion_ratio(original, draft)
    )


# Layer 3: Gate Decision
class GateDecision(Enum):
    ACCEPT = "accept"    # Apply the diff
    REJECT = "reject"    # Discard, log reason
    ESCALATE = "escalate" # Needs human review

def gate_draft(submission: DraftSubmission) -> GateResult:
    """
    Floor Manager reviews draft and decides.

    Scar story: Local model wrote API keys into a config file.
    Without the gate, it would have been committed.
    """
    safety = analyze_diff(submission.original, submission.draft)

    if safety.has_secrets:
        return GateResult.reject("Contains secrets")

    if safety.has_hardcoded_paths:
        return GateResult.reject("Contains hardcoded paths")

    if safety.deletion_ratio > 0.5:
        return GateResult.escalate("Large deletion (>50%)")

    return GateResult.accept(diff_summary, safety)
```

**Draft Workflow:**

```
Worker                      Floor Manager              Target
  │                              │                        │
  ├──request_draft(file.py)─────▶│                        │
  │                              ├──copy to sandbox──────▶│
  │◀──────────────draft_path─────┤                        │
  │                              │                        │
  ├──write_draft(content)───────▶│                        │
  │                              ├──write to sandbox      │
  │                              │                        │
  ├──submit_draft()─────────────▶│                        │
  │                              ├──GATE: analyze diff    │
  │                              ├──GATE: check safety    │
  │                              ├──GATE: decide          │
  │                              │                        │
  │                              ├───[ACCEPT]────────────▶│ apply
  │◀──────────────result─────────┤                        │
```

### Evidence from Projects

**agent-hub (V4):**
- Workers write to `_handoff/drafts/` only
- Floor Manager gates all submissions
- Parse failure rate: ~15% → ~0%
- Security bypasses: 0
- Scar: Pre-V4, had to parse Worker output with regex, broke constantly

### Trade-offs

| Pro | Con |
|-----|-----|
| Workers can "edit" files safely | Extra complexity in tooling |
| Parse failures eliminated | Requires sandbox directory |
| Security maintained | Gate adds latency |
| Full audit trail | Workers need draft tools |

### When NOT to Use

- Single-agent systems (no untrusted actors)
- Read-only workflows
- When direct file access is acceptable (trusted environment)

---

## Safety System Checklist

When building a new project, ask these questions:

### Data Safety
- [ ] Is there critical data that shouldn't be modified?
  - → Implement append-only archives (Pattern 1)
- [ ] Is there source data that should never change?
  - → Implement read-only source pattern (Pattern 2)
- [ ] Are there files where corruption would be disastrous?
  - → Implement atomic writes (Pattern 3)

### File Safety
- [ ] Are there files with companions/metadata?
  - → Implement move-with-companions (Pattern 4)
- [ ] Are there user-facing deletions?
  - → Implement trash-don't-delete (Pattern 5)
- [ ] Are there structured data files (JSON, YAML)?
  - → Implement validate-before-write (Pattern 6)

### Multi-Agent Safety
- [ ] Do untrusted agents need to write files?
  - → Implement Sandbox Draft Pattern (Pattern 7)

### Don't Overdo It
- [ ] Have you actually experienced this failure mode?
  - If NO: Don't build it yet. Wait for the scar.
  - If YES: Document the scar story, then build protection.

---

## Scar Story Template

When documenting a safety system, always include the scar story:

```markdown
### Pattern Name

**Scar story:** [What broke? When? What were the consequences?]

**Protection:** [What system did you build to prevent recurrence?]

**Trade-offs:** [What does this cost? Speed? Complexity? Is it worth it?]

**Evidence:** [Which projects use this? Has it prevented issues?]
```

---

## Anti-Patterns

### ❌ Safety Theater

Building safety systems for problems you haven't experienced.

**Why it's bad:**
- Adds complexity without benefit
- Slows development
- May not actually protect against real risks

**Instead:** Wait for the scar, then protect against THAT specific failure.

---

### ❌ Redundant Safety

Multiple layers of protection for the same failure mode.

**Example:**
- Atomic writes ✓
- Backup before write ✓
- Write to separate file ✓
- Checksum validation ✓
- ← This is overkill

**Instead:** Pick the appropriate pattern for your risk level.

---

### ❌ Undocumented Safety

Safety systems without scar stories.

**Why it's bad:**
- Future developers don't know why it exists
- Might get removed as "unnecessary complexity"
- Can't evaluate if it's still needed

**Instead:** Always document the scar story. Why does this exist?

---

## Summary

**Core principle:** "Every safety system was a scar"

**Seven proven patterns:**
1. **Append-Only Archives** - Never modify historical data
2. **Read-Only Source Data** - Never write to original files
3. **Atomic Writes** - No partial/corrupted files
4. **Move, Don't Modify** - Keep file groups together
5. **Trash, Don't Delete** - Recoverable deletions
6. **Validate Before Writing** - Catch errors before persistence
7. **Sandbox Draft Pattern** - Gate untrusted agent writes (V4)

**When to use them:**
- Wait for the scar (actual failure)
- Build focused protection
- Document WHY (scar story)
- Don't over-engineer

---

*Based on battle scars from image-workflow (2.5 months), Cortana Personal AI, and trading-copilot.*

**Remember:** The best safety system is the one that prevents a failure you've actually experienced.

## Related Documentation

- [[PROJECT_KICKOFF_GUIDE]] - project setup
- [[trustworthy_ai_report]] - AI safety
- [[ai_training_methodology]] - AI training
- [[cost_management]] - cost management
- [[database_setup]] - database
- [[queue_processing_guide]] - queue/workflow
- [[ai_model_comparison]] - AI models
- [[case_studies]] - examples
- [[cortana_architecture]] - Cortana AI
- [[performance_optimization]] - performance
- [[cortana-personal-ai/README]] - Cortana AI
- [[image-workflow/README]] - Image Workflow
- [[trading-copilot/README]] - Trading Copilot
