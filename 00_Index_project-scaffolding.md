---
tags:
  - map/project
  - p/project-scaffolding
  - type/meta-project
  - domain/pattern-extraction
  - status/production
  - status/hardened
  - tech/python
  - mission-critical
created: 2025-12-31
---

# project-scaffolding

Meta-project for extracting patterns from experiments to build better projects faster, serving as the "scaffolding is the product" philosophy repository. This system documents 20+ proven patterns from battle-tested projects, provides templates for new projects, enforces code quality standards through multi-model review orchestration (DeepSeek + Kiro), and tracks external resources to prevent duplicate services and surprise bills. Initial extraction is complete with comprehensive pattern analysis, safety systems, and development philosophy documentation.

## Key Components

### Patterns
- `patterns/` - Documented patterns (64 MD files)
  - `safety-systems.md` - 6 proven patterns
  - `development-philosophy.md` - 7 core principles
  - `tiered-ai-sprint-planning.md` - Cost-effective AI usage
  - `code-review-standard.md` - Review orchestration
  - `ssot-via-yaml.md` - Data management

### Templates
- `templates/` - Reusable starting points
  - `Documents/` - Documentation structure
  - `.cursorrules.template` - Project rules
  - `CLAUDE.md.template` - AI instructions
  - `TIERED_SPRINT_PLANNER.md` - Sprint planning

### Core Library
- `scaffold/` - Automation library (10 Python files)
  - `review.py` - Code review orchestrator
  - `cli.py` - CLI tools
- `scripts/` - Maintenance & Governance utilities
  - `pre_review_scan.sh` - Mandatory v1.1 Gate 0 scan
  - `archive_reviews.py` - Automated review history retention
  - `warden_audit.py` - Infrastructure audit agent (Phase 1)
  - Multi-model coordination
  - YAML processing

### Documentation
- `docs/` - Meta-documentation
  - `PATTERN_ANALYSIS.md` - Pattern extraction
  - `USAGE_GUIDE.md` - How to use scaffolding
  - `PROJECT_KICKOFF_GUIDE.md` - Starting new projects
  - `CODE_QUALITY_STANDARDS.md` - Mandatory rules
  - `CODE_REVIEW_ANTI_PATTERNS.md` - Database of recurring defects
  - `REVIEW_SYSTEM_DESIGN.md` - Process-based review philosophy

### Resource Tracking
- `EXTERNAL_RESOURCES.yaml` - Service registry
  - API costs by project
  - Credential locations
  - Service health monitoring
  - Prevents duplicate signups

### Tests
- `tests/` - Test suite
  - Integration tests (19/19 passing)
  - Code review validation
  - YAML processing tests

## Status

**Tags:** #map/project #p/project-scaffolding  
**Status:** #status/production #status/hardened  
**Audit Evidence:** [[REVIEW.md]] (Comprehensive Hardening Audit)  
**Last Major Update:** December 2025 (actively maintained)  
**Priority:** #mission-critical (multiplier effect on all projects)



## Recent Activity
 
+- **2026-01-07 11:30**: Ecosystem Governance v1.2: Refined `pre_review_scan.sh` and DNA tests to allow absolute paths in documentation and config files while blocking them in code. Verified all 28 tests pass.
 - **2026-01-07 10:30**: Ecosystem Governance v1.2: Hardened protocol with industrial subprocess rules, data clobber guards, and context window scaling strategies. Automated DNA integrity scans in `validate_project.py`.
- **2026-01-07 09:00**: Ecosystem Governance v1.1: Implemented `pre_review_scan.sh`, updated `CODE_REVIEW.md.template`, and established Anti-Patterns Database.
- **2026-01-06 17:00**: Master Registry: Migrated all ecosystem API keys to `project-scaffolding/.env` for centralized record-keeping.
- **2026-01-06 16:30**: Decentralization: Implemented global environment template and decentralized key management mappings.
- **2026-01-06 16:00**: Official Graduation: Marked project as #status/production and #status/hardened following completion of all Mission Orders.
- **2026-01-06 15:30**: Dependency Shielding: Secured `requirements.txt` with compatible release pinning.
- **2026-01-06 15:00**: Automated Warden: Built CI-ready standards guard and added type hints to all scripts.
- **2026-01-06 14:30**: Institutional Memory: Documented review archive purpose and retention policy.
- **2026-01-06 14:00**: Documentation Hygiene: Completed Hardening Sprint and sanitized documentation examples.
- **2026-01-06 13:30**: Automated Governance: Installed git hooks and YAML schema validation.
- **2026-01-06 13:00**: Type Safety & Error Hardening: Refactored `archive_reviews.py` into a production-grade script.

- **2026-01-01 18:16**: validate_project.py: .

- **2026-01-01 18:19**: validate_project.py: .

