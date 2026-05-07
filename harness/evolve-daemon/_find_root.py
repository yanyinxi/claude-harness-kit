#!/usr/bin/env python3
"""
_find_root — 项目根目录查找工具（evolve-daemon 模块共享版）

提供 find_root() 函数：向上查找包含 .claude 目录的项目根。
"""
import os
from pathlib import Path


def find_root(start: Path | str | None = None) -> Path:
    """
    向上查找包含 .claude 目录的项目根目录。

    查找顺序：
    1. 环境变量 CLAUDE_PROJECT_DIR
    2. start 目录向上遍历
    3. 当前工作目录向上遍历
    """
    if start is None:
        start = Path.cwd()
    elif isinstance(start, str):
        start = Path(start)

    # 优先使用环境变量
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        p = Path(project_dir)
        if (p / ".claude").exists() or (p / "harness").exists():
            return p

    # 向上遍历
    current = start.resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "harness").exists():
            return parent

    # 最后回退到 cwd
    return Path.cwd()


def _find_root() -> Path:
    """kb_shared 兼容别名（避免循环导入）"""
    return find_root()


if __name__ == "__main__":
    print(find_root())
