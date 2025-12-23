# Kiro Deep Dive - Complete Guide

> **Purpose:** Master Kiro for Tier 1 architecture work and project planning

**Last Updated:** December 23, 2025

---

## 🎯 **What Makes Kiro Different**

Kiro is **NOT** a code editor like Cursor. It's a **spec-driven development system** built on four pillars:

1. **SPECS** - Structured project planning (requirements, tasks, design)
2. **AGENT STEERING** - Configure AI behavior and coding standards
3. **AGENT HOOKS** - Automate repetitive tasks with triggers
4. **MCP SERVERS** - Connect external tools and data sources

---

## 📁 **Kiro's File Structure**

Kiro stores project-specific data in `.kiro/` directories within your project:

```
project-root/
  .kiro/
    specs/
      feature-name/
        requirements.md  # What needs to be built
        design.md        # How it will be built
        tasks.md         # Step-by-step implementation plan
        summary.md       # Overview and status
    steering/
      product.md         # Product principles and constraints
      structure.md       # Code structure and organization
      tech.md            # Technical standards and patterns
    hooks/               # Automation triggers (future)
```

**Key Insight:** These are **markdown files** that can be version controlled, edited programmatically, and used across teams!

---

## 🔧 **CLI vs GUI Capabilities**

### ✅ **Available via CLI**

| Feature | Command | Use Case |
|---------|---------|----------|
| **Chat** | `kiro-cli chat --no-interactive "prompt"` | One-off architecture questions |
| **Chat with Agent** | `kiro-cli chat --agent my_agent "prompt"` | Use custom agent config |
| **Agent Management** | `kiro-cli agent list/create/edit` | Manage custom agents |
| **MCP Management** | `kiro-cli mcp add/list/status` | Connect external tools |

### ❌ **GUI-Only (For Now)**

| Feature | Workaround |
|---------|------------|
| **SPECS Creation** | Create `.kiro/specs/` directories manually, Kiro will recognize them |
| **AGENT STEERING** | Create `.kiro/steering/*.md` files manually |
| **AGENT HOOKS** | Not yet implemented (coming soon?) |

---

## 📋 **Kiro Workflow for Tier 1 Tasks**

### **Phase 1: Project Setup (One-time)**

1. **Create `.kiro` directory structure:**
```bash
mkdir -p .kiro/specs .kiro/steering
```

2. **Write Product Steering** (`.kiro/steering/product.md`):
```markdown
# Product Name - Product Overview

## What It Is
[Brief description]

## What It Does
- [Feature 1]
- [Feature 2]

## What It Does NOT Do
- [Anti-feature 1]

## Target User
[Who is this for?]

## Core Principles
- [Principle 1]
- [Principle 2]
```

3. **Write Technical Steering** (`.kiro/steering/tech.md`):
```markdown
# Technical Standards

## Language & Framework
- Python 3.11+
- Modern typing (dict, list, str | None)

## Architecture Patterns
- Layer-by-layer development
- Privacy-first (local data, API for processing only)

## Code Style
- [Your standards]

## Safety Rules
- Never modify source data in-place
- All changes must be reversible
```

---

### **Phase 2: Feature Planning (Per Feature)**

1. **Create Spec Directory:**
```bash
mkdir -p .kiro/specs/feature-name
```

2. **Write Requirements** (`.kiro/specs/feature-name/requirements.md`):
```markdown
# Feature Requirements

## Functional Requirements
1. User must be able to...
2. System must...

## Non-Functional Requirements
1. Performance: < 60s for 10k records
2. Memory: < 500MB

## Constraints
- Must work offline
- No external dependencies
```

3. **Write Design** (`.kiro/specs/feature-name/design.md`):
```markdown
# Architecture Design

## High-Level Approach
[Architectural decision]

## Components
1. Component A: [Purpose]
2. Component B: [Purpose]

## Data Flow
[How data moves through system]

## Edge Cases
1. [Edge case 1]
2. [Edge case 2]
```

4. **Generate Tasks** (`.kiro/specs/feature-name/tasks.md`):
```bash
# Use Kiro to generate from requirements + design
kiro-cli chat --no-interactive "Based on the requirements in .kiro/specs/feature-name/requirements.md and design in design.md, create a detailed task breakdown in tasks.md format"
```

**OR** manually structure:
```markdown
# Implementation Plan

- [ ] 1. Setup infrastructure
  - [ ] 1.1 Install dependencies
  - [ ] 1.2 Create directory structure
  - _Requirements: 1.1, 1.2_

- [ ] 2. Implement core logic
  - [ ] 2.1 Build Component A
  - [ ] 2.2 Build Component B
  - _Requirements: 2.1, 2.2_

- [ ] 3. Checkpoint - Test integration
```

---

### **Phase 3: Execution (Handoff to Tier 2/3)**

**Option A: Use Kiro Chat**
```bash
# Kiro will automatically read .kiro/specs/ and .kiro/steering/
kiro-cli chat --no-interactive "Implement task 2.1 from tasks.md"
```

**Option B: Use DeepSeek/Cursor**
- Open `.kiro/specs/feature-name/tasks.md`
- Copy specific task
- Pass to Tier 2/3 AI with context:
  ```
  Context: See .kiro/steering/ for coding standards
  Specs: See .kiro/specs/feature-name/ for requirements
  Task: Implement [task description]
  ```

---

## 🤖 **Custom Agents**

Agents are **reusable AI configurations** with specific behaviors.

### **List Available Agents**
```bash
kiro-cli agent list
```

**Output:**
```
* kiro_default    (Built-in)
  kiro_planner    (Built-in)
```

### **Create Custom Agent**
```bash
kiro-cli agent create --name architecture_reviewer --from kiro_default
```

This creates a config file that you can edit to customize:
- System prompts
- Temperature settings
- Context providers
- Behavior rules

### **Use Custom Agent**
```bash
kiro-cli chat --agent architecture_reviewer "Review this design for flaws"
```

---

## 🔌 **MCP Servers (Model Context Protocol)**

MCP servers give Kiro access to **external tools and data** like:
- Database connections
- File systems
- APIs
- Git repositories

### **List MCP Servers**
```bash
kiro-cli mcp list
```

### **Add MCP Server**
```bash
kiro-cli mcp add --name postgres_dev --type database --config config.json
```

### **Check Status**
```bash
kiro-cli mcp status postgres_dev
```

**Use Case:** Kiro can query your actual database, read real files, or call APIs **during architecture planning**.

---

## 💡 **Programmatic Workflow**

### **Automated Spec Generation**

```python
#!/usr/bin/env python3
"""Generate Kiro specs from project description"""

import subprocess
import os
from pathlib import Path

def generate_kiro_specs(project_root: str, feature_name: str, description: str):
    """Generate Kiro spec files programmatically"""
    
    # Create directories
    spec_dir = Path(project_root) / ".kiro" / "specs" / feature_name
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate requirements using Kiro
    prompt = f"""
    Feature: {feature_name}
    Description: {description}
    
    Generate a comprehensive requirements.md document in the format used by Kiro specs.
    Include functional requirements, non-functional requirements, and constraints.
    """
    
    result = subprocess.run(
        ["/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli", "chat", "--no-interactive", prompt],
        capture_output=True,
        text=True
    )
    
    # Save to file
    (spec_dir / "requirements.md").write_text(result.stdout)
    
    # Generate design from requirements
    prompt2 = f"""
    Based on the requirements in {spec_dir}/requirements.md, generate a design.md document.
    Include high-level architecture, components, data flow, and edge cases.
    """
    
    result2 = subprocess.run(
        ["/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli", "chat", "--no-interactive", prompt2],
        capture_output=True,
        text=True
    )
    
    (spec_dir / "design.md").write_text(result2.stdout)
    
    print(f"✅ Generated specs for {feature_name} in {spec_dir}")

# Usage
generate_kiro_specs(
    project_root="/Users/eriksjaastad/projects/my-project",
    feature_name="user-authentication",
    description="JWT-based auth with refresh tokens"
)
```

---

## 🎯 **Integration with Our Tiered System**

### **Tier 1 (Kiro): Architecture & Planning**

**Inputs:**
- Project vision
- High-level requirements

**Kiro's Job:**
1. Create `.kiro/steering/` (product principles, tech standards)
2. Create `.kiro/specs/feature-name/` (requirements, design, tasks)
3. Review architecture for flaws (via `kiro-cli chat`)

**Outputs:**
- Structured specs ready for Tier 2/3
- Task breakdown with dependencies
- Architecture diagrams (if using MCP with drawing tools)

### **Tier 2/3 (DeepSeek/Cursor): Implementation**

**Inputs:**
- `.kiro/specs/feature-name/tasks.md` (specific task)
- `.kiro/steering/` (coding standards)

**Their Job:**
- Implement the task
- Follow steering docs
- Mark task complete in tasks.md

---

## 📊 **Kiro vs Cursor: When to Use What**

| Task | Tool | Why |
|------|------|-----|
| Define product vision | **Kiro GUI** | Structured planning UI |
| Break down features | **Kiro CLI** | Generate specs from requirements |
| Review architecture | **Kiro CLI** | Use for document reviews |
| Write code | **Cursor** | Best for actual coding |
| Refactor code | **Cursor** | Best for code manipulation |
| Debug issues | **Cursor** | Better context of codebase |

---

## 🔥 **Next Steps for Project Scaffolding**

1. **Create Kiro Spec Templates** in `project-scaffolding/templates/.kiro/`
2. **Document Steering Patterns** (what goes in product.md, tech.md, structure.md)
3. **Build Automation Scripts** to generate specs programmatically
4. **Integrate with Review System** (use Kiro for Tier 1 architecture reviews)
5. **Test on Real Project** (dogfood on a new feature)

---

## 📝 **Example: Real Tax Organizer Spec**

**Product Steering** (from your Kiro):
```markdown
# Tax Organizer - Product Overview

## What It Is
A personal tax organization tool for classifying transactions and generating CPA reports.

## Core Principles
- **Categorization + reporting tool**, not an accounting system
- **Surfaces possibilities** for CPA review, doesn't make tax conclusions
- Treats source CSVs as immutable - never re-save after import
```

**Task Breakdown** (from your Kiro):
```markdown
- [ ] 1. Set up testing infrastructure
  - [ ] 1.1 Install testing dependencies
  - [ ] 1.2 Create test directory structure
  - [ ] 1.3 Configure pytest and coverage
  - _Requirements: 1.2, 1.3, 2.5_
```

This is **exactly** the format we want for Tier 1 → Tier 2/3 handoffs!

---

## 🚀 **Bottom Line**

**Kiro is programmable!** 

- **CLI works** for chat, agents, MCP
- **File structure is standard** (`.kiro/specs/`, `.kiro/steering/`)
- **Can be automated** via Python scripts
- **Can be version controlled** (git commit `.kiro/`)
- **Integrates with our workflow** (Tier 1 planning → Tier 2/3 execution)

**We can absolutely use Kiro programmatically AND through the GUI depending on the task!**

---

**Status:** Ready to integrate into project-scaffolding templates! 🎉

