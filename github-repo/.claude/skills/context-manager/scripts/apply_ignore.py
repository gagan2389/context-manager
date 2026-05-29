#!/usr/bin/env python3
"""
apply_ignore.py — Manage .claudeignore file.
Usage:
  python3 apply_ignore.py add <pattern>
  python3 apply_ignore.py remove <pattern>
  python3 apply_ignore.py list
  python3 apply_ignore.py init
"""

import os
import sys
import shutil


TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "assets", ".claudeignore.template"
)


def find_project_root():
    path = os.getcwd()
    for _ in range(10):
        if any(os.path.exists(os.path.join(path, f)) for f in [".claude", ".git", "CLAUDE.md"]):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return os.getcwd()


def read_ignore(ignore_path):
    if not os.path.exists(ignore_path):
        return []
    with open(ignore_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_ignore(ignore_path, lines):
    with open(ignore_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def get_patterns(lines):
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]


def cmd_add(ignore_path, pattern):
    lines = read_ignore(ignore_path)
    existing = get_patterns(lines)
    if pattern in existing:
        print(f"  ℹ️  '{pattern}' is already in .claudeignore")
        return
    lines.append(f"{pattern}\n")
    write_ignore(ignore_path, lines)
    print(f"  ✅ Added '{pattern}' to .claudeignore")


def cmd_remove(ignore_path, pattern):
    lines = read_ignore(ignore_path)
    new_lines = [l for l in lines if l.strip() != pattern]
    if len(new_lines) == len(lines):
        print(f"  ⚠️  '{pattern}' not found in .claudeignore")
        return
    write_ignore(ignore_path, new_lines)
    print(f"  ✅ Removed '{pattern}' from .claudeignore")


def cmd_list(ignore_path):
    lines = read_ignore(ignore_path)
    patterns = get_patterns(lines)
    if not patterns:
        print("  .claudeignore is empty or does not exist")
        return
    print(f"\n  📋 .claudeignore ({len(patterns)} patterns):\n")
    for p in patterns:
        print(f"    • {p}")
    print()


def cmd_init(ignore_path):
    if os.path.exists(ignore_path):
        ans = input("  .claudeignore already exists. Overwrite? [y/N]: ").strip().lower()
        if ans != "y":
            print("  Cancelled.")
            return

    template = os.path.abspath(TEMPLATE_PATH)
    if os.path.exists(template):
        shutil.copy(template, ignore_path)
        print(f"  ✅ .claudeignore created from template")
    else:
        # Fallback: write a minimal default
        default = """# Claude Code — .claudeignore
# Files and patterns Claude will NEVER read

# Dependencies
node_modules/
vendor/
.venv/
venv/

# Build outputs
dist/
build/
out/
.next/
.nuxt/
target/

# Lock files
package-lock.json
yarn.lock
pnpm-lock.yaml
Cargo.lock
poetry.lock
composer.lock

# Environment & secrets
.env
.env.*
*.pem
*.key
*.cert
*.p12

# Logs
*.log
logs/
npm-debug.log*

# Test coverage
coverage/
.nyc_output/
.pytest_cache/

# Cache
.cache/
.turbo/
.parcel-cache/
__pycache__/
*.pyc

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Binary & media (usually not useful for code context)
*.png
*.jpg
*.jpeg
*.gif
*.ico
*.svg
*.mp4
*.mp3
*.zip
*.tar.gz
*.pdf

# Generated
*.min.js
*.min.css
*.map
"""
        with open(ignore_path, "w") as f:
            f.write(default)
        print(f"  ✅ .claudeignore created with defaults")

    cmd_list(ignore_path)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_root = find_project_root()
    ignore_path = os.path.join(project_root, ".claudeignore")
    cmd = sys.argv[1].lower()

    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: apply_ignore.py add <pattern>")
            sys.exit(1)
        cmd_add(ignore_path, sys.argv[2])

    elif cmd == "remove":
        if len(sys.argv) < 3:
            print("Usage: apply_ignore.py remove <pattern>")
            sys.exit(1)
        cmd_remove(ignore_path, sys.argv[2])

    elif cmd == "list":
        cmd_list(ignore_path)

    elif cmd == "init":
        cmd_init(ignore_path)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
