#!/usr/bin/env python3
"""
scheduler 模块测试
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# 添加父目录到 path
sys.path.insert(0, str(Path(__file__).parent))

# 导入前先确保模块路径正确
import importlib.util
spec = importlib.util.spec_from_file_location("scheduler", Path(__file__).parent / "scheduler.py")
scheduler_module = importlib.util.module_from_spec(spec)
sys.modules["scheduler"] = scheduler_module
spec.loader.exec_module(scheduler_module)

parse_interval = scheduler_module.parse_interval
SchedulerManager = scheduler_module.SchedulerManager
load_config = scheduler_module.load_config
APSCHEDULER_AVAILABLE = scheduler_module.APSCHEDULER_AVAILABLE


class TestParseInterval(unittest.TestCase):
    """测试 parse_interval 函数"""

    def test_parse_seconds(self):
        self.assertEqual(parse_interval("30 seconds"), 30)
        self.assertEqual(parse_interval("30 s"), 30)
        self.assertEqual(parse_interval("60 seconds"), 60)

    def test_parse_minutes(self):
        self.assertEqual(parse_interval("30 minutes"), 1800)
        self.assertEqual(parse_interval("30 m"), 1800)
        self.assertEqual(parse_interval("1 minute"), 60)

    def test_parse_hours(self):
        self.assertEqual(parse_interval("2 hours"), 7200)
        self.assertEqual(parse_interval("2 h"), 7200)
        self.assertEqual(parse_interval("1 hour"), 3600)

    def test_parse_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_interval("invalid")
        with self.assertRaises(ValueError):
            parse_interval("30")
        with self.assertRaises(ValueError):
            parse_interval("abc minutes")

    def test_parse_invalid_unit(self):
        with self.assertRaises(ValueError):
            parse_interval("30 days")


class TestSchedulerManager(unittest.TestCase):
    """测试 SchedulerManager 类"""

    def test_singleton(self):
        m1 = SchedulerManager()
        m2 = SchedulerManager()
        self.assertIs(m1, m2)

    def test_status_returns_dict(self):
        # 强制重置状态
        m = SchedulerManager()
        m._running = False
        m._scheduler = None
        status = m.status()
        self.assertIsInstance(status, dict)
        self.assertIn("available", status)

    def test_is_available(self):
        # APScheduler 可用性应该返回布尔值
        self.assertIsInstance(APSCHEDULER_AVAILABLE, bool)


class TestConfigLoading(unittest.TestCase):
    """测试配置加载"""

    def test_load_default_config(self):
        config = load_config()
        self.assertIn("daemon", config)
        self.assertIn("mode", config["daemon"])
        self.assertIn("scheduler_interval", config["daemon"])


if __name__ == "__main__":
    unittest.main()