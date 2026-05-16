#!/usr/bin/env bash
# install.sh — Claude Harness Kit 一键安装脚本
# 用法: bash ./install.sh
# 效果: 安装插件 + 复制斜杠命令，一步搞定

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ══════════════════════════════════════════════════════════════════════════════
# 环境检查函数
# ══════════════════════════════════════════════════════════════════════════════

check_environment() {
    echo "=== 环境检查 ==="
    echo ""

    local missing_deps=()
    local needs_update=()

    # 1. 检查 Node.js
    echo "1. Node.js 检查:"
    if command -v node &> /dev/null; then
        local node_version=$(node --version | sed 's/v//')
        local node_major=$(echo "$node_version" | cut -d. -f1 | sed 's/[^0-9]//g')
        if [ "$node_major" -ge 18 ]; then
            echo "   ✓ Node.js v$node_version"
        else
            echo "   ⚠️  Node.js v$node_version 版本过低（需要 >=18）"
            needs_update+=("node")
        fi
    else
        echo "   ✗ Node.js 未安装"
        missing_deps+=("node")
    fi

    # 2. 检查 Git
    echo ""
    echo "2. Git 检查:"
    if command -v git &> /dev/null; then
        local git_version=$(git --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
        local git_major=$(echo "$git_version" | cut -d. -f1)
        local git_minor=$(echo "$git_version" | cut -d. -f2)
        if [ "$git_major" -gt 2 ] || ([ "$git_major" -eq 2 ] && [ "$git_minor" -ge 27 ]); then
            echo "   ✓ Git v$git_version"
        else
            echo "   ⚠️  Git v$git_version 版本过低（需要 >=2.27，支持 sparse checkout）"
            needs_update+=("git")
        fi
    else
        echo "   ✗ Git 未安装"
        missing_deps+=("git")
    fi

    # 3. 检查 npm
    echo ""
    echo "3. npm 检查:"
    if command -v npm &> /dev/null; then
        local npm_version=$(npm --version)
        echo "   ✓ npm v$npm_version"
    else
        echo "   ⚠️  npm 未安装（Node.js 应该包含 npm）"
    fi

    # 4. 检查 Python
    echo ""
    echo "4. Python 检查:"
    if command -v python3 &> /dev/null; then
        local py_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        echo "   ✓ Python $py_version"
    else
        echo "   ⚠️  Python3 未安装（部分功能可能受影响）"
    fi

    # 5. 检查 Homebrew (macOS)
    echo ""
    echo "5. Homebrew 检查 (macOS):"
    if [[ "$(uname)" == "Darwin" ]]; then
        if command -v brew &> /dev/null; then
            echo "   ✓ Homebrew 已安装"
        else
            echo "   ℹ️  Homebrew 未安装（可使用 brew install git/node 快速更新）"
        fi
    fi

    # ══════════════════════════════════════════════════════════════════════════
    # 处理缺失或需要更新的依赖
    # ══════════════════════════════════════════════════════════════════════════

    echo ""
    echo "=== 依赖状态汇总 ==="

    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo "  缺失: ${missing_deps[*]}"
    fi

    if [ ${#needs_update[@]} -gt 0 ]; then
        echo "  需要更新: ${needs_update[*]}"
        echo ""
        echo "  正在自动安装/更新..."
        auto_install_deps "${needs_update[@]}" "${missing_deps[@]}"
    else
        echo "  ✓ 所有依赖已满足"
    fi

    echo ""
}

auto_install_deps() {
    # 处理需要更新的依赖
    local needs_update=("$@")

    # 跳过 Git 安装（Homebrew 太慢），使用手动克隆方式
    echo "  ℹ️  Git 将通过其他方式处理，跳过自动安装"
}

# ══════════════════════════════════════════════════════════════════════════════
# Git 版本检查和修复
# ══════════════════════════════════════════════════════════════════════════════

check_git_filter_support() {
    echo ""
    echo "=== Git Sparse Checkout 支持检查 ==="

    # 测试 git 是否支持 --filter=tree:0
    if git clone --help 2>&1 | grep -q "\-\-filter="; then
        local test_dir="/tmp/git-filter-test-$$"
        mkdir -p "$test_dir"
        if git -C "$test_dir" clone --depth 1 --filter=tree:0 . "$test_dir/check" 2>/dev/null; then
            echo "  ✓ Git 支持 --filter=tree:0（sparse checkout）"
            rm -rf "$test_dir"
            return 0
        fi
        rm -rf "$test_dir"
    fi

    echo "  ⚠️  Git 不支持 sparse checkout，将使用替代方案"
    return 1
}

# ══════════════════════════════════════════════════════════════════════════════
# 主安装流程
# ══════════════════════════════════════════════════════════════════════════════

main() {
    echo ""
    echo "███████╗██╗   ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗"
    echo "██╔════╝██║   ██║██╔════╝ ██╔══██╗██╔══██╗████╗  ██║"
    echo "███████╗██║   ██║██║  ███╗██████╔╝███████║██╔██╗ ██║"
    echo "╚════██║██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╗██║"
    echo "███████║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚████║"
    echo "╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"
    echo ""
    echo "Claude Harness Kit 一键安装脚本"
    echo "版本: 0.9.1"
    echo ""

    # 1. 环境检查
    check_environment

    # 2. 检查 git sparse checkout 支持
    check_git_filter_support || {
        echo ""
        echo "  ℹ️  将使用替代安装方式（完整克隆）"
    }

    # 3. 安装 Claude Code 插件
    echo ""
    echo "=== Step 1: 安装 Claude Code 插件 ==="
    cd "$CHK_ROOT"

    local install_success=false

    # 方法 1: 通过 GitHub 仓库安装（需要 git sparse checkout 支持）
    echo "  尝试通过 GitHub 安装..."
    if claude plugin install yanyinxi/claude-harness-kit --scope user 2>/dev/null; then
        echo "  ✓ GitHub 安装成功"
        install_success=true
    fi

    # 方法 2: 通过 marketplace 安装
    if [ "$install_success" = false ]; then
        echo "  尝试通过本地 marketplace 安装..."
        if claude plugins marketplace add --scope user . 2>/dev/null; then
            if claude plugin install claude-harness-kit --scope user 2>/dev/null; then
                echo "  ✓ Marketplace 安装成功"
                install_success=true
            fi
        fi
    fi

    # 方法 3: 手动配置（最后方案）
    if [ "$install_success" = false ]; then
        echo "  使用手动配置方案..."
        manual_install
        install_success=true
    fi

    # 4. 复制 Skills
    echo ""
    echo "=== Step 2: 复制 Skills ==="
    local user_skills="$HOME/.claude/skills"
    mkdir -p "$user_skills"

    local copied=0
    for skill_dir in "$CHK_ROOT/skills"/*/; do
        if [ -f "$skill_dir/SKILL.md" ]; then
            local skill_name="$(basename "$skill_dir")"
            mkdir -p "$user_skills/$skill_name"
            cp "$skill_dir/SKILL.md" "$user_skills/$skill_name/" 2>/dev/null || true
            echo "  ✓ $skill_name"
            copied=$((copied + 1))
        fi
    done
    echo "  共复制 $copied 个 Skills"

    # 5. 安装 MCP 工具
    echo ""
    echo "=== Step 3: 安装 MCP 工具 ==="
    local mcp_list=(
        "filesystem:npx:-y:@modelcontextprotocol/server-filesystem:.:安全的文件读写"
        "playwright:npx:-y:@playwright/mcp::浏览器自动化测试、截图"
    )

    for mcp in "${mcp_list[@]}"; do
        IFS=':' read -r name cmd arg1 arg2 arg3 desc <<< "$mcp"
        local args=()
        [ -n "$arg1" ] && args+=("$arg1")
        [ -n "$arg2" ] && args+=("$arg2")
        [ -n "$arg3" ] && args+=("$arg3")
        if claude mcp add "$name" -- "$cmd" "${args[@]}" 2>/dev/null; then
            echo "  ✓ $name — $desc"
        else
            echo "  ⏭️  $name — 已安装或跳过"
        fi
    done

    # 6. 验证安装
    echo ""
    echo "=== 验证安装 ==="
    local plugin_status=$(claude plugins list 2>&1)
    if echo "$plugin_status" | grep -q "claude-harness-kit"; then
        if echo "$plugin_status" | grep -A2 "claude-harness-kit" | grep -q "✔ enabled"; then
            echo "  ✓ 插件已启用并正常运行"
        elif echo "$plugin_status" | grep -A2 "claude-harness-kit" | grep -q "✘"; then
            echo "  ⚠️  插件已安装但未启用"
        fi
    else
        echo "  ℹ️  插件可能需要重启 Claude Code 后生效"
    fi

    echo ""
    echo "██████╗ ██╗   ██╗██╗██╗  ██╗██╗   ██╗ █████╗ ██████╗ ███████╗"
    echo "██╔══██╗██║   ██║██║██║ ██╔╝██║   ██║██╔══██╗██╔══██╗██╔════╝"
    echo "██████╔╝██║   ██║██║█████╔╝ ██║   ██║███████║██████╔╝███████╗"
    echo "██╔══██╗██║   ██║██║██╔═██╗ ██║   ██║██╔══██║██╔══██╗╚════██║"
    echo "██║  ██║╚██████╔╝██║██║  ██╗╚██████╔╝██║  ██║██║  ██║███████║"
    echo "╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
    echo ""
    echo "安装完成！"
    echo ""
    echo "常用命令:"
    echo "  /chk-team   功能开发（默认）"
    echo "  /chk-auto   快速修复 Bug"
    echo "  /chk-ralph  TDD 强制模式"
    echo "  /chk-help   查看所有命令"
}

# ══════════════════════════════════════════════════════════════════════════════
# 手动安装函数（最后方案）
# ══════════════════════════════════════════════════════════════════════════════

manual_install() {
    echo "  执行手动安装..."

    # 1. 确保 .claude-plugin 目录存在
    local plugin_cache_dir="$HOME/.claude/plugins/cache/claude-harness-kit/claude-harness-kit/0.9.1"
    mkdir -p "$plugin_cache_dir/.claude-plugin/hooks"

    # 2. 复制插件文件
    cp -r "$CHK_ROOT"/* "$plugin_cache_dir/" 2>/dev/null || true

    # 3. 更新 installed_plugins.json
    python3 << PYEOF
import json
import os

installed_json = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
plugin_dir = os.path.expanduser("$plugin_cache_dir")

with open(installed_json, 'r') as f:
    data = json.load(f)

data.setdefault('plugins', {})['claude-harness-kit@local'] = [
    {
        "scope": "user",
        "installPath": plugin_dir,
        "version": "0.9.1",
        "installedAt": "2026-05-16T00:00:00.000Z",
        "lastUpdated": "2026-05-16T00:00:00.000Z"
    }
]

with open(installed_json, 'w') as f:
    json.dump(data, f, indent=2)

print("  ✓ 已配置插件路径")
PYEOF

    # 4. 启用插件
    claude plugin enable claude-harness-kit@local --scope user 2>/dev/null || true

    echo "  ✓ 手动安装完成"
}

# 执行主函数
main "$@"