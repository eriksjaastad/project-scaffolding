# Project Kickoff Guide

> **Purpose:** How to start a new project using project-scaffolding templates and patterns  
> **Audience:** You (Erik) and AI collaborators starting fresh projects
> **Last Updated:** January 15, 2026

---

## Quick Start: "I'm Starting a New Project"

### Step 1: Copy the Bones

You can use the automated `apply` command to bootstrap your project:

```bash
# In project-scaffolding directory
doppler run -- ./venv/bin/python scaffold_cli.py apply my-new-project
```

This will copy the core scripts, docs, and update references automatically. See [PROJECT_STRUCTURE_STANDARDS](PROJECT_STRUCTURE_STANDARDS.md) for the expected result.

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

### Step 3: Create Project Index (MANDATORY)

**This is required. No project goes forward without this.**

```bash
# Copy template
cp "$SCAFFOLDING/templates/00_Index.md.template" \
   "./00_Index_$(basename "$NEW_PROJECT").md"
```

**See:** [PROJECT_INDEXING_SYSTEM](PROJECT_INDEXING_SYSTEM.md) for the complete guide.

### Step 4: Discover Relevant Skills (RECOMMENDED)

**Check the skills library for patterns that could help this project:**

```bash
# See what skills exist
ls $PROJECTS_ROOT/agent-skills-library/playbooks/

# Run detection to see which skills might be relevant
python $PROJECTS_ROOT/agent-skills-library/scripts/detect_skill_candidates.py
```

**Ask the AI:**
> "Review the skills in agent-skills-library/playbooks/ and recommend which ones would be useful for this project based on [project description]."

**Then:**
1. Add relevant skills to `00_Index_*.md` → "Skills Used" section
2. Add skills to `AGENTS.md` → "Skills Library" section
3. Update `agent-skills-library/SKILL_USAGE.md` to track adoption

**Why this matters:**
- Skills encode proven patterns - don't reinvent the wheel
- Using skills in more projects helps promote them (🟡 → 🟢)
- Feedback from real usage improves the skills for everyone

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
