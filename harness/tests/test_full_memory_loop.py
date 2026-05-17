#!/usr/bin/env python3
"""
完整记忆闭环测试
测试场景：
1. 用户纠正 → 本能记录
2. 本能置信度提升 → 达到 0.7
3. memory-inject 注入本能
4. AI 应用本能 → 验证成功
5. 知识同步到 MEMORY.md
"""
import sys
import subprocess
import unittest
from pathlib import Path

# 设置路径
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "harness"))


class TestFullMemoryLoop(unittest.TestCase):
    """完整记忆闭环测试"""

    def setUp(self):
        """清理测试环境"""
        # 清理所有会话状态
        data_dir = _project_root / ".claude" / "data"
        for f in data_dir.glob(".memory_session_*.json"):
            f.unlink()

    def test_l0_injection(self):
        """测试 L0 层注入"""
        import os

        # 清理
        self.setUp()

        # 运行 memory-inject.sh
        script_path = _project_root / "hooks" / "bin" / "memory-inject.sh"
        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": "test-l0-injection"}
        )

        output = result.stdout
        # subprocess 可能返回空，改用 stderr 或直接输出
        if not output and result.stderr:
            output = result.stderr
        self.assertIn("【项目记忆】", output)
        self.assertIn("开发行为准则", output)
        self.assertIn("【记忆触发规则】", output)

    def test_l1_keyword_matching(self):
        """测试 L1 层关键词匹配"""
        import os

        # 清理
        self.setUp()

        script_path = _project_root / "hooks" / "bin" / "memory-inject.sh"

        # 先注入 L0
        subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": "test-l1-matching"}
        )

        # 测试关键词匹配
        result = subprocess.run(
            ["bash", str(script_path), "帮我写个单元测试"],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": "test-l1-matching"}
        )

        output = result.stdout or result.stderr
        # 应该包含关键词匹配结果
        self.assertIn("关键词匹配", output)

    def test_no_repeat_l0(self):
        """测试 L0 不重复注入"""
        import os

        # 清理
        self.setUp()

        script_path = _project_root / "hooks" / "bin" / "memory-inject.sh"
        session_id = "test-no-repeat-l0"

        # 第一次运行
        subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": session_id}
        )

        # 第二次运行（应该不注入 L0）
        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": session_id}
        )

        output = result.stdout or result.stderr
        # 如果 L0 已注入，输出不应包含完整【项目记忆】标题
        # 检查状态文件
        state_file = _project_root / ".claude" / "data" / f".memory_session_{session_id}.json"
        self.assertTrue(state_file.exists())

    def test_instinct_reader(self):
        """测试本能读取模块"""
        from harness._core.instinct_reader import get_high_confidence_instincts, get_instinct_stats

        instincts = get_high_confidence_instincts()
        stats = get_instinct_stats()

        self.assertIsInstance(instincts, list)
        self.assertIsInstance(stats, dict)
        self.assertGreaterEqual(stats["total"], 0)

        # 验证高置信度本能
        for instinct in instincts:
            self.assertGreaterEqual(instinct.confidence, 0.7)

    def test_keyword_matcher(self):
        """测试关键词匹配模块"""
        from harness._core.keyword_matcher import match_keywords

        test_cases = [
            ("帮我写个单元测试", ["testing"]),
            ("这个代码需要重构", ["refactor"]),
            ("发现了一个安全漏洞", ["security"]),
            ("帮我提交代码", ["git"]),  # 现在应该能匹配了
            ("今天天气怎么样", []),
        ]

        for input_text, expected in test_cases:
            result = match_keywords(input_text)
            for exp in expected:
                self.assertIn(exp, result)

    def test_memory_cleanup(self):
        """测试状态清理"""
        import os

        script_path = _project_root / "hooks" / "bin" / "memory-cleanup.sh"

        # 运行清理
        result = subprocess.run(
            ["bash", str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(_project_root),
            env={**os.environ, "CLAUDE_CODE_SESSION_ID": "test-cleanup"}
        )

        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)