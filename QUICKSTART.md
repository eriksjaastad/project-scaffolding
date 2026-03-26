# Project Scaffolding - Quick Start

Scaffold a new project in under 5 minutes.

---

## UV Run-First Policy

New Python commands use `uv run` for reproducible execution. Existing venv/Poetry workflows stay until explicitly migrated.

---

## New Project Checklist

```bash
# 1. Create project and bootstrap
mkdir -p "$PROJECTS_ROOT/my-new-project" && cd "$PROJECTS_ROOT/my-new-project"
git init
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" apply "my-new-project"

# 2. Install governance hooks
"$PROJECTS_ROOT/_tools/governance/install-hooks.sh" .

# 3. Customize templates
#    - 00_Index_*.md  → 3-sentence summary + YAML tags (MANDATORY)
#    - AGENTS.md      → tech stack, run/test commands, constraints
#    - README.md      → project description + quick start

# 4. Sync agent configs
uv run "$PROJECTS_ROOT/project-scaffolding/agentsync/sync.py" "my-new-project"

# 5. First commit
git add -A
git commit -m "Initial commit: project scaffolded from project-scaffolding"
```

---

## Key Commands

| Command | What it does |
|---------|-------------|
| `scaffold apply <project>` | Apply templates to a project |
| `scaffold validate <project>` | Check required files, DNA integrity, secrets |
| `scaffold agent-health` | Lint agent config files for bloat/staleness |
| `uv run agentsync/sync.py <project>` | Sync rules + governance to a project |

---

## Quick Validation

```bash
# Validate project structure
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" validate "$(basename $(pwd))"

# Security audit
uv run "$PROJECTS_ROOT/project-scaffolding/scripts/warden_audit.py" --root . --fast
```

---

## Troubleshooting

**PROJECTS_ROOT not set** -- Add `export PROJECTS_ROOT="$HOME/projects"` to `~/.zshrc`.

**Validation failing** -- Usually: missing `00_Index_*.md`, missing YAML frontmatter, or hardcoded absolute paths. Fix and re-run.

**Which files are required?** -- At minimum: `00_Index_*.md`, `AGENTS.md`, `.cursorrules`. Code projects also need `.agent/rules/` and a dependency manifest.

---

*See `README.md` for project overview. See `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for the review standard.*
