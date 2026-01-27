# Scaffolding as Dependency (DRAFT)

**Pattern Type:** Draft - Needs Discussion
**Created:** January 10, 2026
**Status:** Conceptual - Pre-Implementation

---

## The Problem

When project-scaffolding applies rules/templates to existing projects, it can steamroll intentional decisions.

**Example:** Cortana has:
- `WHY_WERE_PAUSING.md` - Intentional decision to slow down
- `ETHICS_AND_SAFETY.md` - Project-specific values framework
- A philosophy of "slow is sustainable"

If we blindly apply scaffolding patterns like "ship fast" or "automate everything," we destroy the intentional context.

**The Core Issue:**
Scaffolding treats all projects as blank slates. It doesn't:
1. Understand what already exists
2. Distinguish intentional decisions from gaps
3. Preserve project-specific context during updates

---

## The Vision: Scaffolding as a Dependency

Think of project-scaffolding like a **node_module** that projects inherit from:

```
project-scaffolding (base)
    ├── patterns/
    ├── templates/
    └── rules/
         │
         ▼ inherits
    ┌─────────────┐
    │  Cortana    │ ← has local overrides
    │  - .scaffold-config.yaml
    │  - preserves WHY_WERE_PAUSING.md
    │  - opts out of "velocity" patterns
    └─────────────┘
```

**Like npm/node_modules:**
- Projects declare which version of scaffolding they use
- Updates can be pulled (like `npm update`)
- Local config survives updates (like `package.json` overrides)
- Breaking changes are versioned

---

## Key Concepts

### 1. Project Scaffolding Manifest

Each project that uses scaffolding has a manifest:

```yaml
# .scaffold-config.yaml

scaffolding:
  version: "1.2.0"  # Which version of scaffolding this project follows

  # What we inherit
  inherit:
    - patterns/safety-systems.md
    - patterns/api-key-management.md
    - templates/CLAUDE.md.template

  # What we explicitly don't use (with reason)
  opt_out:
    - patterns/tiered-ai-sprint-planning.md
      reason: "Intentionally paused - see WHY_WERE_PAUSING.md"

  # Project-specific overrides
  overrides:
    velocity: "slow"  # vs default "fast"
    philosophy: "docs/core/WHY_WERE_PAUSING.md"

  # Protected files (never overwrite during updates)
  protected:
    - docs/core/ETHICS_AND_SAFETY.md
    - docs/vision/PERSONAL_AI_ARCHITECTURE_VISION.md
    - WHY_WERE_PAUSING.md
```

### 2. Pre-Application Analysis

Before applying scaffolding to a project:

```
scaffold analyze /path/to/project
```

**Output:**
```
Project: Cortana Personal AI
Existing Foundation Documents:
  ✓ CLAUDE.md (exists, custom content)
  ✓ README.md (exists)
  ✗ AGENTS.md (missing)

Existing Patterns Detected:
  ✓ safety-systems: docs/core/ETHICS_AND_SAFETY.md
  ✓ api-key-management: .env + .gitignore
  ~ foundation-documents-first: PARTIAL (has CLAUDE.md, missing AGENTS.md)

Intentional Documents Found:
  ⚠ WHY_WERE_PAUSING.md - Contains intentional pause rationale
  ⚠ PERSONAL_AI_ARCHITECTURE_VISION.md - Vision document

Recommendation:
  - Add to protected list: WHY_WERE_PAUSING.md
  - Create AGENTS.md (doesn't exist)
  - Do NOT apply velocity patterns (project is intentionally slow)
```

### 3. Reconciliation (Not Overwrite)

When applying updates:

```
scaffold update --project /path/to/cortana
```

**Behavior:**
1. Read `.scaffold-config.yaml`
2. Check what's new in scaffolding since version 1.2.0
3. For each new pattern/template:
   - If in `protected` list → skip
   - If in `opt_out` list → skip
   - If file exists with custom content → propose merge, don't overwrite
   - If file missing → create
4. Generate diff for review before applying

---

## The Understanding Phase

**Before ANY scaffolding is applied to an existing project:**

### Step 1: Discovery
```bash
scaffold discover /path/to/project
```

Scans for:
- Existing documentation structure
- Foundation documents (CLAUDE.md, AGENTS.md, etc.)
- Philosophy/vision documents
- Intentional pauses or slow-down documents
- Ethics/safety frameworks
- Custom patterns already in use

### Step 2: Context Interview

The scaffolding system asks:
- "This project has a `WHY_WERE_PAUSING.md`. Is this still active?"
- "Found custom ethics framework. Should this be protected?"
- "No AGENTS.md found. Should we create one or is this intentional?"

### Step 3: Generate Manifest

Based on discovery + interview, generate `.scaffold-config.yaml` that:
- Documents what's intentional
- Protects custom decisions
- Identifies real gaps (not intentional absences)

---

## Update Flow

When project-scaffolding releases new patterns:

### For Maintainer (you):
1. Version the change (semver)
2. Document what's new
3. Flag breaking changes

### For Projects:
```bash
scaffold check-updates --project /path/to/cortana
```

**Output:**
```
Scaffolding Updates Available:
  Current: 1.2.0
  Latest: 1.3.0

New in 1.3.0:
  + patterns/automation-reliability.md (NEW)
  ~ patterns/safety-systems.md (UPDATED - non-breaking)

Compatibility Check:
  ✓ automation-reliability.md - compatible with project philosophy
  ✓ safety-systems.md - update is additive, no conflicts

Protected Files (will not be touched):
  - WHY_WERE_PAUSING.md
  - ETHICS_AND_SAFETY.md

Run `scaffold update` to apply.
```

---

## Project Maturity Context

The manifest can declare project state:

```yaml
project:
  state: intentional-pause  # incubating | active | mature | intentional-pause

  # What this means for scaffolding
  state_implications:
    intentional-pause:
      - Do not apply velocity patterns
      - Preserve philosophical documents
      - No "ship fast" pressure
```

This tells scaffolding: "This project isn't slow because it's behind. It's slow because that's intentional."

---

## Implementation Phases

### Phase 1: Manual Manifest
- Create `.scaffold-config.yaml` manually for key projects
- Document what's protected and why
- No automation yet

### Phase 2: Discovery Script
- Build `scaffold discover` command
- Auto-detect existing structure
- Propose manifest

### Phase 3: Update Reconciliation
- Build `scaffold update` with diff/merge behavior
- Respect protected files
- Version tracking

### Phase 4: Full Dependency Model
- Scaffolding versions in manifest
- Breaking change detection
- Ecosystem-wide update propagation

---

## Questions to Resolve

1. **Granularity:** File-level protection? Section-level? Line-level?
2. **Versioning:** Semver? Date-based? Git commit hashes?
3. **Breaking Changes:** How do we handle patterns that fundamentally change?
4. **Inheritance Depth:** Can projects inherit from other projects (not just scaffolding)?
5. **Conflict Resolution:** When scaffolding and project disagree, who wins?

---

## Related Patterns

- `foundation-documents-first.md` - The foundation we're protecting
- `safety-systems.md` - Example of a pattern that should be inherited carefully
- `development-philosophy.md` - Philosophy that might be overridden per-project

---

## The Meta-Point

**Project Scaffolding should be a wise mentor, not a bulldozer.**

A good mentor:
- Understands where you are before giving advice
- Respects your intentional decisions
- Offers updates without forcing them
- Knows when to stay silent

A bulldozer:
- Applies rules without context
- Overwrites custom work
- Treats all projects the same
- Values consistency over appropriateness

**We want the mentor.**

---

*"Understand deeply. Apply thoughtfully. Preserve intentionality."*

## Related Documentation

- [Automation Reliability](patterns/automation-reliability.md) - automation
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [cortana-personal-ai/README](../../ai-model-scratch-build/README.md) - Cortana AI
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
