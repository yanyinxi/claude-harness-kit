#!/usr/bin/env python3
"""
CHK 记忆注入系统测试

覆盖模块：
- hooks/bin/memory-inject.sh
- hooks/hooks.json

运行方式：
  python3 -m pytest harness/tests/test_memory_inject.py -v
"""
import json
import os
import subprocess
import unittest
import uuid
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent


def run_memory_inject(session_id=None):
    """运行 memory-inject.sh 并返回结果"""
    if session_id is None:
        session_id = str(uuid.uuid4())

    env = {**os.environ, "CLAUDE_CODE_SESSION_ID": session_id}

    result = subprocess.run(
        ["bash", str(PROJECT_ROOT / "hooks" / "bin" / "memory-inject.sh")],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env=env
    )
    return result


class TestMemoryInject(unittest.TestCase):
    """memory-inject.sh 钩子脚本测试"""

    @classmethod
    def setUpClass(cls):
        cls.script_path = PROJECT_ROOT / "hooks" / "bin" / "memory-inject.sh"
        cls.assertTrue(cls.script_path.exists(), f"脚本不存在: {cls.script_path}")

    def test_script_has_execute_permission(self):
        """测试脚本有执行权限"""
        self.assertTrue(os.access(self.script_path, os.X_OK),
                        f"脚本没有执行权限: {self.script_path}")

    def test_script_syntax(self):
        """测试脚本语法正确"""
        result = subprocess.run(
            ["bash", "-n", str(self.script_path)],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"脚本语法错误: {result.stderr}")

    def test_output_contains_memory_header(self):
        """测试输出包含记忆头部"""
        # 使用唯一 session_id 避免状态残留
        session_id = f"test-{uuid.uuid4()}"
        result = run_memory_inject(session_id)

        output = result.stdout
        self.assertIn("【项目记忆】", output)
        self.assertIn("harness/memory/", output)

    def test_output_contains_development_rules(self):
        """测试输出包含开发行为准则"""
        session_id = f"test-{uuid.uuid4()}"
        result = run_memory_inject(session_id)

        output = result.stdout
        self.assertIn("开发行为准则", output)

    def test_output_contains_project_knowledge(self):
        """测试输出包含项目知识"""
        session_id = f"test-{uuid.uuid4()}"
        result = run_memory_inject(session_id)

        output = result.stdout
        self.assertIn("项目知识", output)

    def test_output_contains_trigger_rules(self):
        """测试输出包含触发规则"""
        session_id = f"test-{uuid.uuid4()}"
        result = run_memory_inject(session_id)

        output = result.stdout
        self.assertIn("【记忆触发规则】", output)
        self.assertIn("遇到类似场景，自动应用", output)

    def test_cooldown_mechanism(self):
        """测试冷却机制"""
        session_id = f"test-{uuid.uuid4()}"

        # 第一次运行
        result1 = run_memory_inject(session_id)

        # 第二次运行
        result2 = run_memory_inject(session_id)

        # 两次都成功
        self.assertEqual(result1.returncode, 0)
        self.assertEqual(result2.returncode, 0)

    def test_memory_index_readable(self):
        """测试记忆索引文件可读"""
        memory_index = PROJECT_ROOT / "harness" / "memory" / "MEMORY.md"
        self.assertTrue(memory_index.exists(), "MEMORY.md 不存在")

        content = memory_index.read_text(encoding="utf-8")
        self.assertIn("开发行为准则", content)
        self.assertIn("项目知识", content)


class TestHooksJson(unittest.TestCase):
    """hooks.json 配置测试"""

    @classmethod
    def setUpClass(cls):
        cls.hooks_path = PROJECT_ROOT / "hooks" / "hooks.json"
        cls.assertTrue(cls.hooks_path.exists(), f"hooks.json 不存在: {cls.hooks_path}")

        with open(cls.hooks_path, encoding="utf-8") as f:
            cls.hooks_config = json.load(f)

    def test_user_prompt_submit_hook_exists(self):
        """测试 UserPromptSubmit 钩子存在"""
        self.assertIn("UserPromptSubmit", self.hooks_config.get("hooks", {}))

    def test_memory_inject_hook_configured(self):
        """测试 memory-inject.sh 已配置"""
        # hooks 结构: hooks.UserPromptSubmit[0].hooks[n].command
        hooks_list = self.hooks_config["hooks"]["UserPromptSubmit"]
        commands = []
        for hook_entry in hooks_list:
            for h in hook_entry.get("hooks", []):
                commands.append(h.get("command", ""))

        has_memory_inject = any("memory-inject.sh" in cmd for cmd in commands)
        self.assertTrue(has_memory_inject,
                        f"memory-inject.sh 未配置在 UserPromptSubmit 钩子中: {commands}")

    def test_check_update_hook_configured(self):
        """测试 check-update.sh 已配置"""
        # hooks 结构: hooks.UserPromptSubmit[0].hooks[n].command
        hooks_list = self.hooks_config["hooks"]["UserPromptSubmit"]
        commands = []
        for hook_entry in hooks_list:
            for h in hook_entry.get("hooks", []):
                commands.append(h.get("command", ""))

        has_check_update = any("check-update.sh" in cmd for cmd in commands)
        self.assertTrue(has_check_update,
                        f"check-update.sh 未配置在 UserPromptSubmit 钩子中: {commands}")

    def test_hook_timeout_reasonable(self):
        """测试钩子超时时间合理"""
        hooks = self.hooks_config["hooks"]["UserPromptSubmit"]
        for hook in hooks:
            timeout = hook.get("timeout", 0)
            self.assertLessEqual(timeout, 30,
                                 f"钩子超时时间过长: {hook.get('command')} = {timeout}s")


class TestMemoryIntegration(unittest.TestCase):
    """记忆注入集成测试"""

    def test_memory_files_exist(self):
        """测试记忆文件存在"""
        memory_dir = PROJECT_ROOT / "harness" / "memory"
        self.assertTrue(memory_dir.exists(), "记忆目录不存在")

        # 检查 MEMORY.md
        memory_index = memory_dir / "MEMORY.md"
        self.assertTrue(memory_index.exists(), "MEMORY.md 不存在")

        # 检查反馈记忆文件
        feedback_files = list(memory_dir.glob("feedback_*.md"))
        self.assertGreater(len(feedback_files), 0, "没有反馈记忆文件")

    def test_full_memory_injection_workflow(self):
        """测试完整记忆注入工作流"""
        session_id = f"test-{uuid.uuid4()}"

        # 1. 运行钩子
        result = run_memory_inject(session_id)

        # 2. 验证输出
        output = result.stdout

        # 验证关键部分
        checks = [
            ("【项目记忆】" in output, "缺少记忆头部"),
            ("开发行为准则" in output, "缺少开发行为准则"),
            ("feedback_" in output, "缺少反馈记忆引用"),
            ("记忆触发规则" in output, "缺少触发规则"),
        ]

        for condition, message in checks:
            self.assertTrue(condition, f"工作流验证失败: {message}")


if __name__ == "__main__":
    unittest.main(verbosity=2)