# Deep Technical Research: Kiro & Antigravity IDE Integration

## Context

I'm building an automated multi-AI project scaffolding system that:
- Routes tasks to different AI tiers (Tier 1: expensive/smart, Tier 2: mid-level, Tier 3: cheap/simple)
- Calls APIs programmatically (OpenAI, Anthropic, etc.) to automate reviews and builds
- Tracks costs in real-time per API, per task
- Needs to integrate multiple tools/IDEs into a unified workflow

I need to evaluate if **Amazon Kiro** and **Google Antigravity** can integrate into this system.

---

## Research Questions (Critical for Decision)

### 1. Pricing & Cost Model

**For Kiro:**
- What is the exact pricing? (Per month? Per token? Included in AWS?)
- Are there free tiers or trial periods?
- How does cost compare to:
  - OpenAI API ($15-75 per 1M tokens depending on model)
  - Anthropic API ($3-15 per 1M tokens)
  - Cursor ($200/month for $400 credits)
- Can we track cost per project or per task?

**For Antigravity:**
- Same questions as above
- Is it bundled with Google Cloud credits?
- Does the Browser Agent have separate pricing?

### 2. API Access & Programmatic Integration

**For Kiro:**
- Does Kiro have a REST API or Python SDK?
- Can I call Kiro programmatically from my Python CLI tool?
- Example: Can I do `kiro.generate_code(prompt="Build user auth", model="architect")`?
- Does the "CLI integration" mentioned mean:
  - A) A REST API I can call from any language?
  - B) A command-line tool I can shell out to?
  - C) Just an IDE with keyboard shortcuts?
- Can I get responses back as JSON/text for processing?

**For Antigravity:**
- Does Antigravity have an API?
- Can I trigger the "Browser Agent" programmatically?
- Can I spawn multiple agents from a Python script?
- How do I retrieve screenshots/artifacts without the IDE?

### 3. Model Selection & Control

**For Kiro:**
- What AI models power Kiro? (GPT-4? Claude? Custom AWS model?)
- Can I choose which model to use? (e.g., fast model for simple tasks, smart model for complex)
- Does "Agent Hooks" let me specify different models for different triggers?
- Are models updated automatically or can I pin versions?

**For Antigravity:**
- It's powered by Gemini 3 - but which variant? (Gemini Pro? Ultra?)
- Can I choose Gemini Flash (cheap) vs Gemini Pro (expensive)?
- When spawning multiple agents, can each use different models?

### 4. Real-Time Usage & Cost Tracking

**For Kiro:**
- Can I query Kiro's API for current usage/cost?
- Does it expose metrics like:
  - Tokens used per request?
  - Cost per request?
  - Total monthly usage?
- Can I set budget limits (e.g., "stop if cost exceeds $50")?
- Is usage data exportable (JSON, CSV)?

**For Antigravity:**
- Same questions as above
- Does the Browser Agent's usage count separately?
- Can I track cost per agent when running 5 agents in parallel?

### 5. Availability & Access

**For Kiro:**
- Is Kiro publicly available or beta/invite-only?
- How do I sign up? (AWS account required?)
- What regions is it available in?
- Are there waitlists or approval processes?

**For Antigravity:**
- Is Antigravity publicly available?
- How do I sign up? (Google Cloud account required?)
- Is it tied to specific Google Workspace tiers?
- Beta program or general availability?

### 6. Integration with Existing Tools

**For Kiro:**
- Can Kiro coexist with Cursor, VS Code, or other IDEs?
- If I'm using Cursor for building, can Kiro handle just the testing phase?
- Does Kiro have a VS Code extension or is it standalone?
- Can I use Kiro's CLI from a GitHub Actions workflow?

**For Antigravity:**
- Can Antigravity coexist with other IDEs?
- Can I use just the Browser Agent without the full IDE?
- Does it have a VS Code extension?
- Can I run Antigravity agents on a server (headless)?

### 7. Concrete Use Case Examples

**For Kiro:**
- Show me an example of calling Kiro programmatically to:
  1. Generate a Python function based on a spec
  2. Trigger an "Agent Hook" from a script
  3. Get the code response as text
  4. Query the cost of that operation
- If this is not possible, explain what IS possible

**For Antigravity:**
- Show me an example of calling Antigravity programmatically to:
  1. Spawn an agent to test a web app
  2. Get screenshots back as files
  3. Retrieve the agent's report as JSON
  4. Query the cost of that operation
- If this is not possible, explain what IS possible

### 8. Comparison to Our Current Stack

Help me understand:
- **OpenAI API:** We call it, get responses, track costs. Can Kiro/Antigravity do the same?
- **Anthropic API:** Same as above. Can Kiro/Antigravity match this workflow?
- **Cursor IDE:** We use it for building (great credits), but no programmatic API. Are Kiro/Antigravity more like Cursor (IDE only) or more like OpenAI (API + IDE)?

### 9. Limitations & Gotchas

**For Both:**
- What are the rate limits?
- Are there usage caps per month?
- What happens if my API key is compromised?
- Can I use them for commercial projects?
- Are there terms of service restrictions?
- Known bugs or issues in production?

---

## What I Need

**Format:** Detailed technical documentation, not marketing content.

**Include:**
- Direct links to official documentation
- Code examples if available
- Pricing pages or cost calculators
- API reference docs
- Sign-up links

**Goal:** By the end of this research, I should know:
1. Can I integrate Kiro/Antigravity into my Python automation system?
2. What would it cost compared to OpenAI/Anthropic?
3. Are they worth the integration effort?

---

## Why This Matters

If Kiro/Antigravity have:
- Programmatic APIs ✅
- Competitive pricing ✅
- Real-time cost tracking ✅

Then I'll integrate them into my tiered AI system (maybe Kiro for Tier 1 architecture, Antigravity for E2E testing).

If they're just IDEs without APIs (like Cursor), then they're not useful for my automation system, and I'll skip them.

---

**Please provide a technical deep-dive with hard facts, not a philosophical overview.**

