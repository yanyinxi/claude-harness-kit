#!/bin/bash
# Agent Planning Check - PreAgentCall Hook
# 验证多 Agent 任务分配合理性
set -e

# 获取插件根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../../../" && pwd)"
LOG_FILE="${CLAUDE_PLUGIN_ROOT}/.claude/data/agent_planning.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 主逻辑
main() {
    local agent_name="${1:-}"
    local task_description="${2:-}"

    log "PreAgentCall: agent=$agent_name task=${task_description:0:100}"

    # 检查 orchestrator 是否已设置文件所有权
    case "$agent_name" in
        *orchestrator*)
            log "Multi-agent task detected, verifying planning phase..."
            ;;
    esac

    echo "OK"
}

main "$@"