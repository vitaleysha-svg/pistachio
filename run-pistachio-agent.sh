#!/bin/bash
# Pistachio Autonomous Intelligence Agent
# Run ONLY when Matt specifically requests it
# NOT part of overnight agent system

set -e

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
PISTACHIO_DIR="/Users/mateuszjez/Desktop/pistachio"

echo "========================================"
echo "Pistachio Agent - $DATE $TIME"
echo "========================================"
echo ""
echo "Goal: \$30k/month in 60 days"
echo "Partners: Matt + VS"
echo ""
echo "Agent will:"
echo "  - Read all Pistachio context"
echo "  - Think about what the business needs"
echo "  - Research autonomously"
echo "  - Rank by impact on \$30k goal"
echo "  - Output briefing"
echo ""

mkdir -p "$PISTACHIO_DIR/autonomous-research"

claude -p "
$(cat $PISTACHIO_DIR/agents/pistachio-agent-v2.md)

TODAY: $DATE
"

echo ""
echo "========================================"
echo "Complete"
echo "========================================"
echo "Briefing: $PISTACHIO_DIR/autonomous-research/briefing-$DATE.md"
