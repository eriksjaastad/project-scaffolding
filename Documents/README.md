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
- [AUDIT_ASSEMBLY_LINE.md](guides/AUDIT_ASSEMBLY_LINE.md) - Standardized process for ecosystem-wide project hardening
- [CODE_REVIEW_PROMPT.md](guides/CODE_REVIEW_PROMPT.md)
- [DEEPSEEK_SETUP.md](guides/DEEPSEEK_SETUP.md)
- [FREE_CREDITS_GUIDE.md](guides/FREE_CREDITS_GUIDE.md)
- [REPOMIX_USAGE.md](guides/REPOMIX_USAGE.md) - How to use Repomix for project audits and context bundling
- [USAGE_GUIDE.md](guides/USAGE_GUIDE.md)

### Reference
- [CODE_REVIEW_ANTI_PATTERNS.md](reference/CODE_REVIEW_ANTI_PATTERNS.md)
- [DOCUMENTATION_HYGIENE.md](reference/DOCUMENTATION_HYGIENE.md)
- [DOPPLER_MIGRATION_PLAN.md](reference/DOPPLER_MIGRATION_PLAN.md) - Historical record of Doppler secrets management migration
- [DOPPLER_SECRETS_MANAGEMENT.md](reference/DOPPLER_SECRETS_MANAGEMENT.md) - Comprehensive guide for Doppler usage across ecosystem
- [LOCAL_MODEL_LEARNINGS.md](reference/LOCAL_MODEL_LEARNINGS.md)
- [MODEL_COST_COMPARISON.md](reference/MODEL_COST_COMPARISON.md)
- [PATTERN_ANALYSIS.md](reference/PATTERN_ANALYSIS.md)
- [PATTERN_MANAGEMENT.md](reference/PATTERN_MANAGEMENT.md)
- [REVIEW_SYSTEM_DESIGN.md](reference/REVIEW_SYSTEM_DESIGN.md)

### Reports
- [trustworthy_ai_report.md](reports/trustworthy_ai_report.md) - Industry patterns for making AI trustworthy in production (Google DeepMind, Anthropic, OpenAI, Microsoft case studies)

## Archives
- `planning/`: Historical planning and context handoff
  - `knowledge_transfer_pt/`: Obsolete 12-prompt approach for standalone projects (Jan 12, 2026)
  - `warden_evolution/`: Research and prompts for Warden security enhancement (Jan 10, 2026)
  - `safety/audit/`: Prompts and index for Safety Audit and send2trash migration (Jan 10, 2026)
  - `PROJECT_INDEX_ENFORCEMENT.md`: Obsolete enforcement doc (Jan 12, 2026)
  - `Do you have any other recommendations for research.md`: Research report (Jan 12, 2026)
  - `QUICKSTART_VALIDATION_REPORT_2026-01-11.md`: One-off validation report (Jan 12, 2026)
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
