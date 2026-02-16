# Autonomous Loops Architecture

**Created:** 2026-02-16  
**Status:** Production Ready

## Overview

The Autonomous Loops system provides continuous monitoring, template enforcement, and bounded automated fixes across the project ecosystem. Three specialized loops work together to maintain project health without human intervention.

## The Three Loops

### 1. Janitor Loop 🧹
**Purpose:** Continuous health monitoring  
**Frequency:** Tier-based (Tier 1: hourly, Tier 2: daily, Tier 3: weekly)  
**Operations:** Read-only

**Responsibilities:**
- Run healthcheck commands for each project
- Monitor cron job freshness
- Detect dependency risks (outdated packages, security vulnerabilities)
- Check for broken links in documentation
- Validate project structure integrity

**Outputs:**
- Creates Kanban cards in `TRIAGED` status
- Labels cards with severity (P0/P1/P2)
- Includes evidence and reproduction steps
- Never modifies code or configuration

**Safety Boundaries:**
- Read-only file system access
- No network requests (except to check URLs)
- No code execution (except configured healthcheck commands)
- No database writes (except card creation)

### 2. Librarian Loop 📚
**Purpose:** Template drift detection and auto-fix  
**Frequency:** Tier-based  
**Operations:** Read + conditional write (governed files only)

**Responsibilities:**
- Detect drift from canonical templates
- Validate immutable files haven't changed
- Check extendable file markers (AGENTSYNC blocks)
- Track scaffolding version mismatches
- Optionally auto-fix safe changes

**Outputs:**
- Updates `drift_status` field in projects table
- Creates drift cards in `TRIAGED` status
- Optionally creates PRs for safe fixes (if autonomy_level allows)
- Logs all changes for audit

**Safety Boundaries:**
- Only edits files within `<!-- AGENTSYNC:START -->` markers
- Never touches files outside `.agentsync/rules/`
- Requires `autonomy_level >= 'fix_safe'` for auto-fixes
- Always creates backup before modifications
- Validates checksums after changes

### 3. Patch-Bot Loop 🤖
**Purpose:** Bounded automated fixes  
**Frequency:** Triggered (watches for `READY_FOR_PATCH` status)  
**Operations:** Read + write (within allowed_paths only)

**Responsibilities:**
- Process tasks in `READY_FOR_PATCH` status
- Validate required fields (allowed_paths, definition_of_done)
- Implement deterministic fix workflow
- Create PRs for review
- Escalate on failure or ambiguity

**Workflow:**
1. **Validate:** Check required fields, autonomy level, cost budget
2. **Checkout:** Create isolated branch
3. **Reproduce:** Verify issue exists
4. **Plan:** Generate fix plan, estimate cost
5. **Patch:** Apply changes (only to allowed_paths)
6. **Verify:** Run tests, check definition_of_done
7. **Deliver:** Create PR or commit, move to `PR_READY`

**Safety Boundaries:**
- Hard boundary: NEVER edit outside `allowed_paths`
- Cost control: Escalate if exceeds budget
- Retry limit: Max 3 attempts, then escalate
- Time limit: Timeout after configured duration
- Human escalation: Required for P0 issues or ambiguous fixes

## Autonomy Levels

Projects can configure their autonomy level:

| Level | Janitor | Librarian | Patch-Bot |
|-------|---------|-----------|-----------|
| `report` | ✅ Create cards | ✅ Create cards | ❌ Disabled |
| `fix_safe` | ✅ Create cards | ✅ Auto-fix governed files | ❌ Disabled |
| `fix_bounded` | ✅ Create cards | ✅ Auto-fix governed files | ✅ Fix within allowed_paths |

**Default:** `report` (safest)

## Tier System

Projects are assigned tiers based on criticality:

| Tier | Frequency | Examples |
|------|-----------|----------|
| 1 | Hourly | project-tracker, project-scaffolding |
| 2 | Daily | Most projects |
| 3 | Weekly | Experimental/archived projects |

## Configuration

Loops are configured via YAML files in `project-scaffolding/autonomous-loops/config/`:

- **loops.yaml** - Loop schedules and operations
- **tiers.yaml** - Tier definitions and frequencies
- **models.yaml** - Model selection for different tasks
- **escalation.yaml** - Cost controls and escalation rules

Projects can override global config with `.autonomous-loops.yaml` in their root.

## Monitoring

The Project Tracker dashboard displays loop health at the top:

- **Loop Status:** 🟢 Healthy / 🟡 Warning / 🔴 Failed
- **Last Run:** Timestamp of last execution
- **Next Run:** Scheduled next execution
- **Cards Created:** Count from last run
- **Success Rate:** Over last 24 hours

**Health Logic:**
- 🟢 **Healthy:** Last run within expected interval
- 🟡 **Warning:** Overdue by 1.5x expected interval
- 🔴 **Failed:** Overdue by 2x interval OR last run status was 'failed'

## Safety Philosophy: "Agents Don't Wander"

**Core Principle:** Autonomous agents operate within hard boundaries. They never explore, experiment, or make creative decisions.

**Implementation:**
1. **Explicit Allowlists:** Patch-Bot only edits files in `allowed_paths`
2. **Marker-Based Editing:** Librarian only edits within `<!-- AGENTSYNC -->` blocks
3. **Read-Only Default:** Janitor never modifies anything
4. **Escalation Over Guessing:** When uncertain, create a card for humans
5. **Audit Trail:** All actions logged to `loop_executions` table

## Escalation Paths

Loops escalate to humans when:

- **Cost Threshold:** Exceeds configured budget
- **Retry Limit:** Failed 3 times
- **Ambiguity:** Multiple valid solutions
- **Severity:** P0 issues always require human review
- **Boundary Violation:** Requested action outside allowed scope

**Escalation Actions:**
1. Create detailed card with evidence
2. Set priority based on severity
3. Add `[ESCALATED]` tag
4. Log to monitoring dashboard
5. Optionally send notification (future)

## Running the Loops

**Manual Execution:**
```bash
# Run individual loops
python project-scaffolding/autonomous-loops/janitor.py
python project-scaffolding/autonomous-loops/librarian.py
python project-scaffolding/autonomous-loops/patch_bot.py
```

**Scheduled Execution:**
Add to crontab or use system scheduler:
```bash
# Janitor - every hour
0 * * * * cd /path/to/projects && python project-scaffolding/autonomous-loops/janitor.py

# Librarian - every 6 hours
0 */6 * * * cd /path/to/projects && python project-scaffolding/autonomous-loops/librarian.py

# Patch-Bot - every 30 minutes
*/30 * * * * cd /path/to/projects && python project-scaffolding/autonomous-loops/patch_bot.py
```

## Troubleshooting

### Loop Not Running
1. Check `loop_executions` table for last run
2. Verify cron job is active: `crontab -l`
3. Check logs for errors
4. Verify database connectivity

### Cards Not Being Created
1. Check autonomy_level is not blocking
2. Verify tier configuration
3. Check if issues actually exist
4. Review loop execution logs

### Auto-Fixes Not Applied
1. Verify `autonomy_level >= 'fix_safe'`
2. Check if files have proper markers
3. Review `allowed_paths` configuration
4. Check for permission issues

### High Cost/Token Usage
1. Review escalation rules in `config/escalation.yaml`
2. Check model tier assignments
3. Verify retry limits are reasonable
4. Consider lowering autonomy level

## Future Enhancements

- [ ] Slack/email notifications for failures
- [ ] Web UI for pausing/resuming loops
- [ ] Per-project schedule overrides
- [ ] Machine learning for issue prioritization
- [ ] Integration with CI/CD pipelines
- [ ] Automatic rollback on failed fixes
