# 🗂️ Context Manager for Claude Code

> Save 60–90% of tokens per session. Each feature ships as a real `/slash-command` visible in Claude Code's autocomplete.

![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Mac%20%7C%20Windows%20%7C%20Linux-supported-lightgrey)
![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-blue)

---

## Slash Commands (all visible in autocomplete)

| Command | What it does |
|---|---|
| `/tokenstatus` | Live token usage bar — used, saved, remaining |
| `/ignore-init` | Create `.claudeignore` with smart defaults |
| `/ignore-add <pattern>` | Add a file/glob to ignore |
| `/ignore-remove <pattern>` | Remove a pattern |
| `/ignore-list` | Show current ignore list |
| `/filecontext <path>` | Pin Claude to one file only |
| `/filecontext-clear` | Remove the file pin |
| `/topiccontext-create <name>` | Interactively map a feature area to files |
| `/topiccontext-list` | See all saved topic scopes |
| `/topiccontext-show <name>` | See files in a topic |
| `/topiccontext-delete <name>` | Delete a topic |
| `/usetopiccontext <name>` | Restrict Claude to only that topic's files |
| `/projectcontext` | Full project map grouped by topics |
| `/clearcontext` | Reset all active restrictions |
| `/remember <fact>` | Save a fact to CLAUDE.md for every session |
| `/scope <task>` | Lock Claude to one specific task |

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — `npm install -g @anthropic-ai/claude-code`
- Python 3.8+
- Mac, Linux, or Windows

---

## Installation

**Step 1** — Clone or download this repo

```bash
git clone https://github.com/YOUR_USERNAME/context-manager.git
cd context-manager
```

Or: GitHub → **Code** → **Download ZIP** → unzip → open terminal in the folder.

**Step 2** — Run the installer

```bash
# Mac / Linux
python3 install.py

# Windows
python install.py
```

**Step 3** — Restart Claude Code desktop app

**Step 4** — Type `/` in any Claude Code session — all commands appear in autocomplete.

---

## Uninstall

```bash
python3 install.py --uninstall
```

---

## Quick Start

```
/ignore-init
```
Creates `.claudeignore` — skips node_modules, dist, .env, lock files, media, logs automatically.

```
/topiccontext-create feature-a
```
Scans your project, shows numbered file list, you pick which files belong to this feature. Saved to `.topiccontext/feature-a.json`.

```
/usetopiccontext feature-a
```
Claude now only reads files from `feature-a` for this session.

```
/tokenstatus
```
See exactly how many tokens you're saving.

---

## How It Works

Each command is a `.md` file in `~/.claude/commands/`. Claude Code discovers them at startup and shows them in the `/` autocomplete menu. When you run one, Claude reads the instructions and executes the corresponding Python script from `~/.claude/skills/context-manager/scripts/`.

The scripts are pure Python 3 standard library — no dependencies to install.

---

## Repo Structure

```
context-manager/
├── install.py                    ← run once to install
├── README.md
├── LICENSE
├── .gitignore
└── .claude/
    ├── commands/                 ← 16 slash command definitions
    │   ├── tokenstatus.md
    │   ├── ignore-init.md
    │   ├── ignore-add.md
    │   ├── ignore-remove.md
    │   ├── ignore-list.md
    │   ├── filecontext.md
    │   ├── filecontext-clear.md
    │   ├── topiccontext-create.md
    │   ├── topiccontext-list.md
    │   ├── topiccontext-show.md
    │   ├── topiccontext-delete.md
    │   ├── usetopiccontext.md
    │   ├── projectcontext.md
    │   ├── clearcontext.md
    │   ├── remember.md
    │   └── scope.md
    └── skills/
        └── context-manager/      ← Python scripts + SKILL.md
            ├── SKILL.md
            ├── scripts/
            │   ├── token_status.py
            │   ├── apply_ignore.py
            │   ├── build_topic_tree.py
            │   └── topic_manager.py
            ├── references/
            └── assets/
                └── .claudeignore.template
```

---

## Troubleshooting

**Commands not showing in autocomplete**
Restart Claude Code after running `install.py`.

**Script not found error**
Make sure you ran `python3 install.py` — the scripts live in `~/.claude/skills/context-manager/scripts/`.

**Windows: "python3 not found"**
Use `python install.py`. Install Python from [python.org](https://python.org) with "Add to PATH" checked.

---

## License

MIT
