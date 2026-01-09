# Cursor Configuration Best Practices

**Pattern:** Optimize Cursor AI assistant behavior through workspace-level configuration files

**Status:** ✅ Implemented across workspace

**Related:**
- `.cursorrules` - AI behavior and coding standards
- `.cursorignore` - Context window optimization

---

## The Problem

Without configuration, Cursor AI:
- Wastes context window reading `node_modules/`, `__pycache__/`, and other junk
- May not follow consistent markdown/documentation standards
- Lacks project-specific conventions and patterns

**Impact:** Slower responses, inconsistent output, wasted tokens on irrelevant files.

---

## The Solution

### 1. `.cursorrules` - Behavior Configuration

**Location:** `$PROJECTS_ROOT/.cursorrules`

**Purpose:** Tell Cursor how to behave in this workspace.

**Key Sections:**

#### Markdown & Documentation Standards
```markdown
## 📝 Markdown & Documentation Standards

### YAML Frontmatter (CRITICAL)
- **ALWAYS preserve YAML frontmatter** when editing `.md` files
- Use nested tags: #type/project, #tech/python/pandas, #status/active
```

**Why:** Ensures all markdown files follow Obsidian-compatible taxonomy system.

#### Context Window Management
```markdown
## 🚫 Context Window Management

**NEVER waste context on:**
- node_modules/, __pycache__/, .git/
- Use targeted reads with line ranges for large files
```

**Why:** Reminds AI to use efficient file reading strategies.

---

### 2. `.cursorignore` - File Filtering

**Location:** `$PROJECTS_ROOT/.cursorignore`

**Purpose:** Prevent Cursor from reading binary/junk files entirely.

**Pattern:**
```gitignore
# Dependencies & Packages
node_modules/
venv/
__pycache__/

# Python Bytecode
*.pyc
*.pyo

# Build Artifacts
dist/
build/

# OS Files
.DS_Store

# Logs
*.log

# Large Binary Files
*.pdf
*.zip
*.dmg

# Database Files (usually too large)
*.db
*.sqlite

# Machine Learning Models
*.pth
*.h5
```

**Why:** Prevents context window bloat from 100MB+ node_modules or model weights.

---

## Usage Guidelines

### When to Update `.cursorrules`

**Add rules when:**
1. You notice Cursor making the same mistake repeatedly
2. New project-wide standards are established
3. New documentation taxonomy is introduced
4. Specific file handling patterns emerge

**Example additions:**
```markdown
## Project-Specific Patterns

### File Safety (image-workflow)
- NEVER modify PNG/YAML files in-place
- Use move_file_with_all_companions() for file moves
- Use send2trash() for deletions
```

### When to Update `.cursorignore`

**Add patterns when:**
1. New large directories appear (data/raw/, logs/)
2. New build artifacts accumulate
3. Context window is slow/bloated

**Testing:**
```bash
# Check what Cursor can see
find . -type f | grep -v -f .cursorignore | head -20

# Verify ignore patterns work
ls -la node_modules/  # Should not appear in Cursor context
```

---

## Best Practices

### 1. Frontmatter Preservation (CRITICAL)

**Rule in `.cursorrules`:**
```markdown
- **ALWAYS preserve YAML frontmatter** when editing `.md` files
```

**Why:** Without this, Cursor might accidentally delete frontmatter when editing markdown, breaking Obsidian taxonomy.

**Enforcement:** Remind Cursor in every markdown edit request if needed.

---

### 2. Nested Tag Taxonomy

**Rule in `.cursorrules`:**
```markdown
- Use **nested tags** for hierarchy: #type/project, #tech/python/pandas
```

**Why:** Enables powerful Obsidian Dataview queries:
```dataview
LIST FROM #tech/python/fastapi WHERE #status/active
```

---

### 3. Context Window Efficiency

**Rule in `.cursorrules`:**
```markdown
- Use targeted reads with line ranges for large files
- Prefer codebase_search over reading entire files
```

**Rule in `.cursorignore`:**
```gitignore
node_modules/
__pycache__/
*.log
```

**Why:** Keeps Cursor fast and focused on relevant code.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: No Configuration

**Problem:**
```
No .cursorrules or .cursorignore
↓
Cursor reads 500MB node_modules/
↓
Slow responses, wasted context
```

**Solution:** Create both files at workspace root.

---

### ❌ Anti-Pattern 2: Too Many Rules

**Problem:**
```markdown
.cursorrules with 50+ specific rules for every edge case
↓
Cursor ignores most rules (too long)
↓
Ineffective configuration
```

**Solution:** Focus on top 5-10 most important patterns. Use project-specific `.cursorrules` in subdirectories for detailed rules.

---

### ❌ Anti-Pattern 3: Ignoring Too Much

**Problem:**
```gitignore
*.py  # Ignore all Python files!
```

**Solution:** Only ignore junk, not source code. Test with `find` command.

---

## Project-Specific Configuration

Some projects need custom rules. Place `.cursorrules` in project directory:

**Example: `image-workflow/.cursorrules`**
```markdown
# image-workflow Cursor Rules

## 🚨 CRITICAL FILE SAFETY RULES

### Rule #1: NO FILE CONTENT MODIFICATIONS
- NEVER modify image files (PNG, JPG) in-place
- NEVER modify companion files (YAML, txt) in-place
- Exception: 04_desktop_multi_crop.py may write cropped PNG files

### Rule #2: File Operations Allowed
✅ Moving files: move_file_with_all_companions()
✅ Deleting files: send2trash()
✅ Reading files: Path.read_text()

❌ open(file, 'w') on existing PNG/YAML
❌ PIL.Image.save() overwriting existing files
```

**Why:** image-workflow has strict safety requirements not applicable to other projects.

---

## Template

**New Project `.cursorrules` Template:**

```markdown
# [Project Name] Cursor Rules

## Markdown Standards
- Preserve YAML frontmatter
- Use nested tags: #p/[project_name]

## Project-Specific Patterns
- [Add patterns specific to this project]

## Context Window
- Prefer targeted reads for large files
- Use codebase_search for exploration
```

**New Project `.cursorignore` Template:**

```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build Artifacts
dist/
build/

# OS Files
.DS_Store

# Logs
*.log
```

---

## Verification

**Check if rules are working:**

1. **Test frontmatter preservation:**
   - Edit a markdown file with Cursor
   - Verify YAML frontmatter remains intact

2. **Test ignore patterns:**
   ```bash
   # Should see no node_modules in context
   cursor --list-files | grep node_modules
   ```

3. **Test context efficiency:**
   - Measure response time before/after `.cursorignore`
   - Should be faster with proper ignores

---

## Resources

- **Cursor Documentation:** https://cursor.sh/docs
- **Related Patterns:**
  - `project-scaffolding/Documents/CODE_QUALITY_STANDARDS.md`
  - `project-scaffolding/templates/00_Index_Template.md`

---

## Summary

**Do this for every new project:**
1. Copy `.cursorrules` and `.cursorignore` from workspace root
2. Customize with project-specific patterns
3. Test with a few AI-assisted edits
4. Update as patterns emerge

**Result:** Faster, more consistent AI assistance with proper context management.

---

*Last Updated: 2025-12-31*  
*Pattern Status: ✅ Implemented*  
*Projects Using This: All (workspace-level)*

