# Autonomous Loops - Installation & Setup Guide

## Overview

The autonomous loops system provides continuous monitoring and maintenance for all projects:

- **Janitor** - Health monitoring, dependency checks, application heartbeats (runs hourly)
- **Librarian** - Template drift detection (runs every 6 hours)
- **Patch-Bot** - Bounded automated fixes (runs every 30 minutes)

## Prerequisites

### 1. Install Python Dependencies

```bash
# Install certifi for HTTPS requests
brew install python-certifi

# Verify installation
python3 -c "import certifi, requests; print('✓ Dependencies installed')"
```

### 2. Database Setup

The loops use the project-tracker database. Ensure it's initialized:

```bash
cd /Users/eriksjaastad/projects/project-tracker
./pt scan  # Initialize database
```

## Installation

### 1. Schedule Loops via Cron

```bash
# Edit your crontab
crontab -e

# Add these lines (or use CRON_SCHEDULE.txt):
0 * * * * cd /Users/eriksjaastad/projects/project-scaffolding/autonomous-loops && /opt/homebrew/bin/python3 janitor.py >> /tmp/janitor.log 2>&1
0 */6 * * * cd /Users/eriksjaastad/projects/project-scaffolding/autonomous-loops && /opt/homebrew/bin/python3 librarian.py >> /tmp/librarian.log 2>&1
*/30 * * * * cd /Users/eriksjaastad/projects/project-scaffolding/autonomous-loops && /opt/homebrew/bin/python3 patch_bot.py >> /tmp/patch_bot.log 2>&1
```

### 2. Test Manual Execution

```bash
cd /Users/eriksjaastad/projects/project-scaffolding/autonomous-loops

# Test Janitor
python3 janitor.py

# Test Librarian
python3 librarian.py

# Test Patch-Bot
python3 patch_bot.py
```

## Monitoring

### Dashboard

View loop status at: `http://localhost:8000/dashboard`

The "🤖 Autonomous Loops" card shows:
- Health status (🟢 🟡 🔴)
- Last run time
- Cards created
- Error messages

### Check Loop Status

```bash
cd /Users/eriksjaastad/projects/project-tracker
python3 scripts/test_loop_status.py
```

### View Logs

```bash
# Janitor logs
tail -f /tmp/janitor.log

# Librarian logs
tail -f /tmp/librarian.log

# Patch-Bot logs
tail -f /tmp/patch_bot.log
```

## Application Heartbeat Monitoring

The Janitor loop now monitors deployed applications, replacing Healthchecks.io.

### Configured Heartbeats

Edit `janitor.py` to add/modify heartbeat URLs:

```python
heartbeat_urls = {
    "trading-copilot": "https://trading-copilot.up.railway.app/health",
    "cortana-personal-ai": None,  # Local only
}
```

### Health Endpoint Requirements

Your application should expose a `/health` endpoint that:
- Returns HTTP 200 when healthy
- Responds within 10 seconds
- Can be accessed publicly

Example (FastAPI):
```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

## Troubleshooting

### Loop Not Running

1. Check cron is active:
   ```bash
   crontab -l  # List current cron jobs
   ```

2. Check logs for errors:
   ```bash
   tail -50 /tmp/janitor.log
   ```

3. Test manual execution:
   ```bash
   cd autonomous-loops && python3 janitor.py
   ```

### Missing Dependencies

```bash
# Install certifi
brew install python-certifi

# Install requests (usually pre-installed)
python3 -m pip install --user requests
```

### Database Errors

```bash
# Verify database exists
ls -lh /Users/eriksjaastad/projects/project-tracker/data/tracker.db

# Re-scan projects
cd /Users/eriksjaastad/projects/project-tracker
./pt scan
```

## Configuration

### Loop Intervals

Modify in `config/loops.yaml`:

```yaml
loops:
  janitor:
    interval_hours: 1
    tier_rotation: [1, 2, 1, 2, 1, 2, 1, 2]
  
  librarian:
    interval_hours: 6
  
  patch-bot:
    interval_minutes: 30
```

### Tier System

Projects are assigned tiers for monitoring frequency:

- **Tier 1** (Critical): Checked every run
- **Tier 2** (Standard): Checked every other run
- **Tier 3** (Low Priority): Checked occasionally

## Replacing Healthchecks.io

✅ **Complete!** The autonomous loops now handle all monitoring.

### Migration Checklist

- [x] Implement heartbeat checking in Janitor
- [x] Add `/api/loops` endpoint to dashboard
- [x] Create dashboard monitoring widget
- [x] Remove Healthchecks.io from EXTERNAL_RESOURCES.yaml
- [ ] Cancel Healthchecks.io account
- [ ] Remove `TRADING_HEALTHCHECKS_KEY` from `.env`

## Architecture

See `ARCHITECTURE.md` for detailed documentation on:
- Loop responsibilities
- Safety boundaries
- Autonomy levels
- Error handling
- Escalation protocols

## Support

For issues or questions:
1. Check logs: `/tmp/janitor.log`, `/tmp/librarian.log`, `/tmp/patch_bot.log`
2. Review `ARCHITECTURE.md` for design decisions
3. Check dashboard for loop health status
4. Review created Kanban cards for detected issues
