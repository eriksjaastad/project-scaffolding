# External Resources & Services

> **Purpose:** Track which external services, APIs, and resources are used across all projects  
> **Last Updated:** January 7, 2026
> **Status:** Using Decentralized .env System

**Why this exists:** When you get a bill or notification, you need to know which project uses that service.

**Prevents two problems:**
1. 🚫 **Duplicate services** - Signing up for something that does what we already have
2. 🚫 **Orphaned accounts** - Forgetting we signed up for something

---

## ⚠️ API Key Management Pattern

**CRITICAL:** Each project manages its own API keys. Never share API keys across projects.

**Standard:** `{project-name}-{service}` → `{project}/.env`
**Master Registry:** `project-scaffolding/.env` (Centralized Record)
**Template:** `../.env.project-template`

**Examples:**
- `SCAFFOLDING_DEEPSEEK_KEY` → `project-scaffolding/.env`
- `CORTANA_OPENAI_KEY` → `cortana-personal-ai/.env`
- `TRADING_OPENAI_KEY` → `trading-copilot/.env`

**Why this matters:**
- ✅ Cost attribution (which project spent what?)
- ✅ Failure isolation (one project's rate limit doesn't affect others)
- ✅ Security isolation (compromise one → others safe)
- ✅ Clear ownership (each project pays for itself)

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
- DeepSeek (V3, R1)
- Google AI (Gemini 2.0/2.5 Flash)
- xAI (Grok-3)

**Before adding another LLM:** Do we really need it, or can we use one of these?

---

### Cloud Hosting/Deployment
**What we have:**
- Railway (Python cron jobs + Postgres)
- Cloudflare R2 (S3-compatible storage for 3d-pose-factory)
- Vercel (muffinpanrecipes)

---

### Cloud Storage/Backup
**What we have:**
- rclone (tool that connects to storage)
- Cloudflare R2 (via rclone for 3d-pose-factory)
- Google Drive (via rclone for image-workflow backups)

---

### Databases
**What we have:**
- PostgreSQL (Railway)
- SQLite (local, multiple projects)

---

### Monitoring/Notifications
**What we have:**
- Discord Webhooks (free, unlimited)
- Autonomous Loops (Janitor, Librarian, Patch-Bot)

---

### Voice-to-Text
**What we have:**
- SuperWhisper (local, one-time purchase)
- Wispr Flow (local, one-time purchase)

---

## Quick Reference

| Service | Projects Using It | Env Var Name | Status |
|---------|------------------|--------------|--------|
| DeepSeek | Scaffolding | `SCAFFOLDING_DEEPSEEK_KEY` | Active |
| OpenAI | Trading, Cortana, Scaffolding | `TRADING_OPENAI_KEY`, etc. | Active |
| Anthropic | Trading, Scaffolding | `TRADING_ANTHROPIC_KEY`, etc. | Active |
| Railway | Trading | `TRADING_RAILWAY_API_KEY` | Active |
| Discord | Trading, Scaffolding | `TRADING_DISCORD_WEBHOOK_URL` | Active |
| Cloudflare R2 | 3d-pose-factory | `POSE_FACTORY_CLOUDFLARE_R2_KEY` | Active |

---

## Detailed Breakdown

### AI APIs

#### OpenAI
- **Projects:** Trading, Cortana, Scaffolding, image-workflow
- **Env Vars:** `TRADING_OPENAI_KEY`, `CORTANA_OPENAI_KEY`, `SCAFFOLDING_OPENAI_KEY`
- **Pattern:** Per-project isolation

#### DeepSeek
- **Projects:** Scaffolding (Logic/Drafting)
- **Env Var:** `SCAFFOLDING_DEEPSEEK_KEY`
- **Status:** Integrated Jan 2026

---

## Cleanup Checklist

**Review quarterly:**
- [ ] Are all listed services still in use?
- [ ] Are credentials still valid?
- [ ] **Any orphaned accounts to cancel?**
- [ ] Check email for unknown service notifications

---

## Emergency Audit: "What Am I Paying For?"

1. **Check this file** - Is the service listed?
2. **Search all projects** - grep for service name:
   ```bash
   grep -ri "service-name" ./
   ```
3. **Check .env files** - Look for project-prefixed keys:
   ```bash
   grep -r "_API_KEY" ./*/.env
   ```

---

*This file is the Source of Truth for resource mapping. See EXTERNAL_RESOURCES.yaml for automated parsing.*

## Related Documentation

- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - local AI
- [Automation Reliability](patterns/automation-reliability.md) - automation
- [Cost Management](Documents/reference/MODEL_COST_COMPARISON.md) - cost management
- [Discord Webhooks Per Project](patterns/discord-webhooks-per-project.md) - Discord
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md) - AI models
- [Safety Systems](patterns/safety-systems.md) - security
- [3d-pose-factory/README](../ai-model-scratch-build/README.md) - 3D Pose Factory
- [cortana-personal-ai/README](../ai-model-scratch-build/README.md) - Cortana AI
- [image-workflow/README](../ai-model-scratch-build/README.md) - Image Workflow
- [muffinpanrecipes/README](../ai-model-scratch-build/README.md) - Muffin Pan Recipes
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
- [trading-copilot/README](../ai-model-scratch-build/README.md) - Trading Copilot
