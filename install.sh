#!/usr/bin/env bash
# Install the name-wizard slash command, sub-agents, and domain-check script
# into Claude Code's config directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
COMMANDS_DIR="$CLAUDE_DIR/commands"
AGENTS_DIR="$CLAUDE_DIR/agents"
TOOLS_DIR="$CLAUDE_DIR/name-wizard"

mkdir -p "$COMMANDS_DIR" "$AGENTS_DIR" "$TOOLS_DIR"

cp "$SCRIPT_DIR/name-wizard.md" "$COMMANDS_DIR/name-wizard.md"
echo "Installed /name-wizard            -> $COMMANDS_DIR/name-wizard.md"

for agent in "$SCRIPT_DIR"/agents/*.md; do
  name="$(basename "$agent")"
  cp "$agent" "$AGENTS_DIR/$name"
  echo "Installed agent                   -> $AGENTS_DIR/$name"
done

cp "$SCRIPT_DIR/scripts/check_domains.py" "$TOOLS_DIR/check_domains.py"
chmod +x "$TOOLS_DIR/check_domains.py"
echo "Installed domain check script     -> $TOOLS_DIR/check_domains.py"

echo ""
echo "Done. Restart Claude Code (or open a new session) and run /name-wizard."
