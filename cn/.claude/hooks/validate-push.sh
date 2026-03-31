#!/bin/bash
# Claude Code PreToolUse hook: Validates git push commands
# Receives JSON on stdin with tool_input.command
# Exit 0 = allow, Exit 2 = block (stderr shown to Claude)
#
# Input schema (PreToolUse for Bash):
# { "tool_name": "Bash", "tool_input": { "command": "git push ..." } }

INPUT=$(cat)

# Parse command -- use jq if available, fall back to grep
if command -v jq >/dev/null 2>&1; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
else
    COMMAND=$(echo "$INPUT" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"command"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

# Only process git push commands
if ! echo "$COMMAND" | grep -qE '^git[[:space:]]+push'; then
    exit 0
fi

# Check for uncommitted changes
UNSTAGED=$(git diff --name-only 2>/dev/null)
if [ -n "$UNSTAGED" ]; then
    echo "BLOCKED: You have uncommitted changes. Please commit or stash them first." >&2
    exit 2
fi

# Check for diverged branches
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$BRANCH" ] && [ "$BRANCH" != "HEAD" ]; then
    # Get remote branch
    REMOTE=$(git config branch."$BRANCH".remote 2>/dev/null || echo "origin")
    if [ -n "$REMOTE" ]; then
        # Check if branch exists on remote
        if git show-ref --quiet --verify "refs/remotes/$REMOTE/$BRANCH" 2>/dev/null; then
            # Check if we need to pull first
            LOCAL=$(git rev-parse "$BRANCH" 2>/dev/null)
            REMOTE_SHA=$(git rev-parse "$REMOTE/$BRANCH" 2>/dev/null)
            if [ -n "$LOCAL" ] && [ -n "$REMOTE_SHA" ]; then
                # Check if local is behind remote
                if git merge-base --is-ancestor "$LOCAL" "$REMOTE_SHA" 2>/dev/null; then
                    echo "BLOCKED: Your branch is behind the remote. Please pull before pushing." >&2
                    exit 2
                fi
            fi
        fi
    fi
fi

# Check for missing production planning (for branches other than feature branches)
if echo "$BRANCH" | grep -vE '^(feature|bugfix|hotfix)/'; then
    if [ ! -d "production/sprints" ] && [ ! -d "production/milestones" ]; then
        echo "WARNING: No production planning found (production/sprints/ or production/milestones/)" >&2
    fi
fi

exit 0