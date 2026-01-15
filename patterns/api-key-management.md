# API Key Management Pattern

**Status:** Proven  
**Confidence:** 🟢 High  
**Source Projects:** All projects (migration in progress)  
**Last Updated:** December 22, 2025

---

## The Pattern

**Each project manages its own API keys.** Never share API keys across projects via a centralized service.

---

## Why This Matters

### The Problem (What We're Fixing)

**Anti-pattern:** Centralized API key storage
```
agent-os/.env:
  OPENAI_API_KEY=sk-shared-key-123
  ANTHROPIC_API_KEY=sk-shared-key-456

Projects import agent-os and use shared keys
```

**Problems:**
- ❌ **Can't attribute costs** - Which project spent $50 on OpenAI?
- ❌ **Shared failure** - One project hits rate limit → all projects affected
- ❌ **Security blast radius** - Compromise agent-os → compromise all projects
- ❌ **Unclear ownership** - Who pays for the shared key?
- ❌ **No isolation** - Can't disable one project without affecting others

---

### The Solution (Per-Project Keys)

**Pattern:** Each project has its own `.env` with its own API keys

```
project-a/.env:
  OPENAI_API_KEY=sk-project-a-key

project-b/.env:
  OPENAI_API_KEY=sk-project-b-key
```

**Benefits:**
- ✅ **Cost attribution** - OpenAI dashboard shows usage per key → per project
- ✅ **Failure isolation** - project-a rate limited → project-b unaffected
- ✅ **Security isolation** - Compromise project-a → project-b safe
- ✅ **Clear ownership** - Each project pays for its own usage
- ✅ **Independent control** - Disable project-a key without affecting project-b

---

## Implementation

### Step 1: Create Project-Specific API Keys

**Naming convention:** `{project-name}-{service}`

Examples:
- `cortana-openai`
- `trading-openai`
- `image-workflow-openai`
- `billing-tracker-anthropic`

**Why this naming?** OpenAI/Anthropic dashboards show key names. Clear names = instant cost attribution.

**Where to create:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys
- Google AI: https://aistudio.google.com/app/apikey

---

### Step 2: Add to Project's `.env`

```bash
# project/.env
OPENAI_API_KEY=sk-proj-abc123...
ANTHROPIC_API_KEY=sk-ant-xyz789...
```

**Critical:** Add `.env` to `.gitignore`

```gitignore
# .gitignore
.env
.env.local
*.env
```

---

### Step 3: Load in Application Code

**Python:**
```python
from dotenv import load_dotenv
import os

# Load from project's .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")
```

**Critical:** Load from `.env` in **current project directory**, not from parent or shared location.

---

### Step 4: Create `.env.example`

**Template for other developers (or future you):**

```bash
# .env.example
# Copy to .env and fill in your keys

# OpenAI API Key (https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-proj-your-key-here

# Anthropic API Key (https://console.anthropic.com/settings/keys)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Why?** Documents what keys are needed without exposing actual keys.

---

### Step 5: Document in EXTERNAL_RESOURCES.md

**Required:** Update `$PROJECTS_ROOT/project-scaffolding/EXTERNAL_RESOURCES.md`

```markdown
## OpenAI

**Projects using OpenAI:**
| Project | Key Name | Monthly Cost | Status |
|---------|----------|--------------|--------|
| Cortana | cortana-openai | ~$0.60 | Active |
| Trading | trading-openai | ~$15 | Active |
| image-workflow | image-workflow-openai | ~$8 | Active |

**Key Locations:**
- Cortana: `cortana-personal-ai/.env`
- Trading: `trading-copilot/.env`
- image-workflow: `image-workflow/.env`
```

**Why?** Single source of truth for which project uses which key.

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Shared Keys in Parent Directory

```
# DON'T DO THIS
/projects/.env:
  OPENAI_API_KEY=shared-key

# All projects load from parent
```

**Problem:** Can't attribute costs, shared failure, no isolation.

---

### ❌ Anti-Pattern 2: Keys in Version Control

```
# DON'T DO THIS
project/.env:
  OPENAI_API_KEY=sk-proj-abc123

# Committed to git
```

**Problem:** Keys exposed in git history forever, even if deleted later.

**Fix:** Add `.env` to `.gitignore` immediately. If already committed, rotate keys.

---

### ❌ Anti-Pattern 3: Hardcoded Keys

```python
# DON'T DO THIS
api_key = "sk-proj-abc123..."
```

**Problem:** Keys in source code, visible in commits, hard to rotate.

**Fix:** Always use environment variables.

---

### ❌ Anti-Pattern 4: One Key for "Personal Use"

```
# DON'T DO THIS
All projects use "Erik's personal OpenAI key"
```

**Problem:** OpenAI dashboard shows $200/month but can't tell which project spent what.

**Fix:** Create per-project keys, name them clearly.

---

## Key Rotation Strategy

**When to rotate:**
- If key is exposed (git commit, shared accidentally, etc.)
- If project is compromised
- Periodically (every 6-12 months for security hygiene)

**How to rotate:**
1. Create new key with same naming pattern
2. Update project's `.env`
3. Test project still works
4. Revoke old key
5. Update EXTERNAL_RESOURCES.md with new key name

**Tip:** Rotate keys during low-usage periods (not production deployments).

---

## Cost Attribution

### Problem Statement

With shared keys:
```
OpenAI Dashboard:
  sk-shared-key: $200/month

Question: Which project spent the $200?
Answer: Unknown. ❌
```

With per-project keys:
```
OpenAI Dashboard:
  sk-proj-cortana-openai: $0.60/month
  sk-proj-trading-openai: $15/month
  sk-proj-image-workflow-openai: $8/month
  Total: $23.60/month

Question: Which project spent what?
Answer: Clear. ✅
```

### Implementation

**Step 1:** Create keys with descriptive names  
**Step 2:** Each project uses its own key  
**Step 3:** Check OpenAI/Anthropic dashboard  
**Step 4:** See usage per key = usage per project

---

## Security Considerations

### Defense in Depth

**Layer 1: Don't commit keys**
- Add `.env` to `.gitignore`
- Use `.env.example` as template

**Layer 2: Separate keys per project**
- Compromise one project → other projects safe
- Revoke one key → other projects unaffected

**Layer 3: Least privilege**
- OpenAI: Use project-specific keys (no global admin key)
- Scope keys to minimum permissions needed

**Layer 4: Monitor usage**
- Check OpenAI dashboard for unexpected spikes
- Set up alerts (when Cursor adds this feature)

**Layer 5: Rotate periodically**
- Every 6-12 months
- Immediately if exposed

---

## Migration from Centralized Keys

### Current State (Before Migration)

```
agent-os/.env:
  OPENAI_API_KEY=sk-shared-123

Projects:
  - Cortana (uses agent-os key)
  - Trading (uses agent-os key)
  - image-workflow (has own key ✓)
```

### Target State (After Migration)

```
Projects:
  - Cortana/.env: OPENAI_API_KEY=sk-proj-cortana-openai
  - Trading/.env: OPENAI_API_KEY=sk-proj-trading-openai
  - image-workflow/.env: OPENAI_API_KEY=sk-proj-image-workflow-openai

agent-os:
  - No API keys (becomes library, not service)
```

### Migration Steps

**For each project using centralized keys:**

1. **Create project-specific key**
   - Go to OpenAI dashboard
   - Create new key: `{project-name}-openai`
   - Copy key value

2. **Add to project's `.env`**
   ```bash
   cd project-directory
   echo "OPENAI_API_KEY=sk-proj-..." >> .env
   ```

3. **Update code to load from project's `.env`**
   ```python
   # If code loads from agent-os, change it:
   # Before:
   # sys.path.insert(0, '../agent-os')
   # from agent-os import get_api_key
   
   # After:
   from dotenv import load_dotenv
   load_dotenv()  # Loads from THIS project's .env
   api_key = os.getenv("OPENAI_API_KEY")
   ```

4. **Test**
   - Run project
   - Verify it uses new key (check OpenAI dashboard usage)

5. **Update EXTERNAL_RESOURCES.md**
   - Document key name
   - Document location

6. **After all projects migrated:** Remove keys from agent-os

---

## Examples from Real Projects

### Example 1: Cortana Personal AI

**Before:**
```python
# Used agent-os key
sys.path.insert(0, '../agent-os')
api_key = os.getenv("OPENAI_API_KEY")  # From agent-os/.env
```

**After:**
```python
# Uses own key
from dotenv import load_dotenv
load_dotenv()  # Loads from cortana-personal-ai/.env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found - check .env file")
```

**Key created:** `cortana-openai`  
**Cost attribution:** ~$0.60/month visible in OpenAI dashboard  

---

### Example 2: trading-copilot

**Before:**
```python
# Used agent-os key (potentially)
```

**After:**
```python
# Uses own key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
```

**Keys created:**
- `trading-openai`
- `trading-anthropic`

**Cost attribution:** Clear per-provider spend

---

### Example 3: image-workflow

**Status:** Already using per-project key ✓

```python
# image-workflow has always had its own .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

**Key name:** `image-workflow-openai`  
**Why it's good:** Been isolated from day 1

---

## When to Share Keys (Rare Exceptions)

### Exception 1: Development vs. Production

**Pattern:** Different keys for different environments

```
project/.env.development:
  OPENAI_API_KEY=sk-proj-myproject-dev

project/.env.production:
  OPENAI_API_KEY=sk-proj-myproject-prod
```

**Why?** Separate dev costs from prod costs.

---

### Exception 2: Multiple Sub-Projects in Monorepo

**Pattern:** If truly coupled sub-projects (not independent)

```
monorepo/.env:
  OPENAI_API_KEY=sk-proj-monorepo-shared

monorepo/
  ├── service-a/ (uses shared key)
  ├── service-b/ (uses shared key)
  └── service-c/ (uses shared key)
```

**When this is okay:**
- Services are tightly coupled
- You don't need per-service cost attribution
- Failure in one affects all anyway

**When this is NOT okay:**
- Services are independent
- You need cost attribution
- Services have different criticality

---

## Checklist for New Projects

When starting a new project:

- [ ] Create project-specific API keys (name: `{project}-{service}`)
- [ ] Add keys to project's `.env`
- [ ] Add `.env` to `.gitignore`
- [ ] Create `.env.example` as template
- [ ] Load keys with `load_dotenv()` in code
- [ ] Test that keys work
- [ ] Update `EXTERNAL_RESOURCES.md` in project-scaffolding
- [ ] Document key names and locations

---

## Key Naming Conventions

**Format:** `{project-name}-{service-name}`

**Examples:**
- `cortana-openai`
- `trading-anthropic`
- `image-workflow-openai`
- `billing-tracker-anthropic`
- `land-openai`

**Why lowercase-with-dashes?**
- Consistent with project directory names
- Easy to type
- Clear in dashboards
- No special characters

---

## Related Patterns

- **EXTERNAL_RESOURCES.md** - Single source of truth for all services
- **Safety Systems** - `.env` in `.gitignore` is a safety system
- **Project Scaffolding** - Templates include `.env.example`

---

## Success Metrics

**After migration:**
- [ ] Each project has its own `.env`
- [ ] OpenAI dashboard shows usage per project
- [ ] Can answer "Which project spent $X?" instantly
- [ ] No shared keys in centralized locations
- [ ] EXTERNAL_RESOURCES.md documents all key locations

---

## Lessons Learned

**From agent-os experience:**
- Centralized keys seemed efficient initially
- Cost attribution became impossible at scale
- Shared rate limits caused mysterious failures
- Migration took longer than setting up correctly from start

**Takeaway:** Set up per-project keys from day 1. Don't centralize "for convenience."

---

**Last Updated:** December 22, 2025  
**Status:** Migration in progress (Cortana pending)  
**Next Review:** After Cortana migration complete

