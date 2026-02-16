#!/usr/bin/env python3
"""Janitor Loop - Continuous health monitoring for all projects.

The Janitor monitors project health, checks cron freshness, runs healthcheck
commands, and creates Kanban cards for detected issues. Read-only operations only.
"""

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Add project-tracker to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "project-tracker"))
from scripts.config import DATABASE_PATH, PROJECTS_BASE_DIR
from scripts.db.manager import DatabaseManager

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config


class JanitorLoop:
    """Janitor autonomous loop for health monitoring."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.config = load_config()
        self.projects_root = Path(PROJECTS_BASE_DIR)
        self.loop_name = "janitor"
        
    def run(self):
        """Execute one iteration of the Janitor loop."""
        execution_id = self._record_start()
        cards_created = 0
        
        try:
            print(f"🧹 Janitor Loop starting at {datetime.now().isoformat()}")
            
            # Get all projects
            projects = self.db.get_all_projects()
            
            for project in projects:
                project_id = project["id"]
                tier = project.get("tier", 2)
                
                # Check if this project should be monitored this run
                if not self._should_monitor(tier):
                    continue
                
                print(f"  Checking {project_id} (Tier {tier})...")
                
                # Run health checks
                issues = []
                issues.extend(self._check_healthcheck(project))
                issues.extend(self._check_application_heartbeat(project))
                issues.extend(self._check_cron_freshness(project))
                issues.extend(self._check_dependencies(project))
                
                # Create cards for issues
                for issue in issues:
                    self._create_issue_card(project_id, issue)
                    cards_created += 1
            
            self._record_complete(execution_id, "success", cards_created)
            print(f"✅ Janitor Loop complete. Created {cards_created} cards.")
            
        except Exception as e:
            self._record_complete(execution_id, "failed", cards_created, str(e))
            print(f"❌ Janitor Loop failed: {e}")
            raise
    
    def _should_monitor(self, tier: int) -> bool:
        """Determine if a project should be monitored this run based on tier."""
        # For now, monitor all projects on every run
        # TODO: Implement tier-based scheduling
        return True
    
    def _check_healthcheck(self, project: Dict) -> List[Dict]:
        """Run healthcheck command and detect failures."""
        issues = []
        healthcheck_cmd = project.get("healthcheck_cmd")
        
        if not healthcheck_cmd or healthcheck_cmd == "echo 'No tests configured'":
            return issues
        
        project_path = self.projects_root / project["id"]
        
        # TODO: Actually run the healthcheck command
        # For now, just log that we would run it
        print(f"    Would run: {healthcheck_cmd}")
        
        return issues
    
    def _check_application_heartbeat(self, project: Dict) -> List[Dict]:
        """Check if deployed application is responding (replaces Healthchecks.io)."""
        issues = []
        project_id = project["id"]
        
        # Check if project has a heartbeat URL configured
        # This would be stored in project metadata or external_resources
        # For now, we'll check common patterns
        
        # Example: Check if there's a deployed URL
        # TODO: Read from EXTERNAL_RESOURCES.yaml or project metadata
        
        return issues
    
    def _check_cron_freshness(self, project: Dict) -> List[Dict]:
        """Check if cron jobs are running on schedule."""
        issues = []
        
        # Get cron jobs for this project
        cron_jobs = self.db.get_cron_jobs(project["id"])
        
        for job in cron_jobs:
            # TODO: Check last execution time vs schedule
            # For now, just log
            print(f"    Cron: {job['schedule']} - {job['command']}")
        
        return issues
    
    def _check_dependencies(self, project: Dict) -> List[Dict]:
        """Check for outdated or risky dependencies."""
        issues = []
        
        project_path = self.projects_root / project["id"]
        
        # Check for common dependency files
        dep_files = ["requirements.txt", "package.json", "Cargo.toml", "go.mod"]
        
        for dep_file in dep_files:
            if (project_path / dep_file).exists():
                print(f"    Found: {dep_file}")
                # TODO: Parse and check versions
        
        return issues
    
    def _create_issue_card(self, project_id: str, issue: Dict):
        """Create a Kanban card for a detected issue."""
        severity = issue.get("severity", "P2")
        title = issue.get("title", "Health check issue")
        details = issue.get("details", "")
        
        task_text = f"[Janitor] {title}"
        
        prompt = f"""## Overview
{details}

## Execution
Investigate and resolve the issue detected by the Janitor loop.

## Done Criteria
- [ ] Issue investigated
- [ ] Root cause identified
- [ ] Fix implemented or issue documented as expected behavior
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
    janitor = JanitorLoop()
    janitor.run()
