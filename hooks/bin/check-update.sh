#!/bin/bash
# ============================================================
# CHK 插件更新检查钩子 - UserPromptSubmit
#
# 功能：
# - 每次用户提交消息时检查插件更新
# - 检查是否处于通知冷却期（24小时）
# - 发现新版本时输出更新提示
#
# 触发时机：UserPromptSubmit（用户提交消息前）
# ============================================================

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 通知冷却时间（小时）
COOLDOWN_HOURS=24

# 日志文件
LOG_DIR="$PROJECT_ROOT/.claude/data"
LOG_FILE="$LOG_DIR/update_check.log"

# 创建日志目录
mkdir -p "$LOG_DIR" 2>/dev/null

# 日志函数
log_info() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE" 2>/dev/null
}

# 检查是否应该执行更新检查
should_check() {
    local last_check_file="$LOG_DIR/.last_update_check"
    local last_check=0

    if [ -f "$last_check_file" ]; then
        last_check=$(cat "$last_check_file")
    fi

    local now=$(date +%s)
    local hours_since=$(( (now - last_check) / 3600 ))

    # 每 24 小时检查一次
    if [ $hours_since -ge $COOLDOWN_HOURS ]; then
        echo "$now" > "$last_check_file"
        return 0  # 应该检查
    fi

    return 1  # 冷却中
}

# 获取本地版本
get_local_version() {
    local version_file="$PROJECT_ROOT/harness/_core/version.json"
    if [ -f "$version_file" ]; then
        python3 -c "import json; print(json.load(open('$version_file')).get('version', 'unknown'))" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# 获取远程版本
get_remote_version() {
    # 从 GitHub API 获取最新 release
    local response=$(curl -s --max-time 10 \
        -H "Accept: application/vnd.github+json" \
        -H "User-Agent: CHK-Update-Checker" \
        "https://api.github.com/repos/yanyinxi/claude-harness-kit/releases/latest" 2>/dev/null)

    if [ $? -ne 0 ] || [ -z "$response" ]; then
        echo ""
        return
    fi

    # 提取 tag_name
    echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tag_name', ''))" 2>/dev/null
}

# 比较版本 (v1 < v2)
version_lt() {
    local v1=$1
    local v2=$2

    python3 -c "
import sys
v1 = '$v1'.lstrip('v').split('-')[0].split('.')
v2 = '$v2'.lstrip('v').split('-')[0].split('.')
for i in range(max(len(v1), len(v2))):
    p1 = int(v1[i]) if i < len(v1) else 0
    p2 = int(v2[i]) if i < len(v2) else 0
    if p1 < p2:
        sys.exit(0)
    elif p1 > p2:
        sys.exit(1)
sys.exit(2)
" 2>/dev/null
    local result=$?
    [ $result -eq 0 ]
}

# 输出更新通知
show_update_notification() {
    local local_ver=$1
    local remote_ver=$2

    # 生成框线
    local line="════════════════════════════════════════════════════════════"
    local half=$(( ${#line} / 2 ))

    cat << EOF

╔${line}╗
║  🔔 CHK 插件更新可用                                       ║
╠${line}╣
║  当前版本: ${local_ver}                                       ║
║  最新版本: ${remote_ver}                                       ║
╠${line}╣
║  更新命令: claude plugins update chk                       ║
╚${line}╝
EOF
}

# 主逻辑
main() {
    # 检查是否应该执行
    if ! should_check; then
        log_info "更新检查跳过（冷却中）"
        exit 0
    fi

    log_info "开始更新检查..."

    # 获取版本信息
    local_ver=$(get_local_version)
    remote_ver=$(get_remote_version)

    if [ -z "$remote_ver" ]; then
        log_info "无法获取远程版本（网络问题）"
        exit 0
    fi

    log_info "本地版本: $local_ver, 远程版本: $remote_ver"

    # 比较版本
    if version_lt "$local_ver" "$remote_ver"; then
        log_info "发现新版本: $remote_ver"

        # 检查是否已通知过这个版本
        local notified_file="$LOG_DIR/.notified_version"

        if [ -f "$notified_file" ]; then
            local notified_ver=$(cat "$notified_file")
            if [ "$notified_ver" = "$remote_ver" ]; then
                log_info "已通知过此版本，跳过"
                exit 0
            fi
        fi

        # 输出通知
        show_update_notification "$local_ver" "$remote_ver"

        # 记录已通知版本
        echo "$remote_ver" > "$notified_file"
    else
        log_info "当前版本已是最新"
    fi
}

main "$@"