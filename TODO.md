# Project Scaffolding - TODO

> **Purpose:** Current actionable tasks for project-scaffolding
> **Last Updated:** January 12, 2026
> **Type:** Infrastructure

---

## ✅ COMPLETED: Clean Up project-scaffolding & Apply to Canary Projects

**Status:** DONE (Jan 12, 2026)
**Result:** All 3 canary projects (project-tracker, tax-organizer, analyze-youtube-videos) are now standalone with scaffolding applied. Tasks A-D complete.

**What was done:**
- Task A: Removed Ollama/Worker references from file operations (Workers are for code gen only)
- Task B: Ran doc hygiene, cleaned up bloated docs
- Task C: Verified `scaffold_cli.py apply` command works (dry-run, idempotent)
- Task D: Applied scaffolding to all 3 canary projects

**Key Learning:** The 12-prompt approach was overcomplicated. File copies don't need AI - they need bash. Workers can't execute commands - they only generate text.

---

## 🚨 CURRENT PRIORITY: Remaining Cleanup

- [ ] **Doc hygiene pass on image-workflow:** After we prove the pattern works here

---

## 📚 Architecture (Reference)

### Core Model: Template Generator (Like Create React App)

project-scaffolding is a **template source**, not a runtime dependency.
- Scripts get **COPIED** to projects
- Projects are **standalone** after scaffolding
- No `$SCAFFOLDING` references in target projects

---

### Industry Patterns Research

Before implementing, let's understand how professional tools handle this:

#### Pattern 1: Template Generator (Create React App, Vite)
**How it works:**
- One-time generation: `npx create-react-app my-app`
- COPIES template into new project
- Project is standalone after creation
- No ongoing dependency on generator

**Updates:**
- Manual migration guides
- Sometimes automated codemods (`npx react-codemod`)
- User chooses when to update

**Pros:** Projects are independent, portable
**Cons:** Updates don't propagate automatically

#### Pattern 2: Cookiecutter (Python)
**How it works:**
- Template with variables: `cookiecutter gh:user/template`
- Prompts for customization
- Generates standalone project
- Can "replay" to regenerate

**Updates:**
- Manual re-application
- Diff and merge changes

**Pros:** Flexible, well-established
**Cons:** No automated sync

#### Pattern 3: Dependabot / Renovate (Dependency Updates)
**How it works:**
- Bot monitors dependencies
- Opens PRs when updates available
- Automated but requires approval

**Could we adapt this?**
- Bot monitors scaffolding changes
- Opens PRs to sync projects
- Human reviews and merges

#### Pattern 4: Shared Library (Node modules, Python packages)
**How it works:**
- Common code in npm package
- Projects depend on `@myorg/shared-lib`
- Update via version bump

**Why this DOESN'T work for us:**
- Our "code" is templates, patterns, scripts
- Each project needs to customize
- Not suitable for package distribution

---

### Recommended Architecture

**Model: Template Generator + Sync Bot (Hybrid)**

**Phase 1: Initial Generation (Like Create React App)**
```bash
# New project
./scaffold_cli.py create my-new-project

# Existing project
./scaffold_cli.py apply my-existing-project
```

**Phase 2: Ongoing Sync (Like Dependabot)**
- Bot monitors scaffolding repo for changes
- Detects when projects are "behind"
- Creates PRs with updates
- Human reviews and approves

**What Gets Copied (Full Independence):**
1. **Scripts:** `warden_audit.py`, `validate_project.py`, `pre_review_scan.sh`
2. **Protocols:** `REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
3. **Patterns:** `patterns/code-review-standard.md`, `patterns/learning-loop-pattern.md`
4. **Reference:** `LOCAL_MODEL_LEARNINGS.md`
5. **Templates:** `CODE_REVIEW.md.template`

**What Stays in Scaffolding (Centralized for Updates):**
- The templates themselves (`.cursorrules-template`, etc.)
- The generator CLI (`scaffold_cli.py`)
- Meta-documentation about the system

---

### Architecture Decisions

#### Decision 1: Use Relative Paths (Jan 12, 2026)

**When removing `$SCAFFOLDING` references, use relative paths:**
- ✅ **Correct:** `python ./scripts/warden_audit.py`
- ❌ **Wrong:** `python $SCAFFOLDING/scripts/warden_audit.py` (runtime dependency)
- ❌ **Wrong:** `python $PROJECT/scripts/warden_audit.py` (unnecessary variable)

**Why relative paths:**
- **Simplest:** No environment variable resolution needed
- **Clone-friendly:** Works immediately after `git clone`
- **Portable:** Works from project root on any machine
- **Standard:** Industry convention for project-local scripts

**Assumption:** Commands run from project root (document this in each project's README)

#### Decision 2: Sync Bot for Patch Propagation (Jan 12, 2026)

**Purpose:** When project-scaffolding gets bug fixes or improvements, propagate to all downstream projects.

**How it works:**
1. Bug fix committed to `project-scaffolding/scripts/warden_audit.py`
2. Sync bot detects change
3. Bot opens PR to each downstream project: "Update warden_audit.py (scaffolding v1.6)"
4. Human reviews PR (via dashboard or GitHub)
5. Human decides: Accept patch OR ignore (keep local version)

**This is Phase 2 work** - design after manual transfers are complete and patterns are established.

**Why this matters:**
- Security patches propagate automatically
- Bug fixes reach all projects
- Projects can opt-out if they've customized
- Surface patches on dashboard for visibility


---

## 📋 BACKLOG - High Priority

### Modular AI Workflow System (Jan 13, 2026)
**Goal:** Separate "what to do" (project identity) from "how to do" (execution workflow) so workflows can be plugged/unplugged ecosystem-wide without editing every project.

**Problem Discovered:**
- Ollama delegation instructions were hardcoded into project `.cursorrules` and `AGENTS.md`
- To "unplug" Ollama, we'd have to edit 36 projects manually
- "How to execute" shouldn't be baked into project identity files

**Proposed Architecture:**

```
_tools/workflows/                    ← Ecosystem-level (Erik's local control)
├── active.md                        ← Symlink or current strategy
├── direct-execution.md              ← "FM does work directly"
├── ollama-delegation.md             ← "FM delegates to local Ollama workers"
└── agent-hub.md                     ← "FM delegates via Agent Hub"

project-scaffolding/templates/workflows/  ← Source templates
└── (same files as above)
```

**How It Works:**

1. **For Erik's ecosystem (36 projects):**
   - Project `.cursorrules` says: "For execution workflow, see `$PROJECTS_ROOT/_tools/workflows/active.md`"
   - Change `active.md` once → all projects inherit the change
   - Central control, instant propagation

2. **For standalone/downloaded projects:**
   - `scaffold apply` COPIES the active workflow into `project/Documents/workflows/`
   - Project checks: "Does `$PROJECTS_ROOT/_tools/workflows/` exist? Use that. Otherwise use my embedded copy."
   - Graceful degradation - works standalone, but ecosystem can override

**Tasks:**
- [ ] Create `_tools/workflows/` directory structure
- [ ] Create workflow files: `direct-execution.md`, `ollama-delegation.md`, `agent-hub.md`
- [ ] Set `direct-execution.md` as `active.md` (current state - Ollama unplugged)
- [ ] Create `project-scaffolding/templates/workflows/` with same files
- [ ] Update `.cursorrules-template` to reference workflow system
- [ ] Update existing projects to use new pattern (can be gradual)
- [ ] Document in README: "How to switch execution workflows"

**Why This Matters:**
- One switch to change all projects
- Workflows are versioned and can evolve
- Projects remain standalone when shared
- Clean separation of concerns (identity vs execution)

**⚠️ CRITICAL PRINCIPLE: Build-Time vs Runtime**

`_tools/` is **BUILD-TIME ONLY** infrastructure:
- Used when DEVELOPING projects (scaffolding, validation, AI-assisted coding)
- Referenced by developers and AI assistants during development
- NEVER referenced by deployed/running projects

Deployed projects must be 100% self-contained:
- A website (muffin pan recipes) has no idea `_tools/` exists
- An autonomous agent inside a project uses its OWN logic, not `_tools/agent-hub/`
- If it would break when deployed to the internet, it shouldn't reference `_tools/`

**Simple test:** "If I `git clone` this project on a fresh machine and run it, does it work without `_tools/`?"
- YES → Correct architecture
- NO → Build-time dependency leaked into runtime

---

### Ecosystem Integrity Warden (NEW TOOL)
**Location:** `_tools/integrity-warden/integrity_warden.py`
**Purpose:** Unified scanner for broken connections ecosystem-wide.
- [x] Detect broken WikiLinks & Markdown links
- [x] Detect broken absolute paths (`[absolute_path]/.../projects/`)
- [x] Detect broken relative cross-project refs (`../other-project/`)
- [ ] Add detector for broken Python imports (sys.path)
- [ ] Add detector for broken Shell environment dependencies

---

### Cortana Investigation & Monitoring
**Goal:** Investigate why Cortana broke and set up monitoring to prevent future silent failures
**Context:** Cortana was broken from Dec 18, 2025 to Jan 10, 2026 (22 days) - undetected until manual check

- [x] **Investigation:**
  - [x] Determine root cause of agent-os dependency breaking Cortana (COMPLETE: Cortana was sourcing agent-os venv)
  - [x] Review why 130 historical dates were missing (COMPLETE: Backfilled)
  - [x] Document findings in Cortana project (COMPLETE: INVESTIGATION_HANDOFF_2026-01-10.md)

- [ ] **Monitoring System:**
  - [ ] Set up health check for Cortana LaunchAgent (daily cron? heartbeat file?)
  - [ ] Alert if daily update hasn't run in 24+ hours
  - [ ] Consider: log rotation, disk space monitoring, API key expiry warnings

- [ ] **Prevent Recurrence:**
  - [ ] Ensure Cortana remains self-sufficient (no external venv dependencies)
  - [ ] Add Cortana to project-tracker dashboard for visibility

**Why This Matters:**
- 22 days of silent failure is unacceptable
- Personal AI should be the most reliable system in the ecosystem

**Fixes Applied (Jan 10, 2026):**
- Created Cortana's own venv and .env (no agent-os dependency)
- Fixed Wispr Flow timestamp parsing (trailing space issue)
- Backfilled all 130 missing dates

---

### Code Review System Integration (Medium Priority)
**Goal:** Standardize code review process across all projects

- [x] Create CODE_REVIEW.md.template
- [x] Define standard code review format
- [x] Add to PROJECT_STRUCTURE_STANDARDS.md
- [ ] Integrate with TODO.md format: `- [ ] Task **[IN REVIEW]** - See CODE_REVIEW.md #123`
- [ ] Update TODO_FORMAT_STANDARD.md
- [ ] Update TODO.md.template
- [ ] Create examples from real code reviews
- [ ] Test with project-tracker (dogfood it!)

**Why This Matters:**
- Project-tracker dashboard will display pending code reviews
- Alerts table will show code review status
- Need standard format to parse and display

---

### Document SCAR TISSUE SLA
**Goal:** Formalize the "defect → checklist within 24 hours" pattern

- [ ] **Add to CODE_QUALITY_STANDARDS.md (20 min)**
  - [ ] Create Critical Rule #7: SCAR TISSUE SLA
  - [ ] Include: test case + anti-pattern doc + checklist item requirements
  - [ ] Document accountability guidelines
  - [ ] Add example: test_scripts_follow_standards.py indentation bug

- [ ] **Create TESTING_PHILOSOPHY.md**
  - [ ] Document inverse testing approach (test what can go WRONG)
  - [ ] Explain why this exists (institutional memory in solo workflow)

**Why This Matters:**
- Web-Claude praised this as distinguishing feature
- Turns every defect into permanent system improvement
- Prevents repeated mistakes

**Time Estimate:** 40 minutes total

---

#### Coverage Reporting & Fuzzing
**Goal:** Visibility into what's NOT tested + adversarial fuzzing

- [ ] **Coverage Setup (30 min)**
  - [ ] Install pytest-cov
  - [ ] Add coverage commands to testing workflow
  - [ ] Target: 80% line coverage minimum
  - [ ] 100% coverage for security-critical functions (safe_slug, find_project_root, save_atomic)
  - [ ] Generate HTML reports in .coverage_html/ (add to .gitignore)

- [ ] **CI Integration (15 min)**
  - [ ] Run coverage on every test suite execution
  - [ ] Fail if coverage drops below 75%

- [ ] **Fuzzing Lite (45 min)**
  - [ ] Create tests/test_fuzzing.py
  - [ ] Random filenames: unicode, emojis, null bytes, max length, path traversal
  - [ ] Random file sizes: 0B, 1B, 500KB, 501KB, 1GB
  - [ ] Symlinks: valid, broken, circular, pointing to excluded dirs
  - [ ] Concurrent operations: 10 threads with save_atomic()

**Success Criteria:**
- Coverage report shows 80%+
- Fuzzing finds no crashes

**Time Estimate:** 90 minutes total

---

### Cost Tracking
- [ ] Add cost tracking log (logs/cost-tracking.jsonl)
- [ ] Validate pricing against real bills (monthly)

---

## 📋 BACKLOG - Medium Priority

### Ecosystem Resilience
- [ ] Integrate disaster recovery templates
- [ ] Add project lifecycle scripts
- [ ] Integrate backup system as default component

### AI Safety & Trustworthiness (For Projects with Embedded AI)
**Context:** See trustworthy_ai_report.md for full patterns. This scaffolding project focuses on file-level safety (Warden, send2trash), but other projects with active AI agents need model-level defenses.

- [ ] **Model Layer Defense-in-Depth (Not applicable to scaffolding, but critical for AI-heavy projects)**
  - [ ] Research Constitutional AI approach (Anthropic pattern, report lines 40-43, 604-615)
  - [ ] Evaluate RLHF with safety principles for agent training
  - [ ] Implement chain-of-thought for transparency in agent decision-making
  - [ ] Document which projects need model-level safety (vs. just tool-level)
  - [ ] Reference: trustworthy_ai_report.md Section 1.2 (Layered Architecture)

**Projects this applies to:**
- Any project using LangGraph, LangChain, or custom agent orchestration
- Projects where AI generates code, makes decisions, or interacts with users
- Multi-agent systems with autonomous decision-making

**Why this matters:**
- Scaffolding focuses on preventing file system mistakes (Layer 1, 4, 5)
- AI-heavy projects need all 6 layers, including Model Layer training/alignment
- This is Medium Priority because it's strategic planning, not immediate implementation

### Local Model Learning System
**Goal:** Build institutional memory about local AI model behavior
**Document:** `Documents/reference/LOCAL_MODEL_LEARNINGS.md` ✅ CREATED

- [ ] **After each major session with local models:**
  - [ ] Record model used, task type, outcome in Failure Log
  - [ ] Note any prompt adjustments that helped
  - [ ] Update Model Profiles with new quirks/tips
- [ ] **Monthly review:**
  - [ ] Identify patterns in failure log
  - [ ] Promote successful prompt patterns to Pattern Library
  - [ ] Update model tier recommendations if quality changed
- [ ] **Integration:**
  - [ ] Reference LOCAL_MODEL_LEARNINGS.md in AGENTS.md
  - [ ] Add to Floor Manager handoff checklist (update after session)

**Why this matters:**
- Local models are a black box without persistent memory
- Knowledge about what works evaporates between sessions
- Structured capture prevents re-learning same lessons

---

### Scaffolding Versioning System
**Goal:** Version project-scaffolding like npm modules - deployable, upgradeable, trackable
**Philosophy:** "Safety is an evolution. Projects are never done - just at some point in evolution."

- [ ] **Design versioned scaffolding:**
  - [ ] Define what constitutes a "version" (safety rules, templates, patterns)
  - [ ] Track which projects are on which version
  - [ ] Upgrade path: how to bring old projects to new version
  - [ ] Compatibility matrix: what breaks between versions
- [ ] **Visibility:**
  - [ ] Dashboard showing project compliance levels
  - [ ] "Checking all boxes" vs "checking some boxes" status per project
  - [ ] Stale project detection (hasn't been upgraded)

**Why this matters:**
- Projects can be months between work sessions
- Need to know at a glance what's current vs outdated
- Upgrade should be intentional, not forced

---

### Backstage-Lite: Full Ecosystem Governance (Vision - Jan 12, 2026)

**Goal:** Build a lightweight version of Spotify's Backstage for the ecosystem - software catalog, drift detection, bidirectional learning.

**Industry Research (from Claude Code Review):**

| Pattern | How It Works | Fits Our Vision? |
|---------|--------------|------------------|
| Create React App | One-time scaffold, then "eject" | ❌ No ongoing updates |
| Nx/Turborepo | Monorepo with shared generators + migrations | ✅ Has "migrations" concept |
| Backstage (Spotify) | Software catalog + golden path templates + scorecards | ✅ Very close to full vision |
| Renovate/Dependabot | Bots scan repos, create PRs for updates | ✅ Our "sync bot" concept |

**What Backstage-Lite Would Include:**

1. **Software Catalog**
   - Central registry of all 36+ projects
   - Each project's scaffolding_version tracked
   - Health status at a glance (project-tracker dashboard integration)

2. **Golden Path Templates**
   - project-scaffolding remains the source of truth
   - `scaffold_cli.py apply` copies templates to projects
   - Version tracking on each transfer

3. **Drift Detection / Scorecards**
   - Bot scans all projects weekly
   - Compares against current scaffolding version
   - Surfaces gaps: "project-tracker is 2 versions behind"
   - Scorecard per project: which standards are met vs missing

4. **Bidirectional Learning**
   - LOCAL_MODEL_LEARNINGS.md from each project aggregates back
   - Learnings inform scaffolding improvements
   - Skills library (`agent-skills-library`) as the aggregation point
   - Pattern: Project discovers quirk → Documents it → Flows to scaffolding → Propagates to all projects

5. **Patch Propagation**
   - When scaffolding gets a bug fix, sync bot opens PRs to all downstream projects
   - Human reviews and accepts/rejects
   - Surface on dashboard: "5 projects have pending scaffolding updates"

**Why This Matters:**
- Current model requires manual tracking of what's out of date
- No visibility into which projects are "healthy" vs "drifting"
- Learnings in one project don't propagate to others
- Security patches require manual effort to push everywhere

**Trigger:** Build this when manual sync becomes painful (estimated: after 5+ projects using scaffolding actively)

**Inspiration:** Spotify Backstage, but without the Kubernetes/cloud complexity. Just Python scripts + dashboard integration.

---

### Infrastructure Research
- [ ] Prompt versioning system
- [ ] AWS Activate research (Q2 2026)
- [ ] Google Cloud credits (Q2 2026)

### EXTERNAL_RESOURCES Crawler (Future)
**Goal:** Auto-discover projects/tools across ecosystem to keep registry current
**Trigger:** When manual updates become painful (projected: 12 months at current pace)

- [ ] Crawler scans projects directory weekly/monthly
- [ ] Detects new projects, MCPs, tools, external services
- [ ] Updates EXTERNAL_RESOURCES.yaml automatically
- [ ] Reports what's new since last scan

**Why:** Two months spent on image workflow alone. At this pace, will lose track of what exists.
**Current state:** Manual additions to EXTERNAL_RESOURCES.yaml (good enough for now)

---

## 📋 BACKLOG - Low Priority
**Only build if manual process becomes painful**

- [ ] Task dispatch system (only if manual tiering becomes painful)
- [ ] Multi-AI build automation (only after 3+ projects prove manual works)

---

## 📚 Pattern Management

**System:** See `Documents/reference/PATTERN_MANAGEMENT.md` for full details
**Registry:** Pattern status tracked in PATTERN_MANAGEMENT.md (SSOT)
**Last Review:** January 9, 2026

### Monthly Review (Next: February 9, 2026)

**Quick checks (10 min):**
- [ ] Any new projects launched? → Note which patterns were applied in registry
- [ ] Any patterns cause problems? → Document in registry notes
- [ ] Any 🟡 patterns hit 3 projects? → Promote to 🟢 in registry
- [ ] Update "Last Review" date in registry

**Current Action Items:**
- [ ] Apply `tiered-ai-sprint-planning.md` to 3rd project → promote to 🟢
- [ ] Apply `local-ai-integration.md` to 3rd project → promote to 🟢

### Quarterly Audit (Next: April 9, 2026)

**Full review (30 min):**
- [ ] Review all 🟢 patterns for accuracy
- [ ] Check for fluff (enforce 300-line soft limit)
- [ ] Update PATTERN_ANALYSIS.md to match registry
- [ ] Update 00_Index with any new patterns

**Identified Issues:**
- ⚠️ `development-philosophy.md` is 776 lines (8 patterns = ~97 lines each) - **ACCEPTABLE** (comprehensive guide)

### Pattern Quality Check

**Current status (10 patterns total):**
- 🟢 Proven: 8 patterns (extracted to `patterns/`)
- 🟡 Emerging: 2 patterns (needs 3rd project evidence)
- 🔵 Candidate: 0 (watch for new patterns in projects)

**Quality metrics:**
- ✅ All patterns have status tags
- ✅ All patterns under 550 lines (within guidelines)
- ✅ Registry is current (updated Jan 9, 2026)

---

## 🎯 Success Metrics

**This scaffolding is working if:**
1. ✅ New project setup takes < 30 min (vs. hours of copy-paste)
2. ✅ EXTERNAL_RESOURCES.md prevents duplicate signups
3. ✅ DeepSeek reviews save money vs. Cursor (backtest after 1 month)
4. ⏭️ Templates get customized (not shipped with placeholders)
5. ⏭️ Someone else can use it in < 30 min

**As of Dec 23:**
- Metrics 1-3: Proven
- Metrics 4-5: TBD (need dogfooding)

---

## 🗑️ Deleted/Archived

**Archived (Documents/archives/):**
- Original 1353-line TODO (brain dump)
- Historical planning docs (Option C build plan, system walkthrough, etc.)

**Reason:** Claude Code review identified "documentation about automation" not "automation"

**Archive Reference:** See `Documents/archives/planning/planning-notes-dec-2025.md` for historical brain dumps

---

**END OF TODO**
