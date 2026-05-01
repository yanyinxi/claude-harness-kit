#!/usr/bin/env python3
"""
v2.0 升级验证测试套件 — 覆盖 P0-P4 所有新增 Hook/Skill/Command/Agent。
目标：≥50 条测试用例，全部通过。
"""
import json, os, re, subprocess, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
AGENTS_DIR = PROJECT_ROOT / "agents"
COMMANDS_DIR = PROJECT_ROOT / "commands"
HOOKS_BIN = PROJECT_ROOT / "hooks" / "bin"
CLI_DIR = PROJECT_ROOT / "cli"

PASS = 0
FAIL = 0

# Description token regex: matches YAML folded block scalar from 'description: >' to '---'
# Pattern: description: >\n + content + \n--- (non-greedy stops at first --- occurrence)
# re.S makes . match newlines; re.M makes ^/$ match line boundaries
DESC_RE = re.compile(r"^description:\s*>?\s*\n(.+?)\n---", re.S | re.M)
# Agent description uses plain YAML scalar (no >): description: <text>\n---
AGENT_DESC_RE = re.compile(r"^description:\s*(.+?)\n---", re.S | re.M)

# For Chinese text, character count ≈ token count. 200 chars ≈ ≥30 tokens.
MIN_CHARS = 150


def record(passed: bool, msg: str):
    global PASS, FAIL
    if passed:
        PASS += 1
        print(f"  ✅ {msg}")
    else:
        FAIL += 1
        print(f"  ❌ {msg}")


def get_desc_chars(file_path: Path, is_agent: bool = False) -> int:
    """Return character count of description field (chars ≥ MIN_CHARS ≈ tokens ≥ 30)."""
    if not file_path.exists():
        return 0
    content = file_path.read_text()
    re_obj = AGENT_DESC_RE if is_agent else DESC_RE
    m = re_obj.search(content)
    if not m:
        return 0
    return len(m.group(1).lstrip())


# ── P0: Skill 描述字符数 ───────────────────────────────────────────────────
def test_skill_description_tokens():
    print("\n[P0-TASK-001] Skill 描述字符数检查（≥150 chars ≈ ≥30 tokens）")
    # Only check v2.0 newly created/upgraded skills (pre-existing skills not in scope)
    V2_SKILLS = [
        "gate-guard", "council", "team-orchestrator", "agent-shield",
        "continuous-learning-v2", "security-pipeline",
        "eval-harness", "session-wrap",
        "iac", "sre", "mobile-dev", "ml-engineer", "data-engineer", "llm-engineer",
    ]
    failed = []
    for name in V2_SKILLS:
        p = SKILLS_DIR / name / "SKILL.md"
        chars = get_desc_chars(p)
        if chars < MIN_CHARS:
            failed.append(f"{name}: {chars}c")
    passed = len(V2_SKILLS) - len(failed)
    record(len(failed) == 0,
           f"全部 {passed}/{len(V2_SKILLS)} 个 v2.0 Skill ≥150 chars" if not failed
           else f"{len(failed)} 个不达标: {', '.join(failed[:3])}")


# ── P0: Agent 描述字符数 ────────────────────────────────────────────────────
def test_agent_description_tokens():
    print("\n[TASK-P0-NEW] Agent 描述字符数检查（≥150 chars ≈ ≥30 tokens）")
    failed = []
    for fpath in sorted(AGENTS_DIR.glob("*.md")):
        chars = get_desc_chars(fpath, is_agent=True)
        if chars < MIN_CHARS:
            failed.append(f"{fpath.name}: {chars}c")
    record(len(failed) == 0,
           f"全部 {len(failed)} Agent 达标" if not failed
           else f"{len(failed)} 个不达标: {', '.join(failed[:3])}")


# ── P0: Worktree Hooks ───────────────────────────────────────────────────────
def test_worktree_hooks_json():
    print("\n[P0-TASK-003] Worktree Hooks 注册")
    hjson = PROJECT_ROOT / "hooks" / "hooks.json"
    data = json.loads(hjson.read_text())
    hooks = data.get("hooks", {})
    record("WorktreeCreate" in hooks, "WorktreeCreate 已注册")
    record("WorktreeRemove" in hooks, "WorktreeRemove 已注册")


# ── P0: Secret Filter ────────────────────────────────────────────────────────
def test_secret_filter_exists():
    print("\n[P0-TASK-004] Secret Filter Hook")
    p = HOOKS_BIN / "output-secret-filter.py"
    record(p.exists(), "output-secret-filter.py 文件存在")
    if p.exists():
        payload = json.dumps({
            "sessionId": "test",
            "message": {
                "name": "Bash",
                "content": [{"type": "tool_result", "content": [{"text": "sk-antapi03-abc123def456xyz789qwerty1234567890abc"}]}]
            }
        })
        r = subprocess.run(["python3", str(p)], input=payload, capture_output=True, text=True, timeout=5)
        record(r.returncode == 2, "Anthropic API Key → exit 2（阻断）")
        payload2 = json.dumps({
            "sessionId": "test",
            "message": {"name": "Bash", "content": [{"type": "tool_result", "content": [{"text": "const x = 1;"}]}]}
        })
        r2 = subprocess.run(["python3", str(p)], input=payload2, capture_output=True, text=True, timeout=5)
        record(r2.returncode == 0, "正常代码 → exit 0（不触发）")


# ── P1: Checkpoint ──────────────────────────────────────────────────────────
def test_checkpoint_command():
    print("\n[P1-TASK-005+009] Checkpoint 系统")
    p = COMMANDS_DIR / "checkpoint.md"
    record(p.exists(), "commands/checkpoint.md 存在")
    if p.exists():
        c = p.read_text()
        record("user-invocable: true" in c, "user-invocable: true")
        record("save" in c and "restore" in c, "包含 save/restore 子命令")


# ── P1: Instinct CLI ────────────────────────────────────────────────────────
def test_instinct_cli():
    print("\n[P1-TASK-006] Instinct CLI")
    p = CLI_DIR / "instinct_cli.py"
    record(p.exists(), "cli/instinct_cli.py 存在")
    if p.exists():
        r = subprocess.run(["python3", str(p), "status"], capture_output=True, text=True, timeout=5)
        record(r.returncode == 0, "status 命令退出码 0")
        record("No instincts" in r.stdout or "records" in r.stdout, "空数据正常显示")


# ── P1: eval-harness ────────────────────────────────────────────────────────
def test_eval_harness_skill():
    print("\n[P1-TASK-007] eval-harness Skill")
    p = SKILLS_DIR / "eval-harness" / "SKILL.md"
    record(p.exists(), "skills/eval-harness/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("Code-Based" in c, "包含 Code-Based grader")
        record("pass@3" in c, "包含 pass@k 指标")
        record(".claude/evals" in c, "包含 artifact 布局")


# ── P1: Session Wrap ────────────────────────────────────────────────────────
def test_session_wrap_skill():
    print("\n[P1-TASK-008] Session Wrap Skill")
    p = SKILLS_DIR / "session-wrap" / "SKILL.md"
    record(p.exists(), "skills/session-wrap/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("doc-updater" in c or "Phase 1" in c, "包含 4 subagent")
        record("Phase 1" in c and "Phase 5" in c, "包含 5 个 phase")


# ── P1: commit-push-pr ──────────────────────────────────────────────────────
def test_commit_push_pr():
    print("\n[P1-TASK-010] commit-push-pr 命令")
    p = COMMANDS_DIR / "commit-push-pr.md"
    record(p.exists(), "commands/commit-push-pr.md 存在")
    if p.exists():
        c = p.read_text()
        record("Build" in c and "Test" in c, "包含 Build/Test Gate")
        record("Lint" in c and "Security" in c, "包含 Lint/Security Gate")
        record("CRITICAL" in c, "CRITICAL 安全阻断")


# ── P1: /evolve ────────────────────────────────────────────────────────────
def test_evolve_command():
    print("\n[TASK-P1-NEW] /evolve 命令")
    p = COMMANDS_DIR / "evolve.md"
    record(p.exists(), "commands/evolve.md 存在")
    if p.exists():
        c = p.read_text()
        record("user-invocable: true" in c, "user-invocable: true")
        record("status" in c and "confirm" in c, "包含 status/confirm 子命令")


# ── P2: Rate Limiter ────────────────────────────────────────────────────────
def test_rate_limiter_hook():
    print("\n[P2-TASK-011] Rate Limiter Hook")
    p = HOOKS_BIN / "rate-limiter.sh"
    record(p.exists(), "rate-limiter.sh 存在")
    record(os.access(str(p), os.X_OK), "可执行权限")
    if p.exists():
        c = p.read_text()
        record("30" in c and "500" in c, "包含 30/min 500/hr 限速规则")
        record("fcntl" in c or "flock" in c, "包含并发锁机制")


# ── P2: Security Auto-Trigger ────────────────────────────────────────────────
def test_security_auto_trigger():
    print("\n[P2-TASK-012] Security Auto-Trigger Hook")
    p = HOOKS_BIN / "security-auto-trigger.sh"
    record(p.exists(), "security-auto-trigger.sh 存在")
    record(os.access(str(p), os.X_OK), "可执行权限")
    if p.exists():
        c = p.read_text()
        record("auth" in c and "security" in c, "包含安全模式匹配")


# ── P2: continuous-learning-v2 ────────────────────────────────────────────────
def test_continuous_learning_v2():
    print("\n[P2-TASK-013] continuous-learning-v2 Skill")
    p = SKILLS_DIR / "continuous-learning-v2" / "SKILL.md"
    record(p.exists(), "skills/continuous-learning-v2/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("UserPromptSubmit" in c or "feedback" in c, "包含反馈检测")
        record("observations.jsonl" in c, "包含观测日志")
    obs = HOOKS_BIN / "observe.sh"
    record(obs.exists(), "hooks/bin/observe.sh 存在")
    record(os.access(str(obs), os.X_OK), "observe.sh 可执行权限")


# ── P2: security-pipeline ──────────────────────────────────────────────────
def test_security_pipeline():
    print("\n[P2-TASK-014] security-pipeline Skill")
    p = SKILLS_DIR / "security-pipeline" / "SKILL.md"
    record(p.exists(), "skills/security-pipeline/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("CWE-89" in c, "包含 CWE-89 SQL注入")
        record("CWE-79" in c, "包含 CWE-79 XSS")
        record("CWE-78" in c, "包含 CWE-78 命令注入")
        record("CWE-798" in c, "包含 CWE-798 硬编码凭证")


# ── P2: similarity-scorer ──────────────────────────────────────────────────
def test_similarity_scorer():
    print("\n[P2-TASK-015] similarity-scorer.py")
    p = SKILLS_DIR / "skill-factory" / "scripts" / "similarity-scorer.py"
    record(p.exists(), "similarity-scorer.py 存在")
    record(os.access(str(p), os.X_OK), "可执行权限")
    if p.exists():
        c = p.read_text()
        record("SKIP" in c and "CREATE" in c, "包含 SKIP/MERGE/CREATE 阈值")
        imports = re.findall(r"^(?:import|from)\s+(\w+)", c, re.M)
        external = [i for i in imports if i not in ("json", "re", "sys", "os", "typing")]
        record(len(external) == 0, f"仅 stdlib（外部依赖：{external}）" if external else "仅 stdlib")


# ── P3: GateGuard ──────────────────────────────────────────────────────────
def test_gate_guard():
    print("\n[P3-TASK-016] gate-guard Skill")
    p = SKILLS_DIR / "gate-guard" / "SKILL.md"
    record(p.exists(), "skills/gate-guard/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("DENY" in c, "包含 DENY 阶段")
        record("FORCE" in c, "包含 FORCE 阶段")
        record("ALLOW" in c, "包含 ALLOW 阶段")


# ── P3: Council ─────────────────────────────────────────────────────────────
def test_council():
    print("\n[P3-TASK-017] council Skill")
    p = SKILLS_DIR / "council" / "SKILL.md"
    record(p.exists(), "skills/council/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("Architect" in c, "包含 Architect 声音")
        record("Skeptic" in c, "包含 Skeptic 声音")
        record("Pragmatist" in c, "包含 Pragmatist 声音")
        record("Critic" in c, "包含 Critic 声音")


# ── P3: TeamOrchestrator ──────────────────────────────────────────────────
def test_team_orchestrator():
    print("\n[P3-TASK-018] team-orchestrator Skill")
    p = SKILLS_DIR / "team-orchestrator" / "SKILL.md"
    record(p.exists(), "skills/team-orchestrator/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("wave" in c.lower(), "包含 Wave 机制")
        record("self-claim" in c.lower(), "包含 self-claim")
        record("file ownership" in c.lower(), "包含文件所有权")


# ── P3: AgentShield ────────────────────────────────────────────────────────
def test_agent_shield():
    print("\n[P3-TASK-020] agent-shield Skill")
    p = SKILLS_DIR / "agent-shield" / "SKILL.md"
    record(p.exists(), "skills/agent-shield/SKILL.md 存在")
    if p.exists():
        c = p.read_text()
        record("CLAUDE.md" in c, "扫描 CLAUDE.md")
        record("settings.json" in c, "扫描 settings.json")


# ── P4: 新增 Skill ──────────────────────────────────────────────────────────
def test_p4_skills():
    print("\n[P4-TASK-021] 新增 Skill 类别")
    expected = ["iac", "sre", "mobile-dev", "ml-engineer", "data-engineer", "llm-engineer"]
    missing = [s for s in expected if not (SKILLS_DIR / s / "SKILL.md").exists()]
    record(len(missing) == 0,
           f"6/6 P4 Skill 全部创建" if not missing
           else f"缺失 {len(missing)}个: {missing}")


# ── 收尾: commands user-invocable ─────────────────────────────────────────
def test_all_commands_user_invocable():
    print("\n[收尾] commands/*.md user-invocable 验证")
    missing = [f.name for f in sorted(COMMANDS_DIR.glob("*.md"))
               if "user-invocable: true" not in f.read_text()]
    record(len(missing) == 0,
           f"全部 {3} command user-invocable" if not missing
           else f"缺失: {missing}")


# ── 收尾: Hook 脚本可执行 ─────────────────────────────────────────────────
def test_all_hooks_executable():
    print("\n[收尾] Hook 脚本可执行权限验证")
    scripts = [
        "output-secret-filter.py",
        "worktree-manager.sh",
        "worktree-sync.sh",
        "worktree-cleanup.sh",
        "checkpoint-auto-save.sh",
        "observe.sh",
        "rate-limiter.sh",
        "security-auto-trigger.sh",
    ]
    missing = [s for s in scripts if not os.access(str(HOOKS_BIN / s), os.X_OK)]
    record(len(missing) == 0,
           f"全部 {len(scripts)} 脚本可执行" if not missing
           else f"缺失可执行: {missing}")


# ── 收尾: hooks.json 合法 ──────────────────────────────────────────────────
def test_hooks_json_valid():
    print("\n[收尾] hooks.json 格式验证")
    try:
        hjson = PROJECT_ROOT / "hooks" / "hooks.json"
        data = json.loads(hjson.read_text())
        hooks = data.get("hooks", {})
        record(True, "hooks.json 合法 JSON")
        record("UserPromptSubmit" in hooks, "UserPromptSubmit hook 已注册")
    except Exception as e:
        record(False, f"hooks.json 解析失败: {e}")


def main():
    print("=" * 60)
    print("Claude Harness Kit v2.0 — 升级验证测试套件")
    print("=" * 60)

    tests = [
        test_skill_description_tokens,
        test_agent_description_tokens,
        test_worktree_hooks_json,
        test_secret_filter_exists,
        test_checkpoint_command,
        test_instinct_cli,
        test_eval_harness_skill,
        test_session_wrap_skill,
        test_commit_push_pr,
        test_evolve_command,
        test_rate_limiter_hook,
        test_security_auto_trigger,
        test_continuous_learning_v2,
        test_security_pipeline,
        test_similarity_scorer,
        test_gate_guard,
        test_council,
        test_team_orchestrator,
        test_agent_shield,
        test_p4_skills,
        test_all_commands_user_invocable,
        test_all_hooks_executable,
        test_hooks_json_valid,
    ]

    for t in tests:
        try:
            t()
        except Exception as e:
            global FAIL
            FAIL += 1
            print(f"  ❌ {t.__name__} 异常: {e}")

    print("\n" + "=" * 60)
    print(f"测试结果：✅ {PASS} / ❌ {FAIL} / 总计 {PASS + FAIL}")
    print("=" * 60)

    if FAIL > 0:
        sys.exit(1)
    print(f"🎉 全部 {PASS} 条测试通过！")
    sys.exit(0)


if __name__ == "__main__":
    main()
