# Doppler Secrets Management Guide

> **Status:** Production (as of January 2026)  
> **Scope:** 8 projects migrated, ecosystem-wide standard

---

## 🎯 Overview

**Doppler** is the centralized secrets management system for the ecosystem. It replaces local `.env` files with cloud-based secret storage.

This is a core component of our safety stack, as documented in the [[trustworthy_ai_report]].

---

## 🚀 How to Use Doppler

Instead of relying on a local `.env` file, prefix your commands with `doppler run --`.

For new projects started via the [[PROJECT_KICKOFF_GUIDE]], add Doppler from the start.

---

## 📝 Best Practices

### 1. Never Commit `.env` Files

Always ensure your `.gitignore` follows the [[PROJECT_STRUCTURE_STANDARDS]] to exclude environment files.

```gitignore
.env
.env.*
!.env.example
```

---
*See also: [[CODE_QUALITY_STANDARDS]] for security rules and [[LOCAL_MODEL_LEARNINGS]] for troubleshooting Doppler-related AI behavior.*

## Related Documentation

- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[case_studies]] - examples
- [[security_patterns]] - security
