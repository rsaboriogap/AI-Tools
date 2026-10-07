#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:?Usage: detect_project_type.sh <path>}"
echo "# Project detection: $TARGET"
for marker in package.json pom.xml build.gradle go.mod Cargo.toml requirements.txt composer.json Gemfile; do
  find "$TARGET" -maxdepth 2 -name "$marker" -not -path "*/node_modules/*" 2>/dev/null | while read -r f; do echo "STACK: $f"; done
done
for artifact in Dockerfile "docker-compose*.yml" k8s terraform serverless.yml; do
  find "$TARGET" -maxdepth 3 -name "$artifact" -not -path "*/node_modules/*" 2>/dev/null | while read -r f; do echo "DEPLOY: $f"; done
done
