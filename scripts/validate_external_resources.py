#!/usr/bin/env python3
"""
Validates EXTERNAL_RESOURCES.yaml against a Pydantic schema.
Ensures cost tracking consistency and prevents typos in YAML keys.
"""

import sys
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class Service(BaseModel):
    name: str
    purpose: str
    service_type: str = Field(..., alias="type")
    cost: Union[float, int, str]

class Project(BaseModel):
    monthly_cost: Union[float, int, str]
    services: List[Service] = []
    aliases: Optional[List[str]] = None
    notes: Optional[str] = None

class ExternalResources(BaseModel):
    metadata: Dict[str, str]
    projects: Dict[str, Project]
    services_by_function: Dict[str, List[str]]
    api_key_pattern: Dict[str, Union[str, List[str]]]
    cost_summary: Dict[str, Union[float, int]]
    rejected_services: List[Dict] = []
    cancelled_accounts: List[Dict] = []
    action_items: Dict[str, List[str]]
    emergency_response: List[str]
    before_adding_service: Dict[str, Union[List[str], Dict[str, List[str]]]]
    security: Dict[str, List[str]]
    recent_changes: List[Dict[str, str]]

def validate_yaml(yaml_path: Path) -> bool:
    """Validates the YAML file against the ExternalResources schema."""
    if not yaml_path.exists():
        logger.error(f"File not found: {yaml_path}")
        return False

    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Validate using Pydantic
        ExternalResources(**data)
        logger.info("EXTERNAL_RESOURCES.yaml is valid.")
        return True

    except yaml.YAMLError as e:
        logger.error(f"YAML Parsing Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Validation Error:\n{e}")
        return False

if __name__ == "__main__":
    yaml_file = Path("EXTERNAL_RESOURCES.yaml")
    success = validate_yaml(yaml_file)
    sys.exit(0 if success else 1)

