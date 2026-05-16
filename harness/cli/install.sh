#!/usr/bin/env bash
# install.sh — Claude Harness Kit 一键安装脚本
# 用法: bash ./install.sh
# 效果: 安装插件 + 复制斜杠命令，一步搞定

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "CHK 一键安装开始..."
echo ""

# Step 1: 安装 Claude Code 插件
echo "Step 1: 安装 Claude Code 插件"
cd "$CHK_ROOT"

# 尝试通过 GitHub 安装（推荐方式）
echo "  正在安装 claude-harness-kit..."

INSTALL_RESULT=$(claude plugin install yanyinxi/claude-harness-kit --scope user 2>&1) || true

if echo "$INSTALL_RESULT" | grep -q "Successfully\|already"; then
    echo "  ✅ 插件安装成功"
else
    # 如果 GitHub 安装失败，尝试其他方式
    echo "  ⚠️ GitHub 安装遇到问题，尝试本地安装..."

    # 添加 marketplace
    claude plugins marketplace add --scope user ./ 2>/dev/null || true

    # 手动添加到 installed_plugins.json
    PLUGIN_PATH="$CHK_ROOT"
    INSTALLED_JSON="$HOME/.claude/plugins/installed_plugins.json"

    # 读取并更新 installed_plugins.json
    if [ -f "$INSTALLED_JSON" ]; then
        # 检查是否已安装
        if grep -q "claude-harness-kit" "$INSTALLED_JSON"; then
            echo "  ✅ 插件已在配置中"
        else
            # 手动添加（需要 Python）
            python3 << PYEOF
import json
import os

installed_json = os.path.expanduser("$INSTALLED_JSON")
plugin_path = "$PLUGIN_PATH"

with open(installed_json, 'r') as f:
    data = json.load(f)

# 检查是否已存在
if 'claude-harness-kit@claude-harness-kit' not in data.get('plugins', {}):
    data.setdefault('plugins', {})['claude-harness-kit@claude-harness-kit'] = [
        {
            "scope": "user",
            "installPath": plugin_path,
            "version": "0.9.1",
            "installedAt": "2026-05-16T00:00:00.000Z",
            "lastUpdated": "2026-05-16T00:00:00.000Z"
        }
    ]

    with open(installed_json, 'w') as f:
        json.dump(data, f, indent=2)

    print("  ✅ 插件已添加到 installed_plugins.json")
else:
    print("  ✅ 插件已在列表中")
PYEOF
        fi
    fi

    # 更新 settings.json 启用插件
    SETTINGS_JSON="$HOME/.claude/settings.json"
    python3 << PYEOF
import json
import os

settings_json = os.path.expanduser("$SETTINGS_JSON")

with open(settings_json, 'r') as f:
    data = json.load(f)

# 启用插件
data.setdefault('enabledPlugins', {})['claude-harness-kit'] = True

# 添加到 marketplace（使用 directory 类型，但 CLI 可能不支持）
data.setdefault('extraKnownMarketplaces', {})['claude-harness-kit'] = {
    "source": {
        "source": "directory",
        "path": "$CHK_ROOT"
    }
}

with open(settings_json, 'w') as f:
    json.dump(data, f, indent=2)

print("  ✅ enabledPlugins 已更新")
PYEOF
fi

# 验证安装
echo ""
echo "  验证插件状态..."
PLUGIN_STATUS=$(claude plugins list 2>&1)
if echo "$PLUGIN_STATUS" | grep -q "claude-harness-kit"; then
    if echo "$PLUGIN_STATUS" | grep -A1 "claude-harness-kit" | grep -q "✔ enabled"; then
        echo "  ✅ 插件已启用并正常运行"
    elif echo "$PLUGIN_STATUS" | grep -A1 "claude-harness-kit" | grep -q "✗"; then
        echo "  ⚠️ 插件已安装但未启用，尝试启用..."
        claude plugin enable claude-harness-kit --scope user 2>/dev/null || true
    fi
else
    echo "  ⚠️ 插件未在列表中显示（可能是 directory source type 不被支持）"
fi

# Step 2: 复制 Skills 到用户目录
echo ""
echo "Step 2: 复制 Skills 到用户目录"

USER_SKILLS="$HOME/.claude/skills"
mkdir -p "$USER_SKILLS"

# 复制所有 skills
copied=0
for skill_dir in "$CHK_ROOT/skills"/*/; do
    skill_name="$(basename "$skill_dir")"
    if [ -f "$skill_dir/SKILL.md" ] && [ "$skill_name" != "_meta.json" ]; then
        mkdir -p "$USER_SKILLS/$skill_name"
        cp "$skill_dir/SKILL.md" "$USER_SKILLS/$skill_name/" 2>/dev/null || true
        echo "  ✅ $skill_name"
        copied=$((copied + 1))
    fi
done

if [ $copied -gt 0 ]; then
    echo "  ✅ 共复制 $copied 个 Skills 到 $USER_SKILLS"
else
    echo "  ⚠️ 未找到 Skills 文件"
fi

# Step 3: 安装推荐 MCP 工具
echo ""
echo "Step 3: 安装推荐 MCP 工具（可选）"

mcp_list=(
  "filesystem:npx:-y:@modelcontextprotocol/server-filesystem:.:安全的文件读写"
  "playwright:npx:-y:@playwright/mcp::浏览器自动化测试、截图"
)

for mcp in "${mcp_list[@]}"; do
  IFS=':' read -r name cmd arg1 arg2 arg3 desc <<< "$mcp"
  args=()
  [ -n "$arg1" ] && args+=("$arg1")
  [ -n "$arg2" ] && args+=("$arg2")
  [ -n "$arg3" ] && args+=("$arg3")
  if claude mcp add "$name" -- "$cmd" "${args[@]}" 2>/dev/null; then
    echo "  ✅ $name — $desc"
  else
    echo "  ⏭️  $name — 已安装或跳过"
  fi
done

echo ""
echo "✅ 安装完成！"
echo ""
echo "验证安装:"
claude plugins list 2>&1 | grep -E "claude-harness|Installed" || echo "  （查看上方列表）"
echo ""
echo "常用命令:"
echo "  /chk-init   初始化项目"
echo "  /chk-team   功能开发（默认）"
echo "  /chk-auto   快速修复 Bug"
echo "  /chk-ultra  批量代码改造"
echo "  /chk-ralph  写支付/安全代码"
echo "  /chk-ccg    架构决策"
echo "  /chk-help   查看所有命令"
