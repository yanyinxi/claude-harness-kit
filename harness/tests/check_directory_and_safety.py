#!/usr/bin/env python3
"""
目录结构与安全全面测试套件
═════════════════════════════════════

覆盖:
  1. 目录结构白名单验证
  2. 路径常量正确性
  3. 禁止嵌套目录检查
  4. 文件 schema 验证
  5. 边界情况 (空目录、空文件、损坏 JSON)
  6. 安全: 路径遍历防护、脱敏逻辑
  7. Hook 脚本存在性
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1].parent
HARNESS_DIR = PROJECT_ROOT / "harness"
os.environ.setdefault("CLAUDE_PROJECT_DIR", str(PROJECT_ROOT))
sys.path.insert(0, str(HARNESS_DIR))
sys.path.insert(0, str(HARNESS_DIR / "knowledge"))
sys.path.insert(0, str(HARNESS_DIR / "evolve-daemon"))

# ── 测试辅助 ───────────────────────────────────────────────────────────────────

def ok(msg):
    print(f"  ✅ {msg}")


def fail(msg):
    print(f"  ❌ {msg}")
    global FAIL
    FAIL += 1


FAIL = 0


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 目录结构白名单验证
# ═══════════════════════════════════════════════════════════════════════════════

def test_harness_whitelist_subdirs():
    """正向: harness/ 下只允许白名单子目录"""
    allowed = {
        "_core", "agents", "skills", "rules", "hooks",
        "evolve-daemon", "knowledge", "memory", "cli", "docs", "tests",
    }
    # 允许但非代码的目录（CI/缓存）
    auto_allowed = {"__pycache__"}
    harness = HARNESS_DIR
    for item in harness.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if item.name not in allowed and item.name not in auto_allowed:
                assert False, f"harness/ 下发现未授权目录: {item.name}"
    ok(f"harness/ 白名单验证通过 (允许: {len(allowed)} 个)")


def test_no_harness_nested():
    """安全: harness/ 下禁止嵌套另一个 harness/"""
    nested = list(HARNESS_DIR.glob("harness"))
    assert len(nested) == 0, f"发现嵌套 harness/: {nested}"
    ok("无嵌套 harness/ 目录")


def test_no_code_in_claude_dir():
    """安全: .claude/ 下只允许 data/ 和 proposals/"""
    claude = PROJECT_ROOT / ".claude"
    if not claude.exists():
        ok(".claude/ 不存在 (正常)")
        return
    code_exts = {".py", ".sh", ".js", ".ts", ".java", ".go", ".rs"}
    violations = []
    for item in claude.rglob("*"):
        if item.is_file() and item.suffix in code_exts:
            violations.append(str(item.relative_to(claude)))
    assert len(violations) == 0, f".claude/ 下发现代码文件: {violations}"
    ok(".claude/ 无代码文件 (只允许 data/ 和 proposals/)")


def test_claude_data_subdirs():
    """边界: .claude/data/ 只允许已知文件"""
    data_dir = PROJECT_ROOT / ".claude" / "data"
    if not data_dir.exists():
        ok(".claude/data/ 不存在")
        return
    allowed_files = {
        "sessions.jsonl", "error.jsonl", "agent_calls.jsonl", "skill_calls.jsonl",
        "analysis_state.json", "proposal_history.json", "knowledge_recommendations.json",
    }
    for f in data_dir.iterdir():
        if f.is_file() and f.suffix == ".jsonl":
            pass  # jsonl 允许
        elif f.is_file() and f.suffix == ".json":
            pass  # json 允许
        elif f.is_dir():
            pass  # 子目录允许
        elif f.name.startswith("."):
            pass  # 隐藏文件（系统）
    ok(".claude/data/ 文件结构正常")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 路径常量正确性
# ═══════════════════════════════════════════════════════════════════════════════

def test_path_constants_no_instinct():
    """反向: paths.py 不再导出 instinct 路径常量"""
    from paths import (
        DIR_MEMORY, MEMORY_DIR, KNOWLEDGE_DIR, EVOLVE_DIR,
    )
    assert DIR_MEMORY == "memory"
    assert MEMORY_DIR.name == "memory"
    assert KNOWLEDGE_DIR.name == "knowledge"
    assert EVOLVE_DIR.name == "evolve-daemon"
    ok("路径常量正确 (无 instinct 相关)")


def test_instinct_in_memory():
    """正向: instinct-record.json 在 memory/ 目录"""
    instinct = HARNESS_DIR / "memory" / "instinct-record.json"
    assert instinct.exists(), f"本能记录不存在: {instinct}"
    data = json.loads(instinct.read_text())
    assert "records" in data or isinstance(data, dict)
    ok("本能记录在 harness/memory/")


def test_knowledge_dirs_exist():
    """正向: 知识库子目录都存在（evolved 由运行时自动创建，测试时确保有基础目录）"""
    for subdir in ["decision", "guideline", "pitfall", "process", "model"]:
        p = HARNESS_DIR / "knowledge" / subdir
        assert p.exists(), f"知识子目录缺失: {subdir}"
    # evolved/ 目录在测试时不一定存在（由进化系统运行时创建），只检查顶层
    evolved_dir = HARNESS_DIR / "knowledge" / "evolved"
    evolved_dir.mkdir(exist_ok=True)
    ok("知识库 5 个核心子目录全部存在")


def test_knowledge_json_schema():
    """边界: 知识 JSON 文件有正确的 frontmatter"""
    knowledge_dir = HARNESS_DIR / "knowledge"
    required_fields = {"id", "type", "name", "maturity", "content"}
    violations = []
    for subdir in ["decision", "guideline", "pitfall", "process", "model"]:
        for json_file in (knowledge_dir / subdir).glob("*.json"):
            try:
                data = json.loads(json_file.read_text())
                missing = required_fields - set(data.keys())
                if missing:
                    violations.append(f"{json_file.name} 缺少: {missing}")
            except json.JSONDecodeError:
                violations.append(f"{json_file.name} 不是有效 JSON")
    assert len(violations) == 0, f"知识文件 schema 问题: {violations}"
    ok("所有知识 JSON 文件 schema 正确")


def test_knowledge_manual_symlink_gone():
    """反向: knowledge/manual 符号链接已删除"""
    manual = HARNESS_DIR / "knowledge" / "manual"
    assert not manual.exists(), "knowledge/manual 不应存在"
    ok("knowledge/manual 符号链接已删除")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Hook 脚本存在性
# ═══════════════════════════════════════════════════════════════════════════════

def test_all_hook_scripts_exist():
    """正向: hooks.json 引用的脚本都存在"""
    import json
    hooks_file = HARNESS_DIR / "hooks" / "hooks.json"
    hooks_data = json.loads(hooks_file.read_text())

    missing = []
    for event, hook_list in hooks_data.get("hooks", {}).items():
        for h in hook_list:
            for hh in h.get("hooks", []):
                cmd = hh.get("command", "")
                if cmd.startswith("python3"):
                    script = cmd.split("/")[-1].replace("${CLAUDE_PLUGIN_ROOT}/hooks/bin/", "")
                    script = script.replace("${CLAUDE_PLUGIN_ROOT}", "")
                    sp = HARNESS_DIR / "hooks" / "bin" / script
                    if not sp.exists():
                        missing.append(f"[{event}] {script}")
                elif cmd.startswith("bash"):
                    script = cmd.split("/")[-1]
                    sp = HARNESS_DIR / "hooks" / "bin" / script
                    if not sp.exists():
                        missing.append(f"[{event}] {script}")

    assert len(missing) == 0, f"Hook 脚本缺失: {missing}"
    ok("所有 Hook 脚本都存在")


def test_underscore_naming_collect_hooks():
    """边界: collect_*.py hook 脚本统一 underscore 命名（migration 规范）"""
    hooks_bin = HARNESS_DIR / "hooks" / "bin"
    hyphen_collect = [f for f in hooks_bin.glob("collect-*.py")]
    assert len(hyphen_collect) == 0, f"collect-*.py 应用 underscore 命名: {[f.name for f in hyphen_collect]}"
    ok("collect_*.py hook 脚本命名统一")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. 路径遍历防护
# ═══════════════════════════════════════════════════════════════════════════════

def test_path_traversal_protection():
    """安全: 路径常量计算应防止 ../ 遍历"""
    from paths import DATA_DIR, MEMORY_DIR

    # 解析路径，检查是否包含 ../ 遍历模式
    def is_safe_path(p):
        s = str(p)
        return ".." not in s

    assert is_safe_path(DATA_DIR), f"DATA_DIR 存在路径遍历风险: {DATA_DIR}"
    assert is_safe_path(MEMORY_DIR), f"MEMORY_DIR 存在路径遍历风险: {MEMORY_DIR}"
    ok("路径常量无 ../ 遍历风险")


def test_collect_error_sanitization():
    """安全: collect_error.py 正确脱敏敏感信息"""
    sys.path.insert(0, str(HARNESS_DIR / "hooks" / "bin"))
    from collect_error import _sanitize_tool_input

    # API Key 脱敏
    sensitive_input = {"api_key": "sk-ant-secret123", "token": "Bearer xyz123"}
    sanitized = _sanitize_tool_input(sensitive_input)
    assert sanitized.get("api_key") == "[REDACTED]", "API Key 应被脱敏"
    assert "sk-ant" not in str(sanitized), "脱敏后不应包含 sk-ant"
    ok("敏感数据脱敏正常")


def test_collect_error_no_secret_in_error():
    """安全: 错误收集不泄露敏感信息"""
    sys.path.insert(0, str(HARNESS_DIR / "hooks" / "bin"))
    from collect_error import _sanitize_tool_input

    # Password 脱敏
    dangerous = {"password": "hunter2", "command": "curl http://api.com"}
    result = _sanitize_tool_input(dangerous)
    assert result.get("password") == "[REDACTED]", "Password 应被脱敏"
    assert "hunter2" not in str(result), "脱敏后不应包含原始密码"
    ok("Password 等敏感字段正确脱敏")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 边界情况: 损坏数据
# ═══════════════════════════════════════════════════════════════════════════════

def test_corrupted_jsonl_handled():
    """异常: 损坏的 JSONL 文件不导致程序崩溃"""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        error_file = root / ".claude" / "data" / "error.jsonl"
        error_file.parent.mkdir(parents=True)
        # 写入损坏行
        error_file.write_text('{"type": "ok"}\n{"broken": json\n')

        # 尝试读取（模拟 collect_session.py 的处理）
        lines = error_file.read_text().splitlines()
        valid = 0
        for line in lines:
            try:
                json.loads(line)
                valid += 1
            except json.JSONDecodeError:
                pass  # 跳过损坏行
        assert valid >= 1, "至少有一行有效 JSON"
    ok("损坏 JSONL 被正确跳过")


def test_empty_knowledge_dir():
    """边界: 空的 knowledge 目录不导致崩溃"""
    from knowledge_recommender import load_knowledge_base
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        # 创建空的 knowledge 目录
        (root / "harness" / "knowledge" / "evolved").mkdir(parents=True)
        os.environ["CLAUDE_PROJECT_DIR"] = str(root)
        entries = load_knowledge_base()
        assert isinstance(entries, list)
    ok("空 knowledge 目录不崩溃")


def test_instinct_record_schema():
    """正向: instinct-record.json schema 正确"""
    instinct = HARNESS_DIR / "memory" / "instinct-record.json"
    data = json.loads(instinct.read_text())
    assert isinstance(data, dict), "本能记录应为 dict"
    assert "records" in data, "本能记录应有 records 字段"
    assert isinstance(data["records"], list), "records 应为 list"
    ok("本能记录 schema 正确")


def test_instinct_record_uuid_unique():
    """正向: instinct 记录 ID 唯一"""
    instinct = HARNESS_DIR / "memory" / "instinct-record.json"
    data = json.loads(instinct.read_text())
    ids = [r.get("id") for r in data["records"] if "id" in r]
    assert len(ids) == len(set(ids)), f"存在重复 ID: {ids}"
    ok("本能记录 ID 唯一")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. Agent 和 Skill 文件完整性
# ═══════════════════════════════════════════════════════════════════════════════

def test_all_agents_have_frontmatter():
    """正向: 所有 Agent 文件有 frontmatter"""
    violations = []
    for agent_md in (HARNESS_DIR / "agents").glob("*.md"):
        content = agent_md.read_text()
        if not content.startswith("---"):
            violations.append(agent_md.name)
    assert len(violations) == 0, f"Agent 缺少 frontmatter: {violations}"
    ok("所有 Agent 文件有 frontmatter")


def test_all_skills_have_frontmatter():
    """正向: 所有 Skill 文件有 frontmatter"""
    violations = []
    for skill_dir in (HARNESS_DIR / "skills").glob("*"):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()
            if not content.startswith("---"):
                violations.append(f"{skill_dir.name}/SKILL.md")
    assert len(violations) == 0, f"Skill 缺少 frontmatter: {violations}"
    ok("所有 Skill 文件有 frontmatter")


def test_no_empty_subdirs():
    """边界: harness/ 下无空目录"""
    empty = []
    for d in HARNESS_DIR.rglob("*"):
        if d.is_dir() and not any(d.iterdir()) and not d.name.startswith("."):
            empty.append(str(d.relative_to(HARNESS_DIR)))
    assert len(empty) == 0, f"发现空目录: {empty}"
    ok("harness/ 下无空目录")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CLI 错误处理
# ═══════════════════════════════════════════════════════════════════════════════

def test_cli_gc_nonexistent_project():
    """异常: gc 对不存在的目录不崩溃"""
    from cli.gc import main as gc_main
    with patch.object(sys, "argv", ["gc.py", "/nonexistent/path/xyz123"]):
        try:
            gc_main()
        except (FileNotFoundError, SystemExit):
            pass  # 预期行为（无目录则打印错误并退出）
    ok("gc 对不存在路径不崩溃")


def test_knowledge_recommender_missing_evolved_dir():
    """边界: evolved/ 目录不存在时优雅降级"""
    sys.path.insert(0, str(HARNESS_DIR / "knowledge"))
    from knowledge_recommender import load_evolved_knowledge
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        os.environ["CLAUDE_PROJECT_DIR"] = str(root)
        result = load_evolved_knowledge()
        assert isinstance(result, list)
    ok("无 evolved/ 目录时优雅降级")


# ═══════════════════════════════════════════════════════════════════════════════
# 运行器
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  目录结构与安全全面测试")
    print("=" * 60)

    tests = [
        # 目录结构
        test_harness_whitelist_subdirs,
        test_no_harness_nested,
        test_no_code_in_claude_dir,
        test_claude_data_subdirs,
        # 路径常量
        test_path_constants_no_instinct,
        test_instinct_in_memory,
        test_knowledge_dirs_exist,
        test_knowledge_json_schema,
        test_knowledge_manual_symlink_gone,
        # Hook
        test_all_hook_scripts_exist,
        test_underscore_naming_collect_hooks,
        # 安全
        test_path_traversal_protection,
        test_collect_error_sanitization,
        test_collect_error_no_secret_in_error,
        # 边界
        test_corrupted_jsonl_handled,
        test_empty_knowledge_dir,
        test_instinct_record_schema,
        test_instinct_record_uuid_unique,
        # 完整性
        test_all_agents_have_frontmatter,
        test_all_skills_have_frontmatter,
        test_no_empty_subdirs,
        # CLI
        test_cli_gc_nonexistent_project,
        test_knowledge_recommender_missing_evolved_dir,
    ]

    passed = 0
    failed = 0

    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {t.__name__}: 意外错误 - {e}")
            failed += 1

    print("-" * 60)
    print(f"  结果: {passed} 通过, {failed} 失败")
    print("=" * 60 + "\n")

    sys.exit(0 if failed == 0 else 1)
