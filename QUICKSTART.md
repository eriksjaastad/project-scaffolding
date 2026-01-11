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

# 2. Copy all templates
cp -r "$SCAFFOLDING/templates/Documents" ./Documents
cp "$SCAFFOLDING/templates/AGENTS.md.template" ./AGENTS.md
cp "$SCAFFOLDING/templates/CLAUDE.md.template" ./CLAUDE.md
cp "$SCAFFOLDING/templates/.cursorrules-template" ./.cursorrules
cp "$SCAFFOLDING/templates/.cursorignore.template" ./.cursorignore
cp "$SCAFFOLDING/templates/TODO.md.template" ./TODO.md
cp "$SCAFFOLDING/templates/README.md.template" ./README.md
cp "$SCAFFOLDING/templates/.gitignore" ./.gitignore
cp "$SCAFFOLDING/templates/00_Index_Template.md" "./00_Index_$(basename $NEW_PROJECT).md"

# 3. Initialize git
git init
```

**Checklist:**
- [ ] Project directory created
- [ ] Templates copied from scaffolding
- [ ] Git initialized

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

- [ ] Replace `{project_description}` with clear summary
- [ ] Update `{language}`, `{frameworks}`, `{ai_strategy}`
- [ ] Set `{run_command}` and `{test_command}`
- [ ] Add project-specific constraints
- [ ] Update Definition of Done checklist

#### 2.3 CLAUDE.md (AI Working Instructions)

**File:** `CLAUDE.md`

- [ ] Write project summary (2-3 sentences)
- [ ] Update current status
- [ ] Specify key constraints (budget, privacy, etc.)
- [ ] Update project structure diagram
- [ ] Define Safety Rules:
  - 🔴 NEVER modify (append-only/read-only files)
  - 🟡 Be careful with (config, APIs)
  - ✅ Safe to modify (code, docs)
- [ ] Add validation commands

#### 2.4 .cursorrules (Cursor AI Rules)

**File:** `.cursorrules`

- [ ] Replace `[PROJECT_NAME]` with project name
- [ ] Write 1-2 sentence description
- [ ] Set domain and status
- [ ] Update tech stack
- [ ] Add project-specific constraints
- [ ] Update execution commands

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

**Reference:** `Documents/PROJECT_KICKOFF_GUIDE.md` for detailed planning workflow

---

## Existing Project Checklist

### Prerequisites

```bash
# Navigate to your project
cd /path/to/your/existing-project

# Set scaffolding path
export SCAFFOLDING="$PROJECTS_ROOT/project-scaffolding"
```

---

### Phase 1: Assess Current State (5 minutes)

**Check what you already have:**

```bash
# Check for existing files
ls -la AGENTS.md CLAUDE.md .cursorrules README.md TODO.md 2>/dev/null
ls -la 00_Index_*.md 2>/dev/null
ls -d Documents 2>/dev/null
```

**Checklist - What's Missing?**
- [ ] `00_Index_[ProjectName].md` - Project index (MANDATORY)
- [ ] `AGENTS.md` - AI source of truth
- [ ] `CLAUDE.md` - AI working instructions
- [ ] `.cursorrules` - Cursor AI rules
- [ ] `.cursorignore` - Context window filtering
- [ ] `Documents/` - Documentation structure
- [ ] `TODO.md` - Task tracking
- [ ] `.gitignore` - Git ignore rules

---

### Phase 2: Add Missing Core Files (10-15 minutes)

**Copy only what you need:**

```bash
# Project Index (MANDATORY if missing)
[[ ! -f 00_Index_*.md ]] && \
  cp "$SCAFFOLDING/templates/00_Index_Template.md" \
  "./00_Index_$(basename $(pwd)).md"

# AGENTS.md (if missing)
[[ ! -f AGENTS.md ]] && \
  cp "$SCAFFOLDING/templates/AGENTS.md.template" ./AGENTS.md

# CLAUDE.md (if missing)
[[ ! -f CLAUDE.md ]] && \
  cp "$SCAFFOLDING/templates/CLAUDE.md.template" ./CLAUDE.md

# .cursorrules (if missing)
[[ ! -f .cursorrules ]] && \
  cp "$SCAFFOLDING/templates/.cursorrules-template" ./.cursorrules

# .cursorignore (if missing)
[[ ! -f .cursorignore ]] && \
  cp "$SCAFFOLDING/templates/.cursorignore.template" ./.cursorignore

# Documents structure (if missing)
[[ ! -d Documents ]] && \
  cp -r "$SCAFFOLDING/templates/Documents" ./Documents

# TODO.md (if missing)
[[ ! -f TODO.md ]] && \
  cp "$SCAFFOLDING/templates/TODO.md.template" ./TODO.md
```

---

### Phase 3: Customize for Your Project (15-20 minutes)

**Priority order - do these first:**

#### 3.1 Project Index (HIGHEST PRIORITY)

**File:** `00_Index_[YourProject].md`

This is MANDATORY. No project is complete without it.

- [ ] Write 3-sentence summary of your existing project
- [ ] List your actual key components/directories
- [ ] Update tags to match your project
- [ ] Set correct status tag

#### 3.2 AGENTS.md

Adapt the template to describe your existing project:

- [ ] Replace placeholders with your actual tech stack
- [ ] Update run/test commands for your project
- [ ] Add any existing constraints or rules you follow
- [ ] Keep what's working, add what's missing

#### 3.3 CLAUDE.md

This tells AI how to work on YOUR project:

- [ ] Document your existing project structure
- [ ] List files that should NEVER be modified
- [ ] List files that need careful handling
- [ ] Add your validation commands (tests, linting)
- [ ] Document any existing patterns/conventions

#### 3.4 .cursorrules

- [ ] Describe what your project actually does
- [ ] List your actual tech stack
- [ ] Add project-specific constraints
- [ ] Reference your existing documentation

---

### Phase 4: Add Documents Structure (if needed)

If you don't have a `Documents/` directory:

```bash
# The template was already copied in Phase 2
# Now organize your existing docs

# Move existing documentation to Documents/
# Example:
# mv architecture.md Documents/ARCHITECTURE.md
# mv operations.md Documents/OPERATIONS.md
# mv SETUP.md Documents/guides/
```

**Standard Documents/ structure:**
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
```

**IMPORTANT:** Core documents (Architecture, Operations, Standards) go **at the Documents/ root level**, NOT in a `core/` subdirectory. This makes them immediately visible and discoverable.

---

### Phase 5: Verify Structure

Run the project validator:

```bash
python "$SCAFFOLDING/scripts/validate_project.py" .
```

**Or manually verify:**
- [ ] `00_Index_*.md` exists and has YAML frontmatter
- [ ] `AGENTS.md` exists with project-specific content
- [ ] `CLAUDE.md` exists with safety rules defined
- [ ] `.cursorrules` exists and is customized
- [ ] `Documents/` directory exists
- [ ] No hardcoded absolute paths in files
- [ ] No API keys in committed files

---

### Phase 6: Commit the Scaffolding

```bash
git add -A
git commit -m "Add project scaffolding structure

- Added project index (00_Index_*.md)
- Added AI collaboration files (AGENTS.md, CLAUDE.md, .cursorrules)
- Added Documents/ structure for documentation
- Standardized project structure for AI collaboration"
```

---

## What's Included

### Templates (`templates/`)

| Template | Purpose |
|----------|---------|
| `00_Index_Template.md` | Project index for Obsidian discovery |
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
| `code-review-standard.md` | Multi-AI review process |
| `api-key-management.md` | Per-project API key strategy |
| `ssot-via-yaml.md` | Single source of truth patterns |

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
```

### Run Multi-AI Review
```bash
cd "$SCAFFOLDING"
source venv/bin/activate
python scaffold_cli.py review --type document --input /path/to/doc.md --round 1
```

### Archive Old Reviews
```bash
python "$SCAFFOLDING/scripts/archive_reviews.py" /path/to/project
```

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
3. **Hardcoded paths:** Replace `/Users/...` with relative paths

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
