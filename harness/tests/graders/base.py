#!/usr/bin/env python3
"""
LLM Grader 基类

定义评分器接口和通用评估逻辑
用于 LLM-as-Judge 评估
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import os

# 可选导入 anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class GradingResult:
    """评分结果"""
    passed: bool
    score: float  # 0-1
    reason: str
    details: Dict[str, Any]


class BaseGrader(ABC):
    """评分器基类"""

    def __init__(self, model: str = None):
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-opus-4-5")
        self.client = None
        if HAS_ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)

    @abstractmethod
    def grade(self, input_data: Dict, output: str, expected: Optional[Dict] = None) -> GradingResult:
        """评估输出质量"""
        pass

    def call_llm(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        """调用 LLM"""
        if not self.client:
            return self._fallback_grading(prompt)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _fallback_grading(self, prompt: str) -> str:
        """当无法调用 LLM 时的降级评估"""
        return json.dumps({
            "score": 0.5,
            "passed": True,
            "reason": "Fallback evaluation (LLM unavailable)",
            "details": {}
        })

    def parse_json_response(self, response: str) -> Dict:
        """解析 JSON 响应"""
        try:
            # 尝试直接解析
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取 JSON 部分
            import re
            match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        return {"error": "Failed to parse response"}


class CodeQualityGrader(BaseGrader):
    """代码质量评分器"""

    SYSTEM_PROMPT = """你是一位代码审查专家。请评估代码质量。

评分维度（每项 0-1 分）：
1. 正确性：正确处理输入，逻辑无错误
2. 可读性：命名清晰，注释完整
3. 安全性：无 SQL 注入、XSS、硬编码密钥等
4. 可维护性：模块化，职责单一
5. 性能：无明显性能问题

请返回 JSON 格式：
{"correctness": 0.8, "readability": 0.9, "security": 1.0, "maintainability": 0.7, "overall": 0.85, "issues": []}
"""

    def grade(self, input_data: Dict, output: str, expected: Optional[Dict] = None) -> GradingResult:
        code = input_data.get("code", output)

        prompt = f"""评估以下代码的质量：

```{code}
```

请返回 JSON 格式评分结果。"""

        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        scores = self.parse_json_response(response)

        if "error" in scores:
            return GradingResult(
                passed=False,
                score=0.0,
                reason=f"LLM 响应解析失败: {scores['error']}",
                details={"raw_response": response}
            )

        overall = scores.get("overall", 0.5)
        issues = scores.get("issues", [])

        return GradingResult(
            passed=overall >= 0.7,
            score=overall,
            reason=f"代码质量评分 {overall:.2f}",
            details={
                "correctness": scores.get("correctness", 0),
                "readability": scores.get("readability", 0),
                "security": scores.get("security", 0),
                "maintainability": scores.get("maintainability", 0),
                "issues": issues
            }
        )


class OutputQualityGrader(BaseGrader):
    """输出质量评分器"""

    SYSTEM_PROMPT = """你是一位 AI 质量评估专家。请评估 AI 输出质量。

评分维度（每项 0-1 分）：
1. 准确性：回答正确，无事实错误
2. 完整性：回答全面，无遗漏
3. 清晰性：表达清晰，逻辑连贯
4. 相关性：回答与问题相关
5. 格式：格式规范，易于理解

请返回 JSON 格式：
{"accuracy": 0.8, "completeness": 0.9, "clarity": 1.0, "relevance": 0.9, "format": 0.85, "overall": 0.88, "issues": []}
"""

    def grade(self, input_data: Dict, output: str, expected: Optional[Dict] = None) -> GradingResult:
        question = input_data.get("question", "")
        expected_answer = input_data.get("expected", "")

        prompt = f"""评估以下 AI 回答的质量：

问题：{question}

回答：{output}

期望回答特征：{expected_answer}

请返回 JSON 格式评分结果。"""

        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        scores = self.parse_json_response(response)

        if "error" in scores:
            return GradingResult(
                passed=False,
                score=0.0,
                reason=f"LLM 响应解析失败: {scores['error']}",
                details={"raw_response": response}
            )

        overall = scores.get("overall", 0.5)

        return GradingResult(
            passed=overall >= 0.7,
            score=overall,
            reason=f"输出质量评分 {overall:.2f}",
            details={
                "accuracy": scores.get("accuracy", 0),
                "completeness": scores.get("completeness", 0),
                "clarity": scores.get("clarity", 0),
                "relevance": scores.get("relevance", 0),
                "format": scores.get("format", 0),
                "issues": scores.get("issues", [])
            }
        )


class BehaviorGrader(BaseGrader):
    """行为评分器 - 验证 Agent/Skill 行为是否符合预期"""

    SYSTEM_PROMPT = """你是一位 AI 行为分析专家。请评估 AI Agent 的行为是否符合预期。

评分维度（每项 0-1 分）：
1. 角色一致性：行为符合定义的角色
2. 工具使用：正确使用可用工具
3. 响应格式：输出格式符合规范
4. 任务完成：成功完成分配的任务
5. 错误处理：正确处理异常情况

请返回 JSON 格式：
{"role_consistency": 0.9, "tool_usage": 0.85, "response_format": 1.0, "task_completion": 0.9, "error_handling": 0.8, "overall": 0.88, "issues": []}
"""

    def grade(self, input_data: Dict, output: str, expected: Optional[Dict] = None) -> GradingResult:
        agent_name = input_data.get("agent_name", "unknown")
        task = input_data.get("task", "")
        expected_behavior = input_data.get("expected", "")

        prompt = f"""评估 AI Agent 的行为：

Agent：{agent_name}
任务：{task}
期望行为：{expected_behavior}
实际行为：{output}

请返回 JSON 格式评分结果。"""

        response = self.call_llm(prompt, self.SYSTEM_PROMPT)
        scores = self.parse_json_response(response)

        if "error" in scores:
            return GradingResult(
                passed=False,
                score=0.0,
                reason=f"LLM 响应解析失败: {scores['error']}",
                details={"raw_response": response}
            )

        overall = scores.get("overall", 0.5)

        return GradingResult(
            passed=overall >= 0.7,
            score=overall,
            reason=f"行为评分 {overall:.2f}",
            details={
                "role_consistency": scores.get("role_consistency", 0),
                "tool_usage": scores.get("tool_usage", 0),
                "response_format": scores.get("response_format", 0),
                "task_completion": scores.get("task_completion", 0),
                "error_handling": scores.get("error_handling", 0),
                "issues": scores.get("issues", [])
            }
        )


# 导出所有 grader 类
__all__ = [
    "BaseGrader",
    "GradingResult",
    "CodeQualityGrader",
    "OutputQualityGrader",
    "BehaviorGrader",
]