# Project Scaffolding

Health checks, multi-AI review, and safety tooling for the project ecosystem.

> **Want to set up a new project or get briefed on an existing one?** Use `/intake`.
> Project scaffolding no longer pushes files into projects. See `PRD.md` for what changed and why.

## Commands

| Command | What it does |
|---------|-------------|
| `scaffold agent-health` | Lint agent configs (CLAUDE.md, .agent/rules/) for bloat and staleness |
| `scaffold agent-health -p <project>` | Check a single project |
| `scaffold review --type code --input <path>` | Run multi-AI code review |
| `scaffold review --type document --input <path>` | Run multi-AI document review |

## Safety Scripts

| Script | What it does |
|--------|-------------|
| `scripts/warden_audit.py --root . --fast` | Security audit (hardcoded paths, dangerous functions, secrets) |
| `scripts/validate_project.py <project>` | Structure validation (mandatory files, DNA integrity) |

## Templates

Reference templates for bootstrapping new projects live in `templates/`:

- `git-hooks/` — pre-commit, pre-push, post-merge hooks with safety checks
- `claude-code/` — Claude Code agent/command templates, settings.json
- `claude-review.yml` — GitHub Actions workflow for automated PR review
- `github-workflows/` — PR label checks and other CI templates
- `test-coverage/` — Coverage config and runner script
- `spec-template.md.template` — Kiro spec template

## Structure

```
project-scaffolding/
├── scaffold/           # CLI (review, agent-health)
├── scripts/            # Standalone validation + security tools
├── templates/          # Reference templates for new projects
├── agentsync/          # sync_mcp.py only (infra config sync)
└── config/             # scan_config.yaml (protected projects)
```

## What This Is Not

This project used to push governance files, agent configs, and templates into every project via "agentsync." That system was retired in March 2026. If you're looking for:

- **Project briefings** — Use `/intake` (pulls from Open Brain, project tracker, git)
- **Governance rules** — Read `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` (canonical source)
- **Agent config setup** — Copy from `templates/claude-code/` manually

---

*See `QUICKSTART.md` for usage details. See `PRD.md` for the full v2 scope.*
