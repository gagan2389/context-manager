# Ignore Patterns Reference

Quick reference for common `.claudeignore` patterns by project type.
Run `/ignore init` to apply the full default template.

---

## By Project Type

### Node.js / React / Next.js
```
node_modules/
dist/
.next/
.turbo/
package-lock.json
yarn.lock
*.map
```

### Python / Django / FastAPI
```
__pycache__/
.venv/
*.pyc
.pytest_cache/
htmlcov/
poetry.lock
```

### Rust
```
target/
Cargo.lock
```

### Go
```
vendor/
```

### Monorepo (Turborepo / Nx)
```
node_modules/
dist/
.turbo/
.nx/cache/
**/node_modules/
**/dist/
```

---

## Always Safe to Ignore

These are safe for almost every project:

```
# Secrets
.env
.env.*
*.key
*.pem

# OS junk
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Coverage
coverage/
.nyc_output/

# IDE
.idea/
.vscode/

# Binaries & media
*.png *.jpg *.zip *.pdf *.mp4

# Minified
*.min.js *.min.css *.map
```

---

## Patterns Syntax

| Pattern | What it matches |
|---|---|
| `node_modules/` | That exact directory anywhere |
| `*.log` | All .log files recursively |
| `dist/` | dist directory at any level |
| `src/generated/` | Exact path from project root |
| `**/*.test.ts` | All .test.ts files everywhere |
| `!important.log` | Negation — do NOT ignore this |

---

## Token Savings Estimates

| What you ignore | Typical savings |
|---|---|
| `node_modules/` | 50,000–500,000 tokens |
| `*.lock` files | 5,000–20,000 tokens |
| `dist/build/` | 10,000–100,000 tokens |
| `coverage/` | 2,000–15,000 tokens |
| `*.map` files | 1,000–10,000 tokens |
| `*.log` files | varies widely |
