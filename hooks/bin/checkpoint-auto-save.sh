#!/bin/bash
# checkpoint-auto-save.sh — PreToolUse hook: detect /compact and auto-save checkpoint
# Called by Claude Code before tool execution. Detects /compact in message content.

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Read hook data from stdin
HOOK_DATA="$(cat)"
[[ -z "$HOOK_DATA" ]] && exit 0

# Extract message content
CONTENT=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
msg=d.get('message',{})
content=msg.get('content','')
if isinstance(content,list):
    for b in content:
        if isinstance(b,dict):
            t=b.get('text','')
            if t: print(t,end='')
elif isinstance(content,str):
    print(content,end='')
" 2>/dev/null) || exit 0

# Check for /compact trigger
if ! echo "$CONTENT" | grep -qi '/compact\|/checkpoint\s*save'; then
  exit 0
fi

CHECKPOINT_DIR="${PLUGIN_ROOT}/.claude/checkpoints"
mkdir -p "$CHECKPOINT_DIR"

TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
SESSION_ID=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d.get('sessionId','default'))
" 2>/dev/null) || SESSION_ID="default"

SESSION_STATE="${CHECKPOINT_DIR}/.auto-save-${SESSION_ID}.json"

# Collect basic checkpoint data from hook data
echo "$HOOK_DATA" | python3 -c "
import json,sys,datetime
d=json.load(sys.stdin)
ts=datetime.datetime.utcnow().isoformat()+'Z'
# Basic extraction
session=d.get('sessionId','unknown')
msg=d.get('message',{})
content=msg.get('content','')
text=''
if isinstance(content,list):
    for b in content:
        if isinstance(b,dict):
            text+=b.get('text','')+' '
elif isinstance(content,str):
    text=content
data={
    'timestamp': ts,
    'session_id': session,
    'checkpoint_name': 'auto-${ts[:10]}',
    'message_preview': text[:200],
    'auto_saved': True
}
with open('${SESSION_STATE}','w') as f:
    json.dump(data,f,ensure_ascii=False)
" 2>/dev/null

echo "Auto-checkpoint saved to ${SESSION_STATE}" >&2
exit 0