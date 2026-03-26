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

# Project Scaffolding: Building Better Projects Faster

This meta-project serves as a central repository for proven patterns, templates, and automation tools designed to accelerate project development and ensure consistent quality. It embodies the "scaffolding is the product" philosophy, providing a robust framework for new projects and continuous improvement.

**Goal:** To provide a standardized, efficient, and reliable foundation for all new projects, reducing development time and improving overall quality.

## Table of Contents

1.  [Key Components](#key-components)
    *   [Patterns](#patterns)
    *   [Templates](#templates)
    *   [Core Library](#core-library)
    *   [Project Rules](#project-rules)
    *   [Resource Tracking](#resource-tracking)
2.  [Usage](#usage)
3.  [Status](#status)
4.  [Recent Activity](#recent-activity)

## Key Components

### Templates

The `templates/` directory provides reusable starting points for new projects, ensuring consistency and accelerating setup.

*   `.cursorrules.template`: A template file for defining project-specific rules and guidelines.
*   `CLAUDE.md.template`: A template for AI instruction prompts, tailored for the Claude model.
*   `TIERED_SPRINT_PLANNER.md`: A template for tiered sprint planning, optimizing resource allocation.

### Core Library

The `scaffold/` directory contains the automation library, written in Python, that powers many of the project scaffolding features.

*   `review.py`: The code review orchestrator, responsible for managing the multi-model review process.
*   `cli.py`: Provides command-line interface (CLI) tools for interacting with the scaffolding system.

### Project Rules (.agent/rules/)

The `.agent/rules/` directory contains active rules and standards that guide both AI agents and human developers.

*   `governance.md`: **MANDATORY** code review and governance protocol.
*   `CODE_QUALITY_STANDARDS.md`: **MANDATORY** coding rules and standards.
*   `PROJECT_STRUCTURE_STANDARDS.md`: Defines directory and file naming conventions.
*   `PROJECT_PHILOSOPHY.md`: The "why" behind the ecosystem and its design.
*   `code-review-anti-patterns.md`: Database of recurring defects and anti-patterns to avoid.
*   `documentation-hygiene.md`: Standards for maintaining clean and discoverable documentation.
*   `ANTIGRAVITY_ORCHESTRATION_PATTERNS.md`: Multi-tier orchestration model for Google's AI IDE.
*   `GOLD_STANDARD_DEFINITION.md`: What "Production Ready" means in this ecosystem.

### Resource Tracking

The `EXTERNAL_RESOURCES.yaml` file serves as a service registry, tracking external resources used by projects.

*   API costs by project
*   Credential locations
*   Service health monitoring
*   Prevents duplicate signups

## Usage

To start a new project using the scaffolding:

```bash
uv run "$PROJECTS_ROOT/project-scaffolding/scaffold_cli.py" apply "my-new-project"
```

## Status

**Tags:** #map/project #p/project-scaffolding  
**Status:** #status/production #status/hardened  
**Last Major Update:** March 2026 (active cleanup)  
**Priority:** #mission-critical (multiplier effect on all projects)

## Recent Activity

- 2026-03-10: [CLEANUP] Deprecated Documents/ directory in favor of .agent/rules/
- 2026-03-10: [CLEANUP] Removed stale docs, guides, and reports
- 2026-03-10: [FEAT] Migrated account tracking to EXTERNAL_RESOURCES.yaml
- 2026-02-27: fix: Exclude backtick-quoted rmtree mentions from pre-push block

<!-- LIBRARIAN-INDEX-START -->

### Subdirectories

| Directory | Files | Description |
| :--- | :---: | :--- |
| [.agent/rules/](.agent/rules/) | 10 | Project-specific rules and governance. |
| [agentsync/](agentsync/README.md) | 6 | Synchronizes AI instruction rules from a single source to multiple IDE-specific config files. |
| [examples/](examples/) | 0 | No description available. |
| [scaffold/](scaffold/) | 6 | Core scaffolding library code. |

### Files

| File | Description |
| :--- | :--- |
| [AGENTS.md](AGENTS.md) | The single source of truth for hierarchy, workflow, and AI collaboration philosophy. |
| [CLAUDE.md](CLAUDE.md) | AI agent instructions (auto-generated). |
| [EXTERNAL_RESOURCES.yaml](EXTERNAL_RESOURCES.yaml) | Central registry for services and APIs. |
| [PRD.md](PRD.md) | Project Requirements Document. |
| [QUICKSTART.md](QUICKSTART.md) | Step-by-step onboarding guide. |
| [README.md](README.md) | Project overview and workflows. |

<!-- LIBRARIAN-INDEX-END -->
