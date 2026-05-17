#!/usr/bin/env python3
"""
本能状态管理模块 - 跟踪当前会话已注入的本能

功能：
- 跟踪当前会话已注入的本能
- 避免重复注入相同本能
- 会话结束时清理状态

使用方式：
  from harness._core.instinct_state import get_session_state, mark_instinct_injected
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# 统一 sys.path 设置
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(_project_root))


class SessionState:
    """会话状态管理"""

    def __init__(self):
        self.session_id = self._get_session_id()
        self.state_dir = _project_root / ".claude" / "data"
        self.state_file = self.state_dir / f".memory_session_{self.session_id}.json"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_id(self) -> str:
        """获取会话 ID"""
        # 优先使用环境变量
        session_id = os.environ.get("CLAUDE_CODE_SESSION_ID")
        if session_id:
            return session_id

        # 回退到时间戳
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _load_state(self) -> dict:
        """加载状态"""
        if not self.state_file.exists():
            return {
                "session_id": self.session_id,
                "injected_L0": False,
                "injected_L0_at": None,
                "injected_instincts": [],
                "L1_matches": [],
                "created_at": datetime.now().isoformat(),
            }

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {
                "session_id": self.session_id,
                "injected_L0": False,
                "injected_L0_at": None,
                "injected_instincts": [],
                "L1_matches": [],
                "created_at": datetime.now().isoformat(),
            }

    def _save_state(self, state: dict):
        """保存状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def is_L0_injected(self) -> bool:
        """检查 L0 是否已注入"""
        state = self._load_state()
        return state.get("injected_L0", False)

    def mark_L0_injected(self):
        """标记 L0 已注入"""
        state = self._load_state()
        state["injected_L0"] = True
        state["injected_L0_at"] = datetime.now().isoformat()
        self._save_state(state)

    def is_instinct_injected(self, instinct_id: str) -> bool:
        """检查本能是否已注入"""
        state = self._load_state()
        return instinct_id in state.get("injected_instincts", [])

    def mark_instinct_injected(self, instinct_id: str):
        """标记本能已注入"""
        state = self._load_state()
        if instinct_id not in state.get("injected_instincts", []):
            state.setdefault("injected_instincts", []).append(instinct_id)
            self._save_state(state)

    def add_L1_match(self, category: str):
        """添加 L1 匹配"""
        state = self._load_state()
        if category not in state.get("L1_matches", []):
            state.setdefault("L1_matches", []).append(category)
            self._save_state(state)

    def get_uninjected_instincts(self, instinct_ids: list[str]) -> list[str]:
        """获取未注入的本能 ID 列表"""
        state = self._load_state()
        injected = set(state.get("injected_instincts", []))
        return [iid for iid in instinct_ids if iid not in injected]

    def clear(self):
        """清理状态"""
        if self.state_file.exists():
            self.state_file.unlink()

    def get_state(self) -> dict:
        """获取当前状态"""
        return self._load_state()


# 全局单例
_session_state: Optional[SessionState] = None


def get_session_state() -> SessionState:
    """获取会话状态单例"""
    global _session_state
    if _session_state is None:
        _session_state = SessionState()
    return _session_state


def cleanup_all_sessions():
    """清理所有会话状态"""
    state_dir = _project_root / ".claude" / "data"
    if not state_dir.exists():
        return

    for f in state_dir.glob(".memory_session_*.json"):
        try:
            f.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    # 测试
    print("=== 会话状态测试 ===")

    state = get_session_state()
    print(f"会话 ID: {state.session_id}")
    print(f"状态文件: {state.state_file}")

    print(f"\nL0 已注入: {state.is_L0_injected()}")
    print(f"当前状态: {state.get_state()}")