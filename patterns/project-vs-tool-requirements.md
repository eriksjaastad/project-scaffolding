# Project vs Tool Requirements

> **Purpose:** Define different levels of requirements for full projects vs utility tools
> **Created:** January 2026
> **Core Principle:** Everything needs quality, but not everything needs bureaucracy

---

## The Distinction

| Type | Location | Purpose |
|------|----------|---------|
| **Project** | `/projects/[name]/` | A product, system, or substantial body of work |
| **Tool** | `/projects/_tools/[name]/` | A utility, script, or helper that supports projects |

---

## Project Requirements (Full Kitchen Sink)

Projects are first-class citizens. They get the full treatment.

### Required Files

| File | Purpose |
|------|---------|
| `README.md` | Overview, quick start, what it does |
| `AGENTS.md` | AI collaboration source of truth |
| `CLAUDE.md` | Claude-specific instructions |
| `TODO.md` | Task tracking and status |
| `00_Index_[name].md` | Obsidian index, project tracker integration |
| `.cursorrules` | Cursor IDE configuration |
| `.cursorignore` | Context optimization |

### Required Structure

```
project-name/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── TODO.md
├── 00_Index_project-name.md
├── .cursorrules
├── .cursorignore
├── scripts/           # Or src/ - main code
├── tests/             # Test suite
│   └── test_*.py
├── .coveragerc        # Coverage configuration
└── Documents/         # Extended documentation
    ├── core/          # Architecture decisions
    └── archives/      # Historical records
```

### Required Quality Gates

- [ ] Tests exist and pass
- [ ] Coverage report available (`.coveragerc` configured)
- [ ] Pre-commit hooks installed
- [ ] No hardcoded absolute paths
- [ ] No exposed secrets
- [ ] Index file current

---

## Tool Requirements (Lighter Touch)

Tools are supporting infrastructure. They need quality, not ceremony.

### Required Files

| File | Purpose |
|------|---------|
| `README.md` | What it does, how to use it, examples |
| Tests | At least basic functionality tests |

### Optional (Nice to Have)

| File | When to Add |
|------|-------------|
| `CLAUDE.md` | If AI collaborates on this tool frequently |
| `.coveragerc` | If the tool has significant logic worth measuring |
| `TODO.md` | If there's ongoing development |

### Required Structure

```
tool-name/
├── README.md          # Required: usage docs
├── tool_name.py       # Main script (or multiple files)
├── tests/             # Required: basic tests
│   └── test_tool.py
└── .coveragerc        # Optional: coverage config
```

### Required Quality Gates

- [ ] README explains what it does and how to use it
- [ ] At least one test file exists
- [ ] No hardcoded absolute paths
- [ ] No exposed secrets

---

## Test Requirements by Type

### Projects: Comprehensive Testing

```
tests/
├── test_core.py           # Core functionality
├── test_edge_cases.py     # Edge cases and error handling
├── test_integration.py    # Integration with other components
└── conftest.py            # Shared fixtures
```

**Coverage target:** 70%+ for critical paths

### Tools: Smoke Testing

```
tests/
└── test_tool.py           # Basic functionality works
```

**Coverage target:** Main happy path covered

---

## Coverage Configuration

### For Projects

Copy from `templates/test-coverage/`:
- `coveragerc.template` → `.coveragerc`
- `run_coverage.py` → `scripts/tests/run_coverage.py`

Customize the `[run] source` directive for your project structure.

### For Tools

Minimal `.coveragerc`:

```ini
[run]
source = .
omit =
    tests/*
    */__pycache__/*

[report]
exclude_lines =
    if __name__ == .__main__.:
```

---

## Migration Checklist

### Promoting a Tool to a Project

When a tool grows substantial enough to be a project:

- [ ] Move from `_tools/` to `/projects/`
- [ ] Add `AGENTS.md`
- [ ] Add `CLAUDE.md`
- [ ] Add `TODO.md`
- [ ] Add `00_Index_[name].md`
- [ ] Add `.cursorrules` and `.cursorignore`
- [ ] Expand test coverage
- [ ] Create `Documents/` structure

### Demoting a Project to a Tool

When a project is really just a utility:

- [ ] Move to `_tools/`
- [ ] Keep `README.md` and tests
- [ ] Archive or remove ceremonial files
- [ ] Simplify structure

---

## Examples

### Tool: `integrity-warden`

```
_tools/integrity-warden/
├── README.md              # Usage, examples, checker list
├── integrity_warden.py    # Main script
├── tests/                 # Basic tests
│   └── test_checkers.py
└── cleanup-prompts.md     # Generated artifacts
```

### Project: `project-tracker`

```
project-tracker/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── TODO.md
├── 00_Index_project-tracker.md
├── .cursorrules
├── .cursorignore
├── .coveragerc
├── scripts/
│   └── ...
├── tests/
│   ├── test_discovery.py
│   ├── test_scanner.py
│   └── conftest.py
├── dashboard/
│   └── ...
└── Documents/
    ├── core/
    └── archives/
```

---

## The Philosophy

**Projects** are investments. They have roadmaps, they evolve, they need governance. The overhead pays off over time.

**Tools** are utilities. They do one thing well. Overhead should be proportional to complexity. A 200-line script doesn't need a Documents/ directory.

**The line isn't always clear.** When in doubt:
- If it has users beyond you → Project
- If it has a roadmap → Project
- If it's "fire and forget" → Tool
- If you keep adding features → Maybe promote to Project

---

*Pattern from project-scaffolding, January 2026*

## Related Documentation

- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure
- [[architecture_patterns]] - architecture
- [[dashboard_architecture]] - dashboard/UI
- [[error_handling_patterns]] - error handling
- [[prompt_engineering_guide]] - prompt engineering
- [[ai_model_comparison]] - AI models
- [[case_studies]] - examples
- [[performance_optimization]] - performance
- [[project_planning]] - planning/roadmap
- [[testing_strategy]] - testing/QA
- [[project-scaffolding/README]] - Project Scaffolding
- [[project-tracker/README]] - Project Tracker
