# Project Scaffolding - Quick Start

Health checks and multi-AI review for your project ecosystem.

---

## UV Run-First Policy

New Python commands use `uv run` for reproducible execution. Existing venv/Poetry workflows stay until explicitly migrated.

---

## Key Commands

| Command | What it does |
|---------|-------------|
| `scaffold agent-health` | Lint agent config files for bloat/staleness |
| `scaffold agent-health --project X` | Check a single project |
| `scaffold review --type code --input src/` | Run multi-AI code review |

---

## Quick Validation

```bash
# Agent config health
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" agent-health
```

Safety enforcement runs through the installed git hooks and the
`safety-check.yml` workflow — no standalone audit script to invoke.

---

## Troubleshooting

**PROJECTS_ROOT not set** -- Add `export PROJECTS_ROOT="$HOME/projects"` to `~/.zshrc`.

**Validation failing** -- Usually: hardcoded absolute paths or missing mandatory files. Fix and re-run.

---

*See `README.md` for project overview. See `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for the review standard.*
