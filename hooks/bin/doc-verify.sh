#!/usr/bin/env bash
# doc-verify.sh - 文档验证器 Shell 包装器
# 用于 Claude Code hook，自动检测插件根目录

set -e

# 自动检测插件根目录
detect_plugin_root() {
    # 优先级 1: 环境变量
    if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -d "$CLAUDE_PLUGIN_ROOT" ]; then
        echo "$CLAUDE_PLUGIN_ROOT"
        return 0
    fi

    # 优先级 2: 从当前脚本位置向上查找
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    current="$script_dir"

    while [ "$current" != "/" ]; do
        if [ -f "$current/.claude-plugin/plugin.json" ] || [ -f "$current/index.js" ]; then
            echo "$current"
            return 0
        fi
        current="$(dirname "$current")"
    done

    # 优先级 3: 向上查找 harness/hooks 结构
    current="$script_dir"
    while [ "$current" != "/" ]; do
        if [ "$(basename "$current")" = "hooks" ] && [ "$(basename "$(dirname "$current")")" = "harness" ]; then
            dirname "$(dirname "$current")"
            return 0
        fi
        current="$(dirname "$current")"
    done

    # 兜底: 返回当前工作目录
    pwd
}

PLUGIN_ROOT="$(detect_plugin_root)"
PYTHON_SCRIPT="$PLUGIN_ROOT/harness/hooks/bin/doc-verify.py"

# 执行 Python 脚本
if [ -f "$PYTHON_SCRIPT" ]; then
    python3 "$PYTHON_SCRIPT" "$@"
else
    # 备用: doc_verify.py (下划线命名)
    PYTHON_SCRIPT_ALT="$PLUGIN_ROOT/harness/hooks/bin/doc_verify.py"
    if [ -f "$PYTHON_SCRIPT_ALT" ]; then
        python3 "$PYTHON_SCRIPT_ALT" "$@"
    else
        echo "[doc-verify.sh] Warning: doc-verify.py not found at $PYTHON_SCRIPT" >&2
        exit 0
    fi
fi