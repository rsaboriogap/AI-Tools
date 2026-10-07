#!/bin/bash
# Wrapper script to save evaluation results automatically
# Usage: save_result.sh <evaluation_id>
# Reads JSON from stdin

EVAL_ID="${1:-eval-$(date +%s)}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create documents directory if it doesn't exist
mkdir -p documents

# Create temp file for the JSON input
TEMP_JSON=$(mktemp)
cat > "$TEMP_JSON"

# Call the Python saver with the temp file
python3 "$SKILL_DIR/evaluation_saver.py" "$TEMP_JSON"

# Clean up
rm -f "$TEMP_JSON"
