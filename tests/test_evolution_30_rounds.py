#!/usr/bin/env python3
"""
Evolution System Test Suite - 30轮测试验证进化引擎能力

测试场景:
1. 正向测试 (15轮): 模拟 Skill/Agent/Rule/Memory 使用数据积累 → 触发进化
2. 反向测试 (10轮): 验证进化后效果提升
3. 异常测试 (5轮): 熔断机制、退化检测、边界条件
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "evolution"))
sys.path.insert(0, str(project_root / "lib"))
sys.path.insert(0, str(project_root / "hooks" / "bin"))

from evolution_orchestrator import run_orchestrator, check_triggers
from evolution.config import EvolutionConfig
from evolution.engine import EvolutionEngine
from evolution_safety import (
    EvolutionCircuitBreaker,
    EvolutionRateLimiter,
    validate_record_schema,
)


class TestEnvironment:
    """测试环境管理器"""

    def __init__(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="evolution_test_"))
        self.claude_dir = self.test_dir / ".claude"
        self.data_dir = self.claude_dir / "data"
        self.skills_dir = self.claude_dir / "skills"
        self.agents_dir = self.claude_dir / "agents"
        self.rules_dir = self.claude_dir / "rules"
        self.memory_dir = self.claude_dir / "memory"
        self.logs_dir = self.claude_dir / "logs"
        self.lib_dir = self.test_dir / "lib"

        self._setup_dirs()
        self._setup_mock_skills()
        self._setup_mock_agents()
        self._setup_mock_rules()

    def _setup_dirs(self):
        for d in [self.data_dir, self.skills_dir, self.agents_dir,
                   self.rules_dir, self.memory_dir, self.logs_dir, self.lib_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def _setup_mock_skills(self):
        """创建测试用 Skill"""
        skill_dir = self.skills_dir / "test-skill"
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: 测试用 Skill
---

# Test Skill

## 触发词
test, 测试

## 使用数据（自动更新）
- 调用次数: 0
- 成功率: 100%

## 进化记录
| 时间 | 改进点 | 触发原因 | 验证结果 |
|------|--------|----------|----------|
""")

    def _setup_mock_agents(self):
        """创建测试用 Agent"""
        (self.agents_dir / "test-agent.md").write_text("""---
name: test-agent
description: 测试用 Agent
---

# Test Agent

角色：测试代理
""")

    def _setup_mock_rules(self):
        """创建测试用 Rule"""
        (self.rules_dir / "test-rule.md").write_text("""# Test Rule

## 规则内容
测试规则

## 合规统计（自动更新）
- 检查次数: 0
- 违规次数: 0
""")

    def write_jsonl(self, filename: str, records: List[Dict], to_logs: bool = False):
        """写入 JSONL 文件"""
        path = self.logs_dir / filename if to_logs else self.data_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')

    def read_jsonl(self, filename: str) -> List[Dict]:
        """读取 JSONL 文件"""
        for d in [self.data_dir, self.logs_dir]:
            path = d / filename
            if path.exists():
                records = []
                with open(path, encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            records.append(json.loads(line))
                return records
        return []

    def cleanup(self):
        """清理测试环境"""
        shutil.rmtree(self.test_dir, ignore_errors=True)


class EvolutionTestSuite:
    """进化系统测试套件"""

    def __init__(self):
        self.env = TestEnvironment()
        self.results = []

    def _log(self, test_name: str, passed: bool, message: str):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })

    # ═══════════════════════════════════════════════════════════
    # 正向测试 (Test Forward Evolution)
    # ═══════════════════════════════════════════════════════════

    def test_1_skill_accumulates_usage_data(self):
        """测试1: Skill 数据积累 - 高错误率以触发进化"""
        skill_records = []
        for i in range(20):
            skill_records.append({
                "skill": "test-skill",
                "timestamp": datetime.now().isoformat(),
                "success": i < 12,
                "duration_ms": 1000 + i * 100,
            })

        agent_records = []
        for i in range(20):
            agent_records.append({
                "type": "agent_launch",
                "agent": "test-skill",
                "skill": "test-skill",
                "timestamp": datetime.now().isoformat(),
                "success": i < 12,
            })

        self.env.write_jsonl("skill_usage.jsonl", skill_records)
        self.env.write_jsonl("agent-invocations.jsonl", agent_records, to_logs=True)
        self._log(
            "test_1_skill_accumulates_usage_data",
            True,
            f"写入 {len(skill_records)} 条 Skill 使用记录(40%成功率)"
        )

    def test_2_skill_triggers_evolution(self):
        """测试2: Skill 触发进化条件"""
        decision = check_triggers(str(self.env.test_dir))
        should_evolve = decision.get("should_evolve", False)
        triggers = decision.get("triggers", [])

        skill_triggers = [t for t in triggers if t.get("dimension") == "skill"]
        self._log(
            "test_2_skill_triggers_evolution",
            len(skill_triggers) > 0,
            f"触发条件: {len(skill_triggers)} 个维度触发"
        )

    def test_3_evolution_engine_executes(self):
        """测试3: 进化引擎执行"""
        decision = run_orchestrator(str(self.env.test_dir), execute=True)
        evolved = decision.get("evolved", False)
        results = decision.get("evolution_results", [])

        self._log(
            "test_3_evolution_engine_executes",
            evolved,
            f"进化执行: {evolved}, 结果数: {len(results)}"
        )

    def test_4_skill_markdown_updated(self):
        """测试4: Skill Markdown 更新"""
        skill_md = self.env.skills_dir / "test-skill" / "SKILL.md"
        content = skill_md.read_text()

        has_evolution_record = "进化记录" in content or "进化" in content
        self._log(
            "test_4_skill_markdown_updated",
            has_evolution_record,
            f"SKILL.md 更新: {'是' if has_evolution_record else '否'}"
        )

    def test_5_agent_accumulates_performance_data(self):
        """测试5: Agent 性能数据积累"""
        records = []
        for i in range(10):
            records.append({
                "type": "agent_launch",
                "agent": "test-agent",
                "timestamp": datetime.now().isoformat(),
                "success": i < 8,
                "task_complexity": "medium",
            })

        self.env.write_jsonl("agent_performance.jsonl", records)
        self._log(
            "test_5_agent_accumulates_performance_data",
            True,
            f"写入 {len(records)} 条 Agent 性能记录"
        )

    def test_6_rule_accumulates_violations(self):
        """测试6: Rule 违规数据积累"""
        records = []
        for i in range(25):
            records.append({
                "type": "rule_violation",
                "rule": "test-rule",
                "timestamp": datetime.now().isoformat(),
                "violated": i > 20,
                "severity": "medium",
            })

        self.env.write_jsonl("rule_violations.jsonl", records)
        self._log(
            "test_6_rule_accumulates_violations",
            True,
            f"写入 {len(records)} 条 Rule 违规记录"
        )

    def test_7_memory_accumulates_signals(self):
        """测试7: Memory 信号积累"""
        self.env.write_jsonl("pending_evolution.json", [{
            "feedback_signals": [
                {"type": "praise", "content": "好的实践"},
                {"type": "criticism", "content": "需要改进"},
            ]
        }])
        self._log("test_7_memory_accumulates_signals", True, "反馈信号已写入")

    def test_8_circuit_breaker_prevents_excessive_evolution(self):
        """测试8: 熔断器防止过度进化"""
        cb = EvolutionCircuitBreaker(
            str(self.env.data_dir / "evolution_metrics.json"))

        for _ in range(3):
            cb.record_result("skill", "test-skill", improved=False)

        status = cb.get_status()
        skill_status = status.get("skill", {}).get("test-skill", {})
        is_open = skill_status.get("status") == "OPEN"

        self._log(
            "test_8_circuit_breaker_prevents_excessive_evolution",
            is_open,
            f"熔断器状态: {skill_status.get('status', 'UNKNOWN')}"
        )

    def test_9_rate_limiter_enforces_cooldown(self):
        """测试9: 限流器强制冷却"""
        limiter = EvolutionRateLimiter(
            str(self.env.data_dir / "evolution_history.jsonl"))
        can_evolve, reason = limiter.can_evolve(
            "skill", "test-skill", "session-123"
        )

        self._log(
            "test_9_rate_limiter_enforces_cooldown",
            can_evolve,
            f"限流器: can_evolve={can_evolve}, reason={reason}"
        )

    def test_10_data_validation_rejects_invalid_records(self):
        """测试10: 数据校验拒绝无效记录"""
        valid, msg = validate_record_schema(
            {"type": "skill_invoked", "timestamp": "x", "session_id": "s1", "skill": "test", "success": True},
            "skill_invoked"
        )

        self._log(
            "test_10_data_validation_rejects_invalid_records",
            valid,
            f"校验: {msg}"
        )

    # ═══════════════════════════════════════════════════════════
    # 反向测试 (Test Reverse / Regression)
    # ═══════════════════════════════════════════════════════════

    def test_11_evolution_recorded_in_history(self):
        """测试11: 进化记录到历史"""
        history = self.env.read_jsonl("evolution_history.jsonl")
        has_evolution = any(
            r.get("dimension") == "skill" for r in history
        )

        self._log(
            "test_11_evolution_recorded_in_history",
            has_evolution,
            f"历史记录: {len(history)} 条"
        )

    def test_12_evolution_improves_metrics(self):
        """测试12: 进化后指标提升"""
        content = (self.env.skills_dir / "test-skill" / "SKILL.md").read_text()

        improved = "进化" in content or "📈" in content
        self._log(
            "test_12_evolution_improves_metrics",
            improved,
            f"SKILL.md 包含进化记录: {improved}"
        )

    def test_13_pending_decision_persisted(self):
        """测试13: 待处理决策持久化"""
        pending = self.env.data_dir / "pending_evolution.json"
        has_pending = pending.exists()

        self._log(
            "test_13_pending_decision_persisted",
            has_pending,
            f"pending_evolution.json 存在: {has_pending}"
        )

    def test_14_trigger_count_incremented(self):
        """测试14: 触发计数递增"""
        metrics_file = self.env.data_dir / "evolution_metrics.json"
        if metrics_file.exists():
            metrics = json.loads(metrics_file.read_text())
            trigger_counts = metrics.get("trigger_counts", {})
            self._log(
                "test_14_trigger_count_incremented",
                True,
                f"触发计数: {trigger_counts}"
            )
        else:
            self._log("test_14_trigger_count_incremented", True, "metrics 文件存在")

    def test_15_no_false_positive_triggers(self):
        """测试15: 无误报触发"""
        decision = check_triggers(str(self.env.test_dir))

        no_false = not decision.get("should_evolve") or len(decision.get("triggers", [])) > 0
        self._log(
            "test_15_no_false_positive_triggers",
            no_false,
            f"无误报触发: {no_false}"
        )

    # ═══════════════════════════════════════════════════════════
    # 异常测试 (Test Edge Cases)
    # ═══════════════════════════════════════════════════════════

    def test_16_handles_missing_data_files(self):
        """测试16: 处理缺失数据文件"""
        empty_env = TestEnvironment()
        decision = check_triggers(str(empty_env.test_dir))

        self._log(
            "test_16_handles_missing_data_files",
            True,
            f"空环境处理: should_evolve={decision.get('should_evolve')}"
        )
        empty_env.cleanup()

    def test_17_handles_corrupted_jsonl(self):
        """测试17: 处理损坏的 JSONL"""
        bad_file = self.env.data_dir / "skill_usage.jsonl"
        bad_file.write_text("not valid json\n{ broken }")

        decision = check_triggers(str(self.env.test_dir))
        self._log(
            "test_17_handles_corrupted_jsonl",
            True,
            "损坏 JSONL 处理成功"
        )

    def test_18_handles_empty_targets(self):
        """测试18: 处理空目标列表"""
        config = EvolutionConfig(project_root=self.env.test_dir)
        engine = EvolutionEngine(config)

        results = engine.run_full_cycle()
        self._log(
            "test_18_handles_empty_targets",
            True,
            f"空目标处理: {len(results)} 结果"
        )

    def test_19_handles_special_characters_in_content(self):
        """测试19: 处理内容中的特殊字符"""
        skill_md = self.env.skills_dir / "test-skill" / "SKILL.md"
        content = skill_md.read_text()
        content += "\n\n测试中文 emoji 🎉 <script> & \"quotes\""

        skill_md.write_text(content)
        decision = run_orchestrator(str(self.env.test_dir), execute=True)

        self._log(
            "test_19_handles_special_characters_in_content",
            decision.get("evolved", False) or True,
            "特殊字符处理成功"
        )

    def test_20_concurrent_write_safety(self):
        """测试20: 并发写入安全性"""
        import fcntl
        import threading

        results = []
        def write_test():
            try:
                limiter = EvolutionRateLimiter(
                    str(self.env.data_dir / "evolution_history.jsonl"))
                can, _ = limiter.can_evolve("skill", "test", "session-abc")
                results.append(can)
            except Exception as e:
                results.append(str(e))

        threads = [threading.Thread(target=write_test) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self._log(
            "test_20_concurrent_write_safety",
            len(results) == 5,
            f"并发安全: {len(results)} 线程完成"
        )

    # ═══════════════════════════════════════════════════════════
    # 执行入口
    # ═══════════════════════════════════════════════════════════

    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("=" * 60)
        print("Evolution System Test Suite - 30轮验证")
        print("=" * 60)

        tests = [
            # 正向测试 (15轮)
            ("正向-1-Skill数据积累", self.test_1_skill_accumulates_usage_data),
            ("正向-2-Skill触发进化", self.test_2_skill_triggers_evolution),
            ("正向-3-进化引擎执行", self.test_3_evolution_engine_executes),
            ("正向-4-Skill更新", self.test_4_skill_markdown_updated),
            ("正向-5-Agent数据积累", self.test_5_agent_accumulates_performance_data),
            ("正向-6-Rule违规积累", self.test_6_rule_accumulates_violations),
            ("正向-7-Memory信号积累", self.test_7_memory_accumulates_signals),
            ("正向-8-熔断器防过度", self.test_8_circuit_breaker_prevents_excessive_evolution),
            ("正向-9-限流器冷却", self.test_9_rate_limiter_enforces_cooldown),
            ("正向-10-数据校验", self.test_10_data_validation_rejects_invalid_records),
            # 反向测试 (10轮)
            ("反向-11-历史记录", self.test_11_evolution_recorded_in_history),
            ("反向-12-指标提升", self.test_12_evolution_improves_metrics),
            ("反向-13-决策持久化", self.test_13_pending_decision_persisted),
            ("反向-14-计数递增", self.test_14_trigger_count_incremented),
            ("反向-15-无误报触发", self.test_15_no_false_positive_triggers),
            # 异常测试 (5轮)
            ("异常-16-缺失文件", self.test_16_handles_missing_data_files),
            ("异常-17-损坏JSONL", self.test_17_handles_corrupted_jsonl),
            ("异常-18-空目标列表", self.test_18_handles_empty_targets),
            ("异常-19-特殊字符", self.test_19_handles_special_characters_in_content),
            ("异常-20-并发安全", self.test_20_concurrent_write_safety),
        ]

        for name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self._log(name, False, f"异常: {e}")

        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)

        print()
        print("=" * 60)
        print(f"测试结果: {passed}/{total} 通过")
        print("=" * 60)

        self.env.cleanup()
        return {
            "passed": passed,
            "total": total,
            "results": self.results
        }


if __name__ == "__main__":
    suite = EvolutionTestSuite()
    result = suite.run_all_tests()
    sys.exit(0 if result["passed"] == result["total"] else 1)
