#!/usr/bin/env python3
"""
本能读取模块测试
"""
import sys
import unittest
from pathlib import Path

# 设置路径
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "harness"))

from harness._core.instinct_reader import (
    get_high_confidence_instincts,
    format_instinct_for_injection,
    format_all_instincts_for_injection,
    get_instinct_stats,
    DEFAULT_MIN_CONFIDENCE,
    Instinct,
)


class TestInstinctReader(unittest.TestCase):
    """本能读取模块测试"""

    def test_get_high_confidence_instincts(self):
        """测试获取高置信度本能"""
        instincts = get_high_confidence_instincts()
        self.assertIsInstance(instincts, list)
        # 验证所有本能都 >= 阈值
        for instinct in instincts:
            self.assertGreaterEqual(instinct.confidence, DEFAULT_MIN_CONFIDENCE)

    def test_format_instinct_for_injection(self):
        """测试格式化单个本能"""
        instinct = Instinct(
            id="test-1",
            pattern="不要用 eval",
            confidence=0.85,
            applied_count=3,
            reinforcement_count=2,
            source="user-correction",
            created_at="2026-05-17T10:00:00",
            root_cause="安全风险",
        )

        output = format_instinct_for_injection(instinct)
        self.assertIn("不要用 eval", output)
        self.assertIn("85%", output)
        self.assertIn("应用: 3次", output)

    def test_format_all_instincts_for_injection(self):
        """测试格式化所有本能"""
        instincts = get_high_confidence_instincts()
        if instincts:
            output = format_all_instincts_for_injection(instincts)
            self.assertIn("【本能记录】", output)
            self.assertIn("confidence", output.lower())
        else:
            self.skipTest("No high confidence instincts")

    def test_get_instinct_stats(self):
        """测试本能统计"""
        stats = get_instinct_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("total", stats)
        self.assertIn("high_confidence", stats)
        self.assertIn("avg_confidence", stats)
        self.assertGreaterEqual(stats["total"], 0)
        self.assertLessEqual(stats["high_confidence"], stats["total"])


class TestInstinctState(unittest.TestCase):
    """本能状态管理测试"""

    def test_session_state(self):
        """测试会话状态管理"""
        from harness._core.instinct_state import get_session_state, cleanup_all_sessions

        # 清理所有会话
        cleanup_all_sessions()

        # 获取会话状态
        state = get_session_state()
        self.assertIsNotNone(state.session_id)
        self.assertFalse(state.is_L0_injected())

        # 标记 L0 已注入
        state.mark_L0_injected()
        self.assertTrue(state.is_L0_injected())

        # 清理
        state.clear()


class TestInstinctApplicationStats(unittest.TestCase):
    """本能应用统计测试"""

    def setUp(self):
        """清理测试环境"""
        import os
        from pathlib import Path

        # 清理统计文件
        test_root = Path(__file__).parent.parent.parent
        stats_file = test_root / ".claude" / "data" / "instinct_stats.json"
        if stats_file.exists():
            stats_file.unlink()

    def test_record_application(self):
        """测试记录本能应用"""
        from harness._core.instinct_reader import record_instinct_application, get_application_stats

        # 记录几次应用
        record_instinct_application("test-1", True)
        record_instinct_application("test-1", True)
        record_instinct_application("test-1", False)
        record_instinct_application("test-2", True)

        stats = get_application_stats()
        self.assertEqual(stats["total_apps"], 4)
        self.assertEqual(stats["total_success"], 3)
        self.assertEqual(stats["success_rate"], 0.75)
        self.assertIn("test-1", stats["by_instinct"])
        self.assertEqual(stats["by_instinct"]["test-1"]["attempts"], 3)
        self.assertEqual(stats["by_instinct"]["test-1"]["successes"], 2)

    def test_format_application_stats(self):
        """测试格式化应用统计"""
        from harness._core.instinct_reader import record_instinct_application, format_application_stats

        # 记录应用
        record_instinct_application("test-1", True)
        record_instinct_application("test-1", False)

        output = format_application_stats()
        self.assertIn("总应用次数", output)
        self.assertIn("成功率", output)


class TestKeywordMatcher(unittest.TestCase):
    """关键词匹配测试"""

    def test_match_keywords(self):
        """测试关键词匹配"""
        from harness._core.keyword_matcher import match_keywords

        # 测试测试相关
        categories = match_keywords("帮我写个单元测试")
        self.assertIn("testing", categories)

        # 测试重构相关
        categories = match_keywords("这个代码需要重构")
        self.assertIn("refactor", categories)

        # 测试安全相关
        categories = match_keywords("发现了一个安全漏洞")
        self.assertIn("security", categories)

        # 测试无匹配
        categories = match_keywords("今天天气怎么样")
        self.assertEqual(len(categories), 0)

    def test_get_matching_files(self):
        """测试获取匹配文件"""
        from harness._core.keyword_matcher import get_matching_files

        files = get_matching_files(["testing", "security"])
        self.assertIsInstance(files, list)
        self.assertIn("harness/memory/feedback_test_required.md", files)


class TestMemoryInject(unittest.TestCase):
    """记忆注入脚本测试"""

    def setUp(self):
        """设置测试路径"""
        # 计算项目根目录：harness/tests/ -> parent -> parent -> 项目根
        test_file = Path(__file__).resolve()
        project_root = test_file.parent.parent.parent
        # 脚本路径
        self.script_path = project_root / "hooks" / "bin" / "memory-inject.sh"

    def test_script_exists(self):
        """测试脚本存在"""
        self.assertTrue(self.script_path.exists(), f"脚本不存在: {self.script_path}")

    def test_script_executable(self):
        """测试脚本可执行"""
        import subprocess
        result = subprocess.run(
            ["bash", "-n", str(self.script_path)],
            capture_output=True
        )
        self.assertEqual(result.returncode, 0)


class TestHookConfig(unittest.TestCase):
    """Hook 配置验证测试"""

    def test_user_prompt_submit_configured(self):
        """验证 UserPromptSubmit 钩子已配置 memory-inject"""
        import json

        hooks_path = _project_root / "hooks" / "hooks.json"
        self.assertTrue(hooks_path.exists(), "hooks.json 不存在")

        with open(hooks_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 检查 UserPromptSubmit 钩子
        self.assertIn("UserPromptSubmit", config.get("hooks", {}))
        user_prompt_hooks = config["hooks"]["UserPromptSubmit"]

        # 检查是否配置了 memory-inject.sh
        found = False
        for hook_config in user_prompt_hooks:
            for hook in hook_config.get("hooks", []):
                if "memory-inject.sh" in hook.get("command", ""):
                    found = True
                    break

        self.assertTrue(found, "UserPromptSubmit 钩子未配置 memory-inject.sh")

    def test_memory_inject_script_exists_and_executable(self):
        """验证 memory-inject.sh 存在且可执行"""
        script_path = _project_root / "hooks" / "bin" / "memory-inject.sh"
        self.assertTrue(script_path.exists(), "memory-inject.sh 不存在")

        # 检查文件权限
        import stat
        mode = script_path.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "memory-inject.sh 不可执行")


if __name__ == "__main__":
    unittest.main(verbosity=2)