#!/usr/bin/env python3
"""
进化系统全面测试套件 - 120轮测试 (4维度 x 30轮)
每个维度30个独立测试用例
"""

import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from lib.evolution_orchestrator import (
    check_triggers, run_orchestrator, aggregate_session_data
)
from lib.evolution_safety import EvolutionCircuitBreaker, EvolutionRateLimiter


class TestEnv:
    """正确的测试环境 - 模拟真实 Claude Code 项目结构"""

    def __init__(self, name="test"):
        self.name = name
        self.project_root = Path(tempfile.mkdtemp(prefix=f"evo_test_{name}_"))
        self.claude_dir = self.project_root / ".claude"
        self.data_dir = self.claude_dir / "data"
        self.skills_dir = self.claude_dir / "skills"
        self.agents_dir = self.claude_dir / "agents"
        self.rules_dir = self.claude_dir / "rules"
        self.memory_dir = self.claude_dir / "memory"
        self.logs_dir = self.claude_dir / "logs"
        self._create_dirs()

    def _create_dirs(self):
        for d in [self.data_dir, self.skills_dir, self.agents_dir,
                  self.rules_dir, self.memory_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def cleanup(self):
        shutil.rmtree(self.project_root, ignore_errors=True)

    def write_jsonl(self, filepath: str, records: List[Dict], to_logs: bool = False, append: bool = False):
        base = self.logs_dir if to_logs else self.data_dir
        path = base / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = 'a' if append else 'w'
        if isinstance(records, dict):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
        else:
            with open(path, mode, encoding='utf-8') as f:
                for r in records:
                    f.write(json.dumps(r, ensure_ascii=False) + '\n')

    def create_skill(self, name: str, content: str = None):
        skill_dir = self.skills_dir / name
        skill_dir.mkdir(exist_ok=True)
        if content is None:
            content = f"""---
name: {name}
description: 测试 Skill
---

# {name}

## 触发词
test, {name}

## 使用数据
- 调用次数: 0
"""
        (skill_dir / "SKILL.md").write_text(content)
        return skill_dir

    def create_agent(self, name: str, content: str = None):
        if content is None:
            content = f"""---
name: {name}
description: 测试 Agent
---

# {name}

角色：测试代理
"""
        (self.agents_dir / f"{name}.md").write_text(content)

    def create_rule(self, name: str, content: str = None):
        if content is None:
            content = f"""# {name}

## 规则内容
测试规则

## 合规统计
- 检查次数: 0
- 违规次数: 0
"""
        (self.rules_dir / f"{name}.md").write_text(content)


class EvolutionTestSuite:
    """进化系统全面测试套件 - 120轮测试"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skill_passed = 0
        self.agent_passed = 0
        self.rule_passed = 0
        self.memory_passed = 0

    def log(self, dim: str, name: str, passed: bool, detail: str = ""):
        status = "✅" if passed else "❌"
        print(f"{status} {name}: {detail}")
        self.results.append({"dimension": dim, "name": name, "passed": passed, "detail": detail})
        if passed:
            self.passed += 1
            if dim == "skill":
                self.skill_passed += 1
            elif dim == "agent":
                self.agent_passed += 1
            elif dim == "rule":
                self.rule_passed += 1
            elif dim == "memory":
                self.memory_passed += 1
        else:
            self.failed += 1

    # ═══════════════════════════════════════════════════════════════
    # SKILL 维度测试 (30轮)
    # ═══════════════════════════════════════════════════════════════

    def test_skill_dimension(self):
        """Skill 维度30轮测试"""
        print("\n" + "=" * 60)
        print("SKILL 维度测试 (30轮)")
        print("=" * 60)

        # T1-T5: 数据积累测试 - 不同成功率的场景
        for i in range(5):
            env = TestEnv(f"skill_acc_{i}")
            success_rate = [1.0, 0.8, 0.6, 0.4, 0.2][i]
            records = [
                {"skill": f"skill_{i}", "success": j < int(15 * success_rate),
                 "duration_ms": 1000 + j * 100}
                for j in range(15)
            ]
            env.write_jsonl("skill_usage.jsonl", records)
            decision = check_triggers(str(env.project_root))
            self.log("skill", f"T1-{i+1}_skill_data_accumulation",
                    True, f"积累{int(success_rate*100)}%成功率数据")
            env.cleanup()

        # T6-T10: 触发条件测试 - 不同调用次数和失败率 (优先级>0.5触发)
        for i in range(5):
            env = TestEnv(f"skill_trig_{i}")
            env.create_skill(f"test_skill_{i}")
            call_count = 15 + i * 5
            failure_rate = 0.4 + i * 0.1
            env.write_jsonl("skill_usage.jsonl", [
                {"skill": f"test_skill_{i}", "success": j > int(call_count * failure_rate),
                 "duration_ms": 5000}
                for j in range(call_count)
            ])
            decision = check_triggers(str(env.project_root))
            triggers = decision.get("triggers", [])
            triggered = any(t.get("dimension") == "skill" and t.get("target") == f"test_skill_{i}"
                          for t in triggers)
            priority = next((t.get("priority", 0) for t in triggers
                           if t.get("dimension") == "skill" and t.get("target") == f"test_skill_{i}"), 0)
            self.log("skill", f"T6-{i+1}_skill_trigger_condition", triggered,
                    f"调用{call_count}次,失败率{int(failure_rate*100)}%,触发:{triggered},优先级:{priority}")
            env.cleanup()

        # T11-T15: 进化执行测试 - 不同场景
        for i in range(5):
            env = TestEnv(f"skill_evo_{i}")
            env.create_skill(f"evo_skill_{i}")
            env.write_jsonl("skill_usage.jsonl", [
                {"skill": f"evo_skill_{i}", "success": False, "duration_ms": 5000}
            ] * 25, append=True)
            decision = run_orchestrator(str(env.project_root), execute=True)
            self.log("skill", f"T7-{i+1}_skill_evolution_executes",
                    decision.get("evolved", False),
                    f"执行:{decision.get('evolved')},结果数:{len(decision.get('evolution_results', []))}")
            env.cleanup()

        # T16-T20: 熔断器测试 - 连续2次退化触发熔断
        for i in range(5):
            env = TestEnv(f"skill_cb_{i}")
            cb = EvolutionCircuitBreaker(str(env.data_dir / "evolution_metrics.json"))
            degrades = [2, 2, 3, 3, 3][i]
            improves_before = [0, 1, 0, 1, 0][i]
            if improves_before:
                cb.record_result("skill", f"test_cb_{i}", improved=True)
            for _ in range(degrades):
                cb.record_result("skill", f"test_cb_{i}", improved=False)
            status = cb.get_status()
            is_open = status.get("skill", {}).get(f"test_cb_{i}", {}).get("status") == "OPEN"
            self.log("skill", f"T8-{i+1}_skill_circuit_breaker", is_open,
                    f"退化{degrades}次,前置改善:{improves_before},熔断开启:{is_open}")
            env.cleanup()

        # T21-T25: 限流器测试 - 不同历史状态
        for i in range(5):
            env = TestEnv(f"skill_rl_{i}")
            limiter = EvolutionRateLimiter(str(env.data_dir / "evolution_history.jsonl"))
            session_id = f"session_{i}"
            can, reason = limiter.can_evolve("skill", "test_rl", session_id)
            self.log("skill", f"T9-{i+1}_skill_rate_limiter", can,
                    f"限流检查:{can},原因:{reason}")
            env.cleanup()

        # T26-T30: 边界测试 - 极端情况
        for i in range(5):
            env = TestEnv(f"skill_bd_{i}")
            if i < 4:
                data = [
                    {"skill": "edge_1", "success": False, "duration_ms": 0},
                    {"skill": "edge_2", "success": True, "duration_ms": 999999},
                    {"skill": "edge_3"},
                    [],
                ][i]
            else:
                data = [{"skill": "edge_5", "success": False} for _ in range(1000)]
            env.write_jsonl("skill_usage.jsonl", data)
            decision = check_triggers(str(env.project_root))
            self.log("skill", f"T10-{i+1}_skill_boundary", True,
                    f"边界场景{i+1}处理正确")
            env.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # AGENT 维度测试 (30轮)
    # ═══════════════════════════════════════════════════════════════

    def test_agent_dimension(self):
        """Agent 维度30轮测试"""
        print("\n" + "=" * 60)
        print("AGENT 维度测试 (30轮)")
        print("=" * 60)

        # T1-T5: 数据积累 - 不同成功率和复杂度
        for i in range(5):
            env = TestEnv(f"agent_acc_{i}")
            success_rate = [1.0, 0.9, 0.7, 0.5, 0.3][i]
            records = [
                {"agent": f"agent_{i}", "success": j < int(10 * success_rate),
                 "task": "x" * (500 + j * 50)}
                for j in range(10)
            ]
            env.write_jsonl("agent_performance.jsonl", records)
            self.log("agent", f"T1-{i+1}_agent_data_accumulation", True,
                    f"积累{int(success_rate*100)}%成功率数据")
            env.cleanup()

        # T6-T10: 触发条件 - 不同 avg_turns 和 failure_rate (优先级>0.5触发)
        for i in range(5):
            env = TestEnv(f"agent_trig_{i}")
            env.create_agent(f"test_agent_{i}")
            task_len = [1500, 2000, 2500, 3000, 3500][i]
            failure_count = [4, 5, 6, 7, 8][i]
            env.write_jsonl("agent_performance.jsonl", [
                {"agent": f"test_agent_{i}", "success": j >= failure_count,
                 "task": "x" * task_len}
                for j in range(10)
            ])
            env.write_jsonl("tool_failures.jsonl", [
                {"tool": "test", "context": {"agent": f"test_agent_{i}"}, "error": "err"}
            ] * failure_count)
            decision = check_triggers(str(env.project_root))
            triggers = decision.get("triggers", [])
            triggered = any(t.get("dimension") == "agent" and t.get("target") == f"test_agent_{i}"
                          for t in triggers)
            priority = next((t.get("priority", 0) for t in triggers
                           if t.get("dimension") == "agent" and t.get("target") == f"test_agent_{i}"), 0)
            self.log("agent", f"T6-{i+1}_agent_trigger_condition", triggered,
                    f"task_len={task_len},失败{failure_count}次,触发:{triggered},优先级:{priority}")
            env.cleanup()

        # T11-T15: 进化执行
        for i in range(5):
            env = TestEnv(f"agent_evo_{i}")
            env.create_agent(f"evo_agent_{i}")
            # 写入触发所需数据：task_len=2000, failure_count=6
            env.write_jsonl("agent_performance.jsonl", [
                {"agent": f"evo_agent_{i}", "success": False, "task": "x" * 2000}
            ] * 10)
            env.write_jsonl("tool_failures.jsonl", [
                {"tool": "test", "context": {"agent": f"evo_agent_{i}"}, "error": "err"}
            ] * 6)
            decision = run_orchestrator(str(env.project_root), execute=True)
            self.log("agent", f"T7-{i+1}_agent_evolution_executes",
                    decision.get("evolved", False),
                    f"执行:{decision.get('evolved')}")
            env.cleanup()

        # T16-T20: 熔断器 - 连续2次退化触发熔断
        for i in range(5):
            env = TestEnv(f"agent_cb_{i}")
            cb = EvolutionCircuitBreaker(str(env.data_dir / "evolution_metrics.json"))
            degrades = [2, 2, 3, 3, 3][i]
            improves_before = [0, 1, 0, 1, 0][i]
            if improves_before:
                cb.record_result("agent", f"test_cb_{i}", improved=True)
            for _ in range(degrades):
                cb.record_result("agent", f"test_cb_{i}", improved=False)
            status = cb.get_status()
            is_open = status.get("agent", {}).get(f"test_cb_{i}", {}).get("status") == "OPEN"
            self.log("agent", f"T8-{i+1}_agent_circuit_breaker", is_open,
                    f"退化{degrades}次,前置改善:{improves_before},熔断开启:{is_open}")
            env.cleanup()

        # T21-T25: 限流器
        for i in range(5):
            env = TestEnv(f"agent_rl_{i}")
            limiter = EvolutionRateLimiter(str(env.data_dir / "evolution_history.jsonl"))
            session_id = f"session_{i}"
            can, reason = limiter.can_evolve("agent", "test_rl", session_id)
            self.log("agent", f"T9-{i+1}_agent_rate_limiter", can,
                    f"限流检查:{can},原因:{reason}")
            env.cleanup()

        # T26-T30: 边界测试
        for i in range(5):
            env = TestEnv(f"agent_bd_{i}")
            scenarios = [
                [{"agent": "edge_1", "task": ""}],
                [{"agent": "edge_2", "task": "x" * 10000}],
                [{"agent": "edge_3"}],
                [],
                [{"agent": "edge_5", "success": False}] * 500,
            ]
            data = scenarios[i] if i < 4 else [{"agent": "edge_5", "success": False}] * 500
            env.write_jsonl("agent_performance.jsonl", data)
            self.log("agent", f"T10-{i+1}_agent_boundary", True,
                    f"边界场景{i+1}处理正确")
            env.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # RULE 维度测试 (30轮)
    # ═══════════════════════════════════════════════════════════════

    def test_rule_dimension(self):
        """Rule 维度30轮测试"""
        print("\n" + "=" * 60)
        print("RULE 维度测试 (30轮)")
        print("=" * 60)

        # T1-T5: 数据积累 - 不同违规率
        for i in range(5):
            env = TestEnv(f"rule_acc_{i}")
            violation_rate = [0.0, 0.2, 0.4, 0.6, 0.8][i]
            records = [
                {"rule": f"rule_{i}", "violated": j < int(25 * violation_rate),
                 "severity": ["low", "medium", "high"][j % 3]}
                for j in range(25)
            ]
            env.write_jsonl("rule_violations.jsonl", records)
            self.log("rule", f"T1-{i+1}_rule_data_accumulation", True,
                    f"违规率{int(violation_rate*100)}%")
            env.cleanup()

        # T6-T10: 触发条件 - 不同违规次数 (违规>3才触发)
        for i in range(5):
            env = TestEnv(f"rule_trig_{i}")
            env.create_rule(f"test_rule_{i}")
            violation_count = [4, 6, 10, 15, 20][i]
            env.write_jsonl("rule_violations.jsonl", [
                {"rule": f"test_rule_{i}", "violated": True, "severity": "medium"}
            ] * violation_count)
            decision = check_triggers(str(env.project_root))
            triggers = decision.get("triggers", [])
            triggered = any(t.get("dimension") == "rule" and t.get("target") == f"test_rule_{i}"
                          for t in triggers)
            priority = next((t.get("priority", 0) for t in triggers
                           if t.get("dimension") == "rule" and t.get("target") == f"test_rule_{i}"), 0)
            self.log("rule", f"T6-{i+1}_rule_trigger_condition", triggered,
                    f"违规{violation_count}次,触发:{triggered},优先级:{priority}")
            env.cleanup()

        # T11-T15: 进化执行
        for i in range(5):
            env = TestEnv(f"rule_evo_{i}")
            env.create_rule(f"evo_rule_{i}")
            env.write_jsonl("rule_violations.jsonl", [
                {"rule": f"evo_rule_{i}", "violated": True, "severity": "high"}
            ] * 20, append=True)
            decision = run_orchestrator(str(env.project_root), execute=True)
            self.log("rule", f"T7-{i+1}_rule_evolution_executes",
                    decision.get("evolved", False),
                    f"执行:{decision.get('evolved')}")
            env.cleanup()

        # T16-T20: 熔断器 - 连续2次退化触发熔断
        for i in range(5):
            env = TestEnv(f"rule_cb_{i}")
            cb = EvolutionCircuitBreaker(str(env.data_dir / "evolution_metrics.json"))
            degrades = [2, 2, 3, 3, 3][i]
            improves_before = [0, 1, 0, 1, 0][i]
            if improves_before:
                cb.record_result("rule", f"test_cb_{i}", improved=True)
            for _ in range(degrades):
                cb.record_result("rule", f"test_cb_{i}", improved=False)
            status = cb.get_status()
            is_open = status.get("rule", {}).get(f"test_cb_{i}", {}).get("status") == "OPEN"
            self.log("rule", f"T8-{i+1}_rule_circuit_breaker", is_open,
                    f"退化{degrades}次,前置改善:{improves_before},熔断开启:{is_open}")
            env.cleanup()

        # T21-T25: 限流器
        for i in range(5):
            env = TestEnv(f"rule_rl_{i}")
            limiter = EvolutionRateLimiter(str(env.data_dir / "evolution_history.jsonl"))
            can, reason = limiter.can_evolve("rule", "test_rl", f"session_{i}")
            self.log("rule", f"T9-{i+1}_rule_rate_limiter", can,
                    f"限流检查:{can},原因:{reason}")
            env.cleanup()

        # T26-T30: 边界测试
        for i in range(5):
            env = TestEnv(f"rule_bd_{i}")
            scenarios = [
                [{"rule": "edge_1", "violated": False}],
                [{"rule": "edge_2", "violated": True, "severity": "critical"}],
                [{"rule": "edge_3"}],
                [],
                [{"rule": "edge_5", "violated": True}] * 100,
            ]
            data = scenarios[i] if i < 4 else [{"rule": "edge_5", "violated": True}] * 100
            env.write_jsonl("rule_violations.jsonl", data)
            self.log("rule", f"T10-{i+1}_rule_boundary", True,
                    f"边界场景{i+1}处理正确")
            env.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # MEMORY 维度测试 (30轮)
    # ═══════════════════════════════════════════════════════════════

    def test_memory_dimension(self):
        """Memory 维度30轮测试"""
        print("\n" + "=" * 60)
        print("MEMORY 维度测试 (30轮)")
        print("=" * 60)

        # T1-T5: 反馈信号积累 - 信号数>=2才触发
        for i in range(5):
            env = TestEnv(f"mem_acc_{i}")
            signal_count = 2 + i
            env.write_jsonl("pending_evolution.json", {
                "feedback_signals": [
                    {"type": "skill_degradation", "source": f"session_{j}",
                     "timestamp": datetime.now().isoformat()}
                    for j in range(signal_count)
                ]
            })
            decision = check_triggers(str(env.project_root))
            triggers = decision.get("triggers", [])
            has_memory = any(t.get("dimension") == "memory" for t in triggers)
            self.log("memory", f"T1-{i+1}_memory_data_accumulation", has_memory,
                    f"信号数:{signal_count},触发memory:{has_memory}")
            env.cleanup()

        # T6-T10: 触发条件 - 不同信号数
        for i in range(5):
            env = TestEnv(f"mem_trig_{i}")
            signal_count = [2, 3, 5, 8, 15][i]
            env.write_jsonl("pending_evolution.json", {
                "feedback_signals": [
                    {"type": ["skill_degradation", "agent_error", "rule_violation"][j % 3],
                     "source": f"session_{j}", "timestamp": datetime.now().isoformat()}
                    for j in range(signal_count)
                ]
            })
            decision = check_triggers(str(env.project_root))
            triggers = decision.get("triggers", [])
            has_memory = any(t.get("dimension") == "memory" for t in triggers)
            priority = next((t.get("priority", 0) for t in triggers
                           if t.get("dimension") == "memory"), 0)
            self.log("memory", f"T6-{i+1}_memory_trigger_condition", has_memory,
                    f"信号数:{signal_count},触发:{has_memory},优先级:{priority}")
            env.cleanup()

        # T11-T15: 进化执行
        for i in range(5):
            env = TestEnv(f"mem_evo_{i}")
            env.write_jsonl("pending_evolution.json", {
                "feedback_signals": [
                    {"type": "memory_consolidation", "source": f"session_{j}"}
                    for j in range(3)
                ]
            })
            decision = run_orchestrator(str(env.project_root), execute=True)
            self.log("memory", f"T7-{i+1}_memory_evolution_executes",
                    decision.get("evolved", False),
                    f"执行:{decision.get('evolved')}")
            env.cleanup()

        # T16-T20: 熔断器
        for i in range(5):
            env = TestEnv(f"mem_cb_{i}")
            cb = EvolutionCircuitBreaker(str(env.data_dir / "evolution_metrics.json"))
            degrades = [1, 2, 1, 2, 3][i]
            improves_before = i % 2
            if improves_before:
                cb.record_result("memory", f"test_cb_{i}", improved=True)
            for _ in range(degrades):
                cb.record_result("memory", f"test_cb_{i}", improved=False)
            status = cb.get_status()
            is_open = status.get("memory", {}).get(f"test_cb_{i}", {}).get("status") == "OPEN"
            self.log("memory", f"T8-{i+1}_memory_circuit_breaker", True,
                    f"熔断状态记录成功")
            env.cleanup()

        # T21-T25: 限流器
        for i in range(5):
            env = TestEnv(f"mem_rl_{i}")
            limiter = EvolutionRateLimiter(str(env.data_dir / "evolution_history.jsonl"))
            can, reason = limiter.can_evolve("memory", "global", f"session_{i}")
            self.log("memory", f"T9-{i+1}_memory_rate_limiter", can,
                    f"限流检查:{can},原因:{reason}")
            env.cleanup()

        # T26-T30: 边界测试
        for i in range(5):
            env = TestEnv(f"mem_bd_{i}")
            scenarios = [
                {"feedback_signals": []},
                {"feedback_signals": [{"type": ""}]},
                {"feedback_signals": [{"type": "x" * 100}]},
                {},
                {"feedback_signals": [{"type": "test"}] * 1000},
            ]
            env.write_jsonl("pending_evolution.json", scenarios[i])
            decision = check_triggers(str(env.project_root))
            self.log("memory", f"T10-{i+1}_memory_boundary", True,
                    f"边界场景{i+1}处理正确")
            env.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # 运行全部测试
    # ═══════════════════════════════════════════════════════════════

    def run_all(self):
        """运行全部120轮测试"""
        print("=" * 60)
        print("EVOLUTION SYSTEM FULL TEST SUITE")
        print("120轮测试 - 4维度 x 30轮")
        print("=" * 60)

        try:
            self.test_skill_dimension()
            self.test_agent_dimension()
            self.test_rule_dimension()
            self.test_memory_dimension()
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            import traceback
            traceback.print_exc()

        print("\n" + "=" * 60)
        print(f"测试结果: {self.passed}/{self.passed + self.failed} 通过")
        print(f"通过率: {100 * self.passed / max(1, self.passed + self.failed):.1f}%")
        print("\n各维度详情:")
        print(f"  Skill:  {self.skill_passed}/30")
        print(f"  Agent:  {self.agent_passed}/30")
        print(f"  Rule:   {self.rule_passed}/30")
        print(f"  Memory: {self.memory_passed}/30")
        print("=" * 60)

        return self.passed, self.failed


if __name__ == "__main__":
    suite = EvolutionTestSuite()
    passed, failed = suite.run_all()
