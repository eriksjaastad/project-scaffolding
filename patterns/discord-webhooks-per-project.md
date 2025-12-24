# Discord Webhooks: One Channel Per Project

**Pattern:** Create dedicated Discord channels for each project's notifications

**Status:** ✅ Proven (Trading Co-Pilot, Dec 2024)

**Category:** Notification Architecture

---

## The Problem

When multiple projects send notifications to a single Discord channel:
- 🚫 Channel becomes overwhelming and noisy
- 🚫 Hard to tell which notification came from which project
- 🚫 Can't mute one project without muting everything
- 🚫 Debugging is confusing (which error belongs to what?)
- 🚫 Can't set different notification rules per project

**Real example:** Trading Co-Pilot sends 4+ messages per day (morning briefing, model predictions, reviews). If image-workflow, Cortana, and other projects also sent to the same channel, it would be chaos.

---

## The Solution

**Create one Discord channel per project/context:**

```
Discord Server: Erik's Projects
├── #trading-copilot (webhook: Captain Hook)
├── #image-workflow (webhook: Image Bot)
├── #cortana (webhook: Cortana)
├── #hypocrisy-now (webhook: Hypocrisy Bot)
└── #general (personal use, no webhooks)
```

**Each project gets:**
- Its own dedicated channel
- Its own named webhook (makes it obvious in logs)
- Its own notification settings
- Clean separation of concerns

---

## Implementation

### 1. Create Discord Channel

In your Discord server:
1. Create new channel: `#project-name`
2. Set channel topic: "Automated notifications from [project-name]"
3. Mute if needed (you can always check history)

### 2. Create Webhook

1. Right-click channel → Edit Channel → Integrations
2. Create Webhook
3. Name it something recognizable (e.g., "Captain Hook", "Image Bot")
4. Copy webhook URL

### 3. Store in Project .env

```bash
# In project-name/.env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/[webhook-id]/[token]
```

### 4. Document in EXTERNAL_RESOURCES.md

Add to your project-scaffolding/EXTERNAL_RESOURCES.md:

```markdown
#### Discord Webhooks
- **Projects:** [List all projects using Discord]
- **Cost:** Free
- **Pattern:** One channel per project
- **Channels:**
  - #trading-copilot → Trading Projects
  - #image-workflow → image-workflow
  - etc.
```

---

## Benefits

### For Daily Use
✅ **Focused attention:** Only see notifications you care about  
✅ **Easy muting:** Mute verbose projects without missing critical ones  
✅ **Clear attribution:** Know instantly which project sent what  
✅ **Better mobile experience:** Can customize notifications per channel

### For Debugging
✅ **Easier troubleshooting:** Error messages clearly tied to specific project  
✅ **Better logging:** Search channel for project-specific history  
✅ **No cross-contamination:** One project's spam doesn't hide another's errors

### For Collaboration
✅ **Selective sharing:** Share #trading-copilot with trading partner without exposing everything  
✅ **Granular permissions:** Different access levels per channel  
✅ **Professional presentation:** Each project has its own clean feed

---

## Real-World Example: Trading Co-Pilot

**Channel:** `#trading-copilot`  
**Webhook Name:** Captain Hook ⚓  
**Notifications:**
- 7:55 AM ET - Morning Briefing
- 8:00 AM, 10:00 AM, 2:00 PM, 4:00 PM - Model Arena predictions
- Monday 7:00 AM - Weekly Preview
- Friday 5:00 PM - Weekly Review
- Last day of month 6:00 PM - Monthly Review
- Daily 5:30 PM - Health Check
- Any time - Error alerts (🚨 LOUD failures)

**Why dedicated channel works:**
- Can mute during work hours, check at end of day
- Error alerts still break through (🚨 emoji catches attention)
- Clean history for reviewing past predictions
- No confusion with other project notifications

---

## Anti-Pattern: Shared Channel

❌ **Don't do this:**
```
All projects → #general or #notifications
```

**Why it fails:**
- Within a week, 100+ messages per day
- Can't tell what's important
- Miss critical errors in the noise
- Eventually stop checking entirely
- Defeats the purpose of notifications

---

## Naming Convention

**Channel names:** Use project names directly
- ✅ `#trading-copilot`
- ✅ `#image-workflow`
- ✅ `#cortana`
- ❌ `#notifications-1`, `#bot-stuff` (not descriptive)

**Webhook names:** Use personality/theme
- ✅ "Captain Hook" (trading = nautical theme)
- ✅ "Image Bot" (descriptive)
- ✅ "Cortana" (matches project)
- ❌ "Webhook 1", "Bot" (generic)

---

## Scaling

**When you have 5+ projects:**

Consider organizing with categories:
```
📊 DATA PROJECTS
├── #trading-copilot
└── #market-analysis

🎨 CREATIVE PROJECTS
├── #image-workflow
└── #3d-pose-factory

🤖 AI ASSISTANTS
├── #cortana
└── #agent-os

🌐 WEB PROJECTS
└── #hypocrisy-now
```

Still one channel per project, just organized better.

---

## Cost

**Discord:** Free, unlimited webhooks  
**Time to set up:** 2 minutes per project  
**Maintenance:** None (webhooks don't expire)

**ROI:** Immediately better organization, scales indefinitely

---

## Related Patterns

- **API Key Management:** Each project gets its own keys → each project gets its own webhook
- **Failure Isolation:** One project's errors don't spam other projects' channels
- **Observable Systems:** Notifications are only useful if you can find them later

---

## Implementation Checklist

When setting up a new project:

- [ ] Create Discord channel: `#project-name`
- [ ] Create webhook with descriptive name
- [ ] Add `DISCORD_WEBHOOK_URL` to project `.env`
- [ ] Add to `.env.example` with placeholder
- [ ] Document in project README (how to get notifications)
- [ ] Add to EXTERNAL_RESOURCES.md
- [ ] Test with a "Hello from [project]" message
- [ ] Configure notification settings (mute if needed)

---

## When NOT to Use This Pattern

**Use a shared channel if:**
- Personal project with 1-2 notifications per week
- Testing/prototyping (not worth creating channel yet)
- Notifications are truly cross-project (shared monitoring)

**But:** When in doubt, create dedicated channel. Easy to delete later, hard to untangle later.

---

## Example Code

**Test your webhook:**
```python
import json
import urllib.request

DISCORD_WEBHOOK_URL = "your-webhook-url"

def send_test_message():
    message = {
        "content": "🎉 **[Project Name] is now connected!**\n\nYou'll receive notifications in this channel."
    }
    
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=json.dumps(message).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    urllib.request.urlopen(req, timeout=10)
    print("✅ Test message sent!")

send_test_message()
```

---

**Pattern discovered:** December 24, 2024  
**First implementation:** Trading Co-Pilot (#trading-copilot channel)  
**Contributed by:** Erik (user insight) + Claude (documentation)  

---

*"One project, one channel, zero chaos."*

