"""SKILL.md 场景解析器 - 从 SKILL.md 中提取适用场景"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Scenario:
    """单个适用场景"""
    name: str
    description: str
    is_positive: bool  # True=适用, False=不适用
    input_example: Optional[str] = None
    output_expected: Optional[str] = None


class ScenarioParser:
    """解析 SKILL.md 中的适用场景"""

    SCENARIO_MARKERS = [
        r"## 适用场景",
        r"## 何时使用",
        r"## 使用场景",
        r"## When to Use",
    ]

    POSITIVE_MARKERS = ["✅", "适用", "用于", "when"]
    NEGATIVE_MARKERS = ["❌", "不适用", "不用于", "not for", "don't"]

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir

    def parse_skill(self, skill_name: str) -> List[Scenario]:
        """解析指定 skill 的场景"""
        skill_file = self.skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            return []

        content = skill_file.read_text(encoding="utf-8")
        return self.parse_content(content)

    def parse_content(self, content: str) -> List[Scenario]:
        """从 SKILL.md 内容中提取场景"""
        scenarios = []
        lines = content.split("\n")

        in_scenario_section = False
        collecting_bullets = False
        bullet_lines = []
        parsed_at_section = False

        for line in lines:
            stripped = line.strip()

            if self._is_scenario_header(stripped):
                in_scenario_section = True
                collecting_bullets = False
                continue

            if in_scenario_section and self._is_section_header(stripped):
                if bullet_lines and not parsed_at_section:
                    scenarios.extend(self._parse_bullet_scenarios(bullet_lines))
                    parsed_at_section = True
                break

            if in_scenario_section:
                if stripped.startswith("-") or stripped.startswith("*"):
                    collecting_bullets = True
                    bullet_lines.append(stripped)
                elif stripped.startswith("#") or not stripped:
                    pass
                elif collecting_bullets:
                    pass

        if bullet_lines and not parsed_at_section:
            scenarios.extend(self._parse_bullet_scenarios(bullet_lines))

        return scenarios

    def _parse_bullet_scenarios(self, bullet_lines: List[str]) -> List[Scenario]:
        """从 bullet 列表中解析场景"""
        scenarios = []
        for line in bullet_lines:
            line = line.lstrip("-*•").strip()
            if not line or not line.startswith("**"):
                continue

            parts = line.split("**：", 1) if "**：" in line else line.split(":", 1)
            name_part = parts[0].strip().lstrip("**").rstrip("**")

            is_positive = not any(neg in name_part for neg in self.NEGATIVE_MARKERS)

            desc = parts[1].strip() if len(parts) > 1 else name_part

            scenarios.append(Scenario(
                name=name_part,
                description=desc,
                is_positive=is_positive,
            ))
        return scenarios

    def _is_scenario_header(self, line: str) -> bool:
        return any(re.match(marker, line, re.IGNORECASE) for marker in self.SCENARIO_MARKERS)

    def _is_section_header(self, line: str) -> bool:
        return line.startswith("## ") and not any(
            marker in line.lower() for marker in self.SCENARIO_MARKERS
        )

    def _finalize_scenario(self, name: str, lines: List[str]) -> Scenario:
        is_positive = not any(neg in name for neg in self.NEGATIVE_MARKERS)

        description = " ".join(
            line.strip().lstrip("-*•").strip()
            for line in lines
            if line.strip() and not line.strip().startswith("|")
        ).strip()

        return Scenario(
            name=name.strip(),
            description=description,
            is_positive=is_positive,
            input_example=self._extract_example(lines, "input"),
            output_expected=self._extract_example(lines, "output"),
        )

    def _extract_example(self, lines: List[str], example_type: str) -> Optional[str]:
        for line in lines:
            if example_type in line.lower():
                match = re.search(r"[`'\"]?([^{}`'\"]+)[`'\"]?", line)
                if match:
                    return match.group(1).strip()
        return None

    def get_all_scenarios(self) -> Dict[str, List[Scenario]]:
        """获取所有 skill 的场景"""
        result = {}
        if not self.skills_dir.exists():
            return result

        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                scenarios = self.parse_skill(skill_dir.name)
                if scenarios:
                    result[skill_dir.name] = scenarios

        return result

    def scenarios_to_test_prompts(self, scenarios: List[Scenario]) -> List[Dict[str, str]]:
        """将场景转换为测试提示"""
        prompts = []
        for scenario in scenarios:
            prompts.append({
                "name": scenario.name,
                "description": scenario.description,
                "expected_behavior": "should select" if scenario.is_positive else "should NOT select",
                "input_hint": scenario.input_example or scenario.description,
            })
        return prompts
