"""功能测试 - 验证 skill 基本功能"""

import pytest
from pathlib import Path

SKILL_NAME = "workflow-pause"
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class TestFunctionality:

    def test_skill_loads(self):
        """验证 workflow-pause 可以正常加载"""
        skill_file = PROJECT_ROOT / "skills" / SKILL_NAME / "SKILL.md"
        assert skill_file.exists(), f"Skill file not found: {{skill_file}}"

    def test_skill_content_valid(self):
        """验证 workflow-pause 内容有效"""
        skill_file = PROJECT_ROOT / "skills" / SKILL_NAME / "SKILL.md"
        content = skill_file.read_text()
        assert "---" in content, "Missing YAML front matter"
        assert "name:" in content, "Missing name field"
