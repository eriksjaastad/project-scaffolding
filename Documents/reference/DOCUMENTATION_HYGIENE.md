# Documentation Hygiene

> **Purpose:** Prevent doc bloat. Keep documentation useful, not exhaustive.
> **Created:** January 12, 2026
> **Rule of thumb:** If no one reads it, delete it.

---

## The Problem

Documentation grows faster than code. The result is noise. New contributors can't find what matters.

---

## Required Docs (Keep These)

Every project needs exactly these, as defined in the [[PROJECT_STRUCTURE_STANDARDS]]:

| File | Purpose | Max Size |
|------|---------|----------|
| `README.md` | What is this, how to run it | 100 lines |
| `AGENTS.md` | AI collaboration rules | 200 lines |
| `00_Index_*.md` | Project metadata (See [[PROJECT_INDEXING_SYSTEM]]) | 50 lines |
| `TODO.md` | Current work, backlog | No limit |

---

## Adding to Project Scaffolding

When scaffolding a new project via the [[PROJECT_KICKOFF_GUIDE]]:

1. Create only required docs.
2. Set a 3-month review reminder.
3. Start with zero optional docs.

**Templates should be minimal.** It's easier to add docs than to delete them.

---
*See also: [[PROJECT_STRUCTURE_STANDARDS]] for the standard directory layout.*

## Related Documentation

- [[DOCUMENTATION_HYGIENE]] - documentation
- [[project-scaffolding/README]] - Project Scaffolding
