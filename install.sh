#!/bin/bash
# Claude Harness Kit 一键安装脚本
# 用法: ./install.sh 或 ./install.sh --local

set -e

PLUGIN_NAME="chk"
MARKETPLACE_NAME="chk-marketplace"

# 解析参数
INSTALL_MODE="auto"  # auto: 自动检测, local: 本地目录, github: GitHub
if [ "$1" = "--local" ]; then
    INSTALL_MODE="local"
elif [ "$1" = "--github" ]; then
    INSTALL_MODE="github"
fi

echo "========================================"
echo "Claude Harness Kit 安装脚本"
echo "========================================"

# 获取脚本所在目录（支持从子目录调用）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 清理旧配置
echo "[1/4] 清理旧配置..."
claude plugins marketplace remove "$MARKETPLACE_NAME" 2>/dev/null || true
claude plugins uninstall "$PLUGIN_NAME" 2>/dev/null || true

# 根据安装模式配置
case "$INSTALL_MODE" in
    local)
        echo "[2/4] 使用本地目录模式..."
        MARKETPLACE_SOURCE="$SCRIPT_DIR"
        ;;
    github)
        echo "[2/4] 使用 GitHub 模式..."
        MARKETPLACE_SOURCE="https://github.com/yanyinxi/claude-harness-kit.git"
        ;;
    auto)
        echo "[2/4] 自动检测安装模式..."
        if curl -s --max-time 5 -o /dev/null -w "%{http_code}" https://github.com/yanyinxi/claude-harness-kit | grep -q "200"; then
            echo "      检测到可访问 GitHub，使用远程模式"
            MARKETPLACE_SOURCE="https://github.com/yanyinxi/claude-harness-kit.git"
        else
            echo "      GitHub 不可访问，使用本地目录模式"
            MARKETPLACE_SOURCE="$SCRIPT_DIR"
        fi
        ;;
esac

# 添加 marketplace
echo "[3/4] 添加插件市场..."
claude plugins marketplace add "$MARKETPLACE_SOURCE" 2>/dev/null || {
    echo "      GitHub 模式失败，切换到本地目录模式..."
    MARKETPLACE_SOURCE="$SCRIPT_DIR"
    claude plugins marketplace remove "$MARKETPLACE_NAME" 2>/dev/null || true
    claude plugins marketplace add "$MARKETPLACE_SOURCE"
}
echo "      marketplace: $MARKETPLACE_SOURCE"

# 安装插件
echo "[4/4] 安装插件..."
if claude plugins install "$PLUGIN_NAME" --scope user 2>&1; then
    echo ""
    echo "========================================"
    echo "✓ 安装成功!"
    echo "========================================"
    echo ""
    echo "重启 Claude Code 后即可使用 CHK 功能"
    echo ""
    echo "常用命令:"
    echo "  /chk-team   - 团队开发模式 (默认)"
    echo "  /chk-auto   - 全自动模式"
    echo "  /chk-ralph  - TDD 强制模式"
    echo "  /chk-ultra  - 极限并行模式"
    echo ""
else
    echo ""
    echo "========================================"
    echo "✘ 安装失败"
    echo "========================================"
    echo ""
    echo "常见问题:"
    echo "  1. 如果网络有问题，使用本地模式: ./install.sh --local"
    echo "  2. 确保 Claude Code 版本 >= 2.0"
    echo "  3. 查看错误信息重试"
    echo ""
    exit 1
fi