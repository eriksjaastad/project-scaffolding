# AgentSync

Synchronizes AI instruction rules from a single source to multiple IDE-specific config files.

---

## Why This Exists

**The Problem (January 2026):**

We were using two AI coding assistants simultaneously: Claude Code and Antigravity (Gemini). Each reads a different config file:

| IDE | Config File |
|-----|-------------|
| Claude Code | `CLAUDE.md` |
| Antigravity | `.agent/rules/instructions.md` |

When we discovered a great pattern (like the IndyDevDan video on self-validating agents with hooks), we'd implement it in Claude's rules... and then the other agents had no idea. We were building siloed knowledge.

**The Insight:**

Great ideas shouldn't be siloed into one IDE. All our agents should get the same benefit from every improvement we make.

The Solution:

Single source of truth → auto-generate all agent configs.

Edit once in `.agentsync/rules/`, run sync, all tools get the same instructions. No more copy-paste drift.

**Why It Lives in project-scaffolding:**

AgentSync is infrastructure for setting up projects correctly. It's part of the "make projects work well from day one" toolset, alongside templates, scripts, and documentation patterns. Keeping it here makes the relationship obvious: AGENTS.md templates → AgentSync → Agent configs.

---

## How It Works

```
.agentsync/rules/                     Target Files
├── 00-overview.md          ─────►    CLAUDE.md (Claude Code)
├── 01-workflow.md          ─────►    .agent/rules/instructions.md (Antigravity)
├── 02-constraints.md       ─────►    .agent/rules/instructions.md (Antigravity)
└── 03-safety.md
```

**Single source of truth.** Edit rules in `.agentsync/rules/`, run sync, all agents get updated.

## Target Tools

| Tool | Output File | How It Reads |
|-----|-------------|--------------|
| Claude Code | `CLAUDE.md` | Automatically reads project root |
| Antigravity (Gemini) | `.agent/rules/instructions.md` | Uses `trigger: always_on` frontmatter |

### Antigravity Note

Antigravity reads rules from `.agent/rules/instructions.md` when the file includes YAML frontmatter with `trigger: always_on`. AgentSync adds this automatically:

```yaml
---
trigger: always_on
---
```

This is NOT the same as AGENTS.md - Antigravity reads from `.agent/`, not the project root.

## Usage

```bash
# Sync a single project
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync.py project-name

# Sync all eligible projects
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync.py --all

# Sync only rules for one project
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync.py project-name --components rules

# List eligible projects for the selected components
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync.py --list
```

## Files

| Script | Purpose |
|--------|---------|
| `sync.py` | Canonical project sync for rules, AGENTS.md, and governance |
| `sync_rules.py` | Rules-only sync: `.agentsync/rules/` → IDE configs |
| `sync_agents_md.py` | AGENTS.md template sync |
| `sync_governance.py` | Governance file sync |
| `migrate_agents_md.py` | One-time migration: AGENTS.md → `.agentsync/rules/` structure |
| `sync_mcp.py` | Syncs MCP server configurations |

## MCP Config Locations

`sync_mcp.py` keeps MCP configs in sync across IDEs. Current locations:

| Location | IDE | Notes |
|----------|-----|-------|
| `~/.claude/claude_desktop_config.json` | Claude Desktop | |
| `~/.antigravity/mcp_config.json` | Antigravity (standalone) | |
| `~/.gemini/antigravity/mcp_config.json` | Antigravity (via Gemini) | May have different server names |

**Source of truth:** `$PROJECT_ROOT/_configs/mcp/`

## Integration with Scaffold

AgentSync lives inside project-scaffolding. The `scaffold apply` command:

1. Copies `.agentsync/rules/` templates with placeholder substitution
2. Runs `sync.py --components rules` to generate CLAUDE.md and .agent/rules/instructions.md
3. Appends project-specific content outside AGENTSYNC markers

## AGENTSYNC Markers

Generated files use markers to separate synced content from custom additions:

```markdown
<!-- AGENTSYNC:START -->
[synced content here - do not edit]
<!-- AGENTSYNC:END -->

[custom project-specific content below - preserved on re-sync]
```

---

## Comprehensive Sync Script Documentation

### sync.py - Unified Project Sync

Canonical project-scoped AgentSync entrypoint.

**Usage:**
```bash
# Sync the default project-scoped components for one project
uv run project-scaffolding/agentsync/sync.py project-name

# Sync all eligible projects
uv run project-scaffolding/agentsync/sync.py --all

# Sync a subset of components
uv run project-scaffolding/agentsync/sync.py project-name --components rules,agents

# Preview without writing
uv run project-scaffolding/agentsync/sync.py project-name --dry-run
```

By default `sync.py` includes `rules`, `agents`, and `governance`.
`sync_mcp.py` remains separate because it manages workstation-level config.

### sync_agents_md.py - AGENTS.md Template Sync

Syncs `templates/AGENTS.md.template` to all projects' `AGENTS.md` files, preserving project-specific customizations.

**Usage:**
```bash
# Sync all scaffolded projects
uv run project-scaffolding/agentsync/sync_agents_md.py

# Sync a single project
uv run project-scaffolding/agentsync/sync_agents_md.py smart-invoice-workflow

# Preview changes without applying
uv run project-scaffolding/agentsync/sync_agents_md.py --dry-run

# Sync and git add changed files
uv run project-scaffolding/agentsync/sync_agents_md.py --stage

# List projects that have AGENTS.md
uv run project-scaffolding/agentsync/sync_agents_md.py --list
```

### sync_rules.py - IDE Configuration Sync

Syncs `.agentsync/rules/` templates to IDE-specific rule files (CLAUDE.md, .agent/rules/instructions.md).
This remains available as a specialized/backwards-compatible command.

**Usage:**
```bash
# Sync a single project
uv run project-scaffolding/agentsync/sync_rules.py project-name

# Sync all projects with .agentsync/
uv run project-scaffolding/agentsync/sync_rules.py --all

# Preview changes without applying
uv run project-scaffolding/agentsync/sync_rules.py project-name --dry-run

# Sync and git add changed files
uv run project-scaffolding/agentsync/sync_rules.py project-name --stage

# List all projects with .agentsync/ directories
uv run project-scaffolding/agentsync/sync_rules.py --list
```

### sync_governance.py - Governance File Sync

Syncs governance and review protocol files to all scaffolded projects.

**Usage:**
```bash
# Sync all scaffolded projects
uv run project-scaffolding/agentsync/sync_governance.py

# Sync a single project
uv run project-scaffolding/agentsync/sync_governance.py smart-invoice-workflow

# Preview changes without applying
uv run project-scaffolding/agentsync/sync_governance.py --dry-run

# Sync and git add changed files
uv run project-scaffolding/agentsync/sync_governance.py --stage
```

### sync_mcp.py - MCP Configuration Sync

Syncs MCP (Model Context Protocol) server configurations to IDE-specific config files.

**Usage:**
```bash
# Sync all tools (Claude, Antigravity, Gemini)
uv run project-scaffolding/agentsync/sync_mcp.py

# Sync a specific tool only
uv run project-scaffolding/agentsync/sync_mcp.py claude
uv run project-scaffolding/agentsync/sync_mcp.py antigravity

# Preview changes without writing
uv run project-scaffolding/agentsync/sync_mcp.py --dry-run
```

### scaffold apply - Full Scaffolding Application

Applies complete scaffolding to a project: copies templates, runs all syncs, and generates IDE configs.

**Usage:**
```bash
# Apply scaffolding to a new or existing project
uv run project-scaffolding/scaffold_cli.py apply project-name

# Preview what will be copied and synced
uv run project-scaffolding/scaffold_cli.py apply project-name --dry-run

# Only verify references without making changes
uv run project-scaffolding/scaffold_cli.py apply project-name --verify-only
```

**What it does:**
1. Copies scripts (`warden_audit.py`, `validate_project.py`)
2. Copies documentation templates
3. Copies `.agentsync/rules/` templates
4. Runs `sync.py --components rules` to generate IDE configs
5. Updates AGENTS.md, README.md from templates

### Quick Reference: Common Workflows

**Update AGENTS.md template and sync everywhere:**
```bash
# 1. Edit the template
vim project-scaffolding/templates/AGENTS.md.template

# 2. Sync to all projects (with preview)
uv run project-scaffolding/agentsync/sync_agents_md.py --dry-run

# 3. Apply for real
uv run project-scaffolding/agentsync/sync_agents_md.py
```

**Update IDE rules and sync everywhere:**
```bash
# 1. Edit the rules in .agentsync/rules/
vim project-scaffolding/templates/.agentsync/rules/00-overview.md

# 2. Sync to all projects
uv run project-scaffolding/agentsync/sync.py --all --components rules
```

**Sync only what changed (with staging):**
```bash
# Sync and automatically git add changed files
uv run project-scaffolding/agentsync/sync.py --all --stage
```
