#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:?Usage: scan_secrets.sh <path>}"
PATTERNS=(
  "password\s*=\s*[\"