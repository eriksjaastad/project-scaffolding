# Kiro CLI Integration Plan

> **Decision Date:** December 22, 2025  
> **Reason:** Cost savings (80-90% reduction on Tier 1 tasks)

---

## Why Kiro?

**Cost Analysis:**
- **Current:** Tier 1 tasks via Cursor/APIs = ~$180/month (30% of $600 total)
- **With Kiro:** $19/month for 1,000 interactions
- **Savings:** ~$160/month = ~$2,000/year on Tier 1 alone

**What Kiro Provides:**
- Access to Claude Sonnet 4/4.5 (top-tier architecture model)
- Spec-driven workflow (forces requirements.md + design.md)
- CLI integration (we can script it via subprocess)
- 1,000 interactions/month included ($19/mo when out of preview)

**What We're NOT Getting:**
- ❌ REST API or Python SDK (it's a CLI tool)
- ❌ Real-time cost tracking via API
- ❌ Flexibility (rigid spec-driven workflow)

**Trade-off:** Rigidity is acceptable for Tier 1. We WANT architecture to be spec-driven!

---

## Integration Architecture

### Tier 1 Task Flow

```
User/System defines task
    ↓
Python script creates spec file (requirements.md)
    ↓
Script calls Kiro CLI via subprocess
    ↓
Kiro generates:
  - design.md
  - Code files (writes to disk)
  - Tests
    ↓
Script reads created files
    ↓
Script commits changes
    ↓
Updates task status (1 interaction used)
```

### Code Example

```python
# scaffold/kiro.py

import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class KiroTask:
    id: str
    description: str
    requirements: str
    output_dir: Path

@dataclass
class KiroResult:
    created_files: List[Path]
    design_doc: Path
    interaction_cost: float
    stdout: str
    stderr: str

class KiroExecutor:
    """Execute Tier 1 tasks via Kiro CLI"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.specs_dir = project_root / "specs"
        self.specs_dir.mkdir(exist_ok=True)
        self.interactions_used = 0
        self.max_interactions = 1000
    
    def execute(self, task: KiroTask) -> KiroResult:
        """Execute a Tier 1 task"""
        # Create spec file
        spec_file = self.specs_dir / f"{task.id}_requirements.md"
        spec_file.write_text(task.requirements)
        
        # Ensure output directory exists
        task.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Call Kiro CLI
        cmd = [
            "kiro", "run",
            "--spec", str(spec_file),
            "--task", task.description,
            "--output", str(task.output_dir)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Kiro CLI failed: {result.stderr}")
        
        # Increment interaction count
        self.interactions_used += 1
        
        # Find created files
        created_files = list(task.output_dir.rglob("*.py"))
        design_doc = task.output_dir / "design.md"
        
        return KiroResult(
            created_files=created_files,
            design_doc=design_doc,
            interaction_cost=0.019,  # $19/1000
            stdout=result.stdout,
            stderr=result.stderr
        )
    
    def get_remaining_interactions(self) -> int:
        """How many interactions left this month"""
        return self.max_interactions - self.interactions_used
    
    def get_cost_estimate(self) -> float:
        """Estimated cost so far"""
        return self.interactions_used * 0.019
```

### CLI Integration

```bash
# Add to scaffold CLI
scaffold dispatch --tier 1 --task "Implement user authentication"

# Internally routes to Kiro CLI
# User sees:
┌─────────────────────────────────────────────┐
│ Tier 1 Task: Implement user authentication │
│ Method: Kiro CLI                            │
│ Cost: $0.019 (1 interaction)                │
│ Remaining: 999/1000 interactions            │
└─────────────────────────────────────────────┘

⠋ Running Kiro CLI...
✓ Spec created: specs/t1-001_requirements.md
✓ Kiro generated: design.md
✓ Kiro generated: src/auth.py
✓ Kiro generated: tests/test_auth.py

Files created: 3
Interaction cost: $0.019
Total cost this month: $0.47 (25 interactions used)
```

---

## What Tasks Go to Kiro? (Tier 1 Criteria)

**YES - Route to Kiro:**
- Project scaffolding (initial structure)
- Architecture design (how components interact)
- Complex algorithm design (needs thinking)
- Database schema design
- API design (endpoints, contracts)
- Security implementation (auth, permissions)

**NO - Use APIs instead (Tier 2/3):**
- Simple bug fixes
- Documentation updates
- Boilerplate generation
- Quick refactors
- UI tweaks

**Rule of thumb:** If it needs a `requirements.md` and `design.md`, use Kiro. Otherwise, use APIs.

---

## Cost Tracking

**Kiro's Credit System:**
- 1,000 interactions/month ($19/mo when out of preview)
- Each "run" = 1 interaction
- Kiro IDE shows: "850/1000 credits remaining"
- **No API to query this programmatically**

**Our Tracking:**
```python
# Track manually in our system
kiro_executor.interactions_used  # 25
kiro_executor.get_remaining_interactions()  # 975
kiro_executor.get_cost_estimate()  # $0.475
```

**Monthly reset:** Interactions reset on billing cycle (1st of month)

---

## Setup Instructions

### 1. Install Kiro CLI

```bash
# Visit kiro.dev and sign up
# Download Kiro IDE (includes CLI)
# Or install CLI separately (if available)

# Verify installation
kiro --version
```

### 2. Authenticate

```bash
# Kiro uses AWS Builder ID
aws sso login

# Verify Kiro can access
kiro auth status
```

### 3. Test Kiro CLI

```bash
# Create a simple spec
cat > test_spec.md << EOF
# Requirements: Hello World API
- Create a simple Flask API
- Endpoint: GET /hello returns {"message": "Hello World"}
- Include tests
EOF

# Run Kiro
kiro run --spec test_spec.md --task "Create Hello World API" --output ./test_output

# Check results
ls test_output/
# Should see: design.md, app.py, tests/
```

### 4. Integrate into scaffold

```python
# Add to scaffold/kiro.py (code above)
# Add to scaffold/dispatch.py:

from scaffold.kiro import KiroExecutor

if task.tier == 1:
    kiro = KiroExecutor(project_root)
    result = kiro.execute(task)
    return result
```

---

## Limitations & Workarounds

### Limitation 1: No JSON Response

**Problem:** Kiro writes files, doesn't return JSON/text  
**Workaround:** Read files it creates from disk

### Limitation 2: Rigid Spec Workflow

**Problem:** Can't just ask "fix this bug" - it wants a spec  
**Workaround:** Only use for Tier 1. Use APIs for quick fixes.

### Limitation 3: No Real-Time Cost API

**Problem:** Can't query "how much did this cost" via API  
**Workaround:** Track interactions manually (1 run = $0.019)

### Limitation 4: AWS Auth Required

**Problem:** Needs AWS Builder ID session  
**Workaround:** Run `aws sso login` before automation, or use long-lived tokens on server

---

## Migration Plan

### Phase 1: Test Locally (This Week)
- [ ] Install Kiro CLI
- [ ] Test with simple task
- [ ] Verify output quality
- [ ] Check interaction usage

### Phase 2: Build Integration (Week 1)
- [ ] Create `scaffold/kiro.py`
- [ ] Add subprocess execution
- [ ] Add cost tracking
- [ ] Test with real Tier 1 task

### Phase 3: Production Use (Week 2+)
- [ ] Route all Tier 1 tasks to Kiro
- [ ] Monitor cost savings
- [ ] Compare quality vs API results
- [ ] Adjust if needed

---

## Success Metrics

**Cost:**
- Target: <$20/month on Tier 1 (vs $180 current)
- Actual: Track via `kiro_executor.get_cost_estimate()`

**Quality:**
- Compare Kiro output vs API output
- Track: Did Kiro specs catch issues early?
- Measure: Fewer bugs in Tier 1 code?

**Usage:**
- Track: Interactions per month
- Alert: If >900 interactions (approaching limit)
- Decision: If consistently hitting limit, evaluate $39/mo tier (3,000 interactions)

---

## Antigravity: DROPPED

**Decision:** Do not integrate Antigravity.

**Why:**
- No CLI, no API (GUI only)
- No cost savings (uses Gemini 3 API under hood)
- Just another IDE (we have Cursor)
- Browser Agent is cool but we can build with Playwright + Gemini Vision if needed

**Verdict:** Not worth the complexity. Skip entirely.

---

**Status:** Ready to test Kiro CLI  
**Next:** Install Kiro, run test task, evaluate output quality  
**Timeline:** Test this week, integrate Week 1 of 2026

