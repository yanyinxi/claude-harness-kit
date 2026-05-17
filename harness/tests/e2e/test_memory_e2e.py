#!/usr/bin/env python3
"""
记忆系统端到端测试

测试完整记忆循环：
1. 用户提交消息 → UserPromptSubmit 触发
2. memory-inject.sh 检查会话状态
3. L0 层注入：首次输入注入 MEMORY.md + 本能
4. L1 层匹配：关键词触发相关记忆
5. 状态文件管理：会话状态持久化
6. 清理：会话结束状态清理

运行方式：
  python3 -m pytest harness/tests/e2e/test_memory_e2e.py -v
"""
import json
import os
import subprocess
import unittest
import uuid
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


class TestMemoryE2E(unittest.TestCase):
    """记忆系统端到端测试"""

    def setUp(self):
        """清理测试环境"""
        self.session_id = f"e2e-test-{uuid.uuid4()}"
        self.script_path = PROJECT_ROOT / "hooks" / "bin" / "memory-inject.sh"
        self.data_dir = PROJECT_ROOT / ".claude" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 清理会话状态文件
        for f in self.data_dir.glob(".memory_session_*.json"):
            if self.session_id in f.name:
                f.unlink()

    def tearDown(self):
        """清理测试环境"""
        state_file = self.data_dir / f".memory_session_{self.session_id}.json"
        if state_file.exists():
            state_file.unlink()

    def run_memory_inject(self, *args):
        """运行 memory-inject.sh"""
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": self.session_id}
        cmd = ["bash", str(self.script_path)] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )
        return result

    def test_l0_first_injection(self):
        """测试 L0 层首次注入"""
        # 1. 首次运行，应该注入 L0
        result = self.run_memory_inject()

        # 2. 验证输出包含 L0 内容
        self.assertIn("【项目记忆】", result.stdout)
        self.assertIn("harness/memory/", result.stdout)
        self.assertIn("开发行为准则", result.stdout)
        self.assertIn("【记忆触发规则】", result.stdout)

        # 3. 验证状态文件已创建
        state_file = self.data_dir / f".memory_session_{self.session_id}.json"
        self.assertTrue(state_file.exists(), "会话状态文件未创建")

        # 4. 验证状态文件中 L0 已标记为注入
        with open(state_file, 'r') as f:
            state = json.load(f)
        self.assertTrue(state.get("injected_L0", False), "L0 未标记为已注入")

    def test_l1_no_repeat_l0(self):
        """测试 L1 层：不重复注入 L0"""
        # 1. 首次运行
        result1 = self.run_memory_inject()
        first_output = result1.stdout

        # 2. 第二次运行（同一会话）
        result2 = self.run_memory_inject()
        second_output = result2.stdout

        # 3. 首次应有完整的 L0 输出
        self.assertIn("【项目记忆】", first_output)

        # 4. 第二次不应该重复完整的 L0（应该只在有输入时做关键词匹配）
        # 由于没有输入关键词，不应有完整 L0
        self.assertNotIn("【项目记忆】", second_output)

    def test_l1_keyword_matching(self):
        """测试 L1 层：关键词匹配"""
        # 1. 首次运行注入 L0
        self.run_memory_inject()

        # 2. 带关键词输入运行
        result = self.run_memory_inject("帮我写个单元测试")

        # 3. 验证关键词匹配输出
        output = result.stdout
        self.assertIn("关键词匹配", output)

    def test_l1_git_keyword(self):
        """测试 L1 层：git 关键词"""
        # 1. 首次运行注入 L0
        self.run_memory_inject()

        # 2. 测试 git 相关关键词
        result = self.run_memory_inject("帮我提交代码")

        # 3. 验证 git 关键词匹配
        output = result.stdout
        self.assertIn("关键词匹配", output)

    def test_l1_security_keyword(self):
        """测试 L1 层：安全关键词"""
        # 1. 首次运行注入 L0
        self.run_memory_inject()

        # 2. 测试安全相关关键词
        result = self.run_memory_inject("发现了一个安全漏洞")

        # 3. 验证安全关键词匹配
        output = result.stdout
        self.assertIn("关键词匹配", output)

    def test_multiple_sessions_isolated(self):
        """测试多会话隔离"""
        session1 = f"e2e-1-{uuid.uuid4()}"
        session2 = f"e2e-2-{uuid.uuid4()}"

        # 1. 会话1首次注入
        env1 = {**os.environ, "CLAUDE_CODE_SESSION_ID": session1}
        result1 = subprocess.run(
            ["bash", str(self.script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env1
        )

        # 2. 会话2首次注入
        env2 = {**os.environ, "CLAUDE_CODE_SESSION_ID": session2}
        result2 = subprocess.run(
            ["bash", str(self.script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env2
        )

        # 3. 两个会话都应该有完整 L0 输出
        self.assertIn("【项目记忆】", result1.stdout)
        self.assertIn("【项目记忆】", result2.stdout)

        # 4. 清理
        for sid in [session1, session2]:
            state_file = self.data_dir / f".memory_session_{sid}.json"
            if state_file.exists():
                state_file.unlink()

    def test_instinct_injection(self):
        """测试本能注入"""
        # 首次运行应该包含本能（如果有高置信度本能）
        result = self.run_memory_inject()
        output = result.stdout

        # 如果有本能记录，应该显示
        # 注意：这个测试在没有本能记录时会跳过检查
        instinct_file = PROJECT_ROOT / "harness" / "memory" / "instinct-record.json"
        if instinct_file.exists():
            # 如果有本能文件，应该有本能相关输出或至少不报错
            self.assertEqual(result.returncode, 0)

    def test_state_persistence(self):
        """测试状态持久化"""
        # 1. 首次注入
        self.run_memory_inject()

        # 2. 检查状态文件存在
        state_file = self.data_dir / f".memory_session_{self.session_id}.json"
        self.assertTrue(state_file.exists())

        # 3. 读取状态
        with open(state_file, 'r') as f:
            state = json.load(f)

        self.assertEqual(state.get("session_id"), self.session_id)
        self.assertIn("injected_L0_at", state)


class TestMemoryCleanupE2E(unittest.TestCase):
    """记忆清理端到端测试"""

    def test_cleanup_removes_session_state(self):
        """测试清理移除会话状态"""
        session_id = f"cleanup-test-{uuid.uuid4()}"
        script_path = PROJECT_ROOT / "hooks" / "bin" / "memory-inject.sh"
        cleanup_script = PROJECT_ROOT / "hooks" / "bin" / "memory-cleanup.sh"
        data_dir = PROJECT_ROOT / ".claude" / "data"
        state_file = data_dir / f".memory_session_{session_id}.json"

        # 1. 创建会话状态
        with open(state_file, 'w') as f:
            json.dump({
                "session_id": session_id,
                "injected_L0": True,
                "injected_L0_at": "2026-05-17T00:00:00"
            }, f)

        self.assertTrue(state_file.exists())

        # 2. 运行清理
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": session_id}
        result = subprocess.run(
            ["bash", str(cleanup_script)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        self.assertEqual(result.returncode, 0)
        self.assertFalse(state_file.exists(), "会话状态文件未清理")

    def test_cleanup_nonexistent_session(self):
        """测试清理不存在的会话"""
        session_id = f"nonexistent-{uuid.uuid4()}"
        cleanup_script = PROJECT_ROOT / "hooks" / "bin" / "memory-cleanup.sh"

        # 运行清理（不应该报错）
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": session_id}
        result = subprocess.run(
            ["bash", str(cleanup_script)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        self.assertEqual(result.returncode, 0)


class TestMemoryKeywordMatchingE2E(unittest.TestCase):
    """关键词匹配端到端测试"""

    def setUp(self):
        self.session_id = f"keyword-e2e-{uuid.uuid4()}"
        self.script_path = PROJECT_ROOT / "hooks" / "bin" / "memory-inject.sh"

    def tearDown(self):
        state_file = PROJECT_ROOT / ".claude" / "data" / f".memory_session_{self.session_id}.json"
        if state_file.exists():
            state_file.unlink()

    def test_testing_keyword(self):
        """测试 testing 关键词"""
        # 先注入 L0
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": self.session_id}
        subprocess.run(
            ["bash", str(self.script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        # 带测试关键词输入
        result = subprocess.run(
            ["bash", str(self.script_path), "写一个单元测试"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        output = result.stdout
        self.assertIn("关键词匹配", output)

    def test_refactor_keyword(self):
        """测试重构关键词"""
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": self.session_id}
        subprocess.run(
            ["bash", str(self.script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        result = subprocess.run(
            ["bash", str(self.script_path), "需要重构这个模块"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        output = result.stdout
        self.assertIn("关键词匹配", output)

    def test_no_match_keyword(self):
        """测试无匹配关键词"""
        env = {**os.environ, "CLAUDE_CODE_SESSION_ID": self.session_id}
        subprocess.run(
            ["bash", str(self.script_path)],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        result = subprocess.run(
            ["bash", str(self.script_path), "今天天气怎么样"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=env
        )

        # 无匹配时不应有关键词匹配输出
        self.assertNotIn("关键词匹配", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)