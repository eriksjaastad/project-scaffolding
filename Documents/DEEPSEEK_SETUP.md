# DeepSeek Setup Guide

## 1. Get API Key

**Sign up:**
1. Go to: https://platform.deepseek.com/
2. Create account
3. Add credits (starts at $5 minimum)
4. Generate API key

**Pricing:**
- Input: $0.27 per 1M tokens
- Output: $1.10 per 1M tokens
- Cache hits: $0.014 per 1M tokens (98% discount!)

---

## 2. Test DeepSeek Quality

Before integrating, let's test if quality is acceptable:

```bash
# Install OpenAI-compatible client (DeepSeek uses OpenAI format)
pip install openai

# Test script
python scripts/test_deepseek.py
```

**Test script** (`scripts/test_deepseek.py`):
```python
#!/usr/bin/env python3
"""Test DeepSeek quality vs Claude"""

from openai import OpenAI

# DeepSeek uses OpenAI-compatible API
client = OpenAI(
    api_key="YOUR_DEEPSEEK_KEY",
    base_url="https://api.deepseek.com/v1"
)

# Test prompt (typical Tier 2 task)
prompt = """
Write a Python function that:
1. Takes a list of user objects (dicts with 'id', 'name', 'email')
2. Validates email format using regex
3. Removes duplicates based on email
4. Returns sorted list by name
5. Include type hints and docstring
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.0
)

print("DeepSeek Response:")
print("=" * 80)
print(response.choices[0].message.content)
print("=" * 80)
print(f"\nTokens: {response.usage.total_tokens}")
print(f"Cost: ${response.usage.total_tokens * 0.00000027:.6f}")
```

---

## 3. Integrate into scaffold

**Add to `scaffold/deepseek.py`:**
```python
"""DeepSeek integration for Tier 2/3 tasks"""

from openai import OpenAI
from typing import Dict, Any

class DeepSeekExecutor:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-chat"
    
    def execute(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """Execute task with DeepSeek"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0  # Deterministic for code
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        cost = tokens * 0.00000027  # $0.27 per 1M
        
        return {
            "content": content,
            "tokens": tokens,
            "cost": cost,
            "model": self.model
        }
```

---

## 4. Environment Setup

**Add to `.env`:**
```bash
# DeepSeek
DEEPSEEK_API_KEY=sk-...

# XAI (Grok)
XAI_API_KEY=xai-...
```

---

## 5. Usage in Tier System

```python
# In scaffold/dispatch.py

if task.tier == 1:
    # Use Ollama CLI
    result = deepseek.execute(task)

elif task.tier == 2:
    # Use DeepSeek (cheap, quality)
    result = deepseek.execute(task.prompt)

elif task.tier == 3:
    # Use DeepSeek (even cheaper with caching)
    result = deepseek.execute(task.prompt)
```

---

## Next Steps

1. [ ] Sign up for DeepSeek
2. [ ] Get $5 in credits
3. [ ] Test quality with real task
4. [ ] Compare to Claude Sonnet output
5. [ ] If good → integrate
6. [ ] If bad → try GPT-4o-mini instead

