# Cursor Security Configuration

This directory contains Cursor agent rules for prompt-level guidance. However, **rules alone don't enforce behavior** - you must also configure Cursor's UI settings.

## Required UI Configuration

Open Cursor and navigate to: **Settings → Cursor Settings → Agents → Auto-Run**

### Step 1: Set Auto-Run Mode
| Setting | Recommended Value |
|---------|-------------------|
| **Auto-Run Mode** | "Ask Every Time" |

This ensures ALL commands require manual approval by default.

### Step 2: Clear Command Allowlist
Start with an empty allowlist. Add commands back only as needed with justification.

### Step 3: Enable Protection Toggles
| Protection | Status |
|------------|--------|
| File-Deletion Protection | ON |
| Dotfile Protection | ON |
| External-File Protection | ON |

## Defense Layers

| Layer | Type | Enforcement |
|-------|------|-------------|
| 1. Cursor UI Settings | Allowlist | **Hard** - blocks execution |
| 2. Shell-level blocks (.zshrc) | Delete commands | **Hard** - blocks execution |
| 3. .cursor/rules/*.md | Prompt guidance | **Soft** - can be ignored |
| 4. .cursorrules | Prompt guidance | **Soft** - can be ignored |

## Files in This Directory

- `00_security_allowlist.md` - Default-deny policy, command categories
- `README.md` - This file

## Adding to Allowlist

When adding a command to Cursor's auto-run allowlist, document WHY:

```
Command: pytest
Justification: Test runner, read-only on code, no network access
Risk level: Low
```

Keep this documentation in your project's security log.
