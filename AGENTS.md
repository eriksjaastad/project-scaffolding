# AGENTS.md - Source of Truth for Project Scaffolding

## 🎯 Project Overview
The "heart and brain" of the ecosystem. Extracts patterns from experiments to build better projects faster.

## 🛠 Tech Stack
- Language: Python 3.11+
- Frameworks: pytest, PyYAML, rich
- AI Strategy: **Gemini 3 Flash** (Primary) + DeepSeek + Kiro for reviews

## 📋 Definition of Done (DoD)
- [ ] Code has type hints and follows coding standards.
- [ ] Technical changes are logged to `_obsidian/WARDEN_LOG.yaml`.
- [ ] `00_Index_project-scaffolding.md` is updated.
- [ ] All 19 tests pass (`pytest`).

## 🚀 Execution Commands
- Environment: `source venv/bin/activate`
- Run Full Tests: `pytest tests/test_review.py tests/test_kiro.py`
- Run Fast Tests: `pytest -m "not slow"`

## 📋 Coding Standards
- **File Ops:** Use `pathlib.Path`.
- **Typing:** Use built-in generics (`dict[str, Any]`).
- **Data:** Use YAML for structured data (SSOT pattern).
- **Library Code:** No prints, use `logging`.

## ⚠️ Critical Constraints
- NEVER modify `.env` or `venv/`.
- ALWAYS update `EXTERNAL_RESOURCES.yaml` when adding services.
- ALWAYS use retry logic and cost tracking for API callers.

## 📖 Reference Links
- [[00_Index_project-scaffolding]]
- [[Project Philosophy]]
- [[patterns/development-philosophy]]

