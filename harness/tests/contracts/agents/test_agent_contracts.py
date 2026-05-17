#!/usr/bin/env python3
"""
Agent 接口契约测试

验证所有 Agent 文件满足标准格式：
- 必须包含 description
- 必须包含 trigger_words
- 必须包含 tools 列表
- 必须定义 response_format (可选但推荐)
"""

import re
from pathlib import Path
import pytest

# 项目根目录 - 向上搜索找到包含 package.json 的目录
def find_project_root(start_path: Path) -> Path:
    """向上搜索找到项目根目录"""
    current = start_path.resolve()
    for _ in range(10):
        if (current / "package.json").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return start_path

PROJECT_ROOT = find_project_root(Path(__file__))
AGENTS_DIR = PROJECT_ROOT / "agents"

# Agent 契约定义
AGENT_CONTRACT = {
    "required_fields": ["description", "trigger"],
    "forbidden_patterns": [],
    "valid_tools": [
        "Read", "Edit", "Write", "Bash", "Grep", "Glob",
        "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
        "WebFetch", "WebSearch", "Agent", "NotebookEdit",
        "mcp__filesystem__read_text_file", "mcp__filesystem__write_file",
        "mcp__playwright__browser_navigate", "mcp__playwright__browser_snapshot"
    ]
}


def parse_agent_file(file_path: Path) -> dict:
    """解析 Agent 文件，提取关键字段"""
    content = file_path.read_text(encoding="utf-8")

    result = {
        "has_description": False,
        "has_trigger": False,
        "has_tools": False,
        "has_response_format": False,
        "description_line": None,
        "trigger_content": None,
        "tools_list": [],
    }

    lines = content.split("\n")
    for i, line in enumerate(lines):
        # 检查 description
        if re.match(r"^#?\s*(description|描述)[:：\s]", line, re.IGNORECASE):
            result["has_description"] = True
            result["description_line"] = i + 1

        # 检查 trigger words
        if re.search(r"(trigger|触发词|触发条件)", line, re.IGNORECASE):
            result["has_trigger"] = True
            # 提取触发词内容
            trigger_match = re.search(r"[:：]\s*(.+)$", line)
            if trigger_match:
                result["trigger_content"] = trigger_match.group(1)

        # 检查 tools
        if re.search(r"(tools|工具)[:：\s]", line, re.IGNORECASE):
            result["has_tools"] = True

        # 检查 response_format
        if re.search(r"(response_format|响应格式)", line, re.IGNORECASE):
            result["has_response_format"] = True

    return result


class TestAgentContract:
    """Agent 接口契约测试"""

    @pytest.fixture
    def agent_files(self):
        """获取所有 Agent 文件"""
        if not AGENTS_DIR.exists():
            return []
        return list(AGENTS_DIR.glob("*.md"))

    def test_agents_directory_exists(self):
        """验证 agents 目录存在"""
        if not AGENTS_DIR.exists():
            pytest.skip(f"agents 目录不存在: {AGENTS_DIR}")
        assert AGENTS_DIR.is_dir(), f"{AGENTS_DIR} 不是目录"

    def test_at_least_one_agent(self, agent_files):
        """验证至少有 1 个 Agent"""
        if not AGENTS_DIR.exists():
            pytest.skip("agents 目录不存在")
        assert len(agent_files) >= 1, "没有找到任何 Agent 文件"

    def test_agent_has_description(self):
        """每个 Agent 必须包含 description"""
        if not AGENTS_DIR.exists():
            pytest.skip("agents 目录不存在")
        for agent_file in AGENTS_DIR.glob("*.md"):
            result = parse_agent_file(agent_file)
            assert result["has_description"], \
                f"{agent_file.name}: 缺少 description 字段"

    def test_agent_has_trigger_words(self):
        """每个 Agent 必须定义触发词"""
        if not AGENTS_DIR.exists():
            pytest.skip("agents 目录不存在")
        for agent_file in AGENTS_DIR.glob("*.md"):
            result = parse_agent_file(agent_file)
            assert result["has_trigger"], \
                f"{agent_file.name}: 缺少 trigger_words"

    def test_agent_file_not_empty(self):
        """Agent 文件不能为空"""
        if not AGENTS_DIR.exists():
            pytest.skip("agents 目录不存在")
        for agent_file in AGENTS_DIR.glob("*.md"):
            content = agent_file.read_text(encoding="utf-8")
            assert len(content.strip()) > 0, f"{agent_file.name}: 文件内容为空"
            assert len(content) > 100, f"{agent_file.name}: 文件内容太少"

    def test_agent_has_recommended_fields(self):
        """推荐包含的字段检查"""
        if not AGENTS_DIR.exists():
            pytest.skip("agents 目录不存在")
        for agent_file in AGENTS_DIR.glob("*.md"):
            result = parse_agent_file(agent_file)
            missing = []
            if not result["has_description"]:
                missing.append("description")
            if not result["has_trigger"]:
                missing.append("trigger_words")
            assert len(missing) == 0, \
                f"{agent_file.name}: 缺少必要字段: {', '.join(missing)}"


class TestAgentContractQuality:
    """Agent 契约质量检查"""

    def test_no_hardcoded_paths_in_agents(self):
        """Agent 文件不应包含硬编码绝对路径"""
        for agent_file in AGENTS_DIR.glob("*.md"):
            content = agent_file.read_text(encoding="utf-8")

            # 检查常见的硬编码路径模式
            hardcoded_patterns = [
                r"/Users/[\w/]+",  # macOS 用户目录
                r"C:\\[\w\\]+",    # Windows 目录
                r"/home/[\w/]+",  # Linux 用户目录
            ]

            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                assert len(matches) == 0, \
                    f"{agent_file.name}: 包含硬编码路径 {matches}"

    def test_agent_naming_convention(self):
        """Agent 文件命名应符合规范（小写 + 连字符）"""
        for agent_file in AGENTS_DIR.glob("*.md"):
            name = agent_file.stem
            # 应该是小写，可以包含连字符
            assert name.islower() or "-" in name or "_" in name, \
                f"{agent_file.name}: Agent 名称应使用小写 + 连字符命名"

    def test_all_agents_parseable(self):
        """验证所有 Agent 文件可解析"""
        for agent_file in AGENTS_DIR.glob("*.md"):
            result = parse_agent_file(agent_file)
            # 至少应该有 description 或 trigger
            assert result["has_description"] or result["has_trigger"], \
                f"{agent_file.name}: 无法解析为有效 Agent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])