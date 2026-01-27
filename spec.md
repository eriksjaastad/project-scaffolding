# spec.md - Project Scaffolding System Contract

**Document Type:** System Specification (Auditor-Generated)
**Date:** 2026-01-08
**Auditor:** Claude (Opus 4.5)
**Source:** Repomix snapshot analysis
**Status:** Contract Definition (Pre-Security Review)

---

## Executive Summary

`project-scaffolding` is a **meta-project** serving as the "heart and brain" of a multi-project ecosystem. Its purpose is to extract patterns from experiments to help all projects get done quickly at the highest quality and lowest cost.

**Core Functions:**
1. **Multi-AI Review Orchestration** - Dispatch document/code reviews to multiple AI models in parallel
2. **Project Governance Utilities** - Validation, archival, indexing, and auditing of projects
3. **Template & Pattern Library** - Reusable starting points and documented best practices
4. **Cost Optimization Framework** - Tiered AI usage patterns to reduce API spending

**Tech Stack:** Python 3.11+, pytest, PyYAML, Rich, Click, Tenacity, Anthropic SDK, OpenAI SDK

---

## Part 1: System Architecture

### 1.1 Directory Structure

```bash
project-scaffolding/
├── scaffold/                    # Core library
│   ├── __init__.py              # Package definition (v0.1.0)
│   ├── cli.py                   # CLI interface (Click-based)
│   └── review.py                # Multi-AI orchestrator
│
├── scripts/                     # Utility scripts
│   ├── archive_reviews.py       # Review file archival
│   ├── validate_project.py      # Project structure validation
│   ├── reindex_projects.py      # Index file generation
│   ├── warden_audit.py          # Ecosystem audit agent
│   ├── pre_review_scan.sh       # Pre-review gatekeeper
│   ├── compare_models.py        # Model comparison utility
│   ├── test_deepseek.py         # DeepSeek integration test
│   └── validate_external_resources.py
│
├── templates/                   # Reusable templates
│   ├── Documents/               # Standard documentation structure
│   ├── AGENTS.md.template       # AI agent instructions template
│   ├── CLAUDE.md.template       # Claude-specific instructions
│   ├── 00_Index.md.template     # Project index template
│   ├── TODO.md.template         # TODO format template
│   ├── CODE_REVIEW.md.template  # Code review template
│   ├── .cursorrules.template    # Cursor IDE rules
│   └── .gitignore               # Standard gitignore
│
├── patterns/                    # Documented patterns
│   ├── tiered-ai-sprint-planning.md
│   ├── safety-systems.md
│   ├── development-philosophy.md
│   ├── api-key-management.md
│   ├── code-review-standard.md
│   └── ssot-via-yaml.md
│
├── prompts/active/              # Active review prompts
│   └── document_review/
│       ├── architecture.md
│       ├── security.md
│       └── performance.md
│
├── tests/                       # Test suite
│   ├── test_review.py           # Orchestrator tests
│   ├── test_scripts_follow_standards.py
│   └── test_smoke.py
│
├── reviews/                     # Historical review outputs
│   └── round_{N}/               # Per-round results
│
├── Documents/                   # Project documentation
│   ├── archives/                # Archived documents
│   └── march-2026-review/       # Planning documents
│
├── scaffold_cli.py              # CLI entry point
├── AGENTS.md                    # Project's own AI instructions
├── CLAUDE.md                    # Claude-specific instructions
├── EXTERNAL_RESOURCES.yaml      # Service/API tracking (SSOT)
├── REVIEWS_AND_GOVERNANCE_PROTOCOL.md
├── requirements.txt             # Pinned dependencies
└── pytest.ini                   # Test configuration
```

### 1.2 Component Dependency Graph

```bash
┌─────────────────────────────────────────────────────────────────────┐
│                           ENTRY POINTS                               │
├─────────────────────────────────────────────────────────────────────┤
│  scaffold_cli.py ─────────► scaffold/cli.py ───────► scaffold/review.py
│                                    │                        │
│  scripts/*.py ◄──────────── Independent utilities          │
│                                                              │
│                              ▼                              ▼
│                        Click CLI              ReviewOrchestrator
│                            │                        │
│                            ▼                        ▼
│                      ReviewConfig ◄──── Prompt files (.md)
│                            │
│                            ▼
│                   AsyncAnthropic / AsyncOpenAI / Ollama CLI
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Core Logic

### 2.1 Multi-AI Review Orchestrator (`scaffold/review.py`)

**Purpose:** Dispatch document/code reviews to multiple AI models in parallel, track costs, collect responses.

**Key Classes:**

| Class | Purpose | Fields |
|-------|---------|--------|
| `ReviewConfig` | Single reviewer configuration | `name`, `api`, `model`, `prompt_path` |
| `ReviewResult` | Result from one reviewer | `reviewer_name`, `api`, `model`, `content`, `cost`, `tokens_used`, `duration_seconds`, `timestamp`, `error` |
| `ReviewSummary` | Aggregated round summary | `round_number`, `document_path`, `results`, `total_cost`, `total_duration`, `timestamp` |
| `ReviewOrchestrator` | Main orchestration class | API clients (OpenAI, Anthropic, DeepSeek) |

**Supported APIs:**
- `openai` - OpenAI API via `AsyncOpenAI`
- `anthropic` - Anthropic API via `AsyncAnthropic`
- `deepseek` - DeepSeek API via OpenAI-compatible client
- `ollama` - Local Ollama CLI via subprocess
- `google` - **STUB (Not Implemented)**

**Key Functions:**

```bash
# Factory function
create_orchestrator(openai_key, anthropic_key, google_key, deepseek_key) → ReviewOrchestrator

# Main entry point
ReviewOrchestrator.run_review(document_path, configs, round_number, output_dir) → ReviewSummary

# Internal methods
_run_single_review(document, config, progress, task_id) → ReviewResult
_call_openai(model, prompt) → Dict[str, Any]  # With retry logic
_call_anthropic(model, prompt) → Dict[str, Any]  # With retry logic
_call_deepseek(model, prompt) → Dict[str, Any]  # With retry logic
_call_ollama(model, prompt) → Dict[str, Any]  # Subprocess, timeout=300s
```

**Industrial Hardening Features:**
- `safe_slug()` - Filename sanitization with path traversal prevention
- `save_atomic()` - Atomic writes using temp file + rename pattern
- File size limit: 500KB max document size
- Retry logic: 3 attempts with exponential backoff (2-10s)
- Subprocess hardening: `check=True`, `timeout=300`, `capture_output=True`

**Cost Calculation:**
- OpenAI: `$15/1M tokens` (GPT-4o), `$1.50/1M` (GPT-4o-mini)
- Anthropic: `$15/$75/1M` (Opus), `$3/$15/1M` (Sonnet), `$0.25/$1.25/1M` (Haiku)
- DeepSeek: `$0.27/1M tokens`
- Ollama: `$0` (local)

### 2.2 CLI Interface (`scaffold/cli.py`)

**Commands:**

```bash
# Main command group
scaffold --version

# Review command
scaffold review --type [document|code] --input PATH --round N [--output DIR]
                --openai-key KEY --anthropic-key KEY --google-key KEY
                --deepseek-key KEY --ollama-model MODEL
```

**Environment Variables:**
- `SCAFFOLDING_OPENAI_KEY`
- `SCAFFOLDING_ANTHROPIC_KEY`
- `SCAFFOLDING_GOOGLE_KEY`
- `SCAFFOLDING_DEEPSEEK_KEY`
- `SCAFFOLDING_OLLAMA_MODEL` (default: `llama3.2`)

**Validation:**
- Input file must contain "Definition of Done" or "DoD" section
- Prompt directory must exist (`prompts/active/{document,code}_review/`)

**Default Reviewer Mapping:**
| Prompt Prefix | API | Model | Display Name |
|--------------|-----|-------|--------------|
| `security` | deepseek | deepseek-chat | Security Reviewer |
| `performance` | deepseek | deepseek-chat | Performance Reviewer |
| `architecture` | ollama | llama3.2 | Architecture Reviewer |
| `quality` | deepseek | deepseek-chat | Code Quality Reviewer |
| (other) | openai | gpt-4o | {Prefix} Reviewer |

### 2.3 Project Validation (`scripts/validate_project.py`)

**Purpose:** Enforce project structure standards and DNA integrity.

**Mandatory Files:**
- `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursorignore`
- `TODO.md`, `README.md`, `.gitignore`

**Mandatory Directories:**
- `Documents/` (core docs at root level, NOT in a `core/` subdirectory)

**Validation Checks:**
1. Index file exists (`00_Index_*.md`)
2. Index has YAML frontmatter
3. Index has required tags (`map/project`, `p/[project-name]`)
4. Index has required sections (`## Key Components`, `## Status`)
5. Mandatory files/directories exist
6. **DNA Integrity Scan:**
   - No `/Users/` absolute paths
   - No hardcoded API keys (`sk-*`, `AIza*`)

### 2.4 Review Archival (`scripts/archive_reviews.py`)

**Purpose:** Move review files to project-specific archive directories.

**Target Files Pattern:**
- `REVIEW.md`
- `CODE_REVIEW_*.md`
- `*review*.md` (case-insensitive)

**Project Root Detection:**
- Searches for `00_Index_*.md` in parent directories (max 10 levels)

**Destination:** `{PROJECT_ROOT}/Documents/archives/reviews/`

**Safety Features:**
- Dry-run mode (`--dry-run`)
- Uses `send2trash` for conflict resolution (not `os.remove`)

### 2.5 Project Re-indexing (`scripts/reindex_projects.py`)

**Purpose:** Generate/update `00_Index_*.md` files automatically.

**Detection Logic:**
- **Primary Tech:** Count file extensions (`.py` → python, `.ts` → typescript, etc.)
- **Status:** `archived` if last modified >180 days, else `active`
- **Components:** Top 6 directories by file count

**Commands:**
```bash
doppler run -- python3 ./scripts/reindex_projects.py --missing   # Create missing indexes
doppler run -- python3 ./scripts/reindex_projects.py --stale     # Update >6 month old indexes
doppler run -- python3 ./scripts/reindex_projects.py --all       # Recreate all (requires confirmation)
doppler run -- python3 ./scripts/reindex_projects.py PROJECT     # Specific project
```

### 2.6 Ecosystem Audit (`scripts/warden_audit.py`)

**Purpose:** Crawl ecosystem and perform governance audits.

**Tier Classification:**
- **Tier 1 (Code):** Has `#type/code` or `#type/project` tag, or tech language in header
- **Tier 2 (Other):** Non-code projects

**Checks:**
1. **Dependency Manifest (Tier 1 only):** Must have `requirements.txt`, `package.json`, `pyproject.toml`, or `setup.py`
2. **Dangerous Functions (All Tiers):** Flags `os.remove`, `os.unlink`, `shutil.rmtree`

### 2.7 Pre-Review Scan (`scripts/pre_review_scan.sh`)

**Purpose:** Mechanical gatekeeper before human/AI review.

**Tiered Checks:**

| Tier | Category | Checks |
|------|----------|--------|
| 1 | Blast Radius | Hardcoded paths in `templates/`, YAML files |
| 2 | Security | API keys, silent `except: pass`, `.env` gitignored |
| 3 | Dependencies | Unpinned `>=` versions, anthropic 0.x warning |
| 4 | Code Quality | Functions without return type hints |

**Exit Codes:**
- `0` = All checks pass
- `1` = One or more failures

---

## Part 3: Data Models

### 3.1 External Resources Schema (`EXTERNAL_RESOURCES.yaml`)

```yaml
metadata:
  purpose: str
  last_updated: str
  why_exists: str

projects:
  {project-name}:
    monthly_cost: float
    credential_file: str
    services:
      - name: str
        purpose: str
        type: str  # ai, hosting, storage, notifications, etc.
        env_var: str
        cost: float

services_by_function:
  ai_apis: [str]
  hosting: [str]
  storage: [str]
  databases: [str]
  monitoring: [str]

api_key_pattern:
  rule: str
  format: str
  template: str
  naming_rule: str
  examples: [str]

cost_summary:
  infrastructure: float
  ai_apis: float
  total_known: float
```bash

### 3.2 Review Prompt Schema (YAML Frontmatter)

```yaml
version: int
created: date
type: str  # document_review, code_review
focus: str  # architecture, security, performance
api: str    # openai, anthropic, deepseek, ollama
model: str  # Model identifier
```bash

### 3.3 Project Index Schema (YAML Frontmatter)

```yaml
tags:
  - map/project
  - p/{project-name}
  - type/{standard|evergreen|infrastructure|ai-agent|...}
  - domain/{domain}
  - status/{active|archived|production|planning}
  - tech/{python|typescript|...}
created: date
```bash

---

## Part 4: Entry Points Summary

| Entry Point | Type | Purpose |
|-------------|------|---------|
| `scaffold_cli.py` | CLI | Main CLI wrapper |
| `scaffold review` | CLI Command | Multi-AI review orchestration |
| `scripts/archive_reviews.py` | Script | Review file archival |
| `scripts/validate_project.py` | Script | Project structure validation |
| `scripts/reindex_projects.py` | Script | Index file generation |
| `scripts/warden_audit.py` | Script | Ecosystem governance audit |
| `scripts/pre_review_scan.sh` | Shell | Pre-review gatekeeper |

---

## Part 5: Test Coverage Contract

### 5.1 Existing Tests

| Test File | Coverage |
|-----------|----------|
| `test_review.py` | ReviewOrchestrator creation, DeepSeek review, Ollama review, multi-reviewer parallel, CLI command, safe_slug traversal |
| `test_scripts_follow_standards.py` | No hardcoded paths, no API keys, type hints |
| `test_smoke.py` | Basic imports |

### 5.2 Test Markers

- `@pytest.mark.slow` - Integration tests calling real APIs
- `@pytest.mark.asyncio` - Async test functions

### 5.3 Asserted Behaviors

1. Orchestrator can be created with/without API keys
2. DeepSeek reviews return valid content, cost, and tokens
3. Ollama reviews work with local CLI (skipped if not available)
4. Parallel reviews complete successfully
5. `safe_slug()` prevents path traversal attacks
6. Scripts contain no `/Users/` paths
7. Scripts contain no `sk-*` API keys

---

## Part 6: Technical Debt Registry

### 6.1 🔴 CRITICAL - Ghost Logic / Undocumented Behavior

| ID | Location | Issue | Impact |
|----|----------|-------|--------|
| **TD-01** | `scaffold/review.py:390-393` | `_call_google()` raises `NotImplementedError` | Google AI integration is non-functional |
| **TD-02** | `scripts/reindex_projects.py:70-90` | Silent exception swallowing in `get_last_modified()` | Git failures silently ignored, fallback to filesystem scan |
| **TD-03** | `test_review.py:144` | Assertion uses wrong filename pattern | Test asserts `test_reviewer.md` but orchestrator outputs `CODE_REVIEW_TEST_REVIEWER.md` |

### 6.2 🟠 HIGH - Governance Bypass

| ID | Location | Issue | Impact |
|----|----------|-------|--------|
| **TD-04** | `scripts/pre_review_scan.sh:24` | Path pattern uses character class `[U]sers` to avoid self-detection | Intentional bypass, documented |
| **TD-05** | `.cursorrules`, `templates/*.template` | `$PROJECTS_ROOT` references | Not truly portable - assumes specific ecosystem structure |
| **TD-06** | `tests/test_scripts_follow_standards.py:13-26` | Only checks `scripts/` and `scaffold/` for hardcoded paths | Misses `templates/`, `.cursorrules`, YAML files |

### 6.3 🟡 MEDIUM - Missing Hardening

| ID | Location | Issue | Impact |
|----|----------|-------|--------|
| **TD-07** | `tests/test_scripts_follow_standards.py:12,26` | subprocess.run without `check=True` | Test silently passes on grep errors |
| **TD-08** | `scripts/archive_reviews.py:97` | `send2trash()` may prompt interactively | CI/CD pipeline hang risk |
| **TD-09** | `test_scripts_follow_standards.py:57-76` | Type hint check only examines last file in loop | Logic bug - `content = script.read_text()` is outside inner loop |

### 6.4 🟢 LOW - Code Quality

| ID | Location | Issue | Impact |
|----|----------|-------|--------|
| **TD-10** | Multiple scripts | Uses `Path(os.getenv(...))` instead of dedicated config | Environment variable handling scattered |
| **TD-11** | `scaffold/review.py` | Cost calculation uses magic numbers | Pricing may drift from reality |
| **TD-12** | `EXTERNAL_RESOURCES.yaml:214,284` | References `$PROJECTS_ROOT/.env.project-template` | Non-portable ecosystem assumption |

---

## Part 7: Invariants & Constraints

### 7.1 System Invariants

1. **Every project MUST have an index file** (`00_Index_*.md`) - Critical Rule #0
2. **API keys MUST NOT be committed** - Enforced by pre-review scan
3. **No silent exception swallowing** - Violations flagged in review
4. **Subprocess calls MUST use `check=True` and `timeout`** - H1 hardening rule
5. **File writes MUST be atomic** - H3 hardening rule

### 7.2 Data Invariants

1. `ReviewConfig.api` ∈ {openai, anthropic, google, deepseek, ollama}
2. `ReviewResult.cost` ≥ 0
3. `ReviewResult.tokens_used` ≥ 0
4. `ReviewSummary.total_cost` = Σ(result.cost for result in results)

### 7.3 Environmental Constraints

1. Python 3.11+ required
2. `.env` file for credentials (gitignored)
3. Ollama CLI must be on PATH for local reviews
4. `$PROJECTS_ROOT` environment variable expected (ecosystem assumption)

---

## Part 8: API Contracts

### 8.1 CLI Contract

```bash
# Input: Markdown document with "Definition of Done" section
# Output: Review files in {output_dir}/round_{N}/
#         Cost summary JSON at {output_dir}/round_{N}/COST_SUMMARY.json
#         Terminal output with cost breakdown table

scaffold review --type document --input PATH --round N

# Exit codes:
# 0 = Success
# 1 = Error (missing DoD, no API keys, review failure)
```bash

### 8.2 Orchestrator Contract

```python
# Input: Document path, list of ReviewConfigs, round number, output directory
# Output: ReviewSummary with all results
# Side effects: Creates review files, COST_SUMMARY.json

async def run_review(
    document_path: Path,
    configs: List[ReviewConfig],
    round_number: int,
    output_dir: Path
) -> ReviewSummary

# Guarantees:
# - All reviews run in parallel
# - Failures are captured in ReviewResult.error (not raised)
# - Output files use safe_slug() for filenames
# - Atomic writes prevent partial files
```bash

### 8.3 Validation Contract

```python
# Input: Project directory path
# Output: Boolean (valid/invalid)
# Side effects: Prints validation results to stdout

def validate_project(project_path: Path, verbose: bool = True) -> bool

# Exit codes (CLI):
# 0 = All validations pass
# 1 = One or more failures
```

---

## Part 9: Known Limitations

### 9.1 Architectural Limitations

1. **Single-machine design** - No distributed orchestration
2. **Synchronous CLI** - Async orchestrator wrapped in `asyncio.run()`
3. **File-based configuration** - No database, no API for configuration
4. **Template-based approach** - Copy-paste deployment, no package installation

### 9.2 Scalability Ceiling

1. **Context window limit** - Large documents may exceed LLM context
2. **Parallel review limit** - No rate limiting for API calls
3. **No caching** - Every review re-processes from scratch
4. **No incremental review** - Entire document reviewed each round

### 9.3 Integration Gaps

1. **Google AI not implemented** - Raises `NotImplementedError`
2. **No CI/CD integration** - Manual execution only
3. **No webhook notifications** - Discord mentioned but not implemented in review flow
4. **No cost alerts** - Costs tracked but no alerting mechanism

---

## Part 10: Glossary

| Term | Definition |
|------|------------|
| **Tiered AI** | Cost-optimization strategy using cheaper models for simpler tasks |
| **Blast Radius** | Potential impact of changes (Tier 1 = highest, templates) |
| **DNA Integrity** | Portability - no machine-specific paths or secrets |
| **SSOT** | Single Source of Truth (YAML files as authoritative data) |
| **Warden** | Governance audit agent |
| **Scar Tissue** | Defects that become new standards (hardening) |
| **Dark Territory** | What tests DON'T cover (inverse audit) |

---

## Appendix A: File-to-Function Map

| File | Key Functions |
|------|--------------|
| `scaffold/cli.py` | `cli()`, `review()`, `_load_review_configs()` |
| `scaffold/review.py` | `safe_slug()`, `save_atomic()`, `create_orchestrator()`, `ReviewOrchestrator.*` |
| `scripts/archive_reviews.py` | `find_project_root()`, `find_review_files()`, `archive_reviews()`, `main()` |
| `scripts/validate_project.py` | `find_projects()`, `has_index_file()`, `validate_index_content()`, `validate_dna_integrity()`, `validate_project()`, `main()` |
| `scripts/reindex_projects.py` | `find_projects()`, `get_last_modified()`, `detect_primary_tech()`, `detect_status()`, `scan_components()`, `generate_index_content()`, `create_index()`, `main()` |
| `scripts/warden_audit.py` | `is_tier_1_project()`, `check_dependencies()`, `check_dangerous_functions()`, `run_audit()` |

---

## Appendix B: Environment Variable Reference

| Variable | Purpose | Default |
|----------|---------|---------|
| `SCAFFOLDING_OPENAI_KEY` | OpenAI API authentication | None |
| `SCAFFOLDING_ANTHROPIC_KEY` | Anthropic API authentication | None |
| `SCAFFOLDING_GOOGLE_KEY` | Google AI authentication (unused) | None |
| `SCAFFOLDING_DEEPSEEK_KEY` | DeepSeek API authentication | None |
| `SCAFFOLDING_OLLAMA_MODEL` | Ollama model for local reviews | `llama3.2` |
| `PROJECTS_ROOT` | Ecosystem root directory | REQUIRED (Must be configured in environment) |
| `OLLAMA_PATH` / `SCAFFOLDING_OLLAMA_PATH` | Override Ollama binary location | Auto-detect |

---

**End of Specification**

*This document defines the "Contract" of what project-scaffolding currently is. Security review is deferred to a subsequent audit.*

## Related Documentation

- [CODE_QUALITY_STANDARDS](Documents/CODE_QUALITY_STANDARDS.md) - code standards
- [Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md) - code review
- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - local AI
- [Cost Management](Documents/reference/MODEL_COST_COMPARISON.md) - cost management
- [Discord Webhooks Per Project](patterns/discord-webhooks-per-project.md) - Discord
- [Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md) - prompt engineering
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [AI Team Orchestration](patterns/ai-team-orchestration.md) - orchestration
- [Safety Systems](patterns/safety-systems.md) - security
- [audit-agent/README](../ai-model-scratch-build/README.md) - Audit Agent
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
