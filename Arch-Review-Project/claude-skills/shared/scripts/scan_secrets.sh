#!/usr/bin/env bash
# Read-only secret scan. Prints file:line [type] with the matched value masked.
set -euo pipefail
TARGET="${1:?Usage: scan_secrets.sh <path>}"
[ -e "$TARGET" ] || { echo "Path not found: $TARGET" >&2; exit 2; }

declare -A PATTERNS=(
  [password]='password[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{4,}'
  [api_key]='api[_-]?key[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{8,}'
  [aws_key]='AKIA[0-9A-Z]{16}'
  [pem_key]='-----BEGIN (RSA|EC|OPENSSH|DSA)? ?PRIVATE KEY-----'
  [conn_string]='(Password|Pwd)=[^;"'"'"' ]{4,};'
)

echo "# Secret scan: $TARGET"
for name in "${!PATTERNS[@]}"; do
  grep -rIEn \
    --exclude-dir={node_modules,.git,dist,build,vendor,bin,obj,.venv,venv,.vs} \
    --exclude={package-lock.json,yarn.lock,*.lock} \
    -e "${PATTERNS[$name]}" "$TARGET" 2>/dev/null |
  sed -E "s/^(.*):([0-9]+):.*/\1:\2 [$name] <masked>/"
done || true
