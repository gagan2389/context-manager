# 🗂️ Context Manager for Claude Code

> **Cut token usage by 60–90% per session.** Control exactly which files Claude reads — with ignore lists, topic scoping, and a live token status bar.

![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Mac%20%7C%20Windows%20%7C%20Linux-supported-lightgrey)
![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-blue)

---

## Why

Claude Code reads your project files to understand context. In a large project this gets expensive:

| Without this skill | With this skill |
|---|---|
| ~200 files scanned | ~15 files scanned |
| ~80,000 tokens used | ~6,000 tokens used |
| Slow, noisy responses | Fast, focused responses |

---

## Commands

| Command | What it does |
|---|---|
| `/ignore init` | Create `.claudeignore` — skip node_modules, dist, .env, lock files, media, etc. |
| `/ignore add <pattern>` | Add any file or glob pattern to the ignore list |
| `/filecontext <file>` | Pin Claude to one file only for this task |
| `/topiccontext create <name>` | Interactively map a feature area to its files |
| `/usetopiccontext <name>` | Restrict Claude to only that topic's files |
| `/topiccontext list` | See all saved topic scopes |
| `/tokenstatus` | Live token usage bar — shows usage, savings, remaining budget |
| `/remember <fact>` | Save a fact to `CLAUDE.md` so Claude knows it every session |
| `/scope <task>` | Lock Claude to one specific task, no drifting |
| `/clearcontext` | Remove all active restrictions for this session |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed — `npm install -g @anthropic-ai/claude-code`
- Python 3.8+
- Mac, Linux, or Windows

---

## Installation

### Method 1 — Run `install.py` (easiest, works everywhere)

**Step 1** — Download or clone this repo

```bash
git clone https://github.com/gagan2389/context-manager.git
cd context-manager
```

Or click **Code → Download ZIP** on GitHub, unzip it, and open a terminal in that folder.

**Step 2** — Run the installer

```bash
# Mac / Linux
python3 install.py

# Windows
python install.py
```

**Step 3** — Done. Open Claude Code in any project and type `/tokenstatus` to verify.

---

### Method 2 — Manual copy

```bash
# Mac / Linux
mkdir -p ~/.claude/skills
cp -r .claude/skills/context-manager ~/.claude/skills/

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse .\.claude\skills\context-manager "$env:USERPROFILE\.claude\skills\"
```

---

### Uninstall

```bash
python3 install.py --uninstall
```

---

## Quick Start

After installing, open Claude Code in your project and run these three commands once:

**1. Set up the ignore list**
```
/ignore init
```
Writes `.claudeignore` to your project root. Automatically skips node_modules, dist, build, .env files, lock files, media files, and coverage reports.

**2. Create a topic scope**
```
/topiccontext create feature-a
```
Claude scans your project and shows a numbered file list. Type numbers (`1 5 12`), ranges (`3-10`), or a folder prefix (`src/feature-a`) to pick which files belong to this topic. Saved to `.topiccontext/feature-a.json`.

Repeat for each part of your project:
```
/topiccontext create feature-b
/topiccontext create shared-utils
```

**3. Activate a scope before you start working**
```
/usetopiccontext feature-a
```
Claude now only reads files from `feature-a` for the rest of this session.

---

## How Topic Scoping Works

Each topic is a named set of files saved as JSON in your project:

```json
{
  "topic": "feature-a",
  "description": "User authentication flow",
  "entry_point": "src/auth/index.ts",
  "files": [
    "src/auth/",
    "api/auth-routes.ts",
    "types/auth.types.ts"
  ]
}
```

Switch between topics at any time:
```
/usetopiccontext feature-a
/usetopiccontext feature-b
/usetopiccontext off            ← remove restriction
```

When a topic is active and you ask about a file outside it, Claude will say:
> ⚠️ That file is outside the `feature-a` context. Switch with `/usetopiccontext feature-b` or run `/clearcontext`.

---

## Token Status Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊  CONTEXT MANAGER — TOKEN STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Project:      my-app
  Total files:  247  (~82.3k tokens)

  ── Restrictions ────────────────────────────────────
  .claudeignore: 34 patterns → 89 files skipped
                 saved ~48.2k tokens
  Topic scope:   'feature-a' (User authentication flow)
                 18 files, ~6.1k tokens
                 saved ~28.0k tokens vs full project

  ── Available in Context ────────────────────────────
  Readable now:  ~6.1k tokens
  Context window:200k tokens
  🟢 [████░░░░░░░░░░░░░░░░░░░░░░░░░░] 3%

  ── Total Savings ───────────────────────────────────
  Tokens saved:  ~76.2k (93% of project)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Full Command Reference

### `/ignore`

```
/ignore init                    Apply smart defaults to .claudeignore
/ignore add node_modules/       Add a directory
/ignore add *.test.ts           Add a glob pattern
/ignore add .env.local          Add a specific file
/ignore remove *.test.ts        Remove a pattern
/ignore list                    Show all current patterns
```

### `/filecontext`

```
/filecontext src/auth/login.ts  Pin to one file — Claude won't read others
/filecontext clear              Remove the pin
```

### `/topiccontext`

```
/topiccontext create <name>     Interactive file picker for a topic
/topiccontext list              See all saved topics with file counts
/topiccontext show <name>       See exactly which files are in a topic
/topiccontext delete <name>     Delete a topic
```

### `/usetopiccontext`

```
/usetopiccontext <name>         Activate a topic scope
/usetopiccontext off            Remove topic restriction
```

### Others

```
/tokenstatus                    Token usage dashboard
/remember <fact>                Persist a fact to CLAUDE.md
/scope <task description>       Lock Claude to one task
/clearcontext                   Reset all session restrictions
```

---

## Daily Workflow Example

```
# Start working on feature A
/usetopiccontext feature-a
/tokenstatus

# ... work ...

# Need to check a shared config
/filecontext config/db.ts

# Switch to feature B
/usetopiccontext feature-b

# Save something for future sessions
/remember Always run pnpm test before committing

# Done — reset
/clearcontext
```

---

## What to Commit to Git

| File | Commit? | Why |
|---|---|---|
| `.claudeignore` | ✅ Yes | Whole team skips the same files |
| `.topiccontext/*.json` | ✅ Yes | Whole team can use the same topic scopes |
| `CLAUDE.md` | ✅ Yes | Shared facts Claude knows every session |
| `.topiccontext/.active` | ❌ No | Personal session state |

---

## Repo Structure

```
context-manager/
├── install.py                                    ← run this to install
├── README.md
├── LICENSE
├── .gitignore
└── .claude/
    └── skills/
        └── context-manager/
            ├── SKILL.md                          ← Claude reads this to understand commands
            ├── scripts/
            │   ├── build_topic_tree.py           ← /topiccontext create
            │   ├── topic_manager.py              ← /topiccontext list/show/delete
            │   ├── token_status.py               ← /tokenstatus
            │   └── apply_ignore.py               ← /ignore commands
            ├── references/
            │   ├── ignore-patterns.md
            │   └── token-guide.md
            └── assets/
                └── .claudeignore.template
```

After installing, the skill lives at `~/.claude/skills/context-manager/` and works in every project automatically.

---

## Troubleshooting

**Skill not appearing in Claude Code**
```bash
ls ~/.claude/skills/              # Mac/Linux — should list context-manager
dir %USERPROFILE%\.claude\skills\ # Windows
```
Restart Claude Code after installing.

**`/tokenstatus` shows 0 or wrong numbers**
Run from your project root. Token count is an estimate (~4 chars = 1 token).

**`/topiccontext create` doesn't find my files**
Run from the project root (where `.git/` or `.claude/` lives).

**Windows: "python3 not found"**
Use `python install.py` instead. Make sure Python is installed from [python.org](https://python.org) with "Add to PATH" checked.

---

## Contributing

Issues and PRs welcome. Ideas:
- Auto-detect project type and suggest topic groupings
- Sync `.claudeignore` patterns with `.gitignore`
- More project-type templates in the default ignore list

---

## License

MIT
