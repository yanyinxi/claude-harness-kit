"""失败分析器 - 分析测试失败原因并给出改进建议"""

from typing import List, Dict, Any
from dataclasses import dataclass
from .test_runner import TestResult


@dataclass
class FailureAnalysis:
    """失败分析结果"""
    test_name: str
    failure_reason: str
    category: str
    suggestions: List[str]


class FailureAnalyzer:
    """分析测试失败原因"""

    CATEGORIES = {
        "scenario": ["场景", "适用", "选择", "should select"],
        "functionality": ["功能", "执行", "结果", "assert"],
        "performance": ["超时", "时间", "性能", "duration"],
        "dependency": ["依赖", "缺失", "import", "not found"],
    }

    def analyze(self, failed_tests: List[TestResult]) -> List[FailureAnalysis]:
        """分析失败测试"""
        analyses = []
        for test in failed_tests:
            if not test.passed:
                analyses.append(self._analyze_single(test))
        return analyses

    def _analyze_single(self, test: TestResult) -> FailureAnalysis:
        category = self._categorize(test)
        reason = self._extract_reason(test)
        suggestions = self._generate_suggestions(test, category)

        return FailureAnalysis(
            test_name=test.test_name,
            failure_reason=reason,
            category=category,
            suggestions=suggestions
        )

    def _categorize(self, test: TestResult) -> str:
        for category, keywords in self.CATEGORIES.items():
            if any(kw in test.test_name.lower() or kw in (test.error_message or "") for kw in keywords):
                return category
        return "unknown"

    def _extract_reason(self, test: TestResult) -> str:
        msg = test.error_message or ""
        if "assert" in msg.lower():
            return "预期结果与实际不符"
        if "timeout" in msg.lower():
            return "执行超时"
        if "import" in msg.lower() or "not found" in msg.lower():
            return "依赖缺失或导入错误"
        if "scenario" in test.test_name.lower():
            return "场景匹配错误"
        if "functionality" in test.test_name.lower():
            return "功能执行失败"
        return msg[:100] if msg else "未知错误"

    def _generate_suggestions(self, test: TestResult, category: str) -> List[str]:
        suggestions = []
        if category == "scenario":
            suggestions.append("检查场景描述是否准确")
            suggestions.append("验证适用条件是否完整")
        elif category == "functionality":
            suggestions.append("检查 skill 执行逻辑")
            suggestions.append("验证工具调用是否正确")
        elif category == "performance":
            suggestions.append("优化执行步骤")
            suggestions.append("减少不必要的等待")
        elif category == "dependency":
            suggestions.append("检查依赖是否正确安装")
            suggestions.append("验证路径配置是否正确")
        else:
            suggestions.append("检查 skill 实现是否符合预期")

        return suggestions

    def summarize(self, analyses: List[FailureAnalysis]) -> str:
        """生成分析摘要"""
        if not analyses:
            return "所有测试通过"

        by_category = {}
        for a in analyses:
            if a.category not in by_category:
                by_category[a.category] = []
            by_category[a.category].append(a)

        lines = ["# 测试失败分析\n"]
        for category, items in by_category.items():
            lines.append(f"\n## {category} ({len(items)} 项)")
            for item in items:
                lines.append(f"\n### {item.test_name}")
                lines.append(f"- 原因: {item.failure_reason}")
                lines.append("- 建议:")
                for s in item.suggestions:
                    lines.append(f"  - {s}")

        return "\n".join(lines)
