# Project Scaffolding - TODO

## 🚨 Cleanup Required
- [ ] **Remove Kiro:** Remove all Kiro references and `.kiro` directories from ecosystem. Kiro integration was abandoned.

> **Purpose:** Current actionable tasks for project-scaffolding
> **Last Updated:** January 11, 2026
> **Type:** Infrastructure

---

## 🎯 NEW TOP PRIORITY: Code Review Infrastructure Integration (Jan 11+)

**Context:** We have comprehensive code review infrastructure (review orchestrator, validation scripts, DNA integrity scans, review prompts) but it's trapped in `project-scaffolding` and not documented or accessible to other projects that use the scaffolding.

**Problem Statement:**
- When scaffolding new projects, we copy templates but NOT the review system
- Projects don't know the code review workflow exists
- The powerful `validate_project.py` script (scans for hardcoded paths, secrets, etc.) only runs FROM scaffolding, not IN projects
- Templates don't reference or document the review infrastructure
- New projects have no guidance on requesting code reviews or running validation

**Goal:** Make code review infrastructure discoverable, documented, and accessible to all scaffolded projects.

---

### Phase 1: Documentation Updates (High Priority)

These tasks update existing documentation to reference and explain the code review system.

#### Task 1.1: Update QUICKSTART.md - Add Code Review Section
**File:** `QUICKSTART.md`
**Goal:** Add a new section explaining code review and validation workflow

**What to add:**
- Section: "Phase 6: Validation and Code Review" (after Phase 5: Start Building)
- Explain how to validate project structure: `python $SCAFFOLDING/scripts/validate_project.py [project-name]`
- Explain DNA integrity checks (scans for hardcoded paths, exposed secrets)
- Explain how to request code reviews: `python $SCAFFOLDING/scaffold_cli.py review --type document --input [file]`
- Link to `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for full review standards
- Link to `patterns/code-review-standard.md` for pattern documentation

**Acceptance Criteria:**
- [ ] New "Phase 6" section exists in QUICKSTART.md
- [ ] Code review workflow documented with commands
- [ ] Validation workflow documented with commands
- [ ] Links to detailed review docs included
- [ ] Examples show both new project and existing project scenarios

---

#### Task 1.2: Update AGENTS.md.template - Add Code Review to Definition of Done
**File:** `templates/AGENTS.md.template`
**Goal:** Include code review as a standard step in the Definition of Done checklist

**What to add:**
- In the "Definition of Done" section, add checklist item: "Code review completed (if significant architectural changes)"
- Add reference to code review standards: "See `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`"
- In constraints section, add: "ALWAYS run validation before considering work complete: `python $SCAFFOLDING/scripts/validate_project.py [project-name]`"

**Acceptance Criteria:**
- [ ] Code review added to Definition of Done checklist in template
- [ ] Reference to REVIEWS_AND_GOVERNANCE_PROTOCOL.md included
- [ ] Validation command documented in constraints section
- [ ] Template makes it clear this is centralized (runs from $SCAFFOLDING)

---

#### Task 1.3: Update CLAUDE.md.template - Add Code Review and Validation Instructions
**File:** `templates/CLAUDE.md.template`
**Goal:** Tell AI assistants how to request reviews and validate code

**What to add:**
- New section: "## Code Review and Validation"
- Subsection: "When to Request a Code Review" (architectural decisions, security-critical code, before major features)
- Subsection: "How to Request a Review" (use CODE_REVIEW.md.template, run scaffold_cli.py review command)
- Subsection: "How to Validate Your Work" (run validate_project.py, what it checks for)
- List what validation catches: hardcoded paths (/Users/, /home/), exposed secrets (API keys), missing files, structural issues

**Acceptance Criteria:**
- [ ] New "Code Review and Validation" section exists in template
- [ ] When to review documented
- [ ] How to request review documented with command
- [ ] How to validate documented with command
- [ ] AI understands this is available tooling, not something to implement

---

#### Task 1.4: Update .cursorrules-template - Reference Code Review Standards
**File:** `templates/.cursorrules-template`
**Goal:** Make Cursor-based AI aware of code review infrastructure

**What to add:**
- In "Definition of Done" section: Add "Code validated (no hardcoded paths, no secrets exposed)"
- In "Related Files" section: Add link to `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- In "Execution Commands" section: Add validation command example

**Acceptance Criteria:**
- [ ] Code validation added to Definition of Done
- [ ] Link to review protocol in Related Files section
- [ ] Validation command in Execution Commands section
- [ ] Format matches existing .cursorrules style

---

#### Task 1.5: Update Documents/PROJECT_KICKOFF_GUIDE.md - Add Code Review Phase
**File:** `Documents/PROJECT_KICKOFF_GUIDE.md`
**Goal:** Include code review as a standard phase in project kickoff workflow

**What to add:**
- New section after project setup: "Step 6: Validate Your Setup"
- Explain running `validate_project.py` on new project
- Show expected output (what passes, what might need fixes)
- Add to "Quick Start" workflow
- Reference ongoing validation during development

**Acceptance Criteria:**
- [ ] New "Step 6" section exists in PROJECT_KICKOFF_GUIDE.md
- [ ] Validation command documented
- [ ] Expected output shown (example of clean validation)
- [ ] Integrated into main workflow, not just appendix
- [ ] Mentions ongoing validation, not just initial setup

---

### Phase 2: Template Enhancement (Medium Priority)

These tasks improve templates to better leverage the code review system.

#### Task 2.1: Enhance CODE_REVIEW.md.template - Add Workflow Instructions
**File:** `templates/CODE_REVIEW.md.template`
**Goal:** The template currently is just a checklist; add instructions on HOW to use it

**What to add:**
- Header section: "How to Use This Template"
- Step 1: Fill out the Definition of Done section (what makes this code "done")
- Step 2: Run the review command from scaffolding
- Step 3: Reviews saved to `Documents/archives/reviews/CODE_REVIEW_{REVIEWER}_{VERSION}.md`
- Step 4: Archive old reviews before new rounds
- Reference to `patterns/code-review-standard.md` for full pattern

**Acceptance Criteria:**
- [ ] "How to Use This Template" section exists
- [ ] Step-by-step workflow documented
- [ ] Command examples included
- [ ] Links to pattern documentation included
- [ ] Template explains review output location and archival

---

#### Task 2.2: Add Validation to TODO.md.template
**File:** `templates/TODO.md.template`
**Goal:** Include validation as a standard task category in new projects

**What to add:**
- Section: "## Validation Checklist"
- Checklist items:
  - [ ] No hardcoded absolute paths (/Users/, /home/)
  - [ ] No exposed secrets (API keys in code)
  - [ ] All mandatory files present (from PROJECT_STRUCTURE_STANDARDS.md)
  - [ ] Project passes: `python $SCAFFOLDING/scripts/validate_project.py [project-name]`

**Acceptance Criteria:**
- [ ] "Validation Checklist" section in TODO.md.template
- [ ] Key validation items listed
- [ ] Validation command included
- [ ] Format matches rest of TODO.md.template

---

### Phase 3: Infrastructure Documentation (Medium Priority)

These tasks create new documentation explaining the review system architecture.

#### Task 3.1: Create Documents/guides/CODE_REVIEW_SYSTEM.md
**File:** `Documents/guides/CODE_REVIEW_SYSTEM.md` (NEW FILE)
**Goal:** Comprehensive guide to the entire code review infrastructure

**What to include:**
- Overview: What the code review system does
- Architecture: Components (review orchestrator, validation scripts, prompts, templates)
- How to Request Reviews: Step-by-step with examples
- How to Run Validation: Command examples and interpretation
- Multi-AI Review: How the orchestrator works (parallel reviews, cost tracking)
- Review Prompts: Available prompts (architecture, performance, security)
- Centralized vs Distributed: Why the system is centralized in scaffolding
- Integration with Projects: How projects reference and use the system

**Acceptance Criteria:**
- [ ] New file created at Documents/guides/CODE_REVIEW_SYSTEM.md
- [ ] All sections listed above included
- [ ] Examples and commands throughout
- [ ] Links to related files (REVIEWS_AND_GOVERNANCE_PROTOCOL.md, patterns, scripts)
- [ ] Explains both the "what" and the "why"

---

#### Task 3.2: Update patterns/code-review-standard.md - Add "How Projects Use This" Section
**File:** `patterns/code-review-standard.md`
**Goal:** Pattern doc currently explains the pattern but not how projects access it

**What to add:**
- New section: "## How to Use This Pattern in Your Project"
- Explain that review system lives in scaffolding
- Show commands to run from your project
- Explain template usage (CODE_REVIEW.md.template)
- Link to CODE_REVIEW_SYSTEM.md guide (once created)

**Acceptance Criteria:**
- [ ] New "How to Use This Pattern" section exists
- [ ] Commands shown with $SCAFFOLDING variable
- [ ] Template usage explained
- [ ] Practical examples included
- [ ] Links to full system guide

---

### Phase 4: Architecture Decision (Strategic Priority)

These tasks require strategic decisions about the review system architecture.

#### Task 4.1: Document Architecture Options for Review System
**File:** `Documents/architecture/CODE_REVIEW_ARCHITECTURE_OPTIONS.md` (NEW FILE)
**Goal:** Evaluate and document the three architectural approaches

**Options to analyze:**
1. **Centralized (Current):** Review system stays in scaffolding, projects call back to it
2. **Distributed:** Copy review system to each project (fully independent)
3. **Hybrid:** Keep orchestrator centralized, copy lightweight validation script per-project

**For each option, document:**
- Pros and cons
- Maintenance burden
- Discoverability
- Independence vs centralization trade-offs
- When each approach makes sense

**Recommendation:** Analyze and recommend one approach

**Acceptance Criteria:**
- [ ] New file created at Documents/architecture/CODE_REVIEW_ARCHITECTURE_OPTIONS.md
- [ ] All three options documented with pros/cons
- [ ] Trade-offs clearly explained
- [ ] Recommendation provided with reasoning
- [ ] Migration path outlined (if changing from current centralized model)

---

#### Task 4.2: (Conditional) Implement Distributed Validation Script
**File:** `scripts/distribute_validation.py` (NEW FILE - only if hybrid/distributed chosen)
**Goal:** If we choose hybrid/distributed model, create script to copy validation to projects

**What it should do:**
- Copy a lightweight version of `validate_project.py` to target project
- Create project-local validation command
- Update project's .cursorrules to reference local validation
- Keep it in sync when scaffolding validation updates

**Note:** Only create this if Task 4.1 recommends hybrid or distributed architecture

**Acceptance Criteria:**
- [ ] Script created (if needed)
- [ ] Can copy validation to existing project
- [ ] Project can run validation locally
- [ ] Documentation updated to reflect new workflow

---

### Phase 5: Quality Assurance (After Phase 1-3)

These tasks verify the integration is complete and documented correctly.

#### Task 5.1: Validate New Project Workflow with Updated Templates
**Goal:** Create a test new project using updated templates and verify workflow is clear

**Steps:**
1. Create new test project: `test-code-review-integration`
2. Copy all updated templates
3. Follow QUICKSTART.md exactly as written
4. Verify validation works
5. Verify code review workflow is clear from documentation
6. Document any confusion or gaps

**Acceptance Criteria:**
- [ ] Test project created successfully
- [ ] Validation runs and works as documented
- [ ] Code review workflow clear from templates
- [ ] Any gaps identified and fixed
- [ ] Test project can be used as reference example

---

#### Task 5.2: Validate Existing Project Integration
**Goal:** Apply updated templates to an existing project and verify workflow

**Steps:**
1. Choose existing project (e.g., project-tracker)
2. Update its AGENTS.md, CLAUDE.md, .cursorrules using new templates
3. Run validation
4. Verify the project now understands code review workflow
5. Document experience

**Acceptance Criteria:**
- [ ] Existing project updated with new template content
- [ ] Validation runs successfully
- [ ] Project documentation now references review system
- [ ] Any issues in "existing project" workflow fixed

---

#### Task 5.3: Create Example Code Review Request
**Goal:** Create a real example of requesting and receiving a code review

**Steps:**
1. Use the updated CODE_REVIEW.md.template
2. Request an actual review of some project-scaffolding component
3. Run the multi-AI review orchestrator
4. Archive the results properly
5. Document the entire process as an example

**Acceptance Criteria:**
- [ ] Example review request created
- [ ] Review actually run (multi-AI if possible)
- [ ] Results archived correctly
- [ ] Full process documented in CODE_REVIEW_SYSTEM.md as example

---

### Summary: What Success Looks Like

After completing these tasks, any project scaffolded from project-scaffolding will:
1. ✅ Know that code review infrastructure exists
2. ✅ Understand when to request reviews
3. ✅ Know how to request reviews (commands documented)
4. ✅ Know how to validate their code (DNA integrity checks)
5. ✅ Have templates that reference the review system
6. ✅ Have AI collaborators that understand the review workflow
7. ✅ Have clear documentation linking back to scaffolding

**Estimated Effort:**
- Phase 1 (Documentation Updates): ~3-4 hours of worker time
- Phase 2 (Template Enhancement): ~1-2 hours of worker time  
- Phase 3 (Infrastructure Docs): ~2-3 hours of worker time
- Phase 4 (Architecture Decision): ~2-3 hours of analysis + potential implementation
- Phase 5 (QA): ~2-3 hours of validation and examples

**Total:** ~10-15 hours of focused work across multiple sessions

---

## 🚨 TOP PRIORITY: Canary Monitoring (Jan 10-12, 2026)

**Status:** LIVE - 48-hour monitoring window Complete
**Deployed:** January 10, 2026 ~evening
**Ends:** January 12, 2026 ~evening

### FOCUS: Work in these projects daily for next 2 days

| Project | Has Work? | Notes |
|---------|-----------|-------|
| **project-tracker** | ✅ Loads | New bells and whistles not integrated yet |
| **Tax Processing** | ✅ Lots | Active project with pending work |
| **analyze-youtube-videos** | ❓ Check | May or may not be active |

### What to watch for:
- [ ] Safety rules appear in each project's .cursorrules
- [ ] No errors or complaints when working in projects
- [ ] Warden still passes in each project
- [ ] Nothing breaks unexpectedly

### After 48 hours (Jan 12):
- If clean: Full rollout to all 15+ projects
- If issues: Rollback via `.cursorrules.backup` files

---

## 🌙 TONIGHT'S SESSION (Jan 10, 2026)

**Cursor Usage:** 49% (Recorded Jan 10, 2026 @ 9:27 PM)
**Note:** 49% includes $100 overage buffer - actual base usage higher
**Strategy:** Option B (Dependency Chain - Bottom-Up)

### Active Work (Complete in Order)

#### 1. Warden Research & Enhancement
**Goal:** Make warden_audit.py ready for pre-commit hook use

- [x] **Research Phase (30 min)** ✅ COMPLETE
  - [x] Read warden_audit.py line-by-line and document current capabilities
  - [x] Compare current features vs. TODO expectations
  - [x] Map Warden to industry patterns (trustworthy_ai_report.md Patterns 4, 5, 13)
  - [x] Identify gaps: --fast flag, hardcoded path detection, test coverage, severity levels
  - [x] Document findings → `Documents/archives/planning/warden_evolution/WARDEN_RESEARCH_REPORT.md`
  - [x] Created Worker task prompts → `Documents/archives/planning/warden_evolution/WARDEN_PROMPTS_INDEX.md`

- [x] **Enhancement Phase (45 min)** ✅ COMPLETE (Floor Manager + Claude verification)
  - [x] Add --fast flag (grep-only mode, target < 1 second) ✅ 0.16s verified
  - [x] Add hardcoded path detection (/Users/, /home/, absolute paths) ✅ COMPLETE
  - [x] Add severity levels (P0: dangerous functions in production, P1: hardcoded paths, P2: warnings) ✅ COMPLETE
  - [x] Write tests in tests/test_security.py::TestWardenEnhanced (8 tests) ✅ COMPLETE
  - [x] Test against project-scaffolding itself ✅ Found P0 in scaffold/review.py (expected)
  - [x] Verify tests pass ✅ All 8 tests passing (verified by Erik)

**Acceptance Criteria:**
- Warden runs in < 1 sec with --fast flag
- Detects os.remove, os.unlink, shutil.rmtree
- Detects hardcoded /Users/ and /home/ paths
- Outputs severity levels (P0/P1/P2) for each finding
- Has passing tests in tests/test_warden.py
- Pre-commit hook can block P0/P1, warn on P2

**Known Issues to Fix:**
- scaffold/review.py:79 uses os.unlink (will be fixed in Safety Audit)

---

#### 2. Safety Audit
**Goal:** Fix known os.unlink usage and validate no other issues exist
**Unblocked by:** Warden Enhancement (need enhanced warden to validate)

- [x] **Fix Known Issue (15 min)** ✅ COMPLETE
  - [x] Replace os.unlink in scaffold/review.py:79 with send2trash ✅
  - [x] Verify send2trash is in requirements.txt (already present ✓)
  - [x] Test the change (run full test suite) ✅ (Warden tests pass)

- [x] **Validate Ecosystem (10 min)** ✅ COMPLETE
  - [x] Run enhanced warden_audit.py on project-scaffolding ✅ (0 P0 issues)
  - [x] Document any additional findings ✅
  - [x] Confirm zero dangerous function usage ✅

**Acceptance Criteria:**
- scaffold/review.py:79 uses send2trash instead of os.unlink
- All tests pass
- Warden reports zero dangerous function usage in production code

**Note:** This consolidates duplicate entries previously on lines 15, 95, 244

---

#### 3. Global Rules Injection
**Goal:** Design and implement rollout strategy for pushing safety rules to all projects
**Design Doc:** `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md` ✅ CREATED

- [x] **Design Script (30 min)** ✅ COMPLETE
  - [x] Draft update_cursorrules.py design with --dry-run mode
  - [x] Add --projects flag for gradual rollout (Pattern 9: Canary Deployment)
  - [x] Include rules: "Trash, Don't Delete" and "No Silent Failures"
  - [x] Add safety: backup original .cursorrules before modifying
  - [x] Write rollback procedure (restore from backup)

- [x] **Test Strategy (15 min)** ✅ COMPLETE
  - [x] Identify 3 test projects: project-tracker, Tax Processing, analyze-youtube-videos
  - [x] Define success criteria (projects build, no complaints, Warden clean)
  - [x] 48-hour monitoring window
  - [x] Success metrics documented
  - [x] Document blast radius: 16 projects with .cursorrules

- [x] **Get Human Approval** ✅ APPROVED (Jan 10, 2026)
  - [x] Present design to Erik
  - [x] Canary projects approved: project-tracker, Tax Processing, analyze-youtube-videos
  - [x] 48-hour monitoring approved
  - [x] Add --create flag for projects without .cursorrules

---

##### Implementation Attempt #1 (Jan 10, 2026)

**What we tried:**
- Super Manager (Claude) drafted Worker prompts with micro-task decomposition
- Prompts created: `Documents/planning/global_rules_injection/GLOBAL_RULES_PROMPT_1a-1d.md`
- Floor Manager dispatched to Workers (DeepSeek-R1, Qwen 2.5)

**What happened:**
- Tasks 1a-1b (skeleton, scanner) succeeded with DeepSeek-R1
- Tasks 1c-1d (detection, integration) timed out at 180s on both models
- Floor Manager completed the work manually - **PROTOCOL VIOLATION** (AGENTS.md prohibits Floor Manager from writing code)

**Outcome:**
- [x] Script exists and works (`scripts/update_cursorrules.py`)
- [x] 13 tests passing (`tests/test_update_cursorrules.py`)
- [x] Dry-run verified (0.28s execution, found 15 projects needing update)
- ⚠️ Workers did NOT build this - Floor Manager did
- ⚠️ Process failed even though artifact exists

**What we discovered:**
1. Micro-tasks helped (1a, 1b succeeded) but integration tasks still too heavy
2. File rewriting is expensive - should use StrReplace/diffs instead of full writes
3. Floor Manager needs explicit "HALT and escalate" instructions, not implicit
4. 120-180s timeout insufficient for file-heavy tasks (need 300s+)

**New patterns documented:** See `Documents/reference/LOCAL_MODEL_LEARNINGS.md`
- 3-Strike Escalation Rule
- Incremental Diff Style
- Updated Model Profiles with timeout guidance

---

##### Blocked: Questions Before Re-Implementation

Before attempting again with Workers doing the work properly, we need answers to:

1. **Knowledge Cycle:** How do learnings get applied to future prompts?
   - ✅ **PROPOSED SOLUTION:** Learning Loop Pattern (`patterns/learning-loop-pattern.md`)
   - Key mechanisms: Downstream Harm Estimate, Learning Debt Tracker, Preventable Failure Flag
   - AGENTS.md prompt template updated with new required sections
   - **Status:** Ready to test on next task

2. **Task Granularity:** What's the smallest atomic unit Workers can reliably complete?
   - 5-min tasks still too big for integration work
   - Need to test: diff-only output vs. full file writes
   - **Status:** Open - needs experimentation

3. **Escalation Protocol:** How do we enforce "stop and alert" vs. "Floor Manager takes over"?
   - ✅ **DOCUMENTED:** 3-Strike Escalation Rule in LOCAL_MODEL_LEARNINGS.md
   - ⚠️ **NOT YET STRUCTURAL:** Still relies on Floor Manager following instructions
   - ✅ **PROPOSED SOLUTION:** MCP-level enforcement via ollama-mcp enhancement
   - **Spec:** `Documents/planning/ollama_mcp_enhancement/OLLAMA_MCP_RETRY_ESCALATION_SPEC.md`
   - **Status:** Spec drafted, ready for implementation

**Decision:** Canary deployment is ON HOLD until we test the Learning Loop Pattern on a real task. The script works, but we want to prove:
1. The new prompt template structure works
2. Workers can complete tasks with the improved prompts
3. The Worker → Floor Manager → Conductor workflow holds

---

##### Canary Deployment (BLOCKED)

- [ ] Resolve knowledge cycle questions (see above)
- [ ] Re-attempt implementation with Workers using improved prompts
- [ ] Execute canary deployment on 3 projects
- [ ] Wait 48 hours, then full rollout

**Acceptance Criteria:**
- Script exists with --dry-run flag ✅
- Script supports --projects flag for subset rollout ✅
- Rollback procedure documented (restore from backups) ✅
- 3 test projects identified (10% canary) ✅
- 24-48 hour monitoring plan defined ✅
- Human approval received before ecosystem-wide execution ✅
- **NEW:** Workers successfully build the implementation (not Floor Manager)

**Why This Matters:**
- Pushes safety rules to all 30+ project .cursorrules files
- High blast radius - must be carefully tested first
- **Process matters:** We're building a repeatable system, not just shipping one script

---

## ✅ TONIGHT'S WORK (Jan 9, 2026) - COMPLETED

**What we did:**
1. ✅ Updated `PROJECT_STRUCTURE_STANDARDS.md` with new Code Review standards.
2. ✅ Reorganized `Documents/` directory into "Flat Root" (Active OS) model.
3. ✅ Created `Documents/README.md` as the master index (Grand Central Station).
4. ✅ Decanted floating root docs into `guides/` and `reference/`.
5. ✅ Cleaned up and organized `Documents/archives/` into functional subdirectories.
6. ✅ Updated templates (`CLAUDE.md.template`, `README.md.template`) to match flat root model.
7. ✅ Moved obsolete AWS setup notes to `_trash/`.

---

## ✅ What Exists & Works

**Templates:**
- `CLAUDE.md.template` (Updated for Flat Root)
- `CLAUDE.md` (Project standard) ✅ NEW (Dec 30)
- `CODE_REVIEW.md.template` ✅ NEW (Dec 30)
- `.cursorrules.template`
- `Documents/` structure (Flat Root / Active OS)
- `TIERED_SPRINT_PLANNER.md`
- `TODO.md.template` ✅ NEW (Dec 30)

**Standards:**
- `TODO_FORMAT_STANDARD.md` (Updated for Flat Root)
- `PROJECT_STRUCTURE_STANDARDS.md` (Updated with Code Review & Flat Root)
- `CODE_QUALITY_STANDARDS.md` (Active OS root)
- `PROJECT_INDEXING_SYSTEM.md` (Active OS root)

**Automation:**
- Multi-AI review orchestrator (DeepSeek + Ollama)
- 19 passing tests

**Tracking:**
- `EXTERNAL_RESOURCES.md` (560 lines, actually useful!)
- Per-project API key pattern

**Patterns:**
- Tiered AI sprint planning
- Safety systems
- Development philosophy
- API key management

---

## 🎯 Current Sprint: Post-Claude-Code-Review Cleanup

### ✅ DONE: Chunk 1 (Quick Wins)
- Created `requirements.txt`
- Verified tests pass (24/24)
- Fixed silent reviewer skipping (red errors)
- Removed hardcoded paths

### ✅ DONE: Chunk 2 (Defensive Programming)
- Added retry logic (3x exponential backoff)
- Better error messages

### ✅ DONE: Chunk 3 (Clean up & Stability)
- Archived TODO.md brain dump → `Documents/archives/planning-notes-dec-2025.md`
- Archived historical planning docs
- Cleaned up root directory
- Fixed OpenAI retry logic
- Simplified over-engineered templates
- Standardized code review result naming (`CODE_REVIEW_ALL_CAPS`)
- Enforced Definition of Done (DoD) in CLI requests
- Created `templates/CODE_REVIEW.md.template`
- Documented `patterns/code-review-standard.md`
- Established **YAML SSOT Pattern** for data management
- Transitioned `EXTERNAL_RESOURCES.yaml` as the source of truth

### ✅ DONE: Chunk 4 (Dogfood & Validate)
- [x] **Redemption Audit:** Successfully transitioned from 'NEEDS MAJOR REFACTOR' to 'Grade: A' using the Audit Assembly Line.

---

## 📋 BACKLOG - High Priority

### Cortana Investigation & Monitoring
**Goal:** Investigate why Cortana broke and set up monitoring to prevent future silent failures
**Context:** Cortana was broken from Dec 18, 2025 to Jan 10, 2026 (22 days) - undetected until manual check

- [ ] **Investigation:**
  - [ ] Determine root cause of agent_os dependency breaking Cortana
  - [ ] Review why 130 historical dates were missing (backfilled Aug 2025 - Jan 2026)
  - [ ] Document findings in Cortana project

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
- Created Cortana's own venv and .env (no agent_os dependency)
- Fixed Wispr Flow timestamp parsing (trailing space issue)
- Backfilled all 130 missing dates

---

### Ollama MCP Enhancement: Smart Local Routing ✅ COMPLETE (Jan 10, 2026)
**Goal:** Intelligent task routing + structural escalation enforcement
**Project:** ollama-mcp (TypeScript)
**Related:** Ported best features from AI Router (`_tools/ai_router`)

- [x] **Phase 1: Basic Smart Routing**
  - [x] Add `task_type` parameter (classification, extraction, code, reasoning, file_mod)
  - [x] Implement default fallback chains per task type (config/routing.yaml)
  - [x] Add `models_tried` to response metadata
  - [x] Add `escalate: true` when all local models fail

- [x] **Phase 2: Response Quality Detection**
  - [x] Port `isGoodResponse()` from AI Router
  - [x] Auto-retry on poor response (too short, refusal)

- [x] **Phase 3: Telemetry Trigger + Learned Routing**
  - [x] Telemetry review trigger (30 days + 50 runs = auto-reminder)
  - [x] Analysis script for success rate tracking
  - [x] Route adjustment based on historical performance (manual review)

**Verified via:** `ollama-mcp/Documents/planning/SMART_ROUTING_PROMPTS_INDEX.md` (6 prompts)

**Next:** AI Router can be archived - its features are now in Ollama MCP

---

### Pre-Commit Hook ✅ COMPLETE (Jan 10, 2026)
**Goal:** Prevent "over-caffeinated" agents from committing DNA defects

- [x] Create .git/hooks/pre-commit script
- [x] Script runs: `python scripts/warden_audit.py --root . --fast`
- [x] Block commit if warden finds issues (exit code 1)
- [x] --no-verify flag works for emergency commits (built into git)
- [x] Tested: blocks commits with P0 violations

**Implemented by:** Worker (qwen3:14b) via Floor Manager
**Learning Loop Pattern Test:** ✅ SUCCESS - First task using new prompt template structure

---

### Code Review System Integration (CRITICAL - Not Urgent)
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

### Security & Testing (Jan 2026 - Web-Claude Feedback)

#### ✅ DONE: Quick Wins - Security Test Suite
- [x] Created `tests/test_security.py` with adversarial tests
- [x] Hardened `archive_reviews.py` with validation
- [x] Completed Jan 8, 2026

#### Document SCAR TISSUE SLA
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

### Harden Cursor Rules (Original High Priority)
**Goal:** Add "Trash, Don't Delete" safety rule to all projects

- [ ] Update .cursorrules.template in scaffolding
- [ ] Retroactively apply to existing 30+ projects (use Global Rules Injection script)

**Note:** This will be executed via the Global Rules Injection script after planning + approval

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
