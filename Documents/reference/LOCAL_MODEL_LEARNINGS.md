# Local Model Learnings

> **Purpose:** Institutional memory for working with local AI models (Ollama)
> **Created:** January 10, 2026
> **Updated:** January 10, 2026

---

## Why This Document Exists

Local models are a black box. When they fail or succeed, the knowledge evaporates between sessions. This document captures:
- What works and what doesn't
- Model-specific quirks
- Prompt patterns that improve results
- Failure modes to avoid

**Goal:** Stop re-learning the same lessons. Make prompts better over time.

---

## Model Profiles

### DeepSeek-R1 (14b)

**Best for:**
- Complex reasoning tasks
- Multi-step problem solving
- Code generation (with caveats)

**Known limitations:**
- Timeout issues on long tasks (observed Jan 10, 2026)
- Can be slow (87s average response)
- Sometimes over-explains when brevity needed

**Prompt tips that work:**
- Be explicit about output format
- Break complex tasks into steps
- Include examples when possible

**Prompt anti-patterns:**
- (Add as discovered)

---

### Qwen 2.5 / Qwen 3 (4b, 14b)

**Best for:**
- General-purpose tasks
- Shows reasoning (helpful for debugging)
- Good balance of speed/quality

**Known limitations:**
- (Add as discovered)

**Prompt tips that work:**
- (Add as discovered)

**Prompt anti-patterns:**
- (Add as discovered)

---

### Llama 3.2 (3b)

**Best for:**
- Speed-critical tasks
- Simple classification
- High-volume filtering

**Known limitations:**
- Lower quality on complex tasks
- May miss nuance

**Prompt tips that work:**
- Keep prompts short and direct
- Binary yes/no questions work well

**Prompt anti-patterns:**
- (Add as discovered)

---

## Prompt Pattern Library

### Pattern: Acceptance Criteria Checklist

**What:** Structure prompts with explicit checkboxes for the model to verify against.

**Why it works:** Local models respond well to concrete, binary success criteria. Reduces ambiguity.

**Example:**
```markdown
### [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [ ] **Functional:** Code correctly implements X
- [ ] **Syntax:** File passes linting
- [ ] **Standards:** Uses pathlib.Path
- [ ] **Verification:** Tests pass
```

**First observed:** Warden Enhancement prompts (Jan 10, 2026)
**Models tested:** DeepSeek-R1, Qwen 2.5

---

### Pattern: Context Bridge

**What:** Explicitly provide file contents and context rather than assuming the model can find them.

**Why it works:** Local models don't have tool access like cloud models. They need context spoon-fed.

**Example:**
```markdown
**Current code (lines 73-82):**
\`\`\`python
try:
    os.replace(temp_name, path)
except Exception as e:
    # ... show actual code
\`\`\`
```

**First observed:** Safety Audit prompts (Jan 10, 2026)
**Models tested:** DeepSeek-R1

---

### Pattern: (Add more as discovered)

---

## Failure Log

Track specific failures to identify patterns.

| Date | Model | Task | Failure Mode | Resolution |
|------|-------|------|--------------|------------|
| Jan 10, 2026 | DeepSeek-R1 | Warden enhancement | Timeout on complex tasks | Floor Manager took over |
| | | | | |

---

## Session Observations

### Jan 10, 2026 - Warden Enhancement Sprint

**Models used:** DeepSeek-R1, Qwen 2.5 (via Floor Manager)

**What happened:**
- DeepSeek had timeout issues on worker tasks
- Floor Manager (Gemini Flash) ended up doing the work directly
- Prompts written by Claude Opus worked well when Floor Manager executed them

**Learnings:**
- Structured prompts with acceptance criteria translate well across models
- Local models may need simpler, more atomic tasks
- Floor Manager as QA + backup executor is a good pattern

**Prompt refinements:**
- (Add any adjustments made)

---

## Improvement Backlog

Things to try or investigate:

- [ ] Test if breaking tasks into smaller chunks helps DeepSeek timeout issues
- [ ] Compare same prompt across DeepSeek vs Qwen for quality
- [ ] Create prompt templates optimized for each model tier
- [ ] Add timing benchmarks to session observations
- [ ] Track success rate by task type + model combination

---

## Related Documents

- `patterns/local-ai-integration.md` - Model tiers and when to use each
- `AGENTS.md` - Caretaker Role (working with memory-less entities)
- `Documents/archives/planning/warden_evolution/WARDEN_PROMPTS_INDEX.md` - Example of structured prompts

---

*This is a living document. Update it when you learn something new about local models.*
