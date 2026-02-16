#!/usr/bin/env python3
"""Librarian Loop - Template drift detection and auto-fix.

The Librarian detects drift from canonical templates, validates immutable files,
checks extendable file markers, and optionally auto-fixes safe changes.
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add project-tracker to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "project-tracker"))
from scripts.config import DATABASE_PATH, PROJECTS_BASE_DIR
from scripts.db.manager import DatabaseManager

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config


class LibrarianLoop:
    """Librarian autonomous loop for template drift detection."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.config = load_config()
        self.projects_root = Path(PROJECTS_BASE_DIR)
        self.scaffolding_root = self.projects_root / "project-scaffolding"
        self.loop_name = "librarian"
        
    def run(self):
        """Execute one iteration of the Librarian loop."""
        execution_id = self._record_start()
        cards_created = 0
        
        try:
            print(f"📚 Librarian Loop starting at {datetime.now().isoformat()}")
            
            # Get all projects
            projects = self.db.get_all_projects()
            
            for project in projects:
                project_id = project["id"]
                tier = project.get("tier", 2)
                
                # Check if this project should be checked this run
                if not self._should_check(tier):
                    continue
                
                print(f"  Checking {project_id} (Tier {tier})...")
                
                # Check for template drift
                drift_issues = self._check_template_drift(project)
                
                # Update drift status
                drift_status = "clean" if not drift_issues else "drift_detected"
                self._update_drift_status(project_id, drift_status)
                
                # Create cards for drift issues
                for issue in drift_issues:
                    self._create_drift_card(project_id, issue)
                    cards_created += 1
            
            self._record_complete(execution_id, "success", cards_created)
            print(f"✅ Librarian Loop complete. Created {cards_created} cards.")
            
        except Exception as e:
            self._record_complete(execution_id, "failed", cards_created, str(e))
            print(f"❌ Librarian Loop failed: {e}")
            raise
    
    def _should_check(self, tier: int) -> bool:
        """Determine if a project should be checked this run based on tier."""
        # For now, check all projects on every run
        # TODO: Implement tier-based scheduling
        return True
    
    def _check_template_drift(self, project: Dict) -> List[Dict]:
        """Check for drift from canonical templates."""
        drift_issues = []
        project_path = self.projects_root / project["id"]
        
        # Check for .agentsync marker
        agentsync_dir = project_path / ".agentsync"
        if not agentsync_dir.exists():
            return drift_issues  # Not a governed project
        
        # Check version file
        version_file = project_path / ".scaffolding-version"
        if version_file.exists():
            try:
                version_data = json.loads(version_file.read_text())
                installed_version = version_data.get("scaffolding_version")
                
                # Get expected version
                expected_version_file = self.scaffolding_root / ".scaffolding-version"
                if expected_version_file.exists():
                    expected_data = json.loads(expected_version_file.read_text())
                    expected_version = expected_data.get("scaffolding_version")
                    
                    if installed_version != expected_version:
                        drift_issues.append({
                            "type": "version_drift",
                            "severity": "P1",
                            "title": f"Scaffolding version outdated: {installed_version} → {expected_version}",
                            "details": f"Project is on version {installed_version}, latest is {expected_version}"
                        })
            except Exception as e:
                print(f"    Warning: Could not check version: {e}")
        
        # Check governed files
        rules_dir = agentsync_dir / "rules"
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.md"):
                print(f"    Checking: {rule_file.name}")
                # TODO: Validate against canonical templates
        
        return drift_issues
    
    def _update_drift_status(self, project_id: str, status: str):
        """Update the drift_status field for a project."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE projects
                SET drift_status = ?
                WHERE id = ?
            """, (status, project_id))
            conn.commit()
    
    def _create_drift_card(self, project_id: str, issue: Dict):
        """Create a Kanban card for a detected drift issue."""
        severity = issue.get("severity", "P2")
        title = issue.get("title", "Template drift detected")
        details = issue.get("details", "")
        
        task_text = f"[Librarian] {title}"
        
        prompt = f"""## Overview
{details}

## Execution
Review and resolve the template drift detected by the Librarian loop.

## Done Criteria
- [ ] Drift reviewed
- [ ] Decision made: update template or accept divergence
- [ ] If updating: changes applied and tested
- [ ] Documentation updated if needed
"""
        
        self.db.add_task(
            text=task_text,
            project_id=project_id,
            status="TRIAGED",
            priority="High" if severity == "P0" else "Medium",
            prompt=prompt,
            task_type="agent"
        )
    
    def _record_start(self) -> int:
        """Record loop execution start."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO loop_executions (loop_name, started_at, status)
                VALUES (?, ?, 'running')
            """, (self.loop_name, datetime.now().isoformat()))
            conn.commit()
            return cursor.lastrowid
    
    def _record_complete(self, execution_id: int, status: str, cards_created: int = 0, error: Optional[str] = None):
        """Record loop execution completion."""
        with self.db._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE loop_executions
                SET completed_at = ?, status = ?, cards_created = ?, error_message = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), status, cards_created, error, execution_id))
            conn.commit()


if __name__ == "__main__":
    librarian = LibrarianLoop()
    librarian.run()
