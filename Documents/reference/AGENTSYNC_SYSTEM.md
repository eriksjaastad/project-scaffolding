# .agentsync System Documentation

**Version:** 1.0  
**Last Updated:** 2026-01-28  
**Canonical Location:** `project-scaffolding/Documents/reference/AGENTSYNC_SYSTEM.md`

---

## Table of Contents

1. [What is .agentsync?](#what-is-agentsync)
2. [Directory Structure](#directory-structure)
3. [How sync_rules.py Works](#how-sync_rulespy-works)
4. [Rules File Organization](#rules-file-organization)
5. [Detecting Manual Edits](#detecting-manual-edits)
6. [Resolving Conflicts](#resolving-conflicts)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## 1. What is .agentsync?

`.agentsync` is a rule synchronization system that generates IDE-specific configuration files from a single source of truth.

### Purpose

- **Single Source of Truth:** Define AI agent rules once in `.agentsync/rules/*.md`
- **Multi-IDE Support:** Automatically generate config files for Claude Code, Cursor, and Antigravity
- **Preserve Custom Content:** User edits outside auto-generated sections are preserved
- **Version Tracking:** Rules have versions to detect outdated projects

### Supported IDEs

| IDE | Output File | Marker Style |
|-----|-------------|--------------|
| **Claude Code** | `CLAUDE.md` | Markdown comments |
| **Cursor** | `.cursorrules` | Shell comments |
| **Antigravity** | `.agent/rules/instructions.md` | Markdown comments + frontmatter |

---

## 2. Directory Structure

```
project-name/
├── .agentsync/
│   ├── README.md              # Brief overview, points here
│   └── rules/
│       ├── 00_header.md       # Project overview, tech stack
│       ├── 01_workflow.md     # Agent hierarchy, workflow
│       ├── 02_constraints.md  # Universal constraints
│       ├── 03_safety.md       # Safety rules
│       └── ...                # Additional rule files
├── CLAUDE.md                  # Auto-generated (with preserved custom sections)
├── .cursorrules               # Auto-generated
└── .agent/
    └── rules/
        └── instructions.md    # Auto-generated
```

### Rule Files Naming Convention

- **Numeric prefix (00-99):** Controls concatenation order
- **Descriptive name:** Explains the rule's purpose
- **.md extension:** Markdown format for readability

**Example:**
```
00_header.md       # Appears first
01_workflow.md     # Appears second
02_constraints.md  # Appears third
```

---

## 3. How sync_rules.py Works

### Execution

```bash
# Sync a specific project
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name

# Sync all projects with .agentsync/
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py --all

# Preview changes without writing
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name --dry-run

# Sync and git add changed files
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name --stage
```

### The Sync Process

1. **Load Rules:** Reads all `.md` files from `.agentsync/rules/` in alphabetical order
2. **Parse Frontmatter:** Checks YAML frontmatter for `targets:` field (which IDEs to include)
3. **Concatenate Content:** Combines rule files (excluding frontmatter) with `\n\n` separator
4. **Preserve Custom Sections:** Extracts content before `START` marker and after `END` marker
5. **Generate Output:** Wraps concatenated rules in IDE-specific markers
6. **Write Files:** Updates `CLAUDE.md`, `.cursorrules`, `.agent/rules/instructions.md`

### Marker System

**Markdown Style (CLAUDE, Antigravity):**
```markdown
<!-- AGENTSYNC:START - Do not edit between markers -->
<!-- To modify synced rules: Edit .agentsync/rules/*.md, then run: -->
<!-- uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name -->

[AUTO-GENERATED CONTENT HERE]

<!-- Source: .agentsync/rules/*.md -->
<!-- AGENTSYNC:END - Custom rules below this line are preserved -->

[CUSTOM CONTENT PRESERVED HERE]
```

**Comment Style (Cursor):**
```bash
# AGENTSYNC:START - Do not edit between markers
# To modify synced rules: Edit .agentsync/rules/*.md, then run:
# uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name

[AUTO-GENERATED CONTENT HERE]

# Source: .agentsync/rules/*.md
# AGENTSYNC:END - Custom rules below this line are preserved

[CUSTOM CONTENT PRESERVED HERE]
```

---

## 4. Rules File Organization

### Frontmatter (Optional)

Each rule file can have YAML frontmatter to control which IDEs receive it:

```yaml
---
targets: ["claude", "cursor"]  # Only sync to Claude and Cursor
---

# Rule Content Here
```

**Supported targets:**
- `"*"` - All IDEs (default if no frontmatter)
- `"claude"` - Claude Code only
- `"cursor"` - Cursor only
- `"antigravity"` - Antigravity only
- `["claude", "cursor"]` - Multiple specific IDEs

### Content Structure

**Each rule file should contain:**
1. Clear heading (`#` or `##`)
2. Concise explanation
3. Specific rules or constraints
4. Examples if needed

**Example rule file:**

```markdown
---
targets: ["*"]
---

# Universal Constraints

## Never Do

- NEVER modify `.env` or `venv/`
- NEVER hard-code API keys, secrets, or credentials
- NEVER use absolute paths

## Always Do

- ALWAYS update `EXTERNAL_RESOURCES.yaml` when adding external services
- ALWAYS use retry logic for API calls
```

---

## 5. Detecting Manual Edits

### Manual Edits vs. Generated Content

**ALLOWED (preserved):**
- Content **before** `<!-- AGENTSYNC:START -->` marker
- Content **after** `<!-- AGENTSYNC:END -->` marker

**FORBIDDEN (will be overwritten):**
- Content **between** `START` and `END` markers

### How to Detect Drift

Currently, there's no built-in drift detection. To check if a file has manual edits between markers:

```bash
# Check if content between markers differs from regenerated version
# (Note: This requires a proper drift detector script)

# Manual check:
# 1. Run sync with --dry-run
# 2. Save current file
# 3. Run actual sync
# 4. Diff the files
```

**Known Issue:** The `--dry-run` flag prints preview messages, not actual content, making automated drift detection difficult without additional tooling.

---

## 6. Resolving Conflicts

### Scenario 1: Manual Edits in Auto-Generated Section

**Problem:** You edited content between `START` and `END` markers.

**Solution:**
1. Copy your edits
2. Move them to the appropriate `.agentsync/rules/*.md` file
3. Re-run sync: `uv run sync_rules.py project-name`
4. Your edits are now part of the auto-generated section

### Scenario 2: Project-Specific Rules

**Problem:** You need rules that only apply to this project.

**Solution:**
Place them **after** the `<!-- AGENTSYNC:END -->` marker:

```markdown
<!-- AGENTSYNC:END - Custom rules below this line are preserved -->

## Project-Specific Rules

- This project uses a special database connection pool
- Run migrations with `./migrate.sh` before testing
```

### Scenario 3: Outdated Rules Version

**Problem:** `sync_rules.py` reports "Project has older rules version".

**Solution:**
```bash
# Re-sync to update to latest rules
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name
```

The script automatically updates `.scaffolding-version` with the new `rules_version`.

---

## 7. Best Practices

### DO

✅ **Keep rules in `.agentsync/rules/`** - Never edit CLAUDE.md, .cursorrules directly between markers  
✅ **Use numeric prefixes** - Control import order with `00_`, `01_`, etc.  
✅ **Add project-specific rules after END marker** - They'll be preserved  
✅ **Run sync after editing rules** - Keep all IDEs in sync  
✅ **Use `--dry-run` to preview** - Check changes before applying  
✅ **Commit .agentsync/rules/ to git** - Version control your governance

### DON'T

❌ **Don't edit between START/END markers** - Changes will be overwritten  
❌ **Don't skip frontmatter on targeted rules** - Default is `targets: ["*"]`  
❌ **Don't create gaps in numbering** - Use sequential prefixes (00, 01, 02...)  
❌ **Don't put secrets in rules** - These are committed to git!  
❌ **Don't delete markers manually** - sync_rules.py won't know where to insert content

### IDE-Specific Customization

If you need IDE-specific rules:

```yaml
---
targets: ["claude"]  # Only for Claude
---

# Claude-Specific Optimizations

Use the following shortcuts when working in Claude Code...
```

---

## 8. Troubleshooting

### Problem: "No .agentsync/rules/ directory"

**Solution:** Create the directory structure:
```bash
mkdir -p .agentsync/rules
echo "# Project Overview\n\nTODO: Add project description" > .agentsync/rules/00_header.md
```

### Problem: "AGENTSYNC markers not found"

**Solution:** The file was created manually. Run sync to add markers:
```bash
# Backup first
cp CLAUDE.md CLAUDE.md.backup

# Run sync (it will add markers)
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name
```

### Problem: "Custom content disappeared after sync"

**Cause:** Custom content was between START/END markers.

**Solution:**
```bash
# Restore from backup
cp CLAUDE.md.backup CLAUDE.md

# Extract custom content
# Move it AFTER the END marker
# Re-run sync
```

### Problem: "sync_rules.py not found"

**Solution:** Ensure you're running from correct location:
```bash
# Must be run via absolute path or $PROJECTS_ROOT
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py project-name

# Or cd to the directory first
cd $PROJECTS_ROOT/project-scaffolding
uv run agentsync/sync_rules.py project-name
```

### Problem: "Some projects skip sync"

**Cause:** Projects in `SAFE_ZONES` list are protected from auto-sync.

**Current safe zones:**
- `ai-journal` - Personal journal entries
- `writing` - Personal writing projects

**Solution:** If you need to sync a safe zone, edit `sync_rules.py` line 130 to remove it from the list.

---

## Version History

- **v1.0 (2026-01-28):** Initial comprehensive documentation
  - Documented all 8 sections
  - Explained marker system
  - Added troubleshooting guide

---

## See Also

- [.agentsync/README.md](../../.agentsync/README.md) - Quick reference
- [Project-workflow.md](../../../Project-workflow.md) - Master workflow
- [AGENTS.md](../../AGENTS.md) - Ecosystem constitution
