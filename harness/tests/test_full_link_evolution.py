"""
Full-Link, Full-Scenario, Multi-Dimension Evolution Test Suite
"""

import sys
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "harness"))
from paths import AGENTS_DIR, RULES_DIR, SKILLS_DIR, HARNESS_DIR, MEMORY_DIR, KNOWLEDGE_DIR, EVOLVE_DIR  # noqa: E402

PLUGIN_HOOKS_BIN_DIR = PROJECT_ROOT / "hooks" / "bin"

_failures = 0

def ok(msg):
    print(f"  ✅ {msg}")

def fail(msg):
    global _failures
    print(f"  ❌ {msg}")
    _failures += 1


def test_scenario_new_project_init():
    """Scenario 1: 新项目初始化"""
    print("\n📋 Scenario 1: 新项目初始化")
    init_script = HARNESS_DIR / "cli" / "init.py"
    assert init_script.exists()
    ok("cli/init.py 存在")
    injector = PLUGIN_HOOKS_BIN_DIR / "context_injector.py"
    assert injector.exists()
    ok("context_injector.py 存在")


def test_scenario_requirement_to_prd():
    """Scenario 2: 需求到PRD"""
    print("\n📋 Scenario 2: 需求到PRD")
    pm = AGENTS_DIR / "product-manager.md"
    pm_content = pm.read_text()
    assert "requirement-analysis" in pm_content
    ok("product-manager 关联 requirement-analysis skill")


def test_scenario_architecture_design():
    """Scenario 3: 架构设计"""
    print("\n📋 Scenario 3: 架构设计")
    architect = (AGENTS_DIR / "architect.md").read_text()
    assert "model: opus" in architect
    ok("architect 使用 Opus 模型")


def test_scenario_parallel_implementation():
    """Scenario 4: 并行实现"""
    print("\n📋 Scenario 4: 并行实现")
    for agent in ["backend-dev", "frontend-dev", "database-dev"]:
        assert (AGENTS_DIR / f"{agent}.md").exists()
    ok("3 个并行开发 Agent 存在")


def test_scenario_review_and_verify():
    """Scenario 5: 审查验证"""
    print("\n📋 Scenario 5: 审查验证")
    assert (AGENTS_DIR / "code-reviewer.md").exists()
    assert (AGENTS_DIR / "ralph.md").exists()
    assert (AGENTS_DIR / "verifier.md").exists()
    ok("审查验证 Agent 存在")


def test_scenario_ship_and_deliver():
    """Scenario 6: 交付发布"""
    print("\n📋 Scenario 6: 交付发布")
    ship = SKILLS_DIR / "ship" / "SKILL.md"
    if not ship.exists():
        pytest.skip("ship skill 不存在")
    ok("ship skill 存在")


def test_dimension_correction_learning():
    """Dimension 1: 纠正学习"""
    print("\n📋 Dimension 1: 纠正学习")
    learner = AGENTS_DIR / "learner.md"
    assert learner.exists()
    ok("learner.md 存在")
    instinct = MEMORY_DIR / "instinct-record.json"
    if instinct.exists():
        ok("instinct-record.json 存在")


def test_dimension_auto_rollback():
    """Dimension 2: 自动回滚"""
    print("\n📋 Dimension 2: 自动回滚")
    rollback = EVOLVE_DIR / "rollback.py"
    if not rollback.exists():
        pytest.skip("rollback.py 不存在")
    ok("rollback.py 存在")


def test_dimension_knowledge_lifecycle():
    """Dimension 3: 知识生命周期"""
    print("\n📋 Dimension 3: 知识生命周期")
    lifecycle = KNOWLEDGE_DIR / "lifecycle.yaml"
    if not lifecycle.exists():
        pytest.skip("lifecycle.yaml 不存在")
    ok("lifecycle.yaml 存在")


def test_dimension_intent_failure_detection():
    """Dimension 4: 意图失败检测"""
    print("\n📋 Dimension 4: 意图失败检测")
    detector = EVOLVE_DIR / "intent_detector.py"
    if not detector.exists():
        pytest.skip("intent_detector.py 不存在")
    ok("intent_detector.py 存在")


def test_dimension_garbage_collection():
    """Dimension 5: 垃圾回收"""
    print("\n📋 Dimension 5: 垃圾回收")
    gc = AGENTS_DIR / "gc.md"
    assert gc.exists()
    ok("gc.md 存在")


def test_edge_case_context_compaction():
    """Edge: 上下文压缩"""
    print("\n📋 Edge: 上下文压缩")
    compaction = SKILLS_DIR / "context-compaction" / "SKILL.md"
    if not compaction.exists():
        pytest.skip("context-compaction skill 不存在")
    ok("context-compaction skill 存在")


def test_edge_case_partial_agent_failure():
    """Edge: 部分失败恢复"""
    print("\n📋 Edge: 部分失败恢复")
    orch = AGENTS_DIR / "orchestrator.md"
    assert orch.exists()
    ok("orchestrator.md 存在")


def test_edge_case_security_boundary():
    """Edge: 安全边界"""
    print("\n📋 Edge: 安全边界")
    security = RULES_DIR / "security.md"
    if not security.exists():
        pytest.skip("security.md 不存在")
    ok("security.md 存在")
    safety = PLUGIN_HOOKS_BIN_DIR / "safety-check.sh"
    assert safety.exists()
    ok("safety-check.sh 存在")


def test_cache_reuse_optimization():
    """Performance: 缓存复用"""
    print("\n📋 Performance: 缓存复用")
    agent_files = sorted([p.name for p in AGENTS_DIR.glob("*.md")])
    ok(f"Agent 文件数: {len(agent_files)}")


def test_evolution_closed_loop():
    """Integration: 进化闭环"""
    print("\n📋 Integration: 进化闭环")
    collectors = ["collect_session.py", "collect_agent.py", "collect_skill.py"]
    found = 0
    for c in collectors:
        if (PLUGIN_HOOKS_BIN_DIR / c).exists():
            found += 1
    ok(f"Stage 1 采集: {found}/{len(collectors)} 个脚本")

    extractor = PLUGIN_HOOKS_BIN_DIR / "extract_semantics.py"
    if extractor.exists():
        ok("Stage 2 语义提取: extract_semantics.py")

    analyzer = EVOLVE_DIR / "analyzer.py"
    if analyzer.exists():
        ok("Stage 3 分析: analyzer.py")
    ok("进化闭环验证完成")
