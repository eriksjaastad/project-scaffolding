# Pattern Analysis - Extracted from Source Projects

> **Status:** Living document  
> **Last Updated:** December 21, 2025  
> **Purpose:** Identify repeating patterns across projects for extraction into scaffolding

---

## How to Read This Document

Patterns are marked by **confidence level**:
- 🟢 **PROVEN** - Appears in 3+ projects, battle-tested
- 🟡 **EMERGING** - Appears in 2 projects, promising
- 🔵 **CANDIDATE** - Appears in 1 project, watch for repetition

---

## Pattern Categories

### 1. Documentation Structure Patterns

#### 🟢 PROVEN: The `Documents/` Pattern (image-workflow)

**What:** Centralized documentation directory with standardized subdirectories

**Structure:**
```
Documents/
├── core/              # Architecture, operations, disaster recovery
├── guides/            # How-to documents
├── reference/         # Code quality rules, knowledge base
├── ai/                # AI-specific documentation
├── safety/            # Safety systems and policies
├── archives/          # Timestamped historical docs
│   ├── sessions/      # (12-month retention)
│   ├── implementations/ # (keep indefinitely)
│   └── misc/          # (3-month retention)
└── README.md          # Index with quick links
```

**Evidence:**
- **image-workflow:** Full implementation, 2.5 months battle-tested
- **Cortana:** Has `docs/` with similar structure (core, guides, reference, archives)
- **Trading Projects:** Has `docs/` directory with guides and reference material

**Benefits:**
- Prevents root-level documentation sprawl
- Clear retention policies (archives with expiration dates)
- Easy onboarding ("Read core/ARCHITECTURE_OVERVIEW.md first")
- AI collaborators can find information quickly

**Extraction Ready:** Yes - create template structure

---

#### 🟡 EMERGING: The CLAUDE.md Pattern

**What:** Project-specific instructions file for AI collaborators

**Core Sections:**
1. **Required Reading** - What to read before writing code
2. **Project Summary** - Quick context
3. **Coding Standards** - Language-specific rules
4. **Safety Rules** - What never to modify
5. **Validation Commands** - How to check your work
6. **Common Patterns** - Frequently used code snippets

**Evidence:**
- **image-workflow:** `CLAUDE.md` (58 lines, focused on safety + typing)
- **Cortana:** `CLAUDE.md` (544 lines, comprehensive with examples)
- **Trading Projects:** No CLAUDE.md yet (but should have one!)

**Benefits:**
- AI gets context without guessing
- Reduces mistakes (especially file safety violations)
- Faster iterations (AI knows the patterns)
- Human developers benefit too (same rules)

**Extraction Ready:** Yes - create template with sections

---

#### 🟡 EMERGING: The ROADMAP.md Pattern

**What:** Long-term vision document separate from implementation tracking

**Structure:**
- Executive summary
- Current status
- Layered roadmap (incremental phases)
- Technical architecture
- Future integrations

**Evidence:**
- **Cortana:** Comprehensive ROADMAP.md (1400+ lines, 7 layers)
- **Trading Projects:** MODEL_ARENA_ROADMAP.md + TRADE_SNAPSHOT_ROADMAP.md
- **image-workflow:** No formal ROADMAP (uses TODO.md instead)

**Benefits:**
- Keeps big picture visible
- Helps AI understand "why" not just "what"
- Shows where the project is going (helps prioritize)
- Documents design decisions

**Extraction Ready:** Almost - need to see 3rd instance

---

### 2. Safety System Patterns

#### 🟢 PROVEN: "Every Safety System Was a Scar"

**What:** Build protections AFTER you learn what breaks, not before

**Philosophy:**
- Don't over-engineer safety for theoretical risks
- Wait until something actually breaks
- Then build the specific protection needed
- Document WHY the safety system exists

**Evidence:**
- **image-workflow:** FileTracker, send2trash, companion file tracking (all from real incidents)
- **Cortana:** Atomic writes for memory files, read-only SuperWhisper access
- **Trading Projects:** Risk breach logging (from actual trading mistakes)

**Benefits:**
- Focused safety systems (not bloated)
- Clear purpose (scar = story = lesson)
- Easier to maintain (you know why it matters)

**Extraction Ready:** Yes - create pattern documentation

---

#### 🟡 EMERGING: Append-Only Archives Pattern

**What:** Critical data files are never modified, only appended

**Implementation:**
- Write to temp file first
- Validate before committing
- Atomic rename (won't corrupt if interrupted)
- Never delete, only archive

**Evidence:**
- **image-workflow:** File operation logs (append-only)
- **Cortana:** Memory files (append-only JSON + MD per day)
- **Trading Projects:** Trade journal entries (one file per day, immutable)

**Benefits:**
- Data integrity (can't accidentally corrupt history)
- Easy disaster recovery (just restore the files)
- Audit trail (every entry is preserved)

**Code Pattern:**
```python
import tempfile
import shutil
from pathlib import Path

def save_safely(target: Path, data: str) -> None:
    """Atomic write - won't corrupt if interrupted."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=target.suffix, dir=target.parent)
    try:
        with open(temp_fd, 'w') as f:
            f.write(data)
        shutil.move(temp_path, target)
    except Exception:
        Path(temp_path).unlink(missing_ok=True)
        raise
```

**Extraction Ready:** Yes - create code snippet library

---

#### 🟡 EMERGING: Read-Only Source Data Pattern

**What:** Source data is NEVER modified, only read and transformed elsewhere

**Examples:**
- **image-workflow:** PNG/YAML files moved, never modified
- **Cortana:** SuperWhisper database read-only access
- **Trading Projects:** Raw market data CSV files preserved

**Benefits:**
- Can always re-run from original data
- No accidental corruption
- Easy to add new transformations

**Extraction Ready:** Yes - document as principle

---

### 3. Code Quality Patterns

#### 🟢 PROVEN: Python 3.11+ Modern Typing

**What:** Use built-in generic types, not `typing` module classes

**Standard:**
```python
# ✅ CORRECT
from typing import Any
data: dict[str, Any] = {}
items: list[int] = []
value: str | None = None

# ❌ WRONG
from typing import Dict, List, Optional
data: Dict[str, Any] = {}
items: List[int] = []
value: Optional[str] = None
```

**Evidence:**
- **image-workflow:** Enforced in CODE_QUALITY_RULES.md + Ruff config
- **Cortana:** Documented in CLAUDE.md, used throughout
- **Trading Projects:** Python 3.14 venv (should enforce this)

**Benefits:**
- Cleaner code (less imports)
- Faster type checking
- Python 3.9+ standard (future-proof)

**Extraction Ready:** Yes - add to template .cursorrules

---

#### 🟡 EMERGING: Linter Configuration Pattern

**What:** Ruff + mypy configured at project root

**Evidence:**
- **image-workflow:** `pyproject.toml` with Ruff config, validation commands in CLAUDE.md
- **Cortana:** mypy commands in CLAUDE.md, no pyproject.toml yet
- **Trading Projects:** Has requirements.txt, no linter config

**Standard Commands:**
```bash
# Ruff linting
ruff check scripts/

# Type checking
mypy scripts --ignore-missing-imports --allow-untyped-defs
```

**Extraction Ready:** Almost - need consistent pyproject.toml pattern

---

### 4. Development Philosophy Patterns

#### 🟢 PROVEN: Layer-by-Layer Development

**What:** Build incrementally useful layers, not "all or nothing"

**Evidence:**
- **Cortana:** Explicit 7-layer roadmap, Layer 1 complete and USEFUL
- **Trading Projects:** Layer 1-3 complete, each layer functional
- **image-workflow:** Evolved over 2.5 months, tools added incrementally

**Benefits:**
- Each layer delivers value (not waiting for "done")
- Can stop at any layer (not over-built)
- Easy to test (one layer at a time)
- Clear progress milestones

**Pattern:**
```
Layer 1: Foundation (data collection)
  ↓ Is this useful alone? Yes → Ship it
Layer 2: Query & Analysis
  ↓ Is this useful alone? Yes → Ship it
Layer 3: Automation & Intelligence
  ... etc
```

**Extraction Ready:** Yes - document as principle

---

#### 🟢 PROVEN: "Data Before Decisions" (30-60 Days)

**What:** Collect data for 30-60 days BEFORE evaluating success

**Evidence:**
- **Trading Projects:** "Let it run 30 days before judging"
- **image-workflow:** 2.5 months of real use before major decisions
- **Cortana:** 3 months of data backfilled before building features

**Benefits:**
- Avoid premature optimization
- Real patterns emerge (not gut feelings)
- Can kill features with confidence (or double down)

**Extraction Ready:** Yes - document as principle

---

#### 🟡 EMERGING: "Consolidate on 3rd Duplicate"

**What:** First instance = custom, second = notice, third = extract pattern

**Evidence:**
- **PROJECT_PHILOSOPHY.md:** Explicitly stated
- **image-workflow:** Waited until 3rd similar tool before abstracting
- **This meta-project:** Waiting for 3rd instance of patterns

**Benefits:**
- Don't abstract too early (premature patterns fail)
- Let patterns prove themselves
- Consolidation is informed by real usage

**Extraction Ready:** Yes - document as principle

---

### 5. Deployment & Automation Patterns

#### 🟡 EMERGING: Daily Automation Pattern

**What:** Scheduled daily processing for data collection projects

**Evidence:**
- **Cortana:** launchd daily at 10pm (macOS native)
- **Trading Projects:** Railway cron daily (cloud deployment)
- **image-workflow:** Manual workflow (but has session tracking)

**Two Approaches:**

**A. Local Automation (launchd on macOS):**
```xml
<!-- config/com.user.project.plist -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>22</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

**B. Cloud Automation (Railway cron):**
```toml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
healthcheckPath = "/health"
startCommand = "python scripts/run_daily.py"

[[deploy.cron]]
schedule = "0 0 * * *"
command = "python scripts/daily_job.py"
```

**Extraction Ready:** Yes - document both patterns

---

#### 🔵 CANDIDATE: Cron Dispatcher Pattern

**What:** Single cron entry dispatches to multiple jobs

**Evidence:**
- **Trading Projects:** One schedule, multiple model evaluations
- Not yet seen in other projects

**Benefits:**
- Easier schedule management (one place)
- Shared logging/error handling
- Can skip jobs conditionally

**Extraction Ready:** Not yet - watch for 2nd instance

---

### 6. Data Structure Patterns

#### 🟡 EMERGING: Dual-Format Storage (JSON + Markdown)

**What:** Store data in both machine-readable (JSON) and human-readable (Markdown) formats

**Evidence:**
- **Cortana:** Every memory is `.json` + `.md` (same date)
- **image-workflow:** Session logs in structured + markdown format
- **Trading Projects:** Trade journal has CSV + Markdown

**Benefits:**
- Machines can process efficiently (JSON)
- Humans can read easily (Markdown)
- No conversion needed (both written at same time)
- Redundancy (if one corrupts, other remains)

**Pattern:**
```python
from pathlib import Path
import json

def save_dual_format(base_path: Path, data: dict, summary: str) -> None:
    """Save data in both JSON and Markdown formats."""
    # Machine-readable
    json_path = base_path.with_suffix('.json')
    json_path.write_text(json.dumps(data, indent=2))
    
    # Human-readable
    md_path = base_path.with_suffix('.md')
    md_path.write_text(summary)
```

**Extraction Ready:** Yes - create code snippet

---

#### 🟡 EMERGING: Date-Based File Organization

**What:** One file per day, named YYYY-MM-DD.*

**Evidence:**
- **Cortana:** `data/memories/daily/2025-12-15.json`
- **Trading Projects:** `04_journal/daily/2025-09-30_journal.md`
- **image-workflow:** `data/daily_summaries/` (similar pattern)

**Benefits:**
- Easy to find specific days
- Chronological sorting (ls works!)
- Clear retention policies (delete old files)
- No database needed for simple queries

**Extraction Ready:** Yes - document as pattern

---

### 7. Cost & Resource Patterns

#### 🟡 EMERGING: Cost-Conscious AI Usage

**What:** Track token usage, optimize for cost, use smaller models

**Evidence:**
- **Cortana:** gpt-4o-mini by default, ~$0.02/day, cost tracking in code
- **Trading Projects:** Multiple model comparison (includes cost factors)
- **image-workflow:** AI training uses batch processing (not real-time)

**Pattern:**
```python
def call_with_cost_tracking(prompt: str) -> tuple[str, float]:
    """Call API and return (response, cost_usd)."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    
    usage = response.usage
    cost = (usage.prompt_tokens * 0.00015 + 
            usage.completion_tokens * 0.0006) / 1000
    
    return response.choices[0].message.content, cost
```

**Extraction Ready:** Yes - create utility function

---

#### 🔵 CANDIDATE: Privacy-First Architecture

**What:** Raw sensitive data stays local, only processed/anonymized data sent to APIs

**Evidence:**
- **Cortana:** Voice recordings local, only transcripts to OpenAI
- Not yet seen in other projects (not applicable)

**Benefits:**
- User data privacy maintained
- Compliance-friendly
- Offline capabilities

**Extraction Ready:** Not yet - watch for 2nd instance

---

## Cross-Cutting Observations

### Testing Philosophy

**Observed pattern across projects:**
- ✅ Test fragile parts: parsers, data integrity, grading logic
- ❌ Don't test one-off scripts or UI tools
- ✅ Manual testing for Layer 1 (establish patterns first)
- ✅ Automated tests for Layer 2+ (when patterns are clear)

**Evidence:**
- **image-workflow:** Tests for utils, not for workflow scripts
- **Cortana:** Manual testing Layer 1, planning automated for Layer 2
- **Trading Projects:** Tests for grading systems (critical logic)

**Extraction Ready:** Yes - document testing philosophy

---

### Git & Version Control

**Observed patterns:**
- ✅ `.gitignore`: API keys, logs, `__pycache__`, venv
- ✅ Commit message format (some projects have standards)
- ✅ Branch protection (not yet seen, but mentioned in docs)

**Not yet consistent:**
- Commit message format varies
- Tag/release strategies unclear
- Contribution guidelines vary

**Extraction Ready:** Partial - document what's consistent

---

### AI Collaboration

**Observed patterns:**
- ✅ CLAUDE.md or similar instructions file
- ✅ Safety rules prominently documented
- ✅ Common code patterns provided as examples
- ✅ Validation commands listed

**Emerging:**
- Cross-tool collaboration (Cursor + browser Claude)
- Commit communication standards
- Context preservation across sessions

**Extraction Ready:** Yes - CLAUDE.md template

---

## Next Steps

### Immediate Extractions (Ready Now)

1. **Documentation Structure Template**
   - Create `templates/Documents/` structure
   - Include retention policies
   - Add README template

2. **CLAUDE.md Template**
   - Standard sections
   - Common Python patterns
   - Safety rules section

3. **Safety System Patterns Document**
   - "Every safety system was a scar" philosophy
   - Append-only archives pattern
   - Read-only source data pattern
   - Atomic writes code snippet

4. **Development Philosophy Document**
   - Layer-by-layer development
   - Data before decisions (30-60 days)
   - Consolidate on 3rd duplicate
   - Testing philosophy

### Watch For (Need More Evidence)

1. **Cron Dispatcher Pattern** - Seen in 1 project, wait for 2nd
2. **Privacy-First Architecture** - Seen in 1 project (domain-specific?)
3. **Linter Config Pattern** - Seen in 2 projects, different approaches
4. **Multi-Model Comparison** - Seen in 1 project (Trading), interesting

### Revisit Later

- Deployment patterns (Railway vs local automation) - both valid, not converged yet
- Database patterns (SQLite vs Postgres vs none) - varies by project needs
- API architecture patterns - only Trading Projects has this

---

## Pattern Extraction Priority

**Priority 1 (Extract This Week):**
- 🟢 Documents/ structure template
- 🟢 CLAUDE.md template
- 🟢 Safety systems documentation
- 🟢 Development philosophy doc

**Priority 2 (Extract When Proven):**
- 🟡 Dual-format storage pattern (2/3 projects)
- 🟡 Daily automation patterns (2/3 projects)
- 🟡 Modern Python typing (2/3 projects enforced)

**Priority 3 (Watch For 3rd Instance):**
- 🔵 Cron dispatcher (1/3)
- 🔵 Privacy-first architecture (1/3)
- 🔵 Multi-model comparison (1/3)

---

*This document grows as patterns emerge. Don't force extraction too early.*

**Last updated:** December 21, 2025  
**Projects analyzed:** image-workflow, Trading Projects, Cortana Personal AI  
**Patterns identified:** 20+ candidates, 5 proven, 11 emerging, 4 candidates

---

## Related Files

- **PROJECT_PHILOSOPHY.md** - Core philosophy that drives these patterns
- **USAGE_GUIDE.md** - How to apply patterns in new projects
- **patterns/** - Detailed pattern documentation

