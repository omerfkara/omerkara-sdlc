#!/bin/bash
# Auto-update script for omerkara-sdlc skill
# Usage: ./update.sh
#    or: bash ~/.claude/skills/omerkara-sdlc/update.sh

set -e

SKILL_PATH="${HOME}/.claude/skills/omerkara-sdlc"

echo "📦 Updating omerkara-sdlc skill..."
echo ""

if [ ! -d "$SKILL_PATH" ]; then
    echo "❌ Skill not found at $SKILL_PATH"
    echo ""
    echo "Install first with:"
    echo "  git clone https://github.com/omerfkara/omerkara-sdlc.git $SKILL_PATH"
    exit 1
fi

echo "📂 Checking repository at: $SKILL_PATH"
cd "$SKILL_PATH"

echo "🔄 Fetching latest changes..."
git fetch origin main

echo "📥 Pulling latest version..."
git pull origin main

echo ""
echo "✅ omerkara-sdlc is up to date!"
echo ""
echo "Latest changes:"
git log --oneline -n 3
echo ""
echo "Version info:"
git describe --tags 2>/dev/null || echo "No version tags yet"
echo ""
echo "Next: Restart Claude Code and use /omerkara-sdlc"
