---
tags:
  - p/project-scaffolding
  - type/meta-project
  - domain/pattern-extraction
  - status/active
  - tech/python
created: 2025-12-31
---

# Project Indexing System

**Purpose:** Automated project discovery and index file generation for Obsidian vault navigation.

---

## Overview

This system automatically creates and maintains `00_Index_[ProjectName].md` files in each project folder, providing:
- **Quick project summaries** (3 sentences)
- **Key components** listing (main files/directories)
- **Dataview-compatible tags** for Obsidian filtering
- **Auto-detected status** based on recent activity

---

## Index File Structure

### Template Format
```markdown
---
tags:
  - map/project
  - p/[project-name]
  - type/[project-type]
  - domain/[domain]
  - status/[active|archived]
  - tech/[primary-tech]
created: YYYY-MM-DD
---

# Project Name

[3-sentence summary: What it does. Key technologies. Current status.]

## Key Components

### [Section Name]
- `directory/` - Description ([X] files)
  - Key file 1
  - Key file 2

[Repeat for major components]

## Status

**Tags:** #map/project #p/[project-name]
**Status:** #status/[active|archived]
**Last Major Update:** [Date or period]
[Additional context]
```

---

## Status Detection Logic

### Active Projects
**Criteria:** Last edit within 6 months
- `#status/active` - Currently being developed
- `#status/production` - Live, in use

### Archived Projects
**Criteria:** No edits in 6+ months
- `#status/archived` - Dormant but preserved
- `#status/complete` - Finished, no longer changing

---

## Re-Indexing Process

### Manual Re-Index (Current Method)

1. **Review project folder**
   ```bash
   ls -lt $PROJECTS_ROOT/[ProjectName]/
   ```

2. **Check last modification**
   ```bash
   find $PROJECTS_ROOT/[ProjectName]/ \
     -type f -not -path "*/\.*" -exec stat -f "%m %N" {} \; | \
     sort -rn | head -1
   ```

3. **Update index file**
   - Revise 3-sentence summary if project evolved
   - Add new key components
   - Update status tag based on activity
   - Update "Last Major Update" date

### Automated Re-Index (Future Script)

**Script:** `scripts/reindex_projects.py`

```python
#!/usr/bin/env python3
"""
Re-index all projects or specific projects.

Usage:
    ./scripts/reindex_projects.py                # All projects
    ./scripts/reindex_projects.py image-workflow # Specific project
    ./scripts/reindex_projects.py --stale        # Only outdated indexes
"""

import os
import datetime
from pathlib import Path

PROJECT_ROOT = Path("$PROJECTS_ROOT")
ARCHIVE_THRESHOLD_DAYS = 180  # 6 months

def get_last_modified(project_path: Path) -> datetime.datetime:
    """Get most recent file modification in project."""
    # Implementation
    pass

def needs_reindex(index_path: Path, project_path: Path) -> bool:
    """Check if index is outdated."""
    if not index_path.exists():
        return True
    
    index_modified = datetime.datetime.fromtimestamp(index_path.stat().st_mtime)
    project_modified = get_last_modified(project_path)
    
    # Re-index if project changed after index was created
    return project_modified > index_modified

def generate_index(project_path: Path) -> str:
    """Generate index content for project."""
    # Scan project structure
    # Detect primary language
    # Count files by type
    # Determine status
    # Generate markdown
    pass

# Implementation...
```

---

## Integration with Project Scaffolding

### 1. New Project Template

**Location:** `templates/00_Index_Template.md`

```markdown
---
tags:
  - map/project
  - p/PROJECT_NAME_HERE
  - type/TYPE_HERE  # ai-agent, pipeline, webapp, etc.
  - domain/DOMAIN_HERE  # image-processing, finance, etc.
  - status/active
  - tech/TECH_HERE  # python, typescript, etc.
created: YYYY-MM-DD
---

# PROJECT_NAME_HERE

[Sentence 1: What this project does.] [Sentence 2: Key technologies and approach.] [Sentence 3: Current status and next steps.]

## Key Components

### Main Components
- `src/` - Core source code
  - Main application files
  - Business logic

### Documentation
- `docs/` - Project documentation
  - Architecture
  - Usage guides

### Configuration
- Config files
- Environment setup

## Status

**Tags:** #map/project #p/PROJECT_NAME_HERE
**Status:** #status/active
**Last Major Update:** [DATE]
```

### 2. Project Kickoff Checklist

**Add to:** `docs/PROJECT_KICKOFF_GUIDE.md`

```markdown
## Step 5: Create Project Index (NEW!)

After initial project setup, create the index file:

1. **Copy template**
   ```bash
   cp templates/00_Index_Template.md \
      "00_Index_[ProjectName].md"
   ```

2. **Fill in details**
   - Project name (H1 title)
   - 3-sentence summary
   - Key components list
   - Update all tags

3. **Place in project root**
   ```bash
   mv "00_Index_[ProjectName].md" \
      $PROJECTS_ROOT/[ProjectName]/
   ```

4. **Commit to Git**
   ```bash
   git add "00_Index_[ProjectName].md"
   git commit -m "Add project index for Obsidian"
   ```
```

### 3. Maintenance Reminder

**Add to:** `patterns/maintenance-checklist.md`

```markdown
## Monthly: Update Project Indexes

- [ ] Run re-index script for stale projects
  ```bash
  cd project-scaffolding
  ./scripts/reindex_projects.py --stale
  ```

- [ ] Review changed indexes
- [ ] Update status tags if projects archived
- [ ] Commit updated indexes
```

---

## Benefits

### For Discovery
✅ **Quick orientation** - 3-sentence summary tells you what project does  
✅ **Component overview** - Know what's in the project without exploring  
✅ **Status clarity** - See if project is active or archived

### For Obsidian
✅ **Map of Content** - All projects tagged with `#map/project`  
✅ **Dataview queries** - Filter by status, tech, domain  
✅ **Graph view** - Visual project relationships  
✅ **Automatic linking** - Wikilinks between related projects

### For Project Management
✅ **Health monitoring** - Stale projects become obvious  
✅ **Taxonomy enforcement** - Consistent tagging across all projects  
✅ **Resource tracking** - See which projects use which tech  
✅ **Pattern recognition** - Identify similar projects easily

---

## Example Dataview Queries

### All Active Projects
```dataview
TABLE status, tech, domain
FROM #map/project
WHERE contains(status, "active")
SORT file.name ASC
```

### Projects by Technology
```dataview
TABLE domain, status
FROM #map/project
WHERE contains(tech, "python")
SORT status ASC
```

### Archived Projects (Candidates for Cleanup)
```dataview
TABLE status, file.mtime as "Last Modified"
FROM #map/project
WHERE contains(status, "archived")
SORT file.mtime ASC
```

### Production Systems
```dataview
TABLE domain, tech
FROM #map/project
WHERE contains(status, "production")
```

---

## Re-Indexing Triggers

### When to Re-Index

1. **Major feature additions** - New components added
2. **Status changes** - Active → Production, Active → Archived
3. **Tech stack changes** - Added/removed major dependencies
4. **Every 3-6 months** - Regular maintenance
5. **Before project retrospectives** - Ensure current state documented

### Quick Check for Staleness

```bash
# Find projects with indexes older than 6 months
find $PROJECTS_ROOT -name "00_Index_*.md" \
  -type f -mtime +180
```

---

## Current Index Files (2025-12-31)

### Production (8 projects)
- [x] image-workflow
- [x] Trading Projects
- [x] Cortana personal AI
- [x] 3D Pose Factory
- [x] AI usage-billing tracker
- [x] hypocrisynow
- [x] project-scaffolding
- [x] AI-journal

### Active Development (6 projects)
- [x] hologram
- [x] agent_os
- [x] agent-skills-library
- [x] Automation Consulting
- [x] Country AI Futures Tracker
- [x] project-tracker

### Pending (~22 projects)
- [ ] Tax processing
- [ ] Smart Invoice Follow-Up
- [ ] Speech-to-text
- [ ] writing
- [ ] Van Build
- [ ] epstien files
- [ ] NationalCattleBrands
- [ ] duplicate-detection
- [ ] find-names-chrome-plugin
- [ ] Flo-Fi
- [ ] SynthInsightLabs
- [ ] AI video-image generation
- [ ] ollama-mcp
- [ ] Portfolio-ai
- [ ] actionable-ai-intel
- [ ] AI agent training lab
- [ ] ai-model-testing
- [ ] analyze-youtube-videos
- [ ] Land
- [ ] Prospector
- [ ] Quake III
- [ ] AI Class

---

## Next Steps

### Immediate
1. **Create template file**
   - Add `templates/00_Index_Template.md`
   - Include in project-scaffolding repo

2. **Update kickoff guide**
   - Add index creation step
   - Link to template

3. **Add to maintenance checklist**
   - Monthly re-index reminder
   - Stale detection command

### Short-term
1. **Build re-index script**
   - Auto-detect status changes
   - Generate component lists
   - Update timestamps

2. **Complete remaining indexes**
   - Create for all 36 projects
   - Start with active projects
   - Archive old/dormant ones

### Long-term
1. **GitHub Action**
   - Auto-check for stale indexes
   - Generate PR with updates
   - Run monthly

2. **Integration with project-tracker**
   - Cross-reference index status
   - Health dashboard
   - Alert on stale indexes

---

## Files to Create/Update

### In project-scaffolding/
- [x] `docs/PROJECT_INDEXING_SYSTEM.md` (this file)
- [ ] `templates/00_Index_Template.md`
- [ ] `scripts/reindex_projects.py`
- [ ] Update `docs/PROJECT_KICKOFF_GUIDE.md`
- [ ] Update `patterns/maintenance-checklist.md`

### In each project/
- [ ] `00_Index_[ProjectName].md`

---

**Created:** 2025-12-31  
**Status:** Documentation complete, tooling pending  
**Priority:** High - improves discoverability across entire ecosystem

