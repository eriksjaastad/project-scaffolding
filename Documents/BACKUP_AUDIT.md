# Backup Audit Report

**Generated:** 2026-01-27  
**Scope:** All projects in ecosystem

---

## Projects with SQLite Databases

| Project | Database | Purpose | Has JSON Export | Priority |
|---------|----------|---------|-----------------|----------|
| project-tracker | data/tracker.db | Task/project tracking | Unknown | High |
| project-tracker | data/projects.db | Project metadata | Unknown | High |
| project-tracker | tracker.db | Legacy/duplicate? | Unknown | Low |
| ai-usage-billing-tracker | data/usage.db | API usage stats | Unknown | Medium |
| trading-copilot | data/model_arena.db | Model comparison | Unknown | Low |
| tax-organizer | tax_organizer.db | Tax document tracking | Unknown | Medium |
| hypocrisynow | hypocrisynow.db | Detection data | Unknown | Low |
| hypocrisynow | detection_cache.db | Cache (ephemeral) | N/A | None |
| hypocrisynow | *_backup_*.db | Backup file | N/A | None |

**Total:** 9 database files across 5 projects

---

## Analysis

### High Priority (Critical Data)
- **project-tracker**: Contains task prompts, project metadata, kanban state
  - Recommendation: Implement JSON export for tasks and projects
  - Already has infrastructure for this

### Medium Priority (Useful Data)
- **ai-usage-billing-tracker**: API usage and cost tracking
  - Recommendation: JSON export for cost analysis and portability
- **tax-organizer**: Tax document organization
  - Recommendation: JSON export if data is valuable year-over-year

### Low Priority (Ephemeral/Cache)
- **trading-copilot**: Model arena comparisons (can be regenerated)
- **hypocrisynow**: Detection cache and results (ephemeral)

---

## Recommendations

1. **project-tracker** should have JSON export as it contains critical workflow data
2. Cache databases (detection_cache.db) don't need backup
3. Backup files (*_backup_*.db) are already backups, no action needed
4. Consider SQLite `.dump` for disaster recovery, JSON for portability

---

## Next Steps

Review each high/medium priority database and decide:
- Does this data need to be version-controlled (JSON export)?
- Is there existing export capability?
- What's the recovery story if the DB is lost?
