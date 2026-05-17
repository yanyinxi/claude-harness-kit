#!/usr/bin/env python3
"""
Skill 接口契约测试

验证所有 Skill 目录满足标准格式：
- 必须包含 SKILL.md
- 必须包含 bin/ 目录
- SKILL.md 必须包含 trigger_words 和执行流程
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
SKILLS_DIR = PROJECT_ROOT / "skills"


def parse_skill_directory(skill_path: Path) -> dict:
    """解析 Skill 目录，提取关键信息"""
    result = {
        "has_skill_md": False,
        "has_bin_dir": False,
        "has_trigger": False,
        "has_execute_flow": False,
        "skill_md_line": None,
        "trigger_content": None,
    }

    if not skill_path.is_dir():
        return result

    # 检查 SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        result["has_skill_md"] = True
        content = skill_md.read_text(encoding="utf-8")
        lines = content.split("\n")

        for i, line in enumerate(lines):
            # 检查 trigger words
            if re.search(r"(trigger|触发词|触发条件)", line, re.IGNORECASE):
                result["has_trigger"] = True
                trigger_match = re.search(r"[:：]\s*(.+)$", line)
                if trigger_match:
                    result["trigger_content"] = trigger_match.group(1)

            # 检查执行流程
            if re.search(r"(执行流程|workflow|执行)", line, re.IGNORECASE):
                result["has_execute_flow"] = True

    # 检查 bin/ 目录
    bin_dir = skill_path / "bin"
    if bin_dir.exists() and bin_dir.is_dir():
        result["has_bin_dir"] = True

    return result


class TestSkillContract:
    """Skill 接口契约测试"""

    @pytest.fixture
    def skill_directories(self):
        """获取所有 Skill 目录"""
        if not SKILLS_DIR.exists():
            return []
        return [p for p in SKILLS_DIR.iterdir() if p.is_dir() and not p.name.startswith('.')]

    def test_skills_directory_exists(self):
        """验证 skills 目录存在"""
        if not SKILLS_DIR.exists():
            pytest.skip(f"skills 目录不存在: {SKILLS_DIR}")
        assert SKILLS_DIR.is_dir(), f"{SKILLS_DIR} 不是目录"

    def test_at_least_one_skill(self, skill_directories):
        """验证至少有 1 个 Skill"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills 目录不存在")
        assert len(skill_directories) >= 1, "没有找到任何 Skill 目录"

    def test_skill_has_skill_md(self):
        """每个 Skill 必须包含 SKILL.md"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills 目录不存在")
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            skill_md = skill_dir / "SKILL.md"
            assert skill_md.exists(), \
                f"{skill_dir.name}: 缺少 SKILL.md 文件"

    def test_skill_md_not_empty(self):
        """SKILL.md 不能为空"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills 目录不存在")
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text(encoding="utf-8")
            assert len(content.strip()) > 0, f"{skill_dir.name}/SKILL.md: 文件内容为空"
            assert len(content) > 100, f"{skill_dir.name}/SKILL.md: 文件内容太少"

    def test_skill_has_trigger_words(self):
        """每个 Skill 必须定义触发词"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills 目录不存在")
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            result = parse_skill_directory(skill_dir)
            assert result["has_trigger"], \
                f"{skill_dir.name}: SKILL.md 缺少触发词定义 (trigger_words/触发条件)"

    def test_skill_has_bin_directory(self):
        """每个 Skill 推荐包含 bin/ 目录"""
        if not SKILLS_DIR.exists():
            pytest.skip("skills 目录不存在")
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            result = parse_skill_directory(skill_dir)
            if not result["has_bin_dir"]:
                import warnings
                warnings.warn(f"{skill_dir.name}: 建议包含 bin/ 目录")


class TestSkillContractQuality:
    """Skill 契约质量检查"""

    def test_skill_naming_convention(self):
        """Skill 目录命名应符合规范（小写 + 连字符）"""
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue

            name = skill_dir.name
            assert name.islower() or "-" in name or "_" in name, \
                f"{skill_dir.name}: Skill 名称应使用小写 + 连字符命名"

    def test_skill_md_has_description(self):
        """SKILL.md 应包含描述"""
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            content = skill_md.read_text(encoding="utf-8")
            # 应该包含 description 或 描述
            has_description = re.search(r"(description|描述)[:：]", content, re.IGNORECASE)
            assert has_description, \
                f"{skill_dir.name}/SKILL.md: 建议包含 description 字段"

    def test_all_skills_parseable(self):
        """验证所有 Skill 可解析"""
        for skill_dir in SKILLS_DIR.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue

            result = parse_skill_directory(skill_dir)
            assert result["has_skill_md"], \
                f"{skill_dir.name}: 无法解析为有效 Skill (缺少 SKILL.md)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])