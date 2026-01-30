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

This meta-project serves as a central repository for proven patterns, templates, and automation tools designed to accelerate project development and ensure consistent quality.  It embodies the "scaffolding is the product" philosophy, providing a robust framework for new projects and continuous improvement.  The system documents over 20 battle-tested patterns, offers project templates, enforces code quality standards through multi-model review orchestration (DeepSeek + Ollama), and tracks external resources to prevent duplication and unexpected costs.

**Goal:** To provide a standardized, efficient, and reliable foundation for all new projects, reducing development time and improving overall quality.

## Table of Contents

1.  [Key Components](#key-components)
    *   [Patterns](#patterns)
    *   [Templates](#templates)
    *   [Core Library](#core-library)
    *   [Documentation](#documentation)
    *   [Resource Tracking](#resource-tracking)
    *   [Tests](#tests)
2.  [Usage](#usage)
3.  [Status](#status)
4.  [Recent Activity](#recent-activity)
5.  [Contributing](#contributing)
6.  [License](#license)

## Key Components

### Patterns

The `patterns/` directory contains documented patterns extracted from successful projects. These patterns represent best practices and proven solutions to common development challenges.

*   `safety-systems.md`:  Details 6 proven patterns for building robust and secure systems.
*   `development-philosophy.md`: Outlines 7 core principles guiding our development approach.
*   `tiered-ai-sprint-planning.md`:  Explains how to leverage AI cost-effectively in sprint planning.
*   `learning-loop-pattern.md`: Describes the implementation of reinforcement learning cycles for continuous improvement.
*   `code-review-standard.md`: Defines the standards and orchestration process for code reviews.
*   `ssot-via-yaml.md`:  Explains how to manage data using a Single Source of Truth (SSOT) approach with YAML.

### Templates

The `templates/` directory provides reusable starting points for new projects, ensuring consistency and accelerating setup.

*   `Documents/`: A pre-defined documentation structure to promote clear and comprehensive documentation.
*   `.cursorrules.template`:  A template file for defining project-specific rules and guidelines.
*   `CLAUDE.md.template`: A template for AI instruction prompts, tailored for the Claude model.
*   `TIERED_SPRINT_PLANNER.md`: A template for tiered sprint planning, optimizing resource allocation.

### Core Library

The `scaffold/` directory contains the automation library, written in Python, that powers many of the project scaffolding features.

*   `review.py`:  The code review orchestrator, responsible for managing the multi-model review process.
*   `cli.py`:  Provides command-line interface (CLI) tools for interacting with the scaffolding system.

### Scripts

The `scripts/` directory contains maintenance and governance utilities used to manage and maintain the project scaffolding system.

*   `pre_review_scan.sh`: A mandatory script that performs a pre-review scan (v1.1 Gate 0) to identify potential issues early.
*   `archive_reviews.py`:  Automates the process of archiving review history for compliance and analysis.
*   `warden_audit.py`:  An infrastructure audit agent (Phase 1) for monitoring and ensuring infrastructure compliance.
*   Multi-model coordination scripts (details to be added).
*   YAML processing scripts (details to be added).

### Documentation

The `Documents/` directory (formerly `Documents/`) contains meta-documentation about the project scaffolding system itself.

*   `PATTERN_ANALYSIS.md`:  Describes the process of pattern extraction and analysis.
*   `USAGE_GUIDE.md`:  Provides a comprehensive guide on how to use the project scaffolding system.
*   `PROJECT_KICKOFF_GUIDE.md`:  Offers step-by-step instructions for starting new projects using the scaffolding.
*   `CODE_QUALITY_STANDARDS.md`:  Defines the mandatory code quality standards that must be followed.
*   `CODE_REVIEW_ANTI_PATTERNS.md`:  Maintains a database of recurring defects and anti-patterns identified during code reviews.
*   `REVIEW_SYSTEM_DESIGN.md`:  Explains the process-based review philosophy and design of the review system.

### Resource Tracking

The `EXTERNAL_RESOURCES.yaml` file serves as a service registry, tracking external resources used by projects.

*   API costs by project
*   Credential locations
*   Service health monitoring
*   Prevents duplicate signups

### Tests

The `tests/` directory contains the test suite for the project scaffolding system.

*   Integration tests (19/19 passing)
*   Code review validation tests
*   YAML processing tests

## Usage

To use the project scaffolding system, follow these steps:

1.  **Install the `scaffold` CLI:**  (Instructions to be added)
2.  **Create a new project:**  Use the `scaffold` CLI to create a new project from a template. (Example command to be added)
3.  **Configure the project:**  Customize the project settings and dependencies as needed.
4.  **Develop the project:**  Follow the code quality standards and development principles outlined in the documentation.
5.  **Submit code for review:**  Use the `review.py` script to initiate the multi-model code review process.
6.  **Deploy the project:**  (Deployment instructions to be added)

## Status

**Tags:** #map/project #p/project-scaffolding  
**Status:** #status/production #status/hardened  
**Audit Evidence:** [REVIEW.md](REVIEW.md) (Comprehensive Hardening Audit)  
**Last Major Update:** January 2026 (actively maintained)  
**Priority:** #mission-critical (multiplier effect on all projects)

## Recent Activity

- 2026-01-22: chore: Finalize project scaffolding and ecosystem synchronization
- 2026-01-16: feat: Integrate agent-skills-library discovery into project kickoff
- 2026-01-14: Update scaffolding ecosystem: standardize templates and enhance governance documentation
- 2026-01-14: Add Doppler secrets management and fix DNA defects
- 2026-01-12: Apply project scaffolding: standalone scripts and version metadata
- 2026-01-12: Merge pull request #9 from eriksjaastad/claude/code-review-recommendations-HVRym
- 2026-01-12: docs: add systematic code review based on documented recommendations
- 2026-01-12: Update AGENTS.md role mandates and archive knowledge transfer prompts
- 2026-01-11: Archive code review integration prompts and add validation updates
- 2026-01-11: docs: add Raw Output Limitation pattern to LOCAL_MODEL_LEARNINGS
## Contributing

We welcome contributions to the project scaffolding system!  Please see the `CONTRIBUTING.md` file for guidelines on how to contribute. (File to be created)

## License

This project is licensed under the [MIT License](LICENSE). (License file to be created)

<!-- LIBRARIAN-INDEX-START -->

### Subdirectories

| Directory | Files | Description |
| :--- | :---: | :--- |
| [Documents/](Documents/README.md) | 11 | *Auto-generated index. Last updated: 2026-01-24* |
| [agentsync/](agentsync/README.md) | 4 | Synchronizes AI instruction rules from a single source to multiple IDE-specific config files. |
| [examples/](examples/) | 0 | No description available. |
| [patterns/](patterns/) | 15 | No description available. |
| [scaffold/](scaffold/) | 6 | No description available. |

### Files

| File | Description |
| :--- | :--- |
| [AGENTS.md](AGENTS.md) | > The single source of truth for hierarchy, workflow, and AI collaboration philosophy. |
| [CHANGELOG.md](CHANGELOG.md) | All notable changes to project-scaffolding will be documented in this file. |
| [CLAUDE.md](CLAUDE.md) | 🛑 READ AGENTS.md FIRST |
| [DECISIONS.md](DECISIONS.md) | > *Documenting WHY we made decisions, not just WHAT we built.* |
| [Documents/ANTIGRAVITY_ORCHESTRATION_PATTERNS.md](Documents/ANTIGRAVITY_ORCHESTRATION_PATTERNS.md) | Antigravity (Google's AI IDE) employs a sophisticated multi-tier orchestration model that balances s... |
| [Documents/BACKUP_AUDIT.md](Documents/BACKUP_AUDIT.md) | **Generated:** 2026-01-27 |
| [Documents/CODE_QUALITY_STANDARDS.md](Documents/CODE_QUALITY_STANDARDS.md) | Code Quality Standards |
| [Documents/EXTERNAL_RESOURCES.md](Documents/EXTERNAL_RESOURCES.md) | > **Purpose:** Track which external services, APIs, and resources are used across all projects |
| [Documents/GOLD_STANDARD_DEFINITION.md](Documents/GOLD_STANDARD_DEFINITION.md) | What "Production Ready" means in this ecosystem. |
| [Documents/PROJECT_INDEXING_SYSTEM.md](Documents/PROJECT_INDEXING_SYSTEM.md) | Project Indexing System |
| [Documents/PROJECT_KICKOFF_GUIDE.md](Documents/PROJECT_KICKOFF_GUIDE.md) | Project Kickoff Guide |
| [Documents/PROJECT_PHILOSOPHY.md](Documents/PROJECT_PHILOSOPHY.md) | > *"We're explorers. We're finding cool ways to collect data, interpret data, and look for patterns.... |
| [Documents/PROJECT_STRUCTURE_STANDARDS.md](Documents/PROJECT_STRUCTURE_STANDARDS.md) | Project Structure Standards |
| [Documents/README.md](Documents/README.md) | Project Documentation |
| [Documents/TODO_FORMAT_STANDARD.md](Documents/TODO_FORMAT_STANDARD.md) | TODO.md Format Standard |
| [Documents/guides/AUDIT_ASSEMBLY_LINE.md](Documents/guides/AUDIT_ASSEMBLY_LINE.md) | 🏭 The Audit Assembly Line (V2.1) |
| [Documents/guides/CODE_REVIEW_PROMPT.md](Documents/guides/CODE_REVIEW_PROMPT.md) | Code Review Prompt: Project Scaffolding System |
| [Documents/guides/DEEPSEEK_SETUP.md](Documents/guides/DEEPSEEK_SETUP.md) | DeepSeek Setup Guide |
| [Documents/guides/FREE_CREDITS_GUIDE.md](Documents/guides/FREE_CREDITS_GUIDE.md) | AWS Activate & Google Cloud Credits - Quick Guide |
| [Documents/guides/REPOMIX_USAGE.md](Documents/guides/REPOMIX_USAGE.md) | You’re right—pandering is the opposite of progress. In engineering, "You're exactly right" is often ... |
| [Documents/guides/USAGE_GUIDE.md](Documents/guides/USAGE_GUIDE.md) | Project Scaffolding - Usage Guide |
| [Documents/patterns/code-review-standard.md](Documents/patterns/code-review-standard.md) | **Status:** Proven Pattern |
| [Documents/patterns/learning-loop-pattern.md](Documents/patterns/learning-loop-pattern.md) | > **Purpose:** Guide for creating reinforcement learning cycles in any project |
| [Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md](Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md) | Global Rules Injection - Design Document |
| [Documents/planning/KNOWLEDGE_CYCLE_DISCUSSION.md](Documents/planning/KNOWLEDGE_CYCLE_DISCUSSION.md) | Knowledge Cycle Discussion |
| [Documents/planning/README.md](Documents/planning/README.md) | Planning Directory Overview |
| [Documents/planning/SCAFFOLDING_SIMPLIFICATION_PLAN.md](Documents/planning/SCAFFOLDING_SIMPLIFICATION_PLAN.md) | Scaffolding Simplification Plan |
| [Documents/planning/ollama_mcp_enhancement/OLLAMA_MCP_RETRY_ESCALATION_SPEC.md](Documents/planning/ollama_mcp_enhancement/OLLAMA_MCP_RETRY_ESCALATION_SPEC.md) | Ollama MCP Enhancement: Retry & Escalation Tracking |
| [Documents/planning/pre_commit_hook/PRE_COMMIT_HOOK_PROMPTS_INDEX.md](Documents/planning/pre_commit_hook/PRE_COMMIT_HOOK_PROMPTS_INDEX.md) | Pre-Commit Hook: Worker Task Prompts |
| [Documents/planning/pre_commit_hook/PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md](Documents/planning/pre_commit_hook/PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md) | Worker Task: Create Pre-Commit Hook |
| [Documents/reference/AGENTSYNC_SYSTEM.md](Documents/reference/AGENTSYNC_SYSTEM.md) | **Version:** 1.0 |
| [Documents/reference/AGENT_CONFIG_SYNC.md](Documents/reference/AGENT_CONFIG_SYNC.md) | > **Single Source of Truth:** `.agentsync/rules/*.md` files are the only files you edit. All IDE con... |
| [Documents/reference/CLAUDE_CODE_HOOKS_AND_SUBAGENTS.md](Documents/reference/CLAUDE_CODE_HOOKS_AND_SUBAGENTS.md) | Claude Code Hooks and Sub-Agents |
| [Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md) | Code Review Anti-Patterns Database |
| [Documents/reference/DOCUMENTATION_HYGIENE.md](Documents/reference/DOCUMENTATION_HYGIENE.md) | Documentation Hygiene |
| [Documents/reference/DOPPLER_MIGRATION_PLAN.md](Documents/reference/DOPPLER_MIGRATION_PLAN.md) | Doppler Migration Strategy |
| [Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) | Doppler Secrets Management Guide |
| [Documents/reference/LOCAL_MODEL_LEARNINGS.md](Documents/reference/LOCAL_MODEL_LEARNINGS.md) | Local Model Learnings |
| [Documents/reference/MODEL_COST_COMPARISON.md](Documents/reference/MODEL_COST_COMPARISON.md) | AI Model Cost Comparison (December 2025) |
| [Documents/reference/PATTERN_ANALYSIS.md](Documents/reference/PATTERN_ANALYSIS.md) | Pattern Analysis - Extracted from Source Projects |
| [Documents/reference/PATTERN_MANAGEMENT.md](Documents/reference/PATTERN_MANAGEMENT.md) | Pattern Management System |
| [Documents/reference/REVIEW_SYSTEM_DESIGN.md](Documents/reference/REVIEW_SYSTEM_DESIGN.md) | Review System Design & Recommendations |
| [Documents/reference/SILENT_FAILURES_AUDIT.md](Documents/reference/SILENT_FAILURES_AUDIT.md) | **Created:** 2026-01-23 |
| [Documents/reference/SPEC_2026-01-08.md](Documents/reference/SPEC_2026-01-08.md) | **Document Type:** System Specification (Auditor-Generated) |
| [EXTERNAL_RESOURCES.yaml](EXTERNAL_RESOURCES.yaml) | No description available. |
| [PRD.md](PRD.md) | The Erik Sjaastad project ecosystem consists of 30+ projects that need to follow consistent standard... |
| [QUICKSTART.md](QUICKSTART.md) | Project Scaffolding - Quick Start |
| [README.md](README.md) | Project Scaffolding |
| [REVIEWS_AND_GOVERNANCE_PROTOCOL.md](REVIEWS_AND_GOVERNANCE_PROTOCOL.md) | **Date:** 2026-01-27 |
| [TODO.md](TODO.md) | > **Purpose:** Current actionable tasks for project-scaffolding |
| [agentsync/README.md](agentsync/README.md) | Synchronizes AI instruction rules from a single source to multiple IDE-specific config files. |
| [agentsync/migrate_agents_md.py](agentsync/migrate_agents_md.py) | No description available. |
| [agentsync/sync_mcp.py](agentsync/sync_mcp.py) | No description available. |
| [agentsync/sync_rules.py](agentsync/sync_rules.py) | No description available. |
| [patterns/ai-team-orchestration.md](patterns/ai-team-orchestration.md) | AI Team Orchestration Pattern |
| [patterns/api-key-management.md](patterns/api-key-management.md) | API Key Management Pattern |
| [patterns/automation-reliability.md](patterns/automation-reliability.md) | Automation Reliability Patterns |
| [patterns/code-review-standard.md](patterns/code-review-standard.md) | Code Review Standardization |
| [patterns/cursor-configuration.md](patterns/cursor-configuration.md) | Cursor Configuration Best Practices |
| [patterns/development-philosophy.md](patterns/development-philosophy.md) | Development Philosophy Patterns |
| [patterns/discord-webhooks-per-project.md](patterns/discord-webhooks-per-project.md) | Discord Webhooks: One Channel Per Project |
| [patterns/foundation-documents-first.md](patterns/foundation-documents-first.md) | Foundation Documents First |
| [patterns/learning-loop-pattern.md](patterns/learning-loop-pattern.md) | Learning Loop Pattern |
| [patterns/local-ai-integration.md](patterns/local-ai-integration.md) | Local AI Integration Guide |
| [patterns/project-vs-tool-requirements.md](patterns/project-vs-tool-requirements.md) | Project vs Tool Requirements |
| [patterns/safety-systems.md](patterns/safety-systems.md) | Safety Systems Patterns |
| [patterns/scaffolding-as-dependency.md](patterns/scaffolding-as-dependency.md) | Scaffolding as Dependency (DRAFT) |
| [patterns/ssot-via-yaml.md](patterns/ssot-via-yaml.md) | Pattern: Single Source of Truth (SSOT) via YAML |
| [patterns/tiered-ai-sprint-planning.md](patterns/tiered-ai-sprint-planning.md) | Tiered AI Sprint Planning |
| [pyproject.toml](pyproject.toml) | No description available. |
| [pytest.ini](pytest.ini) | No description available. |
| [requirements.txt](requirements.txt) | No description available. |
| [scaffold/__init__.py](scaffold/__init__.py) | Project Scaffolding - Automated Multi-AI Review & Build System |
| [scaffold/alerts.py](scaffold/alerts.py) | No description available. |
| [scaffold/cli.py](scaffold/cli.py) | CLI for Project Scaffolding automation system |
| [scaffold/constants.py](scaffold/constants.py) | Centralized constants for the project scaffolding system. |
| [scaffold/review.py](scaffold/review.py) | Multi-AI Review Orchestrator |
| [scaffold/utils.py](scaffold/utils.py) | No description available. |
| [scaffold_cli.py](scaffold_cli.py) | No description available. |
| [uv.lock](uv.lock) | No description available. |

<!-- LIBRARIAN-INDEX-END -->

scaffolding_version: 1.0.0
scaffolding_date: 2026-01-27
