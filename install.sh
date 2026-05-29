#!/bin/bash
# ============================================================
#  Context Manager for Claude Code — Installer
#  Installs the skill globally so it works in every project.
# ============================================================

set -e

SKILL_NAME="context-manager"
INSTALL_DIR="$HOME/.claude/skills/$SKILL_NAME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/.claude/skills/$SKILL_NAME"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   Context Manager — Claude Code Skill Installer  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "⚠️  Python 3 is required but not found."
    echo "   Install it from https://python.org and re-run this script."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check if Claude Code config dir exists
if [ ! -d "$HOME/.claude" ]; then
    echo ""
    echo "⚠️  ~/.claude directory not found."
    echo "   Make sure Claude Code is installed first:"
    echo "   npm install -g @anthropic-ai/claude-code"
    echo ""
    read -p "   Create ~/.claude anyway? [y/N]: " ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
        mkdir -p "$HOME/.claude/skills"
    else
        echo "Cancelled."
        exit 1
    fi
fi

# Create skills directory if needed
mkdir -p "$HOME/.claude/skills"

# Backup existing install if present
if [ -d "$INSTALL_DIR" ]; then
    BACKUP="$INSTALL_DIR.backup.$(date +%Y%m%d_%H%M%S)"
    echo ""
    echo "ℹ️  Existing install found. Backing up to:"
    echo "   $BACKUP"
    mv "$INSTALL_DIR" "$BACKUP"
fi

# Copy skill files
echo ""
echo "📦 Installing to: $INSTALL_DIR"
cp -r "$SOURCE_DIR" "$INSTALL_DIR"

# Make scripts executable
chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   ✅  Installation complete!                      ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "The skill is now available in ALL your Claude Code projects."
echo ""
echo "Quick start:"
echo "  1. Open Claude Code in any project"
echo "  2. Type: /ignore init          ← set up ignore list"
echo "  3. Type: /tokenstatus          ← see current token usage"
echo "  4. Type: /topiccontext create hoto   ← create a topic scope"
echo "  5. Type: /usetopiccontext hoto ← activate topic scope"
echo ""
echo "For help, see: https://github.com/gagan2389/context-manager"
echo ""
