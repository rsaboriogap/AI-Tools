"""Tests for score_architecture.py"""
import json, subprocess, sys
from pathlib import Path

SCRIPT = Path("claude-skills/shared/scripts/score_architecture.py")

def run(p):
    out = subprocess.check_output([sys.executable, str(SCRIPT), str(p)])
    return json.loads(out)

def test_no_findings_perfect(tmp_path):
    f = tmp_path / "f.json"; f.write_text("[]")
    assert run(f)["overall"] == 5.0

def test_critical_zeroes_dimension(tmp_path):
    f = tmp_path / "f.json"
    f.write_text(json.dumps([{"dimension": "security", "severity": "Critical"}]))
    assert run(f)["scores"]["security"] == 0.0
