#!/bin/bash
# ============================================================
# Git Hook: 增量更新 Capability Registry
#
# 功能：
#   - 检测 Git commit 中的代码变更
#   - 判断是否需要更新 capability-registry.md
#   - 调用 capability-analyzer.py 进行增量更新
#
# 使用方式：
#   - 作为 Git post-commit hook：将此脚本链接到 .git/hooks/post-commit
#   - 或直接调用：./update-registry-on-commit.sh
#
# ============================================================

set -uo pipefail

# 加载共享日志工具
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/log-utils.sh" 2>/dev/null || true

# 配置
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
REGISTRY_FILE="$PROJECT_ROOT/.claude/knowledge/capability-registry.md"
LAST_UPDATE_FILE="$PROJECT_ROOT/.claude/data/registry.last-update"
ANALYZER_SCRIPT="$PROJECT_ROOT/harness/cli/capability-analyzer.py"

# 需要监控的目录
MONITOR_DIRS="harness hooks agents skills"

# 检查是否有代码变更
check_code_changes() {
    # 获取上次提交变更的文件
    local changed_files
    changed_files=$(git diff --cached --name-only 2>/dev/null)

    if [ -z "$changed_files" ]; then
        # 如果没有 staged 文件，检查上次提交
        if git rev-parse HEAD~1 &>/dev/null; then
            changed_files=$(git diff --name-only HEAD~1 2>/dev/null)
        else
            # 只有一次提交，检查 HEAD
            changed_files=$(git diff --name-only HEAD 2>/dev/null)
        fi
    fi

    if [ -z "$changed_files" ]; then
        echo "no changes"
        return 1
    fi

    # 检查是否涉及需要更新的目录
    for file in $changed_files; do
        for dir in $MONITOR_DIRS; do
            if [[ "$file" == $dir/* ]] || [[ "$file" == $dir.* ]]; then
                echo "$file"
                return 0
            fi
        done
    done

    echo "no relevant changes"
    return 1
}

# 获取变更文件列表
get_changed_files() {
    local files=""

    # 获取 staged 文件
    files+=$(git diff --cached --name-only 2>/dev/null)
    files+=$'\n'

    # 获取上次提交的文件（如果有的话）
    if git rev-parse HEAD~1 &>/dev/null; then
        files+=$(git diff --name-only HEAD~1 2>/dev/null)
    fi

    echo "$files" | sort -u | grep -E "^(${MONITOR_DIRS})" || true
}

# 判断是否需要强制全量更新
needs_full_update() {
    local changed_files="$1"

    # 新增模块文件
    for file in $changed_files; do
        if [[ "$file" =~ \.(py|js|sh)$ ]] && ! git show HEAD:"$file" &>/dev/null; then
            echo "new file detected: $file"
            return 0
        fi
    done

    # 删除文件
    if git ls-files --deleted | grep -qE "^($MONITOR_DIRS)"; then
        echo "deleted file detected"
        return 0
    fi

    return 1
}

# 更新注册表
update_registry() {
    local force_update="${1:-incremental}"

    # 检查分析器脚本是否存在
    if [ ! -f "$ANALYZER_SCRIPT" ]; then
        _hook_log_error "registry-update" "Analyzer script not found: $ANALYZER_SCRIPT"
        return 1
    fi

    # 检查是否在 git 仓库中
    if ! git rev-parse --git-dir &>/dev/null; then
        _hook_log_warn "registry-update" "Not in a git repository"
    fi

    # 获取变更文件
    local changed_files=""
    if git rev-parse HEAD~1 &>/dev/null; then
        changed_files=$(git diff --name-only HEAD~1 2>/dev/null)
    elif git rev-parse HEAD &>/dev/null; then
        changed_files=$(git diff --name-only HEAD 2>/dev/null)
    fi

    # 检查是否有相关变更
    local has_relevant_changes=false
    if [ -n "$changed_files" ]; then
        for file in $changed_files; do
            for dir in $MONITOR_DIRS; do
                if [[ "$file" == $dir/* ]] || [[ "$file" == $dir.* ]]; then
                    has_relevant_changes=true
                    break 2
                fi
            done
        done
    fi

    # 即使没有变更也生成注册表（初始化场景）
    _hook_log_info "registry-update" "Generating Capability Registry..."
    echo "正在生成 Capability Registry..."

    # 调用分析器
    local output
    output=$(python3 "$ANALYZER_SCRIPT" --root "$PROJECT_ROOT" --output "$REGISTRY_FILE" 2>&1)
    local status=$?

    if [ $status -eq 0 ]; then
        # 记录更新时间
        echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LAST_UPDATE_FILE"
        _hook_log_info "registry-update" "Registry updated successfully"
        echo "$output"
    else
        _hook_log_error "registry-update" "Registry update failed: $output"
        return 1
    fi

    return 0
}

# 显示帮助
show_help() {
    echo "Git Hook: 增量更新 Capability Registry"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -f, --force    强制全量更新"
    echo "  -c, --check    只检查，不更新"
    echo "  -h, --help     显示帮助"
    echo ""
    echo "示例:"
    echo "  $0              # 增量更新"
    echo "  $0 --force      # 全量更新"
    echo "  $0 --check      # 检查是否有变更"
}

# 主入口
main() {
    local mode="update"

    # 解析参数
    case "${1:-}" in
        -f|--force)
            mode="full"
            ;;
        -c|--check)
            mode="check"
            ;;
        -h|--help)
            show_help
            return 0
            ;;
    esac

    # 确保目录存在
    mkdir -p "$(dirname "$REGISTRY_FILE")" 2>/dev/null
    mkdir -p "$(dirname "$LAST_UPDATE_FILE")" 2>/dev/null

    case "$mode" in
        check)
            local changes
            changes=$(check_code_changes)
            if [ $? -eq 0 ]; then
                echo "Changes detected: $changes"
                return 0
            else
                echo "No relevant changes"
                return 0
            fi
            ;;
        full)
            update_registry "full"
            ;;
        update)
            update_registry "incremental"
            ;;
    esac
}

main "$@"