# TODO.md Format Standard

> **Purpose:** Establish consistent TODO format across all Erik's projects  
> **Version:** 1.0  
> **Date:** December 30, 2025  
> **Status:** Proposed (awaiting Erik's approval)

---

## TL;DR

**Every project should have `TODO.md` with:**
1. Header (status, phase, last updated)
2. Current State (what works, what's missing, blockers)
3. Completed Tasks (with dates, keep for progress tracking)
4. Pending Tasks (prioritized: 🔴 🟡 🔵 🟢)
5. Success Criteria (clear "done" definition)
6. Notes (AI agents, cron jobs, costs, related projects)

**Template:** `project-scaffolding/templates/TODO.md.template`

---

## Why This Matters

### The Problem
Analyzed TODO files across 4 projects (Cortana, YouTube analysis, AI Intel, project-scaffolding):
- **Inconsistent structure** - Each project organized differently
- **Missing metadata** - AI agents, cron jobs, blockers not tracked consistently
- **Varying detail levels** - 107 lines to 660 lines
- **Hard to handoff** - New AI sessions struggle to understand state

### The Solution
**Standardized format that:**
- Works for both humans and AI sessions
- Scales from simple to complex projects
- Tracks critical metadata (AI agents, automation, blockers)
- Shows progress (keeps completed tasks)
- Provides context for future sessions

---

## Format Analysis

### What We Learned from Real Projects

#### Cortana Personal AI TODO (660 lines) ✅ EXCELLENT
**Strengths:**
- Very detailed current state (data sources, coverage, costs)
- Excellent layering (Layer 1, 1.5, 2, 3, etc.)
- Clear phase progression with dates
- Comprehensive success criteria per layer
- Rich notes section (cost analysis, time estimates, related projects)
- Intentional pause documented (ethical considerations)

**What we're adopting:**
- Current State section with "What's Working" / "Blockers"
- Success Criteria per phase
- Notes section structure (costs, time, related docs)
- Keeping completed tasks visible (shows progress)

#### analyze-youtube-videos TODO (400 lines) ✅ GOOD
**Strengths:**
- Stage-based breakdown (Stage 1-5)
- Clear decision points ("decide path A/B/C")
- Integration learnings section
- Personal context section (Erik's preferences)
- Test methodology documented

**What we're adopting:**
- Decision points documented
- Integration learnings section
- Personal context when relevant

#### actionable-ai-intel TODO (350 lines) ✅ CLEAR
**Strengths:**
- Blockers upfront (Discord webhook, run time)
- Prerequisites section before tasks
- Phase breakdown with time estimates
- Clear "waiting on" items

**What we're adopting:**
- Blockers & Dependencies section upfront
- Prerequisites clearly marked
- Phase-based organization

#### project-scaffolding TODO (107 lines) ✅ MINIMAL
**Strengths:**
- Very focused and actionable
- Sprint-based organization
- "What Exists & Works" section
- Backlog clearly separated
- Success metrics defined

**What we're adopting:**
- Sprint-based structure (optional)
- Focused, actionable tasks
- Clear backlog separation

---

## Standard Format (Required Sections)

### 1. Header
```markdown
# {{PROJECT_NAME}} - TODO

**Last Updated:** {{DATE}}  
**Project Status:** {{STATUS}}  
**Current Phase:** {{PHASE}}
```

**Purpose:** Quick orientation for anyone opening the file

### 2. Current State
```markdown
## 📍 Current State

### What's Working ✅
- Feature/component that's operational

### What's Missing ❌
- Gap or incomplete feature

### Blockers & Dependencies
- What's stopping progress
```

**Purpose:** Honest assessment of where things are RIGHT NOW

### 3. Completed Tasks
```markdown
## ✅ Completed Tasks

### Phase X: {{NAME}} ({{DATE_RANGE}})
- [x] Task completed
- [x] Another task done
```

**Purpose:** Show progress, provide context, never delete completed work

### 4. Pending Tasks
```markdown
## 📋 Pending Tasks

### 🔴 CRITICAL - Must Do First
- [ ] High-priority task

### 🟡 HIGH PRIORITY
- [ ] Important task

### 🔵 MEDIUM PRIORITY
- [ ] Nice to have

### 🟢 LOW PRIORITY
- [ ] Future backlog
```

**Purpose:** Prioritized work queue, clear what's next

### 5. Success Criteria
```markdown
## 🎯 Success Criteria

### {{PHASE}} Complete When:
- [ ] Measurable criterion
- [ ] Specific outcome

### Project Complete When:
- [ ] Final goal achieved
```

**Purpose:** Define "done", prevent scope creep

### 6. Notes
```markdown
## 📊 Notes

### AI Agents in Use
- **{{AI_NAME}}:** Role

### Cron Jobs / Automation
- **Schedule:** cron expression
- **Command:** what runs

### External Services Used
- **{{SERVICE}}:** Purpose, cost

### Cost Estimates
- Development, monthly, one-time

### Time Estimates
- Per phase, total project

### Related Projects & Documentation
- Links to other relevant work

### Key Decisions Made
- Important choices for future reference

### Open Questions
- Unresolved items
```

**Purpose:** Context for future sessions, metadata for dashboard

---

## Optional Sections

### Change Log
For projects with complex history:
```markdown
## 🔄 Change Log

### {{DATE}} - {{PHASE_NAME}}
- Major milestone
```

### Technical Stack
For new team members or AI sessions:
```markdown
### Technical Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** SQLite
```

### Integration Learnings
For projects testing patterns:
```markdown
### Integration Learnings
✅ What's working:
- Pattern that's successful

🤔 What could be improved:
- Area for enhancement
```

---

## Priority System

### Emoji Legend
- 🔴 **CRITICAL** - Must do first, blocks other work
- 🟡 **HIGH** - Important but not blocking
- 🔵 **MEDIUM** - Nice to have, can wait
- 🟢 **LOW** - Backlog, future consideration

### When to Use Each

**🔴 CRITICAL:**
- Bugs breaking core functionality
- Blockers preventing progress
- Prerequisites for other work
- Security issues

**🟡 HIGH:**
- Core features not yet implemented
- Important integrations
- High-value enhancements
- Documentation gaps

**🔵 MEDIUM:**
- Nice-to-have features
- UI polish
- Performance optimizations
- Non-critical integrations

**🟢 LOW:**
- Future ideas
- Experimental features
- Long-term improvements
- Backlog items

---

## Task Organization Patterns

### Pattern 1: Phase-Based (Cortana style)
Best for: Long-term projects with clear evolution stages

```markdown
### Phase 1: Foundation
- [x] Core setup
- [x] Basic features

### Phase 2: Enhancement
- [ ] Advanced features
- [ ] Integrations
```

### Pattern 2: Sprint-Based (Scaffolding style)
Best for: Agile-style iterative development

```markdown
### Sprint 1: Quick Wins
- [ ] Task 1
- [ ] Task 2

### Sprint 2: Core Features
- [ ] Feature A
- [ ] Feature B
```

### Pattern 3: Stage-Based (YouTube style)
Best for: Sequential pipelines or workflows

```markdown
### Stage 1: Data Collection
- [ ] Download data
- [ ] Parse data

### Stage 2: Analysis
- [ ] Run analysis
- [ ] Generate report
```

### Pattern 4: Category-Based
Best for: Small projects with diverse tasks

```markdown
### Setup
- [ ] Environment
- [ ] Dependencies

### Implementation
- [ ] Feature 1
- [ ] Feature 2
```

**Recommendation:** Choose pattern based on project nature, stay consistent within project

---

## New Metadata Sections (December 2025)

### AI Agents in Use
**Why:** Dashboard will track which AI is helping with what

**Format:**
```markdown
### AI Agents in Use
- **Claude Sonnet 4.5:** Project management and architecture
- **Cursor:** Code implementation and refactoring
- **ChatGPT o1:** Complex problem solving
```

**When to update:**
- AI starts working on project
- AI role changes
- AI finishes work on project

### Cron Jobs / Automation
**Why:** Dashboard needs to show scheduled tasks

**Format:**
```markdown
### Cron Jobs / Automation
- **Schedule:** `0 14 * * *` (daily 2 PM)
- **Command:** `python scripts/daily_update.py`
- **Purpose:** Process daily data
- **Status:** Active
```

**When to update:**
- Cron job added
- Schedule changed
- Job enabled/disabled

---

## AI Session Guidance

### When Starting a Session
**Read in this order:**
1. **Current State** - Understand where things are
2. **Blockers & Dependencies** - Know what's stopping progress
3. **Pending Tasks** - See what's next
4. **Success Criteria** - Know what "done" looks like
5. **Notes** - Get context (costs, related projects, decisions)

### When Updating TODO
**Always:**
1. Update "Last Updated" date at top
2. Move completed tasks to Completed section (keep checkbox [x])
3. Add dates to completed phases
4. Update "Current State" as project evolves
5. Keep Blockers section honest and current
6. Mark tasks as [x] when done (don't delete)

**Never:**
- Delete completed tasks (they show progress)
- Leave stale blockers (remove when resolved)
- Forget to update dates
- Skip "Current State" updates

### When Handing Off to Another Session
**Document:**
1. What was accomplished this session
2. Any new blockers discovered
3. Decisions made (add to Notes)
4. Questions that arose (add to Notes)
5. Next recommended step (update priorities)

---

## Flexibility Guidelines

### Simple Projects (< 5 tasks)
- Can use minimal format
- Focus on: Current State, Pending, Success Criteria
- Skip: Phase breakdowns, extensive notes

### Complex Projects (> 50 tasks)
- Use full format
- Add: Change log, integration learnings, technical stack
- Consider: Sub-TODOs per major component

### Experimental Projects
- Focus on: Decision points, learnings, open questions
- Less emphasis on: Rigid task lists, schedules

### Production Projects
- Emphasize: Blockers, automation, success criteria
- Include: Cost tracking, related dependencies

**Rule:** Use format as framework, adapt to project needs

---

## Dashboard Integration

### Metadata Dashboard Will Extract

**From Header:**
- Project name
- Status
- Phase
- Last updated

**From Current State:**
- What's working (feature count)
- What's missing (gap count)
- Blockers (count, descriptions)

**From Tasks:**
- Total tasks
- Completed tasks
- Completion percentage
- Priority breakdown

**From Notes:**
- AI agents in use
- Cron jobs
- External services
- Cost data

### How Dashboard Will Display

**Project card will show:**
- Name + Status badge
- Last updated (sorted by this)
- Progress bar (X% complete)
- AI agent indicator
- Cron job indicator (⏰)
- Services indicator
- Blocker alert (⚠️)

**Click project → Shows:**
- Full TODO.md rendered
- All metadata extracted
- Links to related docs

---

## Examples from Real Projects

### Example 1: New Project (Minimal)
```markdown
# My New Tool - TODO

**Last Updated:** December 30, 2025  
**Project Status:** Development  
**Current Phase:** MVP

## 📍 Current State

### What's Working ✅
- Nothing yet, just started

### What's Missing ❌
- Everything

### Blockers & Dependencies
- None

## 📋 Pending Tasks

### 🔴 CRITICAL
- [ ] Set up project structure
- [ ] Write core functionality
- [ ] Test basic features

## 🎯 Success Criteria

### MVP Complete When:
- [ ] Core feature works
- [ ] Tests pass
- [ ] Documentation written

## 📊 Notes

### AI Agents in Use
- **Claude Sonnet 4.5:** Initial implementation

### Time Estimates
- MVP: 4-6 hours
```

### Example 2: Active Project (Standard)
See: `cortana-personal-ai/TODO.md` for excellent full example

### Example 3: Planning Phase (Detailed)
See: `actionable-ai-intel/TODO.md` for planning with blockers

### Example 4: Mature Project (Minimal)
See: `project-scaffolding/TODO.md` for focused sprint format

---

## Integration with Project Scaffolding

### Where Template Lives
`project-scaffolding/templates/TODO.md.template`

### When to Use
**New project kickoff:**
1. Copy template to project root
2. Fill in placeholders ({{PROJECT_NAME}}, etc.)
3. Delete unused optional sections
4. Add project-specific details

**Existing project:**
1. Read current TODO (if exists)
2. Map content to new format
3. Fill in missing sections (AI agents, cron jobs)
4. Preserve all existing information

### Project Scaffolding Integration
- [ ] Add TODO template to templates/
- [ ] Update PROJECT_KICKOFF_GUIDE.md with TODO creation step
- [ ] Add TODO section to project creation checklist
- [ ] Document format standard (this file)
- [ ] Create examples from real projects

---

## Success Metrics

**This standard is working if:**
1. ✅ New AI sessions can orient in < 2 minutes
2. ✅ Dashboard can extract all needed metadata
3. ✅ Erik can glance at TODO and know project state
4. ✅ Handoffs between sessions are smooth
5. ✅ Completed work is visible (progress tracking)

**After 1 month:**
- [ ] 5+ projects using standard format
- [ ] Dashboard successfully extracts metadata
- [ ] No confusion about project state
- [ ] AI sessions reference TODO at start

**After 3 months:**
- [ ] All active projects using standard
- [ ] Format refined based on usage
- [ ] Pattern extracted to agent-skills-library
- [ ] Others could adopt this format

---

## Next Steps

1. **Get Erik's approval** on this format
2. **Add template to project-scaffolding**
3. **Update 2-3 existing projects** to use format
4. **Build dashboard** to consume this data
5. **Refine based on real usage** (iterate!)

---

## Questions for Erik

1. **Format approval:** Does this structure make sense for your workflow?
2. **Required vs optional:** Are AI agents, cron jobs, costs required or optional?
3. **Priority system:** Do 4 levels (🔴 🟡 🔵 🟢) work, or prefer 3?
4. **Flexibility:** Should simple projects use minimal format, or always full?
5. **Change log:** Required or optional?

---

## Related Documentation

- **Template:** `project-scaffolding/templates/TODO.md.template`
- **Project Kickoff Guide:** `project-scaffolding/Documents/PROJECT_KICKOFF_GUIDE.md`
- **Dashboard README:** `project-tracker/README.md`
- **Dashboard TODO:** `project-tracker/TODO.md` (uses this format!)

---

**Version History:**
- v1.0 (December 30, 2025) - Initial standard based on analysis of 4 projects

---

*This document is the "why" behind the template. The template is the "what". Use both together.*

