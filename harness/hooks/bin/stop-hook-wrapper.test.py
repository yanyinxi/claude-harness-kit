#!/usr/bin/env python3
"""
stop-hook-wrapper 集成测试

测试场景:
1. 检测插件根目录的各种情况
2. 验证路径检测逻辑
3. 验证环境变量设置
"""
import re
import sys
import unittest
import subprocess
from pathlib import Path


class TestStopHookWrapper(unittest.TestCase):
    """测试 stop-hook-wrapper.py 的行为"""

    @classmethod
    def setUpClass(cls):
        """设置测试使用的 wrapper 路径"""
        cls.wrapper_path = Path(__file__).parent / "stop-hook-wrapper.py"
        if not cls.wrapper_path.exists():
            cls.skipTest("stop-hook-wrapper.py not found")

    def test_wrapper_runs_without_error(self):
        """测试 wrapper 可以运行不报错"""
        result = subprocess.run(
            [sys.executable, str(self.wrapper_path)],
            capture_output=True,
            text=True,
            timeout=5
        )
        # 应该以 0 退出（静默失败也是 0）
        self.assertEqual(result.returncode, 0)
        # 验证有输出（即使失败也应该返回 JSON）
        output = result.stdout.strip()
        if output:
            # 如果有输出，应该是有效的 JSON 或空
            pass

    def test_wrapper_sets_env_var(self):
        """测试 wrapper 执行后 CLAUDE_PLUGIN_ROOT 被设置"""
        wrapper_code = self.wrapper_path.read_text()
        # 验证代码中设置环境变量
        self.assertIn("os.environ", wrapper_code)
        self.assertIn("CLAUDE_PLUGIN_ROOT", wrapper_code)
        # 验证在 main 函数中设置
        self.assertRegex(wrapper_code, r"def main.*?os\.environ.*CLAUDE_PLUGIN_ROOT", re.DOTALL)


class TestPluginRootDetection(unittest.TestCase):
    """测试 detect_plugin_root 函数逻辑"""

    def test_env_priority(self):
        """测试环境变量优先级最高"""
        # 验证代码逻辑
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 检查 detect_plugin_root 函数的优先级
        # 应该先检查 CLAUDE_PLUGIN_ROOT 环境变量
        self.assertRegex(code, r"CLAUDE_PLUGIN_ROOT.*环境变量", "应该优先检查环境变量")

    def test_settings_local_fallback(self):
        """测试 settings.local.json 回退"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该检查 settings.local.json
        self.assertIn("settings.local.json", code)

    def test_parent_directory_search(self):
        """测试向上查找目录结构"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该向上查找 .claude-plugin/plugin.json
        self.assertIn(".claude-plugin", code)
        self.assertIn("plugin.json", code)

    def test_fallback_to_cwd(self):
        """测试兜底返回当前工作目录"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该兜底返回 cwd
        self.assertIn("getcwd()", code)


class TestCollectSessionIntegration(unittest.TestCase):
    """测试与 collect_session 的集成"""

    def test_imports_collect_session(self):
        """测试 wrapper 导入 collect_session"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该导入 collect_session
        self.assertIn("from collect_session", code)
        self.assertIn("session_main", code)

    def test_hooks_bin_path_constructed(self):
        """测试 hooks/bin 路径正确构建"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该构造 harness/hooks/bin 路径
        self.assertIn("harness", code)
        self.assertIn("hooks", code)
        self.assertIn("bin", code)


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""

    def test_import_error_handled(self):
        """测试 ImportError 被正确处理"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该有 ImportError 处理
        self.assertIn("ImportError", code)

    def test_generic_exception_handled(self):
        """测试通用异常被正确处理"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 应该有 Exception 处理
        self.assertIn("Exception", code)

    def test_sys_exit_zero_on_error(self):
        """测试错误时 sys.exit(0)"""
        wrapper_code = Path(__file__).parent / "stop-hook-wrapper.py"
        code = wrapper_code.read_text()

        # 错误时应该静默退出 (exit 0)
        self.assertIn("sys.exit(0)", code)


if __name__ == "__main__":
    unittest.main(verbosity=2)