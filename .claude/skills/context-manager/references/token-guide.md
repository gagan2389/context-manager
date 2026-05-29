# Token Estimation Guide

How the context manager estimates token usage and savings.

---

## How Token Counting Works

Claude uses a BPE (byte-pair encoding) tokenizer. A rough heuristic:
- **~4 characters = 1 token** for English/code
- **~3 characters = 1 token** for dense code (lots of symbols)
- **~6 characters = 1 token** for verbose prose

The scripts in this skill use 4 chars/token as the default estimate.

---

## Claude's Context Window (as of 2025)

| Model | Context Window |
|---|---|
| Claude 3.5 Sonnet | 200,000 tokens |
| Claude 3 Opus | 200,000 tokens |
| Claude 3 Haiku | 200,000 tokens |

**Practical limit:** Claude Code typically keeps 50,000–80,000 tokens for the
actual conversation, tool use, and output. The remaining window is available
for file context.

---

## What Uses Tokens in a Session

1. **System prompt** — ~2,000–5,000 tokens (Claude Code internals)
2. **CLAUDE.md files** — loaded every session, can be 500–5,000 tokens
3. **Files read** — biggest variable; depends on what Claude opens
4. **Conversation history** — grows as the session continues
5. **Tool outputs** — bash results, file listings, etc.

---

## Token Saving Strategies (ranked by impact)

### 1. Ignore large generated folders (biggest win)
`node_modules/` alone can be 500k+ tokens. Always ignore it.

### 2. Use topic context for large projects
A 200-file project might have 150,000 tokens. Scoping to a 20-file topic
brings that to ~15,000 — a 10x reduction.

### 3. Use /filecontext for single-file tasks
If you only need to work on `auth.ts`, pin it. Claude won't pull in imports.

### 4. Keep CLAUDE.md lean
Every line in CLAUDE.md costs tokens on every session. Keep it under 200 lines.

### 5. Use /compact when context is large
Claude Code's built-in `/compact` command summarizes history to free up window.

---

## Example Token Budget

For a typical Next.js project (200 files, 80k tokens total):

```
Without context-manager:
  All project files:     ~80,000 tokens
  node_modules:          NOT read (Claude Code is smart about this)
  dist/:                 ~5,000 tokens
  *.map files:           ~3,000 tokens
  Logs, coverage:        ~2,000 tokens
  Effective exposure:    ~50,000 tokens

With context-manager:
  .claudeignore applied:  -10,000 tokens saved
  /usetopiccontext hoto:  restrict to 20 files = ~8,000 tokens
  Net context needed:     ~8,000 tokens (84% reduction!)
```
