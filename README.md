<!-- SCAFFOLD:START - Do not edit between markers -->
# project-scaffolding

Templates, governance rules, and sync tooling for bootstrapping and maintaining projects in this ecosystem. One edit here propagates to all downstream projects via AgentSync.

**Status:** Active | **Language:** Python | **Started:** December 2025

## Setup

```bash
pip install -r requirements.txt
```

## Key Commands

| Command | What it does |
|---------|-------------|
| `scaffold apply <project>` | Bootstrap a project with templates |
| `scaffold validate <project>` | Check structure, DNA integrity, secrets |
| `scaffold agent-health` | Lint agent configs for bloat/staleness |
| `uv run agentsync/sync.py <project>` | Sync rules + governance to a project |
| `uv run agentsync/sync_governance.py` | Sync governance protocol to all projects |

See `QUICKSTART.md` for the full new-project walkthrough.

## Structure

```
project-scaffolding/
├── scaffold/              # CLI source (apply, validate, agent-health)
│   └── cli.py
├── agentsync/             # Sync rules to IDE configs across projects
│   ├── sync.py            # Canonical project sync
│   ├── sync_governance.py # Governance sync
│   └── sync_mcp.py        # MCP config sync
├── templates/             # Source templates for scaffold apply
│   ├── .agentsync/rules/  # Agent rules templates
│   ├── AGENTS.md.template
│   └── CLAUDE.md.template
├── scripts/               # Validation + security audit scripts
│   ├── validate_project.py
│   └── warden_audit.py
└── config/                # Scan config, protected projects
```

## Common Mistakes

- **Copying everything** -- Use `scaffold apply`, not manual copy. Pick what fits.
- **Over-engineering early** -- Patterns are guidelines, not laws. Abstract on the 3rd instance.
- **Skipping docs** -- Even experiments need a README and CLAUDE.md.

## Essential Reading

| Document | Purpose |
|----------|---------|
| `QUICKSTART.md` | Step-by-step new project checklist |
| `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` | Code review and governance standard |
| `.agent/rules/CODE_QUALITY_STANDARDS.md` | Coding rules |
| `agentsync/README.md` | Sync usage, flags, and examples |

---

*This is the canonical source of truth for shared tooling. Changes here trickle down to all projects via AgentSync.*
