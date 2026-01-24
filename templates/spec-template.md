# PROJECT SPEC: [Project Name]
**Status:** Draft / Approved / In-Audit
**Architect:** Erik Sjaastad (The Conductor)
**Super Manager:** Gemini 3 Flash (Strategic Advisor)
**Primary Worker:** Local DeepSeek-R1 (Ollama)

---

## 1. THE "NORTH STAR" (Objective)
*What is the simplest version of this idea? Why are we building it?*
> [Example: A portable, local-first trading dashboard that eliminates ENV-leak risk.]

## 2. CORE REQUIREMENTS (The "Must-Haves")
*If these aren't met, the project is a failure.*
- [ ] **Infrastructure:** Must use Doppler for all secrets (No local .env files).
- [ ] **Portability:** Zero absolute paths. Must run from any directory via `PROJECTS_ROOT` anchor.
- [ ] **Reliability:** No silent failures (`except: pass` is a critical rejection).
- [ ] **Context Optimized:** Must be Repo-Mix compatible for "Stranger's Reviews" (Claude Web).

## 3. DATA ARCHITECTURE (The Shape of Things)
*Describe the 'Source of Truth' for data.*
- **Secrets:** Managed via Doppler (Project: [X], Config: [dev/prod]).
- **Reasoning:** Local-First (Ollama: DeepSeek-R1) for code logic.
- **Storage:** [e.g., Local NDJSON / YAML / SQLite].

## 4. EXECUTION & CLI LOGIC
*Standard ecosystem entry points (Replacing npm/web bias).*
1. **Bootstrap:** `source venv/bin/activate`
2. **Secrets Injection:** `doppler run -- [command]`
3. **Primary Run:** `python scripts/[main_script].py`
4. **Validation:** `pytest` (Standard 100% pass requirement).

## 5. GOVERNANCE & AUDIT RULES
*Rules for the Code Review Agents (The "Ruthless Auditor" layer).*
- **Reject if:** Hardcoded machine-specific paths (e.g., `[USER_HOME]/...`).
- **Reject if:** API keys or secrets in plain text or code comments.
- **Reject if:** Function length > 40 lines without architectural justification.
- **Enforce:** `CODE_QUALITY_STANDARDS.md` and `AGENTS.md` protocols.

## 6. TECHNICAL DEBT & "KNOWNS"
*What are we ignoring for now?*
- [ ] UI is "functional-minimal" (Industrial over Aesthetic).
- [ ] Scaling guards for >1GB datasets not yet implemented.
- [ ] Documentation is Spec-first; full README comes later.

## Related Documentation

**Project-Specific References:**
- Add links to project-specific architecture, patterns, and guides here

**Universal Resources:**
- [Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md)
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md)
- [AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md)
