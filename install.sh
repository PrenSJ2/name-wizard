#!/usr/bin/env bash
# Install the name-wizard slash command and its sub-agents into Claude Code.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
COMMANDS_DIR="$CLAUDE_DIR/commands"
AGENTS_DIR="$CLAUDE_DIR/agents"

mkdir -p "$COMMANDS_DIR" "$AGENTS_DIR"

cp "$SCRIPT_DIR/name-wizard.md" "$COMMANDS_DIR/name-wizard.md"
echo "Installed /name-wizard -> $COMMANDS_DIR/name-wizard.md"

for agent in "$SCRIPT_DIR"/agents/*.md; do
  name="$(basename "$agent")"
  cp "$agent" "$AGENTS_DIR/$name"
  echo "Installed agent -> $AGENTS_DIR/$name"
done

echo ""
echo "Done. Restart Claude Code (or open a new session) and run /name-wizard."
