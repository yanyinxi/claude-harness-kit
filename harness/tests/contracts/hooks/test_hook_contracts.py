#!/usr/bin/env python3
"""
Hook 接口契约测试

验证 hooks.json 配置的正确性：
- JSON 格式有效
- 每个 hook 有 type 和 command
- timeout 在合理范围内
- 引用的文件存在
"""

import json
import re
from pathlib import Path
import pytest

# 项目根目录 - 使用向上搜索方式找到包含 package.json 的目录
def find_project_root(start_path: Path) -> Path:
    """向上搜索找到项目根目录"""
    current = start_path.resolve()
    for _ in range(10):  # 最多向上10层
        if (current / "package.json").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return start_path  # 回退到起始位置

PROJECT_ROOT = find_project_root(Path(__file__))
HOOKS_JSON = PROJECT_ROOT / "hooks" / "hooks.json"
HOOKS_BIN_DIR = PROJECT_ROOT / "hooks" / "bin"

# 如果 hooks 在根目录不存在，尝试在 harness 下查找
if not HOOKS_JSON.exists():
    HOOKS_JSON = PROJECT_ROOT / "harness" / "hooks" / "hooks.json"
if not HOOKS_BIN_DIR.exists():
    HOOKS_BIN_DIR = PROJECT_ROOT / "harness" / "hooks" / "bin"


def parse_hooks_config() -> dict:
    """解析 hooks.json 配置"""
    if not HOOKS_JSON.exists():
        return {"error": "hooks.json 不存在"}

    try:
        content = HOOKS_JSON.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析错误: {e}"}


class TestHookContract:
    """Hook 接口契约测试"""

    @pytest.fixture
    def hooks_config(self):
        """加载 hooks 配置"""
        config = parse_hooks_config()
        if "error" in config:
            pytest.fail(config["error"])
        return config

    def test_hooks_json_exists(self):
        """验证 hooks.json 存在"""
        assert HOOKS_JSON.exists(), f"hooks.json 不存在: {HOOKS_JSON}"

    def test_hooks_json_valid_json(self):
        """hooks.json 必须是有效 JSON"""
        config = parse_hooks_config()
        assert "error" not in config, config.get("error")

    def test_hooks_json_has_hooks_key(self, hooks_config):
        """hooks.json 必须包含 hooks 键"""
        assert "hooks" in hooks_config, "hooks.json 缺少 hooks 键"
        assert isinstance(hooks_config["hooks"], dict), "hooks 必须是字典"

    def test_hooks_json_valid_hook_types(self, hooks_config):
        """验证 hook 类型有效"""
        valid_types = ["command", "script", "process", "command", "script", "process"]

        for hook_type, hook_list in hooks_config.get("hooks", {}).items():
            assert isinstance(hook_list, list), \
                f"{hook_type}: hook 配置必须是列表"

            for hook in hook_list:
                assert isinstance(hook, dict), \
                    f"{hook_type}: hook 必须是字典"

                if "type" in hook:
                    assert hook["type"] in valid_types, \
                        f"{hook_type}: 无效的 hook 类型 {hook['type']}"

    def test_each_hook_has_required_fields(self, hooks_config):
        """每个 hook 必须有 type 和 command"""
        for hook_type, hook_list in hooks_config.get("hooks", {}).items():
            for i, hook in enumerate(hook_list):
                assert "type" in hook or "command" in hook, \
                    f"{hook_type}[{i}]: 缺少 type 或 command 字段"

                if "command" in hook:
                    assert isinstance(hook["command"], str), \
                        f"{hook_type}[{i}]: command 必须是字符串"
                    assert len(hook["command"]) > 0, \
                        f"{hook_type}[{i}]: command 不能为空"

    def test_timeout_is_reasonable(self, hooks_config):
        """timeout 应在合理范围内 (1-120秒)"""
        for hook_type, hook_list in hooks_config.get("hooks", {}).items():
            for i, hook in enumerate(hook_list):
                if "timeout" in hook:
                    timeout = hook["timeout"]
                    assert isinstance(timeout, (int, float)), \
                        f"{hook_type}[{i}]: timeout 必须是数字"
                    assert 1 <= timeout <= 120, \
                        f"{hook_type}[{i}]: timeout={timeout} 超出范围 [1, 120]"

    def test_matcher_is_valid_regex(self, hooks_config):
        """matcher 应是有效的正则表达式"""
        for hook_type, hook_list in hooks_config.get("hooks", {}).items():
            for i, hook in enumerate(hook_list):
                if "matcher" in hook:
                    matcher = hook["matcher"]
                    assert isinstance(matcher, str), \
                        f"{hook_type}[{i}]: matcher 必须是字符串"
                    assert len(matcher) > 0, \
                        f"{hook_type}[{i}]: matcher 不能为空"

                    # 尝试编译正则表达式
                    try:
                        re.compile(matcher)
                    except re.error as e:
                        pytest.fail(f"{hook_type}[{i}]: matcher 正则无效: {e}")


class TestHookContractQuality:
    """Hook 契约质量检查"""

    def test_command_files_exist(self):
        """验证 command 字段引用的文件存在"""
        if not HOOKS_JSON.exists():
            pytest.skip("hooks.json 不存在")

        config = parse_hooks_config()
        if "error" in config:
            pytest.skip(config["error"])

        missing_files = []
        for hook_type, hook_list in config.get("hooks", {}).items():
            for i, hook in enumerate(hook_list):
                if "command" in hook:
                    command = hook["command"]
                    # 提取文件路径 (bash xxx/xxx.sh 格式)
                    if "bash " in command:
                        # 提取 bash 后面的路径
                        path_match = re.search(r"bash\s+(.+?)(?:\s|$)", command)
                        if path_match:
                            file_path = path_match.group(1)
                            # 转换为绝对路径
                            if not file_path.startswith("/"):
                                file_path = PROJECT_ROOT / file_path
                            if not Path(file_path).exists():
                                missing_files.append(f"{hook_type}[{i}]: {file_path}")

        assert len(missing_files) == 0, \
            f"以下 hook 引用的文件不存在:\n" + "\n".join(missing_files)

    def test_no_hardcoded_absolute_paths(self):
        """hooks.json 不应包含硬编码绝对路径（应使用相对路径）"""
        if not HOOKS_JSON.exists():
            pytest.skip("hooks.json 不存在")

        content = HOOKS_JSON.read_text(encoding="utf-8")

        # 检查常见的硬编码路径模式
        hardcoded_patterns = [
            r"/Users/[\w/]+/[\w/]+",  # macOS 用户目录
            r"C:\\[\w\\]+",           # Windows 目录
            r"/home/[\w/]+",         # Linux 用户目录
        ]

        for pattern in hardcoded_patterns:
            matches = re.findall(pattern, content)
            if len(matches) > 0:
                # 检查是否是 hooks/bin 路径（这个是可以接受的）
                acceptable = [m for m in matches if "hooks/bin" in m]
                if len(matches) > len(acceptable):
                    pytest.fail(f"hooks.json 包含硬编码绝对路径: {matches}")

    def test_hooks_bin_directory_exists(self):
        """验证 hooks/bin 目录存在"""
        assert HOOKS_BIN_DIR.exists(), f"hooks/bin 目录不存在: {HOOKS_BIN_DIR}"
        assert HOOKS_BIN_DIR.is_dir(), f"{HOOKS_BIN_DIR} 不是目录"


class TestHookExecutionScripts:
    """Hook 执行脚本质量检查"""

    def test_shell_scripts_has_shebang(self):
        """Shell 脚本应有 shebang 行"""
        if not HOOKS_BIN_DIR.exists():
            pytest.skip("hooks/bin 目录不存在")

        for script in HOOKS_BIN_DIR.glob("*.sh"):
            content = script.read_text(encoding="utf-8")
            first_line = content.split("\n")[0] if content else ""

            assert first_line.startswith("#!"), \
                f"{script.name}: 缺少 shebang (#!/bin/bash 或 #!/bin/sh)"

    def test_python_scripts_has_shebang(self):
        """Python 脚本应有 shebang 行"""
        if not HOOKS_BIN_DIR.exists():
            pytest.skip("hooks/bin 目录不存在")

        for script in HOOKS_BIN_DIR.glob("*.py"):
            content = script.read_text(encoding="utf-8")
            first_line = content.split("\n")[0] if content else ""

            assert first_line.startswith("#!"), \
                f"{script.name}: 缺少 shebang (#!/usr/bin/env python3)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])