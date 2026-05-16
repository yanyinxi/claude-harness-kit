#!/bin/bash
# checkpoint-auto-save.sh — PreToolUse Hook: 检测 /compact 并自动保存 checkpoint
# 设计：永远 exit 0，checkpoint 保存失败不阻断工具调用
set -uo pipefail

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

HOOK_DATA=$(cat 2>/dev/null) || HOOK_DATA=""
[[ -z "$HOOK_DATA" ]] && exit 0

CONTENT=$(echo "$HOOK_DATA" | python3 -c "
import json, sys
d = json.load(sys.stdin)
msg = d.get('message', {})
content = msg.get('content', '')
if isinstance(content, list):
    for b in content:
        if isinstance(b, dict):
            t = b.get('text', '')
            if t:
                print(t, end='')
elif isinstance(content, str):
    print(content, end='')
" 2>/dev/null) || { exit 0; }

if ! echo "$CONTENT" | grep -qi '/compact\|/checkpoint\s*save'; then
    exit 0
fi

CHECKPOINT_DIR="${PLUGIN_ROOT}/.claude/checkpoints"
mkdir -p "$CHECKPOINT_DIR"

SESSION_ID=$(echo "$HOOK_DATA" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('sessionId', 'default'))
" 2>/dev/null) || SESSION_ID="default"

SESSION_STATE="${CHECKPOINT_DIR}/.auto-save-${SESSION_ID}.json"
export CHK_SESSION_STATE="$SESSION_STATE"

# 将 Python 脚本写入临时文件，避免 heredoc 覆盖 stdin
SCRIPT_FILE=$(mktemp)
trap 'rm -f "$SCRIPT_FILE"' EXIT

cat > "$SCRIPT_FILE" << 'PYEOF'
import json, sys, datetime, os
d = json.load(sys.stdin)
ts = datetime.datetime.utcnow().isoformat() + 'Z'
session = d.get('sessionId', 'unknown')
msg = d.get('message', {})
content = msg.get('content', '')
text = ''
if isinstance(content, list):
    for b in content:
        if isinstance(b, dict):
            text += b.get('text', '') + ' '
elif isinstance(content, str):
    text = content
# 通过环境变量获取 SESSION_STATE，避免路径注入风险
session_state = os.environ.get('CHK_SESSION_STATE', '/tmp/checkpoint.json')
data = {
    'timestamp': ts,
    'session_id': session,
    'checkpoint_name': 'auto-' + ts[:10],
    'message_preview': text[:200],
    'auto_saved': True
}
with open(session_state, 'w') as f:
    json.dump(data, f, ensure_ascii=False)
PYEOF
export CHK_SESSION_STATE="$SESSION_STATE"
echo "$HOOK_DATA" | python3 "$SCRIPT_FILE" 2>/dev/null || true

echo "Auto-checkpoint saved to ${SESSION_STATE}" >&2
exit 0
