#!/usr/bin/env python3
"""
Stop Hook 包装器 - 自动检测插件根目录

问题: Claude Code 的 Stop hook 可能无法识别 ${CLAUDE_PLUGIN_ROOT} 环境变量，
即使 hooks 定义在插件的 hooks/hooks.json 中。
解决方案: 使用 Python 脚本自动检测插件根目录。

检测优先级:
  1. CLAUDE_PLUGIN_ROOT 环境变量
  2. settings.local.json 中的配置
  3. 插件 index.js 的父目录向上查找
  4. 当前工作目录向上查找 harness/hooks
"""
import json
import os
import sys
from pathlib import Path


def detect_plugin_root() -> Path:
    """自动检测插件根目录"""
    # 优先级 1: 环境变量
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if env_root and Path(env_root).exists():
        plugin_json = Path(env_root) / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return Path(env_root)

    # 优先级 2: settings.local.json
    settings_local = Path.home() / ".claude" / "settings.local.json"
    if settings_local.exists():
        try:
            data = json.loads(settings_local.read_text())
            root = data.get("env", {}).get("CLAUDE_PLUGIN_ROOT", "")
            if root and Path(root).exists():
                return Path(root)
        except (json.JSONDecodeError, OSError):
            pass

    # 优先级 3/4: 统一遍历，两种条件一起检查
    current = Path(__file__).resolve().parent
    for ancestor in [current] + list(current.parents):
        # 检查 .claude-plugin 或 index.js
        if (ancestor / ".claude-plugin" / "plugin.json").exists() or (ancestor / "index.js").exists():
            return ancestor
        # 检查 hooks/harness 结构
        if ancestor.name == "hooks" and ancestor.parent.name == "harness":
            return ancestor.parent.parent

    # 兜底: 返回当前工作目录
    return Path(os.getcwd())


def main():
    """执行 collect_session.py，使用检测到的插件根目录"""
    plugin_root = detect_plugin_root()
    os.environ["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)

    # 设置 Python 路径以便导入 collect_session
    hooks_bin = plugin_root / "harness" / "hooks" / "bin"
    if hooks_bin.exists():
        sys.path.insert(0, str(hooks_bin))

    try:
        # 动态导入并执行 collect_session
        from collect_session import main as session_main
        session_main()
    except ImportError as e:
        # collect_session 可能不存在，静默跳过
        print(f"[stop-hook-wrapper] collect_session not found: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[stop-hook-wrapper] Error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
