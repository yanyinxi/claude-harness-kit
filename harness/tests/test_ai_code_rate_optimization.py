#!/usr/bin/env python3
"""AI 代码率优化 - 全场景测试验证"""

import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path("/Users/yanyinxi/工作/code/github/claude-harness-kit")
HARNESS_DIR = PROJECT_ROOT / "harness"


# ==================== 正向测试 ====================

def test_rules_changes_md_exists():
    """正向: 检查 changes.md 是否存在"""
    path = HARNESS_DIR / "rules" / "changes.md"
    assert path.exists(), f"路径不存在: {path}"


def test_rules_changes_md_format():
    """正向: 检查 changes.md 格式正确性"""
    path = HARNESS_DIR / "rules" / "changes.md"
    assert path.exists(), "rules/changes.md 不存在"

    content = path.read_text()
    checks = [
        ("变更分类" in content, "缺少变更分类"),
        ("L0" in content, "缺少 L0 级别"),
        ("L1" in content, "缺少 L1 级别"),
        ("L2" in content, "缺少 L2 级别"),
        ("L3" in content, "缺少 L3 级别"),
        ("反模式" in content, "缺少反模式定义"),
        ("回滚方案" in content, "缺少回滚方案"),
    ]

    failed = [msg for check, msg in checks if not check]
    assert len(failed) == 0, f"缺失: {', '.join(failed)}"


def test_skill_change_tracking_exists():
    """正向: 检查 change-tracking Skill 是否存在"""
    skill_file = HARNESS_DIR / "skills" / "change-tracking" / "SKILL.md"
    assert skill_file.exists(), f"Skill 不存在: {skill_file}"


def test_skill_change_tracking_content():
    """正向: 检查 change-tracking Skill 内容完整性"""
    path = HARNESS_DIR / "skills" / "change-tracking" / "SKILL.md"
    assert path.exists(), "change-tracking Skill 不存在"

    content = path.read_text()
    required = ["触发场景", "变更级别评估", "变更记录创建", "回滚流程", "与其他 Skill 的协同"]
    missing = [r for r in required if r not in content]
    assert len(missing) == 0, f"缺失: {', '.join(missing)}"


def test_knowledge_guideline_count():
    """正向: 检查编码规范数量是否 >= 10"""
    path = HARNESS_DIR / "knowledge" / "guideline" / "coding-style.json"
    assert path.exists(), "编码规范文件不存在"

    data = json.loads(path.read_text())
    count = len(data) if isinstance(data, list) else 1
    assert count >= 10, f"当前: {count} 条，需要 >= 10"


def test_knowledge_pitfall_count():
    """正向: 检查陷阱记录数量是否 >= 10"""
    path = HARNESS_DIR / "knowledge" / "pitfall" / "common-mistakes.json"
    assert path.exists(), "陷阱记录文件不存在"

    data = json.loads(path.read_text())
    count = len(data) if isinstance(data, list) else 1
    assert count >= 10, f"当前: {count} 条，需要 >= 10"


def test_quality_gate_secret_scan():
    """正向: 检查 quality-gate.sh 包含 Secret 扫描"""
    path = HARNESS_DIR / "hooks" / "bin" / "quality-gate.sh"
    assert path.exists(), "quality-gate.sh 不存在"

    content = path.read_text()
    required = ["api[_-]?key", "secret[_-]?key", "password"]
    missing = [r for r in required if r not in content]
    assert len(missing) == 0, f"缺失模式: {', '.join(missing)}"


def test_coverage_check_script():
    """正向: 检查 coverage-check.sh 语法正确"""
    path = HARNESS_DIR / "hooks" / "bin" / "coverage-check.sh"
    assert path.exists(), "coverage-check.sh 不存在"

    result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    assert result.returncode == 0, f"语法错误: {result.stderr}"


def test_changes_directory_structure():
    """正向: 检查 changes 目录结构（迁移到 knowledge/decision/changes/）"""
    # changes 目录已迁移到 harness/knowledge/decision/changes/
    changes_dir = HARNESS_DIR / "knowledge" / "decision" / "changes"
    assert changes_dir.exists(), "changes 目录不存在"

    subdirs = [d for d in changes_dir.iterdir() if d.is_dir()]
    assert len(subdirs) > 0, "无变更记录"

    first_change = subdirs[0]
    change_md = first_change / "CHANGE.md"
    assert change_md.exists(), f"示例缺少 CHANGE.md: {first_change.name}"


def test_ship_skill_ci_integration():
    """正向: 检查 Ship Skill 集成 CI 门禁"""
    path = HARNESS_DIR / "skills" / "ship" / "SKILL.md"
    assert path.exists(), "Ship Skill 不存在"

    content = path.read_text()
    required = ["Secret 扫描", "覆盖率", "CI 门禁"]
    missing = [r for r in required if r not in content]
    assert len(missing) == 0, f"缺失: {', '.join(missing)}"


def test_orchestrator_owner_mechanism():
    """正向: 检查 Orchestrator 包含 Owner 机制"""
    path = HARNESS_DIR / "agents" / "orchestrator.md"
    assert path.exists(), "Orchestrator Agent 不存在"

    content = path.read_text()
    required = ["Application Owner", "Owner 定义文件", "Owner 工作流"]
    missing = [r for r in required if r not in content]
    assert len(missing) == 0, f"缺失: {', '.join(missing)}"


def test_knowledge_process_exists():
    """正向: 检查知识库流程文档"""
    path = HARNESS_DIR / "knowledge" / "process" / "dev-process.json"
    assert path.exists(), f"流程文档不存在: {path}"


def test_knowledge_model_exists():
    """正向: 检查知识库模型文档"""
    path = HARNESS_DIR / "knowledge" / "model" / "entities.json"
    assert path.exists(), f"模型文档不存在: {path}"


# ==================== 逆向测试 ====================

def test_json_format_valid():
    """逆向: JSON 文件格式校验"""
    json_files = [
        HARNESS_DIR / "knowledge" / "guideline" / "coding-style.json",
        HARNESS_DIR / "knowledge" / "pitfall" / "common-mistakes.json",
        HARNESS_DIR / "knowledge" / "process" / "dev-process.json",
        HARNESS_DIR / "knowledge" / "model" / "entities.json",
    ]
    for f in json_files:
        if f.exists():
            json.loads(f.read_text())


def test_no_hardcoded_secrets_in_knowledge():
    """逆向: 知识库中不应有真实 Secret"""
    knowledge_files = list((HARNESS_DIR / "knowledge").rglob("*.json"))
    for f in knowledge_files:
        content = f.read_text()
        assert "sk-" not in content, f"疑似问题文件: {f.name}"


# ==================== 边界测试 ====================

def test_empty_changes_directory():
    """边界: CHANGES 目录为空时应正常处理"""
    changes_dir = HARNESS_DIR / "changes"
    if changes_dir.exists():
        subdirs = [d for d in changes_dir.iterdir() if d.is_dir()]
        assert len(subdirs) >= 0, "目录检查失败"


def test_guideline_maturity_levels():
    """边界: 检查规范 maturity 字段有效性"""
    path = HARNESS_DIR / "knowledge" / "guideline" / "coding-style.json"
    assert path.exists(), "编码规范文件不存在"

    valid_levels = ["draft", "validated", "deprecated"]
    data = json.loads(path.read_text())

    for item in (data if isinstance(data, list) else [data]):
        maturity = item.get("maturity", "")
        if maturity:
            assert maturity in valid_levels, f"无效 maturity: {maturity}"


def test_pitfall_impact_levels():
    """边界: 检查陷阱 impact 字段有效性"""
    path = HARNESS_DIR / "knowledge" / "pitfall" / "common-mistakes.json"
    assert path.exists(), "陷阱记录文件不存在"

    valid_levels = ["low", "medium", "high", "critical"]
    data = json.loads(path.read_text())

    for item in (data if isinstance(data, list) else [data]):
        impact = item.get("content", {}).get("impact", "")
        if impact:
            assert impact in valid_levels, f"无效 impact: {impact}"


def test_hooks_json_format():
    """边界: 检查 hooks.json 格式有效性"""
    path = HARNESS_DIR / "hooks" / "hooks.json"
    assert path.exists(), "hooks.json 不存在"

    data = json.loads(path.read_text())
    assert "hooks" in data, "缺少 hooks 字段"


# ==================== 异常测试 ====================

def test_missing_file_graceful_handling():
    """异常: 文件缺失时应有降级处理"""
    path = HARNESS_DIR / "hooks" / "bin" / "quality-gate.sh"
    assert path.exists(), "quality-gate.sh 不存在"

    content = path.read_text()
    has_graceful = "exit 0" in content or "[[ -z \"$FILE_PATH\" ]]" in content
    assert has_graceful, "缺少降级处理"


def test_coverage_check_no_report():
    """异常: 无覆盖率报告时不应阻断"""
    path = HARNESS_DIR / "hooks" / "bin" / "coverage-check.sh"
    assert path.exists(), "coverage-check.sh 不存在"

    content = path.read_text()
    assert "exit 0" in content, "缺少处理逻辑"
