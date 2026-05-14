#!/usr/bin/env python3
"""
_find_root — 项目根目录查找工具（evolve-daemon 模块共享版）

提供 find_root() 函数：向上查找包含 .claude 目录的项目根。
已废弃：请使用 harness/paths.py 中的 find_root() 函数。
本模块仅保留用于向后兼容。
"""
import os
import warnings
from pathlib import Path


def _find_root_deprecation_warning():
    """打印废弃警告（仅一次）"""
    if not hasattr(_find_root_deprecation_warning, "_warned"):
        _find_root_deprecation_warning._warned = True
        warnings.warn(
            "harness/evolve-daemon/_find_root.py 已废弃，请使用 harness/paths.py 中的 find_root()",
            DeprecationWarning,
            stacklevel=2
        )


def find_root(start: Path | str | None = None) -> Path:
    """
    向上查找包含 .claude 目录的项目根目录。

    查找顺序：
    1. 环境变量 CLAUDE_PROJECT_DIR
    2. start 目录向上遍历
    3. 当前工作目录向上遍历

    注意: 此函数已废弃，请使用 harness/paths.find_root()
    """
    # 委托给 paths.py 的实现
    try:
        from paths import find_root as _find_root_from_paths
        return _find_root_from_paths(start)
    except ImportError:
        # 降级：使用本地实现
        _find_root_deprecation_warning()
        return _local_find_root(start)


def _local_find_root(start: Path | str | None = None) -> Path:
    """本地实现（当 paths.py 不可用时的降级方案）"""
    if start is None:
        start = Path.cwd()
    elif isinstance(start, str):
        start = Path(start)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        p = Path(project_dir)
        if (p / ".claude").exists() or (p / "harness").exists():
            return p

    current = start.resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".claude").exists() or (parent / "harness").exists():
            return parent

    return Path.cwd()


def _find_root() -> Path:
    """kb_shared 兼容别名（避免循环导入）"""
    _find_root_deprecation_warning()
    return find_root()


if __name__ == "__main__":
    print(find_root())
