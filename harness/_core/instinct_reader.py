#!/usr/bin/env python3
"""
本能读取模块 - 从 instinct-record.json 读取高置信度本能

功能：
- 读取 instinct-record.json
- 过滤 confidence >= 0.7 的本能
- 生成注入文本（带置信度标注）
- 追踪本能应用成功率

使用方式：
  python3 -m harness._core.instinct_reader
  from harness._core.instinct_reader import get_high_confidence_instincts, format_instinct_for_injection, record_instinct_application
"""
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# 统一 sys.path 设置
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(_project_root))

logger = logging.getLogger(__name__)

# 默认阈值
DEFAULT_MIN_CONFIDENCE = 0.7

# 本能记录文件路径
INSTINCT_RECORD_FILE = _project_root / "harness" / "memory" / "instinct-record.json"

# 本能应用统计文件
INSTINCT_STATS_FILE = _project_root / ".claude" / "data" / "instinct_stats.json"


@dataclass
class Instinct:
    """本能数据结构"""
    id: str
    pattern: str
    confidence: float
    applied_count: int
    reinforcement_count: int
    source: str
    created_at: str
    root_cause: str = ""


def _load_instincts() -> list[dict]:
    """加载本能记录"""
    if not INSTINCT_RECORD_FILE.exists():
        logger.warning(f"本能记录文件不存在: {INSTINCT_RECORD_FILE}")
        return []

    try:
        with open(INSTINCT_RECORD_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 支持两种格式：列表或对象
        if isinstance(data, dict):
            instincts = data.get("instincts", [])
        elif isinstance(data, list):
            instincts = data
        else:
            instincts = []

        return instincts
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"读取本能记录失败: {e}")
        return []


def get_high_confidence_instincts(min_confidence: float = DEFAULT_MIN_CONFIDENCE) -> list[Instinct]:
    """
    获取高置信度本能列表

    Args:
        min_confidence: 最小置信度阈值，默认 0.7

    Returns:
        高置信度本能列表，按置信度降序排列
    """
    instincts_data = _load_instincts()

    high_confidence = []
    for item in instincts_data:
        confidence = item.get("confidence", 0)
        if confidence >= min_confidence:
            instinct = Instinct(
                id=item.get("id", ""),
                pattern=item.get("pattern", ""),
                confidence=confidence,
                applied_count=item.get("applied_count", 0),
                reinforcement_count=item.get("reinforcement_count", 0),
                source=item.get("source", ""),
                created_at=item.get("created_at", ""),
                root_cause=item.get("root_cause", ""),
            )
            high_confidence.append(instinct)

    # 按置信度降序排列
    high_confidence.sort(key=lambda x: x.confidence, reverse=True)

    return high_confidence


def format_instinct_for_injection(instinct: Instinct) -> str:
    """
    格式化本能为注入文本

    Args:
        instinct: 本能对象

    Returns:
        格式化的注入文本
    """
    confidence_bar = "█" * int(instinct.confidence * 10) + "░" * (10 - int(instinct.confidence * 10))

    lines = [
        f"  【本能】{instinct.pattern}",
        f"    置信度: [{confidence_bar}] {instinct.confidence:.0%}",
        f"    应用: {instinct.applied_count}次 | 强化: {instinct.reinforcement_count}次",
    ]

    if instinct.root_cause:
        lines.append(f"    原因: {instinct.root_cause[:50]}...")

    return "\n".join(lines)


def format_all_instincts_for_injection(instincts: list[Instinct]) -> str:
    """
    格式化所有本能为注入文本

    Args:
        instincts: 本能列表

    Returns:
        格式化的注入文本
    """
    if not instincts:
        return ""

    lines = [
        "",
        "──────────────────────────────────────────────────────────────",
        "【本能记录】confidence >= 0.7（按置信度排序）",
        "",
    ]

    for instinct in instincts[:5]:  # 最多显示 5 个
        lines.append(format_instinct_for_injection(instinct))
        lines.append("")

    if len(instincts) > 5:
        lines.append(f"  ... 还有 {len(instincts) - 5} 个本能（查看 harness/memory/instinct-record.json）")

    lines.append("──────────────────────────────────────────────────────────────")

    return "\n".join(lines)


def get_instinct_stats() -> dict:
    """获取本能统计信息"""
    all_instincts = _load_instincts()

    total = len(all_instincts)
    high_conf = len(get_high_confidence_instincts())
    avg_confidence = sum(i.get("confidence", 0) for i in all_instincts) / total if total > 0 else 0

    return {
        "total": total,
        "high_confidence": high_conf,
        "avg_confidence": round(avg_confidence, 2),
    }


def _load_stats() -> dict:
    """加载本能应用统计"""
    if not INSTINCT_STATS_FILE.exists():
        return {"applications": {}, "total_apps": 0, "total_success": 0}

    try:
        with open(INSTINCT_STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"applications": {}, "total_apps": 0, "total_success": 0}


def _save_stats(stats: dict) -> None:
    """保存本能应用统计"""
    INSTINCT_STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(INSTINCT_STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    except OSError as e:
        logger.error(f"保存本能统计失败: {e}")


def record_instinct_application(instinct_id: str, success: bool = True) -> dict:
    """
    记录本能应用结果（用于追踪成功率）

    Args:
        instinct_id: 本能 ID
        success: 是否成功应用

    Returns:
        更新后的统计信息
    """
    stats = _load_stats()

    if instinct_id not in stats["applications"]:
        stats["applications"][instinct_id] = {"attempts": 0, "successes": 0}

    stats["applications"][instinct_id]["attempts"] += 1
    if success:
        stats["applications"][instinct_id]["successes"] += 1

    stats["total_apps"] += 1
    if success:
        stats["total_success"] += 1

    _save_stats(stats)
    return get_application_stats()


def get_application_stats() -> dict:
    """
    获取本能应用成功率统计

    Returns:
        {
            "total_apps": int,      # 总应用次数
            "total_success": int,   # 成功次数
            "success_rate": float,  # 成功率
            "by_instinct": {        # 各本能详情
                "instinct-id": {
                    "attempts": int,
                    "successes": int,
                    "rate": float
                }
            }
        }
    """
    stats = _load_stats()

    result = {
        "total_apps": stats.get("total_apps", 0),
        "total_success": stats.get("total_success", 0),
        "success_rate": 0.0,
        "by_instinct": {}
    }

    if result["total_apps"] > 0:
        result["success_rate"] = round(result["total_success"] / result["total_apps"], 2)

    for instinct_id, data in stats.get("applications", {}).items():
        attempts = data.get("attempts", 0)
        successes = data.get("successes", 0)
        result["by_instinct"][instinct_id] = {
            "attempts": attempts,
            "successes": successes,
            "rate": round(successes / attempts, 2) if attempts > 0 else 0.0
        }

    return result


def format_application_stats() -> str:
    """
    格式化应用统计为可读文本

    Returns:
        格式化的统计文本
    """
    stats = get_application_stats()

    if stats["total_apps"] == 0:
        return ""

    lines = [
        "",
        "──────────────────────────────────────────────────────────────",
        "【本能应用统计】",
        f"  总应用次数: {stats['total_apps']}",
        f"  成功次数: {stats['total_success']}",
        f"  成功率: {stats['success_rate']:.0%}",
    ]

    if stats["by_instinct"]:
        lines.append("")
        lines.append("  各本能详情:")
        for instinct_id, data in stats["by_instinct"].items():
            rate = data["rate"]
            bar = "█" * int(rate * 10) + "░" * (10 - int(rate * 10))
            lines.append(f"    {instinct_id[:20]}: [{bar}] {rate:.0%} ({data['successes']}/{data['attempts']})")

    lines.append("──────────────────────────────────────────────────────────────")

    return "\n".join(lines)


def main():
    """主入口 - 测试用"""
    print("=== 本能读取模块测试 ===\n")

    # 统计信息
    stats = get_instinct_stats()
    print(f"统计: 共 {stats['total']} 个本能，{stats['high_confidence']} 个高置信度，平均置信度 {stats['avg_confidence']}")

    # 高置信度本能
    instincts = get_high_confidence_instincts()
    print(f"\n高置信度本能（>= 0.7）: {len(instincts)} 个")

    if instincts:
        output = format_all_instincts_for_injection(instincts)
        print(output)
    else:
        print("  （无高置信度本能）")


if __name__ == "__main__":
    main()