# AI Services & Credits Tracker

> **Purpose:** Track all AI services, API keys, costs, and available credits  
> **Location:** Lives in project-scaffolding (reference for all projects)

---

## 🔑 Active Services (Currently Using)

| Service | Purpose | Cost | API Key Location | Status |
|---------|---------|------|------------------|--------|
| **Cursor Ultra** | IDE with AI | $200/month + overage | N/A (IDE) | ⚠️ High overage usage |
| **OpenAI** | Reviews, Tier 2/3 | Pay-per-use | `SCAFFOLDING_OPENAI_KEY` | ✅ Active |
| **Anthropic** | Reviews, Tier 1 | Pay-per-use | `SCAFFOLDING_ANTHROPIC_KEY` | ✅ Active |
| **XAI (Grok)** | Testing | $25 prepaid | `XAI_API_KEY` | ✅ Active |

**Current Monthly Spend:** ~$425/month ($200 Cursor + ~$225 overage)

---

## 🎯 Services to Add (Cost Reduction)

| Service | Purpose | Estimated Cost | Setup Status | Notes |
|---------|---------|----------------|--------------|-------|
| **Kiro** | Tier 1 architecture | $19/month (1,000 interactions) | ⏳ To setup | Currently free preview |
| **DeepSeek V3** | Tier 2/3 tasks | ~$30-50/month | ⏳ To setup | $0.27 per 1M tokens (11x cheaper than Claude) |
| **Cline CLI** | Automation tool | Free | ⏳ To install | Works with DeepSeek |

**Projected Monthly Spend:** ~$270-300/month  
**Projected Savings:** ~$125-155/month (~30%)

---

## 💳 Free Credits & Startup Programs (To Apply)

| Program | Provider | Credits Available | Requirements | Status | Link |
|---------|----------|-------------------|--------------|--------|------|
| **AWS Activate** | Amazon (for Kiro) | $1,000 | Website + LinkedIn profile | ⏳ To apply | [aws.amazon.com/activate](https://aws.amazon.com/activate/) |
| **Google Cloud Startup** | Google | $2,000 - $350,000 | Early-stage startup | ⏳ To apply | [cloud.google.com/startup](https://cloud.google.com/startup) |
| **Anthropic Credits** | Anthropic | TBD | Check if available | ⏳ To research | TBD |
| **OpenAI Credits** | OpenAI | TBD | Startup program? | ⏳ To research | TBD |

**Potential Impact:**
- AWS $1,000 = Kiro free for ~4 years
- Google $2,000+ = Gemini Pro/Flash free for extended period
- **Total potential free credits: $3,000 - $351,000**

---

## 📊 Cost Comparison (Per 1M Tokens)

### Input Tokens

| Model | Cost per 1M | vs Claude Sonnet | Use Case |
|-------|-------------|------------------|----------|
| **Claude Opus** | $15.00 | 5x more expensive | ❌ Too expensive |
| **Claude Sonnet** | $3.00 | Baseline | ⚠️ Current default |
| **GPT-4o** | $2.50 | 1.2x cheaper | ✅ Good alternative |
| **Gemini Pro** | $1.25 | 2.4x cheaper | ✅ Worth testing |
| **Claude Haiku** | $0.25 | 12x cheaper | ✅ Tier 3 |
| **DeepSeek V3** | $0.27 | **11x cheaper** | ✅✅ **Best value** |
| **GPT-4o-mini** | $0.15 | 20x cheaper | ✅ Tier 3 |
| **Gemini Flash** | $0.075 | 40x cheaper | ✅ Tier 3 |

### Output Tokens

| Model | Cost per 1M | vs Claude Sonnet | Use Case |
|-------|-------------|------------------|----------|
| **Claude Opus** | $75.00 | 5x more expensive | ❌ Too expensive |
| **Claude Sonnet** | $15.00 | Baseline | ⚠️ Current default |
| **GPT-4o** | $10.00 | 1.5x cheaper | ✅ Good alternative |
| **Gemini Pro** | $5.00 | 3x cheaper | ✅ Worth testing |
| **Claude Haiku** | $1.25 | 12x cheaper | ✅ Tier 3 |
| **DeepSeek V3** | $1.10 | **14x cheaper** | ✅✅ **Best value** |
| **GPT-4o-mini** | $0.60 | 25x cheaper | ✅ Tier 3 |
| **Gemini Flash** | $0.30 | 50x cheaper | ✅ Tier 3 |

---

## 🎯 Recommended Tier Architecture

### Tier 1: Architecture & Complex Design
- **Primary:** Kiro ($19/month, includes Claude Sonnet 4/4.5)
- **Fallback:** Claude Opus API (if Kiro hits limit)
- **Estimated cost:** $19/month (Kiro covers most)

### Tier 2: Feature Building & Refactoring
- **Primary:** DeepSeek V3 ($0.27/$1.10 per 1M)
- **Fallback:** GPT-4o or Gemini Pro
- **Estimated cost:** $30-50/month

### Tier 3: Simple Tasks & Boilerplate
- **Primary:** DeepSeek V3 (with caching)
- **Fallback:** GPT-4o-mini or Gemini Flash
- **Estimated cost:** $10-20/month

### Reviews: Multi-AI System
- **Current:** OpenAI + Anthropic
- **Keep as-is:** Already optimized
- **Estimated cost:** $10-20/month

---

## 📝 API Key Storage

**Per-Project Keys (Recommended):**
```bash
# In each project's .env
CORTANA_OPENAI_KEY=sk-...
TRADING_ANTHROPIC_KEY=sk-ant-...
```

**Scaffolding Keys:**
```bash
# In project-scaffolding/.env
SCAFFOLDING_OPENAI_KEY=sk-...
SCAFFOLDING_ANTHROPIC_KEY=sk-ant-...
SCAFFOLDING_DEEPSEEK_KEY=sk-...
SCAFFOLDING_XAI_KEY=xai-...
SCAFFOLDING_KIRO_AUTH=aws_builder_id
```

See `EXTERNAL_RESOURCES.md` for full key locations.

---

## 🚨 Cost Alerts & Monitoring

**Track in AI Usage Billing Tracker:**
- Cursor: Export CSV monthly, analyze trends
- OpenAI: Query API for usage
- Anthropic: Query API for usage
- DeepSeek: Query API for usage
- XAI: Check dashboard

**Alert thresholds:**
- Cursor overage > $100 → Review model usage
- Any API > $50/month → Investigate spike
- DeepSeek quality issues → Fall back to GPT-4o

---

## 📅 Action Items

### This Week
- [ ] Sign up for DeepSeek ($5 to start)
- [ ] Sign up for Kiro (free preview)
- [ ] Install Cline CLI (`npm install -g cline`)
- [ ] Test DeepSeek quality vs Claude Sonnet
- [ ] Test Kiro quality vs Cursor

### Next Week
- [ ] Apply for AWS Activate ($1,000 credits)
- [ ] Apply for Google Cloud Startup (up to $350k credits)
- [ ] Research Anthropic startup credits
- [ ] Research OpenAI startup credits

### Week 2
- [ ] Integrate Kiro CLI into scaffold
- [ ] Integrate DeepSeek into scaffold
- [ ] Build cost tracking dashboard
- [ ] Set up automated alerts

---

## 🔗 Useful Links

**Sign Up:**
- DeepSeek: https://platform.deepseek.com/
- Kiro: https://kiro.dev/
- Cline: https://github.com/cline/cline
- XAI: https://console.x.ai/

**Credits:**
- AWS Activate: https://aws.amazon.com/activate/
- Google Cloud Startup: https://cloud.google.com/startup

**Documentation:**
- DeepSeek API: https://platform.deepseek.com/docs
- Kiro CLI: https://docs.kiro.dev/cli
- Cline CLI: https://github.com/cline/cline#cli

---

**Last Updated:** December 23, 2025  
**Next Review:** Weekly (track Cursor overage trends)

