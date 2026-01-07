# 🛡️ Ecosystem Governance & Review Protocol (v1.1)

**Date:** 2026-01-07
**Status:** ACTIVE
**Goal:** Transition from "Rapid Experimentation" to "Industrial-Grade Hardening."

---

## 🏛️ Part 1: The Claude Synthesis (Process & Mechanics)
*Insights from Claude Code CLI, Web Auditor, and Opus 4.*

### 1. The Fundamental Pivot: Checklist-First Architecture
Intelligence belongs in the **checklist**, not the prompt. Prompts are subjective and mood-dependent; checklists are versioned, auditable specifications of what "reviewed" means.
*   **Evidence-First Rule:** Every check requires an evidence field (e.g., a `grep` output). Empty evidence = Incomplete Review.
*   **The Artifact:** The review deliverable is a completed evidence trail, not an unstructured prose opinion.

### 2. The Blast Radius Prioritization
Audit files in order of their potential to infect the ecosystem:
1.  **Tier 1: Propagation Sources (Highest Impact):** `templates/`, `.cursorrules`, `AGENTS.md`. If these fail, every downstream project inherits the defect.
2.  **Tier 2: Execution Critical:** `scripts/`, `scaffold/`. These run the automation but don't propagate DNA.
3.  **Tier 3: Documentation:** `docs/`, `patterns/`. Important for humans, zero impact on code execution.

### 3. The Two-Layer Defense Model
*   **Layer 1: Robotic Scan (Gatekeeper):** A mechanical script (`pre_review_scan.sh`) that catches hardcoded paths, secrets, and silent errors. A single "FAIL" blocks the AI/Human review.
*   **Layer 2: Cognitive Audit:** AI Architects focus on architectural debt, logic edge cases, and "Inverse Test Analysis" (what do the tests *not* check?).

---

## 🧠 Part 2: Gemini 3 Flash Strategic Recommendations
*The Super Manager’s perspective on Continual Learning and High-Fidelity Infrastructure.*

### 1. The "Scar Tissue" Learning Loop (SLA)
Every failed review or discovered bug is a "Scar." We must turn it into a "Standard" within 24 hours.
*   **The 24h Update Rule:** If a new defect type is found (e.g., a missing path in a template), it must be added to the **Robotic Scan** and the **Checklist** within one business day.
*   **Regression Harnessing:** Every bug found must result in a **Reproducer Test** in CI. These tests are the "immune system" of the repo and are only retired with strategic sign-off.

### 2. Context-Aware "Mission Orders"
Stop using generic "Be Grumpy" prompts. Instead, use **Role-Play with Consequence**.
*   **The Prompt Anchor:** *"You are auditing the DNA of 30+ projects. A mistake here is 30 mistakes later."*
*   **Weighting:** This forces the model to increase its internal "Self-Correction" weights by establishing high stakes for the specific task.

### 3. The "Zero-Knowledge" Final Audit
Before a GitHub push, perform a **Clean Slate Audit**.
*   **The Test:** Give the repo to an agent or session with zero previous context.
*   **The Metric:** If they cannot understand the project's purpose, setup, and "How to Fix" within 5 minutes, the documentation is failing the "Bus Factor" test.

### 4. The "Cognitive vs. Robotic" Hybrid Compute
We must stop asking high-reasoning models (Claude Opus/Gemini Pro) to do "Robot Work" (finding `/Users/` paths).
*   **Efficiency:** Use cheap, fast local scripts for mechanical sweeps.
*   **Focus:** Save the expensive reasoning compute for **Logic Integrity**, **Scale Ramifications**, and **Dependency Drift Analysis.**

---

## 🛠️ Immediate Action Items
- [ ] **Task 1:** Finalize `scripts/pre_review_scan.sh` as the mandatory Gate 0.
- [ ] **Task 2:** Refactor `test_scripts_follow_standards.py` to `test_ecosystem_dna_integrity.py`, expanding scope to `templates/` and `.cursorrules`.
- [ ] **Task 3:** Establish the "Vault" protocol for the local `.env` record of API keys.

---
**Protocol Authorized by:** The Super Manager (Gemini 3 Flash)
**Strategic Alignment:** Infrastructure (Root)
