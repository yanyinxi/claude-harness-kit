"""测试对比器 - 比较进化前后的测试结果"""

from typing import Dict, List, Any
from dataclasses import dataclass
from .test_runner import TestRunResult


@dataclass
class ComparisonResult:
    """对比结果"""
    skill_name: str
    before_pass_rate: float
    after_pass_rate: float
    pass_rate_change: float
    duration_change_ms: float
    improved: bool
    regressions: List[str]
    improvements: List[str]


class TestComparator:
    """比较进化前后的测试结果"""

    REGRESSION_THRESHOLD = -0.1

    def compare(
        self,
        skill_name: str,
        before: TestRunResult,
        after: TestRunResult
    ) -> ComparisonResult:
        """对比两次测试结果"""
        pass_rate_change = after.pass_rate - before.pass_rate
        duration_change = after.duration_ms - before.duration_ms

        regressions = []
        improvements = []

        if pass_rate_change < self.REGRESSION_THRESHOLD:
            regressions.append(f"通过率下降 {pass_rate_change:.1%}")

        if duration_change > 1000:
            regressions.append(f"执行时间增加 {duration_change:.0f}ms")

        if pass_rate_change > 0.1:
            improvements.append(f"通过率提升 {pass_rate_change:.1%}")

        if duration_change < -500:
            improvements.append(f"执行时间减少 {abs(duration_change):.0f}ms")

        return ComparisonResult(
            skill_name=skill_name,
            before_pass_rate=before.pass_rate,
            after_pass_rate=after.pass_rate,
            pass_rate_change=pass_rate_change,
            duration_change_ms=duration_change,
            improved=pass_rate_change > 0 and len(regressions) == 0,
            regressions=regressions,
            improvements=improvements
        )

    def should_auto_accept(self, result: ComparisonResult) -> bool:
        """判断是否应该自动接受进化"""
        return (
            result.after_pass_rate >= 0.9 and
            result.improved and
            len(result.regressions) == 0
        )

    def should_revert(self, result: ComparisonResult) -> bool:
        """判断是否应该回滚"""
        return (
            result.after_pass_rate < result.before_pass_rate and
            len(result.regressions) > 0
        )

    def generate_report(self, comparisons: List[ComparisonResult]) -> str:
        """生成对比报告"""
        lines = ["# 测试对比报告\n"]
        for c in comparisons:
            status = "✅ 改进" if c.improved else "❌ 退化"
            lines.append(f"\n## {c.skill_name} {status}")
            lines.append(f"- 进化前通过率: {c.before_pass_rate:.1%}")
            lines.append(f"- 进化后通过率: {c.after_pass_rate:.1%}")
            lines.append(f"- 通过率变化: {c.pass_rate_change:+.1%}")
            lines.append(f"- 执行时间变化: {c.duration_change_ms:+.0f}ms")
            if c.improvements:
                lines.append(f"- 改进: {', '.join(c.improvements)}")
            if c.regressions:
                lines.append(f"- 退化: {', '.join(c.regressions)}")
        return "\n".join(lines)
