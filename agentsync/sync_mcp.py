#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
MCP Config Sync

Generates tool-specific MCP configuration files from a single source of truth.

Source: _configs/mcp/servers.json + _configs/mcp/tools/*.json
Targets:
  - Claude Code: ~/.claude/claude_desktop_config.json
  - Antigravity: ~/.gemini/antigravity/mcp_config.json

Usage:
  uv run sync_mcp.py           # Sync all tools
  uv run sync_mcp.py claude    # Sync Claude only
  uv run sync_mcp.py --dry-run # Preview without writing
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# Self-locate: script is at project-scaffolding/agentsync/sync_mcp.py
SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent
PROJECTS_ROOT = SCAFFOLDING_ROOT.parent
TOOLS_ROOT = PROJECTS_ROOT / "_tools"  # MCP servers still live here
CONFIGS_ROOT = PROJECTS_ROOT / "_configs"


# Output locations for each tool
TOOL_OUTPUTS = {
    "claude": Path.home() / ".claude" / "claude_desktop_config.json",
    "antigravity": Path.home() / ".gemini" / "antigravity" / "mcp_config.json",
}


def expand_variables(value: Any, variables: dict[str, str]) -> Any:
    """Recursively expand ${VAR} references in strings."""
    if isinstance(value, str):
        # Replace ${VAR} patterns
        def replace_var(match):
            var_name = match.group(1)
            return variables.get(var_name, match.group(0))
        return re.sub(r'\$\{(\w+)\}', replace_var, value)
    elif isinstance(value, dict):
        return {k: expand_variables(v, variables) for k, v in value.items()}
    elif isinstance(value, list):
        return [expand_variables(item, variables) for item in value]
    return value


def load_servers_config() -> dict:
    """Load the master servers.json file."""
    servers_file = CONFIGS_ROOT / "mcp" / "servers.json"
    if not servers_file.exists():
        print(f"Error: {servers_file} not found", file=sys.stderr)
        sys.exit(1)

    with open(servers_file) as f:
        return json.load(f)


def load_tool_config(tool_name: str) -> dict | None:
    """Load tool-specific config (e.g., claude.json)."""
    tool_file = CONFIGS_ROOT / "mcp" / "tools" / f"{tool_name}.json"
    if not tool_file.exists():
        return None

    with open(tool_file) as f:
        return json.load(f)


def generate_mcp_config(tool_name: str, servers_config: dict, tool_config: dict) -> dict:
    """Generate the MCP config for a specific tool."""
    # Build variable map
    variables = {
        "PROJECTS_ROOT": str(PROJECTS_ROOT),
        "TOOLS_ROOT": str(TOOLS_ROOT),
    }

    # Get enabled servers
    enabled = tool_config.get("enabled", [])
    name_mapping = tool_config.get("nameMapping", {})
    overrides = tool_config.get("overrides", {})

    mcp_servers = {}

    for server_id in enabled:
        if server_id not in servers_config.get("servers", {}):
            print(f"Warning: Server '{server_id}' not found in servers.json", file=sys.stderr)
            continue

        server_def = servers_config["servers"][server_id].copy()

        # Remove description (not needed in output)
        server_def.pop("description", None)

        # Apply tool-specific overrides
        if server_id in overrides:
            for key, value in overrides[server_id].items():
                if key == "env" and "env" in server_def:
                    server_def["env"].update(value)
                else:
                    server_def[key] = value

        # Expand variables
        server_def = expand_variables(server_def, variables)

        # Apply name mapping
        output_name = name_mapping.get(server_id, server_id)
        mcp_servers[output_name] = server_def

    return {"mcpServers": mcp_servers}


def sync_tool(tool_name: str, dry_run: bool = False) -> bool:
    """Sync MCP config for a specific tool."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Syncing {tool_name}...")

    servers_config = load_servers_config()
    tool_config = load_tool_config(tool_name)

    if not tool_config:
        print(f"  No config found for {tool_name}, skipping")
        return True

    output_path = TOOL_OUTPUTS.get(tool_name)
    if not output_path:
        print(f"  Unknown output path for {tool_name}", file=sys.stderr)
        return False

    # Generate config
    mcp_config = generate_mcp_config(tool_name, servers_config, tool_config)

    # Format output
    output_json = json.dumps(mcp_config, indent=2)

    if dry_run:
        print(f"  Would write to: {output_path}")
        print(f"  Content preview:\n{output_json[:500]}...")
        return True

    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if content changed
    if output_path.exists():
        with open(output_path) as f:
            existing = f.read()
        if existing == output_json + "\n":
            print(f"  {output_path} is already up to date")
            return True

    # Write output
    with open(output_path, "w") as f:
        f.write(output_json)
        f.write("\n")

    print(f"  Wrote: {output_path}")
    print(f"  Servers: {', '.join(mcp_config['mcpServers'].keys())}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync MCP configurations from single source of truth")
    parser.add_argument("tools", nargs="*", help="Specific tools to sync (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--list", action="store_true", help="List available tools")

    args = parser.parse_args()

    if args.list:
        print("Available tools:")
        for tool in TOOL_OUTPUTS.keys():
            tool_file = CONFIGS_ROOT / "mcp" / "tools" / f"{tool}.json"
            status = "configured" if tool_file.exists() else "no config"
            print(f"  {tool}: {status}")
        return

    # Determine which tools to sync
    tools_to_sync = args.tools if args.tools else list(TOOL_OUTPUTS.keys())

    print(f"MCP Config Sync")
    print(f"Source: {CONFIGS_ROOT / 'mcp'}")
    print(f"Tools: {', '.join(tools_to_sync)}")

    success = True
    for tool in tools_to_sync:
        if tool not in TOOL_OUTPUTS:
            print(f"\nUnknown tool: {tool}", file=sys.stderr)
            success = False
            continue
        if not sync_tool(tool, dry_run=args.dry_run):
            success = False

    print()
    if success:
        print("MCP sync complete!")
    else:
        print("MCP sync completed with errors", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
