# Architectural Decisions

> *Documenting WHY we made decisions, not just WHAT we built.*
>
> This file exists because January 2026 taught us: without documented reasoning, even the people who made the decisions forget why.

---

## Decision Log

### 2026-01-25: Move AgentSync into project-scaffolding

**Context:** AgentSync was originally in `_tools/agentsync/`. We spent an hour confused about why AgentSync existed separately from AGENTS.md templates.

**Decision:** Move AgentSync into `project-scaffolding/agentsync/`.

**Reasoning:**
1. AgentSync is infrastructure for setting up projects correctly
2. The templates (AGENTS.md, CLAUDE.md) live in project-scaffolding
3. Having the sync tool physically next to the templates makes the relationship obvious
4. Reduces the number of places to look when debugging agent config issues

**Alternatives considered:**
- Keep in `_tools/`: Rejected because it obscured the relationship with templates
- Merge into scaffold CLI: Rejected because agentsync should work standalone (for re-syncing existing projects)

---

### 2026-01-22: Create `.agentsync/rules/` directory structure

**Context:** AGENTS.md was a 500+ line monolith. Different sections applied to different IDEs. Editing was fragile.

**Decision:** Split agent rules into modular files in `.agentsync/rules/`.

**Reasoning:**
1. Modular files (00-overview.md, 01-workflow.md) can be edited independently
2. YAML frontmatter allows targeting specific IDEs (`targets: ["claude", "cursor"]`)
3. Filename ordering (00-, 01-) gives predictable concatenation
4. Smaller files = fewer merge conflicts

**Alternatives considered:**
- Multiple AGENTS.md files: Rejected because IDE tools expect specific filenames
- Single file with section markers: Rejected because still monolithic

---

### 2026-01 (early): Create AgentSync

**Context:** Using three AI assistants (Claude Code, Cursor, Antigravity). Each reads a different config file. Improvements to one set of rules never reached the others.

**Inspiration:** IndyDevDan video on self-validating agents with Claude Code hooks. Great idea, but siloed to Claude.

**Decision:** Build a sync system: single source of truth → generate all IDE configs.

**Reasoning:**
1. Edit once, all IDEs benefit
2. No more copy-paste drift between CLAUDE.md and .cursorrules
3. Hooks can auto-sync on file save (real-time) or pre-commit (batch)
4. Preserves custom content outside AGENTSYNC markers

**Alternatives considered:**
- Manual copy-paste: Rejected because we kept forgetting to sync
- Symlinks: Rejected because IDEs expect different formats/headers
- IDE plugins: Rejected because we can't control all three IDEs' behavior

---

### 2025-12: Create project-scaffolding

**Context:** Every new project was starting from scratch. We kept recreating the same file structures, the same safety patterns, the same documentation layouts.

**Decision:** Extract patterns into a scaffolding project.

**Reasoning:**
1. Capture "what a well-structured project looks like"
2. One command to set up a project correctly
3. Battle-tested patterns from real projects (image-workflow, trading-copilot)
4. Living documentation - patterns evolve as we learn

**Philosophy:** "We're explorers building experiments, not products. The scaffolding is the real product."

---

## Principles Behind Decisions

### 1. Single Source of Truth

Multiple places to edit the same information = guaranteed drift. We repeatedly choose "one place to edit, auto-generate the rest."

Examples:
- `.agentsync/rules/` → CLAUDE.md, .cursorrules, .agent/rules/
- `_configs/mcp/servers.json` → all IDE MCP configs

### 2. Explicit Over Implicit

When we can't remember why something exists, that's a failure of documentation. Every component should have documented reasoning.

### 3. Safe Zones

Some content shouldn't be auto-modified. Personal projects, sensitive data, append-only journals. We explicitly mark these as protected.

### 4. Idempotent Operations

Running scaffold or sync twice should produce the same result. No "it worked the first time but broke on re-run."

### 5. Preserve Custom Content

Generated files use markers (AGENTSYNC:START/END) so project-specific additions aren't blown away on re-sync.

---

## Questions We Still Haven't Answered

### Should AGENTS.md be the source for `.agentsync/rules/`?

**Current state:** Both exist. AGENTS.md is a template. `.agentsync/rules/` is modular files. There's conceptual overlap.

**Open question:** Should we read from AGENTS.md and generate .agentsync/rules/, or vice versa, or are they genuinely separate concerns?

**Tentative answer:** They serve different purposes:
- AGENTS.md = "constitution" (hierarchy, philosophy, roles)
- .agentsync/rules/ = "operational rules" (synced to IDE configs)

But this needs validation through usage.

### Should scaffold be interactive?

**Current state:** Uses defaults, user edits after.

**Open question:** Should `scaffold apply --interactive` prompt for PROJECT_DESCRIPTION, LANGUAGE, etc.?

**Tentative answer:** Not yet. Defaults work. Add interactivity only if users request it.

---

*Last updated: 2026-01-25*
