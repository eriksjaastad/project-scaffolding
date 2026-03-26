# Project Structure Standards

purpose: Consistent directory structure and file placement across all projects
principle: convention over configuration — predictable structure for humans and AI

## Python Project Layout

require: venv/ at project root
require: scripts/ for all executable scripts
require: data/ for data files and databases
require: tests/ for test files
require: requirements.txt for dependencies
require: .gitignore covering venv/, data/, __pycache__/

## Web Project Layout

require: src/ with components/, pages/, utils/
require: public/ for static assets
require: scripts/ for build scripts and utilities

## Documentation Layout

require: .agent/rules/ as centralized documentation directory
layout: ARCHITECTURE.md, OPERATIONS.md, DATA_MODEL.md at .agent/rules/ root
layout: guides/ for how-to docs
layout: reference/ for reference docs
layout: archives/ for historical docs

## Portability

banned: absolute paths (/Users/..., /home/...) in scripts or configs
require: relative paths or environment variables (PROJECTS_ROOT, Path.home())
check: if a path starts with /Users/ it is a bug

## Scaffolded Project Checklist

require: 00_Index_[ProjectName].md — Obsidian index with status tags
require: AGENTS.md — universal source of truth for AI agents
require: CLAUDE.md — project-specific AI instructions
require: .agent/rules/ directory following this standard

---
version: 2.0.0
established: 2026-01-15
updated: 2026-03-26 — trimmed from 129 lines, removed example trees and code review section (covered by governance)
