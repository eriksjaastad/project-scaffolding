# Doppler Secrets Management Guide

> **Status:** Production (as of January 2026)  
> **Scope:** 8 projects migrated, ecosystem-wide standard

---

## 🎯 Overview

**Doppler** is the centralized secrets management system for the eriksjaastad project ecosystem. It replaces local `.env` files with cloud-based secret storage, providing:

- ✅ **Centralized Management**: All secrets in one secure dashboard
- ✅ **Version History**: Track changes to environment variables over time
- ✅ **Audit Logs**: See who accessed what and when
- ✅ **Team Collaboration**: Share secrets securely (if needed)
- ✅ **Zero Git Risk**: Secrets never touch `.env` files that could be committed
- ✅ **Multi-Environment Support**: dev/staging/prod configs per project

---

## 📊 Migration Status

### ✅ Migrated Projects (8 total)

All projects below are **fully operational** with Doppler and have backup `.env.doppler-backup` files:

| Project | Doppler Project ID | Key Secrets | Status |
|---------|-------------------|-------------|---------|
| `ai-usage-billing-tracker` | `ai-usage-billing-tracker` | DB_*, OPENAI_API_KEY, ANTHROPIC_API_KEY | ✅ Active |
| `analyze-youtube-videos` | `analyze-youtube-videos` | OLLAMA_MODEL, LIBRARY_DIR, SKILLS_LIBRARY_PATH | ✅ Active |
| `cortana-personal-ai` | `cortana-personal-ai` | OPENAI_API_KEY, DISCORD_WEBHOOK_URL | ✅ Active |
| `hypocrisynow` | `hypocrisynow` | DATABASE_URL, OPENAI_API_KEY, ADMIN_API_KEY | ✅ Active |
| `muffinpanrecipes` | `muffinpanrecipes` | STABILITY_API_KEY | ✅ Active |
| `project-scaffolding` | `project-scaffolding` | PROJECTS_ROOT, OLLAMA_MODEL, *_API_KEY (scaffolding templates) | ✅ Active |
| `smart-invoice-workflow` | `smart-invoice-workflow` | GOOGLE_SHEETS_*, GMAIL_SENDER, DRY_RUN | ✅ Active |
| `trading-copilot` | `trading-copilot` | DATABASE_URL, OPENAI_API_KEY, FINNHUB_API_KEY, GOOGLE_API_KEY, XAI_API_KEY | ✅ Active |

**Migration Date:** January 14, 2026  
**Doppler Workplace:** "Locol projects" (Erik's account)  
**Security Status:** ✅ All `.env` files removed, `.gitignore` updated, safe to commit

### ⚠️ Projects with Nested `.env` Files (Not Yet Migrated)

These projects require manual investigation before migration:

| Project | Issue | Action Required |
|---------|-------|-----------------|
| `holoscape` | 2 `.env` files (root + `agents/social-media/`) | Investigate architecture: Are these separate services or environments? |
| `3d-pose-factory` | 2 `.env` files (`shared/` + `dashboard/`) | Investigate structure: Why nested? Microservices? |

**Do NOT migrate these until architecture is understood.**

---

## 🚀 How to Use Doppler

### For Migrated Projects

Instead of relying on a local `.env` file, prefix your commands with `doppler run --`:

#### Before Doppler:
```bash
cd [USER_HOME]/projects/trading-copilot
doppler run -- python3 scripts/main.py
```

#### After Doppler:
```bash
cd [USER_HOME]/projects/trading-copilot
doppler run -- python3 scripts/main.py
```

**What happens:**
1. Doppler CLI reads the local `.doppler` config file (created during setup)
2. Fetches secrets from the cloud for that project + config (e.g., `trading-copilot` + `dev`)
3. Injects them as environment variables
4. Runs your command with those variables

### For New Projects

When creating a new project, add Doppler from the start:

```bash
# 1. Create the Doppler project
doppler projects create my-new-project

# 2. Add secrets manually via dashboard or CLI
doppler secrets set DATABASE_URL="postgresql://..." --project my-new-project --config dev

# 3. Initialize the local directory
cd [USER_HOME]/projects/my-new-project
doppler setup --project my-new-project --config dev --no-interactive

# 4. Run your app
doppler run -- python3 main.py
```

**Recommended:** Still create a `.env.example` file with dummy values for documentation purposes, but never commit real secrets.

---

## 🔧 Common Operations

### View Secrets for a Project

```bash
cd [USER_HOME]/projects/trading-copilot
doppler secrets
```

This displays all environment variables for the current project.

### Update a Secret

```bash
doppler secrets set OPENAI_API_KEY="sk-new-key-here" --project trading-copilot --config dev
```

Changes take effect immediately. No need to restart your app - just rerun `doppler run --`.

### Add a New Secret

```bash
doppler secrets set NEW_SERVICE_KEY="abc123" --project trading-copilot --config dev
```

### Delete a Secret

```bash
doppler secrets delete OLD_KEY --project trading-copilot --config dev
```

### Check Which Project You're In

```bash
doppler setup
```

Shows the current project and config for the current directory.

---

## 🛡️ Rollback Procedures

If Doppler breaks or you need to return to `.env` files:

### Per-Project Rollback

```bash
cd [USER_HOME]/projects/trading-copilot
mv .env.doppler-backup .env
```

Your project will work as it did before Doppler.

### Full Ecosystem Rollback (Nuclear Option)

If you need to rollback ALL projects at once:

```bash
cd [USER_HOME]/projects
for project in ai-usage-billing-tracker analyze-youtube-videos cortana-personal-ai hypocrisynow muffinpanrecipes project-scaffolding smart-invoice-workflow trading-copilot; do
    cd "$project"
    if [ -f .env.doppler-backup ]; then
        mv .env.doppler-backup .env
        echo "✅ Rolled back $project"
    fi
    cd ..
done
```

**Important:** Rollback does NOT delete secrets from Doppler. They remain in the cloud dashboard as a backup.

---

## 📝 Best Practices

### 1. Never Commit `.env` Files

Add to `.gitignore`:
```gitignore
.env
.env.*
!.env.example
```bash

The `!.env.example` line allows you to commit a template with dummy values.

### 2. Use `.env.example` for Documentation

Create a template file that shows what variables are needed (without real values):

```bash
# .env.example
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=sk-...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```bash

Commit this to Git as documentation.

### 3. Backup Files Deleted (Security First)

**Status:** All `.env.doppler-backup` files have been deleted as of January 14, 2026.

**Why:** These files contained real API keys and posed a Git commit risk. After verifying all 79 secrets were safely in Doppler, we deleted the backups.

**Safety Net:** All secrets remain in Doppler cloud (accessible via dashboard at https://dashboard.doppler.com).

### 4. Use `dev` Config for Local Development

Doppler supports multiple configs per project (dev/staging/prod). For solo development, stick with `dev` for simplicity.

If you ever deploy to production, create a separate `prod` config with production secrets.

### 5. Check Secrets Before Running Critical Operations

For high-stakes operations (database migrations, production deployments), verify secrets first:

```bash
doppler secrets | grep DATABASE_URL
```bash

### 6. Offline Considerations

**Doppler requires internet** to fetch secrets. However:
- Secrets are cached locally for ~24 hours
- If you need to work offline, keep `.env.doppler-backup` files as fallback

**Reality Check:** You use AI coding assistants (Cursor, Claude), which require internet anyway. This is not a blocker.

---

## 🔐 Security Improvements

Compared to `.env` files, Doppler provides:

### 1. No Accidental Commits
`.env` files can be accidentally committed to Git. Doppler secrets never touch disk (except in memory during `doppler run`).

### 2. Audit Trail
See who accessed secrets and when via Doppler dashboard.

### 3. Secret Rotation
Update a compromised API key in Doppler once, and all team members (or just you) get the new value automatically.

### 4. Remote Revocation
If a secret is leaked, you can delete it from Doppler immediately - no need to check every machine.

### 5. Encryption at Rest
Doppler encrypts secrets in their cloud storage (AES-256).

---

## 🧪 Testing & Verification

### Test Doppler is Working

```bash
cd [USER_HOME]/projects/trading-copilot
doppler run -- python3 -c "import os; print('DATABASE_URL:', os.getenv('DATABASE_URL')[:30])"
```bash

Expected output: `DATABASE_URL: postgresql://postgres:...`

If you see `None`, Doppler is not injecting secrets correctly.

### Debug Steps

1. **Check setup:**
   ```bash
   doppler setup
   ```bash
   Verify project and config are correct.

2. **Check authentication:**
   ```bash
   doppler whoami
   ```bash
   Verify you're logged in.

3. **Check secrets exist:**
   ```bash
   doppler secrets
   ```bash
   Verify the secrets are uploaded.

4. **Check `.doppler` directory:**
   ```bash
   ls -la .doppler
   cat .doppler/.doppler.yaml
   ```bash
   Verify config file exists and has correct project/config.

---

## 📚 Resources

### Official Doppler Documentation
- [Doppler CLI Reference](https://docs.doppler.com/docs/cli)
- [Doppler Guides](https://docs.doppler.com/docs/guides)
- [Doppler Dashboard](https://dashboard.doppler.com)

### Internal Documentation
- **Migration Plan:** `[USER_HOME]/projects/DOPPLER_MIGRATION_PLAN.md` (detailed timeline and steps)
- **Root Governance:** `[USER_HOME]/projects/.cursorrules` (see `.env` rules)
- **Security Standards:** `[USER_HOME]/projects/project-scaffolding/Documents/CODE_QUALITY_STANDARDS.md`

### Quick Reference Commands

```bash
# Install
brew install dopplerhq/cli/doppler

# Login
doppler login

# Check status
doppler whoami
doppler setup

# View secrets
doppler secrets

# Run a command
doppler run -- your-command

# Update a secret
doppler secrets set KEY="value"
```bash

---

## 🚨 Troubleshooting

### Problem: "exec: command not found in $PATH"

**Cause:** Doppler doesn't know where your Python/Node/etc. is.

**Solution:** Use full paths or activate your virtualenv first:
```bash
# Option 1: Full path
doppler run -- /usr/local/bin/python3 script.py

# Option 2: Activate venv first
source venv/bin/activate
doppler run -- python script.py
```bash

### Problem: "No project or config set for this directory"

**Cause:** You didn't run `doppler setup` in this directory.

**Solution:**
```bash
doppler setup --project your-project --config dev --no-interactive
```bash

### Problem: "Rate limit exceeded" or "API error"

**Cause:** Too many rapid API calls or Doppler service issue.

**Solution:**
1. Wait 1 minute and retry
2. Check [Doppler Status Page](https://status.doppler.com)
3. If persistent, rollback to `.env.doppler-backup`

### Problem: "I updated a secret but my app still uses the old value"

**Cause:** Your app cached the environment variable on startup.

**Solution:** Restart your app. Secrets are injected at process start, not live-updated.

---

## 📅 Maintenance

### Monthly Tasks

1. **Review secrets inventory:**
   - Delete unused secrets (old API keys, deprecated services)
   - Update secrets that are approaching expiration (if applicable)

2. **Check for unused projects:**
   ```bash
   doppler projects
   ```bash
   Archive projects that are no longer active.

3. **Verify backups:**
   - Ensure `.env.doppler-backup` files still exist (until you're confident Doppler is stable)

### After 60 Days (Post-Migration)

If all 8 projects have been working flawlessly with Doppler:
1. Consider deleting `.env.doppler-backup` files (keep at least one as a reference)
2. Update project READMEs to document Doppler usage
3. Add Doppler to `project-scaffolding` templates for new projects

---

## 🔮 Future Enhancements

### For Team Collaboration (If Needed)

If you ever add a collaborator (human or AI agent):
1. Invite them to your Doppler workplace
2. Assign role-based permissions (read-only, admin, etc.)
3. They run `doppler login` and get access to secrets automatically

No more "can you send me the `.env` file?" emails.

### Multi-Environment Configs

For projects that deploy to staging/production:
```bash
# Create prod config
doppler configs create prod --project trading-copilot

# Set production secrets
doppler secrets set DATABASE_URL="prod-url" --config prod

# Deploy to production
doppler run --config prod -- deploy-script.sh
```bash

### CI/CD Integration

For automated deployments, generate a service token:
```bash
doppler configs tokens create prod-deploy --config prod
```bash

Add that token to your CI/CD environment (GitHub Actions, Railway, etc.).

---

## 📞 Support

**Questions or issues?**
1. Check this document first
2. Check `[USER_HOME]/projects/DOPPLER_MIGRATION_PLAN.md` for detailed migration notes
3. Check Doppler docs: https://docs.doppler.com

**Emergency rollback?**
```bash
cd [USER_HOME]/projects/{project-name}
mv .env.doppler-backup .env
```

---

*Last Updated: January 2026*  
*Part of the eriksjaastad project ecosystem.*
