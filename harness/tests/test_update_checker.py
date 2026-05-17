#!/usr/bin/env python3
"""
CHK 更新检测系统测试

覆盖模块：
- harness/_core/update_checker.py
- harness/evolve-daemon/update_notifier.py
- hooks/bin/check-update.sh

运行方式：
  python3 -m pytest harness/tests/test_update_checker.py -v
  python3 harness/tests/test_update_checker.py  # 直接运行
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 统一 sys.path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "harness"))

# ============================================================
# 测试 update_checker.py
# ============================================================

class TestUpdateChecker(unittest.TestCase):
    """update_checker 模块测试"""

    @classmethod
    def setUpClass(cls):
        """加载模块"""
        from harness._core import update_checker
        cls.module = update_checker

    def test_parse_version(self):
        """测试版本号解析"""
        # 标准格式
        self.assertEqual(self.module.parse_version("0.9.1"), (0, 9, 1))
        self.assertEqual(self.module.parse_version("1.2.3"), (1, 2, 3))

        # 带 v 前缀
        self.assertEqual(self.module.parse_version("v0.9.1"), (0, 9, 1))
        self.assertEqual(self.module.parse_version("v1.0.0"), (1, 0, 0))

        # 带预发布标签
        self.assertEqual(self.module.parse_version("0.9.1-beta"), (0, 9, 1))
        self.assertEqual(self.module.parse_version("v1.0.0-rc.1"), (1, 0, 0))

        # 边界情况
        self.assertEqual(self.module.parse_version("0"), (0, 0, 0))
        self.assertEqual(self.module.parse_version(""), (0, 0, 0))
        self.assertEqual(self.module.parse_version("invalid"), (0, 0, 0))

    def test_compare_versions(self):
        """测试版本比较"""
        # 大于
        self.assertEqual(self.module.compare_versions("1.0.0", "0.9.0"), 1)
        self.assertEqual(self.module.compare_versions("0.10.0", "0.9.0"), 1)

        # 等于
        self.assertEqual(self.module.compare_versions("0.9.1", "0.9.1"), 0)
        self.assertEqual(self.module.compare_versions("v0.9.1", "0.9.1"), 0)

        # 小于
        self.assertEqual(self.module.compare_versions("0.9.0", "1.0.0"), -1)
        self.assertEqual(self.module.compare_versions("0.8.0", "0.9.0"), -1)

    def test_get_local_version(self):
        """测试获取本地版本"""
        version = self.module.get_local_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)
        # 应该是有效的 semver 格式
        parts = version.lstrip('v').split('.')
        self.assertLessEqual(len(parts), 3)

    def test_format_update_message_no_update(self):
        """测试无更新时的消息格式化"""
        from dataclasses import dataclass

        info = self.module.UpdateInfo(
            has_update=False,
            local_version="1.0.0",
            remote_version="1.0.0",
        )
        message = self.module.format_update_message(info)
        self.assertEqual(message, "")  # 无更新返回空字符串

    def test_format_update_message_has_update(self):
        """测试有更新时的消息格式化"""
        info = self.module.UpdateInfo(
            has_update=True,
            local_version="0.9.1",
            remote_version="1.0.0",
            release_url="https://github.com/test/releases/tag/v1.0.0",
        )
        message = self.module.format_update_message(info)
        self.assertIn("CHK 插件更新可用", message)
        self.assertIn("0.9.1", message)
        self.assertIn("1.0.0", message)
        self.assertIn("claude plugins update chk", message)

    @patch('subprocess.run')
    def test_get_remote_version_api_success(self, mock_run):
        """测试 GitHub API 获取版本成功（通过 curl）"""
        # 模拟 curl 输出 JSON
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({
                "tag_name": "v1.0.0",
                "html_url": "https://github.com/test/releases/tag/v1.0.0",
                "body": "Release notes"
            })
        )

        version, url, notes = self.module.get_remote_version()
        self.assertEqual(version, "v1.0.0")
        self.assertIn("github.com", url)

    @patch('subprocess.run')
    def test_get_remote_version_fallback_git_tags(self, mock_run):
        """测试 GitHub API 失败时使用 git tags"""
        # 模拟 git tag 输出
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="v0.9.1\nv0.8.0\nv0.7.0\n"
        )

        version, url, notes = self.module.get_remote_version()
        # git tags 会返回第一个（最新）tag
        self.assertIn("v0.9.1", version)

    def test_check_update_has_update(self):
        """测试检查更新 - 有可用更新"""
        with patch.object(self.module, 'get_remote_version', return_value=("v1.0.0", "", "")):
            info = self.module.check_update()
            # 如果本地版本 < v1.0.0，应该有更新
            local = self.module.parse_version(info.local_version)
            remote = self.module.parse_version("v1.0.0")
            if local < remote:
                self.assertTrue(info.has_update)
                self.assertEqual(info.remote_version, "v1.0.0")

    def test_check_update_no_update(self):
        """测试检查更新 - 无可用更新"""
        with patch.object(self.module, 'get_remote_version', return_value=("v0.0.1", "", "")):
            info = self.module.check_update()
            # 0.0.1 非常小，大多数版本都比它大
            if info.remote_version != "0.0.0":
                self.assertFalse(info.has_update)


# ============================================================
# 测试 update_notifier.py
# ============================================================

class TestUpdateNotifier(unittest.TestCase):
    """update_notifier 模块测试"""

    @classmethod
    def setUpClass(cls):
        """加载模块"""
        import types
        import sys
        import shutil

        # 保存原始状态文件
        _project_root = Path(__file__).parent.parent.parent
        state_file = _project_root / ".claude" / "data" / "update_state.json"
        backup_file = _project_root / ".claude" / "data" / "update_state.json.test_backup"
        if state_file.exists():
            shutil.copy(state_file, backup_file)

        cls._backup_file = backup_file
        cls._state_file = state_file

        # 手动加载 _daemon_config 依赖
        if '_daemon_config' not in sys.modules:
            spec = __import__('importlib.util').util.spec_from_file_location(
                '_daemon_config',
                str(_project_root / "harness" / "evolve-daemon" / "_daemon_config.py")
            )
            module = __import__('importlib.util').util.module_from_spec(spec)
            sys.modules['_daemon_config'] = module
            spec.loader.exec_module(module)

        # 重置单例
        import update_notifier
        update_notifier._notifier = None
        cls.module = update_notifier

    @classmethod
    def tearDownClass(cls):
        """恢复原始状态"""
        import shutil
        if cls._backup_file.exists():
            shutil.move(str(cls._backup_file), str(cls._state_file))

    def setUp(self):
        """每个测试前重置通知器状态"""
        # 重置单例
        self.module._notifier = None

    def test_should_notify_first_time(self):
        """测试首次通知应该触发"""
        notifier = self.module.get_notifier()
        notifier.reset()
        self.assertTrue(notifier.should_notify("v1.0.0", True))

    def test_should_notify_no_update(self):
        """测试无更新时不触发通知"""
        notifier = self.module.get_notifier()
        notifier.reset()
        self.assertFalse(notifier.should_notify("v1.0.0", False))

    def test_mark_notified(self):
        """测试标记已通知"""
        notifier = self.module.get_notifier()
        notifier.reset()

        # 模拟通知
        notifier.mark_notified("v1.0.0")

        state = notifier.get_state()
        self.assertEqual(state["notified_version"], "v1.0.0")
        self.assertEqual(state["notification_count"], 1)
        self.assertIsNotNone(state["last_notified"])

    def test_format_update_notification(self):
        """测试通知格式化"""
        message = self.module.format_update_notification(
            local="0.9.1",
            remote="1.0.0",
            release_url="https://github.com/test/releases/tag/v1.0.0"
        )
        self.assertIn("CHK 插件更新可用", message)
        self.assertIn("当前版本: 0.9.1", message)
        self.assertIn("最新版本: 1.0.0", message)
        self.assertIn("claude plugins update chk", message)
        self.assertIn("╔", message)  # 框线

    def test_reset(self):
        """测试重置通知状态"""
        notifier = self.module.get_notifier()
        notifier.mark_notified("v1.0.0")
        notifier.reset()

        state = notifier.get_state()
        self.assertIsNone(state["last_notified"])
        self.assertIsNone(state["notified_version"])
        self.assertEqual(state["notification_count"], 0)


# ============================================================
# 测试 Shell 钩子脚本
# ============================================================

class TestCheckUpdateShell(unittest.TestCase):
    """check-update.sh 脚本测试"""

    @classmethod
    def setUpClass(cls):
        cls.script_path = _project_root / "hooks" / "bin" / "check-update.sh"
        cls.assertTrue(cls.script_path.exists(), f"脚本不存在: {cls.script_path}")

    def test_script_has_execute_permission(self):
        """测试脚本有执行权限"""
        self.assertTrue(os.access(self.script_path, os.X_OK),
                        f"脚本没有执行权限: {self.script_path}")

    def test_script_syntax(self):
        """测试脚本语法正确"""
        import subprocess
        result = subprocess.run(
            ["bash", "-n", str(self.script_path)],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0,
                        f"脚本语法错误: {result.stderr}")

    def test_version_lt_function(self):
        """测试版本比较函数"""
        import subprocess

        # 直接测试 Python 版本的版本比较逻辑
        from harness._core.update_checker import compare_versions

        # 测试 v1 < v2
        self.assertEqual(compare_versions("0.9.0", "1.0.0"), -1)

        # 测试 v1 > v2
        self.assertEqual(compare_versions("1.0.0", "0.9.0"), 1)

        # 测试 v1 == v2
        self.assertEqual(compare_versions("1.0.0", "1.0.0"), 0)

    def test_get_local_version(self):
        """测试获取本地版本"""
        from harness._core.update_checker import get_local_version

        version = get_local_version()
        self.assertNotEqual(version, "unknown")
        self.assertNotEqual(version, "")
        # 应该是有效的 semver 格式
        parts = version.lstrip('v').split('.')
        self.assertLessEqual(len(parts), 3)


# ============================================================
# 集成测试
# ============================================================

class TestUpdateIntegration(unittest.TestCase):
    """更新系统集成测试"""

    def setUp(self):
        """创建测试数据目录"""
        self.data_dir = _project_root / ".claude" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 备份状态文件
        self.state_file = self.data_dir / "update_state.json"
        self.backup_file = self.data_dir / "update_state.json.bak"
        if self.state_file.exists():
            import shutil
            shutil.copy(self.state_file, self.backup_file)

    def tearDown(self):
        """清理测试数据"""
        # 恢复状态文件
        if self.backup_file.exists():
            import shutil
            shutil.move(self.backup_file, self.state_file)

        # 清理钩子生成的临时文件
        for temp_file in [".last_update_check", ".notified_version"]:
            temp_path = self.data_dir / temp_file
            if temp_path.exists():
                temp_path.unlink()

    def test_update_workflow(self):
        """测试完整更新工作流"""
        import subprocess

        # 1. 清除冷却状态
        for temp_file in [".last_update_check", ".notified_version"]:
            temp_path = self.data_dir / temp_file
            if temp_path.exists():
                temp_path.unlink()

        # 2. 运行更新检查脚本
        result = subprocess.run(
            ["bash", str(_project_root / "hooks" / "bin" / "check-update.sh")],
            capture_output=True,
            text=True,
            cwd=str(_project_root)
        )

        # 3. 验证：如果有更新，会输出通知
        # 如果没有更新（当前版本已是最新），则无输出
        # 这是预期行为，不应报错

        # 4. 检查冷却状态文件是否创建
        last_check = self.data_dir / ".last_update_check"
        self.assertTrue(last_check.exists(), "应该创建冷却状态文件")


# ============================================================
# 运行入口
# ============================================================

if __name__ == "__main__":
    # 支持直接运行和 pytest 运行
    unittest.main(verbosity=2)