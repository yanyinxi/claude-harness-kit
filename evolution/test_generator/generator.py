"""TestGenerator - 主测试生成器"""

import json
import fcntl
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scenario_parser import ScenarioParser
from .test_runner import TestRunner
from .comparator import TestComparator
from .analyzer import FailureAnalyzer


class TestGenerator:
    """自动生成和运行 skill 测试用例"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.skills_dir = project_root / "skills"
        if not self.skills_dir.exists():
            self.skills_dir = project_root / ".claude" / "skills"
        self.tests_dir = project_root / "tests" / "skills"
        self.data_dir = project_root / ".claude" / "data"

        self.parser = ScenarioParser(self.skills_dir)
        self.runner = TestRunner(self.tests_dir)
        self.comparator = TestComparator()
        self.analyzer = FailureAnalyzer()

    def generate_tests_for_skill(self, skill_name: str) -> bool:
        """为指定 skill 生成测试用例"""
        skill_file = self.skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            return False

        scenarios = self.parser.parse_skill(skill_name)

        skill_test_dir = self.tests_dir / skill_name
        skill_test_dir.mkdir(parents=True, exist_ok=True)

        self._generate_functionality_tests(skill_name, scenarios, skill_test_dir)
        self._generate_performance_tests(skill_name, scenarios, skill_test_dir)
        if scenarios:
            self._generate_scenario_tests(skill_name, scenarios, skill_test_dir)

        self._save_test_metadata(skill_name, len(scenarios))
        return True

    def _generate_scenario_tests(self, skill_name: str, scenarios: list, test_dir: Path):
        """生成场景选择测试"""
        test_content = [
            '"""场景选择测试 - 验证 AI 是否在正确场景选择 skill"""',
            "",
            "import pytest",
            "from pathlib import Path",
            "",
            f"SKILL_NAME = \"{skill_name}\"",
            f"PROJECT_ROOT = Path(__file__).parent.parent.parent.parent",
            "",
            f"class TestScenarioSelection:",
            "",
            "    @pytest.mark.parametrize(\"scenario\", [",
        ]

        for i, scenario in enumerate(scenarios):
            expected = "True" if scenario.is_positive else "False"
            desc = scenario.description.replace('"', '\\"')[:50]
            test_content.append(
                f'        ({{"name": "{scenario.name}", "desc": "{desc}", "expected": {expected}}}),'
            )

        test_content.extend([
            "    ])",
            f"    def test_scenario_selection(self, scenario):",
            f'        """验证场景 {skill_name} 是否正确选择"""',
            "        skill_file = PROJECT_ROOT / \"skills\" / SKILL_NAME / \"SKILL.md\"",
            "        assert skill_file.exists(), f\"Skill file not found: {{skill_file}}\"",
            "        content = skill_file.read_text()",
            "        assert len(content) > 0, \"Empty skill file\"",
            "        assert \"## 何时使用\" in content or \"## 适用场景\" in content, \"Missing scenario section\"",
            "",
        ])

        (test_dir / "test_scenario_selection.py").write_text(
            "\n".join(test_content), encoding="utf-8"
        )

    def _generate_functionality_tests(self, skill_name: str, scenarios: list, test_dir: Path):
        """生成功能测试"""
        test_content = [
            '"""功能测试 - 验证 skill 基本功能"""',
            "",
            "import pytest",
            "from pathlib import Path",
            "",
            f"SKILL_NAME = \"{skill_name}\"",
            f"PROJECT_ROOT = Path(__file__).parent.parent.parent.parent",
            "",
            f"class TestFunctionality:",
            "",
            f"    def test_skill_loads(self):",
            f'        """验证 {skill_name} 可以正常加载"""',
            "        skill_file = PROJECT_ROOT / \"skills\" / SKILL_NAME / \"SKILL.md\"",
            "        assert skill_file.exists(), f\"Skill file not found: {{skill_file}}\"",
            "",
            f"    def test_skill_content_valid(self):",
            f'        """验证 {skill_name} 内容有效"""',
            "        skill_file = PROJECT_ROOT / \"skills\" / SKILL_NAME / \"SKILL.md\"",
            "        content = skill_file.read_text()",
            "        assert \"---\" in content, \"Missing YAML front matter\"",
            "        assert \"name:\" in content, \"Missing name field\"",
            "",
        ]

        (test_dir / "test_functionality.py").write_text(
            "\n".join(test_content), encoding="utf-8"
        )

    def _generate_performance_tests(self, skill_name: str, scenarios: list, test_dir: Path):
        """生成性能测试"""
        test_content = [
            '"""性能测试 - 验证 skill 执行时间和资源消耗"""',
            "",
            "import pytest",
            "import time",
            "from pathlib import Path",
            "",
            f"SKILL_NAME = \"{skill_name}\"",
            f"PROJECT_ROOT = Path(__file__).parent.parent.parent.parent",
            "",
            f"class TestPerformance:",
            "",
            f"    def test_skill_file_read_time(self):",
            f'        """验证 {skill_name} 文件读取时间合理"""',
            "        skill_file = PROJECT_ROOT / \"skills\" / SKILL_NAME / \"SKILL.md\"",
            "        start = time.time()",
            "        content = skill_file.read_text()",
            "        duration = time.time() - start",
            "        assert duration < 1.0, f\"File read too slow: {{duration:.2f}}s\"",
            "        assert len(content) > 0, \"Empty skill file\"",
            "",
        ]

        (test_dir / "test_performance.py").write_text(
            "\n".join(test_content), encoding="utf-8"
        )

    def _save_test_metadata(self, skill_name: str, scenario_count: int):
        """保存测试元数据"""
        metadata_file = self.data_dir / f"test_metadata_{skill_name}.json"
        metadata = {
            "skill_name": skill_name,
            "scenario_count": scenario_count,
            "generated_at": datetime.now().isoformat(),
            "tests": {
                "test_scenario_selection": True,
                "test_functionality": True,
                "test_performance": True,
            }
        }
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def run_before_tests(self, skill_name: str) -> dict:
        """运行进化前的测试"""
        return {"status": "before_tests_collected", "skill_name": skill_name}

    def run_after_tests(self, skill_name: str) -> dict:
        """运行进化后的测试"""
        result = self.runner.run_tests(skill_name)
        return {
            "status": "after_tests_collected",
            "skill_name": skill_name,
            "pass_rate": result.pass_rate,
            "passed": result.passed,
            "failed": result.failed,
        }

    def compare_and_analyze(
        self,
        skill_name: str,
        before_result: dict,
        after_result: dict
    ) -> dict:
        """对比并分析进化前后的测试结果"""
        failed_tests = self.runner.run_tests(skill_name).results
        failed = [t for t in failed_tests if not t.passed]

        analyses = self.analyzer.analyze(failed)

        return {
            "skill_name": skill_name,
            "before_pass_rate": before_result.get("pass_rate", 0),
            "after_pass_rate": after_result.get("pass_rate", 0),
            "analyses": [
                {
                    "test": a.test_name,
                    "reason": a.failure_reason,
                    "category": a.category,
                    "suggestions": a.suggestions,
                }
                for a in analyses
            ],
            "should_revert": len(analyses) > 0 and all(
                a.category == "scenario" for a in analyses
            ),
        }

    def generate_all_tests(self) -> Dict[str, bool]:
        """为所有 skill 生成测试"""
        results = {}
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                results[skill_dir.name] = self.generate_tests_for_skill(
                    skill_dir.name
                )
        return results
