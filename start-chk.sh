#!/bin/bash
# start-chk.sh - 启动带 CHK 插件的 Claude Code
# 用法: bash ./start-chk.sh [claude 选项]

CHK_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "启动 Claude Code + Claude Harness Kit..."
echo "插件目录: $CHK_DIR"
echo ""

# 启动 Claude Code 并加载 CHK 插件
exec claude --plugin-dir "$CHK_DIR" "$@"
