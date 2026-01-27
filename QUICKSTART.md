# Project Scaffolding - Quick Start

> **Mission:** Use these templates and patterns to start projects faster and maintain them better.

---

## Choose Your Path

| Scenario | Jump To |
|----------|---------|
| Starting a brand new project | [New Project Checklist](#new-project-checklist) |
| Adding scaffolding to an existing project | [Existing Project Checklist](#existing-project-checklist) |
| Understanding what's in this scaffolding | [What's Included](#whats-included) |

---

## New Project Checklist

### Prerequisites

```bash
# Set your scaffolding path (add to ~/.zshrc for permanence)
export SCAFFOLDING="$PROJECTS_ROOT/project-scaffolding"
```

---

### Phase 1: Create Structure (5 minutes)

```bash
# 1. Create and enter your project directory
NEW_PROJECT="$PROJECTS_ROOT/my-new-project"
mkdir -p "$NEW_PROJECT"
cd "$NEW_PROJECT"

# 2. Initialize git (needed for governance hooks)
git init

# 3. Copy templates
cp -r "$SCAFFOLDING/templates/Documents" ./Documents
cp "$SCAFFOLDING/templates/AGENTS.md.template" ./AGENTS.md
cp "$SCAFFOLDING/templates/.cursorignore.template" ./.cursorignore
cp "$SCAFFOLDING/templates/TODO.md.template" ./TODO.md
cp "$SCAFFOLDING/templates/README.md.template" ./README.md
cp "$SCAFFOLDING/templates/.gitignore" ./.gitignore
cp "$SCAFFOLDING/templates/00_Index.md.template" "./00_Index_$(basename $NEW_PROJECT).md"

# 4. Generate IDE configs from AGENTS.md (creates .cursorrules, CLAUDE.md, .agent/rules/)
$HOME/.local/bin/uv run "$SCAFFOLDING/scripts/sync_agent_configs.py" "$(basename $NEW_PROJECT)"

# 5. Install governance hooks (secrets scanning, path checking, auto-sync)
"$PROJECTS_ROOT/_tools/governance/install-hooks.sh" .
```

**Checklist:**
- [ ] Project directory created
- [ ] Git initialized
- [ ] Templates copied from scaffolding
- [ ] IDE configs generated via sync script
- [ ] Governance hooks installed

---

### Phase 2: Customize Templates (10-15 minutes)

Edit each file and replace the placeholders:

#### 2.1 Project Index (MANDATORY - Do This First)

**File:** `00_Index_[YourProject].md`

- [ ] Write 3-sentence summary:
  - Sentence 1: What problem does this solve?
  - Sentence 2: Key technologies/approach
  - Sentence 3: Current status
- [ ] Update YAML frontmatter tags:
  - `p/[your-project-name]`
  - `type/[standard|ai-agent|pipeline|dashboard|etc]`
  - `domain/[ai|finance|image|etc]`
  - `status/active`
  - `tech/[python|typescript|etc]`
- [ ] List key components (can be brief initially)
- [ ] Delete the instruction block at the top

#### 2.2 AGENTS.md (AI Source of Truth)

**File:** `AGENTS.md`

> **Important:** AGENTS.md is the **single source of truth** for AI agent configuration. Edit only this file - `.cursorrules`, `CLAUDE.md`, and `.agent/rules/agents.md` are auto-generated from it. See `Documents/reference/AGENT_CONFIG_SYNC.md` for details.

- [ ] Replace `{project_description}` with clear summary
- [ ] Update `{language}`, `{frameworks}`, `{ai_strategy}`
- [ ] Set `{run_command}` and `{test_command}`
- [ ] Add project-specific constraints
- [ ] Update Definition of Done checklist
- [ ] Run sync: `$HOME/.local/bin/uv run $SCAFFOLDING/scripts/sync_agent_configs.py $(basename $(pwd))`

#### 2.3 CLAUDE.md (Auto-Generated)

**File:** `CLAUDE.md`

> **Note:** This file is auto-generated from AGENTS.md. Do not edit directly - your changes will be overwritten. Edit AGENTS.md instead.

After running sync, CLAUDE.md will contain your AGENTS.md content with a Claude-specific header.

#### 2.4 .cursorrules (Auto-Generated)

**File:** `.cursorrules`

> **Note:** This file is auto-generated from AGENTS.md. Do not edit directly - your changes will be overwritten. Edit AGENTS.md instead.

After running sync, .cursorrules will contain your AGENTS.md content with a Cursor-specific header.

#### 2.5 README.md

**File:** `README.md`

- [ ] Update project name and description
- [ ] Add quick start instructions
- [ ] List key features/goals

---

### Phase 3: Project Setup (5-10 minutes)

```bash
# For Python projects
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # if you have one

# For Node projects
npm init -y
npm install

# Create .env.example (if using APIs)
echo "# API Keys (copy to .env and fill in)" > .env.example
echo "PROJECT_API_KEY=" >> .env.example
```

**Checklist:**
- [ ] Virtual environment created (venv/ in project root)
- [ ] Dependencies installed
- [ ] `.env.example` created (if using external services)

---

### Phase 4: First Commit

```bash
git add -A
git commit -m "Initial commit: Project scaffolded from project-scaffolding

- Added project index (00_Index_*.md)
- Configured AI collaboration files (AGENTS.md, CLAUDE.md, .cursorrules)
- Set up Documents/ structure
- Ready for development"
```

**Checklist:**
- [ ] All files staged
- [ ] Initial commit created
- [ ] Verify: `ls -la 00_Index_*.md` shows your index file

---

### Phase 5: Start Building

You're ready! Use the tiered AI planning approach:

1. **Phase 1 Planning (Tier 1):** Chat with Claude/GPT-4 about your big idea
2. **Task Tiering:** Break tasks into Tier 1/2/3 based on complexity
3. **Execute:** Start with Tier 3 boilerplate, then Tier 2 features

---

### Phase 6: Validation and Code Review

Once your project is set up, use the scaffolding's validation and review infrastructure to ensure quality.

#### Validate Your Project Structure

**Command:**
```bash
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**What it checks:**
- ✅ Required files present (00_Index_*.md, AGENTS.md, CLAUDE.md, .cursorrules, etc.)
- ✅ Project index has valid YAML frontmatter and required sections
- ✅ **DNA Integrity:** No hardcoded absolute paths (`[absolute_path]/...`, `/home/...`)
- ✅ **Security:** No exposed secrets (API keys like `sk-...`, `AIza...`)
- ✅ Mandatory directories exist (Documents/, etc.)

**Example output (clean project):**
```bash
✅ my-new-project (Fully Compliant)
```

**Example output (issues found):**
```bash
⚠️ my-new-project
   - Missing mandatory file: .cursorrules
   - DNA Defect: Absolute path found in scripts/helper.py
```

**Fix issues and re-run validation until clean.**

---

#### Request Code Reviews
When you're ready for architectural review, security audit, or performance analysis:

**Step 1: Create review request**
```bash
# Use the template
cp "$SCAFFOLDING/templates/CODE_REVIEW.md.template" ./CODE_REVIEW_REQUEST.md

# Edit CODE_REVIEW_REQUEST.md:
# - Fill out "Definition of Done" section (what makes this code "done"?)
# - Describe what you want reviewed
# - Specify review focus (architecture/security/performance)
```

**Step 2: Run multi-AI review**
```bash
cd "$SCAFFOLDING"
source venv/bin/activate
doppler run -- python scaffold_cli.py review --type document --input /path/to/your/CODE_REVIEW_REQUEST.md --round 1
```

**Step 3: Review results**
- Reviews saved to: `$SCAFFOLDING/review_outputs/round_1/CODE_REVIEW_*.md`
- Cost summary: `$SCAFFOLDING/review_outputs/round_1/COST_SUMMARY.json`

**Step 4: Archive in your project**
```bash
# Copy the most relevant review to your project
cp "$SCAFFOLDING/review_outputs/round_1/CODE_REVIEW_CLAUDE_SONNET.md" \
   ./Documents/archives/reviews/
```

---

#### Ongoing Validation During Development

Run validation periodically as you build:

```bash
# Quick check (< 1 second)
doppler run -- python "$SCAFFOLDING/scripts/warden_audit.py" --root . --fast

# Full validation
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**Best practice:** Validate before major commits or before requesting code reviews.

---

#### Learn More About Code Review System

- **Full Protocol:** `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Pattern Documentation:** `$SCAFFOLDING/patterns/code-review-standard.md`
- **Review Prompts:** `$SCAFFOLDING/prompts/active/document_review/` (architecture, security, performance)
- **Multi-AI Orchestrator:** `$SCAFFOLDING/scaffold/review.py` (supports OpenAI, Anthropic, DeepSeek, Ollama)

**Key principle:** The review system is centralized in `project-scaffolding` to maintain consistency across all your projects. Projects reference and use it via `$SCAFFOLDING` commands.

---

## Existing Project Checklist

### ⚠️ CRITICAL: This is a Multi-Turn, Interactive Process

**DO NOT immediately start copying files or moving things around.**

Scaffolding an existing project requires **deep understanding first**. This is NOT a one-shot execution - it's a dialogue with multiple Q&A sessions before any changes are made.

**The Goal:** Thoughtfully enhance an existing project with scaffolding patterns. **NEVER break what's already working.**

---

### Workflow Overview

| Phase | Action | Output | Approval |
|-------|--------|--------|----------|
| **1. Deep Research** | Explore and understand the existing project | Research Report | — |
| **2. Q&A Session** | Present findings, ask clarifying questions | Answers from human | **Interactive** |
| **3. Scaffolding Analysis** | Compare project to scaffolding patterns | Fit Analysis | — |
| **4. Proposal** | Recommend changes with reasoning and risks | Proposal Document | **Human approval required** |
| **5. Execute** | Make changes incrementally with safety checks | Modified files | — |
| **6. Verify** | Confirm nothing broke | Verification report | — |

---

### 🚨 Red Flags - STOP If You See These

During ANY phase, **stop and ask** if you encounter:

- ❌ **Absolute paths** in your proposed changes (e.g., `[absolute_path]/...`) - This violates scaffolding principles
- ❌ **Overwriting files** that have significant custom content
- ❌ **Moving files** without understanding why they're where they are
- ❌ **Breaking imports** or file references
- ❌ **Conflicting conventions** you don't understand
- ❌ **Missing context** about why something exists

**When in doubt, ASK. Don't assume.**

---

### Phase 1: Deep Project Research

**Do NOT rely on README alone** - many projects won't have one, or it may be outdated.

**Explore the actual project:**

```bash
# 1. Understand the structure
ls -la
tree -L 2 -d  # or: find . -type d -maxdepth 2

# 2. Identify the tech stack
ls *.py *.js *.ts *.go 2>/dev/null  # What language?
cat requirements.txt package.json go.mod 2>/dev/null | head -20  # Dependencies?

# 3. Look for existing patterns
ls -la *.md  # What docs exist?
ls -la .* 2>/dev/null  # Hidden config files?
head -50 README.md 2>/dev/null  # If README exists

# 4. Check for existing AI collaboration files
ls -la AGENTS.md CLAUDE.md .cursorrules 00_Index_*.md 2>/dev/null
```

**Create a Research Report:**

```markdown
## Project Research Report: [ProjectName]

### What This Project Does
[Your understanding based on exploration - code, config, structure]

### Tech Stack
- Language: [Python/Node/Go/etc.]
- Framework: [If identifiable]
- Dependencies: [Key ones]

### Current Structure
[Describe the directory layout and what each part does]

### Existing Conventions
- Documentation: [Where do they keep docs? What format?]
- Configuration: [How is config handled?]
- Code organization: [src/ vs flat? modules?]

### Skills & Continuous Learning
- [ ] Does this project have reusable AI instructions (skills)?
- [ ] Are skills managed per-project, in a shared library, or both?
- [ ] Is there a learning loop for capturing what works?

### What I Don't Understand Yet
[List things you need clarification on]
```bash

**STOP HERE.** Present this report and wait for feedback before proceeding.

---

### Phase 2: Q&A Session

**This is interactive.** Present your research and ask questions:

**Questions to ask:**
- "I see [X pattern] - is this intentional? Should I preserve it?"
- "The project uses [convention] which differs from scaffolding - should I adapt?"
- "I don't understand why [thing] is structured this way - can you explain?"
- "What are the goals for this project? What problems are you trying to solve?"
- "Are there any parts of the project that are fragile or shouldn't be touched?"

**Wait for answers.** Do not proceed until you have the context you need.

---

### Phase 3: Scaffolding Analysis

**Now** compare the project to scaffolding patterns:

```markdown
## Scaffolding Fit Analysis: [ProjectName]

### Patterns That Apply Directly
| Pattern | Why It Fits | How to Apply |
|---------|-------------|--------------|
| [Pattern] | [Reason] | [Specific approach] |

### Patterns That Need Adaptation
| Pattern | Conflict | Proposed Adaptation |
|---------|----------|---------------------|
| [Pattern] | [What conflicts] | [How to adapt] |

### Patterns to Skip
| Pattern | Why Skip |
|---------|----------|
| [Pattern] | [Reason - doesn't apply, already handled, etc.] |

### Potential Pitfalls
- ⚠️ [Risk 1 and how to mitigate]
- ⚠️ [Risk 2 and how to mitigate]

### Files That Will Be Affected
- New: [files to create]
- Modified: [files to change - explain what changes]
- Moved: [files to relocate - explain why]
- Unchanged: [files to leave alone]
```bash

---

### Phase 4: Proposal (Get Approval)

**Create a specific, reasoned proposal:**

```markdown
## Scaffolding Proposal for [ProjectName]

### Recommended Changes

#### 1. [Change Category]
**What:** [Specific change]
**Why:** [Reasoning]
**Risk:** [Low/Medium/High] - [Explanation]

#### 2. [Next Change]
...

### Questions Requiring Your Decision
1. [Question needing human judgment]
2. [Another question]

### Safety Checklist (I Have Verified)
- [ ] No absolute paths in any proposed files
- [ ] No overwriting of files with significant custom content
- [ ] All file moves have clear reasoning
- [ ] Import paths / references will not break
- [ ] Proposed changes align with project's existing conventions where possible

### Awaiting your approval before proceeding.
```bash

**Only proceed after explicit approval.**

---

### Phase 5: Execute (Incrementally)

**Only after approval. Make changes one category at a time.**

**Step 5.1: Add missing scaffolding files**

```bash
# Set scaffolding path
export SCAFFOLDING="$PROJECTS_ROOT/project-scaffolding"

# Project Index (MANDATORY if missing)
[[ ! -f 00_Index_*.md ]] && \
  cp "$SCAFFOLDING/templates/00_Index.md.template" \
  "./00_Index_$(basename $(pwd)).md"

# AI collaboration files (if missing)
[[ ! -f AGENTS.md ]] && cp "$SCAFFOLDING/templates/AGENTS.md.template" ./AGENTS.md
[[ ! -f CLAUDE.md ]] && cp "$SCAFFOLDING/templates/CLAUDE.md.template" ./CLAUDE.md
[[ ! -f .cursorrules ]] && cp "$SCAFFOLDING/templates/.cursorrules-template" ./.cursorrules
[[ ! -f .cursorignore ]] && cp "$SCAFFOLDING/templates/.cursorignore.template" ./.cursorignore

# Documentation structure (if missing AND approved)
[[ ! -d Documents ]] && cp -r "$SCAFFOLDING/templates/Documents" ./Documents

# Task tracking (if missing)
[[ ! -f TODO.md ]] && cp "$SCAFFOLDING/templates/TODO.md.template" ./TODO.md
```bash

**Step 5.2: Customize each file for the project**

| File | Customization Required |
|------|------------------------|
| `00_Index_*.md` | 3-sentence summary, key components, tags |
| `AGENTS.md` | Tech stack, run/test commands, constraints |
| `CLAUDE.md` | Project structure, safety rules (🔴🟡✅), validation commands |
| `.cursorrules` | Project description, tech stack, constraints |

**Step 5.3: After EACH change, verify**
- Does the project still work?
- Did we introduce any absolute paths?
- Are imports/references still valid?

---

### Phase 6: Verify Nothing Broke

**Run project tests (if they exist):**
```bash
# Python
pytest tests/ 2>/dev/null || python -m pytest 2>/dev/null

# Node
npm test 2>/dev/null

# Or whatever the project uses
```bash

**Check for scaffolding violations in YOUR changes:**
```bash
# Did we accidentally add absolute paths?
grep -r "/Users/" . --include="*.md" --include="*.py" --include="*.json" 2>/dev/null

# Did we add any API keys?
grep -rE "(sk-|AIza|AKIA)" . --include="*.md" --include="*.py" 2>/dev/null
```bash

**Verify checklist:**
- [ ] Project runs/builds as before
- [ ] No absolute paths introduced
- [ ] No secrets exposed
- [ ] Existing functionality preserved
- [ ] Document any existing patterns/conventions

---

### Phase 7: Commit the Scaffolding

```bash
git add -A
git commit -m "Add project scaffolding structure

- Added project index (00_Index_*.md)
- Added AI collaboration files (AGENTS.md, CLAUDE.md, .cursorrules)
- Standardized documentation structure
- Project enhanced with scaffolding patterns"
```bash

---

## Documents/ Structure Reference

When adding `Documents/` to a project:

```
Documents/
├── README.md              # Docs index (Grand Central Station)
├── ARCHITECTURE.md        # Core: System design (at root for visibility!)
├── OPERATIONS.md          # Core: How to run/deploy (at root!)
├── CODE_QUALITY_STANDARDS.md  # Core: Coding rules (at root!)
├── guides/                # How-to documents  
├── reference/             # Standards, knowledge base
├── safety/                # Safety systems
└── archives/              # Historical docs
    ├── reviews/           # Code review history
    └── sessions/          # Session notes
```bash

**IMPORTANT:** Core documents (Architecture, Operations, Standards) go **at the Documents/ root level**, NOT in a `core/` subdirectory. This makes them immediately visible and discoverable.

---

## What's Included

### Templates (`templates/`)

| Template | Purpose |
|----------|---------|
| `00_Index.md.template` | Project index for Obsidian discovery |
| `AGENTS.md.template` | AI source of truth (DoD, constraints) |
| `CLAUDE.md.template` | AI working instructions & safety rules |
| `.cursorrules-template` | Cursor IDE configuration |
| `.cursorignore.template` | Context window optimization |
| `Documents/` | Standard documentation structure |
| `README.md.template` | Project overview |
| `TODO.md.template` | Task tracking format |
| `CODE_REVIEW.md.template` | Code review request format |
| `TIERED_SPRINT_PLANNER.md` | Sprint planning template |

### Patterns (`patterns/`)

| Pattern | What It Teaches |
|---------|-----------------|
| `safety-systems.md` | Data protection patterns (append-only, atomic writes) |
| `development-philosophy.md` | Layer-by-layer, data before decisions |
| `tiered-ai-sprint-planning.md` | Cost-effective AI usage (Tier 1/2/3) |
| `learning-loop-pattern.md` | **How to create reinforcement learning cycles** |
| `code-review-standard.md` | Multi-AI review process |
| `api-key-management.md` | Per-project API key strategy |
| `ssot-via-yaml.md` | Single source of truth patterns |

### Self-Learning Projects (Skills Management)

This scaffolding promotes projects that improve over time. Skills (reusable AI instructions) can live:

| Approach | Best For | Location |
|----------|----------|----------|
| **Shared library** | Cross-project patterns | `$PROJECTS_ROOT/agent-skills-library/` |
| **Per-project** | Project-specific patterns | Within `.cursorrules` or `CLAUDE.md` |
| **Both** | Mature ecosystems | Shared + project-specific |

**Recommendation:** Start with per-project skills. Extract to a shared library when you copy the same instructions across 3+ projects.

See `patterns/learning-loop-pattern.md` for establishing feedback cycles.

### Key Documents (`Documents/`)

| Document | Purpose |
|----------|---------|
| `PROJECT_KICKOFF_GUIDE.md` | Detailed guide for starting new projects |
| `PROJECT_STRUCTURE_STANDARDS.md` | Directory structure conventions |
| `CODE_QUALITY_STANDARDS.md` | Coding standards (MANDATORY) |
| `guides/USAGE_GUIDE.md` | How to use this scaffolding |

---

## Quick Reference Commands

### Validate a Project
```bash
python "$SCAFFOLDING/scripts/validate_project.py" /path/to/project
```bash

### Run Multi-AI Review
```bash
cd "$SCAFFOLDING"
source venv/bin/activate
python scaffold_cli.py review --type document --input /path/to/doc.md --round 1
```bash

### Archive Old Reviews
```bash
python "$SCAFFOLDING/scripts/archive_reviews.py" /path/to/project
```bash

---

## Troubleshooting

### "I don't have PROJECTS_ROOT set"

Add to your `~/.zshrc`:
```bash
export PROJECTS_ROOT="/Users/yourusername/projects"
export SCAFFOLDING="$PROJECTS_ROOT/project-scaffolding"
```

### "Validation is failing"

Common issues:
1. **Missing index file:** Create `00_Index_[ProjectName].md`
2. **Missing YAML frontmatter:** Add tags to index file
3. **Hardcoded paths:** Replace `[absolute_path]/...` with relative paths

### "Which files are absolutely required?"

**MANDATORY for all projects:**
- `00_Index_[ProjectName].md` - Project index
- `AGENTS.md` - AI instructions
- `.cursorrules` - Cursor rules

**MANDATORY for code projects:**
- `requirements.txt` or `package.json` - Dependencies
- `Documents/` - Documentation

---

## Next Steps After Scaffolding

1. **Read** `Documents/PROJECT_KICKOFF_GUIDE.md` for detailed planning workflow
2. **Review** `patterns/development-philosophy.md` to understand the mindset
3. **Plan** using tiered AI approach before coding
4. **Track** external resources in `EXTERNAL_RESOURCES.md` when adding services

---

**Remember:** The scaffolding is a starting point, not a rigid rulebook. Adapt templates to fit your project's needs.

---

*Part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*  
*Last Updated: January 2026*

## Related Documentation

- [CODE_QUALITY_STANDARDS](Documents/CODE_QUALITY_STANDARDS.md) - code standards
- [Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md) - code review
- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - local AI
- [PROJECT_KICKOFF_GUIDE](Documents/PROJECT_KICKOFF_GUIDE.md) - project setup
- [Cost Management](Documents/reference/MODEL_COST_COMPARISON.md) - cost management
- [Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md) - prompt engineering
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [AI Team Orchestration](patterns/ai-team-orchestration.md) - orchestration
- [Safety Systems](patterns/safety-systems.md) - security
- [Agent Skills Library](../agent-skills-library/README.md) - Agent Skills
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
