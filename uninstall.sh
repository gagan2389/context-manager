#!/bin/bash
# Uninstall context-manager skill

INSTALL_DIR="$HOME/.claude/skills/context-manager"

echo ""
echo "🗑️  Uninstalling context-manager..."

if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "✅ Removed $INSTALL_DIR"
else
    echo "ℹ️  Not installed at $INSTALL_DIR"
fi

echo ""
echo "Note: Your project .claudeignore files and .topiccontext/ folders"
echo "are NOT removed — they live in your projects and can be kept."
echo ""
