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
**Audit Evidence:** [[REVIEW.md]] (Comprehensive Hardening Audit)  
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

### File Index

| File | Description |
| :--- | :--- |
| [[AGENTS.md]] | > The single source of truth for hierarchy, workflow, and AI collaboration philosophy. |
| [[CLAUDE.md]] | 🛑 READ AGENTS.md FIRST |
| [[CODE_REVIEW_CLAUDE_v1.md]] | Code Review: Project Scaffolding |
| [[Documents/CODE_QUALITY_STANDARDS.md]] | Code Quality Standards |
| [[Documents/PROJECT_INDEXING_SYSTEM.md]] | Project Indexing System |
| [[Documents/PROJECT_KICKOFF_GUIDE.md]] | Project Kickoff Guide |
| [[Documents/PROJECT_STRUCTURE_STANDARDS.md]] | Project Structure Standards |
| [[Documents/README.md]] | Project Documentation |
| [[Documents/TODO_FORMAT_STANDARD.md]] | TODO.md Format Standard |
| [[Documents/guides/AUDIT_ASSEMBLY_LINE.md]] | 🏭 The Audit Assembly Line (V2.1) |
| [[Documents/guides/CODE_REVIEW_PROMPT.md]] | Code Review Prompt: Project Scaffolding System |
| [[Documents/guides/DEEPSEEK_SETUP.md]] | DeepSeek Setup Guide |
| [[Documents/guides/FREE_CREDITS_GUIDE.md]] | AWS Activate & Google Cloud Credits - Quick Guide |
| [[Documents/guides/REPOMIX_USAGE.md]] | You’re right—pandering is the opposite of progress. In engineering, "You're exactly right" is often ... |
| [[Documents/guides/USAGE_GUIDE.md]] | Project Scaffolding - Usage Guide |
| [[Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md]] | Global Rules Injection - Design Document |
| [[Documents/planning/KNOWLEDGE_CYCLE_DISCUSSION.md]] | Knowledge Cycle Discussion |
| [[Documents/planning/README.md]] | Planning Directory Overview |
| [[Documents/planning/SCAFFOLDING_SIMPLIFICATION_PLAN.md]] | Scaffolding Simplification Plan |
| [[Documents/planning/ollama_mcp_enhancement/OLLAMA_MCP_RETRY_ESCALATION_SPEC.md]] | Ollama MCP Enhancement: Retry & Escalation Tracking |
| [[Documents/planning/pre_commit_hook/PRE_COMMIT_HOOK_PROMPTS_INDEX.md]] | Pre-Commit Hook: Worker Task Prompts |
| [[Documents/planning/pre_commit_hook/PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md]] | Worker Task: Create Pre-Commit Hook |
| [[Documents/reference/CLAUDE_CODE_HOOKS_AND_SUBAGENTS.md]] | Claude Code Hooks and Sub-Agents |
| [[Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md]] | Code Review Anti-Patterns Database |
| [[Documents/reference/DOCUMENTATION_HYGIENE.md]] | Documentation Hygiene |
| [[Documents/reference/DOPPLER_MIGRATION_PLAN.md]] | Doppler Migration Strategy |
| [[Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md]] | Doppler Secrets Management Guide |
| [[Documents/reference/LOCAL_MODEL_LEARNINGS.md]] | Local Model Learnings |
| [[Documents/reference/MODEL_COST_COMPARISON.md]] | AI Model Cost Comparison (December 2025) |
| [[Documents/reference/PATTERN_ANALYSIS.md]] | Pattern Analysis - Extracted from Source Projects |
| [[Documents/reference/PATTERN_MANAGEMENT.md]] | Pattern Management System |
| [[Documents/reference/REVIEW_SYSTEM_DESIGN.md]] | Review System Design & Recommendations |
| [[Documents/reports/trustworthy_ai_report.md]] | Making AI Trustworthy Enough for Production Infrastructure Work |
| [[EXTERNAL_RESOURCES.md]] | External Resources & Services |
| [[EXTERNAL_RESOURCES.yaml]] | No description available. |
| [[PROJECT_PHILOSOPHY.md]] | Project Philosophy |
| [[QUICKSTART.md]] | Project Scaffolding - Quick Start |
| [[README.md]] | Project Scaffolding |
| [[REVIEWS_AND_GOVERNANCE_PROTOCOL.md]] | 🛡️ Ecosystem Governance & Review Protocol (v1.2) |
| [[TODO.md]] | > **Purpose:** Current actionable tasks for project-scaffolding |
| [[_cursorrules_backups/manifest.json]] | No description available. |
| [[local-ai-integration.md]] | What LM Studio gives you |
| [[patterns/ai-team-orchestration.md]] | AI Team Orchestration Pattern |
| [[patterns/api-key-management.md]] | API Key Management Pattern |
| [[patterns/automation-reliability.md]] | Automation Reliability Patterns |
| [[patterns/code-review-standard.md]] | Code Review Standardization |
| [[patterns/cursor-configuration.md]] | Cursor Configuration Best Practices |
| [[patterns/development-philosophy.md]] | Development Philosophy Patterns |
| [[patterns/discord-webhooks-per-project.md]] | Discord Webhooks: One Channel Per Project |
| [[patterns/foundation-documents-first.md]] | Foundation Documents First |
| [[patterns/learning-loop-pattern.md]] | Learning Loop Pattern |
| [[patterns/local-ai-integration.md]] | Local AI Integration Guide |
| [[patterns/project-vs-tool-requirements.md]] | Project vs Tool Requirements |
| [[patterns/safety-systems.md]] | Safety Systems Patterns |
| [[patterns/scaffolding-as-dependency.md]] | Scaffolding as Dependency (DRAFT) |
| [[patterns/ssot-via-yaml.md]] | Pattern: Single Source of Truth (SSOT) via YAML |
| [[patterns/tiered-ai-sprint-planning.md]] | Tiered AI Sprint Planning |
| [[prompts/active/document_review/architecture.md]] | You are an **architecture-focused purist reviewer** with expertise in system design, software archit... |
| [[prompts/active/document_review/performance.md]] | You are a **performance-focused critical reviewer** with expertise in scalability, database optimiza... |
| [[prompts/active/document_review/security.md]] | You are a **security-focused skeptical reviewer** with expertise in application security, authentica... |
| [[pytest.ini]] | No description available. |
| [[requirements.txt]] | No description available. |
| [[scaffold/__init__.py]] | Project Scaffolding - Automated Multi-AI Review & Build System |
| [[scaffold/cli.py]] | CLI for Project Scaffolding automation system |
| [[scaffold/review.py]] | Multi-AI Review Orchestrator |
| [[scaffold/utils.py]] | No description available. |
| [[scaffold-20-projects-prompt.md]] | Scaffold 20 Projects Prompt |
| [[scaffold_cli.py]] | No description available. |
| [[scripts/00_Index_scripts.md]] | Scripts Index |
| [[scripts/archive_reviews.py]] | No description available. |
| [[scripts/compare_models.py]] | No description available. |
| [[scripts/mark_scaffolded_files.py]] | No description available. |
| [[scripts/migrate_docs_to_documents.py]] | No description available. |
| [[scripts/pre_review_scan.sh]] | Mandatory pre-review scan for project-scaffolding |
| [[scripts/reindex_projects.py]] | No description available. |
| [[scripts/test_deepseek.py]] | No description available. |
| [[scripts/update_cursorrules.py]] | No description available. |
| [[scripts/validate_external_resources.py]] | No description available. |
| [[scripts/validate_project.py]] | No description available. |
| [[scripts/warden_audit.py]] | No description available. |
| [[spec.md]] | **Document Type:** System Specification (Auditor-Generated) |
| [[templates/00_Index.md.template]] | No description available. |
| [[templates/AGENTS.md.template]] | No description available. |
| [[templates/CLAUDE.md.template]] | No description available. |
| [[templates/CODE_REVIEW.md.template]] | No description available. |
| [[templates/Documents/README.md]] | Documentation Template Directory |
| [[templates/README.md.template]] | No description available. |
| [[templates/TIERED_SPRINT_PLANNER.md]] | Tiered Sprint Planner Template |
| [[templates/TODO.md.template]] | No description available. |
| [[templates/claude-code/README.md]] | Claude Code Templates |
| [[templates/spec-template.md]] | PROJECT SPEC: [Project Name] |
| [[templates/test-coverage/README.md]] | Test Coverage Templates |
| [[templates/test-coverage/coveragerc.template]] | No description available. |
| [[templates/test-coverage/run_coverage.py]] | No description available. |
| [[tests/README.md]] | Tests for Project Scaffolding |
| [[tests/test_review.py]] | Tests for review orchestrator (DeepSeek + Ollama integration) |
| [[tests/test_scripts_follow_standards.py]] | Test that scripts follow CODE_QUALITY_STANDARDS.md |
| [[tests/test_security.py]] | Security-focused adversarial tests - The Dark Territory |
| [[tests/test_smoke.py]] | Quick smoke tests - run these first! |
| [[tests/test_update_cursorrules.py]] | Tests for update_cursorrules.py - Global Rules Injection script. |
| [[validation_report.txt]] | No description available. |

<!-- LIBRARIAN-INDEX-END -->
