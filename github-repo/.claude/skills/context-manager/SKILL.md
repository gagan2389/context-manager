---
name: context-manager
description: >
  Token-efficient context management for Claude Code. Use this skill whenever
  the user types any of these commands: /ignore, /filecontext, /topiccontext,
  /usetopiccontext, /projectcontext, /tokenstatus, /clearcontext, /remember,
  /scope, /summarize. Also trigger automatically when the user mentions "too
  many tokens", "context too large", "only look at X files", "ignore this
  file", "stay in feature-a context", "stay in feature-b context", or any topic-scoping
  request. This skill manages .claudeignore, .topiccontext/ JSON trees, and
  session-level file restrictions to minimize token usage.
invocation: slash_command
---

# Context Manager — Token Efficiency Skill

Reduces token consumption by controlling exactly which files Claude reads per
session. Supports ignore lists, per-file pinning, topic-scoped file trees, and
live token status reporting.

---

## Commands Reference

| Command | What it does |
|---|---|
| `/ignore add <pattern>` | Add file/glob to `.claudeignore` |
| `/ignore remove <pattern>` | Remove from `.claudeignore` |
| `/ignore list` | Show current ignore list |
| `/ignore init` | Apply default `.claudeignore` template |
| `/filecontext <path>` | Pin one file — Claude won't read others |
| `/filecontext clear` | Remove file pin |
| `/topiccontext create <name>` | Interactively build a topic file tree |
| `/topiccontext list` | List all saved topic contexts |
| `/topiccontext show <name>` | Show files in a topic |
| `/topiccontext delete <name>` | Delete a topic context |
| `/usetopiccontext <name>` | Restrict Claude to only that topic's files |
| `/usetopiccontext off` | Remove topic restriction |
| `/projectcontext` | Show full project tree grouped by topics |
| `/tokenstatus` | Show token usage, savings, remaining budget |
| `/clearcontext` | Reset all session restrictions |
| `/remember <fact>` | Save a persistent fact to CLAUDE.md |
| `/scope <task>` | Lock Claude to a specific task boundary |

---

## Behavior Rules

### When `/ignore` is used:
1. Read current `.claudeignore` (or create if missing)
2. Apply the requested change
3. Confirm: "✅ Updated .claudeignore — `<pattern>` will be skipped in all future reads"
4. NEVER read files matching any pattern in `.claudeignore`

### When `/filecontext <path>` is used:
1. Store `activeFileContext = <path>` in session memory
2. For ALL subsequent file reads, ONLY read that file unless user explicitly says otherwise
3. Confirm: "📌 File context pinned to `<path>`. I'll only reference this file until you run `/filecontext clear`"

### When `/topiccontext create <name>` is used:
1. Run: `python3 .claude/skills/context-manager/scripts/build_topic_tree.py <name>`
2. The script will interactively ask which folders/files belong to this topic
3. Save result to `.topiccontext/<name>.json`
4. Confirm: "✅ Topic `<name>` saved with X files. Use `/usetopiccontext <name>` to activate it"

### When `/usetopiccontext <name>` is used:
1. Read `.topiccontext/<name>.json`
2. Store `activeTopicContext = <name>` in session memory
3. For ALL subsequent file reads, ONLY read files listed in that topic's JSON
4. If asked about files outside that topic, respond: "⚠️ That file is outside the `<name>` context. Switch with `/usetopiccontext <other>` or run `/clearcontext` to remove restrictions"
5. Confirm: "🎯 Now scoped to topic `<name>` — X files active"

### When `/tokenstatus` is used:
1. Run: `python3 .claude/skills/context-manager/scripts/token_status.py`
2. Display the formatted status bar
3. Show active restrictions (file context, topic context, ignore count)

### When `/remember <fact>` is used:
1. Open (or create) `CLAUDE.md` in project root
2. Append under a `## Remembered Facts` section
3. Confirm: "💾 Saved to CLAUDE.md — I'll know this in every future session"

### When `/clearcontext` is used:
1. Clear `activeFileContext` and `activeTopicContext` from session memory
2. Confirm: "🔓 Context restrictions cleared. I can read all non-ignored files now"

---

## Auto-ignore on Startup

At the start of every session, check if `.claudeignore` exists in the project root.
If it exists, load all patterns and NEVER read matching files — even if not explicitly asked.

---

## Topic Context JSON Format

`.topiccontext/<name>.json`:
```json
{
  "topic": "feature-a",
  "description": "Project-1-Name flow — handover to operations",
  "created_at": "2025-01-01T00:00:00Z",
  "entry_point": "src/feature-a/index.ts",
  "files": [
    "src/feature-a/",
    "api/feature-a-routes.ts",
    "utils/feature-a-helpers.ts",
    "types/feature-a.types.ts"
  ],
  "excluded_patterns": []
}
```

---

## Reference Files

- `references/ignore-patterns.md` — Curated default ignore lists by project type
- `references/token-guide.md` — How token estimation works
- `scripts/build_topic_tree.py` — Interactive topic builder
- `scripts/token_status.py` — Token usage reporter
- `scripts/apply_ignore.py` — .claudeignore reader/writer
- `assets/.claudeignore.template` — Default ignore template
