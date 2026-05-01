#!/bin/bash
# rate-limiter.sh — Claude Code API Rate Limiter (Sliding Window)
# Usage: Called by Claude Code hooks，检测 API 调用频率，超限则阻断

set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RATE_DIR="${PLUGIN_ROOT}/.claude/rate-limits"
mkdir -p "$RATE_DIR"
STATE_FILE="${RATE_DIR}/state.json"

# ── Rate Limits ────────────────────────────────────────────────────────────────
LIMIT_MIN=30    # 30 requests/minute
LIMIT_HR=500    # 500 requests/hour
LIMIT_DAY=5000  # 5000 requests/day

# ── Helpers ──────────────────────────────────────────────────────────────────

log_warn() { echo "⚠️  rate-limiter: $*" >&2; }
log_block() { echo "🔴 rate-limiter: BLOCKED — $*" >&2; }

# Acquire flock to prevent concurrent writes
acquire_lock() {
    LOCK_FD=200
    flock -n $LOCK_FD || { log_warn "Another instance is updating rate state"; exit 0; }
}

# Load or initialize state
load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        python3 -c "
import json,sys
d=json.load(open('${STATE_FILE}'))
print(json.dumps(d))
" 2>/dev/null || echo '{"minute":[],"hour":[],"day":[]}'
    else
        echo '{"minute":[],"hour":[],"day":[]}'
    fi
}

save_state() {
    python3 -c "
import json,sys
d=json.load(sys.stdin)
with open('${STATE_FILE}','w') as f:
    json.dump(d,f)
" <<< "$1" 2>/dev/null
}

clean_old() {
    local now_ms=$(python3 -c "import time; print(int(time.time()*1000))")
    local window_min=$((60 * 1000))
    local window_hr=$((3600 * 1000))
    local window_day=$((86400 * 1000))

    python3 -c "
import json,sys,json as j
d=json.loads(sys.stdin.read())
now=int(sys.argv[1])
for key,window in [('minute',${window_min}),('hour',${window_hr}),('day',${window_day})]:
    d[key]=[t for t in d.get(key,[]) if now-t < window]
print(json.dumps(d))
" "$now_ms"
}

# Check and record
check_limits() {
    local now_ms
    now_ms=$(python3 -c "import time; print(int(time.time()*1000))")

    local state
    state=$(load_state)
    state=$(clean_old <<< "$state")

    local cnt_min=$(python3 -c "import json; d=json.loads('${state}'); print(len(d.get('minute',[])))")
    local cnt_hr=$(python3 -c "import json; d=json.loads('${state}'); print(len(d.get('hour',[])))")
    local cnt_day=$(python3 -c "import json; d=json.loads('${state}'); print(len(d.get('day',[])))")

    if (( cnt_min >= LIMIT_MIN )); then
        log_block "Minute limit exceeded: $cnt_min/$LIMIT_MIN"
        echo "{\"status\":\"blocked\",\"reason\":\"minute_limit\",\"current\":$cnt_min,\"limit\":$LIMIT_MIN}" >&2
        exit 2
    fi
    if (( cnt_hr >= LIMIT_HR )); then
        log_block "Hour limit exceeded: $cnt_hr/$LIMIT_HR"
        echo "{\"status\":\"blocked\",\"reason\":\"hour_limit\",\"current\":$cnt_hr,\"limit\":$LIMIT_HR}" >&2
        exit 2
    fi
    if (( cnt_day >= LIMIT_DAY )); then
        log_block "Day limit exceeded: $cnt_day/$LIMIT_DAY"
        echo "{\"status\":\"blocked\",\"reason\":\"day_limit\",\"current\":$cnt_day,\"limit\":$LIMIT_DAY}" >&2
        exit 2
    fi

    # Record this request
    local new_state
    new_state=$(python3 -c "
import json
d=json.loads('${state}')
now=int(sys.argv[1])
for key in ['minute','hour','day']:
    d.setdefault(key,[]).append(now)
print(json.dumps(d))
" "$now_ms")
    save_state "$new_state"

    echo "{\"status\":\"ok\",\"minute\":$((cnt_min+1))/$LIMIT_MIN,\"hour\":$((cnt_hr+1))/$LIMIT_HR,\"day\":$((cnt_day+1))/$LIMIT_DAY}" >&2
    exit 0
}

# ── Main ──────────────────────────────────────────────────────────────────────

# Read stdin but don't fail if empty
HOOK_DATA="$(cat 2>/dev/null || echo '{}')"

# Check limits (always run)
check_limits