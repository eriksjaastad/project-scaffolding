# .agentsync Directory

This directory contains the source of truth for agent configurations.

## Structure

```
.agentsync/
└── rules/
    ├── 00-overview.md      # Project description, tech stack
    ├── 01-workflow.md      # Agent hierarchy and workflow
    ├── 02-constraints.md   # Universal constraints
    ├── 03-safety.md        # Safety rules
    └── *.md                # Additional project-specific rules
```

## How It Works

1. **Edit rules here** - These files are the source of truth
2. **Auto-sync on save** - Claude hook syncs when you save
3. **Auto-sync on commit** - Pre-commit hook ensures everything is synced

## Generated Files

The sync script generates:
- `CLAUDE.md` - For Claude Code
- `.cursorrules` - For Cursor IDE
- `.agent/rules/instructions.md` - For Antigravity IDE

**Do not edit the generated files directly.** Your changes will be overwritten.

## YAML Frontmatter

Each rule file can have optional frontmatter:

```yaml
---
targets: ["*"]           # All tools (default)
targets: ["claude"]      # Claude only
targets: ["cursor", "antigravity"]  # Multiple tools
root: true               # Mark as overview/root file
---
```

## Manual Sync

```bash
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py $(basename $(pwd))
```
