# Agent Config Synchronization System

> **Single Source of Truth:** `.agentsync/rules/*.md` files are the only files you edit. All IDE configs are auto-generated.

---

## The Problem

Modern AI-assisted development involves multiple IDEs, each with its own config format:

| IDE | Config File | Location |
|-----|-------------|----------|
| Claude Code | `CLAUDE.md` | Project root |
| Cursor | `.cursorrules` | Project root |
| Antigravity | `.agent/rules/instructions.md` | `.agent//` |

Keeping these in sync manually is error-prone and tedious. Edit one, forget the others, and your agents have inconsistent instructions.

---

## The Solution

**`.agentsync/rules/` is the single source of truth.**

```
.agentsync/rules/*.md (you edit these)
    |
    v  [auto-sync]
    +---> CLAUDE.md             (Claude Code)
    +---> .cursorrules          (Cursor)
    +---> .agent/rules/instructions.md (Antigravity)
```

You only ever edit files in `.agentsync/rules/`. The sync system automatically generates the IDE-specific files with appropriate headers.

---

## Directory Structure

```
project-root/
└── .agentsync/                    # Single source of truth
    ├── README.md                  # Explains the structure
    └── rules/                     # Modular rule files
        ├── 00-overview.md         # Project overview, tech stack
        ├── 01-workflow.md         # Agent hierarchy, workflow
        ├── 02-constraints.md      # Universal constraints
        ├── 03-safety.md           # Safety rules
        └── *.md                   # Additional project-specific rules
```

Files are concatenated in filename order (00-, 01-, etc.) when generating IDE configs.

---

## How It Works

### The Sync Script

**Location:** `project-scaffolding/agentsync/sync_rules.py`

**What it does:**
1. Reads all `.md` files from `.agentsync/rules/` (sorted by filename)
2. Parses YAML frontmatter for tool-specific targeting
3. Applies IDE-specific headers
4. Writes to `CLAUDE.md`, `.cursorrules`, and `.agent/rules/instructions.md`
5. Only updates files if content changed (idempotent)

**Manual usage:**
```bash
# Sync a specific project
uv run project-scaffolding/agentsync/sync_rules.py my-project

# Sync all projects
uv run project-scaffolding/agentsync/sync_rules.py --all

# Sync and stage changes (for pre-commit hook)
uv run project-scaffolding/agentsync/sync_rules.py my-project --stage

# Dry run (preview changes)
uv run project-scaffolding/agentsync/sync_rules.py my-project --dry-run
```

### Auto-Sync Triggers

You don't need to run the sync manually. Two triggers handle it automatically:

#### 1. Claude Code Hook (Real-Time)

**When:** Immediately after Claude writes or edits `.agentsync/rules/*.md`

**How:** PostToolUse hook in `.claude/settings.json` runs `agent-sync-on-write.py`

**Location:** `projects/.claude/hooks/validators/agent-sync-on-write.py`

This means: Edit any rule file in Claude Code, and the derived files update instantly.

#### 2. Git Pre-Commit Hook (All Agents)

**When:** When you stage `.agentsync/rules/*.md` files for commit

**How:** `agent-sync-check.py` auto-syncs and stages the generated files

**Location:** `projects/.claude/hooks/validators/agent-sync-check.py`

This means: Even if you edit rules in Cursor or Antigravity, the commit will include the synced files.

---

## YAML Frontmatter for Tool Targeting

Each rule file can specify which tools receive it:

```markdown
---
targets: ["*"]           # All tools (default)
---

# Your rule content here
```

Or target specific tools only:

```markdown
---
targets: ["claude", "cursor"]  # Skip Antigravity
---

# Claude and Cursor specific rules
```

Available targets: `claude`, `cursor`, `antigravity`, `*` (all)

---

## Generated File Structure

### Header Templates

Each generated file includes a header identifying it as auto-generated:

**`CLAUDE.md`:**
```markdown
# CLAUDE.md - my-project

<!-- AUTO-GENERATED from .agentsync/rules/ - Do not edit directly -->
<!-- Run: uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py my-project -->

[concatenated rules content]

<!-- Source of truth: .agentsync/rules/ -->
```

**`.cursorrules`:**
```
# Cursor Rules for my-project
# AUTO-GENERATED from .agentsync/rules/ - Do not edit directly
# Run: uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py my-project

[concatenated rules content]

# Source of truth: .agentsync/rules/
```

**`.agent/rules/instructions.md`:**
```markdown
# Antigravity Rules for my-project

<!-- AUTO-GENERATED from .agentsync/rules/ - Do not edit directly -->
<!-- Run: uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py my-project -->

[concatenated rules content]

<!-- Source of truth: .agentsync/rules/ -->
```

---

## Safe Zones

Some projects are excluded from sync:

| Project | Reason |
|---------|--------|
| `ai-journal` | Append-only, special handling |
| `writing` | Personal, no AI config needed |

These are hardcoded in `sync_rules.py`.

---

## Workflow

### Daily Workflow

1. **Edit `.agentsync/rules/*.md`** with your agent instructions, constraints, etc.
2. **Save** - Claude hook auto-syncs (if using Claude Code)
3. **Commit** - Pre-commit hook ensures all files are synced
4. **All IDEs** now have consistent instructions

### Adding a New Project

When scaffolding a new project:

1. Run `/scaffold` which creates `.agentsync/` directory with template rules
2. Edit the rule files to customize for your project
3. Run sync: `uv run project-scaffolding/agentsync/sync_rules.py my-project`

---

## MCP Config Sync

MCP configurations are also synced from a central location:

**Source:** `_configs/mcp/`
- `servers.json` - Master MCP server definitions
- `tools/claude.json` - Which servers Claude uses
- `tools/antigravity.json` - Which servers Antigravity uses

**Targets:**
- `~/.claude/claude_desktop_config.json`
- `~/.gemini/antigravity/mcp_config.json`

**Sync command:**
```bash
uv run project-scaffolding/agentsync/sync_mcp.py
```

---

## Troubleshooting

### Files are out of sync

Run the sync manually:
```bash
uv run project-scaffolding/agentsync/sync_rules.py my-project
```

### Project doesn't have .agentsync/ directory

Migrate from old AGENTS.md format:
```bash
uv run project-scaffolding/agentsync/migrate_agents_md.py my-project
```

### Claude hook isn't triggering

Check `.claude/settings.json` includes `agent-sync-on-write.py` in the Write/Edit hooks.

### Antigravity directory not created

The sync script creates `.agent//` automatically. If it doesn't exist after sync, check file permissions.

---

## Architecture Diagram

```
                    +-------------------+
                    | .agentsync/rules/ |  <-- You edit these
                    |  00-overview.md   |
                    |  01-workflow.md   |
                    |  02-constraints.md|
                    |  03-safety.md     |
                    +---------+---------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
      +-------+------+  +-----+------+  +-----+--------+
      | Claude Hook  |  | Pre-Commit |  |   Manual     |
      | (real-time)  |  | (on commit)|  | (CLI)        |
      +-------+------+  +-----+------+  +-----+--------+
              |               |               |
              +---------------+---------------+
                              |
                              v
                    +---------+---------+
                    |   sync_rules.py   |
                    +---------+---------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
      +-------+------+  +-----+------+  +-----+--------+
      |  CLAUDE.md   |  |.cursorrules|  | .agent/ |
      |(Claude Code) |  |  (Cursor)  |  |(Antigravity) |
      +--------------+  +------------+  +--------------+
```

---

## Related Files

| File | Purpose |
|------|---------|
| `project-scaffolding/agentsync/sync_rules.py` | Rules sync script |
| `project-scaffolding/agentsync/sync_mcp.py` | MCP config sync script |
| `project-scaffolding/agentsync/migrate_agents_md.py` | Migration from AGENTS.md |
| `_configs/mcp/servers.json` | Master MCP server definitions |
| `.claude/hooks/validators/agent-sync-on-write.py` | Claude real-time hook |
| `.claude/hooks/validators/agent-sync-check.py` | Pre-commit sync hook |
| `.claude/settings.json` | Hook configuration |

---

## History

- **January 2026:** Initial sync system with AGENTS.md as source
- **January 22, 2026:** Migrated to `.agentsync/rules/` directory structure
- **January 22, 2026:** Added MCP config sync (`_configs/mcp/`)
- **January 22, 2026:** Removed old scripts, updated hooks

---

*Part of the Universal Agent Safety Net - ensuring consistent governance across all AI IDEs.*
