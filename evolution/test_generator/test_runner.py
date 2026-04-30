"""pytest 测试运行器 - 自动执行测试并收集结果"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TestResult:
    """单次测试结果"""
    passed: bool
    test_name: str
    duration_ms: float
    error_message: Optional[str] = None
    skill_name: Optional[str] = None


@dataclass
class TestRunResult:
    """测试运行结果"""
    total: int
    passed: int
    failed: int
    duration_ms: float
    results: List[TestResult]
    pass_rate: float


class TestRunner:
    """运行 pytest 测试并收集结果"""

    def __init__(self, tests_dir: Path):
        self.tests_dir = tests_dir

    def run_tests(self, skill_name: str, test_type: str = "all") -> TestRunResult:
        """运行指定 skill 的测试"""
        test_file = self.tests_dir / "skills" / skill_name
        if not test_file.exists():
            return TestRunResult(0, 0, 0, 0, [], 0.0)

        test_paths = []
        if test_type == "all" or test_type == "functionality":
            fp = test_file / "test_functionality.py"
            if fp.exists():
                test_paths.append(str(fp))
        if test_type == "all" or test_type == "scenario":
            fp = test_file / "test_scenario_selection.py"
            if fp.exists():
                test_paths.append(str(fp))
        if test_type == "all" or test_type == "performance":
            fp = test_file / "test_performance.py"
            if fp.exists():
                test_paths.append(str(fp))

        if not test_paths:
            return TestRunResult(0, 0, 0, 0, [], 0.0)

        start_time = time.time()
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", "-v", "--tb=short", "--json-report", "--json-report-file=/tmp/pytest_report.json"] + test_paths,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.tests_dir.parent)
            )
        except subprocess.TimeoutExpired:
            return TestRunResult(0, 0, 0, 60000, [], 0.0)
        except Exception as e:
            return TestRunResult(0, 0, 0, 0, [], 0.0, [TestResult(False, "test_runner_error", 0, str(e))])

        duration_ms = (time.time() - start_time) * 1000

        report_file = Path("/tmp/pytest_report.json")
        if report_file.exists():
            return self._parse_json_report(report_file, duration_ms)

        return self._parse_pytest_output(result.stdout + result.stderr, duration_ms)

    def _parse_json_report(self, report_file: Path, duration_ms: float) -> TestRunResult:
        try:
            with open(report_file) as f:
                report = json.load(f)

            results = []
            for test in report.get("tests", []):
                results.append(TestResult(
                    passed=test.get("outcome") == "passed",
                    test_name=test.get("nodeid", ""),
                    duration_ms=test.get("duration", 0) * 1000,
                    error_message=test.get("call", {}).get("longrepr", "")
                ))

            total = len(results)
            passed = sum(1 for r in results if r.passed)
            return TestRunResult(
                total=total,
                passed=passed,
                failed=total - passed,
                duration_ms=duration_ms,
                results=results,
                pass_rate=passed / total if total > 0 else 0.0
            )
        except Exception:
            return TestRunResult(0, 0, 0, duration_ms, [], 0.0)

    def _parse_pytest_output(self, output: str, duration_ms: float) -> TestRunResult:
        results = []
        passed = 0
        failed = 0

        for line in output.split("\n"):
            if "::test_" in line:
                if "PASSED" in line:
                    passed += 1
                    results.append(TestResult(True, line.split("::")[1].split()[0], 0))
                elif "FAILED" in line:
                    failed += 1
                    results.append(TestResult(False, line.split("::")[1].split()[0], 0))

        total = passed + failed
        return TestRunResult(
            total=total,
            passed=passed,
            failed=failed,
            duration_ms=duration_ms,
            results=results,
            pass_rate=passed / total if total > 0 else 0.0
        )

    def run_before_after(self, skill_name: str) -> Dict[str, TestRunResult]:
        """运行进化前后的测试对比"""
        before = self.run_tests(skill_name)
        return {"before": before}

    def get_test_coverage(self, skill_name: str) -> Dict[str, bool]:
        """检查测试覆盖情况"""
        test_file = self.tests_dir / "skills" / skill_name
        return {
            "has_functionality": (test_file / "test_functionality.py").exists(),
            "has_scenario": (test_file / "test_scenario_selection.py").exists(),
            "has_performance": (test_file / "test_performance.py").exists(),
        }
