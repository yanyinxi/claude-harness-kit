#!/bin/bash
# Agent Result Sync - PostAgentCall Hook
# 同步 Agent 执行结果到 mailbox
set -e

# 获取插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../../../" && pwd)"
LOG_FILE="${CLAUDE_PLUGIN_ROOT}/.claude/data/agent_result.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 主逻辑
main() {
    local agent_name="${1:-}"
    local exit_code="${2:-0}"
    local output_file="${3:-}"

    log "PostAgentCall: agent=$agent_name exit=$exit_code output=$output_file"

    # 同步结果到 mailbox
    if [[ -n "$output_file" ]] && [[ -f "$output_file" ]]; then
        log "Syncing result from $output_file"
    fi

    echo "OK"
}

main "$@"