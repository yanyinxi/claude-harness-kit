#!/usr/bin/env python3
"""
CHK 插件更新通知器 - 管理更新通知状态，避免重复提示

主要功能：
- format_update_notification() → 格式化通知消息
- should_notify() → 检查是否满足通知条件（每日一次）
- save_notification_state() → 记录上次通知时间

使用方式：
  python3 -m harness.evolve_daemon.update_notifier        # 检查并输出通知
  python3 -m harness.evolve_daemon.update_notifier reset   # 重置通知状态
"""
import json
import logging
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 统一 sys.path 设置
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from _daemon_config import load_config

logger = logging.getLogger(__name__)


@dataclass
class UpdateState:
    """更新通知状态"""
    last_check: Optional[str] = None  # 上次检查时间 (ISO)
    last_notified: Optional[str] = None  # 上次通知时间 (ISO)
    notified_version: Optional[str] = None  # 已通知的版本
    notification_count: int = 0  # 累计通知次数


class UpdateNotifier:
    """更新通知器"""

    # 通知冷却时间（小时）
    NOTIFY_COOLDOWN_HOURS = 24

    def __init__(self):
        self._state_file = self._get_state_file()
        self._state = self._load_state()

    def _get_data_dir(self) -> Path:
        """获取数据目录"""
        try:
            config = load_config()
            paths = config.get("paths", {})
            data_dir = paths.get("data_dir", ".claude/data")
            root = Path(__file__).parent.parent.parent
            return root / data_dir
        except Exception:
            return Path.home() / ".claude" / "data"

    def _get_state_file(self) -> Path:
        """获取状态文件路径"""
        data_dir = self._get_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / "update_state.json"

    def _load_state(self) -> UpdateState:
        """加载通知状态"""
        if not self._state_file.exists():
            return UpdateState()

        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
            return UpdateState(
                last_check=data.get("last_check"),
                last_notified=data.get("last_notified"),
                notified_version=data.get("notified_version"),
                notification_count=data.get("notification_count", 0),
            )
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"加载更新状态失败: {e}")
            return UpdateState()

    def _save_state(self):
        """保存通知状态"""
        try:
            data = {
                "last_check": self._state.last_check,
                "last_notified": self._state.last_notified,
                "notified_version": self._state.notified_version,
                "notification_count": self._state.notification_count,
            }
            self._state_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except OSError as e:
            logger.warning(f"保存更新状态失败: {e}")

    def should_notify(self, current_version: str, has_update: bool) -> bool:
        """
        检查是否应该发送通知

        条件：
        1. 有可用更新
        2. 距离上次通知 >= 24 小时
        3. 或者版本变更（上次通知的版本与当前不同）

        Args:
            current_version: 当前远程版本
            has_update: 是否有可用更新

        Returns:
            True 如果应该通知
        """
        if not has_update:
            return False

        now = datetime.now()
        self._state.last_check = now.isoformat()

        # 首次通知
        if self._state.last_notified is None:
            return True

        # 检查冷却时间
        last_notified = datetime.fromisoformat(self._state.last_notified)
        hours_since = (now - last_notified).total_seconds() / 3600

        if hours_since < self.NOTIFY_COOLDOWN_HOURS:
            return False

        # 检查版本是否变更
        if self._state.notified_version != current_version:
            return True

        # 版本未变但超过 7 天，强制通知一次
        if hours_since >= 24 * 7:
            return True

        return False

    def mark_notified(self, version: str):
        """标记已通知"""
        self._state.last_notified = datetime.now().isoformat()
        self._state.notified_version = version
        self._state.notification_count += 1
        self._save_state()

    def get_state(self) -> dict:
        """获取当前状态"""
        return asdict(self._state)

    def reset(self):
        """重置通知状态"""
        self._state = UpdateState()
        self._save_state()


# ── 全局单例 ──────────────────────────────────────────────────────────────────

_notifier: Optional[UpdateNotifier] = None


def get_notifier() -> UpdateNotifier:
    """获取全局通知器实例"""
    global _notifier
    if _notifier is None:
        _notifier = UpdateNotifier()
    return _notifier


def format_update_notification(local: str, remote: str, release_url: str = "") -> str:
    """
    格式化更新通知消息

    格式参考 Claude Code 升级提示风格：

    ╔════════════════════════════════════════════════════════════╗
    ║  🔔 CHK 插件更新可用                                       ║
    ╠════════════════════════════════════════════════════════════╣
    ║  当前版本: 0.9.1                                            ║
    ║  最新版本: 0.10.0                                           ║
    ╠════════════════════════════════════════════════════════════╣
    ║  更新命令: claude plugins update chk                       ║
    ╚════════════════════════════════════════════════════════════╝
    """
    box_width = 56
    lines = [
        "",
        "╔" + "═" * (box_width - 2) + "╗",
        "║" + "  🔔 CHK 插件更新可用".ljust(box_width - 2) + "║",
        "╠" + "═" * (box_width - 2) + "╣",
        f"║  当前版本: {local}".ljust(box_width - 1) + "║",
        f"║  最新版本: {remote}".ljust(box_width - 1) + "║",
        "╠" + "═" * (box_width - 2) + "╣",
        "║  更新命令: claude plugins update chk".ljust(box_width - 1) + "║",
    ]

    if release_url:
        lines.append(f"║  详情: {release_url[:40]}...".ljust(box_width - 1) + "║")

    lines.append("╚" + "═" * (box_width - 2) + "╝")

    return "\n".join(lines)


def run_update_check() -> str:
    """
    执行完整的更新检查流程

    Returns:
        更新通知消息（如果有更新且应该通知），否则返回空字符串
    """
    from harness._core.update_checker import check_update, get_local_version

    # 执行版本检查
    info = check_update()

    if not info.has_update:
        return ""

    # 检查是否应该通知
    notifier = get_notifier()

    if not notifier.should_notify(info.remote_version, info.has_update):
        # 静默模式：只记录检查时间
        logger.debug(f"更新检查完成（冷却中）: 本地={info.local_version} 远程={info.remote_version}")
        return ""

    # 格式化并发送通知
    message = format_update_notification(
        local=info.local_version,
        remote=info.remote_version,
        release_url=info.release_url,
    )

    # 标记已通知
    notifier.mark_notified(info.remote_version)

    return message


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="CHK 插件更新通知器")
    parser.add_argument("action", nargs="?", default="check", help="操作: check/reset/status")
    args = parser.parse_args()

    notifier = get_notifier()

    if args.action == "reset":
        notifier.reset()
        print("更新通知状态已重置")
        return

    if args.action == "status":
        state = notifier.get_state()
        print(f"当前状态:")
        for key, value in state.items():
            print(f"  {key}: {value}")
        return

    # 默认执行检查
    message = run_update_check()
    if message:
        print(message)
    else:
        print("[CHK] 当前版本已是最新或处于通知冷却期")


if __name__ == "__main__":
    main()