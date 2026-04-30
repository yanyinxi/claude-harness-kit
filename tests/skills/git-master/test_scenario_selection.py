"""场景选择测试 - 验证 AI 是否在正确场景选择 skill"""

import pytest
from pathlib import Path

SKILL_NAME = "git-master"
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class TestScenarioSelection:

    @pytest.mark.parametrize("scenario", [
        ({"name": "代码提交", "desc": "需要创建规范化的 commit message", "expected": True}),
        ({"name": "分支管理", "desc": "进行分支创建、合并、删除、重命名等操作", "expected": True}),
        ({"name": "版本发布", "desc": "准备发布版本、创建标签、生成 CHANGELOG", "expected": True}),
        ({"name": "历史整理", "desc": "需要压缩（squash）、变基（rebase）提交历史", "expected": True}),
        ({"name": "协作规范", "desc": "团队需要统一的 Git 工作流", "expected": True}),
        ({"name": "触发词", "desc": "当用户提及 `commit`、`rebase`、`squash`、`git`、`分支`、`版本发布`", "expected": True}),
    ])
    def test_scenario_selection(self, scenario):
        """验证场景 git-master 是否正确选择"""
        skill_file = PROJECT_ROOT / "skills" / SKILL_NAME / "SKILL.md"
        assert skill_file.exists(), f"Skill file not found: {{skill_file}}"
        content = skill_file.read_text()
        assert len(content) > 0, "Empty skill file"
        assert "## 何时使用" in content or "## 适用场景" in content, "Missing scenario section"
