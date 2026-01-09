# Project Scaffolding - TODO

> **Purpose:** Current actionable tasks for project-scaffolding
> **Last Updated:** January 8, 2026
> **Type:** Infrastructure

---

## 🌙 TONIGHT'S WORK (Jan 8, 2026) - VERIFY BEFORE COMMIT

**What we did:**
1. ✅ Fixed test indentation bug (tests/test_scripts_follow_standards.py)
2. ✅ Created adversarial test suite (tests/test_security.py - 358 lines)
3. ✅ Hardened archive_reviews.py with security validation
4. ✅ Migrated docs/ → Documents/ (126 replacements across 50+ files)
5. ✅ Removed Kiro references, updated to Gemini Super/Floor + DeepSeek + Ollama
6. ✅ Archived reviews/ directory to proper location
7. ✅ Added detailed Options 2-4 to TODO (Warden continuous, SCAR TISSUE SLA, Coverage/Fuzzing)

**VERIFY BEFORE COMMIT (5 minutes):**
```bash
# 1. Activate venv
source venv/bin/activate

# 2. Test imports work
python -c "from scaffold.review import safe_slug; print('✓ Import:', safe_slug('../../etc/passwd'))"
# Should print: ✓ Import: etc_passwd

# 3. Run new security tests
pytest tests/test_security.py::TestPathTraversal -v
# Should show 3 passing tests

# 4. If both work, commit everything:
git add -A
git commit -m "security: implement adversarial test suite and harden archive_reviews

- Add tests/test_security.py with 10 test classes for dark territory
- Harden archive_reviews.py with validation for excluded dirs
- Fix test indentation bug in test_scripts_follow_standards.py
- Migrate all docs/ references to Documents/ (126 replacements)
- Remove Kiro references, update AI strategy
- Archive reviews/ to Documents/archives/reviews/jan-2026-rounds/
- Add detailed TODO items for Options 2-4

Based on web-Claude feedback. Grade: A- → A (mission-critical ready)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**If tests fail:** Don't panic. Read the error, fix it, commit. The code structure is sound.

**What changed:** 58 files (+291, -1566 lines). Mostly cleanups and the new security suite.

---

## ✅ What Exists & Works

**Templates:**
- `CLAUDE.md.template`
- `CLAUDE.md` (Project standard) ✅ NEW (Dec 30)
- `CODE_REVIEW.md.template` ✅ NEW (Dec 30)
- `.cursorrules.template`
- `Documents/` structure
- `TIERED_SPRINT_PLANNER.md`
- `TODO.md.template` ✅ NEW (Dec 30)

**Standards:**
- `TODO_FORMAT_STANDARD.md` (650 lines) ✅ NEW (Dec 30)
- `PROJECT_STRUCTURE_STANDARDS.md` (comprehensive) ✅ NEW (Dec 30)

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

### ⏭️ NEXT: Chunk 4 (Dogfood & Validate)
- [x] **Redemption Audit:** Successfully transitioned from 'NEEDS MAJOR REFACTOR' to 'Grade: A' using the Audit Assembly Line.
- [ ] **Review Migration:** Confirm `archive_reviews.py` handles project-root detection correctly (using `00_Index` files).
- [ ] **Safety Audit:** Ensure all scripts use `send2trash` instead of `os.remove`.
- [ ] Build **The Warden**: Start implementation of `scripts/warden_audit.py` to enforce Tiered Scaffolding rules.
  - [ ] Tier 1 (Code): requirements.txt, tests/, review history.
  - [ ] Tier 2 (Writing): Exempt from tech audits, must have Indexes.
- [ ] **Global Rules Injection:** Draft script to push "Trash, Don't Delete" and "No Silent Failures" to all 30+ project `.cursorrules`.
- [ ] **Ecosystem Rollout:** Execute the Audit Assembly Line (V1.3) across the Alphabetical Queue.

---

## 📚 Pattern Management

**System:** See `Documents/PATTERN_MANAGEMENT.md` for full details
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

## 📋 Backlog (After Chunk 4)

### 🔴 CRITICAL - Code Review System (NEW - Dec 30)

**Goal:** Standardize code review process across all projects

- [x] Create CODE_REVIEW.md.template
- [x] Define standard code review format:
  - [x] Review request info (date, author, purpose)
  - [x] Review checklist (Definition of Done)
  - [x] Reviewer notes and feedback
  - [x] Standard result naming (`CODE_REVIEW_ALL_CAPS`)
- [ ] Add to PROJECT_STRUCTURE_STANDARDS.md
- [ ] Document in PROJECT_KICKOFF_GUIDE.md
- [ ] Integrate with TODO.md format:
  - [ ] Add syntax: `- [ ] Task **[IN REVIEW]** - See CODE_REVIEW.md #123`
  - [ ] Update TODO_FORMAT_STANDARD.md
  - [ ] Update TODO.md.template
- [ ] Create examples from real code reviews
- [ ] Test with project-tracker (dogfood it!)

**Why this matters:**
- Project-tracker dashboard will display pending code reviews
- Alerts table will show code review status
- Need standard format to parse and display

---

### High Priority

#### Security & Testing (Jan 2026 - Web-Claude Feedback)
- [x] **Quick Wins - Security Test Suite:** Created `tests/test_security.py` with adversarial tests for path traversal, file size limits, concurrent operations, and edge cases. Hardened `archive_reviews.py` with validation for excluded dirs and malicious filenames. (Jan 8, 2026)

- [ ] **Make Warden Continuous (Option 2 from review):**
  **Context:** Prevent "over-caffeinated" agents from committing DNA defects.
  **Task:** Set up a lightweight git pre-commit hook that runs a fast-scan version of Warden.
  **Design:** The hook should be grep-based and take < 1 second.
  **Integration:** Findings should also be surfaced to the `project-tracker` dashboard.
  **Steps:**
  1. Create `.git/hooks/pre-commit` script that runs `python scripts/warden_audit.py --root . --fast`
  2. If Warden finds issues (exit code 1), block the commit and show errors.
  3. Add `--skip-warden` flag for emergency manual commits.
  4. Test by having an agent try to commit a file with a `/Users/` path.

- [ ] **Document SCAR TISSUE SLA (Option 3 from review):**
  **Context:** Web-Claude praised the "scar tissue SLA" - turning every defect into a checklist within 24 hours. Need to formalize this as a documented standard.
  **Task:** Add "Critical Rule #7: SCAR TISSUE SLA" to CODE_QUALITY_STANDARDS.md
  **Content to add:**
  ```markdown
  ## 🚨 Critical Rule #7: SCAR TISSUE SLA

  ### The Rule
  Within 24 hours of discovering a defect, add:
  1. Test case that would have caught it (in tests/)
  2. Entry in CODE_REVIEW_ANTI_PATTERNS.md with the scar story
  3. Checklist item in validation script (warden_audit.py or validate_project.py)

  ### Why This Exists
  Every bug is an opportunity to make the system smarter. Missing this window means the lesson fades and the defect repeats. This is how institutional memory compounds in a solo workflow.

  ### Example (Jan 8, 2026)
  **Defect:** Test indentation bug in test_scripts_follow_standards.py
  **SLA Response:**
  - [x] Fixed bug same day (tests/test_scripts_follow_standards.py:62-63)
  - [x] Added adversarial test: test_security.py::test_indentation_validation
  - [ ] Document: Anti-pattern #23 "Loop variable scope confusion"
  - [ ] Add to pre-commit: AST check for common indentation errors

  ### Accountability
  If you find yourself skipping this SLA, that's a signal the defect wasn't real or the system is over-constrained. Trust your judgment but document why you skipped it.
  ```
  **Also add:** Documents/TESTING_PHILOSOPHY.md explaining inverse testing (test what can go WRONG)
  **Time estimate:** 20 minutes

- [ ] **Coverage Reporting & Fuzzing (Option 4 extras):**
  **Context:** Tests exist but no visibility into what's NOT tested. Need coverage metrics and fuzzing.
  **Tasks:**
  1. **Coverage setup:**
     ```bash
     pip install pytest-cov
     pytest --cov=scaffold --cov=scripts --cov-report=html --cov-report=term
     ```
     Target: 80% line coverage minimum, 100% for security-critical functions (safe_slug, find_project_root, save_atomic)
  2. **Add to CI:**
     - Run coverage on every test suite execution
     - Fail if coverage drops below 75%
     - Generate HTML report in `.coverage_html/` (add to .gitignore)
  3. **Fuzzing Lite for file operations:**
     Create `tests/test_fuzzing.py`:
     - Random filenames: valid unicode, emojis, null bytes, max length (255 chars), path traversal attempts
     - Random file sizes: 0 bytes, 1 byte, 500KB (just under limit), 501KB (just over), 1GB
     - Symlinks: valid, broken, circular, pointing to excluded dirs
     - Concurrent operations: 10 threads writing same file with save_atomic()
  **Time estimate:** 90 minutes
  **Success:** Coverage report shows 80%+, fuzzing finds no crashes

#### Original High Priority Items
- [ ] **Harden Cursor Rules:** Add "Trash, Don't Delete" safety rule to all project `.cursorrules`.
  - [ ] Update `.cursorrules.template` in scaffolding.
  - [ ] Retroactively apply to existing 30+ projects.
- [ ] Add cost tracking log (`logs/cost-tracking.jsonl`)
- [ ] Validate pricing against real bills (monthly)

### Medium Priority
- [ ] **Ecosystem Resilience:** Integrate disaster recovery templates, project lifecycle scripts, and the backup system into the scaffolding as default components.
- [ ] Prompt versioning system
- [ ] AWS Activate research (Q2 2026)
- [ ] Google Cloud credits (Q2 2026)

### Low Priority
- [ ] Task dispatch system (only if manual tiering becomes painful)
- [ ] Multi-AI build automation (only after 3+ projects prove manual works)

---

## 🗑️ Deleted/Archived

**Archived (Documents/archives/):**
- Original 1353-line TODO (brain dump)
- Historical planning docs (Option C build plan, system walkthrough, etc.)

**Reason:** Claude Code review identified "documentation about automation" not "automation"

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

**Archive:** See `Documents/archives/planning-notes-dec-2025.md` for historical brain dumps
