#!/usr/bin/env python3
"""
daemon.py 测试文件
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# 添加父目录到 path
sys.path.insert(0, str(Path(__file__).parent))

# 导入前先确保模块路径正确
import importlib.util
spec = importlib.util.spec_from_file_location("daemon", Path(__file__).parent / "daemon.py")
daemon_module = importlib.util.module_from_spec(spec)
sys.modules["daemon"] = daemon_module
spec.loader.exec_module(daemon_module)

load_config = daemon_module.load_config
find_root = daemon_module.find_root
check_thresholds = daemon_module.check_thresholds


class TestLoadConfig(unittest.TestCase):
    """测试配置加载"""

    def test_load_config_returns_dict(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn("daemon", config)

    def test_daemon_config_structure(self):
        config = load_config()
        daemon_config = config.get("daemon", {})
        self.assertIn("mode", daemon_config)
        self.assertIn("scheduler_interval", daemon_config)


class TestFindRoot(unittest.TestCase):
    """测试 find_root 函数"""

    def test_find_root_returns_path(self):
        root = find_root()
        self.assertIsInstance(root, Path)


class TestCheckThresholds(unittest.TestCase):
    """测试 check_thresholds 函数"""

    def test_empty_sessions_returns_empty_triggers(self):
        config = load_config()
        triggers = check_thresholds([], config)
        self.assertIsInstance(triggers, list)

    def test_sessions_count_triggers(self):
        config = load_config()
        sessions = [{"session_id": f"session_{i}"} for i in range(10)]
        triggers = check_thresholds(sessions, config)
        self.assertTrue(len(triggers) > 0)


if __name__ == "__main__":
    unittest.main()