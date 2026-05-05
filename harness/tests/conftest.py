#!/usr/bin/env python3
"""
conftest.py — pytest 共享 fixtures

提供:
  - PROJECT_ROOT: 标准化项目根路径
  - make_session(): 标准 session 构造器
  - get_module(): 动态模块加载
  - EVOLVE_DIR: evolve-daemon 目录路径
"""
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 标准路径设置 ────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EVOLVE_DIR = PROJECT_ROOT / "harness" / "evolve-daemon"

# 强制覆盖 CLAUDE_PROJECT_DIR（防止幽灵目录 bug）
os.environ["CLAUDE_PROJECT_DIR"] = str(PROJECT_ROOT)

# 确保模块可导入
for p in [str(EVOLVE_DIR), str(PROJECT_ROOT / "harness"), str(PROJECT_ROOT / "harness" / "knowledge")]:
    if p not in sys.path:
        sys.path.insert(0, p)


# ── 测试工具函数 ────────────────────────────────────────────────
def make_session(
    session_id: str,
    corrections: Optional[list] = None,
    timestamp: Optional[str] = None,
    status: str = "success",
    tool_failures: int = 0,
    skills_used: Optional[list] = None,
    satisfaction: Optional[float] = None,
) -> dict:
    """标准 session 构造器（所有 evolve-daemon 测试共享）"""
    s = {
        "session_id": session_id,
        "timestamp": timestamp or datetime.now().isoformat(),
        "corrections": corrections or [],
        "correction_count": len(corrections) if corrections else 0,
        "status": status,
        "tool_failures": tool_failures,
        "skills_used": skills_used or [],
        "mode": "solo",
        "duration_minutes": 15,
    }
    if satisfaction is not None:
        s["satisfaction"] = satisfaction
    return s


def make_correction(
    target: str,
    root_cause_hint: str = "unknown",
    context: str = "",
    user_correction: str = "",
) -> dict:
    """标准 correction 构造器"""
    return {
        "target": target,
        "root_cause_hint": root_cause_hint,
        "context": context,
        "user_correction": user_correction,
    }


def get_module(name: str):
    """动态模块加载（避免 import 顺序问题）"""
    import importlib
    return importlib.import_module(name)
