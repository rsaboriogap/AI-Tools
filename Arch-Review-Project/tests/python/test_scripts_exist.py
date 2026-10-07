"""Sanity: every declared script exists."""
from pathlib import Path

SCRIPTS = [
    "claude-skills/shared/scripts/detect_project_type.sh",
    "claude-skills/shared/scripts/scan_secrets.sh",
    "claude-skills/shared/scripts/score_architecture.py",
    "claude-skills/arch-review-structure/scripts/detect_dependencies.py",
]

def test_scripts_exist():
    for s in SCRIPTS:
        assert Path(s).exists(), f"missing {s}"
