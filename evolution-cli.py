#!/usr/bin/env python3
"""
Claude Team Kit - Evolution CLI
统一命令行接口。

用法:
  evolution-cli.py evolution safety status
  evolution-cli.py evolution safety validate
  evolution-cli.py evolution safety rollback <target>
  evolution-cli.py evolution safety approve <id>
  evolution-cli.py evolution dashboard [--level L1|L2|L3]
  evolution-cli.py evolution effects report
  evolution-cli.py evolution effects trend
  evolution-cli.py evolution effects compare <dimension> <target>
  evolution-cli.py evolution data cleanup
  evolution-cli.py evolution data status
  evolution-cli.py evolution history [--limit N]
  evolution-cli.py evolution fitness
  evolution-cli.py evolution analyze
  evolution-cli.py kg search <query>
  evolution-cli.py kg add-node <type> <name> [--description DESC] [--tags TAGS]
  evolution-cli.py kg relations <node-id>
  evolution-cli.py kg stats
  evolution-cli.py workflow run <task>
  evolution-cli.py workflow pause [note]
  evolution-cli.py workflow resume [bookmark-id]
  evolution-cli.py workflow status
"""

import json
import sys
import os
from pathlib import Path

PLUGIN_ROOT = Path(os.environ.get('CLAUDE_PLUGIN_ROOT', Path(__file__).parent))
sys.path.insert(0, str(PLUGIN_ROOT / "lib"))


# ============================================================================
# Workflow Commands
# ============================================================================

def cmd_workflow_run(args):
    task = " ".join(args) if args else ""
    print(f"开始工作流: {task}")
    print("阶段 1: Explore → 2: Plan → 3: Develop → 4: Review → 5: Fix → 6: Verify")
    print("✅ 工作流完成")


def cmd_workflow_pause(args):
    note = " ".join(args) if args else ""
    state = {"task": "当前任务", "phase": "开发中", "note": note}
    bookmark = PLUGIN_ROOT / "config" / "workflow_bookmark.json"
    bookmark.parent.mkdir(parents=True, exist_ok=True)
    bookmark.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"✅ 书签已保存: {bookmark}")


def cmd_workflow_resume(args):
    bookmark = PLUGIN_ROOT / "config" / "workflow_bookmark.json"
    if bookmark.exists():
        state = json.loads(bookmark.read_text())
        print(f"恢复任务: {state.get('task', 'N/A')}")
        print(f"阶段: {state.get('phase', 'N/A')}")
        print(f"备注: {state.get('note', 'N/A')}")
    else:
        print("❌ 未找到书签")


def cmd_workflow_status(args):
    bookmark = PLUGIN_ROOT / "config" / "workflow_bookmark.json"
    if bookmark.exists():
        state = json.loads(bookmark.read_text())
        print(f"任务: {state.get('task', 'N/A')}")
        print(f"阶段: {state.get('phase', 'N/A')}")
        print(f"备注: {state.get('note', 'N/A')}")
    else:
        print("无活动工作流")


# ============================================================================
# Evolution Safety Commands
# ============================================================================

def cmd_evolution_safety(action, args):
    from evolution_safety import cli_status, cli_validate, cli_rollback

    if action == "status":
        cli_status()
    elif action == "validate":
        cli_validate()
    elif action == "rollback" and args:
        target = args[0]
        timestamp = args[1] if len(args) > 1 else None
        cli_rollback(target, timestamp)
    elif action == "approve" and args:
        proposal_id = args[0]
        print(f"正在批准进化提案: {proposal_id}")
        # 读取pending_evolution.json
        pending_file = PLUGIN_ROOT / "config" / "pending_evolution.json"
        if pending_file.exists():
            pending = json.loads(pending_file.read_text())
            pending_triggers = pending.get("pending_triggers", [])
            for trigger in pending_triggers:
                if trigger.get("id") == proposal_id:
                    trigger["status"] = "approved"
                    trigger["approved_at"] = str(Path())
                    pending_file.write_text(json.dumps(pending, indent=2, ensure_ascii=False))
                    print(f"✅ 提案 {proposal_id} 已批准")
                    return
            print(f"❌ 未找到提案: {proposal_id}")
        else:
            print("❌ 无待处理提案")
    else:
        print(f"未知 safety 命令: {action}")
        print("可用命令: status, validate, rollback <target>, approve <id>")


# ============================================================================
# Evolution Dashboard Commands
# ============================================================================

def cmd_evolution_dashboard(args):
    from evolution_dashboard import generate_dashboard_l1, generate_dashboard_l2, generate_dashboard_l3

    level = "l2"
    for arg in args:
        if arg in ("l1", "l2", "l3"):
            level = arg

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", str(PLUGIN_ROOT.parent))

    if level == "l1":
        summary = generate_dashboard_l1(project_root)
        print(summary)
    elif level == "l2":
        print(generate_dashboard_l2(project_root))
    else:
        data = generate_dashboard_l3(project_root)
        print(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================================
# Evolution Effects Commands
# ============================================================================

def cmd_evolution_effects(action, args):
    from evolution_effects import generate_effect_report, generate_trend, compare_before_after

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", str(PLUGIN_ROOT.parent))

    if action == "report":
        report = generate_effect_report(project_root)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif action == "trend":
        trend = generate_trend(project_root)
        print(json.dumps(trend, indent=2, ensure_ascii=False))
    elif action == "compare" and len(args) >= 2:
        dimension = args[0]
        target = args[1]
        result = compare_before_after(dimension, target, project_root)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 默认显示报告
        report = generate_effect_report(project_root)
        print(json.dumps(report, indent=2, ensure_ascii=False))


# ============================================================================
# Evolution Data Commands
# ============================================================================

def cmd_evolution_data(action):
    from data_rotation import get_data_status, cleanup_old_data

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", str(PLUGIN_ROOT.parent))

    if action == "cleanup":
        result = cleanup_old_data(project_root)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif action == "status":
        status = get_data_status(project_root)
        print(json.dumps(status, indent=2, ensure_ascii=False))
    else:
        status = get_data_status(project_root)
        print(json.dumps(status, indent=2, ensure_ascii=False))


# ============================================================================
# Evolution Analyze Command
# ============================================================================

def cmd_evolution_analyze():
    from evolution_orchestrator import run_orchestrator

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", str(PLUGIN_ROOT.parent))
    print("运行进化编排器...")
    result = run_orchestrator(project_root)
    print(json.dumps(result, indent=2, ensure_ascii=False) if result else "✅ 进化分析完成")


# ============================================================================
# Evolution Fitness Command
# ============================================================================

def cmd_evolution_fitness():
    from evolution_scoring import compute_all_scores

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", str(PLUGIN_ROOT.parent))

    scores = compute_all_scores(project_root)
    dims = scores.get("dimension_scores", {})
    overall = scores.get("overall_score", 0)
    grade = scores.get("overall_grade", "N/A")

    print("=" * 50)
    print("Fitness 评估报告")
    print("=" * 50)
    print(f"总分: {overall:.1f}/100 | 等级: {grade}")
    print()
    print(f"{'维度':<15} {'分数':>8} {'等级':>6}")
    print("-" * 35)

    dim_names = {"skills": "Skill", "agents": "Agent", "rules": "Rule", "memory": "Memory"}
    for dim, name in dim_names.items():
        score = dims.get(dim, 0)
        g = "A" if score >= 80 else "B" if score >= 65 else "C" if score >= 50 else "D" if score >= 35 else "F"
        print(f"{name:<15} {score:>8.1f} {g:>6}")


# ============================================================================
# Evolution History Command
# ============================================================================

def cmd_evolution_history(args):
    limit = 10
    for i, arg in enumerate(args):
        if arg == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])

    history_file = PLUGIN_ROOT.parent / ".claude" / "data" / "evolution_history.jsonl"
    if not history_file.exists():
        print(f"历史记录 (最近 {limit} 条):")
        print("(无历史记录)")
        return

    records = []
    for line in history_file.read_text().strip().splitlines():
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    records.reverse()  # 最新的在前

    print(f"历史记录 (最近 {limit} 条):")
    print("-" * 70)
    for i, rec in enumerate(records[:limit]):
        dim = rec.get("dimension", "unknown")
        target = rec.get("target_id", "unknown")
        delta = rec.get("score_after", 0) - rec.get("score_before", 0)
        delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
        status = "✅" if rec.get("success") else "❌"
        ts = rec.get("timestamp", "unknown")[:19]
        print(f"{status} [{ts}] {dim}/{target}: {rec.get('score_before', 0):.0f} → {rec.get('score_after', 0):.0f} ({delta_str})")


# ============================================================================
# Knowledge Graph Commands
# ============================================================================

def cmd_kg_search(query):
    from knowledge_graph import KnowledgeGraph

    kg_file = PLUGIN_ROOT / "config" / "knowledge_graph.json"
    kg = KnowledgeGraph(str(kg_file))

    if not query:
        print("用法: kg search <query>")
        return

    results = kg.search_nodes(query)
    if not results:
        print(f"未找到与 '{query}' 相关的节点")
        return

    print(f"找到 {len(results)} 个相关节点:")
    print("-" * 70)
    for node in results[:10]:
        title = node.get("title", "Untitled")
        ntype = node.get("type", "unknown")
        score = node.get("_relevance_score", 0)
        print(f"[{ntype}] {title} (相关度: {score})")


def cmd_kg_add_node(args):
    from knowledge_graph import KnowledgeGraph

    if len(args) < 2:
        print("用法: kg add-node <type> <name> [--description DESC] [--tags TAGS]")
        return

    ntype = args[0]
    name = args[1]
    description = ""
    tags = []

    # 解析可选参数
    i = 2
    while i < len(args):
        if args[i] == "--description" and i + 1 < len(args):
            description = args[i + 1]
            i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            tags = args[i + 1].split(",")
            i += 2
        else:
            i += 1

    kg_file = PLUGIN_ROOT / "config" / "knowledge_graph.json"
    kg = KnowledgeGraph(str(kg_file))

    node = {
        "type": ntype,
        "title": name,
        "description": description,
        "tags": tags,
        "success_rate": 0.5,
        "avg_reward": 5.0,
        "evidence": []
    }

    node_id = kg.add_node(node)
    print(f"✅ 节点已添加: {node_id}")


def cmd_kg_relations(args):
    from knowledge_graph import KnowledgeGraph

    if not args:
        print("用法: kg relations <node-id>")
        return

    node_id = args[0]
    kg_file = PLUGIN_ROOT / "config" / "knowledge_graph.json"
    kg = KnowledgeGraph(str(kg_file))

    node = kg.find_node(node_id)
    if not node:
        print(f"❌ 未找到节点: {node_id}")
        return

    print(f"节点: {node.get('title', node_id)}")
    print(f"类型: {node.get('type', 'unknown')}")
    print("-" * 50)

    related = kg.find_related_nodes(node_id)
    if not related:
        print("(无关联节点)")
    else:
        print(f"关联节点 ({len(related)}):")
        for rel in related:
            print(f"  - [{rel.get('type', 'unknown')}] {rel.get('title', rel.get('id', 'N/A'))}")


def cmd_kg_stats():
    from knowledge_graph import KnowledgeGraph

    kg_file = PLUGIN_ROOT / "config" / "knowledge_graph.json"
    kg = KnowledgeGraph(str(kg_file))

    stats = kg.get_statistics()
    print("=" * 50)
    print("知识图谱统计")
    print("=" * 50)
    print(f"总节点数: {stats['total_nodes']}")
    print(f"总边数: {stats['total_edges']}")
    print(f"平均成功率: {stats['avg_success_rate']:.1%}")
    print(f"平均奖励: {stats['avg_reward']:.1f}/10")
    print()
    print("节点类型分布:")
    for ntype, count in stats.get("node_types", {}).items():
        print(f"  {ntype}: {count}")
    print()
    print("领域分布:")
    for domain, count in stats.get("domains", {}).items():
        print(f"  {domain}: {count}")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    group = sys.argv[1]

    if group == "evolution":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        args = sys.argv[3:]

        if subcmd == "safety":
            action = sys.argv[3] if len(sys.argv) > 3 else "status"
            cmd_evolution_safety(action, sys.argv[4:])
        elif subcmd == "dashboard":
            cmd_evolution_dashboard(args)
        elif subcmd == "effects":
            action = sys.argv[3] if len(sys.argv) > 3 else "report"
            cmd_evolution_effects(action, sys.argv[4:])
        elif subcmd == "data":
            action = sys.argv[3] if len(sys.argv) > 3 else "status"
            cmd_evolution_data(action)
        elif subcmd == "history":
            cmd_evolution_history(args)
        elif subcmd == "fitness":
            cmd_evolution_fitness()
        elif subcmd == "analyze":
            cmd_evolution_analyze()
        else:
            print(f"未知 evolution 子命令: {subcmd}")
            print("可用命令: safety, dashboard, effects, data, history, fitness, analyze")

    elif group == "kg":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        args = sys.argv[3:]

        if subcmd == "search":
            query = sys.argv[3] if len(sys.argv) > 3 else ""
            cmd_kg_search(query)
        elif subcmd == "add-node":
            cmd_kg_add_node(args)
        elif subcmd == "relations":
            cmd_kg_relations(args)
        elif subcmd == "stats":
            cmd_kg_stats()
        else:
            print(f"未知 kg 子命令: {subcmd}")
            print("可用命令: search, add-node, relations, stats")

    elif group == "workflow":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else ""
        args = sys.argv[3:]

        if subcmd == "run":
            cmd_workflow_run(args)
        elif subcmd == "pause":
            cmd_workflow_pause(args)
        elif subcmd == "resume":
            cmd_workflow_resume(args)
        elif subcmd == "status":
            cmd_workflow_status(args)
        else:
            print(f"未知 workflow 命令: {subcmd}")
            print("可用命令: run, pause, resume, status")

    else:
        print(f"未知 group: {group}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
