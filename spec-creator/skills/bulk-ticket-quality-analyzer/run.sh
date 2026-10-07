#!/bin/bash
# Bulk Ticket Quality Analyzer wrapper
# Aggregates all ticket-quality-*.json reports and generates portfolio insights

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

python3 analyzer.py
