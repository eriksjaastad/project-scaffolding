---
tags:
  - map/project
  - p/project-scaffolding
  - type/meta-project
  - domain/pattern-extraction
  - status/active
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
  - Multi-model coordination
  - YAML processing

### Documentation
- `docs/` - Meta-documentation
  - `PATTERN_ANALYSIS.md` - Pattern extraction
  - `USAGE_GUIDE.md` - How to use scaffolding
  - `PROJECT_KICKOFF_GUIDE.md` - Starting new projects
  - `CODE_QUALITY_STANDARDS.md` - Mandatory rules

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
**Status:** #status/active #status/production  
**Last Major Update:** December 2025 (actively maintained)  
**Priority:** #mission-critical (multiplier effect on all projects)

