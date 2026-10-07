#!/usr/bin/env python3
"""Read-only import graph builder. Emits JSON to stdout."""
import ast, json, os, sys
from pathlib import Path

def py_imports(path):
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return []
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return sorted(imports)

def main(root):
    graph = {}
    for dirpath, _, files in os.walk(root):
        if any(s in dirpath for s in ("node_modules", ".git", "dist", "build", "venv")):
            continue
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, root)
                graph[rel] = py_imports(full)
    print(json.dumps(graph, indent=2))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
