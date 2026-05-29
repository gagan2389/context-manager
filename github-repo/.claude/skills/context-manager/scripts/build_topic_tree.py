#!/usr/bin/env python3
"""
build_topic_tree.py — Interactively build a topic context file tree.
Usage: python3 build_topic_tree.py <topic-name>
Saves result to .topiccontext/<topic-name>.json
"""

import os
import sys
import json
import datetime


def find_project_root():
    """Walk up from CWD to find project root (has CLAUDE.md or .git or .claude)."""
    path = os.getcwd()
    for _ in range(10):
        if any(os.path.exists(os.path.join(path, f)) for f in [".claude", ".git", "CLAUDE.md"]):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return os.getcwd()


def build_file_tree(root, max_depth=4, ignore_dirs=None):
    """Return a flat list of all files/dirs up to max_depth."""
    if ignore_dirs is None:
        ignore_dirs = {
            "node_modules", ".git", "dist", "build", ".next", "__pycache__",
            ".cache", "coverage", ".pytest_cache", "venv", ".venv", "target",
            "out", ".turbo", ".vercel", "tmp", "temp", "logs"
        }
    entries = []
    root = os.path.abspath(root)

    for dirpath, dirnames, filenames in os.walk(root):
        # Compute depth
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth > max_depth:
            dirnames.clear()
            continue

        # Filter ignored dirs in-place so os.walk skips them
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith(".")]

        for fname in filenames:
            if fname.startswith("."):
                continue
            fpath = os.path.relpath(os.path.join(dirpath, fname), root)
            entries.append(fpath)

    return sorted(entries)


def print_tree(entries, root):
    """Print a numbered list of files."""
    print(f"\n📁 Project files (from {root}):\n")
    for i, entry in enumerate(entries, 1):
        print(f"  {i:3}. {entry}")
    print()


def interactive_select(entries):
    """Let user pick files/folders by number, range, or glob prefix."""
    print("=" * 60)
    print("Select files for this topic context.")
    print("You can enter:")
    print("  • Numbers: 1 5 12")
    print("  • Ranges: 1-10")
    print("  • Folder prefix: src/feature-a (selects all files under it)")
    print("  • 'all' to include everything")
    print("  • 'done' when finished")
    print("=" * 60)

    selected = set()

    while True:
        raw = input("\nAdd files > ").strip()
        if raw.lower() in ("done", "q", "exit", ""):
            break
        if raw.lower() == "all":
            selected = set(entries)
            print(f"  ✅ All {len(entries)} files selected")
            continue

        # Folder/path prefix match
        if raw.replace("/", "").replace("\\", "").replace(".", "").replace("_", "").replace("-", "").isalpha() or "/" in raw or "\\" in raw:
            matched = [e for e in entries if e.startswith(raw) or e.replace("\\", "/").startswith(raw.replace("\\", "/"))]
            if matched:
                selected.update(matched)
                print(f"  ✅ Added {len(matched)} files matching '{raw}'")
                continue

        # Parse numbers and ranges
        parts = raw.replace(",", " ").split()
        added = 0
        for part in parts:
            if "-" in part:
                try:
                    lo, hi = part.split("-", 1)
                    for idx in range(int(lo), int(hi) + 1):
                        if 1 <= idx <= len(entries):
                            selected.add(entries[idx - 1])
                            added += 1
                except ValueError:
                    print(f"  ⚠️  Could not parse range '{part}'")
            else:
                try:
                    idx = int(part)
                    if 1 <= idx <= len(entries):
                        selected.add(entries[idx - 1])
                        added += 1
                    else:
                        print(f"  ⚠️  Number {idx} out of range")
                except ValueError:
                    print(f"  ⚠️  Unknown input '{part}'")

        if added:
            print(f"  ✅ Added {added} file(s). Total selected: {len(selected)}")

    return sorted(selected)


def save_topic(project_root, topic_name, description, selected_files, entry_point):
    """Save the topic JSON to .topiccontext/<name>.json"""
    out_dir = os.path.join(project_root, ".topiccontext")
    os.makedirs(out_dir, exist_ok=True)

    data = {
        "topic": topic_name,
        "description": description,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "entry_point": entry_point,
        "files": selected_files,
        "excluded_patterns": []
    }

    out_path = os.path.join(out_dir, f"{topic_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return out_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_topic_tree.py <topic-name>")
        print("Example: python3 build_topic_tree.py feature-a")
        sys.exit(1)

    topic_name = sys.argv[1].lower().strip()
    project_root = find_project_root()

    print(f"\n🗂️  Context Manager — Topic Builder")
    print(f"   Topic: {topic_name}")
    print(f"   Project root: {project_root}\n")

    # Gather description
    description = input(f"Short description for '{topic_name}' (e.g. 'HOTO handover flow'): ").strip()
    if not description:
        description = f"{topic_name} context"

    # Scan project
    print("\n🔍 Scanning project files...")
    entries = build_file_tree(project_root)

    if not entries:
        print("⚠️  No files found. Make sure you're running from the project root.")
        sys.exit(1)

    print_tree(entries, project_root)

    # Interactive select
    selected = interactive_select(entries)

    if not selected:
        print("⚠️  No files selected. Topic not saved.")
        sys.exit(0)

    # Entry point
    print(f"\nSelected {len(selected)} files.")
    entry_point = input("Entry point file (press Enter to skip): ").strip()

    # Save
    out_path = save_topic(project_root, topic_name, description, selected, entry_point)

    print(f"\n✅ Topic '{topic_name}' saved to {out_path}")
    print(f"   {len(selected)} files included")
    print(f"\nUsage in Claude Code:")
    print(f"   /usetopiccontext {topic_name}")


if __name__ == "__main__":
    main()
