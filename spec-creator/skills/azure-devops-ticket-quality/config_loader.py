#!/usr/bin/env python3
"""
Load configuration from .claude/settings.json for the azure-devops-ticket-quality skill.
"""

import json
import os
from pathlib import Path


def load_settings():
    """Load settings from .claude/settings.json."""
    # Look for settings.json in .claude directory
    possible_paths = [
        Path(".claude/settings.json"),
        Path(".") / ".claude" / "settings.json",
    ]

    # Also check parent directories up to 3 levels
    current = Path.cwd()
    for _ in range(3):
        possible_paths.append(current / ".claude" / "settings.json")
        current = current.parent

    for path in possible_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                continue

    return {}


def get_default_project():
    """Get the default Azure DevOps project from settings."""
    settings = load_settings()
    config = settings.get("azureDevOpsTicketQuality", {})
    return config.get("defaultProject")


def get_config():
    """Get the full azureDevOpsTicketQuality config section."""
    settings = load_settings()
    return settings.get("azureDevOpsTicketQuality", {})


if __name__ == "__main__":
    project = get_default_project()
    if project:
        print(f"Default project: {project}")
    else:
        print("No default project configured")

    config = get_config()
    if config:
        print(f"Configuration: {json.dumps(config, indent=2)}")
