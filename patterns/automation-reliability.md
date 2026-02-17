# Automation Reliability Patterns

> **Philosophy:** "Silent failures are the worst failures"
> **Source:** Cortana Personal AI outage (January 2026)
> **Last Updated:** January 10, 2026

---

## The Inaugural Scar: Cortana's 22-Day Silent Failure

**What happened:** Cortana's daily update automation failed silently for 22 days (December 18, 2025 - January 10, 2026). Only discovered when Erik manually asked "is Cortana still running?" during an unrelated late-night session.

**Root causes:**

1. **Cross-Project Dependency:** `run_daily_update.sh` sourced agent-os's virtual environment
   ```bash
   # BROKEN - depended on external project
   source "../../YOUR_PROJECT/venv/bin/activate"
   ../../YOUR_PROJECT/venv/bin/python scripts/core/daily_update.py
   ```

2. **Silent Bash Failure:** When agent-os was cleaned up, the `source` command failed, but bash didn't exit. The script continued but python never ran. No output = nothing logged.

3. **No Heartbeat:** No mechanism to detect "script ran but produced nothing" vs "script succeeded."

4. **No Monitoring:** No alert for "haven't seen a successful run in 24+ hours."

5. **Undocumented Dependency:** Nobody knew Cortana depended on agent-os. When agent-os was cleaned up, it was believed "nothing uses this."

**Impact:**
- 22 days of voice recordings not processed
- Had to backfill 130 dates (mystery: why 130, not 22?)
- Trust erosion in automation systems

**Fix applied:**
```bash
# FIXED - self-sufficient
cd "../../cortana-personal-ai"
export $(grep -v '^#' .env | xargs)
doppler run -- uv run python scripts/core/daily_update.py
```

---

## Pattern 1: Self-Sufficient Automation

### What

Every automated script contains everything it needs to run. No external project dependencies.

### When to Use

- LaunchAgents / cron jobs
- Scheduled tasks
- Any automation that runs unattended

### Implementation

**Each project needs:**
- Its own virtual environment (`./venv/`)
- Its own environment file (`.env`)
- Its own dependencies (`requirements.txt`)

**Shell script pattern:**

```bash
#!/bin/bash
# Self-sufficient automation script
# No external dependencies - everything in this project

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Change to project directory FIRST
cd "/path/to/project"

# Load THIS project's environment
export $(grep -v '^#' .env | xargs)

# Use THIS project's dependencies via uv
uv run python scripts/my_script.py
```

**Anti-pattern (what broke Cortana):**

```bash
#!/bin/bash
# BAD - depends on external project
source "/path/to/OTHER_PROJECT/venv/bin/activate"  # <-- External dependency!
uv run python scripts/my_script.py
```

### Checklist

- [ ] Script uses project's own venv (`./venv/bin/python`)
- [ ] Script uses project's own .env file
- [ ] No `source` from other project directories
- [ ] No imports from sibling projects
- [ ] Can run after cloning fresh (with `pip install -r requirements.txt`)

---

## Pattern 2: Heartbeat Files

### What

Write a timestamp file on every successful run. Stale heartbeat = something is wrong.

### When to Use

- Any scheduled/automated task
- Background services
- Jobs that should run daily/hourly

### Implementation

```bash
from pathlib import Path
from datetime import datetime
import json

def write_heartbeat(project_dir: Path, script_name: str) -> None:
    """
    Write heartbeat file on successful completion.

    Creates: data/logs/heartbeat.json
    {
        "last_success": "2026-01-10T22:00:05",
        "script": "daily_update.py",
        "status": "ok"
    }
    """
    heartbeat_file = project_dir / "data" / "logs" / "heartbeat.json"
    heartbeat_file.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "last_success": datetime.now().isoformat(),
        "script": script_name,
        "status": "ok"
    }

    heartbeat_file.write_text(json.dumps(data, indent=2))
```

**Usage in scripts:**

```bash
def main():
    try:
        # ... do the work ...

        # Only write heartbeat on SUCCESS
        write_heartbeat(PROJECT_DIR, "daily_update.py")

    except Exception as e:
        # Log error but DON'T write heartbeat
        # Stale heartbeat = alert trigger
        logging.error(f"Failed: {e}")
        raise
```

### Monitoring the Heartbeat

```bash
# Check if heartbeat is stale (older than 25 hours for daily job)
doppler run -- python -c "
import json
from pathlib import Path
from datetime import datetime, timedelta

hb = json.loads(Path('data/logs/heartbeat.json').read_text())
last = datetime.fromisoformat(hb['last_success'])
if datetime.now() - last > timedelta(hours=25):
    print(f'STALE: Last success was {last}')
    exit(1)
print(f'OK: Last success was {last}')
"
```

---

## Pattern 3: Discord Failure Alerts

### What

Send Discord notification on script completion (success or failure). Silence = something is very wrong.

### When to Use

- Critical automation (like Cortana's daily memories)
- Jobs where failure has consequences
- Anything you'd be upset to discover broken after 22 days

### Implementation

```bash
import json
import urllib.request
from datetime import datetime
from pathlib import Path

def send_discord_notification(
    webhook_url: str,
    project_name: str,
    success: bool,
    details: str = ""
) -> None:
    """
    Send status notification to Discord.

    Success: Brief confirmation
    Failure: Loud alert with details
    """
    if success:
        message = {
            "content": f"**{project_name}** daily update complete",
            "embeds": [{
                "color": 0x00FF00,  # Green
                "fields": [
                    {"name": "Status", "value": "Success", "inline": True},
                    {"name": "Time", "value": datetime.now().strftime("%I:%M %p"), "inline": True}
                ],
                "footer": {"text": details[:200] if details else "All systems operational"}
            }]
        }
    else:
        message = {
            "content": f"**{project_name}** FAILED",
            "embeds": [{
                "color": 0xFF0000,  # Red
                "fields": [
                    {"name": "Status", "value": "FAILURE", "inline": True},
                    {"name": "Time", "value": datetime.now().strftime("%I:%M %p"), "inline": True},
                    {"name": "Error", "value": details[:500] if details else "Unknown error"}
                ]
            }]
        }

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(message).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        # Don't fail the script if Discord is down
        print(f"Warning: Discord notification failed: {e}")
```

**Wrapper pattern for scripts:**

```bash
import os
import sys
import traceback

def main_with_notifications():
    """Run main() with Discord notifications on success/failure."""
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    try:
        main()  # Your actual logic

        if webhook_url:
            send_discord_notification(
                webhook_url,
                "Cortana",
                success=True,
                details="Daily memories processed"
            )

    except Exception as e:
        if webhook_url:
            send_discord_notification(
                webhook_url,
                "Cortana",
                success=False,
                details=f"{e}\n\n{traceback.format_exc()}"
            )
        raise

if __name__ == "__main__":
    main_with_notifications()
```

---

## Pattern 4: Bash Error Handling

### What

Make bash scripts fail loudly instead of silently continuing.

### When to Use

- All automation wrapper scripts
- Any bash script that runs unattended

### Implementation

```bash
#!/bin/bash
# ALWAYS start with these flags for automation scripts

set -euo pipefail
# -e: Exit immediately if a command exits with non-zero status
# -u: Treat unset variables as an error
# -o pipefail: Pipeline fails if any command fails

# Optional: Trap errors for cleanup/notification
trap 'echo "ERROR on line $LINENO"; exit 1' ERR

# Now your script will FAIL LOUDLY instead of silently continuing
cd "/path/to/project"
export $(grep -v '^#' .env | xargs)
uv run python scripts/my_script.py
```

**Why this matters (the Cortana failure):**

Without `set -e`, this happens:
```bash
source "/nonexistent/venv/bin/activate"  # Fails silently
uv run python scripts/daily_update.py           # Never runs, no error shown
# Script "succeeds" but did nothing
```

With `set -e`:
```bash
source "/nonexistent/venv/bin/activate"  # Script EXITS with error
# Clear failure, shows in logs
```

---

## Pattern 5: Document Cross-Project Dependencies

### What

Explicitly document when Project A depends on Project B.

### When to Use

- Any project that imports from, sources, or uses resources from another project
- Shared virtual environments (anti-pattern, but document if exists)
- Shared .env files (anti-pattern, but document if exists)

### Implementation

**In EXTERNAL_RESOURCES.yaml:**

```yaml
cortana-personal-ai:
  dependencies:
    internal:
      - project: YOUR_PROJECT
        type: virtual_environment  # BAD - caused the failure
        path: "[absolute_path]/.../YOUR_PROJECT/venv"
        why: "Shared Python environment"
        status: REMOVED  # Fixed!
```bash

**In project's CLAUDE.md:**

```markdown
## Dependencies

### External Projects
- **NONE** - This project is self-sufficient

### If you must have cross-project deps (avoid!):
Document here with:
- Which project
- What specifically (venv, .env, module import)
- Why this dependency exists
- What breaks if that project changes
```bash

### Before Removing/Modifying a Project

1. Check EXTERNAL_RESOURCES.yaml for `dependencies.internal`
2. Search all projects: `grep -r "project-name" ~/projects/*/`
3. Check for symlinks: `find ~/projects -type l -ls | grep project-name`
4. Ask: "What depends on this?"

---

## Anti-Patterns

### Silent Bash Scripts

```bash
#!/bin/bash
# BAD - no error handling, will silently fail

source something_that_might_not_exist
do_thing
do_other_thing
# If any of these fail, script continues, no error shown
```bash

### Cross-Project Virtual Environments

```bash
# BAD - external dependency
source "/path/to/OTHER_PROJECT/venv/bin/activate"
```bash

### No Monitoring

```
LaunchAgent runs daily
No Discord notification
No heartbeat file
No health check
→ Can fail for 22 days without anyone noticing
```bash

### Undocumented Dependencies

```
Project A uses Project B's venv
Nobody wrote this down
Project B gets cleaned up
Project A breaks silently
```

---

## Automation Reliability Checklist

When setting up new automation:

### Self-Sufficiency
- [ ] Project has its own venv
- [ ] Project has its own .env
- [ ] Wrapper script uses `set -euo pipefail`
- [ ] No `source` or imports from other projects

### Monitoring
- [ ] Discord webhook for success/failure notifications
- [ ] Heartbeat file updated on success
- [ ] Autonomous Loops monitoring (Janitor checks application health)

### Documentation
- [ ] Automation documented in project README
- [ ] Dependencies listed in EXTERNAL_RESOURCES.yaml
- [ ] LaunchAgent/cron job documented

### Testing
- [ ] Test what happens when script fails
- [ ] Verify Discord notification fires on failure
- [ ] Verify failure is logged somewhere visible

---

## Related Patterns

- **discord-webhooks-per-project.md** - One channel per project for clear attribution
- **api-key-management.md** - Each project manages its own keys (same principle: self-sufficiency)
- **safety-systems.md** - Data safety patterns (this doc is about automation safety)

---

## Summary

**The core lesson:** Cortana failed silently for 22 days because:
1. It depended on another project's venv
2. Bash didn't fail loudly when source failed
3. No heartbeat or monitoring to detect "nothing happened"
4. No Discord alert to say "I ran" or "I failed"

**The fix:** Make every automation:
1. **Self-sufficient** - Own venv, own .env, no external deps
2. **Loud on failure** - `set -euo pipefail` in bash
3. **Monitored** - Discord notifications, heartbeat files
4. **Documented** - Cross-project deps explicitly listed

---

*"If your automation can fail silently for 22 days, it will."*

**Pattern discovered:** January 10, 2026
**First scar:** Cortana Personal AI (22 days of silent failure)
**Contributed by:** Erik (debugging) + Claude (documentation)

## Related Documentation

- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [Automation Reliability](patterns/automation-reliability.md) - automation
- [Discord Webhooks Per Project](patterns/discord-webhooks-per-project.md) - Discord
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [cortana-personal-ai/README](../../ai-model-scratch-build/README.md) - Cortana AI
