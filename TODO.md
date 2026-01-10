# Project Scaffolding - TODO

> **Purpose:** Current actionable tasks for project-scaffolding
> **Last Updated:** January 10, 2026
> **Type:** Infrastructure

---

## 🌙 TONIGHT'S SESSION (Jan 10, 2026)

**Cursor Usage:** 46% (Recorded Jan 10, 2026)
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

#### 3. Global Rules Injection - Planning Only
**Goal:** Design the rollout strategy (DO NOT execute tonight)
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

- [ ] **Implementation** (Next session)
  - [ ] Write update_cursorrules.py script
  - [ ] Run dry-run to verify
  - [ ] Execute canary deployment on 3 projects
  - [ ] Wait 48 hours, then full rollout

**Acceptance Criteria:**
- Script exists with --dry-run flag
- Script supports --projects flag for subset rollout
- Rollback procedure documented (restore from backups)
- 3 test projects identified (10% canary)
- 24-48 hour monitoring plan defined
- Human approval received before ecosystem-wide execution

**Why This Matters:**
- Pushes safety rules to all 30+ project .cursorrules files
- High blast radius - must be carefully tested first

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

### Pre-Commit Hook (Blocked: Requires Warden Enhancement Complete)
**Goal:** Prevent "over-caffeinated" agents from committing DNA defects

- [ ] Create .git/hooks/pre-commit script
- [ ] Script runs: `python scripts/warden_audit.py --root . --fast`
- [ ] Block commit if warden finds issues (exit code 1)
- [ ] Add --skip-warden flag for emergency manual commits
- [ ] Test by attempting to commit file with /Users/ path

**Why This Matters:**
- Catches dangerous functions and hardcoded paths before they reach the repo
- Web-Claude praised this as "Option 2" in security review

**Time Estimate:** 30 minutes (after warden is ready)

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
