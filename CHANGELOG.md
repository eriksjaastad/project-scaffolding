# Changelog

All notable changes to project-scaffolding will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-27
### Added
- Initial scaffolding templates
- CLI for applying templates to projects
- Agentsync rules templates
- .scaffolding-version tracking (JSON format)
- pyproject.toml for centralized version management
- Support for multiple task IDs in `pt tasks show` (project-tracker integration)

### Changed
- Refactored `scaffold apply` to use marker-based updates (npm-like)
- Removed hardcoded versions from `cli.py`
- Updated version metadata in `00_Index_*.md` to use centralized version

## Versioning Policy
- **MAJOR**: Breaking changes to templates or CLI that require manual project migration.
- **MINOR**: New templates, CLI features, or significant improvements to existing templates.
- **PATCH**: Bug fixes, documentation updates, or minor template tweaks.
