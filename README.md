# Project Scaffolding

> *The meta-project: Extracting patterns from experiments to build better projects faster.*

---

## What This Is

This is the **scaffolding project** - a collection of patterns, principles, and templates extracted from building multiple deep projects.

**Our Mission:** Help all projects get done quickly at the highest quality and at the lowest cost.

**Not a framework.** Not rigid rules. Just battle-tested patterns that make future projects:
- Faster to start
- Easier to maintain  
- Safer (data doesn't get lost)
- More consistent across collaborators (AI and human)

**What We DON'T Do:**
- ❌ Cost tracking (that's `AI usage-billing tracker`'s job)
- ❌ Project status monitoring (that's `project-tracker`'s job)
- ✅ We recommend patterns and build automation; others implement monitoring

---

## Quick Start

### Starting a New Project

1. **Read** `docs/PROJECT_KICKOFF_GUIDE.md` - Complete walkthrough for new projects
2. **Follow** `docs/PROJECT_STRUCTURE_STANDARDS.md` - Standard directory layout (venv in root!)
3. **Follow** `docs/CODE_QUALITY_STANDARDS.md` - **MANDATORY** rules (NO silent failures!)
4. **Copy** templates to your new project - Documentation, .cursorrules, CLAUDE.md
5. **Plan** using Tiered AI Sprint Planning - Break work into cost-effective tiers
6. **Execute** with appropriate models - Tier 1 for architecture, Tier 3 for boilerplate
7. **Track** external resources - Update EXTERNAL_RESOURCES.md when adding services

### Understanding This Scaffolding

1. **Pattern Analysis** (`docs/PATTERN_ANALYSIS.md`)
   - See all identified patterns with confidence levels
   - Understand which are proven (🟢), emerging (🟡), or candidates (🔵)

2. **Safety Systems** (`patterns/safety-systems.md`)
   - 6 proven patterns with code examples
   - "Every safety system was a scar" philosophy
   - Real scar stories from projects

3. **Development Philosophy** (`patterns/development-philosophy.md`)
   - 7 core principles: Layer-by-layer, data before decisions, etc.
   - When to apply, when not to apply
   - Anti-patterns to avoid

4. **Tiered AI Sprint Planning** (`patterns/tiered-ai-sprint-planning.md`)
   - Route tasks to cost-appropriate AI models
   - 3 tiers: Big Brain (architecture), Mid-Weight (features), Worker Bee (boilerplate)
   - Escalation system to avoid getting stuck with wrong-tier models
   - Multi-model review automation (from image-workflow)

### Managing Your Projects

**NEW:** `EXTERNAL_RESOURCES.md` - Track which services/APIs each project uses
- Prevents "I got a bill but don't know which project" situations
- Cost tracking across all projects
- Credential locations documented
- Service health monitoring

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

3. **Cortana Personal AI** (Layer 1 complete)
   - Privacy-first architecture
   - Daily automation via launchd
   - Layer-by-layer development (incrementally useful)
   - Local-first data with structured memory storage
   - Cost-conscious AI usage (~$0.60/month)

4. **Hypocrisy Now** (ongoing)
   - RSS infrastructure
   - Sentiment analysis
   - Content aggregation

5. **AI Journal** (ongoing)
   - Documentation patterns
   - Personal knowledge management

---

## Philosophy

**Core document:** `PROJECT_PHILOSOPHY.md` (this directory)

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

**Phase:** Discovery & Pattern Collection → **Initial Extraction Complete! ✅**

**What's Ready:**
- ✅ **Pattern Analysis** - 20+ patterns identified and documented
- ✅ **Templates** - Documentation structure, CLAUDE.md, .cursorrules, Tiered Sprint Planner
- ✅ **Safety Systems** - 6 proven patterns documented with code examples
- ✅ **Development Philosophy** - 7 core principles extracted
- ✅ **Tiered AI Sprint Planning** - Cost-effective AI usage pattern documented
- ✅ **Project Kickoff Guide** - Complete walkthrough for starting new projects
- ✅ **Usage Guide** - How to use this scaffolding in new projects
- ✅ **External Resources Tracking** - System to prevent duplicate services and surprise bills

**Ready for:**
- ✅ Using templates in new projects
- ✅ Following documented patterns
- ✅ Contributing new patterns as they emerge
- ✅ Extracting examples from source projects

**Next phases:**
- Month 2-3: Extract real examples from source projects
- Month 3: Consolidate patterns into categories
- Month 4: Refine templates based on usage
- Month 6: Consider creating actual `project-scaffolding-template` repo

---

## Structure

```
project-scaffolding/
├── README.md                    ← You are here
├── .cursorrules                 ← Project rules for this meta-project
│
├── patterns/                    ← Documented patterns (proven & emerging)
│   ├── safety-systems.md        ← Data protection patterns ✅
│   ├── development-philosophy.md ← Development principles ✅
│   └── tiered-ai-sprint-planning.md ← Cost-effective AI usage ✅
│
├── templates/                   ← Reusable starting points
│   ├── Documents/               ← Documentation structure template ✅
│   │   ├── README.md            ← Index and usage guide
│   │   ├── core/                ← Architecture, operations
│   │   ├── guides/              ← How-to documents
│   │   ├── reference/           ← Standards, knowledge base
│   │   ├── safety/              ← Safety systems
│   │   └── archives/            ← Historical docs with retention
│   ├── .cursorrules.template    ← Project rules template ✅
│   ├── CLAUDE.md.template       ← AI instructions template ✅
│   └── TIERED_SPRINT_PLANNER.md ← Sprint planning template ✅
│
├── examples/                    ← Real examples from source projects
│   └── (Coming soon - extracted from battle-tested projects)
│
└── docs/                        ← Meta-documentation
    ├── PATTERN_ANALYSIS.md      ← Pattern extraction analysis ✅
    ├── USAGE_GUIDE.md           ← How to use this scaffolding ✅
    └── PROJECT_KICKOFF_GUIDE.md ← Starting new projects guide ✅
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

