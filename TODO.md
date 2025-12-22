# Project Scaffolding - TODO

> **Purpose:** Track work specific to project-scaffolding meta-project  
> **Last Updated:** December 22, 2025

---

## Current Status

**Phase:** Pattern extraction and template creation  
**Status:** Core patterns documented, templates created

---

## Open Questions

### Q1: Planning Phase Tiering
**Question:** How to handle tier escalation when planning? Bottom-up scoring?

**Context:** 
- Tiered Sprint Planner uses bottom-up tiering (Tier 3 → 2 → 1)
- But planning phase itself is Tier 1 work (architecture, breaking down problems)
- How to break down planning tasks by tier?

**Needs:**
- Discussion with Erik
- Examples from real planning sessions
- Pattern documentation if we find one

---

## Future Pattern Extraction (When Ready)

### From agent_os (When 2-3 Projects Use It)
- [ ] Run tracking pattern (status, timestamps, errors)
- [ ] Plugin system pattern (provider-agnostic infrastructure)
- [ ] Idempotent execution pattern (database constraints)

**Wait for:** agent_os architecture decisions, other projects adopting patterns

---

### Email Monitoring Pattern (When land + billing-tracker Built)
- [ ] Email monitoring agent pattern
- [ ] Criteria evaluation pattern
- [ ] Notification dispatch pattern

**Wait for:** land project and billing-tracker implementation

---

### Job Crawler Pattern (If Built)
- [ ] Job listing scraping
- [ ] Automated business opportunity identification
- [ ] Service arbitrage pattern

**Wait for:** Job crawler project to prove itself

---

## Maintenance Tasks

### Regular Updates
- [ ] Review patterns quarterly (are they still accurate?)
- [ ] Update EXTERNAL_RESOURCES.md as services added
- [ ] Extract patterns when 2-3 projects show same approach
- [ ] Update templates based on real project usage

### Documentation Health
- [ ] Keep README current with project status
- [ ] Archive outdated session notes
- [ ] Ensure all patterns have "last updated" dates
- [ ] Check that examples still match current projects

---

## Success Metrics

**Pattern Adoption:**
- How many new projects use scaffolding templates?
- Which patterns get adopted vs ignored?
- Are projects more consistent?

**Time Savings:**
- Does scaffolding reduce new project setup time?
- Are patterns saving time on repeat problems?

**Chaos Reduction:**
- Is EXTERNAL_RESOURCES.md preventing duplicate services?
- Are API key patterns preventing confusion?
- Is tiered sprint planning managing costs?

---

## Related Projects

**project-tracker:** 
- Integration documented in `project-tracker/docs/INTEGRATION_WITH_SCAFFOLDING.md`
- Tracker reads EXTERNAL_RESOURCES.md
- Tracker shows which projects use scaffolding templates

**Other projects:**
- Source patterns from: image-workflow, Trading Co-Pilot, Cortana, Hologram
- Extract patterns TO: This project
- Apply patterns IN: All future projects

---

## Notes

**The two-level game:**
- Level 1: Domain projects (trading, images, AI)
- Level 2: Meta projects (scaffolding, tracker)

This is a Level 2 project. It doesn't ship product. It ships TOOLS to build products.

Success = Other projects are easier because of this one.

---

**Last Updated:** December 22, 2025  
**Next Review:** End of January 2026 (after holidays, new projects in 2026)

