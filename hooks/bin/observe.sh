#!/bin/bash
# observe.sh — PreToolUse + PostToolUse + UserPromptSubmit Hook: 自动捕获观测事件
# Usage: Called by Claude Code hooks，读取 HOOK_DATA JSON 从 stdin

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OBS_DIR="${PLUGIN_ROOT}/.claude/homunculus"
mkdir -p "$OBS_DIR"
OBS_LOG="${OBS_DIR}/observations.jsonl"

# ── Read hook data ──────────────────────────────────────────────────────────────

HOOK_DATA="$(cat)"
[[ -z "$HOOK_DATA" ]] && exit 0

# Extract basic info
SESSION_ID=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(d.get('sessionId','unknown'))
" 2>/dev/null) || SESSION_ID="unknown"

HOOK_TYPE=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
# Infer hook type from presence of fields
if 'message' in d:
    msg = d.get('message',{})
    content = str(msg.get('content',''))
    if msg.get('type') == 'user': print('UserPromptSubmit')
    elif 'name' in msg: print('ToolCall:' + msg.get('name',''))
else:
    print('Unknown')
" 2>/dev/null) || HOOK_TYPE="Unknown"

TOOL_NAME=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
msg=d.get('message',{})
print(msg.get('name',''))
" 2>/dev/null) || TOOL_NAME=""

MSG_CONTENT=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
msg=d.get('message',{})
content=msg.get('content','')
if isinstance(content,list):
    for b in content:
        if isinstance(b,dict):
            t=b.get('text','')
            if t: print(t[:500],end='')
elif isinstance(content,str):
    print(content[:500],end='')
" 2>/dev/null) || MSG_CONTENT=""

# ── Event extraction ───────────────────────────────────────────────────────────

# UserPromptSubmit: detect feedback patterns
FEEDBACK=""
if [[ "$HOOK_TYPE" == "UserPromptSubmit" ]]; then
    if echo "$MSG_CONTENT" | grep -qi "不对\|not right\|wrong\|错了\|incorrect\|should be\|应该\|改成\|change to\|fix\|修正"; then
        FEEDBACK="correction"
    elif echo "$MSG_CONTENT" | grep -qi "好\|good\|correct\|可以\|ok\|perfect\|很好"; then
        FEEDBACK="approval"
    elif echo "$MSG_CONTENT" | grep -qi "不对\|no\|don't\|stop\|别"; then
        FEEDBACK="rejection"
    fi
fi

# ToolCall: extract patterns
TOOL_PATTERNS=""
if [[ "$TOOL_NAME" == "Read" ]]; then
    FILE=$(echo "$HOOK_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin)
msg=d.get('message',{})
content=msg.get('content','')
if isinstance(content,list):
    for b in content:
        if isinstance(b,dict) and b.get('type')=='input':
            for inp in b.get('inputs',[]):
                if inp.get('name')=='file_path':
                    print(inp.get('file_path',''),end='')
" 2>/dev/null) || FILE=""
    if [[ -n "$FILE" ]]; then
        EXT="${FILE##*.}"
        TOOL_PATTERNS="file_type:$EXT"
    fi
elif [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
    PATTERN="code_write"
    if echo "$MSG_CONTENT" | grep -qi "test\|spec"; then
        PATTERN="test_write"
    elif echo "$MSG_CONTENT" | grep -qi "config\|setup"; then
        PATTERN="config_write"
    fi
    TOOL_PATTERNS="$PATTERN"
fi

# ── Write observation ──────────────────────────────────────────────────────────

if [[ -n "$FEEDBACK" ]] || [[ -n "$TOOL_PATTERNS" ]]; then
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    python3 -c "
import json,sys
entry = {
    'timestamp': '${TS}',
    'session_id': '${SESSION_ID}',
    'hook_type': '${HOOK_TYPE}',
    'tool': '${TOOL_NAME}',
}
" > /dev/null

    # Append to log
    echo "{\"timestamp\":\"${TS}\",\"session_id\":\"${SESSION_ID}\",\"hook_type\":\"${HOOK_TYPE}\",\"tool\":\"${TOOL_NAME}\",\"feedback\":\"${FEEDBACK}\",\"patterns\":\"${TOOL_PATTERNS}\"}" >> "$OBS_LOG" 2>/dev/null || true
fi

exit 0