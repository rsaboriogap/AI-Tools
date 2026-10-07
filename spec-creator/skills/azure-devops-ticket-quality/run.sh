#!/bin/bash
# Wrapper script to run the ticket quality analyzer

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TICKET_ID="${1:-}"
ANALYSIS_JSON="${2:-}"

if [ -z "$TICKET_ID" ]; then
    echo "Error: Ticket ID is required" >&2
    echo "Usage: run.sh <ticket_id> [analysis_json_file]" >&2
    exit 1
fi

cd "$SKILL_DIR"
python3 analyzer.py "$TICKET_ID" "$ANALYSIS_JSON"
