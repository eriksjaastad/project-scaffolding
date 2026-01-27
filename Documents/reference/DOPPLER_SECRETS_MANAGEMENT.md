# Doppler Secrets Management Guide

> **Status:** 10/10 projects (FREE TIER FULL - Jan 2026)
> **New projects:** Must use local `.env` files

---

## ⚠️ Doppler at Capacity

The free tier limit (10 projects) has been reached. **New projects cannot use Doppler.**

For new projects:
- Use local `.env` files with `python-dotenv`
- Load secrets via `load_dotenv()` at script entry

---

## 🎯 Overview

**Doppler** is used for secrets management in 10 legacy projects. It provides cloud-based secret storage with CLI injection.

---

## ✅ Projects Using Doppler (10)

| Project | Configs |
|---------|---------|
| `3d-pose-factory` | 6 |
| `ai-usage-billing-tracker` | 4 |
| `analyze-youtube-videos` | 4 |
| `cortana-personal-ai` | 4 |
| `holoscape` | 5 |
| `hypocrisynow` | 4 |
| `muffinpanrecipes` | 4 |
| `project-scaffolding` | 4 |
| `smart-invoice-workflow` | 4 |
| `trading-copilot` | 4 |

---

## 🚀 Using Doppler (Legacy Projects Only)

For projects already in Doppler, prefix commands with `doppler run --`:

```bash
cd project-name
doppler run -- python script.py
```

### Common Commands

```bash
doppler secrets              # View all secrets
doppler secrets set KEY=val  # Update a secret
doppler setup                # Check/configure project
```

---

## 📝 New Projects: Use .env

```python
# At top of script
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
```

### .gitignore

```gitignore
.env
.env.*
!.env.example
```

---

## 🔄 Rollback (If Needed)

All Doppler projects have `.env.doppler-backup` files:

```bash
mv .env.doppler-backup .env
```

---

## Related Documentation

- [Safety Systems](../patterns/safety-systems.md) - security
- [CODE_QUALITY_STANDARDS](../CODE_QUALITY_STANDARDS.md) - security rules
