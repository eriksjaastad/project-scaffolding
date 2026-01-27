# Gold Standard Definition

What "Production Ready" means in this ecosystem.

## Criteria

### Security
- No absolute paths (e.g., `/Users/erik/...`)
- No hardcoded secrets in code

### Safety
- "Trash, Don't Delete" enforced
- Use `send2trash` (Python) or `Trash` command (CLI)

### Infrastructure
- AI Router live (Local-first model routing)
- Secrets in `.env` or Doppler (for legacy projects)

### Governance
- Project Tracker ontology-aware
- `00_Index_*.md` up to date
- AGENTS.md synced via agentsync

### Validation
- `warden_audit.py --fast` passes
- `validate_project.py` passes

## Quick Check

```bash
# From project root
python scripts/warden_audit.py --root . --fast
python scripts/validate_project.py "$(basename $(pwd))"
```

Both must pass for Gold Standard status.
