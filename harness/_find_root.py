#!/usr/bin/env python3
"""
统一路径解析模块
所有模块的 find_root() / get_project_root() / get_harness_root() 统一入口
"""
from pathlib import Path
import os


def find_root() -> Path:
    """
    获取项目根目录（支持环境变量覆盖）。

    优先级:
      1. CLAUDE_PROJECT_DIR 环境变量
      2. 当前工作目录（os.getcwd()）

    所有 evolve-daemon 和 CLI 模块统一使用此函数。
    """
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def get_project_root() -> Path:
    """find_root() 的别名，保持向后兼容"""
    return find_root()


def get_harness_root() -> Path:
    """获取 harness/ 目录"""
    return find_root() / "harness"


def get_data_dir() -> Path:
    """获取 .claude/data/ 目录"""
    return find_root() / ".claude" / "data"


def get_knowledge_dir() -> Path:
    """获取 harness/knowledge/ 目录"""
    return find_root() / "harness" / "knowledge"


def get_memory_dir() -> Path:
    """获取 harness/memory/ 目录"""
    return find_root() / "harness" / "memory"


def get_instinct_path() -> Path:
    """获取 instinct-record.json 路径"""
    return get_memory_dir() / "instinct-record.json"


# 向后兼容别名
get_project_dir = find_root