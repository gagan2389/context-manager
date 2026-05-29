#!/usr/bin/env python3
"""
token_status.py — Report token usage, savings, and context state.
Usage: python3 token_status.py [--json]
"""

import os
import sys
import json
import glob
import argparse


# Rough token estimation: ~4 chars per token (GPT/Claude heuristic)
CHARS_PER_TOKEN = 4
# Claude's effective context window for coding (conservative estimate)
CONTEXT_WINDOW = 200_000


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


def estimate_tokens(text):
    return max(1, len(text) // CHARS_PER_TOKEN)


def file_tokens(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return estimate_tokens(f.read())
    except Exception:
        return 0


def load_claudeignore(project_root):
    ignore_path = os.path.join(project_root, ".claudeignore")
    patterns = []
    if os.path.exists(ignore_path):
        with open(ignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def load_active_topic(project_root):
    """Try to read .topiccontext/.active if it exists."""
    active_path = os.path.join(project_root, ".topiccontext", ".active")
    if os.path.exists(active_path):
        with open(active_path, "r") as f:
            return f.read().strip()
    return None


def load_topic_files(project_root, topic_name):
    topic_path = os.path.join(project_root, ".topiccontext", f"{topic_name}.json")
    if os.path.exists(topic_path):
        with open(topic_path, "r") as f:
            data = json.load(f)
        return data.get("files", []), data.get("description", "")
    return [], ""


def count_all_project_files(project_root):
    ignore_dirs = {
        "node_modules", ".git", "dist", "build", ".next", "__pycache__",
        ".cache", "coverage", ".pytest_cache", "venv", ".venv", "target",
        "out", ".turbo", ".vercel", "tmp", "temp", "logs"
    }
    total_files = 0
    total_tokens = 0
    for dirpath, dirnames, filenames in os.walk(project_root):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith(".")]
        for fname in filenames:
            if fname.startswith("."):
                continue
            fpath = os.path.join(dirpath, fname)
            total_files += 1
            total_tokens += file_tokens(fpath)
    return total_files, total_tokens


def count_ignored_tokens(project_root, patterns):
    """Estimate tokens saved by .claudeignore."""
    if not patterns:
        return 0, 0

    ignored_tokens = 0
    ignored_files = 0

    for pattern in patterns:
        # Handle directory patterns
        if pattern.endswith("/"):
            dir_path = os.path.join(project_root, pattern.rstrip("/"))
            if os.path.isdir(dir_path):
                for dirpath, _, filenames in os.walk(dir_path):
                    for fname in filenames:
                        fpath = os.path.join(dirpath, fname)
                        ignored_tokens += file_tokens(fpath)
                        ignored_files += 1
        else:
            # Glob match
            matched = glob.glob(os.path.join(project_root, "**", pattern), recursive=True)
            matched += glob.glob(os.path.join(project_root, pattern))
            for fpath in matched:
                if os.path.isfile(fpath):
                    ignored_tokens += file_tokens(fpath)
                    ignored_files += 1

    return ignored_files, ignored_tokens


def list_topic_files_tokens(project_root, files):
    total = 0
    count = 0
    for f in files:
        full = os.path.join(project_root, f)
        if os.path.isdir(full):
            for dirpath, _, filenames in os.walk(full):
                for fname in filenames:
                    total += file_tokens(os.path.join(dirpath, fname))
                    count += 1
        elif os.path.isfile(full):
            total += file_tokens(full)
            count += 1
    return count, total


def bar(used, total, width=30):
    if total == 0:
        return "[" + "░" * width + "]"
    filled = int((used / total) * width)
    filled = min(filled, width)
    empty = width - filled
    pct = (used / total) * 100
    if pct < 50:
        color = "🟢"
    elif pct < 80:
        color = "🟡"
    else:
        color = "🔴"
    return f"{color} [{'█' * filled}{'░' * empty}] {pct:.0f}%"


def format_k(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


def main():
    parser = argparse.ArgumentParser(description="Token Status Reporter")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    project_root = find_project_root()
    ignore_patterns = load_claudeignore(project_root)
    active_topic = load_active_topic(project_root)

    # Count everything
    total_files, total_tokens = count_all_project_files(project_root)
    ignored_files, ignored_tokens = count_ignored_tokens(project_root, ignore_patterns)

    # Topic context
    topic_files_count = 0
    topic_tokens = 0
    topic_desc = ""
    if active_topic:
        topic_files, topic_desc = load_topic_files(project_root, active_topic)
        topic_files_count, topic_tokens = list_topic_files_tokens(project_root, topic_files)

    # Topic savings (if active)
    topic_savings = 0
    if active_topic and total_tokens > 0:
        topic_savings = total_tokens - ignored_tokens - topic_tokens

    total_saved = ignored_tokens + topic_savings
    available = total_tokens - total_saved
    remaining_window = max(0, CONTEXT_WINDOW - available)

    result = {
        "project_root": project_root,
        "total_files": total_files,
        "total_tokens": total_tokens,
        "ignored_files": ignored_files,
        "ignored_tokens": ignored_tokens,
        "active_topic": active_topic,
        "topic_desc": topic_desc,
        "topic_files": topic_files_count,
        "topic_tokens": topic_tokens,
        "topic_savings": topic_savings,
        "total_saved": total_saved,
        "available_tokens": available,
        "context_window": CONTEXT_WINDOW,
        "remaining_window": remaining_window,
        "ignore_patterns": len(ignore_patterns),
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return

    # Pretty print
    print()
    print("━" * 52)
    print("  📊  CONTEXT MANAGER — TOKEN STATUS")
    print("━" * 52)
    print(f"  Project:      {os.path.basename(project_root)}")
    print(f"  Total files:  {total_files}  (~{format_k(total_tokens)} tokens)")
    print()
    print("  ── Restrictions ──────────────────────────────")
    if ignore_patterns:
        print(f"  .claudeignore: {len(ignore_patterns)} patterns → {ignored_files} files skipped")
        print(f"                 saved ~{format_k(ignored_tokens)} tokens")
    else:
        print("  .claudeignore: not set (run /ignore init)")

    if active_topic:
        print(f"  Topic scope:   '{active_topic}' ({topic_desc})")
        print(f"                 {topic_files_count} files, ~{format_k(topic_tokens)} tokens")
        print(f"                 saved ~{format_k(topic_savings)} tokens vs full project")
    else:
        print("  Topic scope:   none (run /usetopiccontext <name>)")

    print()
    print("  ── Available in Context ──────────────────────")
    print(f"  Readable now:  ~{format_k(available)} tokens")
    print(f"  Context window:{format_k(CONTEXT_WINDOW)} tokens")
    print(f"  {bar(available, CONTEXT_WINDOW)}")
    print()
    print("  ── Total Savings ─────────────────────────────")
    saving_pct = (total_saved / total_tokens * 100) if total_tokens else 0
    print(f"  Tokens saved:  ~{format_k(total_saved)} ({saving_pct:.0f}% of project)")
    print(f"  Remaining cap: ~{format_k(remaining_window)} tokens free")
    print()
    print("  💡 Tips:")
    if not ignore_patterns:
        print("     → Run /ignore init to apply default ignore patterns")
    if not active_topic:
        print("     → Run /topiccontext create <name> to scope to a feature")
    if total_tokens > CONTEXT_WINDOW * 0.8:
        print("     → Project is large — topic scoping will help a lot")
    if total_saved > 0:
        print(f"     → Great! You're saving {format_k(total_saved)} tokens per session")
    print("━" * 52)
    print()


if __name__ == "__main__":
    main()
