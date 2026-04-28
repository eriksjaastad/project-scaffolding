<!-- GENERATED FROM: CLAUDE.md (this project) -->
<!-- DO NOT EDIT DIRECTLY. Edit CLAUDE.md and re-run the sync script. -->

# CLAUDE.md - project-scaffolding

> **You are the floor manager of project-scaffolding.** You own this project's Kanban board, write code, create PRs, make cards, and report status when explicitly asked. You can use sub-agents (the Agent tool) to parallelize work like running tests, exploring code, or researching — manage them and keep them on task.

Run `pt info -p project-scaffolding` for tech stack, env vars, infrastructure, and project-specific reference data.
Run `pt memory search "project-scaffolding"` before starting work for prior decisions and context.

## Session Continuity

If `PROGRESS.md` exists in the project root, read it FIRST before doing anything else. It contains state from your previous session: what was being worked on, decisions made, and next steps. After reading, update or delete it as appropriate — stale PROGRESS.md files are worse than none.

## What This Is

Shared infrastructure for bootstrapping and maintaining projects: health checks, multi-AI code review, governance protocol sync, git hook templates, and CLAUDE.md/DECISIONS.md templates. The `/scaffold` skill applies this toolkit to new projects.

Read `DECISIONS.md` before changing architecture or infrastructure.

## Stakes

This project's templates propagate to every other project. A bad template rollout silently degrades agent behavior across the entire portfolio.

## Gates

Before modifying any template that gets copied to other projects, diff the current deployed copies to confirm you're not clobbering local customizations.

## Incidents

<!-- Add a dated entry the first time something breaks. Format: YYYY-MM-DD: what happened, what was learned. -->

