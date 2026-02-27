# Project Kickoff Guide

> **Purpose:** How to start a new project using project-scaffolding templates and patterns  
> **Audience:** You (Erik) and AI collaborators starting fresh projects
> **Last Updated:** January 15, 2026

---

## Quick Start: "I'm Starting a New Project"

### Step 1: Bootstrap the Project

You can use the automated `apply` command to bootstrap your project:

```bash
# 1. Create and enter your project directory
mkdir -p "$PROJECTS_ROOT/my-new-project" && cd "$PROJECTS_ROOT/my-new-project"

# 2. Initialize git (needed for governance hooks)
git init

# 3. Apply automated scaffolding
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" apply "my-new-project"
```

See [PROJECT_STRUCTURE_STANDARDS](PROJECT_STRUCTURE_STANDARDS.md) for the expected result.

### Step 2: Customize Templates (Critical)

**Edit `AGENTS.md`:**
- Replace `{project_description}` with a clear summary.
- Update `{language}`, `{frameworks}`, and `{ai_strategy}`.
- Update `{run_command}` and `{test_command}`.
- This is the **Source of Truth** for AI assistants. See [[AGENTS_CONSTITUTION]].

**Edit `CLAUDE.md`:**
- Update project summary and tech stack.
- List specific validation commands for the AI to run.
- This tells the AI **how to work** on this specific project.

**Edit `.cursorrules`:**
- Replace `[PROJECT_NAME]` and update the overview.
- Add project-specific safety rules. See [[CURSOR_RULES_BEST_PRACTICES]].

**Edit `Documents/README.md`:**
- Update links and descriptions. See [DOCUMENTATION_HYGIENE](reference/DOCUMENTATION_HYGIENE.md).

### Step 3: Verify Project Index (MANDATORY)

**This is required. No project goes forward without this.**

The automated `scaffold_cli.py apply` command already created a project index for you at `00_Index_[ProjectName].md`.

**You must now:**
1.  **Review the index file** and fill in the 3-sentence summary.
2.  **Update the key components** list if needed.
3.  **Verify the tags** are correct.

**See:** [PROJECT_INDEXING_SYSTEM](PROJECT_INDEXING_SYSTEM.md) for the complete guide.

### Step 4: Discover Relevant Skills (RECOMMENDED)

**Claude Code has 18 skills deployed to `~/.claude/skills/`.** They activate automatically based on conversation context.

**Available skills by category:**
- **Workflow:** `commit`, `pr`, `tasks`, `audit`, `judge`
- **Planning:** `strategy`, `propose`, `trace`, `handoff`
- **Review:** `security-sentinel`, `performance-oracle`, `test-strategist`
- **Domain:** `make-com`, `financial-integrity-guard`, `tax-discovery-engine`
- **Platform:** `platform-rules-expert`, `vercel-react-best-practices`, `youtube-channel-analysis`

Skills are triggered by conversation keywords — no manual activation needed.

---

## The Development Workflow

> **MANDATORY:** All projects in this ecosystem follow the **Unified Project Workflow**.

Do not follow the old Phase 1-4 instructions previously found in this document. Instead, use the single source of truth located in the projects root:

👉 **[Project Workflow](../../Project-workflow.md)** (`/Users/eriksjaastad/projects/Project-workflow.md`)

This workflow covers:
1. **Strategy** (PRD)
2. **Planning** (Kiro)
3. **Proposal** (Agent Hub)
4. **Handoff**
5. **Execution** (Floor Manager + Workers)
6. **Retrospective** (Lessons Learned)

---

## Checklist: New Project Setup

- [ ] Create project directory
- [ ] Copy templates from scaffolding (`scaffold_cli.py apply`)
- [ ] Customize `.cursorrules`
- [ ] Customize `CLAUDE.md`
- [ ] Create Project Index ([PROJECT_INDEXING_SYSTEM](PROJECT_INDEXING_SYSTEM.md))
- [ ] **Follow Unified Workflow:** Start at Phase 1 in [Project Workflow](../../Project-workflow.md)

---

*Part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*

## Related Documentation

- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [PROJECT_KICKOFF_GUIDE](PROJECT_KICKOFF_GUIDE.md) - project setup
- [Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md) - prompt engineering
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
