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

- 2026-03-11: refactor: remove local-model-learnings.md from scaffold system (#5097)
- 2026-03-11: refactor: rewrite learning-loop-pattern (396→51 lines) and recreate governance protocol
- 2026-03-11: feat: add hook-based agentsync and agent-health checks (#5100, #5101)
- 2026-03-11: feat: unify agentsync sync command (#5099)
- 2026-03-10: refactor: remove Documents/ directory, migrate agent rules to .agent/rules/ (#5094)
- 2026-02-27: fix: Exclude backtick-quoted rmtree mentions from pre-push block
- 2026-02-27: fix: Allow rmtree mentions in .md docs in pre-push hook
- 2026-02-27: docs: Template audit and cleanup — The Architect, DRY rules, centralized safety
- 2026-02-27: docs: Add Trickle-Down Updates section documenting propagation model for shared tooling
- 2026-02-27: refactor: Replace duplicate path greps in CI with canonical warden_audit.py call

<!-- LIBRARIAN-INDEX-START -->

### Subdirectories

| Directory | Files | Description |
| :--- | :---: | :--- |
| [agentsync/](agentsync/README.md) | 7 | Synchronizes AI instruction rules from a single source to multiple IDE-specific config files. |
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
| [agentsync/migrate_agents_md.py](agentsync/migrate_agents_md.py) | No description available. |
| [agentsync/sync.py](agentsync/sync.py) | No description available. |
| [agentsync/sync_agents_md.py](agentsync/sync_agents_md.py) | No description available. |
| [agentsync/sync_governance.py](agentsync/sync_governance.py) | No description available. |
| [agentsync/sync_mcp.py](agentsync/sync_mcp.py) | No description available. |
| [agentsync/sync_rules.py](agentsync/sync_rules.py) | No description available. |
| [patterns/ai-team-orchestration.md](patterns/ai-team-orchestration.md) | > **Purpose:** How to structure multi-agent AI workflows with clear roles, metrics, and guardrails |
| [patterns/api-key-management.md](patterns/api-key-management.md) | **Status:** Proven |
| [patterns/automation-reliability.md](patterns/automation-reliability.md) | > **Philosophy:** "Silent failures are the worst failures" |
| [patterns/development-philosophy.md](patterns/development-philosophy.md) | > **Purpose:** Proven principles for building maintainable experimental projects |
| [patterns/discord-webhooks-per-project.md](patterns/discord-webhooks-per-project.md) | **Pattern:** Create dedicated Discord channels for each project's notifications |
| [patterns/foundation-documents-first.md](patterns/foundation-documents-first.md) | **Pattern Type:** 🟢 Proven (learned through pain) |
| [patterns/local-ai-integration.md](patterns/local-ai-integration.md) | > **Purpose:** How to use local AI models to reduce API costs while maintaining quality |
| [patterns/project-vs-tool-requirements.md](patterns/project-vs-tool-requirements.md) | > **Purpose:** Define different levels of requirements for full projects vs utility tools |
| [patterns/safety-systems.md](patterns/safety-systems.md) | > **Philosophy:** "Every safety system was a scar" |
| [patterns/scaffolding-as-dependency.md](patterns/scaffolding-as-dependency.md) | **Pattern Type:** Draft - Needs Discussion |
| [patterns/ssot-via-yaml.md](patterns/ssot-via-yaml.md) | **Status:** Proven Pattern (Dec 31, 2025) |
| [patterns/tiered-ai-sprint-planning.md](patterns/tiered-ai-sprint-planning.md) | **Pattern Type:** 🟡 Emerging (needs validation) |
| [pyproject.toml](pyproject.toml) | No description available. |
| [pytest.ini](pytest.ini) | No description available. |
| [requirements.txt](requirements.txt) | No description available. |
| [scaffold/__init__.py](scaffold/__init__.py) | Project Scaffolding - Automated Multi-AI Review & Build System |
| [scaffold/agent_health.py](scaffold/agent_health.py) | Agent config file health checks for the project scanner. |
| [scaffold/alerts.py](scaffold/alerts.py) | No description available. |
| [scaffold/cli.py](scaffold/cli.py) | CLI for Project Scaffolding automation system |
| [scaffold/constants.py](scaffold/constants.py) | Centralized constants for the project scaffolding system. |
| [scaffold/review.py](scaffold/review.py) | Multi-AI Review Orchestrator |
| [scaffold/utils.py](scaffold/utils.py) | No description available. |
| [scaffold_cli.py](scaffold_cli.py) | No description available. |
| [uv.lock](uv.lock) | No description available. |
>>>>>>> Stashed changes

<!-- LIBRARIAN-INDEX-END -->