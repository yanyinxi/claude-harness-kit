#!/usr/bin/env python3
"""
Pass@k 指标计算

用于评估 LLM 生成能力的稳定性
pass@k = 在 k 次尝试中至少成功一次的概率
"""

import math
import json
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class PassAtKResult:
    """Pass@k 结果"""
    pass_at_1: float
    pass_at_3: float
    pass_at_5: float
    pass_at_10: float
    total_attempts: int
    total_passed: int
    success_rate: float


def binomial(n: int, k: int) -> float:
    """计算二项式系数 C(n, k)"""
    if k > n or k < 0:
        return 0.0
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def calculate_pass_at_k(
    results: List[bool],
    k_values: List[int] = None
) -> PassAtKResult:
    """
    计算 pass@k 指标

    pass@k = E[1 - C(n-c, k) / C(n, k)]

    其中:
    - n = 总尝试次数
    - c = 通过次数
    - k = 每次考虑的样本数

    Args:
        results: 每轮测试的结果列表 (True=通过, False=失败)
        k_values: 要计算的 k 值列表，默认 [1, 3, 5, 10]

    Returns:
        PassAtKResult 对象
    """
    if k_values is None:
        k_values = [1, 3, 5, 10]

    n = len(results)
    c = sum(results)  # 通过次数

    metrics = {}
    for k in k_values:
        if n < k:
            metrics[f"pass_at_{k}"] = 0.0
        else:
            # 使用无偏估计器计算 pass@k
            if c >= k:
                # 所有样本都能在 k 次中成功
                metrics[f"pass_at_{k}"] = 1.0
            else:
                # 使用概率估计公式
                # pass@k = 1 - C(n-c, k) / C(n, k)
                try:
                    numerator = sum(
                        binomial(c, i) * binomial(n - c, k - i)
                        for i in range(c + 1)
                    )
                    denominator = binomial(n, k)
                    if denominator > 0:
                        metrics[f"pass_at_{k}"] = 1.0 - (numerator / denominator)
                    else:
                        metrics[f"pass_at_{k}"] = 0.0
                except (ValueError, ZeroDivisionError):
                    metrics[f"pass_at_{k}"] = 0.0

    return PassAtKResult(
        pass_at_1=metrics.get("pass_at_1", 0.0),
        pass_at_3=metrics.get("pass_at_3", 0.0),
        pass_at_5=metrics.get("pass_at_5", 0.0),
        pass_at_10=metrics.get("pass_at_10", 0.0),
        total_attempts=n,
        total_passed=c,
        success_rate=c / n if n > 0 else 0.0
    )


def calculate_confidence_interval(
    results: List[bool],
    confidence: float = 0.95,
    n_bootstrap: int = 1000
) -> Tuple[float, float]:
    """
    计算 pass@k 的置信区间 (使用 bootstrap)

    Args:
        results: 测试结果列表
        confidence: 置信度 (默认 95%)
        n_bootstrap: bootstrap 采样次数

    Returns:
        (下界, 上界) 元组
    """
    import random

    n = len(results)
    pass_at_k_samples = []

    for _ in range(n_bootstrap):
        # Bootstrap 采样
        sample = [random.choice(results) for _ in range(n)]
        result = calculate_pass_at_k(sample, k_values=[10])
        pass_at_k_samples.append(result.pass_at_10)

    # 计算百分位数
    alpha = (1 - confidence) / 2
    lower = sorted(pass_at_k_samples)[int(alpha * n_bootstrap)]
    upper = sorted(pass_at_k_samples)[int((1 - alpha) * n_bootstrap)]

    return lower, upper


class EvaluationRunner:
    """评估运行器 - 管理多轮评估"""

    def __init__(self, n_rounds: int = 10):
        """
        初始化评估运行器

        Args:
            n_rounds: 每轮评估的重复次数
        """
        self.n_rounds = n_rounds
        self.results: List[List[bool]] = []

    def run_round(self, test_func, *args, **kwargs) -> List[bool]:
        """
        运行一轮评估

        Args:
            test_func: 测试函数
            *args, **kwargs: 传递给测试函数的参数

        Returns:
            该轮所有尝试的结果列表
        """
        round_results = []
        for _ in range(self.n_rounds):
            try:
                result = test_func(*args, **kwargs)
                round_results.append(bool(result))
            except Exception:
                round_results.append(False)
        self.results.append(round_results)
        return round_results

    def get_aggregate_results(self) -> Dict[str, Any]:
        """获取聚合结果"""
        all_results = [r for round_results in self.results for r in round_results]
        pass_at_k = calculate_pass_at_k(all_results)

        return {
            "total_rounds": len(self.results),
            "total_attempts": len(all_results),
            "total_passed": sum(all_results),
            "success_rate": pass_at_k.success_rate,
            "pass_at_k": asdict(pass_at_k),
            "per_round_results": [
                sum(r) / len(r) if r else 0
                for r in self.results
            ]
        }


# ── 命令行工具 ──────────────────────────────────────────────────

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Pass@k 指标计算")
    parser.add_argument("results", help="测试结果 JSON 文件或字符串")
    parser.add_argument("--k", nargs="+", type=int, default=[1, 3, 5, 10],
                        help="要计算的 k 值")
    args = parser.parse_args()

    # 解析结果
    try:
        results = json.loads(args.results)
    except json.JSONDecodeError:
        # 尝试从文件读取
        try:
            with open(args.results) as f:
                results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 尝试解析为逗号分隔的布尔值
            results = [r.strip().lower() == "true" for r in args.results.split(",")]

    # 计算 pass@k
    if isinstance(results, str):
        results = [r.strip().lower() == "true" for r in results.split(",")]

    result = calculate_pass_at_k(results, k_values=args.k)

    # 输出结果
    print(f"Pass@k Results")
    print(f"=" * 40)
    print(f"总尝试次数: {result.total_attempts}")
    print(f"通过次数: {result.total_passed}")
    print(f"成功率: {result.success_rate:.2%}")
    print()
    print(f"Pass@1:  {result.pass_at_1:.2%}")
    print(f"Pass@3:  {result.pass_at_3:.2%}")
    print(f"Pass@5:  {result.pass_at_5:.2%}")
    print(f"Pass@10: {result.pass_at_10:.2%}")


if __name__ == "__main__":
    main()