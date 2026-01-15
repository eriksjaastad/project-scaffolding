# File Organization Note

**Date:** December 21, 2025

## PROJECT_PHILOSOPHY.md Migration

### What Happened

`PROJECT_PHILOSOPHY.md` was originally created in the trading-copilot directory during an early conversation where the idea for project-scaffolding was first articulated.

However, that file contains **zero trading-specific content**. It's pure meta-project philosophy about:
- Building experiments vs products
- The two-level game (domain + meta patterns)
- The scaffolding vision
- Core principles (consolidate on 3rd duplicate, data before decisions, etc.)

### Resolution

**Moved to canonical location:**
- **From:** `$PROJECTS_ROOT/trading-copilot/PROJECT_PHILOSOPHY.md`
- **To:** `$PROJECTS_ROOT/project-scaffolding/PROJECT_PHILOSOPHY.md`

**Created redirect:** Left a redirect file in trading-copilot pointing to the canonical version.

**Updated references:** All `.cursorrules` and READMEs now point to the correct location.

### Why This Matters

1. **Clearer organization** - Meta content lives in the meta-project
2. **Single source of truth** - Only one authoritative philosophy document
3. **Better discoverability** - Looking in project-scaffolding? The philosophy is there
4. **History preserved** - The redirect maintains continuity

### Pattern Recognition

This itself demonstrates a principle: **Move content to where it conceptually belongs, not where it was first created.**

The trading-copilot directory should contain:
- ✅ Trading-specific philosophy (risk management, playbooks)
- ✅ Model Arena roadmaps
- ✅ Trading scripts and data
- ❌ General project scaffolding philosophy

The project-scaffolding directory should contain:
- ✅ Cross-project patterns
- ✅ Development philosophy
- ✅ Meta-project content
- ❌ Domain-specific content (trading, images, etc.)

---

**Action:** File successfully migrated. No other trading-copilot content is scaffolding-related.

