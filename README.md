
<!-- SCAFFOLD:START - Do not edit between markers -->
# project-scaffolding

Brief description of the project's purpose

## Quick Start

```bash
# Setup
pip install -r requirements.txt

# Run
python main.py
```

## Documentation

See the `Documents/` directory for detailed documentation.

## Status

- **Current Phase:** Foundation
- **Status:** #status/active

<!-- SCAFFOLD:END - Custom content below is preserved -->
# Project Scaffolding

|> *The meta-project: Extracting patterns from experiments to build better projects faster.*

---

## What This Is

This is the **scaffolding project** - a collection of patterns, principles, and templates extracted from building multiple deep projects.

**Our Mission:** Help all projects get done quickly at the highest quality and at the lowest cost.

**Not a framework.** Not rigid rules. Just battle-tested patterns that make future projects:
- Faster to start
- Easier to maintain  
- Safer (data doesn't get lost)
- More consistent across collaborators (AI and human)

---

## UV Run-first Policy (Effective: February 2026)

- New Python commands should be executed with `uv run` (or a project-approved `uvrun` wrapper). This enforces tool-managed, reproducible environments without global installs.
- Existing environment setups and `.env` usage are not to be mass-migrated. Do not change a project’s current `.env`/`venv`/Poetry/Pipenv workflow unless there is explicit approval and a tracked migration plan.
- Legacy compatibility: Existing projects may continue using their established runners (e.g., `python`, `poetry run`, `pipenv run`, `make`). When you touch a legacy script or add a new command, prefer introducing `uv run` for the new work and leave the rest unchanged until an approved migration occurs.
- Governance alignment: This standard aligns with AGENTS.md constraints (no global installs; prefer tool-managed environments; do not modify `.env` or `venv/`) and does not supersede secrets-management guidance (e.g., Doppler). Follow each project’s configured secrets workflow.

---


**What We DON'T Do:**
- ❌ Cost tracking (that's `ai-usage-billing-tracker`'s job)
- ❌ Project status monitoring (that's `project-tracker`'s job)
- ✅ We recommend patterns and build automation; others implement monitoring

---

## Why Each Component Exists

|> *Because "what" without "why" leads to forgotten decisions and repeated mistakes.*

### Core Components

| Component | Why It Exists |
|-----------|---------------|
| **templates/** | Every new project was starting from scratch. We kept recreating the same files. Templates capture "what a well-structured project looks like" so we don't reinvent it each time. |
| **agentsync/** | We use Claude, Cursor, and Antigravity simultaneously. Each reads different config files. Without sync, improvements to one agent's rules never reached the others. AgentSync makes one edit propagate everywhere. |
| **scaffold/cli.py** | Copying templates manually was error-prone. The CLI ensures consistent setup: right files, right structure, right placeholders filled in. One command instead of 15 copy-pastes. |
| **patterns/** | Hard-won lessons were getting lost. "Every safety system was a scar" - we kept re-learning the same lessons. Patterns document WHY we do things, not just how. |
| **Documents/** | Project documentation was scattered or missing. This structure (guides/, reference/, safety/) gives every project the same organized home for docs. |

### Why `.agentsync/rules/` Instead of Just AGENTS.md?

**Historical context:** AGENTS.md was the original "agent constitution" - hierarchy, workflow, constraints. It worked well for a single file.

**The problem:** As rules grew, AGENTS.md became a 500+ line monolith. Different sections applied to different IDEs. Maintaining one massive file was fragile.

**The solution:** Split into modular files (`00-overview.md`, `01-workflow.md`, etc.) that can be:
- Targeted to specific IDEs via YAML frontmatter
- Edited independently without merge conflicts
- Ordered by filename (00-, 01-, etc.)

AGENTS.md template still exists for the "constitution" content. `.agentsync/rules/` handles the operational rules that get synced to IDE configs.

### Why AGENTSYNC Markers?

Generated files (CLAUDE.md, .cursorrules) use markers:
```
<!-- AGENTSYNC:START -->
[synced content]
<!-- AGENTSYNC:END -->
[custom content preserved]
```

**Why:** Some projects need project-specific rules that don't belong in the shared templates. Markers let us sync universal rules while preserving custom additions. Re-running sync doesn't blow away your customizations.

### Why Safe Zones?

Certain projects (ai-journal, writing) are excluded from scaffolding and sync.

**Why:** These are personal/sensitive projects where AI agents shouldn't be auto-modifying files. The "safe zone" pattern prevents accidental overwrites of content that matters differently than code.

---

## Quick Start

**See `QUICKSTART.md` for step-by-step checklists with copy-paste commands.**

### Starting a New Project (2-minute version)

```bash
# 1. Create project and apply automated scaffolding
mkdir -p "$PROJECTS_ROOT/my-new-project" && cd "$PROJECTS_ROOT/my-new-project"
git init
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" apply "my-new-project"
```

Then customize the templates (especially the `00_Index_*.md` - it's MANDATORY).

### Adding Scaffolding to an Existing Project

```bash
cd /path/to/existing-project

# Apply scaffolding via CLI
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" apply "$(basename $(pwd))"
```

Then customize for your project. See `QUICKSTART.md` for the full checklist.

### Essential Reading

| Document | Purpose |
|----------|---------|
| `QUICKSTART.md` | Step-by-step checklists (new + existing projects) |
| `DECISIONS.md` | Architectural decision log - document the "why" behind choices |
| `Documents/PROJECT_KICKOFF_GUIDE.md` | Detailed planning workflow |
| `Documents/CODE_QUALITY_STANDARDS.md` | **MANDATORY** coding rules |
| `Documents/PROJECT_STRUCTURE_STANDARDS.md` | Directory conventions |
| `Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md` | Secrets management (replaces `.env` files) |
| `Documents/reference/AGENT_CONFIG_SYNC.md` | **NEW:** Auto-sync AGENTS.md to all IDEs |

### Understanding This Scaffolding

1. **Pattern Analysis** (`Documents/PATTERN_ANALYSIS.md`)
   - See all identified patterns with confidence levels
   - Understand which are proven (🟢), emerging (🟡), or candidates (🔵)

2. **Safety Systems** (`patterns/safety-systems.md`)
   - 6 proven patterns with code examples
   - "Every safety system was a scar" philosophy
   - Real scar stories from projects

3. **Development Philosophy** (`patterns/development-philosophy.md`)
   - 7 core principles: Layer-by-layer, data before decisions, etc.
   - When to apply, when not to apply
   - Anti-patterns to avoid

4. **Tiered AI Sprint Planning** (`patterns/tiered-ai-sprint-planning.md`)
   - Route tasks to cost-appropriate AI models
   - 3 tiers: Big Brain (architecture), Mid-Weight (features), Worker Bee (boilerplate)
   - Escalation system to avoid getting stuck with wrong-tier models
   - Multi-model review automation (from image-workflow)

5. **Learning Loop Pattern** (`patterns/learning-loop-pattern.md`)
   - How to create reinforcement learning cycles in any project
   - 4 universal components: Trigger, Documentation, Analysis, Reinforcement
   - Guidance for model, workflow, and safety learnings
   - Prevents "write-only documentation" - closes the gap between learning and applying

6. **Self-Learning Projects** (Skills Management)
   
   This scaffolding supports projects that improve over time by capturing what works. Skills (reusable AI instructions) can live:
   - In a **shared library** across projects (`$PROJECTS_ROOT/agent-skills-library/`)
   - **Within individual projects** (project-specific patterns)
   - Or **both** - shared patterns + project-specific skills
   
   Skills can move between locations as they mature. Start wherever makes sense; extract to a shared library when you find yourself copying across 3+ projects.
   
   See `patterns/learning-loop-pattern.md` for establishing feedback cycles.

### Managing Your Projects

**Secrets Management (Doppler):**  
As of January 2026, **8 core projects** use Doppler for centralized secrets management instead of local `.env` files. See `Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md` for:
- Which projects are migrated
- How to run projects with `doppler run --`
- Rollback procedures if needed
- Best practices for new projects

**External Resources:**  
`EXTERNAL_RESOURCES.md` - Track which services/APIs each project uses
- Prevents "I got a bill but don't know which project" situations
- Cost tracking across all projects
- Credential locations documented
- Service health monitoring

---

## Current Source Projects

Patterns are being extracted from:

1. **image-workflow** (2.5 months, battle-tested)
   - Documentation structure
   - Safety systems ("every safety system was a scar")
   - Disaster recovery
   - Session archives

2. **Trading Co-Pilot** (3 weeks, Layer 1-3 complete)
   - Railway + Postgres deployment
   - Cron dispatcher pattern
   - Fuzzy grading systems
   - Multi-model comparison

3. **Cortana Personal AI** (Layer 1 complete)
   - Privacy-first architecture
   - Daily automation via launchd
   - Layer-by-layer development (incrementally useful)
   - Local-first data with structured memory storage
   - Cost-conscious AI usage (~$0.60/month)

4. **Hypocrisy Now** (ongoing)
   - RSS infrastructure
   - Sentiment analysis
   - Content aggregation

5. **AI Journal** (ongoing)
   - Documentation patterns
   - Personal knowledge management

---

## Philosophy

**Core document:** `PROJECT_PHILOSOPHY.md` (this directory)

Key principles:
- **We're explorers** - Building experiments, not products
- **Data before decisions** - 30-60 days before judging
- **Two-level game** - Domain patterns + Meta patterns (this project!)
- **The scaffolding is the real product** - Learning how to build maintainable projects

---

## What We're Building Toward

A **template repository** that gives every new project:

1. **Standard structure** (`Documents/`, `.cursorrules`, etc.)
2. **Safety systems** (backups, disaster recovery, data integrity)
3. **Testing approach** (what needs tests, what doesn't)
4. **Deployment patterns** (Railway, .env, cron, databases)
5. **Documentation templates** (README, ARCHITECTURE, SESSION_LOGS)
6. **Decision frameworks** (when to build, consolidate, kill features)

---

## Current Status

**Phase:** Discovery & Pattern Collection → **Initial Extraction Complete! ✅**

**What's Ready:**
- ✅ **Pattern Analysis** - 20+ patterns identified and documented
- ✅ **Templates** - Documentation structure, CLAUDE.md, .cursorrules, Tiered Sprint Planner
- ✅ **Safety Systems** - 6 proven patterns documented with code examples
- ✅ **Development Philosophy** - 7 core principles extracted
- ✅ **Tiered AI Sprint Planning** - Cost-effective AI usage pattern documented
- ✅ **Project Kickoff Guide** - Complete walkthrough for starting new projects
- ✅ **Usage Guide** - How to use this scaffolding in new projects
- ✅ **External Resources Tracking** - System to prevent duplicate services and surprise bills

**Ready for:**
- ✅ Using templates in new projects
- ✅ Following documented patterns
- ✅ Contributing new patterns as they emerge
- ✅ Extracting examples from source projects

**Next phases:**
- Month 2-3: Extract real examples from source projects
- Month 3: Consolidate patterns into categories
- Month 4: Refine templates based on usage
- Month 6: Consider creating actual `project-scaffolding-template` repo

---

## CRITICAL: Source Files for `scaffold apply`

**DO NOT MOVE THESE FILES.** The `scaffold apply` command copies these files to target projects. Moving them breaks the CLI.

### Root-Level Source Files (DO NOT MOVE)

| File | Copied To | Purpose |
|------|-----------|---------|
| `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` | `Documents/` | Code review and governance protocol |
| `scripts/warden_audit.py` | `scripts/` | Security audit script |
| `scripts/validate_project.py` | `scripts/` | Project validation script |
| `patterns/code-review-standard.md` | `Documents/patterns/` | Code review checklist |
| `patterns/learning-loop-pattern.md` | `Documents/patterns/` | Learning loop documentation |

### Template Directory (templates/)

| Template | Creates | Purpose |
|----------|---------|---------|
| `templates/AGENTS.md.template` | `AGENTS.md` | Agent hierarchy and rules |
| `templates/CLAUDE.md.template` | `CLAUDE.md` | Claude-specific instructions |
| `templates/TODO.md.template` | `TODO.md` | Task tracking format |
| `templates/README.md.template` | `README.md` | Project readme |
| `templates/.agentsync/rules/*.md` | `.agentsync/rules/` | Modular agent rules |

### If You Need to Reorganize

1. **Update `scaffold/cli.py`** - Change the source paths in `scripts_to_copy` and `docs_to_copy`
2. **Test with dry-run** - `python scaffold_cli.py apply some-project --dry-run`
3. **Verify no "Source not found" errors**

---

## Structure

```
project-scaffolding/
├── README.md                    ← You are here
├── .cursorrules                 ← Project rules for this meta-project
│
├── REVIEWS_AND_GOVERNANCE_PROTOCOL.md  ← ⚠️ SOURCE FILE - scaffold apply copies this
│
├── scripts/                     ← ⚠️ SOURCE FILES - scaffold apply copies these
│   ├── warden_audit.py          ← Security audit (copied to projects)
│   └── validate_project.py      ← Project validation (copied to projects)
│
├── patterns/                    ← ⚠️ SOURCE FILES - scaffold apply copies these
│   ├── safety-systems.md        ← Data protection patterns
│   ├── development-philosophy.md ← Development principles
│   ├── code-review-standard.md  ← Copied to projects/Documents/patterns/
│   ├── learning-loop-pattern.md ← Copied to projects/Documents/patterns/
│   └── tiered-ai-sprint-planning.md ← Cost-effective AI usage
│
├── templates/                   ← Template sources for scaffold apply
│   ├── root/                    ← Templates for projects root (sync-root command)
│   ├── .agentsync/rules/        ← Agent rules templates
│   ├── Documents/               ← Documentation structure template
│   ├── AGENTS.md.template       ← Agent hierarchy template
│   ├── CLAUDE.md.template       ← AI instructions template
│   ├── TODO.md.template         ← Task format template
│   └── README.md.template       ← Project readme template
│
├── scaffold/                    ← CLI source code
│   └── cli.py                   ← The scaffold command implementation
│
├── agentsync/                   ← Rules sync to IDE configs
│   └── sync_rules.py            ← Syncs .agentsync/rules to CLAUDE.md, etc.
│
└── Documents/                   ← Meta-documentation (NOT copied to projects)
    ├── This folder is for project-scaffolding's OWN docs
    └── Don't confuse with templates/Documents/ which IS copied
```

---

## How to Contribute to This

When working on any project, notice:
1. **Patterns repeating** across 2+ projects (document it)
2. **Decisions you wish you'd made earlier** (capture the framework)
3. **Safety systems that saved you** (document why they exist)
4. **Structures that make maintenance easier** (extract the pattern)

Don't force it. Let patterns emerge naturally.

---

## Timeline

- **Now - Month 2:** Pattern collection phase
- **Month 3:** First consolidation (group patterns into categories)
- Month 4: Extract templates from proven patterns
- Month 6: Consider creating the actual `project-scaffolding-template` repo

---

*This is a living meta-project. It grows as we learn.*  
*Started: December 21, 2025*

## Related Documentation

- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [PROJECT_KICKOFF_GUIDE](Documents/PROJECT_KICKOFF_GUIDE.md) - project setup
- [Automation Reliability](patterns/automation-reliability.md) - automation
- [Cost Management](Documents/reference/MODEL_COST_COMPARISON.md) - cost management
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [AI Team Orchestration](patterns/ai-team-orchestration.md) - orchestration
- [Agent Skills Library](../agent-skills-library/README.md) - Agent Skills
- [ai-usage-billing-tracker/README](../ai-model-scratch-build/README.md) - AI Billing Tracker
- [cortana-personal-ai/README](../ai-model-scratch-build/README.md) - Cortana AI
- [hypocrisynow/README](../ai-model-scratch-build/README.md) - Hypocrisy Now
- [image-workflow/README](../ai-model-scratch-build/README.md) - Image Workflow
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
- [project-tracker/README](../ai-model-scratch-build/README.md) - Project Tracker

## Development Resources
- [[project-tracker/data/WARDEN_LOG.yaml|WARDEN_LOG.yaml]]
- [scripts/warden_audit.py|warden_audit.py](scripts/warden_audit.py|warden_audit.py)
- [scaffold/__init__.py|__init__.py](scaffold/__init__.py|__init__.py)
