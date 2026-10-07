#!/usr/bin/env python3
"""Deterministic scorecard from findings.json."""
import json, sys

WEIGHTS = {"security": 0.25, "scalability": 0.20, "maintainability": 0.20, "performance": 0.15, "availability": 0.10, "cost": 0.05, "documentation": 0.05}
PENALTY = {"Critical": 5, "High": 3, "Medium": 1, "Low": 0.3}

def score(findings, dim):
    base = 5.0
    for f in findings:
        if f.get("dimension") == dim:
            base -= PENALTY.get(f.get("severity"), 0)
    return max(0.0, round(base, 1))

def main(path):
    findings = json.load(open(path))
    dims = list(WEIGHTS.keys())
    scores = {d: score(findings, d) for d in dims}
    overall = round(sum(scores[d] * WEIGHTS[d] for d in dims), 2)
    print(json.dumps({"scores": scores, "weights": WEIGHTS, "overall": overall}, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
