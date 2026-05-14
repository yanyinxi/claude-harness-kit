#!/usr/bin/env python3
"""
hook-wrapper.py — 通用 Hook 执行器

用途: 在 settings.json 中使用，提供通用的 hook 执行能力
- 自动检测项目根目录（支持 CLAUDE_PROJECT_DIR 环境变量）
- 支持相对路径的 hook 脚本
- 提供统一的错误处理和日志

使用方法 (在 settings.json 中):
{
  "type": "command",
  "command": "python3 /path/to/hook-wrapper.py /relative/path/to/hook.sh"
}

环境变量:
  - CLAUDE_HOOKS_DIR: 可选的 hooks 目录（默认从脚本位置推断）
  - CLAUDE_PROJECT_DIR: 项目根目录（由 Claude Code 设置）
"""
import os
import sys
from pathlib import Path


def find_project_root() -> Path:
    """从当前工作目录向上查找 .claude 目录作为项目根"""
    cwd = Path(os.getcwd())
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".claude").exists():
            return parent
    return cwd


def main():
    if len(sys.argv) < 2:
        print("Usage: hook-wrapper.py <hook-script> [args...]", file=sys.stderr)
        sys.exit(1)

    # 获取项目根目录
    project_root = find_project_root()

    # 获取 hook 脚本路径（支持相对路径和绝对路径）
    hook_arg = sys.argv[1]

    if os.path.isabs(hook_arg):
        hook_path = Path(hook_arg)
    else:
        # 相对路径：优先从项目根目录查找
        # 标准结构: <project>/harness/hooks/bin/<hook>
        possible_paths = [
            project_root / "harness" / "hooks" / "bin" / hook_arg,
            project_root / hook_arg,
            Path(__file__).parent / hook_arg,  # 相对于 wrapper 脚本自身
        ]

        hook_path = None
        for p in possible_paths:
            if p.exists():
                hook_path = p
                break

        if hook_path is None:
            print(f"Error: Hook script not found: {hook_arg}", file=sys.stderr)
            print(f"Searched in: {[str(p) for p in possible_paths]}", file=sys.stderr)
            sys.exit(1)

    # 确保脚本可执行
    os.chmod(hook_path, 0o755)

    # 设置环境变量供 hook 脚本使用
    os.environ["CLAUDE_PROJECT_ROOT"] = str(project_root)
    os.environ["CLAUDE_HOOKS_DIR"] = str(project_root / "harness" / "hooks" / "bin")

    # 构建命令
    cmd = [str(hook_path)] + sys.argv[2:]

    # 执行 hook
    try:
        os.execv(cmd[0], cmd)
    except FileNotFoundError:
        print(f"Error: Cannot execute {cmd[0]}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for {cmd[0]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()