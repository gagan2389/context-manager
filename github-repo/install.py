#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          Context Manager for Claude Code — Installer         ║
║                                                              ║
║  Single-file installer. Run once and the skill is globally   ║
║  available in every Claude Code project on this machine.     ║
║                                                              ║
║  Usage:  python3 install.py                                  ║
║  Remove: python3 install.py --uninstall                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import os, sys, base64, zipfile, io, shutil, datetime, platform

# ── Embedded skill bundle (base64-encoded zip) ──────────────────────────────
SKILL_BUNDLE_B64 = "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fGikGDnqo6g0jXo6oL+SHF+p6H7Ot+MYgVKxPOU6r7GLdTL0MN5MJugZEX9GEbfEUUSxPopsX2wC/+R/UEsBAhQDFAAAAAgA6xK9XOEY0XvpBwAArBMAACcAAAAAAAAAAAAAAKSBAAAAAC5jbGF1ZGUvc2tpbGxzL2NvbnRleHQtbWFuYWdlci9TS0lMTC5tZFBLAQIUAxQAAAAIADkTvVz93TENowQAAHsJAAA4AAAAAAAAAAAAAACkgS4IAAAuY2xhdWRlL3NraWxscy9jb250ZXh0LW1hbmFnZXIvcmVmZXJlbmNlcy90b2tlbi1ndWlkZS5tZFBLAQIUAxQAAAAIADETvVxqwjj3IAMAABIGAAA8AAAAAAAAAAAAAACkgScNAAAuY2xhdWRlL3NraWxscy9jb250ZXh0LW1hbmFnZXIvcmVmZXJlbmNlcy9pZ25vcmUtcGF0dGVybnMubWRQSwECFAMUAAAACAArE71cud3TSt4DAADWEAAAPAAAAAAAAAAAAAAApIGhEAAALmNsYXVkZS9za2lsbHMvY29udGV4dC1tYW5hZ2VyL2Fzc2V0cy8uY2xhdWRlaWdub3JlLnRlbXBsYXRlUEsBAhQDFAAAAAgAIxO9XLatooZ/BQAA3xMAADcAAAAAAAAAAAAAAO2B2RQAAC5jbGF1ZGUvc2tpbGxzL2NvbnRleHQtbWFuYWdlci9zY3JpcHRzL3RvcGljX21hbmFnZXIucHlQSwECFAMUAAAACAANE71clu6EnU4KAAD1IgAANgAAAAAAAAAAAAAA7YGtGgAALmNsYXVkZS9za2lsbHMvY29udGV4dC1tYW5hZ2VyL3NjcmlwdHMvdG9rZW5fc3RhdHVzLnB5UEsBAhQDFAAAAAgAFxO9XK/wVAQLBgAA5BAAADYAAAAAAAAAAAAAAO2BTyUAAC5jbGF1ZGUvc2tpbGxzL2NvbnRleHQtbWFuYWdlci9zY3JpcHRzL2FwcGx5X2lnbm9yZS5weVBLAQIUAxQAAAAIAPkSvVy3olxs8ggAAFsZAAA6AAAAAAAAAAAAAADtga4rAAAuY2xhdWRlL3NraWxscy9jb250ZXh0LW1hbmFnZXIvc2NyaXB0cy9idWlsZF90b3BpY190cmVlLnB5UEsFBgAAAAAIAAgAJAMAAPg0AAAAAA=="
# ────────────────────────────────────────────────────────────────────────────

SKILL_NAME   = "context-manager"
WIN          = platform.system() == "Windows"
HOME         = os.path.expanduser("~")
CLAUDE_DIR   = os.path.join(HOME, ".claude")
SKILLS_DIR   = os.path.join(CLAUDE_DIR, "skills")
INSTALL_DIR  = os.path.join(SKILLS_DIR, SKILL_NAME)

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          Context Manager for Claude Code                     ║
╚══════════════════════════════════════════════════════════════╝
"""

def hr(char="─", n=62):
    return char * n

def check_python():
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print(f"  ✗  Python 3.8+ required. You have {major}.{minor}")
        sys.exit(1)
    print(f"  ✓  Python {major}.{minor}")

def check_claude_code():
    claude_exists = os.path.isdir(CLAUDE_DIR)
    if not claude_exists:
        print(f"\n  ⚠  ~/.claude not found.")
        print(f"     Claude Code may not be installed yet.")
        print(f"     Install: npm install -g @anthropic-ai/claude-code")
        ans = input("\n  Create ~/.claude and install anyway? [y/N]: ").strip().lower()
        if ans != "y":
            print("  Cancelled.")
            sys.exit(0)
    else:
        print(f"  ✓  Claude Code config found at {CLAUDE_DIR}")

def backup_existing():
    if os.path.isdir(INSTALL_DIR):
        ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = f"{INSTALL_DIR}.backup.{ts}"
        shutil.move(INSTALL_DIR, bak)
        print(f"  ↩  Previous install backed up → {bak}")

def extract_bundle():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    data  = base64.b64decode(SKILL_BUNDLE_B64)
    buf   = io.BytesIO(data)
    count = 0
    with zipfile.ZipFile(buf, "r") as zf:
        for info in zf.infolist():
            # Strip leading ".claude/skills/context-manager/" so files land
            # directly under INSTALL_DIR
            prefix = ".claude/skills/context-manager/"
            rel    = info.filename
            if rel.startswith(prefix):
                rel = rel[len(prefix):]
            if not rel:          # top-level directory entry
                continue
            dest = os.path.join(INSTALL_DIR, rel.replace("/", os.sep))
            if info.filename.endswith("/"):
                os.makedirs(dest, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with zf.open(info) as src, open(dest, "wb") as dst:
                    dst.write(src.read())
                # mark .py files executable on Unix
                if dest.endswith(".py") and not WIN:
                    os.chmod(dest, 0o755)
                count += 1
    return count

def install():
    print(BANNER)
    print(hr())
    print("  Checking requirements …")
    print(hr())
    check_python()
    check_claude_code()

    print()
    print(hr())
    print("  Installing …")
    print(hr())
    backup_existing()
    n = extract_bundle()
    print(f"  ✓  Installed {n} files → {INSTALL_DIR}")

    print()
    print(hr("═"))
    print("  ✅  Installation complete!")
    print(hr("═"))
    print()
    print("  The skill is available in ALL Claude Code projects now.")
    print()
    print("  First-time setup (run these in Claude Code):")
    print("    /ignore init                   — apply smart default ignore list")
    print("    /tokenstatus                   — see token usage report")
    print("    /topiccontext create project1  — map files for a topic area")
    print("    /usetopiccontext project1      — activate that topic scope")
    print()
    print("  Full command list:  /ignore | /filecontext | /topiccontext")
    print("                      /usetopiccontext | /tokenstatus | /remember")
    print("                      /scope | /clearcontext")
    print()
    print(f"  Docs: https://github.com/gagan2389/{SKILL_NAME}")
    print()

def uninstall():
    print(BANNER)
    if not os.path.isdir(INSTALL_DIR):
        print(f"  ℹ  Not installed at {INSTALL_DIR}")
        return
    ans = input(f"  Remove {INSTALL_DIR}? [y/N]: ").strip().lower()
    if ans == "y":
        shutil.rmtree(INSTALL_DIR)
        print("  ✓  Removed. Project .claudeignore and .topiccontext/ files are untouched.")
    else:
        print("  Cancelled.")

if __name__ == "__main__":
    if "--uninstall" in sys.argv or "-u" in sys.argv:
        uninstall()
    else:
        install()
