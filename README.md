# 🗂️ Context Manager for Claude Code

> **Save 60–90% of your token usage** in Claude Code by controlling exactly which files Claude reads — with ignore lists, topic scoping, and live token tracking.

![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey)

---

## The Problem

Claude Code reads your project files to understand context. In a large project:

- **Without** context-manager → Claude might scan 200 files, 80,000+ tokens, every session
- **With** context-manager → Claude reads only your 15 relevant files, ~6,000 tokens

That's a **92% token reduction** — faster responses, lower cost, less context noise.

---

## What's Inside

| Feature | Command | What it does |
|---|---|---|
| **Ignore List** | `/ignore init` | Never read node_modules, dist, .env, etc. |
| **File Pin** | `/filecontext auth.ts` | Only look at one specific file |
| **Topic Scope** | `/topiccontext create hoto` | Map your feature areas to files |
| **Activate Scope** | `/usetopiccontext hoto` | Restrict Claude to only hoto files |
| **Project Map** | `/projectcontext` | See full project tree with topics |
| **Token Status** | `/tokenstatus` | Live token usage + savings bar |
| **Remember Facts** | `/remember <fact>` | Persist a fact to CLAUDE.md |
| **Task Scope** | `/scope <task>` | Lock Claude to a specific task |
| **Clear All** | `/clearcontext` | Remove all active restrictions |

---

## Requirements

- [Claude Code](https://claude.ai/code) installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.8 or higher
- Mac, Linux, or Windows

---

## Installation

### Option A — Download ZIP (Easiest)

1. Click the green **Code** button on this page → **Download ZIP**
2. Unzip it anywhere (e.g. your Downloads folder)
3. Open Terminal (Mac/Linux) or PowerShell (Windows)
4. Run the installer:

**Mac / Linux:**
```bash
cd context-manager-main
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
cd context-manager-main
.\install.ps1
```

Done. The skill is now installed globally and works in every Claude Code project.

---

### Option B — Clone with Git

```bash
git clone https://github.com/YOUR_USERNAME/context-manager.git
cd context-manager
chmod +x install.sh
./install.sh
```

---

### Option C — Manual Install (if scripts don't work)

Copy the skill folder to Claude Code's global skills directory:

**Mac / Linux:**
```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/context-manager ~/.claude/skills/
```

**Windows:**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse .claude\skills\context-manager "$env:USERPROFILE\.claude\skills\"
```

---

## Verify Installation

Open Claude Code in any project and type:
```
/tokenstatus
```
You should see a token usage report. If you see it, the skill is working.

---

## Quick Start (First Time in a Project)

Open Claude Code in your project and run these 3 commands once:

```
/ignore init
```
This creates a `.claudeignore` file with smart defaults — ignores node_modules, dist, lock files, .env, media files, etc.

```
/topiccontext create hoto
```
This walks you through mapping your HOTO-related files. Claude will scan the project and you pick which files/folders belong to this topic.

```
/usetopiccontext hoto
```
Now Claude only reads files from the HOTO context. Run this at the start of each session when working on HOTO.

---

## Full Command Reference

### `/ignore` — Control What Claude Never Reads

```
/ignore init                    Apply smart defaults to .claudeignore
/ignore add node_modules/       Add a specific pattern
/ignore add *.test.ts           Add a glob pattern  
/ignore add src/generated/      Add a folder
/ignore remove *.test.ts        Remove a pattern
/ignore list                    See all current patterns
```

The `.claudeignore` file is saved in your project root and committed to git — your team benefits too.

**Patterns support:**
- Exact paths: `src/legacy/`
- Globs: `**/*.spec.js`
- Directory suffix: `dist/` (matches at any depth)
- Negation: `!important.env` (un-ignore something)

---

### `/filecontext` — Pin to One File

```
/filecontext src/auth/login.ts      Pin — only this file matters right now
/filecontext clear                  Remove the pin
```

Use this when you're working on a specific file and don't want Claude pulling in related imports or context. Great for bug fixes and small edits.

---

### `/topiccontext` — Define Feature Areas

```
/topiccontext create hoto           Interactive setup — pick your files
/topiccontext create pcc            Create another topic
/topiccontext list                  See all your saved topics
/topiccontext show hoto             See which files are in hoto
/topiccontext delete hoto           Remove a topic
```

**How create works:**
1. Claude scans your project and shows a numbered file list
2. You type numbers, ranges (`1-10`), or folder prefixes (`src/hoto`)
3. The mapping is saved to `.topiccontext/hoto.json`
4. Next session, just run `/usetopiccontext hoto`

**Example `.topiccontext/hoto.json`:**
```json
{
  "topic": "hoto",
  "description": "HOTO handover to operations flow",
  "entry_point": "src/hoto/index.ts",
  "files": [
    "src/hoto/",
    "api/hoto-routes.ts",
    "utils/hoto-helpers.ts",
    "types/hoto.types.ts"
  ]
}
```

---

### `/usetopiccontext` — Activate a Topic Scope

```
/usetopiccontext hoto           Restrict to hoto files only
/usetopiccontext pcc            Switch to pcc files
/usetopiccontext off            Remove all topic restrictions
```

When active, if you ask about a file outside the topic, Claude will tell you and ask if you want to switch.

---

### `/projectcontext` — See the Full Picture

```
/projectcontext
```

Shows your entire project grouped by topic contexts, with file counts and token estimates per group. Useful for planning which context to use before starting work.

---

### `/tokenstatus` — Live Token Dashboard

```
/tokenstatus
```

Example output:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📊  CONTEXT MANAGER — TOKEN STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Project:      my-app
  Total files:  247  (~82.3k tokens)

  ── Restrictions ────────────────────────────────────
  .claudeignore: 34 patterns → 89 files skipped
                 saved ~48.2k tokens
  Topic scope:   'hoto' (HOTO handover flow)
                 18 files, ~6.1k tokens
                 saved ~28.0k tokens vs full project

  ── Available in Context ────────────────────────────
  Readable now:  ~6.1k tokens
  Context window:200k tokens
  🟢 [████░░░░░░░░░░░░░░░░░░░░░░░░░░] 3%

  ── Total Savings ───────────────────────────────────
  Tokens saved:  ~76.2k (93% of project)
  Remaining cap: ~193.9k tokens free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### `/remember` — Persist Facts Across Sessions

```
/remember We use Prisma ORM, not TypeORM
/remember The staging URL is https://staging.myapp.com
/remember Always run 'pnpm test' before committing
```

Saves to `CLAUDE.md` in your project root. Claude reads this at the start of every session.

---

### `/scope` — Lock Claude to a Task

```
/scope Fix the login timeout bug in auth.ts
```

Claude will stay focused on that task and decline to drift into unrelated changes. Good for when you want precise, contained edits.

---

### `/clearcontext` — Reset Everything

```
/clearcontext
```

Removes all active restrictions for this session (file pin, topic scope). The `.claudeignore` stays — it's permanent until you edit it.

---

## Typical Daily Workflow

```
# Start of session — working on HOTO feature
/usetopiccontext hoto
/tokenstatus

# Claude now only reads hoto files
# ... do your work ...

# Need to check a config file outside hoto
/clearcontext
/filecontext config/database.ts

# Done with config, back to hoto
/usetopiccontext hoto

# End of session — save something important
/remember HOTO flow requires approval step before handover
```

---

## File Structure (What Gets Installed)

```
~/.claude/skills/context-manager/       ← global install location
├── SKILL.md                            ← Claude reads this to understand commands
├── scripts/
│   ├── build_topic_tree.py             ← interactive topic builder
│   ├── topic_manager.py               ← list/show/delete topics
│   ├── token_status.py                ← token usage reporter
│   └── apply_ignore.py                ← .claudeignore manager
├── references/
│   ├── ignore-patterns.md             ← quick ignore reference
│   └── token-guide.md                 ← how tokens are counted
└── assets/
    └── .claudeignore.template         ← default ignore list

your-project/                           ← your project (created by the skill)
├── .claudeignore                      ← your project's ignore list
├── .topiccontext/
│   ├── hoto.json                      ← hoto topic definition
│   └── pcc.json                       ← pcc topic definition
└── CLAUDE.md                          ← project memory (Claude reads every session)
```

---

## Commit These to Git

Commit these project files — your team benefits from the same setup:
- `.claudeignore` — shared ignore rules
- `.topiccontext/*.json` — shared topic maps
- `CLAUDE.md` — shared project memory

Add these to `.gitignore` (personal, not shared):
- `.topiccontext/.active` — your personal active session state

---

## Uninstall

**Mac / Linux:**
```bash
./uninstall.sh
```

**Windows:**
```powershell
Remove-Item -Recurse "$env:USERPROFILE\.claude\skills\context-manager"
```

Your project `.claudeignore` and `.topiccontext/` files are NOT removed.

---

## Troubleshooting

**Skill not showing up in Claude Code:**
- Make sure Claude Code is installed: `claude --version`
- Check the install location: `ls ~/.claude/skills/` (Mac/Linux) or `dir $env:USERPROFILE\.claude\skills\` (Windows)
- Restart Claude Code after installing

**Python script errors:**
- Make sure Python 3 is installed: `python3 --version`
- On Windows, try `python` instead of `python3`

**`/tokenstatus` shows wrong numbers:**
- The token count is an estimate (~4 chars/token). Actual numbers vary by file content.
- Run from your project root directory.

**Topic context not working:**
- Make sure you ran `/topiccontext create <name>` first
- Check `.topiccontext/<name>.json` exists in your project root

---

## Contributing

PRs welcome! Ideas for improvements:
- Support for more project types in the ignore template
- VS Code / Cursor extension wrapper
- Token tracking that reads Claude Code's actual usage logs
- Auto-detect common project structures and suggest topic groups

---

## License

MIT — use freely, attribution appreciated.

---

## Credits

Built for developers using [Claude Code](https://claude.ai/code) who want to work faster with less token waste.
