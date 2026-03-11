# .agentsync - Rule Synchronization System

Auto-generates `CLAUDE.md` from rules/*.md files.

## Quick Reference

```bash
# Sync this project
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync.py project-name

# Sync all projects
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync.py --all

# Preview changes
uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync.py project-name --dry-run
```

## Rules Organization

Edit files in `rules/` - they will be synced to IDE config files in filename order:
- `00_*.md` appears first
- `01_*.md` appears second  
- etc.

## Full Documentation

**📖 [AGENTSYNC_SYSTEM.md](README.md)** - Comprehensive guide covering:
1. What is .agentsync?
2. Directory structure
3. How sync.py works
4. Rules file organization
5. Detecting manual edits
6. Resolving conflicts
7. Best practices
8. Troubleshootingscaffolding
