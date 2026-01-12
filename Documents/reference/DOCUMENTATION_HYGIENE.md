# Documentation Hygiene

> **Purpose:** Prevent doc bloat. Keep documentation useful, not exhaustive.
> **Created:** January 12, 2026
> **Rule of thumb:** If no one reads it, delete it.

---

## The Problem

Documentation grows faster than code because:
- AIs are verbose by default
- "Document the decision" creates a new file every time
- It feels productive but often isn't
- No one deletes docs - they only accumulate

**The result:** Docs become noise. Useful information gets buried. New contributors can't find what matters.

---

## Required Docs (Keep These)

Every project needs exactly these:

| File | Purpose | Max Size |
|------|---------|----------|
| `README.md` | What is this, how to run it | 100 lines |
| `AGENTS.md` | AI collaboration rules | 200 lines |
| `00_Index_*.md` | Project metadata | 50 lines |
| `TODO.md` | Current work, backlog | No limit (but prune completed) |

**That's it.** Everything else is optional and must justify its existence.

---

## Optional Docs (Earn Their Keep)

These are allowed IF actively used:

| File | When to keep | When to delete |
|------|--------------|----------------|
| `CLAUDE.md` | If it adds project-specific context beyond AGENTS.md | If it just duplicates AGENTS.md |
| `Documents/guides/*.md` | If someone references it monthly | If no one has read it in 3 months |
| `Documents/reference/*.md` | If it's looked up regularly | If it's "just in case" knowledge |
| `Documents/planning/*.md` | While actively planning | Archive when work is done |
| `Documents/archives/*` | Historical reference | Delete after 6 months if never accessed |

---

## The Sunset Rule

**Every 3 months, ask of each doc:**

1. Has anyone read this in the last 3 months?
2. Has it been updated in the last 3 months?
3. Would anyone miss it if deleted?

If all three answers are "no" → delete or archive.

---

## Size Ratios (Warning Signs)

| Ratio | Status |
|-------|--------|
| Docs < 10% of codebase | Healthy |
| Docs 10-20% of codebase | Acceptable |
| Docs 20-50% of codebase | Warning - review needed |
| Docs > 50% of codebase | Critical - prune immediately |

**How to check:**
```bash
# Lines of code
find . -name "*.py" -o -name "*.js" -o -name "*.ts" | xargs wc -l | tail -1

# Lines of docs
find . -name "*.md" | xargs wc -l | tail -1
```

---

## Before Creating a New Doc

Ask yourself:

1. **Can this go in an existing file?** (Consolidate > Create)
2. **Can this be a code comment instead?** (Code > Docs)
3. **Will someone actually read this?** (If no, don't write it)
4. **Is this a decision that's irreversible?** (If reversible, don't document)
5. **Am I writing this for me or for the AI?** (AIs don't need docs - they read code)

**If you still need a new doc:** Set a review date. If it's not useful by then, delete it.

---

## Consolidation Patterns

### Instead of multiple files → One file with sections

**Before:**
```
Documents/
  ARCHITECTURE_OVERVIEW.md
  ARCHITECTURE_DECISIONS.md
  ARCHITECTURE_PATTERNS.md
  ARCHITECTURE_FUTURE.md
```

**After:**
```
Documents/
  ARCHITECTURE.md  (with sections: Overview, Decisions, Patterns, Future)
```

### Instead of docs → Code comments

**Before:** `Documents/API_DESIGN.md` explaining the API structure

**After:** Docstrings in the actual API code:
```python
def create_project(name: str, template: str = "default") -> Project:
    """
    Create a new project from scaffolding.

    Why template defaults to "default": Most projects don't need
    special handling. Only use other templates for specific cases
    like "minimal" (no docs) or "full" (everything).
    """
```

### Instead of planning docs → TODO.md sections

**Before:** `Documents/planning/FEATURE_X_PLAN.md`

**After:** Section in TODO.md:
```markdown
## Feature X (Planning)
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
```

---

## Monthly Hygiene Checklist

Run this on the 1st of each month:

```markdown
## Doc Hygiene Check - [Month Year]

### Size Check
- [ ] Calculated doc/code ratio: ____%
- [ ] Ratio is healthy (<20%): Yes/No

### Sunset Check
- [ ] Reviewed Documents/planning/ - archived completed plans
- [ ] Reviewed Documents/guides/ - deleted unread guides
- [ ] Reviewed Documents/archives/ - purged old archives

### Consolidation Check
- [ ] Any docs that should be merged?
- [ ] Any docs that should become code comments?

### Result
- [ ] Deleted ___ files
- [ ] Archived ___ files
- [ ] Merged ___ files
```

---

## What NOT to Document

- **Obvious code:** If the code is readable, don't explain it
- **Temporary decisions:** If you might change it next week, don't write it down
- **AI conversations:** Don't save chat logs as docs
- **"Just in case" knowledge:** If you might need it someday, you won't
- **Process for process sake:** If the doc explains how to write other docs, delete it

---

## The Nuclear Option

If docs are out of control:

1. **Delete everything in Documents/** except README.md
2. **Wait 2 weeks**
3. **Only recreate docs that someone actually needed**

What survives is what matters. Everything else was noise.

---

## Adding to Project Scaffolding

When scaffolding a new project:

1. Create only required docs (README, AGENTS, 00_Index, TODO)
2. Set a 3-month review reminder
3. Start with zero optional docs - add only when proven necessary

**Templates should be minimal.** It's easier to add docs than to delete them.
