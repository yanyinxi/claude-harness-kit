#!/bin/bash
# ============================================================
# CHK 共享日志工具 — 被其他 hook 脚本 source 使用
#
# 功能：
#   - `_hook_log_error hook_name msg` — 记录错误到项目日志
#   - `_hook_log_warn hook_name msg`  — 记录警告到项目日志
#   - `_hook_log_info hook_name msg`  — 记录信息到项目日志
#
# 日志位置：<项目>/.claude/data/hook-errors.log
# 自动创建 .claude/data/ 目录
# ============================================================

_HOOK_LOG_FILE=""

_hook_log_init() {
    if [[ -n "$_HOOK_LOG_FILE" ]]; then
        echo "$_HOOK_LOG_FILE"
        return
    fi
    local project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
    local data_dir="$project_dir/.claude/data"
    mkdir -p "$data_dir"
    _HOOK_LOG_FILE="$data_dir/hook-errors.log"
    echo "$_HOOK_LOG_FILE"
}

_hook_log_error() {
    local hook_name="${1:-unknown}"
    local message="${2:-}"
    local log_file
    log_file=$(_hook_log_init)
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [$hook_name] ERROR: $message" >> "$log_file"
}

_hook_log_warn() {
    local hook_name="${1:-unknown}"
    local message="${2:-}"
    local log_file
    log_file=$(_hook_log_init)
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [$hook_name] WARN: $message" >> "$log_file"
}

_hook_log_info() {
    local hook_name="${1:-unknown}"
    local message="${2:-}"
    local log_file
    log_file=$(_hook_log_init)
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [$hook_name] INFO: $message" >> "$log_file"
}
