# PRD: Project Scaffolding System

## 1. Problem Statement
The Erik Sjaastad project ecosystem consists of 30+ projects that need to follow consistent standards for governance, AI agent interaction, and security.
- **Drift**: Projects naturally drift from standards over time as new patterns are established.
- **Fragmentation**: No single source of truth for governance rules (CLAUDE.md, AGENTS.md, etc.).
- **Scalability**: Manual updates across dozens of projects are error-prone and time-consuming.
- **Visibility**: Hard to identify which projects are out-of-sync or failing health checks.

## 2. Definition of 'Properly Scaffolded'
A project is considered 'properly scaffolded' if it meets the following criteria:
- **Version Tracking**: Contains a `.scaffolding-version` file in the root matching the current ecosystem version.
- **Rule Alignment**: The `.agentsync/rules/` directory is in sync with the latest templates.
- **Governed Sections**: Files like `CLAUDE.md`, `AGENTS.md`, and `.cursorrules` have their governed sections (between markers) in sync with templates.
- **Required Files**: Essential files exist: `00_Index_*.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `TODO.md`.
- **DNA Integrity**: No hardcoded absolute paths; uses relative paths or environment variables like `$PROJECTS_ROOT`.
- **Security**: Contains `scripts/warden_audit.py` and `scripts/validate_project.py`.

## 3. Validation Rules
The `validate_project.py` script enforces the following checks:
- **P0 (Critical)**:
    - Missing `00_Index_*.md` file.
    - Hardcoded absolute paths (e.g., `/Users/erik/...`).
    - Unsubstituted mandatory placeholders (e.g., `{{PROJECT_NAME}}`).
- **P1 (Error)**:
    - Missing `CLAUDE.md` or `AGENTS.md`.
    - `.agentsync/rules/` out of sync with templates.
    - Missing `scripts/` directory or core validation scripts.
- **P2 (Warning)**:
    - Missing `Documents/` directory.
    - Outdated scaffolding version.
    - Missing `EXTERNAL_RESOURCES.md`.

## 4. Variable Substitution
The system supports the following placeholders in templates:
- `{{PROJECT_NAME}}`: The directory name of the target project.
- `{{PROJECT_DESCRIPTION}}`: A brief description derived from the index or defaults.
- `{{DATE}}`: Current date in YYYY-MM-DD format.
- `{{PROJECTS_ROOT}}`: The root directory of the ecosystem (from environment).
- `{{AI_STRATEGY}}`: Defaulting to "Local-First".

## 5. Versioning Strategy
We use Semantic Versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to the core scaffolding structure or CLI that require manual intervention.
- **MINOR**: New templates, significant CLI features, or new mandatory rules.
- **PATCH**: Bug fixes in scripts, minor template tweaks, or documentation updates.

**Detection**: Projects detect they need updates during `scaffold apply` or via the `project-tracker` dashboard which scans `.scaffolding-version`.

## 6. Success Metrics
- **100% Adoption**: All active projects have a `.scaffolding-version` file.
- **Low Drift**: < 5% of projects are more than one minor version behind.
- **Audit Health**: Zero P0 failures in the weekly ecosystem-wide governance audit.
