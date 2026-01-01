---
tags:
  - p/project-scaffolding
  - type/meta-project
  - domain/pattern-extraction
  - status/active
created: 2025-12-31
---

# Project Index Enforcement - Critical Rule #0

**Status:** MANDATORY  
**Priority:** Critical  
**Enforcement:** Automated validation available

---

## 🚨 The Rule

**NO PROJECT GOES FORWARD WITHOUT AN INDEX FILE.**

This is **Critical Rule #0** in `docs/CODE_QUALITY_STANDARDS.md` - it comes before even "no silent failures."

---

## Why This Is Non-Negotiable

### The Problem We Had
- **36 projects** with no consistent documentation
- **No way to find** what we're looking for
- **Forgotten context** - "What does this project do again?"
- **Duplicate work** - Didn't know similar project existed
- **No organization** - Can't filter or search effectively
- **Lost knowledge** - Tech decisions and architecture undocumented

### The Pain
- Hours wasted re-learning projects
- Duplicated efforts
- No visibility into project health
- Can't prioritize effectively
- New AI collaborators can't orient themselves

### The Solution
**Every project must have `00_Index_[ProjectName].md` in its root.**

This single file provides:
- 3-sentence summary (instant understanding)
- Key components (know what's in it)
- Status tags (active? archived?)
- Tech stack (Python? TypeScript?)
- Dataview integration (search & filter)

---

## Enforcement Mechanisms

### 1. Documentation (✅ Complete)

**Updated Files:**
- `docs/CODE_QUALITY_STANDARDS.md` - Made indexing Critical Rule #0
- `docs/PROJECT_KICKOFF_GUIDE.md` - Added as mandatory Step 3
- `docs/PROJECT_INDEXING_SYSTEM.md` - Complete indexing guide
- `templates/00_Index_Template.md` - Template for new projects

### 2. Validation Scripts (✅ Complete)

**Created:**
- `scripts/validate_project.py` - Check if projects have valid indexes
- `scripts/reindex_projects.py` - Create/update indexes automatically

**Usage:**
```bash
# Check specific project
./scripts/validate_project.py image-workflow

# Check all projects
./scripts/validate_project.py --all

# List missing indexes
./scripts/validate_project.py --missing

# Create missing indexes
./scripts/reindex_projects.py --missing

# Update stale indexes (>6 months old)
./scripts/reindex_projects.py --stale
```

### 3. Project Kickoff Process (✅ Updated)

**New projects must:**
1. Copy structure from project-scaffolding
2. Edit templates (.cursorrules, CLAUDE.md)
3. **CREATE INDEX FILE** ← MANDATORY STEP
4. Initialize git and commit

**Can't skip Step 3.** No exceptions.

### 4. Git Pre-Commit Hook (Optional)

Add to `.git/hooks/pre-commit` in project:
```bash
#!/bin/bash
# Check for index file
if [ ! -f 00_Index_*.md ]; then
  echo "❌ ERROR: Missing project index file"
  echo "Required: 00_Index_[ProjectName].md"
  echo "Template: project-scaffolding/templates/00_Index_Template.md"
  exit 1
fi
```

### 5. _inbox Policy (New)

**Rule:** Projects stay in `_inbox/` until they have an index.

**Process:**
1. Start experiment in `_inbox/`
2. When it becomes a real project:
   - Create index file
   - Move to main projects folder
   - Add to git

**_inbox/ is for experiments. Main projects/ is for indexed projects only.**

---

## Validation Script Details

### validate_project.py

**What it checks:**
- Index file exists (00_Index_*.md)
- YAML frontmatter present
- Required tags included (map/project, p/[name])
- Required sections present (H1 title, Key Components, Status)
- Minimum content (3-sentence summary)

**Output:**
```bash
$ ./scripts/validate_project.py --all

✅ image-workflow
   Index: 00_Index_image-workflow.md

❌ new-project
   ERROR: Missing index file (00_Index_*.md)
   Create one: cp templates/00_Index_Template.md "new-project/00_Index_new-project.md"

⚠️  old-project
   Index exists: 00_Index_old-project.md
   - Missing required section: ## Key Components
   - Summary section appears too short

========================================
Summary: 13/15 projects valid (2 need attention)
```

### reindex_projects.py

**What it does:**
- Scans project structure
- Detects primary technology (.py → python, .ts → typescript)
- Determines status (>6 months = archived)
- Counts files in major directories
- Generates index from template

**Usage scenarios:**
```bash
# Create indexes for projects that don't have them
./scripts/reindex_projects.py --missing

# Update indexes that are >6 months old
./scripts/reindex_projects.py --stale

# Re-index specific project
./scripts/reindex_projects.py image-workflow

# Recreate ALL indexes (destructive!)
./scripts/reindex_projects.py --all
```

---

## Current Status

### Index Files Created (14/36)
- ✅ All production systems (8/8) - 100%
- ✅ Major active projects (6/12) - 50%
- ⚪ Planning/experimental (0/10) - 0%
- ⚪ Archived (0/6) - 0%

### Next Steps
```bash
# Create remaining indexes
cd /Users/eriksjaastad/projects/project-scaffolding
./scripts/reindex_projects.py --missing

# This will create 22 new index files automatically
```

---

## Integration Points

### With Obsidian Vault
- All indexes tagged `#map/project`
- Enables Dataview queries
- Graph view shows relationships
- Wikilinks enable navigation

### With Project Tracker
- Can cross-reference status
- Detect drift (tracker vs index)
- Health monitoring

### With AI Collaborators
- Quick project orientation
- Understand tech stack instantly
- See what components exist
- Know if project is active or archived

---

## Examples of Good Indexes

### Production System
```markdown
# image-workflow

High-volume image processing pipeline that handles 10,000+ images per day 
through multiple quality control passes. This production system processes 
5,000-7,000 real people images plus 4,500 AI-generated images daily, with 
comprehensive safety systems and disaster recovery built from 2.5+ months 
of battle-testing.

## Key Components
- `scripts/` - Core processing (237 Python files)
- `Documents/` - Documentation (178 MD files)
- Web dashboard for progress tracking

## Status
**Tags:** #map/project #p/image-workflow
**Status:** #status/active #status/production
**Last Major Update:** December 2025
**Priority:** #mission-critical #high-volume
```

### Experimental Project
```markdown
# ai-model-testing

Model evaluation and benchmarking experiments for comparing AI performance 
across tasks. This experimental project tests various prompting strategies 
and model configurations to identify optimal approaches. Currently in 
exploratory phase with minimal structure.

## Key Components
- Test scripts and notebooks
- Results data
- Analysis docs

## Status
**Tags:** #map/project #p/ai-model-testing
**Status:** #status/experimental
**Last Major Update:** 2025
```

---

## Consequences of Non-Compliance

### For New Projects
- **Can't move out of _inbox/** - Projects without indexes stay experimental
- **No git commits** - Pre-commit hook (if installed) blocks commits
- **Validation fails** - Can't pass quality checks
- **Not discoverable** - Won't show up in Obsidian searches

### For Existing Projects
- **Flagged by validation** - `validate_project.py --all` reports them
- **Can't track status** - No way to know if active or abandoned
- **Lost in the noise** - 36 projects become unmanageable
- **Duplicate work** - Team doesn't know project exists

---

## Maintenance Schedule

### Weekly
- No action needed (indexes created on project creation)

### Monthly
- Run `./scripts/validate_project.py --all`
- Fix any validation errors
- Update indexes if projects evolved significantly

### Quarterly
- Run `./scripts/reindex_projects.py --stale`
- Review archived projects (consider cleanup)
- Update status tags (active → production, active → archived)

### Annually
- Full re-index: `./scripts/reindex_projects.py --all`
- Review all 3-sentence summaries
- Update tech stack if changed
- Archive dormant projects

---

## FAQ

### "Do I really need this for small experiments?"
**Yes, but use _inbox/ first.** Small experiments start in `_inbox/`. When they become real projects, create an index and move to main folder.

### "What if I don't know what the project will be yet?"
**Use the template and fill in what you know.** Even "This project explores [topic]" is better than nothing. Update as you learn.

### "Can I skip this for quick scripts?"
**Quick scripts stay in _tools/ or _inbox/.** They don't need indexes. Only projects that live in the main folder need indexes.

### "What if my index gets out of date?"
**Update it!** That's the point. When you add major features, update the index. Think of it as a living document.

### "Is 3 sentences really enough?"
**Yes.** Anyone reading should understand: (1) What it does, (2) How it works, (3) Current status. That's enough to decide if they need to dig deeper.

### "Can automation create these?"
**Yes!** That's what `reindex_projects.py` does. It scans structure, detects tech, determines status, and generates the file. You can still edit it afterward.

---

## Success Metrics

### Before (Pre-Indexing)
- ❌ No way to find projects
- ❌ Forgot what projects do
- ❌ Duplicate work
- ❌ No status visibility
- ❌ Can't organize or prioritize

### After (With Indexes)
- ✅ Instant project discovery
- ✅ Clear 3-sentence summaries
- ✅ Status at a glance
- ✅ Tech stack visible
- ✅ Dataview queries work
- ✅ Graph view shows relationships
- ✅ AI collaborators can orient themselves

---

## Commands Cheat Sheet

```bash
# Validate specific project
./scripts/validate_project.py [project-name]

# Validate all projects
./scripts/validate_project.py --all

# List projects without indexes
./scripts/validate_project.py --missing

# Create missing indexes (auto-generate)
./scripts/reindex_projects.py --missing

# Update stale indexes (>6 months)
./scripts/reindex_projects.py --stale

# Re-index specific project
./scripts/reindex_projects.py [project-name]

# Copy template for new project
cp templates/00_Index_Template.md "../[ProjectName]/00_Index_[ProjectName].md"
```

---

## Bottom Line

**This is not optional.** Project indexing is now a core requirement, enforced through:
1. Documentation (Critical Rule #0)
2. Process (mandatory Step 3 in kickoff)
3. Tooling (validation + auto-generation scripts)
4. Policy (_inbox/ vs. main projects/)

**No project goes forward without an index file.**

---

**Established:** 2025-12-31  
**Enforcement:** Active  
**Status:** MANDATORY  
**Scripts:** Validated and ready to use

