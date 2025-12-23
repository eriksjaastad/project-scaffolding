This deep technical research evaluates **Amazon Kiro** and **Google Antigravity** as of **December 2025**.

### **Executive Summary**

Both tools are currently in **Public Preview** (released Oct/Nov 2025).

* **Amazon Kiro** is a **Spec-Driven IDE** available via `kiro.dev`. It is essentially a wrapper around **Claude Sonnet 4 / 4.5** with a rigid "Requirements  Design  Code" workflow.
* **Google Antigravity** is an **Agentic Platform** (fork of VS Code/Windsurf) powered by **Gemini 3**. It excels at asynchronous multi-agent tasks and visual browser verification.

**The Hard Truth:** Neither tool offers a native `import kiro` or `import antigravity` Python SDK for external orchestration. They are designed as **interactive environments (IDEs)**, not backend APIs.

* **To automate Kiro:** You must use its **CLI** (`kiro-cli`) in a shell subprocess.
* **To automate Antigravity:** You generally cannot "drive" the IDE programmatically. You must use the **Gemini 3 API** directly to replicate its behavior, or use Antigravity manually as a "Mission Control" dashboard.

---

### **1. Pricing & Cost Model**

| Feature | **Amazon Kiro** | **Google Antigravity** |
| --- | --- | --- |
| **Current Status** | Public Preview (Free) | Public Preview (Free) |
| **Future Pricing** | **Tier 1:** Free (50 agent interactions/mo)<br>

<br>**Tier 2 (Pro):** $19/mo (1,000 interactions)<br>

<br>**Tier 3 (Pro+):** $39/mo (3,000 interactions) | Likely bundled with **Google Cloud / Gemini API** usage limits. Currently "generous rate limits" for preview. |
| **Model Cost** | Included in subscription (no per-token fee). | Free in preview. API usage (outside IDE) is ~$2/1M input (Gemini 3 Pro). |
| **Cost Tracking** | **Real-time credit usage** visible in IDE. | **Quota-based.** Hard limits reset every few hours. |
| **Commercial Use** | Yes (AWS Builder ID required). | Yes (Google Cloud account required). |

**Cost vs. API:**

* **Kiro Pro ($19/mo)** is significantly cheaper than raw API calls if you max out your 1,000 interactions (approx. equivalent to ~5M-10M tokens of Claude Sonnet 4).
* **Antigravity** is essentially a "free UI" for Gemini 3 during preview, making it infinite leverage until they gate it.

---

### **2. API Access & Programmatic Integration**

This is the critical blocker for your "Tiered AI System."

#### **Amazon Kiro: The CLI Workaround**

Kiro does **not** have a REST API. However, it ships with a powerful **CLI** that shares the IDE's context.

* **Can you call it programmatically?** Yes, via shell commands.
* **Method:** `subprocess.run(["kiro", "task", "generate", "--prompt", "Fix the auth bug"])`
* **Output:** It modifies files directly on disk. It does *not* return JSON code snippets to your script; it acts on the file system.
* **Automation Strategy:** You can trigger Kiro from your Python script to refactor code, wait for the process to exit, and then run your own tests.

#### **Google Antigravity: The "Mission Control" Limit**

Antigravity is strictly a GUI application. It does **not** have a headless mode or CLI for spawning agents.

* **Can you call it programmatically?** No.
* **The Alternative:** You must use the **Gemini 3 API** directly.
* *Note:* The "Browser Agent" (visual verification) is a feature of the **IDE**, not the raw API. To replicate this programmatically, you would need to build a scaffolding using **Puppeteer + Gemini 3 Vision**.



---

### **3. Model Selection & Control**

| Feature | **Amazon Kiro** | **Google Antigravity** |
| --- | --- | --- |
| **Primary Model** | **Claude Sonnet 4** & **4.5** (Anthropic) | **Gemini 3 Pro** & **Deep Think** (Google) |
| **Backup Model** | Claude 3.7 Sonnet | Gemini 3 Flash (Fast/Cheap) |
| **Model Switching** | **Yes.** Can toggle between "Reliable" (Sonnet 4) and "Fast" (Auto/Mixed). | **Yes.** Can assign different agents (e.g., "Researcher" vs "Coder") to different models. |
| **Context Window** | ~200k tokens (Project-aware) | ~1M+ tokens (Full repo context) |

**Critical Distinction:** Kiro is *rigid*. It forces the model through a "Spec" pipeline. You cannot easily ask Kiro to just "vibe check" something; it will want to write a `requirements.md` first.

---

### **4. Real-Time Usage & Cost Tracking**

* **Kiro:** Displays a "Credit Balance" in the bottom corner (e.g., "850/1000 credits").
* *Programmatic Access:* No API to query this balance. You would have to scrape the logs or track it manually.


* **Antigravity:** Opaque. It hits a rate limit wall (e.g., "You have reached your 5-hour limit for Gemini 3 Deep Think").
* *Programmatic Access:* None.



---

### **5. Concrete Integration Plan (The "How-To")**

Since you are building a **Tiered AI Automation System**, here is the only viable architecture that includes these tools:

#### **Tier 1: Architecture & Logic (Use Kiro CLI)**

Use Kiro for the "Heavy Lift" where you need guaranteed structural integrity.

* **Trigger:** Python script detects a new feature request.
* **Action:** Script creates a branch and runs Kiro CLI.
* **Command:**
```bash
# Conceptual Kiro CLI usage
kiro run --spec "requirements.md" --task "Implement User Auth"

```


* **Result:** Kiro writes the code and tests. Your script commits the changes.

#### **Tier 2: Verification (Replicate Antigravity)**

Since Antigravity cannot be automated headless, you must **replicate** its "Browser Agent" using the Gemini API.

* **Tool:** **Selenium / Playwright** + **Gemini 3 Pro API**.
* **Action:**
1. Script spins up the local server.
2. Script takes a screenshot of the homepage.
3. Script sends screenshot to Gemini 3 API: *"Does this look broken? Return JSON."*



#### **Tier 3: Quick Fixes (Raw API)**

For simple tasks (fixing syntax, updating docs), do **not** use Kiro or Antigravity. Use direct calls to **Gemini 3 Flash** or **Claude 3.5 Haiku** via their respective standard APIs. It is 100x faster and cheaper.

---

### **6. Limitations & Gotchas**

1. **Kiro's "Waterfal" Rigidness:** Kiro can be annoying for small changes. If you ask it to "change the color," it might try to update the `design.md` spec first. It is overkill for small tasks.
2. **Antigravity's Resource Hog:** Running multiple agents in Antigravity (e.g., 5 parallel tasks) can melt a laptop. It is heavy.
3. **Authentication:** Kiro CLI requires an active AWS Builder ID session. You may need to refresh tokens manually (`aws sso login`) on your build server, which makes fully autonomous "headless" servers difficult to maintain.

### **Final Verdict for Your Project**

* **Can you integrate Kiro?** **YES**, via the CLI. It is excellent for "Phase 1: Scaffolding" to ensure your project structure is solid.
* **Can you integrate Antigravity?** **NO**, not programmatically. It is a tool for *you* (the human) to use for review. For automation, use the **Gemini 3 API**.

**Recommendation:**
Use **Kiro CLI** for your "Tier 1" architecture builds. Skip Antigravity for the automation pipeline and instead build a small **"Gemini Vision QA"** script using the raw API to check your UI.

Here is a video reviewing the actual hands-on workflow of Antigravity to see the "Browser Agent" you would be trying to replicate:
[Google Antigravity: Hands on with our new agentic development platform](https://www.youtube.com/watch?v=uzFOhkORVfk)

This video is relevant because it demonstrates the "Mission Control" and "Browser Agent" features in real-time, helping you visualize exactly what logic you would need to replicate programmatically using the Gemini API.