# Code Quality Standards

> **Purpose:** Establish hard rules for code quality across all projects
> **Last Updated:** January 7, 2026
> **Status:** MANDATORY - These are not suggestions

---

## Critical Rule #0: EVERY PROJECT MUST HAVE AN INDEX FILE

### The Rule

**EVERY project MUST have a `00_Index_[ProjectName].md` file in its root directory.**

### Why This Exists

**Projects without indexes are invisible and forgotten.** We've had:
- Projects started and abandoned without documentation
- Forgotten what a project does 3 months later
- Duplicate work because we didn't know a project existed
- No way to search or organize 36+ projects
- Lost context on tech decisions and architecture

---

## Critical Rule #1: NO SILENT FAILURES (Error Laundering Ban)

### The Rule

**NEVER use `except: pass` or `except Exception: pass` without logging.**

### Why This Exists (The Scar)
**Silent failures are UNTRUSTWORTHY failures.** We've had multiple projects where:
- Parsing silently failed -> wrong data in database -> bad decisions
- File operations silently failed -> data loss not discovered until weeks later
- API calls silently failed -> features appeared to work but didn't
- Integration issues silently failed -> wasted hours debugging "phantom" problems

### The "Error Laundering" Ban
Any code that catches an exception and continues without either (a) fixing the issue, (b) logging the error with context, or (c) raising a more specific exception is considered **Toxic**.

---

## Critical Rule #2: INDUSTRIAL SUBPROCESS INTEGRITY

### The Rule
All `subprocess.run()` calls must include `check=True` and a reasonable `timeout`.

### Why This Exists (The "Hanging" Scar)
We have had scripts hang indefinitely in CI or background loops because a subprocess (like `yt-dlp` or `ollama`) became unresponsive. Unbounded subprocesses are resource leaks.

---

## Critical Rule #3: MEMORY & SCALING GUARDS

### The Rule
Any script that aggregates or processes unbounded data (e.g., `synthesis.py` loading a whole library) MUST implement size guards or a Map-Reduce strategy to prevent Out-Of-Memory (OOM) crashes and LLM context overflows.

### Why This Exists (The "Context Ceiling" Scar)
As the `analyze-youtube-videos` library grew, simple string concatenation caused the script to crash once it exceeded 128k tokens.

### What to Do
#### BAD: Unbounded Accumulation
```python
aggregated_text = ""
for file in library.glob("*.md"):
    aggregated_text += file.read_text() # Scaling failure at 100+ files
```

#### GOOD: Size-Aware Batching
```python
MAX_TOKENS = 100000
current_tokens = 0
for file in library.glob("*.md"):
    content = file.read_text()
    if current_tokens + len(content)//4 > MAX_TOKENS:
        # Trigger Map-Reduce or truncate
        break
    aggregated_text += content
```

---

## Critical Rule #4: INPUT SANITIZATION & PATH SAFETY

### The Rule
**ALL user-provided strings used in file paths (titles, slugs, categories) MUST be sanitized using a `safe_slug()` function to prevent Path Traversal and shell injection.**

### Why This Exists (The "Clobber" Scar)
In the `bridge.py` review of Jan 2026, it was discovered that an attacker (or a malicious transcript) could provide a skill name like `../../Documents/Secrets` which would cause the script to write files outside the project root.

### What to Do
#### BAD: Direct Slug Construction
```python
slug = title.lower().replace(" ", "-") # Malicious '../' strings will bypass this
target_path = GLOBAL_LIBRARY_PATH / slug
```

#### GOOD: Sanitized Path Safety
```python
import re
import unicodedata

def safe_slug(text: str) -> str:
    """Sanitize string for safe file path usage."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

# Usage:
slug = safe_slug(title)
target_path = (GLOBAL_LIBRARY_PATH / slug).resolve()
if not target_path.is_relative_to(GLOBAL_LIBRARY_PATH.resolve()):
    raise ValueError("Security Alert: Path Traversal detected.")
```

---

## Critical Rule #5: PORTABLE CONFIGURATION (.env.example)

### The Rule
Every project MUST include a `.env.example` file. This file must be the "Documentation by Example" for the project.

### Why This Exists (The "Machine-Lock" Scar)
If a project is cloned from GitHub without a `.env.example`, the developer has to guess which environment variables are needed. If the project uses absolute paths for things like `SKILLS_LIBRARY_PATH`, the project is "locked" to a specific machine.

### What to Do
# Skills are deployed to ~/.claude/skills/
2. Include a `check_environment()` function in your `config.py` that verifies the presence of required variables and provides a "Human-Actionable" error message if they are missing.

---

## Rule #6: Use Python logging Module

### The Rule
**Use Python's `logging` module, not print() for debugging or errors.**

---

## Rule #7: Type Hints for Public Functions

### The Rule
**All public functions must have type hints for parameters and return values.**

---

## Rule #8: CLI Tool Design (The `pt` Gold Standard)

### The Rule
**All command-line tools MUST be designed for AI-first usage following the `pt` command pattern.**

### Why This Exists (The "Watching AI Work" Lesson)
By observing AI agents interact with our tools, we discovered they consistently:
- Run `--help` on every command to understand usage
- Struggle with rich formatting (colors, tables, progress bars)
- Need structured output for parsing
- Benefit from batch operations to reduce round-trips

The `pt` command (project-tracker CLI) became our gold standard by addressing all these pain points.

### Required Features

#### 1. Comprehensive Help Documentation
```bash
# Every command and subcommand must have --help
tool --help
tool subcommand --help
```

**Why:** AI agents discover functionality through `--help`. If it's not documented there, it doesn't exist to them.

#### 2. Plain Text Output by Default
```bash
# BAD: Rich formatting that AI can't parse
✓ Task #1234 [████████░░] 80% Complete

# GOOD: Plain text, single-line format
#1234 | In Progress | High | Implement feature X
```

**Why:** Colors, progress bars, and tables break AI parsing. Use simple, consistent formats.

#### 3. JSON Output Flag
```bash
# Always provide --json for structured data
tool tasks list --json
```

**Why:** When AI needs to process output programmatically, JSON is the universal format.

#### 4. Batch Operations
```bash
# BAD: Requires multiple commands
tool tasks done 1
tool tasks done 2
tool tasks done 3

# GOOD: Single command with multiple IDs
tool tasks done 1 2 3
```

**Why:** Reduces round-trips and makes AI workflows more efficient.

#### 5. Smart Auto-Detection
```bash
# Auto-detect context when possible
cd my-project/
tool tasks list  # Automatically filters to current project
```

**Why:** Reduces cognitive load and command verbosity.

#### 6. Clear, Actionable Error Messages
```bash
# BAD: Cryptic error
Error: Invalid input

# GOOD: Actionable guidance
Error: Task ID '999' not found.
Available tasks: Run 'tool tasks list' to see all tasks.
```

**Why:** AI agents need to know what went wrong AND how to fix it.

### CLI Design Checklist

When building a new CLI tool, verify:

- [ ] `--help` works on all commands and subcommands
- [ ] Default output is plain text (no colors, no rich formatting)
- [ ] `--json` flag available for structured output
- [ ] Batch operations supported where applicable
- [ ] Auto-detection of context (project, user, etc.)
- [ ] Error messages include next steps
- [ ] Single-line output format for lists
- [ ] Consistent command structure (verb-noun pattern)

### Example: The `pt` Command

```bash
# Help documentation
pt --help
pt tasks --help

# Plain text list output
pt tasks
#4650 | To Do | Medium | Add global warning banner

# JSON output
pt tasks --json
{"id": 4650, "status": "To Do", "priority": "Medium", ...}

# Batch operations
pt tasks done 4650 4651 4652

# Auto-detection
cd project-tracker/
pt tasks  # Automatically shows project-tracker tasks

# Clear errors
pt tasks show 99999
Error: Task #99999 not found.
Run 'pt tasks' to see all available tasks.
```

### What This Means for Development

**CLI = Command-Line Interface** - Any tool you run from the terminal (like `pt`, `git`, `ls`, etc.)

When building tools that AI agents will use:
1. Think about how AI will discover the tool (`--help`)
2. Think about how AI will parse the output (plain text)
3. Think about how AI will use it efficiently (batch operations)
4. Think about how AI will recover from errors (clear messages)

**The `pt` command is our reference implementation.** Study it when building new tools.

---

## Code Quality Checklist
*(Standard checks for every commit)*

- [ ] No silent `except: pass`
- [ ] Subprocess `check=True` and `timeout` present
- [ ] Memory/Scaling guards for large reads
- [ ] Input sanitization with `safe_slug()`
- [ ] `.env.example` relative paths verified
- [ ] Public functions typed
- [ ] CLI tools follow `pt` gold standard (if applicable)

---

**Version:** 1.3.0
**Established:** January 7, 2026
**Updated:** February 22, 2026 - Added Rule #8 (CLI Tool Design)
**Trigger:** Scaffolding v2 review found pervasive portability and safety violations. CLI standards added after `pt` command success.
