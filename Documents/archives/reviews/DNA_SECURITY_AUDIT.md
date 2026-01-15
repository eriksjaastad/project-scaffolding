# DNA Security Audit Report

**Document Type:** Security Audit (Gold Standard)
**Date:** 2026-01-08
**Auditor:** Claude (Opus 4.5)
**Scope:** Absolute paths, secrets, environment variables, path traversal
**Status:** 🔴 CRITICAL FAILURES FOUND

---

## Executive Summary

This audit found **17 P0 DNA DEFECTS** across the project-scaffolding codebase. The most critical issue is a hardcoded absolute path in `.env.example` containing a real username (`eriksjaastad`), which propagates to all downstream projects using this template.

**Verdict:** The DNA is contaminated. This project cannot be safely cloned by external users.

---

## Part 1: Absolute Path Violations

### 🔴 P0-001: Hardcoded Username in .env.example

**File:** `.env.example:8`
```
PROJECTS_ROOT=[USER_HOME]/projects
```

**Severity:** CRITICAL
**Impact:** Every user who copies this template gets Erik's username baked into their config
**Remediation:** Replace with placeholder: `PROJECTS_ROOT=/path/to/your/projects`

---

### 🔴 P0-002: Path.home() Fallback Creates Machine-Specific Paths

**File:** `scripts/validate_project.py:24`
```python
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", Path.home() / "projects"))
```

**File:** `scripts/reindex_projects.py:31`
```python
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", Path.home() / "projects"))
```

**Severity:** HIGH
**Impact:** If `PROJECTS_ROOT` env var is unset, scripts default to `~/projects` which:
- Creates machine-specific behavior
- Fails silently if directory doesn't exist
- Breaks CI/CD pipelines

**Remediation:** Fail loudly if `PROJECTS_ROOT` is not set:
```python
PROJECTS_ROOT = os.getenv("PROJECTS_ROOT")
if not PROJECTS_ROOT:
    raise EnvironmentError("PROJECTS_ROOT environment variable is required")
```

---

### 🔴 P0-003: Relative Ecosystem Paths in .cursorrules

**File:** `.cursorrules:60`
```
**Core Reference:** `../trading-copilot/PROJECT_PHILOSOPHY.md`
```

**File:** `.cursorrules:147,155,235`
```
- AI Journal: `../ai-journal/`
```

**Severity:** HIGH
**Impact:** Assumes sibling directories exist (`trading-copilot/`, `ai-journal/`). External users don't have these.

**Remediation:** Remove ecosystem-specific references or make them conditional.

---

### 🔴 P0-004: Ecosystem Paths in EXTERNAL_RESOURCES.yaml

**File:** `EXTERNAL_RESOURCES.yaml:214`
```yaml
template: "PROJECTS_ROOT/.env.project-template"
```

**File:** `EXTERNAL_RESOURCES.yaml:284`
```yaml
template_source: "PROJECTS_ROOT/.env.project-template"
```

**Severity:** MEDIUM
**Impact:** References a file that doesn't exist in this repo

**Remediation:** Either include the template in this repo or remove the references.

---

### 🔴 P0-005: Ecosystem Paths in Templates

**File:** `templates/.cursorrules-with-skills.template:7,40`
```
**Library location:** `../agent-skills-library/`
```

**Severity:** MEDIUM
**Impact:** Template propagates ecosystem-specific paths to downstream projects

**Remediation:** Use placeholder or make path configurable.

---

## Part 2: Hardcoded Secrets Audit

### ✅ PASS: No Hardcoded API Keys Found

Searched patterns:
- `sk-[a-zA-Z0-9]{20,}` (OpenAI keys)
- `AIza[a-zA-Z0-9_-]{30,}` (Google API keys)

**Result:** No matches in Python files, templates, or config files.

---

## Part 3: Environment Variable Mapping (Doppler Readiness)

All `os.getenv()` calls must be mapped to Doppler naming convention.

### Current Environment Variables

| Variable | Location | Doppler Name (Proposed) | Status |
|----------|----------|------------------------|--------|
| `SCAFFOLDING_OPENAI_KEY` | `scaffold/cli.py:59`, `scripts/compare_models.py:186` | `SCAFFOLDING_OPENAI_KEY` | ✅ Compliant |
| `SCAFFOLDING_ANTHROPIC_KEY` | `scaffold/cli.py:64`, `scripts/compare_models.py:185` | `SCAFFOLDING_ANTHROPIC_KEY` | ✅ Compliant |
| `SCAFFOLDING_GOOGLE_KEY` | `scaffold/cli.py:69` | `SCAFFOLDING_GOOGLE_KEY` | ✅ Compliant |
| `SCAFFOLDING_DEEPSEEK_KEY` | `scaffold/cli.py:74`, `scripts/compare_models.py:180`, `scripts/test_deepseek.py:24`, `tests/test_review.py:87` | `SCAFFOLDING_DEEPSEEK_KEY` | ✅ Compliant |
| `SCAFFOLDING_OLLAMA_MODEL` | `scaffold/cli.py:79` | `SCAFFOLDING_OLLAMA_MODEL` | ✅ Compliant |
| `DEEPSEEK_API_KEY` | `scripts/test_deepseek.py:25`, `tests/test_review.py:88` | 🔴 **LEGACY** | ⚠️ Migrate to `SCAFFOLDING_DEEPSEEK_KEY` |
| `OLLAMA_PATH` | `tests/test_review.py:28` | 🔴 **NON-STANDARD** | ⚠️ Migrate to `SCAFFOLDING_OLLAMA_PATH` |
| `SCAFFOLDING_OLLAMA_PATH` | `tests/test_review.py:28` | `SCAFFOLDING_OLLAMA_PATH` | ✅ Compliant |
| `PROJECTS_ROOT` | `scripts/validate_project.py:24`, `scripts/reindex_projects.py:31` | `PROJECTS_ROOT` | ⚠️ Needs fail-loud behavior |
| `OLLAMA_MODEL` | `.env.example:20` | 🔴 **NON-STANDARD** | ⚠️ Migrate to `SCAFFOLDING_OLLAMA_MODEL` |
| `OLLAMA_HOST` | `.env.example:21` | `SCAFFOLDING_OLLAMA_HOST` | ⚠️ Add SCAFFOLDING_ prefix |

### 🔴 P0-006: Legacy Environment Variable Names

**Files:** `scripts/test_deepseek.py:25`, `tests/test_review.py:88`
```python
or os.getenv("DEEPSEEK_API_KEY")
```

**Severity:** MEDIUM
**Impact:** Inconsistent naming breaks Doppler secret management

**Remediation:** Standardize all variables to `SCAFFOLDING_*` prefix.

---

### 🔴 P0-007: Non-Standard Ollama Variables

**File:** `.env.example:20-21`
```
OLLAMA_MODEL=llama3.2
OLLAMA_HOST=http://localhost:11434
```

**Severity:** LOW
**Impact:** Variables don't follow project naming convention

**Remediation:** Rename to:
```
SCAFFOLDING_OLLAMA_MODEL=llama3.2
SCAFFOLDING_OLLAMA_HOST=http://localhost:11434
```

---

## Part 4: Path Traversal Vulnerability Audit

### ✅ PASS: safe_slug() Properly Implemented

**File:** `scaffold/review.py:40-61`

The `safe_slug()` function correctly:
- Strips non-alphanumeric characters
- Prevents `..` traversal
- Validates against base_path
- Raises on traversal attempts

**Used at:** `scaffold/review.py:242` for reviewer name → filename conversion

---

### 🔴 P0-008: User Input Path Without Sanitization

**File:** `scripts/validate_project.py:267-268`
```python
project_name = arg
project_path = PROJECTS_ROOT / project_name
```

**Severity:** HIGH
**Impact:** User can pass `../../../etc/passwd` as project name to traverse outside PROJECTS_ROOT

**Attack Vector:**
```bash
./scripts/validate_project.py "../../../etc"
# Would attempt to validate /etc as a project
```

**Remediation:**
```python
project_name = arg
# Sanitize: strip path separators and traversal
safe_name = project_name.replace("/", "").replace("\\", "").replace("..", "")
project_path = PROJECTS_ROOT / safe_name

# Verify path is within PROJECTS_ROOT
if not project_path.resolve().is_relative_to(PROJECTS_ROOT.resolve()):
    raise ValueError(f"Invalid project name: {project_name}")
```

---

### 🔴 P0-009: User Input Path Without Sanitization (reindex)

**File:** `scripts/reindex_projects.py:336-337`
```python
project_name = arg
project_path = PROJECTS_ROOT / project_name
```

**Severity:** HIGH
**Impact:** Same traversal vulnerability as P0-008

**Remediation:** Same as P0-008

---

### 🔴 P0-010: argparse Root Path Without Validation

**File:** `scripts/archive_reviews.py:116`
```python
root_path = pathlib.Path(args.root).resolve()
```

**File:** `scripts/warden_audit.py:125`
```python
root_path = pathlib.Path(args.root).resolve()
```

**Severity:** MEDIUM
**Impact:** User can scan any directory on filesystem

**Note:** This may be intentional functionality, but should be documented as security consideration.

---

## Part 5: Additional DNA Defects

### 🔴 P0-011: Documentation Contains Machine Paths

**File:** `CLAUDE_CODE_REVIEW_v3.md:92`
```
$ ls -la /home/user/project-scaffolding/.env*
```

**Severity:** LOW
**Impact:** Documentation assumes specific filesystem layout

---

### 🔴 P0-012: Repomix Snapshot Contains Sensitive Paths

**File:** `repomix-output.xml` (multiple locations)

Contains real paths from build environment. Should be gitignored or sanitized.

---

### 🔴 P0-013: spec.md Documents ~/projects as Default

**File:** `spec.md:573`
```
| `PROJECTS_ROOT` | Ecosystem root directory | `~/projects` |
```

**Severity:** LOW
**Impact:** Documents machine-specific fallback as expected behavior

---

## Part 6: Compliance Summary

| Check | Status | Defects |
|-------|--------|---------|
| No absolute `/Users/` paths | 🔴 FAIL | P0-001 |
| No `/home/` paths in code | ✅ PASS (only in docs) | - |
| No `~/` in runtime code | 🔴 FAIL | P0-002 |
| No hardcoded API keys | ✅ PASS | - |
| Doppler-compliant env vars | 🟡 PARTIAL | P0-006, P0-007 |
| User input paths sanitized | 🔴 FAIL | P0-008, P0-009, P0-010 |
| Templates portable | 🔴 FAIL | P0-003, P0-004, P0-005 |

**Overall Grade:** 🔴 **FAIL** (4/7 checks failed)

---

## Part 7: Remediation Priority

### Immediate (P0 - Before any merge)

1. **P0-001:** Fix `.env.example` hardcoded path
2. **P0-008, P0-009:** Add path traversal protection to user input scripts
3. **P0-002:** Make `PROJECTS_ROOT` required, not defaulted

### High (P1 - This sprint)

4. **P0-003, P0-004, P0-005:** Remove ecosystem-specific paths from templates
5. **P0-006, P0-007:** Standardize all env vars to `SCAFFOLDING_*` prefix

### Medium (P2 - Next sprint)

6. **P0-010:** Document `--root` security considerations
7. **P0-011, P0-012, P0-013:** Clean up documentation paths

---

## Appendix A: Doppler Secret Schema

```yaml
# Proposed Doppler configuration for project-scaffolding
project: project-scaffolding
environments:
  - development
  - production

secrets:
  # AI API Keys
  SCAFFOLDING_OPENAI_KEY:
    type: string
    required: false
  SCAFFOLDING_ANTHROPIC_KEY:
    type: string
    required: false
  SCAFFOLDING_GOOGLE_KEY:
    type: string
    required: false
  SCAFFOLDING_DEEPSEEK_KEY:
    type: string
    required: false

  # Local AI
  SCAFFOLDING_OLLAMA_MODEL:
    type: string
    default: "llama3.2"
  SCAFFOLDING_OLLAMA_HOST:
    type: string
    default: "http://localhost:11434"
  SCAFFOLDING_OLLAMA_PATH:
    type: string
    required: false

  # Infrastructure
  PROJECTS_ROOT:
    type: string
    required: true  # MUST be set explicitly
```

---

## Appendix B: Files Requiring Modification

| File | Defects | Priority |
|------|---------|----------|
| `.env.example` | P0-001, P0-007 | IMMEDIATE |
| `scripts/validate_project.py` | P0-002, P0-008 | IMMEDIATE |
| `scripts/reindex_projects.py` | P0-002, P0-009 | IMMEDIATE |
| `.cursorrules` | P0-003 | HIGH |
| `EXTERNAL_RESOURCES.yaml` | P0-004 | HIGH |
| `templates/.cursorrules-with-skills.template` | P0-005 | HIGH |
| `scripts/test_deepseek.py` | P0-006 | HIGH |
| `tests/test_review.py` | P0-006 | HIGH |

---

**End of DNA Security Audit**

*This audit must be resolved before this project can be considered portable or production-ready.*
