# AI Model Cost Comparison (December 2025)

## Current Situation

**Your usage (Nov 22 - Dec 23):**
- Total: $1,497 in Cursor credits
- Actual cost: $749 ($200 sub + $549 overage)
- Top models: Claude Sonnet Thinking ($769), Claude Opus Thinking ($680)

---

## Tier 1: Architecture & Complex Tasks

### Current
- Cursor: Claude Opus "High Thinking"
- Cost: ~$680/month

### Ollama (Recommended)
- Model: Claude Sonnet 4/4.5
- Cost: **$19/month** (1,000 interactions)
- Savings: **~$660/month**

### Alternatives
- **Direct Claude Opus API:** $15 input / $75 output per 1M tokens
- **Direct Claude Sonnet API:** $3 input / $15 output per 1M tokens
- **Verdict:** Ollama is cheaper than direct APIs for heavy architecture use

---

## Tier 2: Feature Building & Refactoring

### Current (Jan 2026 Update)
- **Primary:** **Gemini 3 Flash**
- **Cost:** **40x cheaper** than Claude Sonnet
- **Context Usage:** <3-6% observed vs 30% with Sonnet for similar output
- **Verdict:** Promoted to the **Primary Workhorse** for the ecosystem.

### Option A: DeepSeek V3 (Secondary)
- **Cost:** $0.27 input / $1.10 output per 1M tokens
- **vs Claude Sonnet:** 11x cheaper input, 14x cheaper output
- **Quality:** Similar to Claude 3.5 Sonnet
- **Access:** Direct API or via OpenRouter
- **Automation:** Use with Cline CLI

### Option B: OpenRouter (Multi-Model Hub)
- **Models:** DeepSeek, Claude, GPT, Gemini, etc.
- **Cost:** Varies by model
- **Benefit:** Single API key for all models
- **URL:** https://openrouter.ai

### Option C: Keep Cursor, Switch Model
- Use Cursor but choose cheaper models
- Avoid "Thinking" variants (most expensive)
- Use regular Claude Sonnet or Haiku

---

## Tier 3: Simple Tasks, Boilerplate, Docs

### Current
- Mostly manual or expensive models

### Option A: DeepSeek V3 + Cline CLI (RECOMMENDED)
- **Model:** DeepSeek V3
- **Cost:** $0.27 per 1M input tokens
- **Tool:** Cline CLI with `-y` flag (YOLO mode)
- **Automation:** Perfect for subprocess calls
- **Install:** `npm install -g cline`
- **Use case:** Docstrings, lint fixes, simple refactors

### Option B: GPT-4o-mini
- **Cost:** $0.15 input / $0.60 output per 1M tokens
- **Quality:** Good for simple tasks
- **Access:** OpenAI API

### Option C: Claude Haiku
- **Cost:** $0.25 input / $1.25 output per 1M tokens
- **Quality:** Fast, cheap, good for simple tasks
- **Access:** Anthropic API

---

## Model Pricing Table (Per 1M Tokens)

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **Claude Opus (Thinking)** | $15 | $75 | Most expensive, what you're using |
| **Claude Sonnet (Thinking)** | $3 | $15 | What you're using most |
| **Claude Sonnet (Regular)** | $3 | $15 | Same cost, less "thinking" |
| **Claude Haiku** | $0.25 | $1.25 | 12x cheaper than Sonnet |
| **GPT-4o** | $2.50 | $10 | Competitive with Sonnet |
| **GPT-4o-mini** | $0.15 | $0.60 | 20x cheaper than Sonnet |
| **DeepSeek V3** | $0.27 | $1.10 | 11x cheaper than Sonnet, similar quality |
| **Gemini Flash** | $0.075 | $0.30 | 40x cheaper than Sonnet |
| **Gemini Pro** | $1.25 | $5.00 | 2.4x cheaper than Sonnet |

---

## Recommended Architecture

### Tier 1: Ollama ($19/mo)
- **Tasks:** Project scaffolding, architecture design, complex algorithms
- **Model:** Claude Sonnet 4/4.5 (included)
- **Integration:** CLI via subprocess
- **Estimated usage:** ~500 interactions/month
- **Cost:** $19/month (flat)

### Tier 2: DeepSeek V3 + Cline
- **Tasks:** Feature building, refactoring, medium complexity
- **Model:** DeepSeek V3 ($0.27/$1.10 per 1M)
- **Integration:** Cline CLI or direct API
- **Estimated usage:** ~100M tokens/month
- **Cost:** ~$30/month (vs $769 currently!)

### Tier 3: DeepSeek V3 + Cline
- **Tasks:** Boilerplate, docs, simple fixes
- **Model:** DeepSeek V3 ($0.27/$1.10 per 1M)
- **Integration:** Cline CLI with `-y` flag
- **Estimated usage:** ~50M tokens/month
- **Cost:** ~$15/month

### Reviews: OpenAI + Anthropic APIs
- **Keep current system** (multi-AI reviews)
- **Cost:** ~$10-20/month for reviews

---

## Total Cost Comparison

### Current (Cursor Ultra)
- Subscription: $200
- Overage: $549
- **Total: $749/month**

### With Ollama Only
- Cursor: $249 ($200 + $49 overage)
- Ollama: $19
- **Total: $268/month**
- **Savings: $481/month**

### With Ollama + DeepSeek (Full Stack)
- Ollama (Tier 1): $19
- DeepSeek (Tier 2/3): $45
- Reviews: $15
- Cursor (minimal use): $200 (just the sub, no overage)
- **Total: $279/month**
- **Savings: $470/month = $5,640/year**

### With Ollama + DeepSeek (Cancel Cursor)
- Ollama (Tier 1): $19
- DeepSeek (Tier 2/3): $45
- Reviews: $15
- Cline (IDE): Free (VS Code extension)
- **Total: $79/month**
- **Savings: $670/month = $8,040/year** 🎯

---

## Free Credits & Startup Programs

### AWS Activate (for Ollama)
- **Credits:** $1,000
- **Duration:** Ollama would be free for ~4 years
- **Requirements:** Website + LinkedIn profile
- **Apply:** https://aws.amazon.com/activate/

### Google Cloud Startup Program
- **Credits:** $2,000 - $350,000
- **Use for:** Gemini Pro, Gemini Flash
- **Requirements:** Early-stage startup
- **Apply:** https://cloud.google.com/startup

### Anthropic Credits
- Check if they have a startup program
- Sometimes offer credits for API usage

---

## Action Items

### Immediate (This Week)
1. [ ] Sign up for Ollama (free preview)
2. [ ] Get DeepSeek API key
3. [ ] Install Cline CLI (`npm install -g cline`)
4. [ ] Test DeepSeek quality vs Claude Sonnet
5. [ ] Test Ollama quality vs Cursor

### Week 1 (2026)
1. [ ] Apply for AWS Activate credits
2. [ ] Apply for Google Cloud credits
3. [ ] Build Ollama integration
4. [ ] Build DeepSeek/Cline integration
5. [ ] Route tasks to appropriate tiers

### Decision Point
- **Keep Cursor?** Only if you need it for complex manual work
- **Cancel Cursor?** If Ollama + Cline + VS Code is enough
- **Target:** Get under $300/month total

---

## Questions to Resolve

1. **DeepSeek quality:** Is it truly comparable to Claude Sonnet?
   - Need to test with real tasks
   - Compare output quality

2. **Cline automation:** Does the `-y` flag work well?
   - Test with simple tasks
   - Verify it doesn't break things

3. **Ollama rigidity:** Is the spec-driven workflow too rigid?
   - Test with real Tier 1 task
   - See if it's helpful or annoying

4. **Cursor dependency:** Can you live without Cursor?
   - What do you actually use Cursor for?
   - Could Cline + VS Code replace it?

---

## Next Steps

**Let's test before committing:**
1. Get DeepSeek API key ($5 credit to start)
2. Run a simple Tier 2 task with DeepSeek
3. Compare quality to Claude Sonnet
4. If good → integrate
5. If bad → look at other options

**Want me to:**
- Help set up DeepSeek testing?
- Create integration code for Cline CLI?
- Research more alternatives?

