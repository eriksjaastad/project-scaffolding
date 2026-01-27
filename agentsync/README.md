# AgentSync

Synchronizes AI instruction rules from a single source to multiple IDE-specific config files.

---

## Why This Exists

**The Problem (January 2026):**

We were using three AI coding assistants simultaneously: Claude Code, Cursor, and Antigravity (Gemini). Each reads a different config file:

| IDE | Config File |
|-----|-------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Antigravity | `.agent/rules/instructions.md` |

When we discovered a great pattern (like the IndyDevDan video on self-validating agents with hooks), we'd implement it in Claude's rules... and then the other agents had no idea. We were building siloed knowledge.

**The Insight:**

Great ideas shouldn't be siloed into one IDE. All our agents should get the same benefit from every improvement we make.

**The Solution:**

Single source of truth → auto-generate all IDE configs.

Edit once in `.agentsync/rules/`, run sync, all IDEs get the same instructions. No more copy-paste drift. No more "I forgot to update Cursor's rules."

**Why It Lives in project-scaffolding:**

AgentSync is infrastructure for setting up projects correctly. It's part of the "make projects work well from day one" toolset, alongside templates, scripts, and documentation patterns. Keeping it here makes the relationship obvious: AGENTS.md templates → AgentSync → IDE configs.

---

## How It Works

```
.agentsync/rules/                     Target Files
├── 00-overview.md          ─────►    CLAUDE.md (Claude Code)
├── 01-workflow.md          ─────►    .cursorrules (Cursor)
├── 02-constraints.md       ─────►    .agent/rules/instructions.md (Antigravity)
└── 03-safety.md
```

**Single source of truth.** Edit rules in `.agentsync/rules/`, run sync, all IDEs get updated.

## Target IDEs

| IDE | Output File | How It Reads |
|-----|-------------|--------------|
| Claude Code | `CLAUDE.md` | Automatically reads project root |
| Cursor | `.cursorrules` | Automatically reads project root |
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
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync_rules.py project-name

# Sync all projects with .agentsync/
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync_rules.py --all

# List projects with .agentsync/
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync_rules.py --list
```

## Files

| Script | Purpose |
|--------|---------|
| `sync_rules.py` | Main sync: `.agentsync/rules/` → IDE configs |
| `migrate_agents_md.py` | One-time migration: AGENTS.md → `.agentsync/rules/` structure |
| `sync_mcp.py` | Syncs MCP server configurations |

## MCP Config Locations

`sync_mcp.py` keeps MCP configs in sync across IDEs. Current locations:

| Location | IDE | Notes |
|----------|-----|-------|
| `~/.claude/claude_desktop_config.json` | Claude Desktop | |
| `~/.cursor/mcp.json` | Cursor | |
| `~/.antigravity/mcp_config.json` | Antigravity (standalone) | |
| `~/.gemini/antigravity/mcp_config.json` | Antigravity (via Gemini) | May have different server names |

**Source of truth:** `$PROJECT_ROOT/_configs/mcp/`

## Integration with Scaffold

AgentSync lives inside project-scaffolding. The `scaffold apply` command:

1. Copies `.agentsync/rules/` templates with placeholder substitution
2. Runs `sync_rules.py` to generate CLAUDE.md, .cursorrules, .agent/rules/instructions.md
3. Appends project-specific content outside AGENTSYNC markers

## AGENTSYNC Markers

Generated files use markers to separate synced content from custom additions:

```markdown
<!-- AGENTSYNC:START -->
[synced content here - do not edit]
<!-- AGENTSYNC:END -->

[custom project-specific content below - preserved on re-sync]
```
