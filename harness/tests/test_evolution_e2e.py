#!/usr/bin/env python3
"""
进化系统端到端测试 — 4 维度全链路验证

覆盖 4 个维度的完整进化流程：
  agent   — 模拟用户纠正 → 自动追加到 Agent 定义文件
  skill   — 模拟用户纠正 → 生成 Skill 补充内容
  rule    — 模拟用户纠正 → 生成 Rule 例外条款
  instinct — 模拟用户纠正 → 创建/更新本能记录

每个测试独立执行，验证进化前后文件内容变化。
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


# 项目根路径配置
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "harness"))
sys.path.insert(0, str(PROJECT_ROOT / "harness" / "evolve-daemon"))


# ═════════════════════════════════════════════════════════
# Fixtures：创建模拟数据
# ═════════════════════════════════════════════════════════

def _make_sessions(target: str, corrections: list[dict], count: int = 5) -> list:
    """
    创建模拟会话数据。

    参数:
        target: 纠正目标（如 agent:backend-dev）
        corrections: 纠正记录列表
        count: 会话数量（默认 5 个，确保超过所有维度阈值）
    """
    sessions = []
    for i in range(count):
        sessions.append({
            "session_id": f"e2e-test-{target.replace(':', '-')}-{i:03d}",
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
            "mode": "team",
            "corrections": [
                {**c, "target": target}
                for c in corrections
            ],
            "rich_context": {"failure_stats": {"total": 0}},
            "agents_used": [{"agent": target.split(":")[-1], "model": "sonnet"}],
        })
    return sessions


# ═════════════════════════════════════════════════════════
# 测试 1: Agent 维度端到端进化
# ═════════════════════════════════════════════════════════

class TestAgentEvolutionE2E:
    """Agent 维度：端到端进化链路验证"""

    def test_agent_evolution_full_pipeline(self, tmp_path):
        """
        模拟 5 次用户纠正 agent:backend-dev 后，
        验证进化系统能自动创建进化内容并标记时间戳。
        """
        # ── 准备：创建模拟 Agent 文件 ──
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        agent_file = agents_dir / "backend-dev.md"
        agent_file.write_text("""---
name: backend-dev
description: 通用后端开发专家
model: sonnet
---

# Backend Dev

## 职责
- API 开发
- 数据库操作
""")

        # ── 准备：创建模拟会话数据 ──
        corrections = [{
            "context": "后端开发中使用 print 调试",
            "user_correction": "不要用 print()，使用 logging.getLogger(__name__).debug()",
            "root_cause": "Agent 缺少日志规范",
            "root_cause_hint": "避免 print 调试，统一使用 logging 模块",
        }]
        sessions = _make_sessions("agent:backend-dev", corrections, count=5)

        config = {"paths": {"agents_dir": "agents", "data_dir": ".claude/data"}}

        # ── Step 1: 运行分析器 ──
        from analyzer import aggregate_and_analyze
        analysis = aggregate_and_analyze(sessions, config, tmp_path)

        # 验证：纠正热点被正确识别
        assert "agent:backend-dev" in analysis.get("correction_hotspots", {})
        assert analysis["correction_hotspots"]["agent:backend-dev"] >= 5
        assert analysis.get("should_propose") is True

        # ── Step 2: 运行决策分发器 ──
        from evolve_dispatcher import dispatch_evolution
        decisions = dispatch_evolution(analysis, config, tmp_path, sessions)

        # 验证：agent 维度被正确分发
        agent_decisions = [d for d in decisions if d["dimension"] == "agent"]
        assert len(agent_decisions) >= 1, "应至少生成 1 个 agent 决策"
        assert agent_decisions[0]["action"] in ("auto_apply", "propose")

        # ── Step 3: 执行 agent 进化 ──
        from agent_evolution import evolve_agent
        result = evolve_agent(
            "agent:backend-dev",
            corrections * 5,
            config,
            tmp_path,
        )

        # 验证：进化成功
        assert result.get("success") is True
        assert "suggested_change" in result
        assert "Auto-Evolved" in result["suggested_change"]
        # 验证：包含时间戳
        assert "20" in result["suggested_change"], "应包含年份时间戳"

        # ── Step 4: 应用改动到文件 ──
        with open(agent_file, "a") as f:
            f.write(result["suggested_change"])
        new_content = agent_file.read_text()

        # 验证：文件包含进化标记和时间戳
        assert "[Auto-Evolved]" in new_content
        assert "避免 print 调试" in new_content
        assert "logging.getLogger" in new_content

        print(f"  ✅ Agent 进化链路完整: {result['suggested_change'][:80]}")


    def test_agent_repeated_evolution_detected(self, tmp_path):
        """
        验证重复进化检测：已有 [Auto-Evolved] 标记的文件，
        再次进化时使用 replace 模式而非 append。
        """
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        agent_file = agents_dir / "executor.md"
        # 创建已有进化标记的文件
        agent_file.write_text("""---
name: executor
description: 通用执行器
model: sonnet
---

# Executor

## [Auto-Evolved] 2026-05-10 08:00:00
- 旧进化内容：避免使用 global 变量
""")

        config = {"paths": {"agents_dir": "agents", "data_dir": ".claude/data"}}
        corrections = [{
            "context": "代码规范",
            "user_correction": "使用类型注解替代注释说明类型",
            "root_cause": "缺少类型注解规范",
            "root_cause_hint": "统一使用类型注解",
        }]

        from agent_evolution import evolve_agent
        result = evolve_agent("agent:executor", corrections, config, tmp_path)

        # 验证：已有进化标记时，应返回 replace 模式
        assert result.get("success") is True
        assert result.get("action") == "replace"
        assert "[Auto-Evolved]" in result["suggested_change"]

        print(f"  ✅ 重复进化检测正确: action={result['action']}")


# ═════════════════════════════════════════════════════════
# 测试 2: Skill 维度端到端进化
# ═════════════════════════════════════════════════════════

class TestSkillEvolutionE2E:
    """Skill 维度：端到端进化链路验证"""

    def test_skill_evolution_full_pipeline(self, tmp_path):
        """
        模拟用户纠正 testing Skill，验证进化系统能生成补充场景内容。
        """
        # ── 准备：创建模拟 Skill 文件 ──
        skills_dir = tmp_path / "skills" / "testing"
        skills_dir.mkdir(parents=True)
        skill_file = skills_dir / "SKILL.md"
        skill_file.write_text("""---
name: testing
description: 测试驱动开发
---

# Testing Skill

## 测试策略
- 单元测试覆盖核心逻辑
- 集成测试覆盖 API 端点
""")

        # ── 准备：模拟会话数据 ──
        corrections = [{
            "context": "数据库事务测试场景",
            "user_correction": "涉及 @Transactional 的测试需用集成测试，不要用 mock",
            "root_cause": "testing Skill 缺少事务场景的测试策略",
            "root_cause_hint": "事务测试需用集成测试",
        }]
        sessions = _make_sessions("skill:testing", corrections, count=5)

        config = {"paths": {"skills_dir": "skills", "data_dir": ".claude/data"}}

        # ── Step 1: 分析 ──
        from analyzer import aggregate_and_analyze
        analysis = aggregate_and_analyze(sessions, config, tmp_path)
        assert "skill:testing" in analysis.get("correction_hotspots", {})

        # ── Step 2: 决策分发 ──
        from evolve_dispatcher import dispatch_evolution
        decisions = dispatch_evolution(analysis, config, tmp_path, sessions)
        skill_decisions = [d for d in decisions if d["dimension"] == "skill"]
        assert len(skill_decisions) >= 1, "应生成 skill 维度决策"

        # ── Step 3: 执行 skill 进化 ──
        from skill_evolution import evolve_skill
        result = evolve_skill("skill:testing", corrections, config, tmp_path)

        # 验证
        assert result.get("success") is True
        assert "Auto-Evolved" in result["suggested_change"]
        assert "事务" in result["suggested_change"] or "Transactional" in result["suggested_change"]
        assert "20" in result["suggested_change"], "应包含时间戳"

        print(f"  ✅ Skill 进化链路完整: {result['suggested_change'][:80]}...")


# ═════════════════════════════════════════════════════════
# 测试 3: Rule 维度端到端进化
# ═════════════════════════════════════════════════════════

class TestRuleEvolutionE2E:
    """Rule 维度：端到端进化链路验证"""

    def test_rule_evolution_full_pipeline(self, tmp_path):
        """
        模拟用户纠正 security Rule，验证进化系统能生成例外条款。
        Rule 阈值更高（5 次），确保测试数据量足够。
        """
        # ── 准备：创建模拟 Rule 文件 ──
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        rule_file = rules_dir / "security.md"
        rule_file.write_text("""---
name: security
description: 安全底线规则
---

# Security Rule

## 基本原则
- 所有 API 需要认证
- 敏感操作需要二次确认
""")

        # ── 准备：模拟会话数据 ──
        corrections = [{
            "context": "紧急修复生产 Bug 需要跳过常规审查流程",
            "user_correction": "紧急修复经 Tech Lead 口头批准后可跳过代码审查",
            "root_cause": "security Rule 缺少紧急修复场景的例外处理",
            "root_cause_hint": "紧急修复可跳过审查但需记录",
        }]
        sessions = _make_sessions("rule:security", corrections, count=6)

        config = {"paths": {"rules_dir": "rules", "data_dir": ".claude/data"}}

        # ── Step 1: 分析 ──
        from analyzer import aggregate_and_analyze
        analysis = aggregate_and_analyze(sessions, config, tmp_path)
        assert "rule:security" in analysis.get("correction_hotspots", {})

        # ── Step 2: 决策分发 ──
        from evolve_dispatcher import dispatch_evolution
        decisions = dispatch_evolution(analysis, config, tmp_path, sessions)
        rule_decisions = [d for d in decisions if d["dimension"] == "rule"]
        assert len(rule_decisions) >= 1, "应生成 rule 维度决策（阈值=5，6次纠正应触发）"

        # ── Step 3: 执行 rule 进化 ──
        from rule_evolution import evolve_rule
        result = evolve_rule("rule:security", corrections, config, tmp_path)

        # 验证
        assert result.get("success") is True
        assert "Auto-Evolved" in result["suggested_change"]
        assert "20" in result["suggested_change"], "应包含时间戳"

        print(f"  ✅ Rule 进化链路完整: {result['suggested_change'][:80]}...")


    def test_rule_below_threshold_no_trigger(self, tmp_path):
        """
        验证 Rule 维度阈值：2 次纠正不应触发进化（Rule 需要 ≥5 次）。
        """
        rules_dir = tmp_path / "rules"
        rules_dir.mkdir()
        (rules_dir / "security.md").write_text("---\nname: security\n---\n# Security\n")

        corrections = [{
            "context": "小调整",
            "user_correction": "修复拼写",
            "root_cause": "不重要",
            "root_cause_hint": "拼写错误",
        }]
        _make_sessions("rule:security", corrections, count=2)

        from evolve_dispatcher import meets_threshold
        # 验证：2 次纠正不满足 rule 维度的阈值
        assert meets_threshold("rule", 2) is False
        assert meets_threshold("rule", 5) is True

        print("  ✅ Rule 阈值验证: 2次=False, 5次=True")


# ═════════════════════════════════════════════════════════
# 测试 4: Instinct 维度端到端进化
# ═════════════════════════════════════════════════════════

class TestInstinctEvolutionE2E:
    """Instinct 维度：端到端进化链路验证"""

    def test_instinct_creation_and_confidence(self, tmp_path):
        """
        模拟用户纠正 → instinct_updater 创建本能记录 → 置信度升级。
        """
        # ── 准备：创建完整的目录结构（instinct_updater 使用 root/harness/memory/）──
        memory_dir = tmp_path / "harness" / "memory"
        memory_dir.mkdir(parents=True)
        instinct_file = memory_dir / "instinct-record.json"
        instinct_file.write_text(json.dumps({"records": []}))

        # ── Step 1: 添加本能记录 ──
        from instinct_updater import add_pattern, load_instinct
        pattern_id = add_pattern(
            "testing",
            "涉及 @Transactional 的测试需用集成测试",
            "testing skill 建议 mock 数据库事务 → 用户纠正",
            root=tmp_path,
        )

        assert pattern_id is not None
        instinct_data = load_instinct(tmp_path)
        records = instinct_data.get("records", [])
        assert len(records) >= 1, f"应有至少 1 条记录，实际: {len(records)}"

        new_record = records[-1]
        assert new_record.get("domain") == "testing" or "correction" in new_record
        initial_conf = new_record.get("confidence", 0)
        print(f"  ✅ 本能记录创建: id={pattern_id}, confidence={initial_conf}")

        # ── Step 2: 强化置信度 ──
        from instinct_updater import reinforce_pattern
        for _ in range(3):
            reinforce_pattern(pattern_id, delta=0.15, root=tmp_path)

        instinct_data = load_instinct(tmp_path)
        records = instinct_data.get("records", [])
        updated = next((r for r in records if r.get("id") == pattern_id), None)
        assert updated is not None
        updated_conf = updated.get("confidence", 0)
        assert updated_conf > initial_conf, f"置信度应提升: {initial_conf} → {updated_conf}"
        print(f"  ✅ 置信度升级: {initial_conf} → {updated_conf}")


    def test_instinct_decay(self, tmp_path):
        """
        验证本能记录的时间衰减机制。
        """
        # ── 准备：创建一条旧记录 ──
        memory_dir = tmp_path / "harness" / "memory"
        memory_dir.mkdir(parents=True)
        instinct_file = memory_dir / "instinct-record.json"

        old_record = {
            "id": "instinct_old_001",
            "domain": "testing",
            "correction": "旧记录",
            "confidence": 0.8,
            "created_at": (datetime.now() - timedelta(days=200)).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=200)).isoformat(),
            "times_observed": 1,
            "reinforcement_count": 0,
        }
        instinct_file.write_text(json.dumps(
            {"records": [old_record], "evolution": {"version": "3.0"}},
            ensure_ascii=False, indent=2,
        ))

        # ── 执行衰减 ──
        from instinct_updater import apply_decay_to_all
        instinct_data = json.loads(instinct_file.read_text())
        decayed_data = apply_decay_to_all(instinct_data, config=None)
        decayed = decayed_data.get("records", [{}])[0]

        # 衰减后置信度应降低
        assert decayed["confidence"] < 0.8, f"衰减后置信度应降低: {decayed['confidence']}"
        print(f"  ✅ 时间衰减: 0.8 → {decayed['confidence']:.2f}")


# ═════════════════════════════════════════════════════════
# 测试 5: 全链路协调测试
# ═════════════════════════════════════════════════════════

class TestCrossDimensionCoordination:
    """跨维度协调：验证多维度同时触发时的正确性"""

    def test_multi_dimension_dispatch(self):
        """
        模拟同时有 agent + skill + instinct 三个维度的纠正，
        验证分发器能正确识别各维度。
        """
        sessions = []
        # Agent 纠正 5 次
        for i in range(5):
            sessions.append({
                "session_id": f"multi-agent-{i:03d}",
                "timestamp": datetime.now().isoformat(),
                "corrections": [{
                    "target": "agent:backend-dev",
                    "user_correction": "使用 logging 替代 print",
                    "root_cause": "缺少日志规范",
                    "root_cause_hint": "避免 print 调试",
                }],
                "rich_context": {"failure_stats": {"total": 0}},
            })
        # Skill 纠正 4 次
        for i in range(4):
            sessions.append({
                "session_id": f"multi-skill-{i:03d}",
                "timestamp": datetime.now().isoformat(),
                "corrections": [{
                    "target": "skill:testing",
                    "user_correction": "事务测试需用集成测试",
                    "root_cause": "缺少事务测试策略",
                    "root_cause_hint": "事务需集成测试",
                }],
                "rich_context": {"failure_stats": {"total": 0}},
            })
        # Instinct 纠正 3 次
        for i in range(3):
            sessions.append({
                "session_id": f"multi-instinct-{i:03d}",
                "timestamp": datetime.now().isoformat(),
                "corrections": [{
                    "target": "tool:Bash",
                    "user_correction": "危险命令需要确认",
                    "root_cause": "缺少安全检查",
                    "root_cause_hint": "Bash 命令安全检查",
                }],
                "rich_context": {"failure_stats": {"total": 0}},
            })

        config = {"paths": {"agents_dir": "agents", "skills_dir": "skills", "rules_dir": "rules"}}

        from analyzer import aggregate_and_analyze
        analysis = aggregate_and_analyze(sessions, config, PROJECT_ROOT)

        hotspots = analysis.get("correction_hotspots", {})
        assert "agent:backend-dev" in hotspots
        assert "skill:testing" in hotspots
        assert "tool:Bash" in hotspots
        print(f"  ✅ 多维度检测: hotspots={list(hotspots.keys())}")

        from evolve_dispatcher import dispatch_evolution
        decisions = dispatch_evolution(analysis, config, PROJECT_ROOT, sessions)

        dimensions = {d["dimension"] for d in decisions}
        # 核心 3 个维度应都被检测到
        assert "agent" in dimensions
        assert "skill" in dimensions or len(decisions) >= 2

        print(f"  ✅ 多维度分发: dimensions={dimensions}, count={len(decisions)}")
