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
- CLAUDE.md present with behavior rules

### Validation
- `pytest tests/` passes (security tests included)
- Pre-commit and pre-push git hooks installed and passing
- Zero unfilled `{{VAR}}` placeholders in `.md`, `.py`, `.sh` files

## Quick Check

```bash
# From project root
pytest tests/ -v
grep -RInE '\{\{[A-Z_]+\}\}' --include='*.md' --include='*.py' --include='*.sh' .
```

Both must pass (zero placeholder hits) for Gold Standard status.
