# Project Scaffolding - Usage Guide

> **Quick Start:** How to use these templates and patterns in new projects

---

## What's Available

This scaffolding provides:

1. **Templates** (`templates/`)
   - Documentation structure (`Documents/`)
   - AI collaboration files (`.cursorrules`, `CLAUDE.md`)

2. **Patterns** (`patterns/`)
   - Safety systems patterns
   - Development philosophy
   - Testing approaches
   - **Code Review Standardization** (`patterns/code-review-standard.md`)

3. **Examples** (`examples/`)
   - Real implementations from source projects

4. **Analysis** (`docs/`)
   - Pattern analysis and extraction notes

---

## Starting a New Project

### Step 1: Copy Template Structure

```bash
# Create new project
mkdir my-new-project
cd my-new-project

# Copy documentation structure
cp -r /path/to/project-scaffolding/templates/Documents ./Documents

# Copy AI collaboration templates
cp /path/to/project-scaffolding/templates/CLAUDE.md.template ./CLAUDE.md
cp /path/to/project-scaffolding/templates/.cursorrules.template ./.cursorrules
```

### Step 2: Customize for Your Project

Edit the templates to fit your project:

**CLAUDE.md:**
- Replace `[PROJECT_NAME]` with your project name
- Update project summary
- Add project-specific patterns
- Specify your safety rules

**.cursorrules:**
- Update project overview
- Add project-specific patterns
- Customize validation commands

**Documents/README.md:**
- Update quick start links
- Adjust to your project structure

### Step 3: Create Core Documentation

Start with these files:

```bash
cd Documents/core/
# Create initial docs
touch ARCHITECTURE_OVERVIEW.md
touch OPERATIONS_GUIDE.md
```

**ARCHITECTURE_OVERVIEW.md** template:

```markdown
# Architecture Overview

**Last Updated:** [DATE]
**Status:** Draft
**Audience:** Developers

## What This Project Does

[2-3 sentence summary]

## System Design

[Diagram or description of main components]

## Tech Stack

- Language: [e.g., Python 3.11]
- Key libraries: [list main dependencies]
- Data storage: [e.g., JSON files, SQLite, Postgres]

## Directory Structure

```
project/
├── [main code directory]/
├── config/
├── data/
└── Documents/
```

## Key Design Decisions

### Decision 1: [Name]
**Why:** [Rationale]
**Trade-offs:** [What we gave up]
**Alternatives considered:** [What else we looked at]
```

### Step 4: Start Building

Use the patterns as guidelines, not rules:

- **Layer-by-Layer:** Plan your layers before building
- **Data Before Decisions:** Set evaluation timeline (30-60 days)
- **Safety Systems:** Wait for the scar, then protect
- **Testing:** Focus on fragile parts first

---

## Using the Patterns

### Safety Systems

Read `patterns/safety-systems.md` and ask:

- [ ] Do I have critical data? → Use append-only archives
- [ ] Do I have source data? → Make it read-only
- [ ] Do I have files that could corrupt? → Use atomic writes
- [ ] Do I have companion files? → Move them together
- [ ] Do I have user deletions? → Use trash, not rm

**Don't:** Build all safety systems upfront. Wait for scars.

### Development Philosophy

Read `patterns/development-philosophy.md` and:

1. **Plan layers** - Make each one independently useful
2. **Set evaluation date** - 30-60 days from start
3. **Watch for duplicates** - Extract on 3rd instance
4. **Test strategically** - Fragile parts only (at first)
5. **Document scars** - When things break, write it down

---

## Adapting the Templates

These templates are **starting points**, not rigid rules.

### Customize freely:
- Add sections relevant to your domain
- Remove sections that don't apply
- Adjust tone to your preference
- Add project-specific patterns

### Keep the structure:
- Documents/ directory organization
- Safety rule prominence (in CLAUDE.md)
- Metadata on documentation files
- Archive retention policies

---

## Pattern Recognition

As you build, watch for patterns:

### Track Potential Patterns

Create `PATTERNS_OBSERVED.md`:

```markdown
## Patterns I'm Noticing

### [Pattern Name]
- **Instance 1:** [Where I used it, when]
- **Instance 2:** [Second time I saw it]
- **Instance 3:** [Third time - extract it!]
- **Status:** [Candidate | Emerging | Ready to extract]

### Example: Date-based file naming
- **Instance 1:** Daily logs (2024-12-21.log)
- **Instance 2:** Session notes (2024-12-21_session.md)
- **Instance 3:** ??? (waiting)
- **Status:** Emerging pattern (2/3)
```

### Contribute Back

If you find patterns worth sharing:

1. Use them across 3+ instances in your project(s)
2. Document with examples and rationale
3. Share with the scaffolding project
4. Help others learn from your scars

---

## Common Mistakes

### ❌ Copying Everything

Don't cargo-cult the templates. Pick what fits.

**Wrong:**
```bash
# Copy entire scaffolding structure
cp -r project-scaffolding/* my-project/
```

**Right:**
```bash
# Copy relevant templates only
cp project-scaffolding/templates/CLAUDE.md.template my-project/CLAUDE.md
# Customize for your needs
```

### ❌ Following Patterns Too Rigidly

Patterns are guidelines, not laws.

**Example:** "Consolidate on 3rd duplicate" doesn't mean:
- ❌ Never abstract before 3rd instance (obvious utils are fine)
- ❌ Always abstract on 3rd instance (maybe it's not a pattern)
- ✅ Be patient, wait to see if it's really a pattern

### ❌ Building Safety Too Early

"Every safety system was a scar" means:
- ❌ Don't build append-only archives "just in case"
- ❌ Don't add validation "to be safe"
- ✅ Wait until something breaks, then protect

### ❌ Skipping Documentation

Even experiments need docs:
- ✅ Quick README (what is this?)
- ✅ CLAUDE.md (how to modify this?)
- ✅ Basic architecture (how does this work?)
- ❌ Exhaustive API docs (too early)

---

## Examples from Real Projects

See `examples/` directory for:
- Real CLAUDE.md files
- Real Documents/ structures
- Real safety system implementations
- Real scar stories

**Study these to see patterns in practice.**

---

## Questions?

### "Which patterns should I use?"

Start with:
1. Documents/ structure (helps everyone)
2. CLAUDE.md (helps AI and humans)
3. Modern Python typing (if using Python)

Add others as you experience the need.

### "When do I know I need a pattern?"

You'll feel the pain:
- Losing data → Need safety systems
- Confused about structure → Need documentation
- Fighting abstractions → Too early
- Copy-paste bugs → Time to abstract

### "Can I change the templates?"

Absolutely! These are starting points. Adapt to your needs.

### "How do I contribute back?"

When you find patterns worth sharing:
1. Document them (with examples)
2. Show evidence (3+ instances)
3. Explain trade-offs (what does it cost?)
4. Open an issue or PR

---

## Next Steps

1. **Read** `patterns/development-philosophy.md` - Understand the mindset
2. **Copy** templates you need - Don't use what doesn't fit
3. **Customize** for your project - Make it yours
4. **Build** your first layer - Keep it simple and useful
5. **Watch** for patterns - Document what repeats
6. **Share** learnings - Help improve the scaffolding

---

*Remember: These patterns come from real scars. Use what helps, skip what doesn't, adapt everything.*

**The goal:** Build better experiments faster, compound learnings across projects.

