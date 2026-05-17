#!/bin/bash
# ============================================================
# CHK 会话状态清理脚本
#
# 功能：
# - 清理当前会话的状态文件
# - 或清理所有会话状态（次日首次启动时）
#
# 使用方式：
#   bash hooks/bin/memory-cleanup.sh           # 清理当前会话
#   bash hooks/bin/memory-cleanup.sh --all     # 清理所有会话
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_ROOT/.claude/data"

# 会话 ID
SESSION_ID="${CLAUDE_CODE_SESSION_ID:-}"
STATE_FILE="$DATA_DIR/.memory_session_${SESSION_ID}.json"

cleanup_current() {
    if [ -n "$SESSION_ID" ] && [ -f "$STATE_FILE" ]; then
        rm -f "$STATE_FILE"
        echo "已清理当前会话状态: $STATE_FILE"
    else
        echo "无当前会话状态需要清理"
    fi
}

cleanup_all() {
    local count=0
    for f in "$DATA_DIR"/.memory_session_*.json; do
        if [ -f "$f" ]; then
            rm -f "$f"
            count=$((count + 1))
        fi
    done
    echo "已清理所有会话状态: $count 个"

    # 清理冷却文件
    rm -f "$DATA_DIR"/.memory_inject_cooldown
}

case "${1:-}" in
    --all)
        cleanup_all
        ;;
    *)
        cleanup_current
        ;;
esac