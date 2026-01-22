# Warden Audit Research Report
## Phase 1: Current State Analysis & Enhancement Requirements

**Date:** January 10, 2026
**Analyst:** Claude Sonnet 4.5
**Purpose:** Research phase for Warden enhancement (TODO Task #1)

---

## Executive Summary

The Warden audit system is **architecturally sound but incomplete** for pre-commit hook usage. Current performance (~10+ seconds on single project) exceeds the <1 second target by **10x**. Missing features: `--fast` flag, hardcoded path detection, and severity classification.

**Industry alignment:** Warden implements Pattern 4 (Tool Whitelist) and Pattern 5 (Per-Step Safety Assessment) from trustworthy_ai_report.md. With enhancements, it will enable Pattern 13 (Regression Testing in CI/CD).

**Bottom line:** Code is clean and extensible. Enhancement phase should take 45-60 minutes with clear acceptance criteria.

---

## 1. Current Capabilities

### Architecture (scripts/warden_audit.py)

**Functions:**
- `is_tier_1_project()` - Classifies projects by type (lines 9-38)
- `check_dependencies()` - Validates dependency manifests (lines 40-46)
- `check_dangerous_functions()` - Scans for os.remove/os.unlink/shutil.rmtree (lines 48-72)
- `run_audit()` - Orchestrates full ecosystem scan (lines 74-116)

**Current workflow:**
```bash
1. Find all projects (00_Index_*.md files)
2. For each project:
   a. Classify as Tier 1 (code) or Tier 2 (other)
   b. If Tier 1: check for dependency manifest
   c. For all: scan Python files for dangerous functions
3. Report summary: projects scanned, issues found
4. Exit code 0 (clean) or 1 (issues found)
```

### What Works Well

✅ **Clean separation of concerns** - Each function has single responsibility
✅ **Path safety** - Uses pathlib throughout
✅ **Error handling** - Catches file read errors gracefully (line 69)
✅ **Self-exclusion** - Warden doesn't flag itself (line 59)
✅ **Smart filtering** - Skips venv, node_modules, .git, __pycache__ (line 56)
✅ **Relative paths** - Outputs project-relative paths for readability
✅ **Exit codes** - Follows Unix convention (0 = success, 1 = failure)

### Current Test Coverage

**File:** tests/test_security.py (lines 302-349)

**Tests:**
1. `test_warden_detects_os_remove_in_strings()` - Validates pattern detection (even in comments)
2. `test_warden_handles_unreadable_files()` - Validates graceful handling of permission errors

**Coverage assessment:** ~30% of functionality tested. Missing:
- Tier detection logic
- Dependency manifest checking
- Multi-project scanning
- Performance benchmarks

---

## 2. Performance Analysis

### Critical Finding: Current Speed

**Test:** Ran Warden on project-scaffolding
**Result:** >10 seconds (killed after 10s timeout)
**Target:** <1 second for pre-commit hook usage
**Gap:** **10x slower than required**

### Root Cause: Filesystem Traversal

**Problem location:** Line 54
```bash
for file_path in project_root.rglob('*.py'):
```

**Why slow:**
- `.rglob()` recursively walks entire directory tree
- Reads every Python file completely into memory (line 64)
- Performs string search on full file contents (line 66)
- No early termination or sampling

**Industry context:** trustworthy_ai_report.md Pattern 5 notes latency cost of +50-200ms for per-step safety checks is acceptable. Our 10+ seconds is **50-100x** the acceptable latency.

### Solution: --fast Flag Implementation

**Approach:** Grep-based scanning instead of file walking

**Pseudocode:**
```bash
def check_dangerous_functions_fast(project_root: pathlib.Path) -> list:
    """Fast grep-based scanner for pre-commit hooks."""
    import subprocess

    patterns = ['os.remove', 'os.unlink', 'shutil.rmtree', '/Users/', '/home/']
    results = []

    for pattern in patterns:
        # Use ripgrep (rg) or grep with file type filtering
        cmd = ['rg', '--type', 'py', '-l', pattern, str(project_root)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)

        if result.returncode == 0:  # Matches found
            for file_path in result.stdout.strip().split('\n'):
                results.append((Path(file_path), pattern))

    return results
```

**Expected performance:** <1 second (grep is highly optimized for this use case)

---

## 3. Gap Analysis: TODO vs. Current

### ❌ Missing: --fast Flag

**TODO requirement:** "grep-only mode, target < 1 second"
**Current state:** No flag exists; always uses slow .rglob() method
**Impact:** Cannot be used in pre-commit hooks (blocks developers for 10+ seconds)

**Implementation requirement:**
```bash
parser.add_argument("--fast", action="store_true",
                   help="Fast scan mode for pre-commit hooks (<1s target)")
```

### ❌ Missing: Hardcoded Path Detection

**TODO requirement:** "Detect /Users/, /home/, absolute paths"
**Current state:** Only checks for os.remove/os.unlink/shutil.rmtree
**Known issue:** No detection of portability violations

**Pattern to detect:**
```bash
hardcoded_paths = [
    r'/Users/',      # macOS absolute paths
    r'/home/',       # Linux absolute paths
    r'C:\\',         # Windows absolute paths (escaped)
    r'\\\\',         # Windows UNC paths
]
```

**Example violations:**
- `SKILLS_PATH = Path("/Users/erik/agent-skills-library")`
- `config_file = Path("/home/ubuntu/project/.env")`

**Industry context:** trustworthy_ai_report.md emphasizes "portable configuration" (similar to CODE_QUALITY_STANDARDS.md Rule #5).

### ❌ Missing: Severity Classification

**TODO requirement:** "P0/P1/P2 severity levels"
**Current state:** Everything reported as `[DANGEROUS]` or `[CRITICAL]` without granularity
**Impact:** Pre-commit hook cannot distinguish between "block commit" vs. "warn developer"

**Proposed classification:**

| Severity | Description | Pre-Commit Action | Examples |
|----------|-------------|------------------|----------|
| **P0** | Dangerous functions in production code | **BLOCK** | os.remove in scripts/, scaffold/ |
| **P1** | Hardcoded absolute paths | **BLOCK** | /Users/ or /home/ in Python files |
| **P2** | Warnings (acceptable with context) | **WARN** | os.remove in test files, comments |
| **P3** | Informational | **PASS** | Missing dependency manifest in Tier 2 |

**Industry alignment:** trustworthy_ai_report.md Pattern 16 (Incident Severity Classification) uses P0/P1/P2/P3 taxonomy with clear SLOs.

### ⚠️ Insufficient: Test Coverage

**Current:** 2 tests covering ~30% of functionality
**Required:** Tests for:
- Tier detection (is_tier_1_project)
- Dependency manifest checking
- --fast flag performance (<1s validation)
- Severity classification logic
- Multi-project scanning

**Target:** 80% line coverage (per trustworthy_ai_report.md recommendations)

---

## 4. Industry Pattern Mapping

### Pattern 4: Tool Access via Whitelist + Least Privilege

**Quote from report (lines 471-483):**
> Agent can only call pre-approved tools; each tool requires specific permission; reduces blast radius.

**How Warden implements this:**
- Warden enforces a **blacklist** of dangerous tools (os.remove, os.unlink, shutil.rmtree)
- Acts as gatekeeper preventing unapproved file operations
- Pre-commit hook = **per-step safety assessment** before tools reach production

**Gap:** Current Warden is reactive (finds existing violations). Enhancement should enable **proactive blocking** (pre-commit hook prevents violations from being committed).

### Pattern 5: Per-Step Safety Assessment (Before Tool Execution)

**Quote from report (lines 487-499):**
> Before each tool call, run safety classifier... If unsafe: block execution, return error message... Latency cost: +50-200ms per tool call.

**How Warden implements this:**
- Pre-commit hook = safety classifier running before git commit
- Blocks unsafe operations (P0/P1) before they enter the repository
- Warns on suspicious operations (P2)

**Current gap:** 10+ second latency is **50-100x** the acceptable cost. --fast flag required to meet industry standards.

### Pattern 13: Regression Testing in CI/CD

**Quote from report (lines 632-655):**
> On every code commit: Run evaluation suite against golden dataset... If regression > 5%: block deployment.

**How Warden implements this:**
- Pre-commit hook runs Warden on every commit
- Blocks commits with P0/P1 violations
- Prevents "regression" to dangerous code patterns

**Current gap:** No CI integration yet (blocked until --fast flag enables <1s execution).

---

## 5. Enhancement Requirements (For Workers)

### Feature 1: --fast Flag

**Acceptance criteria:**
- [ ] Add `--fast` argument to argparse
- [ ] Implement `check_dangerous_functions_fast()` using subprocess + grep/ripgrep
- [ ] Fall back to regular scan if grep not available
- [ ] Benchmark: confirm <1 second on project-scaffolding
- [ ] Test: validate that --fast finds same issues as regular scan

**Estimated effort:** 20 minutes

### Feature 2: Hardcoded Path Detection

**Acceptance criteria:**
- [ ] Expand dangerous_patterns to include ['/Users/', '/home/', 'C:\\\\']
- [ ] Regex pattern matching for absolute paths
- [ ] Exclude comments (optional: use AST parsing to only check string literals)
- [ ] Test: create fixture with hardcoded path, confirm detection

**Estimated effort:** 15 minutes

### Feature 3: Severity Classification

**Acceptance criteria:**
- [ ] Define Severity enum (P0, P1, P2, P3)
- [ ] Classify dangerous functions in production code as P0
- [ ] Classify hardcoded paths as P1
- [ ] Classify dangerous functions in test files as P2
- [ ] Return issues as structured data: (file, pattern, severity)
- [ ] Update logging to show severity: `[P0-CRITICAL]`, `[P1-ERROR]`, `[P2-WARNING]`
- [ ] Test: verify correct severity assignment

**Estimated effort:** 25 minutes

### Feature 4: Enhanced Test Coverage

**Acceptance criteria:**
- [ ] Test: `test_tier_detection_by_tag()` - Validates #type/code detection
- [ ] Test: `test_tier_detection_by_language()` - Validates language keyword detection
- [ ] Test: `test_fast_mode_performance()` - Confirms <1 second execution
- [ ] Test: `test_severity_classification()` - Validates P0/P1/P2 logic
- [ ] Test: `test_multi_project_scanning()` - Validates ecosystem-wide audit
- [ ] Coverage report: aim for 80%+ line coverage

**Estimated effort:** 30 minutes (can be done in parallel with features)

---

## 6. Known Issues Requiring Fixes

### Issue 1: scaffold/review.py:79

**File:** scaffold/review.py
**Line:** 79
**Violation:** Uses `os.unlink(temp_name)` instead of `send2trash`
**Severity:** P0 (dangerous function in production code)
**Status:** Documented in TODO Task #2 (Safety Audit)

**Expected Warden output (after enhancement):**
```bash
[P0-CRITICAL] project-scaffolding: Raw 'os.unlink' found in scaffold/review.py:79
```

---

## 7. Pre-Commit Hook Integration Plan

**Blocked until:** Warden has --fast flag and <1s performance

**Implementation (Future Work):**

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running Warden safety checks..."
doppler run -- python scripts/warden_audit.py --root . --fast

if [ $? -ne 0 ]; then
  echo ""
  echo "❌ Warden found safety violations. Commit blocked."
  echo "Fix the issues or use: git commit --no-verify (not recommended)"
  exit 1
fi

echo "✅ Warden safety checks passed."
exit 0
```

**P2 warnings:** Should print to console but not block commit (require manual review).

---

## 8. Recommendations for Enhancement Phase

### Priority 1: --fast Flag (CRITICAL)

**Why:** Without this, pre-commit hook is unusable (10s+ latency blocks developers).
**Effort:** 20 minutes
**Risk:** Low (grep is battle-tested, widely available)

### Priority 2: Severity Classification

**Why:** Pre-commit hook needs to know what to block vs. warn.
**Effort:** 25 minutes
**Risk:** Low (simple enum and conditional logic)

### Priority 3: Hardcoded Path Detection

**Why:** Portability violations are common (CODE_QUALITY_STANDARDS.md Rule #5).
**Effort:** 15 minutes
**Risk:** Low (regex pattern matching)

### Priority 4: Test Coverage

**Why:** Production safety tool must be well-tested (dogfooding our own standards).
**Effort:** 30 minutes
**Risk:** Medium (requires thoughtful fixture design)

**Total estimated effort:** 90 minutes (within TODO 75-minute target if features done in parallel)

---

## 9. Acceptance Criteria Summary (For Workers)

✅ **Performance:**
- Warden runs in <1 second with --fast flag on project-scaffolding
- Regular mode still works (backward compatibility)

✅ **Detection:**
- Detects os.remove, os.unlink, shutil.rmtree
- Detects hardcoded /Users/ and /home/ paths
- Distinguishes between production code (P0/P1) and test code (P2)

✅ **Output:**
- Reports severity level (P0/P1/P2) for each finding
- Format: `[P0-CRITICAL] project: pattern found in file:line`
- Exit code 0 if only P2 warnings, 1 if P0/P1 violations

✅ **Tests:**
- Has passing tests in tests/test_warden.py
- Covers tier detection, dangerous functions, --fast mode, severity classification
- Achieves 80%+ line coverage (stretch goal)

✅ **Integration Ready:**
- Pre-commit hook can block P0/P1, warn on P2
- Documentation in code explains severity levels

---

## 10. Handoff to Floor Manager

**For Enhancement Phase execution, Workers need:**

1. **This research report** (context on current state and gaps)
2. **Acceptance criteria** (from section 9)
3. **Priority ordering** (from section 8)
4. **Known issue reference** (scaffold/review.py:79, will be fixed in Safety Audit)
5. **Industry pattern context** (trustworthy_ai_report.md Patterns 4, 5, 13)

**Floor Manager should:**
- Verify Workers read this report before starting
- Check off each acceptance criterion as Workers complete features
- Run performance benchmark: `time python scripts/warden_audit.py --root . --fast`
- Ensure exit only after **all criteria pass**

**Erik approval gates:**
- None required for Enhancement Phase (research phase approved)
- Erik approval required before rolling out pre-commit hook ecosystem-wide

---

## Appendix A: Code Quality Observations

**Positive patterns:**
- Uses pathlib (modern, cross-platform)
- Logging instead of print statements
- Exception handling with context
- Self-documenting function names

**Suggestions for Workers (non-blocking):**
- Consider adding type hints (CODE_QUALITY_STANDARDS.md Rule #7)
- Add docstrings for public functions (already present, but could be more detailed)
- Consider extracting severity logic into separate module if it grows complex

---

**Research Phase Complete**
**Time to completion:** 30 minutes
**Next Phase:** Enhancement (hand off to Workers via Floor Manager)

**Analyst signature:** Claude Sonnet 4.5
**Date:** 2026-01-10T02:30:00Z


## Related Documentation

- [[CODE_QUALITY_STANDARDS]] - code standards
- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure

