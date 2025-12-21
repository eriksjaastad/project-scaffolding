# Project Scaffolding

> *The meta-project: Extracting patterns from experiments to build better projects faster.*

---

## What This Is

This is the **scaffolding project** - a collection of patterns, principles, and templates extracted from building multiple deep projects.

**Not a framework.** Not rigid rules. Just battle-tested patterns that make future projects:
- Faster to start
- Easier to maintain  
- Safer (data doesn't get lost)
- More consistent across collaborators (AI and human)

---

## Current Source Projects

Patterns are being extracted from:

1. **image-workflow** (2.5 months, battle-tested)
   - Documentation structure
   - Safety systems ("every safety system was a scar")
   - Disaster recovery
   - Session archives

2. **Trading Co-Pilot** (3 weeks, Layer 1-3 complete)
   - Railway + Postgres deployment
   - Cron dispatcher pattern
   - Fuzzy grading systems
   - Multi-model comparison

3. **Hypocrisy Now** (ongoing)
   - RSS infrastructure
   - Sentiment analysis
   - Content aggregation

4. **AI Journal** (ongoing)
   - Documentation patterns
   - Personal knowledge management

---

## Philosophy

**Core document:** `/Users/eriksjaastad/projects/Trading Projects/PROJECT_PHILOSOPHY.md`

Key principles:
- **We're explorers** - Building experiments, not products
- **Data before decisions** - 30-60 days before judging
- **Two-level game** - Domain patterns + Meta patterns (this project!)
- **The scaffolding is the real product** - Learning how to build maintainable projects

---

## What We're Building Toward

A **template repository** that gives every new project:

1. **Standard structure** (`Documents/`, `.cursorrules`, etc.)
2. **Safety systems** (backups, disaster recovery, data integrity)
3. **Testing approach** (what needs tests, what doesn't)
4. **Deployment patterns** (Railway, .env, cron, databases)
5. **Documentation templates** (README, ARCHITECTURE, SESSION_LOGS)
6. **Decision frameworks** (when to build, consolidate, kill features)

---

## Current Status

**Phase:** Discovery & Pattern Collection

**Not ready for:**
- Creating the template repo yet
- Rigid frameworks or rules
- Forcing patterns before they're proven

**Ready for:**
- Documenting patterns as we notice them
- Cross-project comparisons
- Collecting "scar stories" (what broke and how we fixed it)

---

## Structure (Growing)

```
project-scaffolding/
├── README.md                    ← You are here
├── patterns/
│   ├── documentation.md         ← How to structure project docs
│   ├── safety-systems.md        ← Data protection patterns
│   ├── testing.md               ← Testing philosophy
│   ├── deployment.md            ← Railway, env, cron patterns
│   └── ai-collaboration.md      ← Working with AI assistants
├── templates/
│   ├── .cursorrules.template    ← Project rules template
│   ├── CLAUDE.md.template       ← AI instructions template
│   └── README.template          ← Project README template
├── examples/
│   └── (Real examples from source projects)
└── docs/
    └── extracting-patterns.md   ← How to identify patterns worth documenting
```

---

## How to Contribute to This

When working on any project, notice:
1. **Patterns repeating** across 2+ projects (document it)
2. **Decisions you wish you'd made earlier** (capture the framework)
3. **Safety systems that saved you** (document why they exist)
4. **Structures that make maintenance easier** (extract the pattern)

Don't force it. Let patterns emerge naturally.

---

## Timeline

- **Now - Month 2:** Pattern collection phase
- **Month 3:** First consolidation (group patterns into categories)
- **Month 4:** Extract templates from proven patterns
- **Month 6:** Consider creating the actual `project-scaffolding-template` repo

---

*This is a living meta-project. It grows as we learn.*  
*Started: December 21, 2025*

