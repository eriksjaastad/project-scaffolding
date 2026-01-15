# 🏭 The Audit Assembly Line (V2.1)
> Purpose: A standardized, ruthless process for ecosystem-wide project hardening.
> Strategy: "Snapshot Once, Audit in Slices, Certify at the End."

## 🏛️ THE HIERARCHY
1. **The Conductor (Erik):** Final Approval, Vision, and Context Control.
2. **Super Manager (Strategic Advisor):** Prompt Architect and Roadmap Manager.
3. **Floor Manager (Gemini Sub-Agent):** The "Hands." Middle Management with tool access. Delegates logic to Workers.
4. **The Workers (Ollama Models):** The "Brain." Local thinkers (Llama/DeepSeek/Qwen) who draft the logic and blueprints.

---

## 🛡️ SAFE ZONES (Exempt from Audit)
The following domains are **Human-First Zones** and are strictly exempt from the Audit Assembly Line:
- **The Vault:** `ai-journal/` (Context history & personal notes)
- **Creative:** `writing/` (Drafts and novels)
- **Rule:** If a directory does not contain a code manifest (`requirements.txt`, `package.json`, `go.mod`), it is skipped by default.

## 🧹 STEP 0: The Local Baseline (Ground Truth)
**Management:** Floor Manager (Gemini)
**Execution:** Worker (Ollama / `qwen3:4b`)
**Action:** Noise reduction, dependency extraction, and debt extraction.

**Prompt for Floor Manager:**
> "Execute **Step 0 (Local Baseline)** for this project.
> 1. **Handshake:** Call `mcp_ollama_ollama_list_models` to verify connection.
> 2. **Delegation:** Use **qwen3:4b** to analyze the project. 
> 3. **Safe Zone Verification:** Confirm this is a coding project. If it is a writing or journal folder, ABORT.
> 4. **Noise Reduction:** Clean up unused imports and formatting to reduce snapshot size.
> 5. **Debt Extraction:** Generate a list of all current **TODOs** and **FIXMEs**.
> 6. **Goal:** Prepare this project for a high-fidelity 'Big Brain' architectural audit. Show the Worker's evidence (e.g., TODO list) once complete."

## 🛠 STEP 1: The Standardized Snapshot (Repomix)
**Executed by:** Conductor (Terminal)
**Action:** Pack the repository into `repomix-output.xml`.

**Command:**
```bash
npx repomix@latest --ignore "**/node_modules/**,**/.env*,**/dist/**,**/.git/**,**/__pycache__/**,**/.pytest_cache/**,**/.venv/**,**/venv/**,**/.DS_Store,**/build/**,**/.idea/**,**/.vscode/**,**/ai-journal/**,**/writing/**"
```

## 📝 STEP 2: The "Contract" (Spec Generation)
**Executed by:** Reviewer (Web)
**Action:** Generate `spec.md` from the Repomix snapshot.

**Prompt for Reviewer:**
> "I am the Architect. You are the Auditor. I am providing a Repomix snapshot of [Project Name]. 
> 1. Read the code and generate a comprehensive `spec.md` that describes how this project functions today.
> 2. Identify the core logic, data models, and entry points.
> 3. Be ruthless—if you find 'Ghost Logic' (undocumented or messy code), mark it as 'Technical Debt'.
> Do not review for security yet. Just define the 'Contract' of what this code currently is."

## 🛡️ STEP 3: The "Ruthless" Audit (Phases A, B, C)
**Executed by:** Reviewer (Web)
**Action:** Run sequential security, resilience, and architectural audits.

### 🚩 PHASE A: DNA & SECURITY (The "Warden" Pass)
**Prompt for Reviewer:**
> "Audit this project for DNA Security based on our Gold Standard.
> 1. Find every absolute path (e.g., `[USER_HOME]/...` or `~/...`). These are critical failures.
> 2. Search for hardcoded API keys, secrets, or plain-text credentials.
> 3. **Doppler Readiness:** Flag every instance of `os.getenv` or `process.env`. These must be mapped to our central Doppler naming convention in the new Spec.
> 4. Check all user-input paths for `safe_slug()` and path traversal protection.
> 5. List every violation as a 'P0 DNA DEFECT'."

### 🚩 PHASE B: RESILIENCE & HYGIENE (The "Hardening" Pass)
**Prompt for Reviewer:**
> "Audit this project for Resilience and Professional Hygiene.
> 1. Identify every `except: pass` or `except Exception: pass` block. These must be replaced with logging.
> 2. Check `requirements.txt` (or equivalent). Are dependencies unpinned (using `>=` or `~=`)? They must be hard-pinned with `==`.
> 3. Identify any 'Magic Numbers' or hardcoded constants that should be in a config file or Doppler.
> 4. Check for shell script safety (spaces in filenames, missing error checks)."

### 🚩 PHASE C: ARCHITECTURAL ALIGNMENT (The "Spec" Pass)
**Prompt for Reviewer:**
> "Compare the code against the `spec.md` we just generated.
> 1. Does the code actually do what the Spec says it does?
> 2. Is there 'Dead Code' or 'Feature Creep' that isn't in the Spec?
> 3. Identify any logic that is 'too clever' and needs to be simplified for long-term maintenance.
> 4. Final Verdict: Grade the project from A to F based on its readiness for the Doppler/Hardened ecosystem."

## 🔨 STEP 4: Industrial Remediation (The Redemption)
**Management:** Floor Manager (Gemini Sub-Agent)
**Execution:** Worker (Ollama Models - Tiered)
**Strategy:** The Floor Manager receives the Mission Order and **delegates the logic** to the local Worker before executing tool calls.

### 🛑 OPERATIONAL GUARDRAIL: THE ATOMIC EDIT MANDATE
> "If a `search_replace` tool call fails, **STOP ALL PARALLEL TASKS.**
> 1. Perform a fresh `read_file` on the target area to verify exact whitespace and characters.
> 2. Execute the fix as a single, atomic operation. 
> 3. **NO BRUTE-FORCING:** Do not attempt multiple parallel variations of the same edit."

### **Mission Order Pattern (Local-First):**
Deliver these one-by-one to the Floor Manager.

**Infrastructure Handshake (Mandatory FIRST Step):**
> "Before I provide the Mission Order, you must perform the **Office Check-In**:
> 1. Use the **`PROJECTS_ROOT`** environment variable to locate `${PROJECTS_ROOT}/AGENTS.md`.
> 2. **PROVE CONNECTION:** Call the `mcp_ollama_ollama_list_models` tool. 
> 3. **DELEGATION RULE:** You are the Floor Manager (the Hands). You must not perform code logic yourself. You must send all drafting/refactoring tasks to the specified **Worker** (Ollama) and then use your tools to apply their blueprint."

1. **Mission Order #1: DNA & Security**
   - **Worker:** **DeepSeek-R1:14b** (Tier 4) - *For complex logic and security.*
   - **Task:** Fix P0 DNA defects, absolute paths, and path traversal identified in `spec.md`.
   - **Evidence:** Grep results for absolute paths and secrets.

2. **Mission Order #2: Resilience & Hygiene**
   - **Worker:** **Qwen3:4b** (Tier 2) - *For structural refactoring and safety.*
   - **Task:** Fix `except: pass`, magic numbers, and shell script safety.
   - **Evidence:** Linter results or manual verification of logging.

3. **Mission Order #3: Cleanup & Alignment**
   - **Worker:** **Llama3.2:3b** (Tier 1) - *For documentation and file movement.*
   - **Task:** Remove dead code, update docs, and move files to standard locations.
   - **Evidence:** `ls` and `git status` showing a clean tree.

## 🏆 STEP 5: Final Certification (The Redemption Certificate)
**Executed by:** Reviewer (Web)
**Action:** Verification of all Step 4 remediations and issuance of a Final Grade upgrade.

### 🛑 CRITICAL: THE FRESHNESS MANDATE
> "Before starting the Final Audit, the Reviewer **MUST** verify they are reading the latest code.
> 1. If using a Git tool: **Pull the `main` branch** to clear any local cache.
> 2. If using Repomix: Verify the file contains new symbols (e.g., `safe_slug`) identified in the remediation.
> 3. **DO NOT** rely on memory from previous turns. Treat this as a 'Zero-Knowledge' audit of the new state."

**Prompt for Reviewer:**
> "I am providing a post-remediation Repomix snapshot of [Project Name]. 
> 1. Compare this snapshot against the previous 'Ruthless Audit' findings and the `spec.md`.
> 2. **Verification:** Confirm that every P0 DNA Defect and Resilience issue has been resolved.
> 3. **Final Grade:** If the project is 100% compliant with the Gold Standard, award a **Grade: A**.
> 4. **Archive:** Generate a `REVIEWS/REDEMPTION_CERTIFICATE.md` summarizing the transition from the old grade to the new."

---

## 📋 THE ASSEMBLY LINE QUEUE (Alphabetical)
- [X] `3d-pose-factory`
- [ ] `ai-usage-billing-tracker`
- [ ] `ai-model-testing`
- [ ] `ai_router`
- [ ] `analyze-youtube-videos`
- [ ] `audit-agent`
- [ ] `automation-consulting`
- [ ] ... (Continue down the directory list)
