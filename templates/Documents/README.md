# Documentation

**Last Updated:** [DATE]  
**Audience:** Developers, Operators, AI Collaborators

---

## Quick Start

### New to this project?
1. Read `ARCHITECTURE_OVERVIEW.md` (5-10 min)
2. Skim this README for relevant sections
3. Check `../TODO.md` for current work

### Daily shortcuts
- Current work: `../TODO.md`
- Code standards: `reference/CODE_QUALITY_RULES.md`
- Safety rules: `../.cursorrules`

---

## Documentation Structure

This project follows the **Documents/ pattern** - a centralized documentation directory that prevents root-level sprawl and makes information discoverable.

### Core Directories

### Core Documents

**Purpose:** Essential architecture and operations documentation

**Suggested files:**
- `ARCHITECTURE_OVERVIEW.md` - System map, how components fit together
- `OPERATIONS_GUIDE.md` - How to run, deploy, and maintain
- `DISASTER_RECOVERY_GUIDE.md` - What to do when things break

**Retention:** Keep indefinitely (unless superseded by newer docs)

---

#### `guides/`
**Purpose:** How-to documents for specific tasks

**Examples:**
- Setup guides (installation, configuration)
- Feature-specific workflows
- Integration instructions

**Retention:** Keep while feature exists; archive when deprecated

---

#### `reference/`
**Purpose:** Standards, conventions, and knowledge base

**Suggested files:**
- `CODE_QUALITY_RULES.md` - Linting standards, type hints, style
- `TECHNICAL_KNOWLEDGE_BASE.md` - Domain-specific knowledge
- `DECISION_LOG.md` - Why we made specific technical choices

**Retention:** Keep indefinitely (reference material)

---

#### `safety/`
**Purpose:** Safety systems, policies, and lessons learned

**Philosophy:** "Every safety system was a scar" - document WHY protections exist

**Examples:**
- Data integrity rules
- File safety systems
- Backup/recovery procedures
- Incident post-mortems

**Retention:** Keep indefinitely (especially scar stories)

---

#### `archives/`
**Purpose:** Historical documentation with expiration policies

**Subdirectories:**

```
archives/
├── sessions/           # Session summaries, work logs
│   └── (12-month retention)
├── implementations/    # Completed feature summaries
│   └── (keep indefinitely, compress after 12 months)
└── misc/              # Other historical docs
    └── (3-month retention)
```

**Archive Policy:**
- Sessions: Keep 12 months; delete if not referenced elsewhere
- Implementations: Keep indefinitely; optionally compress >12 months
- Misc: Keep 3 months; delete if not referenced

**"Referenced" means:** Linked from any document outside `archives/`. If referenced, keep regardless of age.

**Cleanup:** Quarterly review (generate candidate list, manual review before deleting)

---

## Documentation Standards

### Metadata (Top of Each Document)

```markdown
# Document Title

**Last Updated:** YYYY-MM-DD
**Status:** [Draft | Active | Deprecated | Archived]
**Audience:** [Developers | Operators | AI Collaborators | All]
**Estimated Reading Time:** X minutes (optional)
```

### Writing Guidelines

- **Keep it concise** - Respect reader's time
- **Keep it accurate** - Update when code changes
- **Keep it discoverable** - Cross-link related docs
- **Archive, don't delete** - Preserve history

### Cross-Linking

Use relative paths:
```markdown
See `ARCHITECTURE_OVERVIEW.md` for system design.
See `../TODO.md` for current work.
```

---

## When to Document

### ✅ Always Document:
- Architectural decisions (Why did we choose X?)
- Safety systems (What scar does this prevent?)
- Non-obvious code patterns (Why this way, not that way?)
- Setup/deployment procedures (How do others run this?)

### ⚠️ Sometimes Document:
- Complex algorithms (If not self-explanatory)
- Integration details (If not covered in code)
- Performance considerations (If critical)

### ❌ Don't Document:
- Things the code says clearly (avoid comment duplication)
- Temporary implementation notes (use TODO comments instead)
- Overly detailed API docs (unless public-facing)

---

## Working with AI Collaborators

AI assistants (Claude, ChatGPT, etc.) benefit from this structure:

1. **They can find information** - Predictable locations
2. **They can update docs** - Clear ownership and format
3. **They understand context** - Architecture + philosophy in one place

**Tip:** Point AI to `ARCHITECTURE_OVERVIEW.md` at session start for quick context.

---

## Maintenance

### Document Review Schedule

**Monthly:**
- Update `../TODO.md` (keep current)
- Check core docs for accuracy

**Quarterly:**
- Review `archives/` for expiration candidates
- Update this README if structure changes
- Check for broken cross-links

**Annually:**
- Full documentation audit
- Archive deprecated features
- Compress old implementations

### Archive Cleanup Process

```bash
# Generate cleanup candidates (if script exists)
python scripts/tools/generate_archive_cleanup_report.py

# Output: data/reports/archive_cleanup_YYYY-MM-DD.txt
# Review manually before deleting anything
```

---

## Documentation Anti-Patterns

### ❌ Root-Level Sprawl
```
project/
├── README.md
├── ARCHITECTURE.md
├── SETUP.md
├── DEPLOY.md
├── OLD_ARCHITECTURE.md    # Lost in the noise
├── SETUP_NEW.md           # Which one is current?
└── ... (20 more docs)
```

### ✅ Organized Structure
```
project/
├── README.md              # Project overview only
├── TODO.md                # Current work
├── Documents/
│   ├── README.md          # This file (index)
│   ├── ARCHITECTURE.md    # Essential docs
│   └── archives/          # Historical docs
```

---

## Related Files

- **Project-wide rules:** `../.cursorrules`
- **AI collaboration:** `../CLAUDE.md` (if exists)
- **Current work:** `../TODO.md`
- **Project vision:** `../ROADMAP.md` (if exists)

---

## Questions?

1. Can't find something? Check this README's index
2. Not sure where to document? Ask in the pattern:
   - Core system? → `Documents/` (root)
   - How-to? → `guides/`
   - Standard/convention? → `reference/`
   - Scar story? → `safety/`
   - Old/superseded? → `archives/`

---

*This structure is based on the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) Documents/ pattern, battle-tested across multiple projects.*

