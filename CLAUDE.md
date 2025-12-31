# CLAUDE.md - AI Collaboration Instructions

**Project:** Project Scaffolding (The Meta-Project)
**Purpose:** Extracting patterns from experiments to build better projects faster.
**Philosophy:** Data before decisions, two-level game (domain + meta), scaffolding is the product.

---

## 📚 Required Reading
1. **README.md** - Project overview
2. **PROJECT_PHILOSOPHY.md** - The core "why" behind this project
3. **patterns/development-philosophy.md** - How we build things
4. **patterns/code-review-standard.md** - Standardized review rules

---

## Project Summary
This is the **heart and brain** of the ecosystem. It provides the reusable starting points and automation for all other projects. It is a living collection of patterns, safety systems, and structures that make maintenance easier.

**Current status:**
- Core review orchestrator (DeepSeek + Kiro) is operational.
- Code review standardization (DoD enforcement + naming) is implemented.
- Archive system is established.
- 19/19 tests passing.

---

## Coding Standards
### Language: Python 3.11+
- Use `pathlib.Path` for all file operations.
- All functions must have type hints.
- Use built-in generics for type hints (`dict[str, Any]`, not `Dict`).
- Modern datetime handling: Use `datetime.now(UTC)` (from `datetime import UTC`).

### Code Organization
- **Library code** (`scaffold/`): No print statements, use `logging`, raise exceptions with context.
- **CLI tools** (`scaffold/cli.py`, `scaffold_cli.py`): Print statements OK, use `rich` for formatting.

### Code Review Standard
- **Input:** Must contain a `Definition of Done` or `DoD` section.
- **Output:** Must be named `CODE_REVIEW_{REVIEWER_NAME_UPPER}.md`.

---

## Safety Rules
### 🔴 NEVER Modify These:
1. **`.env`** - Contains sensitive API keys.
2. **`venv/`** - Local environment dependencies.

### 🟡 Be Careful With These:
1. **`EXTERNAL_RESOURCES.md`** - Update immediately when adding services.
2. **API Callers** (`scaffold/review.py`) - Must have retry logic and cost tracking.

### ✅ Safe to Modify:
1. **`scaffold/`** - Core logic.
2. **`tests/`** - All integration and smoke tests.
3. **`patterns/`** - Documented patterns (once proven).
4. **`templates/`** - Reusable starting points.

---

## Validation Commands
Run these before committing:
```bash
# Run full test suite (takes ~9 mins due to real API calls)
./venv/bin/python -m pytest tests/test_review.py tests/test_kiro.py

# Run fast tests only
./venv/bin/python -m pytest -m "not slow"
```

---

## Git Workflow
- **Commit Format:** `[Component] Brief description` (e.g., `[Review] Standardize result naming`).
- **Standard:** Push all major updates immediately. This project sets the standard for everything else.

---

*Remember: This project has some of the highest standards because it passes its standards on to everything that touches it.*

