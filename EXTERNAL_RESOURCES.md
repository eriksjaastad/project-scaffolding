# External Resources & Services

> **Purpose:** Track which external services, APIs, and resources are used across all projects  
> **Last Updated:** December 21, 2025

**Why this exists:** When you get a bill or notification, you need to know which project uses that service.

**Prevents two problems:**
1. 🚫 **Duplicate services** - Signing up for something that does what we already have
2. 🚫 **Orphaned accounts** - Forgetting we signed up for something

---

## Before Adding a New Service

**STOP and check this file first!**

Ask yourself:
1. **Do we already have something that does this?** (See "Services by Function" below)
2. **Have we tried this before and rejected it?** (See "Rejected/Unused Services" below)
3. **Which project needs this?** (Document it immediately)
4. **What's the cost?** (Know before you commit)
5. **Can we use an existing service instead?** (Avoid proliferation)

---

## Services by Function

> **Purpose:** Prevent signing up for duplicate services

### AI/LLM APIs
**What we have:**
- OpenAI (GPT-4o, 4o-mini, o1)
- Anthropic (Claude Opus 4, Sonnet 4, Haiku 3.5)
- Google AI (Gemini 2.0/2.5 Flash)
- xAI (Grok-3)

**Before adding another LLM:** Do we really need it, or can we use one of these?

---

### Cloud Hosting/Deployment
**What we have:**
- Railway (Python cron jobs + Postgres)
- Cloudflare R2 (S3-compatible storage for 3D Pose Factory)

**Before adding Heroku/Vercel/Netlify/etc:** Can Railway handle it?  
**Before adding S3/B2/etc:** We already have R2.

---

### Cloud Storage/Backup
**What we have:**
- rclone (tool that connects to storage)
- Cloudflare R2 (via rclone for 3D Pose Factory)
- Google Drive (via rclone for image-workflow backups)

**Before adding Dropbox/Box/etc:** We have R2 and Drive.

---

### Databases
**What we have:**
- PostgreSQL (Railway)
- SQLite (local, multiple projects)

**Before adding MySQL/MongoDB/etc:** Can Postgres handle it?

---

### Monitoring/Notifications
**What we have:**
- Discord Webhooks (free, unlimited)

**Before adding Slack/Telegram/etc:** Discord already works.

---

### Voice-to-Text
**What we have:**
- SuperWhisper (local, one-time purchase)
- Wispr Flow (local, one-time purchase)

**Before adding Otter/Rev/etc:** These already work.

---

## Rejected/Unused Services

> **Purpose:** Don't re-sign up for things we already tried and didn't use

### Never Used (Forgot About)

| Service | Date Added | Why Added | Why Not Using | Status |
|---------|-----------|-----------|---------------|--------|
| *Add entries when you find orphaned accounts* | | | | |

**TODO when found:**
- Document why we signed up
- Document why we stopped using it
- Cancel account if no longer needed
- Move to "Cancelled" section below

---

### Tried and Rejected

| Service | Date Tried | Why Tried | Why Rejected | Alternative Used |
|---------|-----------|-----------|--------------|------------------|
| *Add entries when evaluating alternatives* | | | | |

**Example entries when they happen:**
- Service X: Tried for Y, too expensive, using Z instead
- Service A: Evaluated for B, missing feature C, stuck with D

---

### Cancelled Accounts

| Service | Date Cancelled | Reason | Data Migrated To |
|---------|---------------|--------|------------------|
| *Add entries when cancelling* | | | |

**Keep this history to prevent re-signing up!**

---

## Quick Reference

| Service | Projects Using It | Cost | Status |
|---------|------------------|------|--------|
| Railway | Trading Projects | ~$5/mo | Active |
| OpenAI API | Trading, Cortana, image-workflow | ~$15/mo total | Active |
| Anthropic API | Trading | ~$2/mo | Active |
| Google AI (Gemini) | Trading | ~$1/mo | Active |
| xAI (Grok) | Trading | Pay-per-use | Active |
| Cloudflare R2 | 3D Pose Factory | $3-10/mo (storage) | Active |
| rclone | 3D Pose Factory, image-workflow | Free (tool) | Active |
| Postgres (Railway) | Trading | Included in Railway | Active |
| Discord Webhooks | Trading | Free | Active |
| SuperWhisper | Cortana | One-time purchase | Active |
| Google Drive | image-workflow | Free (personal storage) | Active |

---

## Detailed Breakdown

### Cloud Infrastructure

#### Railway.app
- **Projects:** Trading Projects (Model Arena)
- **Cost:** ~$5/month (Hobby plan)
- **Purpose:** Hosting Python cron jobs + PostgreSQL
- **Credentials:** `.env` in Trading Projects
- **Dashboard:** https://railway.app
- **Notes:** Runs 4x daily + weekly/monthly jobs

#### Cloudflare R2
- **Projects:** 3D Pose Factory
- **Cost:** $3-10/month (based on storage usage)
- **Purpose:** S3-compatible object storage for pose outputs
- **Bucket:** `pose-factory`
- **Dashboard:** https://dash.cloudflare.com/
- **Integration:** Via rclone (S3-compatible)
- **Architecture:** RunPod (GPU) → R2 (storage) ↔ Local Mac (download)
- **Why R2:** No egress fees, extremely cheap storage (~$0.015/GB/month)
- **Notes:** 
  - Configured via rclone on both RunPod and local Mac
  - Stores generated 3D pose outputs, skeletons, depth maps
  - Used with: `rclone sync r2_pose_factory:pose-factory/output local_path`

**Action needed:** ~~Check these projects for Cloudflare~~ ✅ **IDENTIFIED: 3D Pose Factory**

---

### Sync & Backup Tools

#### rclone
- **Projects:** 3D Pose Factory, image-workflow
- **Cost:** Free (open source tool)
- **Purpose:** Sync files to/from cloud storage
- **Current backends:** 
  - **Cloudflare R2** (3D Pose Factory: `r2_pose_factory` remote)
  - **Google Drive** (image-workflow: `gbackup` remote)
- **Installation:** Via homebrew: `brew install rclone`
- **Config location:** `~/.config/rclone/rclone.conf`

**Usage in 3D Pose Factory:**
- RunPod → R2: Upload pose outputs
- R2 → Local Mac: Download for ComfyUI
- Bucket: `pose-factory`

**Usage in image-workflow:**
- Daily backups: Local → Google Drive
- Weekly rollups: Compressed archives
- Remote: `gbackup` (scoped to specific folder)
- Schedule: Daily at 2:10 AM (via cron)

**Notes:** 
- Two completely different use cases (active storage vs backup)
- S3-compatible protocol for R2
- Google Drive API for Drive

---

### AI APIs

#### OpenAI
- **Projects:** 
  - Trading Projects (GPT-4o, GPT-4o-mini, o1)
  - Cortana Personal AI (gpt-4o-mini)
  - image-workflow (AI training, quality filtering)
- **Cost:** ~$15/month combined
  - Trading: ~$4/month
  - Cortana: ~$0.60/month
  - image-workflow: Variable (batch processing)
- **Key location:** 
  - Trading: `.env`
  - Cortana: Uses agent_os `.env`
  - image-workflow: Local `.env`
- **Dashboard:** https://platform.openai.com

#### Anthropic (Claude)
- **Projects:** Trading Projects (Opus 4, Sonnet 4, Haiku 3.5)
- **Cost:** ~$2/month
- **Key location:** Trading Projects `.env`
- **Dashboard:** https://console.anthropic.com

#### Google AI (Gemini)
- **Projects:** Trading Projects (Gemini 2.0/2.5 Flash)
- **Cost:** ~$1/month
- **Key location:** Trading Projects `.env`
- **Dashboard:** https://ai.google.dev

#### xAI (Grok)
- **Projects:** Trading Projects (Grok-3)
- **Cost:** Pay-per-use (~$0.50/month)
- **Key location:** Trading Projects `.env`
- **Dashboard:** https://x.ai

---

### Databases

#### PostgreSQL (Railway)
- **Projects:** Trading Projects
- **Cost:** Included in Railway subscription
- **Purpose:** Model Arena data (runs, predictions, snapshots)
- **Access:** Via Railway dashboard or connection string
- **Backup:** Automatic (Railway)

#### SQLite
- **Projects:** 
  - Cortana (reads SuperWhisper DB, Wispr Flow DB)
  - image-workflow (local data)
  - agent_os (local data)
- **Cost:** Free (local files)
- **Purpose:** Local data storage
- **Backup:** Manual file copies

---

### Notification Services

#### Discord Webhooks
- **Projects:** Trading Projects
- **Cost:** Free
- **Purpose:** Daily trading briefings, model predictions
- **Webhook URLs:** In Trading Projects `.env`
- **Notes:** 4x daily + weekly/monthly reports

---

### Local Services

#### SuperWhisper
- **Projects:** Cortana Personal AI
- **Cost:** One-time purchase (~$30?)
- **Purpose:** Voice-to-text, main data source
- **Database location:** `~/Library/Application Support/superwhisper/database/`
- **Access:** Read-only from Cortana scripts

#### Wispr Flow
- **Projects:** Cortana Personal AI
- **Cost:** One-time purchase
- **Purpose:** Voice dictation into apps
- **Database location:** `~/Library/Application Support/Wispr Flow/flow.sqlite`
- **Access:** Read-only from Cortana scripts

#### Google Drive
- **Projects:** image-workflow
- **Cost:** Free (using personal storage allocation)
- **Purpose:** Offsite backups of project data
- **Integration:** Via rclone (`gbackup` remote)
- **Scope:** Restricted to single dedicated backup folder
- **Usage:**
  - Daily backups: `~/project-data-archives/image-workflow/YYYY-MM-DD/`
  - Weekly rollups: Compressed archives
  - Automated via cron (2:10 AM daily)
- **Scripts:**
  - `scripts/backup/daily_backup.py`
  - `scripts/backup/weekly_rollup.py`

---

## Resources by Project

### Trading Projects
- ✅ Railway (hosting + Postgres)
- ✅ OpenAI API (GPT-4o, 4o-mini, o1)
- ✅ Anthropic API (Claude Opus 4, Sonnet 4, Haiku 3.5)
- ✅ Google AI (Gemini 2.0/2.5 Flash)
- ✅ xAI (Grok-3)
- ✅ Discord Webhooks

**Monthly cost:** ~$12

---

### Cortana Personal AI
- ✅ OpenAI API (gpt-4o-mini)
- ✅ SuperWhisper (local, one-time)
- ✅ Wispr Flow (local, one-time)
- ✅ Uses agent_os `.env` for API keys

**Monthly cost:** ~$0.60

---

### image-workflow
- ✅ OpenAI API (batch processing)
- ✅ SQLite (local)
- ✅ rclone (backup tool)
- ✅ Google Drive (via rclone for offsite backups)

**Monthly cost:** Variable (~$5-20 depending on usage) + $0 (Drive uses personal storage)

---

### agent_os
- ⚠️ Provides `.env` for other projects
- ✅ SQLite (local)
- ⚠️ May have its own API usage (check plugins)

**Monthly cost:** TBD

---

### 3D Pose Factory
- ✅ Cloudflare R2 (S3-compatible storage)
- ✅ rclone (sync tool)
- ✅ RunPod (GPU compute - document separately?)

**Monthly cost:** $3-10 (R2 storage) + GPU costs (burst usage)

---

### Hypocrisy Now
- ⚠️ **NEEDS AUDIT**
- Likely using:
  - RSS feed services
  - Storage/hosting?
  - Check for Cloudflare here

**Monthly cost:** Unknown

---

### Hologram
- ⚠️ **NEEDS AUDIT**
- Web client - might use:
  - Hosting service
  - CDN (Cloudflare?)
  - Check here for Cloudflare

**Monthly cost:** Unknown

---

## Action Items

### Immediate
- [x] ~~**Find where Cloudflare is used**~~ ✅ **FOUND: 3D Pose Factory (R2 storage)**
  - Bucket: `pose-factory`
  - Purpose: Store pose outputs from RunPod
  - Integration: rclone (S3-compatible)

- [x] ~~**Find where rclone is used (other projects)**~~ ✅ **FOUND: Both projects identified**
  - [x] 3D Pose Factory ✅ Confirmed (Cloudflare R2 sync)
  - [x] image-workflow ✅ Confirmed (Google Drive backups)
  - [x] Checked `~/.config/rclone/rclone.conf` - 2 remotes total

- [ ] **Audit for orphaned accounts**
  - Check email for service notifications we don't recognize
  - Review credit card statements for recurring charges
  - Check password manager for unused logins
  - Move orphaned accounts to "Never Used" section

### This Week
- [ ] Audit 3D Pose Factory resources
- [ ] Audit Hypocrisy Now resources
- [ ] Audit Hologram resources
- [ ] Audit agent_os plugin resource usage

### Ongoing
- [ ] Update this file when adding new services
- [ ] Monthly cost review (end of each month)
- [ ] Clean up unused accounts
- [ ] Document credential locations

---

## Cost Summary

| Category | Monthly Cost |
|----------|-------------|
| **Infrastructure** | $5 (Railway) |
| **AI APIs** | $15-20 (variable) |
| **Total Known** | **$20-25/month** |
| **Unknown** | TBD (need audits) |

---

## Credential Security

### Where API Keys Live

1. **Trading Projects:** `.env` file (not committed)
2. **Cortana:** Uses `../agent_os/.env`
3. **image-workflow:** Local `.env` file
4. **agent_os:** Master `.env` file (shared)

### Security Notes

- ✅ All `.env` files in `.gitignore`
- ✅ Never committed to git
- ⚠️ Consider password manager for backup
- ⚠️ Consider key rotation policy (every 6-12 months?)

---

## Service Health Check

**Last checked:** December 21, 2025

| Service | Status | Last Verified |
|---------|--------|--------------|
| Railway | ✅ Active | Dec 21, 2025 |
| OpenAI | ✅ Active | Dec 21, 2025 |
| Anthropic | ✅ Active | Dec 21, 2025 |
| Google AI | ✅ Active | Dec 21, 2025 |
| Discord | ✅ Active | Dec 21, 2025 |
| Cloudflare | ✅ Active | Dec 21, 2025 - Found: 3D Pose Factory (R2) |

---

## When You Get a Bill/Notification

1. **Check this file** - See which project uses the service
2. **Update cost if changed** - Keep cost estimates current
3. **Verify still needed** - Cancel if not being used
4. **Document any issues** - Add notes section

---

## Adding New Services

When adding a new external service:

1. **Check "Services by Function"** - Do we already have this capability?
2. **Check "Rejected/Unused Services"** - Have we tried this before?
3. Add to "Quick Reference" table
4. Add to "Detailed Breakdown" section
5. Add to relevant project section
6. Add to "Services by Function" category
7. Update cost summary
8. Document credential location
9. Update this file's "Last Updated" date

**Never add a service without documenting it here IMMEDIATELY.**

---

## Cleanup Checklist

**Review quarterly:**

- [ ] Are all listed services still in use?
- [ ] Are costs still accurate?
- [ ] Are there services we've added but forgot to document?
- [ ] Can we consolidate any services?
- [ ] Are credentials still valid?
- [ ] **Any orphaned accounts to cancel?**
- [ ] **Any duplicate functionality we can eliminate?**
- [ ] Check email for service notifications from unknown services
- [ ] Review credit card for unexpected recurring charges

---

## Emergency Audit: "What Am I Paying For?"

**Run this when you get a bill you don't recognize:**

1. **Check this file** - Is the service listed in Quick Reference?
2. **Search all projects** - grep for service name across codebase:
   ```bash
   grep -ri "service-name" /Users/eriksjaastad/projects/
   grep -ri "service-name" ~/.config/
   ```
3. **Check .env files** - Look for API keys:
   ```bash
   grep -r "SERVICE_" /Users/eriksjaastad/projects/*/\.env 2>/dev/null
   ```
4. **Document immediately** - Once found, update this file

**Then decide:**
- Still using it? → Update this file with correct info
- Not using it? → Cancel and add to "Cancelled Accounts"
- Forgot about it? → Add to "Never Used" section, then cancel

---

*This file prevents "I got a bill but don't know which project" situations.*

**Next update:** When new services are added

**Recent discoveries:**
- Dec 21, 2025: Found Cloudflare R2 usage in 3D Pose Factory (mystery solved!)
- Dec 21, 2025: Found rclone usage in both 3D Pose Factory (R2) and image-workflow (Google Drive backups)

