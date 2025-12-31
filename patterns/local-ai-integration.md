# Local AI Integration Guide

> **Purpose:** How to use local AI models to reduce API costs while maintaining quality  
> **Created:** December 30, 2025  
> **Cost Savings:** $480-1,020/year for typical projects

---

## Why Local AI?

**The Problem:**
- API costs climbing as projects scale ($55-100/month typical)
- Every call costs money
- No cost control
- Rate limits and outages

**The Solution:**
- Run AI models locally (FREE after download)
- Use cloud APIs only when quality is critical
- Save $40-85/month per active project

---

## Recommended Local Models

### The Perfect 4-Tier Setup

**Tier 1: Speed Demon** (10% of tasks)
- **Model:** llama3.2:3b
- **Speed:** 13 seconds
- **Quality:** Good
- **Use for:** Real-time filtering, high-volume tasks
- **Install:** `ollama pull llama3.2:3b`

**Tier 2: Primary Workhorse** ⭐ (80% of tasks)
- **Model:** qwen3:4b
- **Speed:** 27 seconds
- **Quality:** Very good (shows reasoning!)
- **Use for:** Most filtering, analysis, general queries
- **Install:** `ollama pull qwen3:4b`
- **This should be your DEFAULT local model**

**Tier 3: Strategic Thinker** (8% of tasks)
- **Model:** qwen3:14b
- **Speed:** 42 seconds
- **Quality:** Excellent
- **Use for:** Complex analysis, strategic decisions
- **Install:** `ollama pull qwen3:14b`

**Tier 4: Reasoning Expert** (2% of tasks)
- **Model:** deepseek-r1:14b
- **Speed:** 87 seconds
- **Quality:** Exceptional (shows detailed reasoning)
- **Use for:** High-stakes decisions, learning mode
- **Install:** `ollama pull deepseek-r1:14b`

---

## Installation (10 Minutes)

### Step 1: Install Ollama

```bash
# Mac (Homebrew)
brew install ollama

# Start service
brew services start ollama

# Verify
ollama --version
```

### Step 2: Download Models

```bash
# Primary model (use this for most tasks)
ollama pull qwen3:4b

# Speed model (real-time tasks)
ollama pull llama3.2:3b

# Optional: Strategic models (if needed)
ollama pull qwen3:14b
ollama pull deepseek-r1:14b
```

### Step 3: Test

```bash
ollama run qwen3:4b "Hello, how are you?"
```

**Server runs at:** `http://localhost:11434`

---

## Integration Patterns

### Pattern 1: Smart Router (Recommended)

Create a router that chooses local vs cloud based on complexity:

```python
# utils/ai_router.py

import openai
import os

class AIRouter:
    """
    Smart routing between local and cloud AI
    """
    
    def __init__(self):
        self.local_base = "http://localhost:11434/v1"
        self.openai_base = "https://api.openai.com/v1"
        self.openai_key = os.getenv("OPENAI_API_KEY")
    
    def chat(self, messages, complexity="medium", model_override=None):
        """
        Route based on complexity
        
        Args:
            messages: List of message dicts
            complexity: "ultra_fast" | "fast" | "medium" | "strategic" | "reasoning" | "cloud"
            model_override: Specific model to use
        
        Returns:
            Response string
        """
        
        if model_override:
            return self._call_model(model_override, messages)
        
        # Route based on complexity
        if complexity == "ultra_fast":
            # Real-time tasks (13s)
            return self._call_local(messages, "llama3.2:3b")
        
        elif complexity == "fast" or complexity == "medium":
            # Default for most tasks (27s) ⭐
            return self._call_local(messages, "qwen3:4b")
        
        elif complexity == "strategic":
            # Complex analysis (42s)
            return self._call_local(messages, "qwen3:14b")
        
        elif complexity == "reasoning":
            # High-stakes decisions (87s)
            return self._call_local(messages, "deepseek-r1:14b")
        
        else:  # cloud
            # Quality-critical tasks
            return self._call_cloud(messages, "gpt-4o")
    
    def _call_local(self, messages, model):
        """Call local Ollama"""
        openai.api_base = self.local_base
        openai.api_key = "not-needed"
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def _call_cloud(self, messages, model):
        """Call cloud API"""
        openai.api_base = self.openai_base
        openai.api_key = self.openai_key
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content

# Usage:
router = AIRouter()

# Most tasks → Local (FREE)
response = router.chat(
    [{"role": "user", "content": "Is this spam?"}],
    complexity="fast"
)

# Quality-critical → Cloud ($)
response = router.chat(
    [{"role": "user", "content": "Generate production code..."}],
    complexity="cloud"
)
```

---

### Pattern 2: Environment-Based Selection

```python
# .env
AI_PROVIDER=local  # or "cloud"
LOCAL_MODEL=qwen3:4b

# In code
provider = os.getenv("AI_PROVIDER", "local")

if provider == "local":
    openai.api_base = "http://localhost:11434/v1"
    model = os.getenv("LOCAL_MODEL", "qwen3:4b")
else:
    openai.api_base = "https://api.openai.com/v1"
    model = "gpt-4o-mini"
```

---

## When to Use Local vs Cloud

### ✅ Use Local (FREE)

**Perfect for local:**
- Filtering/classification (spam detection, relevance filtering)
- Simple analysis (summarization, keyword extraction)
- Routine queries (calendar, tasks, simple questions)
- Pattern matching
- Sentiment analysis
- Most things that don't require perfect accuracy

**Cost savings:** $40-70/month per project

---

### 🤔 Test Both (Validate Quality)

**Worth testing:**
- Content generation (try local first, cloud if quality insufficient)
- Complex summarization
- Multi-step reasoning
- Strategy recommendations

**Approach:** Use local by default, switch to cloud if results aren't good enough

---

### ❌ Keep Cloud (Quality Critical)

**Always use cloud for:**
- Production code generation
- Architecture decisions
- High-stakes analysis
- Complex writing (documentation, reports)
- When accuracy > cost

**Models to use:**
- Code: GPT-4o or Claude Sonnet
- Analysis: Claude Sonnet or Opus
- Writing: Claude

**Cost:** $5-20/month (acceptable for quality)

---

## Cost Analysis by Project Type

### Small Automation Project
**Before (all cloud):** $10-20/month  
**After (80% local):** $2-5/month  
**Savings:** $5-15/month ($60-180/year)

### Medium Project (like Cortana)
**Before (all cloud):** $30-50/month  
**After (90% local):** $3-8/month  
**Savings:** $25-42/month ($300-504/year)

### Large Project (like Trading)
**Before (all cloud):** $50-100/month  
**After (85% local):** $8-20/month  
**Savings:** $42-80/month ($504-960/year)

---

## Quality Comparison

### Task: Simple Filtering

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| qwen3:4b (local) | 85-90% | 27s | $0 |
| GPT-4o-mini (cloud) | 90-95% | 2s | $0.01 |
| GPT-4o (cloud) | 95-98% | 3s | $0.10 |

**Verdict:** Local is good enough for most filtering

---

### Task: Complex Analysis

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| qwen3:14b (local) | 80-85% | 42s | $0 |
| deepseek-r1 (local) | 85-90% | 87s | $0 |
| GPT-4o (cloud) | 95-98% | 5s | $0.15 |
| Claude Sonnet (cloud) | 98-99% | 4s | $0.20 |

**Verdict:** Test local first, use cloud if quality insufficient

---

### Task: Code Generation

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| qwen3:14b (local) | 60-70% | 45s | $0 |
| GPT-4o (cloud) | 90-95% | 8s | $0.20 |
| Claude Sonnet (cloud) | 95-98% | 7s | $0.25 |

**Verdict:** Use cloud for production code

---

## Integration Checklist

### New Project Setup
- [ ] Install Ollama (`brew install ollama`)
- [ ] Download qwen3:4b (primary model)
- [ ] Download llama3.2:3b (speed model)
- [ ] Create AIRouter utility
- [ ] Set default to local
- [ ] Add cloud API key as fallback
- [ ] Document which tasks use which tier

### Existing Project Migration
- [ ] Identify API usage patterns
- [ ] Categorize tasks (filtering, analysis, code, etc.)
- [ ] Test local models on sample tasks
- [ ] Measure quality vs cloud
- [ ] Migrate non-critical tasks to local
- [ ] Monitor cost savings
- [ ] Fine-tune routing over time

---

## Testing & Validation

**Before full migration:**

1. **Create test suite** with known-good examples
2. **Run same prompts** through local and cloud
3. **Compare outputs** for quality
4. **Measure accuracy** for your specific use case
5. **Set threshold** (e.g., "90% as good is acceptable")

**Ongoing monitoring:**
- Track local vs cloud usage
- Monitor cost savings
- Flag quality issues
- Adjust routing as needed

---

## Troubleshooting

### Ollama Not Running
```bash
brew services restart ollama
# Or manually:
ollama serve
```

### Model Not Found
```bash
ollama list  # See installed models
ollama pull qwen3:4b  # Download if missing
```

### Slow Performance
- Check RAM usage (models need 4-16GB)
- Use smaller model (llama3.2:3b vs qwen3:14b)
- Close other memory-heavy apps

### Poor Quality
- Try larger model (qwen3:14b instead of 4b)
- Use reasoning model (deepseek-r1:14b)
- Fall back to cloud API for that task

---

## Project Scaffolding Integration

### Add to `.env.example`
```bash
# AI Configuration
AI_PROVIDER=local  # or "cloud"
LOCAL_MODEL=qwen3:4b
OPENAI_API_KEY=sk-...  # Fallback for cloud
```

### Add to CLAUDE.md Template
```markdown
## AI Cost Optimization

This project uses local AI for most tasks to reduce costs.

**Local models:** Ollama (qwen3:4b primary)  
**Cloud fallback:** OpenAI/Claude for quality-critical tasks  
**Estimated savings:** $30-60/month

See: /project-scaffolding/patterns/local-ai-integration.md
```

### Add to Project README Template
```markdown
## AI Dependencies

- **Local AI:** Ollama with qwen3:4b (cost optimization)
- **Cloud AI:** OpenAI/Claude (quality-critical tasks only)
- **Setup:** See docs/LOCAL_AI_SETUP.md
```

---

## Success Metrics

**After 1 month:**
- [ ] 70%+ of AI calls use local models
- [ ] API costs reduced by 60%+
- [ ] No quality complaints
- [ ] Smooth developer experience

**After 3 months:**
- [ ] 80%+ of AI calls use local models
- [ ] API costs reduced by 70%+
- [ ] Pattern well-understood
- [ ] Applied to multiple projects

---

## Related Resources

- **Local AI Test Results:** See `/LOCAL_AI_TEST_RESULTS.md` for detailed benchmarks
- **Local AI Setup Script:** `/setup_local_ai.sh`
- **Cost Comparison:** See cost analysis section above

---

*Add this guide to project-scaffolding/patterns/ for future projects*

