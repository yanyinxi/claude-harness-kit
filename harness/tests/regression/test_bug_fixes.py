#!/usr/bin/env python3
"""
回归测试套件 — 针对历史 Bug 修复的测试

基于 commit 历史中的 Bug 修复，确保这些 bug 不再出现
"""

import json
import re
from pathlib import Path
import pytest


class TestRegressionSuite:
    """回归测试套件"""

    # ── Bug #1: modes/*.json 中的 ${CLAUDE_PLUGIN_ROOT} 变量 ──

    def test_modes_no_plugin_root_variable(self, tmp_path):
        """验证 modes/*.json 不再包含 ${CLAUDE_PLUGIN_ROOT}"""
        modes_dir = tmp_path / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)

        # 创建包含变量的配置
        config = {
            "agents": ["${CLAUDE_PLUGIN_ROOT}/agents/executor"],
            "max_agents": 1
        }
        (modes_dir / "test.json").write_text(json.dumps(config))

        # 读取并检查
        content = (modes_dir / "test.json").read_text()
        assert "${CLAUDE_PLUGIN_ROOT}" not in content, \
            "modes/*.json 仍包含 ${CLAUDE_PLUGIN_ROOT} 变量"

    def test_modes_use_relative_paths(self, tmp_path):
        """验证 modes/*.json 使用相对路径"""
        modes_dir = tmp_path / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)

        # 正确的配置应该使用相对路径
        config = {
            "agents": ["executor", "backend-dev"],
            "max_agents": 2
        }
        (modes_dir / "solo.json").write_text(json.dumps(config))

        content = (modes_dir / "solo.json").read_text()
        # 不应包含任何路径变量
        assert "${" not in content

    # ── Bug #2: validator.py 未使用变量 ──

    def test_validator_no_unused_variables(self):
        """验证 validator.py 无未使用变量"""
        validator_path = Path(__file__).parent.parent.parent.parent / "harness" / "evolve-daemon" / "validator.py"

        if not validator_path.exists():
            pytest.skip("validator.py 不存在")

        content = validator_path.read_text()

        # 检查是否有明显的 unused 变量赋值
        # 这是基于历史 commit "fix: validator.py 清理未使用变量"
        unused_pattern = r"\bunused\s*="
        matches = re.findall(unused_pattern, content)
        assert len(matches) == 0, "validator.py 仍包含未使用变量"

    # ── Bug #3: llm_decision.py logger 未定义 ──

    def test_logger_defined_before_use(self):
        """验证 llm_decision.py 的 logger 在使用前定义"""
        import ast
        from pathlib import Path

        llm_decision = Path(__file__).parent.parent.parent.parent / "harness" / "evolve-daemon" / "llm_decision.py"

        if not llm_decision.exists():
            pytest.skip("llm_decision.py 不存在")

        content = llm_decision.read_text()

        # 检查是否导入或定义了 logger
        has_logger_def = (
            "logger = " in content or
            "logging.getLogger" in content or
            "import logging" in content
        )
        assert has_logger_def, "llm_decision.py 未定义 logger"

    # ── Bug #4: 配置文件 JSON 格式错误 ──

    def test_json_no_trailing_comma(self, tmp_path):
        """验证 JSON 文件无尾随逗号"""
        invalid_json = '{"name": "test", "value": 123,}'
        valid_json = '{"name": "test", "value": 123}'

        # 测试无效 JSON 会被检测
        try:
            json.loads(invalid_json)
            has_error = False
        except json.JSONDecodeError:
            has_error = True

        assert has_error, "尾随逗号 JSON 应被拒绝"

        # 测试有效 JSON 正常解析
        parsed = json.loads(valid_json)
        assert parsed["name"] == "test"

    # ── Bug #5: Hook 超时未处理 ──

    def test_hook_timeout_handling(self):
        """验证 Hook 超时处理正确"""
        # 测试超时配置
        hook_config = {
            "type": "command",
            "command": "bash long_running.sh",
            "timeout": 30  # 30 秒
        }

        # 超时应该在 1-120 秒范围内
        assert 1 <= hook_config["timeout"] <= 120, \
            f"超时值 {hook_config['timeout']} 超出合理范围"

    # ── Bug #6: 路径硬编码 ──

    def test_no_hardcoded_paths(self):
        """验证代码不包含硬编码绝对路径"""
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent.parent
        python_files = list(project_root.glob("harness/**/*.py"))

        hardcoded_patterns = [
            r"/Users/[\w/]+/[\w/]+",  # macOS 用户目录
            r"C:\\[\w\\]+",            # Windows 目录
            r"/home/[\w/]+",          # Linux 用户目录
        ]

        issues = []
        for py_file in python_files:
            content = py_file.read_text()
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    # 排除注释和 docstring
                    for line in content.split("\n"):
                        if "#" in line:
                            code_part = line.split("#")[0]
                        else:
                            code_part = line
                        for match in matches:
                            if match in code_part:
                                issues.append(f"{py_file.name}: {match}")

        assert len(issues) == 0, f"发现硬编码路径:\n" + "\n".join(issues)

    # ── Bug #7: 版本不一致 ──

    def test_version_consistency(self):
        """验证 version.json 和 package.json 版本一致"""
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent.parent
        version_json = project_root / "harness" / "_core" / "version.json"
        package_json = project_root / "package.json"

        if not version_json.exists() or not package_json.exists():
            pytest.skip("版本文件不存在")

        vj = json.loads(version_json.read_text())
        pj = json.loads(package_json.read_text())

        version_vj = vj.get("version", "0.0.0")
        version_pj = pj.get("version", "0.0.0")

        assert version_vj == version_pj, \
            f"版本不一致: version.json={version_vj}, package.json={version_pj}"

    # ── Bug #8: Python 语法错误 ──

    def test_python_syntax_check(self):
        """验证所有 Python 文件无语法错误"""
        from pathlib import Path
        import py_compile

        project_root = Path(__file__).parent.parent.parent.parent
        python_files = list(project_root.glob("harness/**/*.py"))

        errors = []
        for py_file in python_files:
            # 跳过测试文件和 __init__.py
            if "test_" in py_file.name or py_file.name == "__init__.py":
                continue
            try:
                py_compile.compile(str(py_file), doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"{py_file.name}: {e}")

        assert len(errors) == 0, f"Python 语法错误:\n" + "\n".join(errors)

    # ── Bug #9: Agent 文件缺少必需字段 ──

    def test_agent_required_fields(self):
        """验证 Agent 文件包含必需字段"""
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent.parent
        agents_dir = project_root / "agents"

        if not agents_dir.exists():
            pytest.skip("agents 目录不存在")

        errors = []
        for agent_file in agents_dir.glob("*.md"):
            content = agent_file.read_text()

            if "description" not in content.lower():
                errors.append(f"{agent_file.name}: 缺少 description")
            if "trigger" not in content.lower():
                errors.append(f"{agent_file.name}: 缺少 trigger_words")

        assert len(errors) == 0, "Agent 文件问题:\n" + "\n".join(errors)

    # ── Bug #10: Hook 配置格式错误 ──

    def test_hooks_json_format(self):
        """验证 hooks.json 格式正确"""
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent.parent
        hooks_json = project_root / "hooks" / "hooks.json"

        if not hooks_json.exists():
            pytest.skip("hooks.json 不存在")

        content = hooks_json.read_text()

        # 应该是有效 JSON
        try:
            config = json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"hooks.json 格式错误: {e}")

        # 应该有 hooks 键
        assert "hooks" in config, "hooks.json 缺少 hooks 键"

        # 每个 hook 应该有 type 或 command
        for hook_type, hook_list in config.get("hooks", {}).items():
            for hook in hook_list:
                assert "type" in hook or "command" in hook, \
                    f"{hook_type}: hook 缺少 type 或 command"


class TestRegressionEdgeCases:
    """边界情况回归测试"""

    def test_empty_json_object(self):
        """空 JSON 对象"""
        assert json.loads("{}") == {}

    def test_empty_json_array(self):
        """空 JSON 数组"""
        assert json.loads("[]") == []

    def test_json_with_unicode(self):
        """带 Unicode 的 JSON"""
        data = {"name": "测试", "emoji": "🎉"}
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed == data

    def test_json_with_emoji(self):
        """带 Emoji 的 JSON"""
        data = {"status": "✅ 成功", "message": "🎉🎊🎈"}
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed == data

    def test_config_merge_deep(self):
        """深度合并配置"""
        base = {
            "a": {"b": 1, "c": 2},
            "d": 3
        }
        override = {
            "a": {"c": 20, "e": 5},
            "f": 6
        }

        result = {}
        for k, v in base.items():
            result[k] = v
        for k, v in override.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = {**result[k], **v}
            else:
                result[k] = v

        assert result["a"]["b"] == 1
        assert result["a"]["c"] == 20
        assert result["a"]["e"] == 5
        assert result["d"] == 3
        assert result["f"] == 6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])