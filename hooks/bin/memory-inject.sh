#!/bin/bash
# ============================================================
# CHK 记忆注入钩子 - UserPromptSubmit
#
# 功能：
# - 会话首次输入时注入 L0 层（MEMORY.md 索引）
# - 每次输入检查关键词匹配 L1 层
# - 读取并注入高置信度本能（confidence >= 0.7）
# - 用户感知：显示"✓ 已记录"通知
#
# 触发时机：UserPromptSubmit（用户提交消息前）
# 输出位置：stdout（作为 hook 输出注入到系统提示）
# ============================================================

# ============================================================
# 配置
# ============================================================

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 记忆目录
MEMORY_DIR="$PROJECT_ROOT/harness/memory"
MEMORY_INDEX="$MEMORY_DIR/MEMORY.md"

# 状态目录
DATA_DIR="$PROJECT_ROOT/.claude/data"
mkdir -p "$DATA_DIR"

# 会话 ID
SESSION_ID="${CLAUDE_CODE_SESSION_ID:-$(date +%s)}"
STATE_FILE="$DATA_DIR/.memory_session_${SESSION_ID}.json"

# 日志
LOG_FILE="$DATA_DIR/memory_inject.log"

# ============================================================
# 工具函数
# ============================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE" 2>/dev/null
}

# 检查是否已注入 L0
is_L0_injected() {
    if [ -f "$STATE_FILE" ]; then
        injected=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('injected_L0', False))" 2>/dev/null)
        [ "$injected" = "True" ] && return 0 || return 1
    fi
    return 1
}

# 标记 L0 已注入
mark_L0_injected() {
    python3 -c "
import json
from datetime import datetime
state = {'session_id': '$SESSION_ID', 'injected_L0': True, 'injected_L0_at': datetime.now().isoformat()}
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
" 2>/dev/null
}

# 读取 MEMORY.md 摘要
read_memory_index() {
    if [ ! -f "$MEMORY_INDEX" ]; then
        echo ""
        return
    fi

    # 读取前 50 行（跳过详细的规则说明）
    head -n 50 "$MEMORY_INDEX"
}

# 读取高置信度本能
read_high_confidence_instincts() {
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from harness._core.instinct_reader import get_high_confidence_instincts, format_all_instincts_for_injection

instincts = get_high_confidence_instincts()
if instincts:
    print(format_all_instincts_for_injection(instincts))
" 2>/dev/null
}

# 关键词匹配
match_keywords() {
    local user_input="$1"

    # 使用环境变量传递，避免 shell 注入
    INPUT_FILE="$DATA_DIR/.keyword_input_$$"
    echo "$user_input" > "$INPUT_FILE"

    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from harness._core.keyword_matcher import match_keywords, format_matched_keywords

with open('$INPUT_FILE') as f:
    user_input = f.read().strip()

categories = match_keywords(user_input)
if categories:
    print(format_matched_keywords(categories))
" 2>/dev/null

    rm -f "$INPUT_FILE"
}

# ============================================================
# Capability Registry 按需加载
# ============================================================

# 从 capability-registry.md 提取相关内容（语义化版）
inject_capability_registry() {
    local user_input="$1"
    local registry_file="$PROJECT_ROOT/.claude/knowledge/capability-registry.md"

    # 关键词到场景的映射
    local scenarios="agent config hook memory error version cli skill evolution path"

    for scenario in $scenarios; do
        if echo "$user_input" | grep -qi "$scenario"; then
            # 转换为大写
            local scenario_upper
            scenario_upper=$(echo "$scenario" | tr '[:lower:]' '[:upper:]')
            # 找到对应的场景章节
            local section
            section=$(grep -A 100 "^### 场景: $scenario_upper" "$registry_file" 2>/dev/null | head -80)
            if [ -n "$section" ]; then
                echo ""
                echo "══════════════════════════════════════════════════════════════"
                echo "【能力地图】场景: $scenario_upper"
                echo "══════════════════════════════════════════════════════════════"
                echo "$section"
                echo "══════════════════════════════════════════════════════════════"
                return
            fi
        fi
    done

    # 尝试按模块名匹配
    local keywords="config_loader instinct memory hook mode path version evolve cli agent safety quality"
    for keyword in $keywords; do
        if echo "$user_input" | grep -qi "$keyword"; then
            local section
            section=$(grep -B 1 -A 30 "^### \`.*$keyword" "$registry_file" 2>/dev/null | head -40)
            if [ -n "$section" ]; then
                echo ""
                echo "══════════════════════════════════════════════════════════════"
                echo "【能力地图】模块: $keyword"
                echo "══════════════════════════════════════════════════════════════"
                echo "$section"
                echo "══════════════════════════════════════════════════════════════"
                return
            fi
        fi
    done
}

# ============================================================
# 核心逻辑
# ============================================================

main() {
    # 获取用户输入（如果作为参数传入）
    USER_INPUT="${1:-}"

    # 检查会话状态
    if is_L0_injected; then
        log "L0 already injected, checking keyword match"

        # L0 已注入，检查关键词匹配 L1
        if [ -n "$USER_INPUT" ]; then
            matched=$(match_keywords "$USER_INPUT")
            if [ -n "$matched" ]; then
                echo "$matched"
                log "Keyword matched: $USER_INPUT"
            fi

            # Capability Registry 按需加载
            registry_info=$(inject_capability_registry "$USER_INPUT")
            if [ -n "$registry_info" ]; then
                echo "$registry_info"
                log "Capability Registry loaded: $USER_INPUT"
            fi
        fi
    else
        log "Injecting L0 memory"

        # 构建 L0 输出
        output=""
        output+="\n"
        output+="══════════════════════════════════════════════════════════════\n"
        output+="【项目记忆】harness/memory/ — 来自 CHK 记忆系统\n"
        output+="══════════════════════════════════════════════════════════════\n"
        output+="\n"

        # 读取 MEMORY.md
        memory_index=$(read_memory_index)
        if [ -n "$memory_index" ]; then
            output+="$memory_index\n"
        fi

        # 读取高置信度本能
        instincts=$(read_high_confidence_instincts)
        if [ -n "$instincts" ]; then
            output+="$instincts\n"
        fi

        # 首次注入时也加载 Capability Registry（如果用户输入了关键词）
        if [ -n "$USER_INPUT" ]; then
            registry_info=$(inject_capability_registry "$USER_INPUT")
            if [ -n "$registry_info" ]; then
                output+="$registry_info\n"
            fi
        fi

        output+="\n"
        output+="══════════════════════════════════════════════════════════════\n"
        output+="【记忆触发规则】\n"
        output+="  • 遇到类似场景，自动应用相关记忆中的最佳实践\n"
        output+="  • 收到用户纠正时，记录到 harness/memory/feedback_*.md\n"
        output+="  • 重要决策记录到 harness/memory/MEMORY.md\n"
        output+="══════════════════════════════════════════════════════════════\n"

        # 输出
        echo -e "$output"

        # 标记 L0 已注入
        mark_L0_injected

        log "L0 injected successfully"
    fi
}

# 清理会话状态
cleanup() {
    if [ -f "$STATE_FILE" ]; then
        rm -f "$STATE_FILE"
        log "Session state cleaned"
    fi
}

# 显示帮助
show_help() {
    echo "CHK 记忆注入钩子"
    echo ""
    echo "用法: $0 [选项] [用户输入]"
    echo ""
    echo "选项:"
    echo "  -c, --cleanup    清理会话状态"
    echo "  -s, --status      显示当前状态"
    echo "  -h, --help        显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                              # 自动注入 L0"
    echo "  $0 '帮我写个单元测试'            # 注入 L0 + 关键词匹配"
    echo "  $0 --cleanup                    # 清理会话状态"
}

# ============================================================
# 入口
# ============================================================

case "${1:-}" in
    -c|--cleanup)
        cleanup
        ;;
    -s|--status)
        if [ -f "$STATE_FILE" ]; then
            cat "$STATE_FILE"
        else
            echo "No session state"
        fi
        ;;
    -h|--help)
        show_help
        ;;
    *)
        main "$@"
        ;;
esac