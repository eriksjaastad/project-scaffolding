# PRD: Project Scaffolding System (v2)

## 1. Problem Statement

The Erik Sjaastad project ecosystem consists of 30+ projects. They need:
- **Health visibility**: Which projects have bloated CLAUDE.md files, stale configs, or missing essentials?
- **Review quality**: Code and document reviews need multiple AI perspectives, not a single model's blind spots.
- **Safe bootstrapping**: New projects need a consistent starting structure without manual copy-paste.

### What v1 got wrong

v1 tried to *push* governance files into every project via agentsync. This created:
- Noise in other projects (synced markers, version files, stale governance copies)
- Maintenance burden (sync scripts, template versioning, marker-based updates)
- False consistency (files existed but agents didn't read them)

v2 is **pull-based**: tools run on demand, nothing gets pushed into other projects.

## 2. Scope

### In scope (v2)

| Capability | Command | Status |
|-----------|---------|--------|
| Agent config health checks | `scaffold agent-health` | Shipped |
| Multi-AI code/document review | `scaffold review` | Shipped |
| Git hook templates (inline safety checks) | `templates/git-hooks/` | Shipped |
| REVIEW.md system | `scaffold review-rules` | Planned (#5110) |
| Git history mining for review rules | `scaffold mine-rules` | Planned (#5111) |

### Out of scope (retired)

- `scaffold apply` — push-based template application
- `scaffold sync-root` — root-level file syncing
- `scaffold gen-manifest` — 00_Index/README auto-generation
- `agentsync/` sync scripts (except sync_mcp.py for infra)
- `.scaffolding-version` tracking
- 00_Index file system
- Template marker system (SCAFFOLD:START/END, AGENTSYNC:START/END)

## 3. Architecture

```
project-scaffolding/
├── scaffold/              # Python package
│   ├── cli.py             # Click CLI: review, agent-health
│   ├── agent_health.py    # Health check engine
│   ├── review.py          # Multi-AI review orchestrator
│   ├── alerts.py          # Discord alerting
│   └── constants.py       # Protected projects config
├── scripts/               # Misc tooling (pre_review_scan.sh, etc.)
├── templates/
│   └── git-hooks/         # Hook templates for new projects
├── agentsync/
│   └── sync_mcp.py        # MCP server config sync (infra only)
└── config/
    └── scan_config.yaml   # Protected projects list
```

## 4. Success Metrics

- **Health coverage**: `scaffold agent-health` runs across all projects with zero false positives
- **Review adoption**: Multi-AI review used for PRDs and critical code changes
- **Zero push footprint**: No files written to other projects by scaffolding automation
- **Warden clean**: Zero P0 findings in warden audit across active projects

## 5. Future Work

- **REVIEW.md**: Portable review rules per project, read by Judge at review time (#5110)
- **Rule mining**: Auto-generate review rules from git history patterns (#5111)
- **`scaffold new`**: One-command project bootstrapping (templates + git init + hooks)
