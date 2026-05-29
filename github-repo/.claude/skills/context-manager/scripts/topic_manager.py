#!/usr/bin/env python3
"""
topic_manager.py — Manage saved topic contexts.
Usage:
  python3 topic_manager.py list
  python3 topic_manager.py show <name>
  python3 topic_manager.py delete <name>
  python3 topic_manager.py activate <name>
  python3 topic_manager.py deactivate
"""

import os
import sys
import json


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


def get_topic_dir(project_root):
    return os.path.join(project_root, ".topiccontext")


def list_topics(topic_dir):
    if not os.path.isdir(topic_dir):
        print("  No topics created yet. Run /topiccontext create <name>")
        return

    active = get_active(topic_dir)
    files = [f for f in os.listdir(topic_dir) if f.endswith(".json")]

    if not files:
        print("  No topics created yet. Run /topiccontext create <name>")
        return

    print(f"\n  🗂️  Topic Contexts ({len(files)} saved):\n")
    for fname in sorted(files):
        name = fname.replace(".json", "")
        fpath = os.path.join(topic_dir, fname)
        try:
            with open(fpath) as f:
                data = json.load(f)
            file_count = len(data.get("files", []))
            desc = data.get("description", "")
            is_active = "  ← ACTIVE" if name == active else ""
            print(f"    • {name:<20} {file_count} files  {desc}{is_active}")
        except Exception:
            print(f"    • {name}  (could not read)")
    print()


def show_topic(topic_dir, name):
    fpath = os.path.join(topic_dir, f"{name}.json")
    if not os.path.exists(fpath):
        print(f"  ⚠️  Topic '{name}' not found")
        return
    with open(fpath) as f:
        data = json.load(f)

    print(f"\n  📋 Topic: {data.get('topic', name)}")
    print(f"  Description: {data.get('description', '-')}")
    print(f"  Created: {data.get('created_at', '-')}")
    print(f"  Entry point: {data.get('entry_point', '-')}")
    print(f"\n  Files ({len(data.get('files', []))}):\n")
    for f in data.get("files", []):
        print(f"    • {f}")
    print()


def delete_topic(topic_dir, name):
    fpath = os.path.join(topic_dir, f"{name}.json")
    if not os.path.exists(fpath):
        print(f"  ⚠️  Topic '{name}' not found")
        return
    ans = input(f"  Delete topic '{name}'? [y/N]: ").strip().lower()
    if ans == "y":
        os.remove(fpath)
        # Deactivate if it was active
        active_path = os.path.join(topic_dir, ".active")
        if os.path.exists(active_path):
            with open(active_path) as f:
                if f.read().strip() == name:
                    os.remove(active_path)
        print(f"  ✅ Topic '{name}' deleted")
    else:
        print("  Cancelled")


def get_active(topic_dir):
    active_path = os.path.join(topic_dir, ".active")
    if os.path.exists(active_path):
        with open(active_path) as f:
            return f.read().strip()
    return None


def activate_topic(topic_dir, name):
    fpath = os.path.join(topic_dir, f"{name}.json")
    if not os.path.exists(fpath):
        print(f"  ⚠️  Topic '{name}' not found. Run /topiccontext create {name} first")
        return
    os.makedirs(topic_dir, exist_ok=True)
    active_path = os.path.join(topic_dir, ".active")
    with open(active_path, "w") as f:
        f.write(name)

    with open(fpath) as f:
        data = json.load(f)
    file_count = len(data.get("files", []))
    print(f"  🎯 Topic '{name}' activated — {file_count} files in scope")
    print(f"  Claude will only read files from this topic until you run /usetopiccontext off")


def deactivate_topic(topic_dir):
    active_path = os.path.join(topic_dir, ".active")
    if os.path.exists(active_path):
        os.remove(active_path)
    print("  🔓 Topic context deactivated — all non-ignored files are now readable")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    project_root = find_project_root()
    topic_dir = get_topic_dir(project_root)
    cmd = sys.argv[1].lower()

    if cmd == "list":
        list_topics(topic_dir)
    elif cmd == "show":
        if len(sys.argv) < 3:
            print("Usage: topic_manager.py show <name>")
            sys.exit(1)
        show_topic(topic_dir, sys.argv[2])
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Usage: topic_manager.py delete <name>")
            sys.exit(1)
        delete_topic(topic_dir, sys.argv[2])
    elif cmd == "activate":
        if len(sys.argv) < 3:
            print("Usage: topic_manager.py activate <name>")
            sys.exit(1)
        activate_topic(topic_dir, sys.argv[2])
    elif cmd == "deactivate":
        deactivate_topic(topic_dir)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
