#!/usr/bin/env bash
# Pistachio Autonomous Intelligence Agent (portable launcher)
# Usage:
#   ./run-pistachio-agent.sh
#   DRY_RUN=1 ./run-pistachio-agent.sh
# Optional env:
#   PISTACHIO_DIR=/abs/path/to/repo
#   AGENT_PROMPT_FILE=/abs/path/to/agents/pistachio-agent-v2.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PISTACHIO_DIR="${PISTACHIO_DIR:-$SCRIPT_DIR}"
AGENT_PROMPT_FILE="${AGENT_PROMPT_FILE:-$PISTACHIO_DIR/agents/pistachio-agent-v2.md}"
OUTPUT_DIR="$PISTACHIO_DIR/autonomous-research"
DATE="$(date +%Y-%m-%d)"
TIME="$(date +%H:%M)"

if ! command -v claude >/dev/null 2>&1; then
  echo "ERROR: 'claude' command not found in PATH." >&2
  exit 1
fi

if [[ ! -f "$AGENT_PROMPT_FILE" ]]; then
  echo "ERROR: Agent prompt file not found: $AGENT_PROMPT_FILE" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

AGENT_PROMPT="$(cat "$AGENT_PROMPT_FILE")"
RUNTIME_CONTEXT=$(cat <<EOF

RUNTIME CONTEXT
- project_root: $PISTACHIO_DIR
- output_dir: $OUTPUT_DIR
- today: $DATE

Execution requirements:
1. Write final briefing to $OUTPUT_DIR/briefing-$DATE.md.
2. Update memory.md, pending-tasks.md, and predictions.md in $OUTPUT_DIR.
3. Treat archive/ files as non-authoritative unless explicitly asked.
EOF
)

FINAL_PROMPT="$AGENT_PROMPT
$RUNTIME_CONTEXT"

echo "========================================"
echo "Pistachio Agent - $DATE $TIME"
echo "========================================"
echo "Project root: $PISTACHIO_DIR"
echo "Prompt file: $AGENT_PROMPT_FILE"
echo "Output dir: $OUTPUT_DIR"

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "DRY_RUN=1 set. Prompt preview only."
  echo "----------------------------------------"
  echo "$FINAL_PROMPT"
  echo "----------------------------------------"
  exit 0
fi

claude -p "$FINAL_PROMPT"

echo "========================================"
echo "Complete"
echo "========================================"
echo "Briefing target: $OUTPUT_DIR/briefing-$DATE.md"
