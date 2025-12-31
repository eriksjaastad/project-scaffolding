# Pattern: Single Source of Truth (SSOT) via YAML

**Status:** Proven Pattern (Dec 31, 2025)
**Context:** Managing data that is "too small for a database but too structured for Markdown."

---

## The Problem
When information needs to be both **human-readable** and **machine-parseable**, Markdown leads to brittle regex parsing and manual updates across multiple files. This results in "documentation theater" where data exists but isn't actionable or accurate.

## The Solution
Use **YAML** as the single source of truth for cross-project data tracking.

### Why YAML?
- **Human-Readable:** Easy to edit and understand without special tools.
- **Machine-Parseable:** Native support in almost every language (Python, JS, Go).
- **Hierarchical:** Can represent complex relationships (projects -> services -> costs).
- **Comments Support:** Unlike JSON, YAML allows documenting *why* a piece of data exists.

---

## Implementation Rules

### 1. Single Source of Truth (SSOT)
Never maintain the same data in two places. If data is in a YAML file, it is the **authoritative source**. If a Markdown summary is needed, it should be generated from the YAML, not manually updated.

### 2. File Naming
Use `.yaml` as the extension (not `.yml`).
- Example: `EXTERNAL_RESOURCES.yaml`

### 3. Structure over Prose
Keep keys consistent across entries. Use lists and dictionaries for data, and reserved `notes` or `comments` keys for descriptive text.

### 4. Integration with Dashboard
Data in YAML format is specifically intended to be ingested by automated tools (like `project-tracker` or `dashboard`) to provide real-time alerts and visualization.

---

## Example: External Resources
Instead of a 500-line Markdown table, use a structured YAML list:

```yaml
projects:
  trading-projects:
    monthly_cost: 12
    services:
      - name: Railway
        purpose: "hosting + Postgres"
        type: hosting
        cost: 5
```

---

## When to Use
- **External Resource Tracking:** APIs, Hosting, Databases.
- **Configuration:** Project-wide settings that multiple agents need to read.
- **Metadata:** Project status, technology stacks, team members.
- **Pricing/Costs:** Tracking AI model costs and budgets.

## When NOT to Use
- **Prose Documentation:** Use Markdown for high-level "why" and philosophy.
- **Large Datasets:** Use SQLite or Postgres if you have >1000 records.
- **Sensitive Secrets:** Use `.env` or a Secret Manager; never commit YAML with secrets to Git.

---

## Scars
- **The "Broken Regex" Scar:** Trying to parse Markdown tables with regex led to silent failures in cost tracking when a single character changed.
- **The "Dual Update" Scar:** Updating a Markdown doc and forgetting to update the DB led to conflicting realities. YAML SSOT prevents this.

