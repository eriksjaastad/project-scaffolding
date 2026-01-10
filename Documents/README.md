# Project Documentation

This project documentation follows a three-part structure to ensure discoverability, maintainability, and hygiene:

## Active OS

The **core standards used daily** (kept at the root for immediate access):

- [PROJECT_STRUCTURE_STANDARDS.md](PROJECT_STRUCTURE_STANDARDS.md)
- [PROJECT_KICKOFF_GUIDE.md](PROJECT_KICKOFF_GUIDE.md)
- [TODO_FORMAT_STANDARD.md](TODO_FORMAT_STANDARD.md)
- [CODE_QUALITY_STANDARDS.md](CODE_QUALITY_STANDARDS.md)
- [PROJECT_INDEXING_SYSTEM.md](PROJECT_INDEXING_SYSTEM.md)

## Full Library Map

**Every file in `guides/` and `reference/` is explicitly listed** to guarantee discoverability. No files are hidden or undocumented.

### Guides
- [CODE_REVIEW_PROMPT.md](guides/CODE_REVIEW_PROMPT.md)
- [DEEPSEEK_SETUP.md](guides/DEEPSEEK_SETUP.md)
- [FREE_CREDITS_GUIDE.md](guides/FREE_CREDITS_GUIDE.md)
- [PROJECT_INDEX_ENFORCEMENT.md](guides/PROJECT_INDEX_ENFORCEMENT.md)
- [USAGE_GUIDE.md](guides/USAGE_GUIDE.md)

### Reference
- [CODE_REVIEW_ANTI_PATTERNS.md](reference/CODE_REVIEW_ANTI_PATTERNS.md)
- [MODEL_COST_COMPARISON.md](reference/MODEL_COST_COMPARISON.md)
- [PATTERN_ANALYSIS.md](reference/PATTERN_ANALYSIS.md)
- [PATTERN_MANAGEMENT.md](reference/PATTERN_MANAGEMENT.md)
- [REVIEW_SYSTEM_DESIGN.md](reference/REVIEW_SYSTEM_DESIGN.md)

### Reports
- [trustworthy_ai_report.md](reports/trustworthy_ai_report.md) - Industry patterns for making AI trustworthy in production (Google DeepMind, Anthropic, OpenAI, Microsoft case studies)
- [WARDEN_RESEARCH_REPORT.md](reports/WARDEN_RESEARCH_REPORT.md) - Research phase analysis for Warden enhancement (Jan 10, 2026)
- [WARDEN_PROMPTS_INDEX.md](reports/WARDEN_PROMPTS_INDEX.md) - Worker task prompts for Warden enhancement (4 focused prompts)

## Archives

*Historical data* (too large to list individually) - only high-level structure descriptions:

- `planning/`: Historical planning and context handoff
- `research/`: Research prompts and cost-saving explorations
- `reviews/`: Past audits and reviews
- `sessions/`: Record of development sessions

## Hygiene

We enforce strict documentation hygiene: **only useful documentation survives**. This means:

1. ❌ **Remove** outdated files from `guides/` and `reference/`
2. ✅ **Archive** completed work in `archives/` (not in active libraries)
3. ⚠️ **Never** create files that don't add immediate value

> ℹ️ *This ensures our documentation remains actionable, not cluttered*

---

*This README is maintained by the Project Documentation Team*
