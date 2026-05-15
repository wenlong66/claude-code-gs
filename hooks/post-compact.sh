#!/usr/bin/env shell
if [ -d "/c/Progra~1/Git/usr/bin" ]; then
  export PATH="/c/Progra~1/Git/usr/bin:/c/Progra~1/Git/bin:$PATH"
fi
# post-compact.sh — fires after conversation compaction
# Reminds Codex to restore session state from the file-backed checkpoint.

ACTIVE="production/session-state/active.md"

echo "=== Context Restored After Compaction ==="

if [ -f "$ACTIVE" ]; then
  SIZE=$(wc -l < "$ACTIVE" 2>/dev/null || echo "?")
  echo "Session state file exists: $ACTIVE ($SIZE lines)"
  echo "IMPORTANT: Read this file now to restore your working context."
  echo "It contains: current spawn_agent, decisions made, files in progress, open questions."
else
  echo "No session state file found at $ACTIVE"
  echo "If you were mid-spawn_agent, check production/session-logs/ for the last session audit."
fi

echo "========================================="
