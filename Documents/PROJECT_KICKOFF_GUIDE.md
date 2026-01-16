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

This will copy the core scripts, docs, and update references automatically. See [[PROJECT_STRUCTURE_STANDARDS]] for the expected result.

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
- Update links and descriptions. See [[DOCUMENTATION_HYGIENE]].

### Step 3: Create Project Index (MANDATORY)

**This is required. No project goes forward without this.**

```bash
# Copy template
cp "$SCAFFOLDING/templates/00_Index.md.template" \
   "./00_Index_$(basename "$NEW_PROJECT").md"
```

**See:** [[PROJECT_INDEXING_SYSTEM]] for the complete guide.

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

## Phase 1: Planning (Tier 1 - Big Idea → Concrete Plan)

### What Happens Here
**This is hours of chatting with Tier 1 models** (Claude Sonnet, GPT-4).

**Outputs:**
- `ROADMAP.md` - Long-term vision
- `ARCHITECTURE.md` - System design
- See [[ARCHITECTURE_OVERVIEW_PATTERN]] for layout ideas.

---

## Phase 2: Task Tiering (Still Tier 1)

Once you have a solid plan, use the **Tiered Sprint Planner**.

### Prompt for This Phase
```
We've finished Phase 1 planning. Now I want to tier the execution work.
Please read:
- Tiered Sprint Planner: [[TIERED_SPRINT_PLANNER]]
- Our project docs: [ROADMAP.md, ARCHITECTURE.md, etc.]
```

**See:** [[TIERED_AI_SPRINT_PLANNING]] for the full pattern.

---

## Phase 3: Execution (Mixed Tiers)

Now you execute using appropriate tiers.

- **Tier 3 Tasks:** [[GPT_4O_MINI_WEE_BEE]]
- **Tier 2 Tasks:** [[GPT_4O_MID_WEIGHT]]
- **Tier 1 Tasks:** [[CLAUDE_SONNET_BIG_BRAIN]]

---

## Phase 4: Code Reviews (Quality Control)

**Goal:** Ensure every significant change is reviewed by multiple AI models.

**Standards:**
- [ ] Active review in project root.
- [ ] Naming: `CODE_REVIEW_{REVIEWER}_{VERSION}.md`.
- [ ] Definition of Done (DoD) included.

**See:** [[CODE_REVIEW_STANDARD]] and [[CODE_REVIEW_PROMPT]].

---

## Checklist: New Project Setup

- [ ] Create project directory
- [ ] Copy templates from scaffolding
- [ ] Customize `.cursorrules`
- [ ] Customize `CLAUDE.md`
- [ ] Create Project Index ([[PROJECT_INDEXING_SYSTEM]])
- [ ] Document in `Documents/SPRINT_PLAN.md` ([[TIERED_SPRINT_PLANNER]])

---

*Part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*
*See also: [[PROJECT_STRUCTURE_STANDARDS]] and [[CODE_QUALITY_STANDARDS]].*


## Related Documentation

- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[architecture_patterns]] - architecture
- [[prompt_engineering_guide]] - prompt engineering


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[ai_model_comparison]] - AI models
- [[project_planning]] - planning/roadmap


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[architecture_patterns]] - architecture
- [[prompt_engineering_guide]] - prompt engineering


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[project-scaffolding/README]] - Project Scaffolding


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[architecture_patterns]] - architecture
- [[prompt_engineering_guide]] - prompt engineering


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[ai_model_comparison]] - AI models
- [[project_planning]] - planning/roadmap


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

- [[architecture_patterns]] - architecture
- [[prompt_engineering_guide]] - prompt engineering


- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_KICKOFF_GUIDE]] - project setup

