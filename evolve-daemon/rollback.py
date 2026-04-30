"""
Evolution Auto-Rollback — 进化自动回滚

借鉴 Harness CI/CD 的 AI-Powered Verification + Auto-Rollback 模式：
提案应用后进入观察期，指标恶化时自动回滚。

Architecture:
    evolve-daemon/proposer.py → 生成 proposal
    → 人工审批 → 应用
    → rollback.py 进入观察期
    → Day 7: 评估 → PASS (固化) or FAIL (回滚)
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path


OBSERVATION_DAYS = 7
CIRCUIT_BREAKER_LIMIT = 2  # 连续回滚次数阈值
MODULE_LOCKOUT_DAYS = 30    # 模块锁定期


def load_proposal_history(history_path: Path) -> list:
    """Load applied proposals with observation windows."""
    if not history_path.exists():
        return []
    return json.loads(history_path.read_text())


def save_proposal_history(history_path: Path, history: list):
    history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False))


def collect_metrics(proposal_id: str, metrics_dir: Path) -> dict:
    """
    Collect post-application metrics from session data.

    Returns:
        {
            "task_success_rate": float,       # 任务成功率变化
            "user_correction_rate": float,    # 用户纠正率变化
            "agent_failure_rate": float,      # Agent 调用失败率变化
            "satisfaction_score": float,      # 用户满意度 (1-5)
        }
    """
    metrics = {
        "task_success_rate": 0.0,
        "user_correction_rate": 0.0,
        "agent_failure_rate": 0.0,
        "satisfaction_score": 3.0,
    }

    # Read from sessions.jsonl (produced by collect-session.py)
    sessions_file = metrics_dir / "sessions.jsonl"
    if not sessions_file.exists():
        return metrics

    cutoff = (datetime.now() - timedelta(days=OBSERVATION_DAYS)).isoformat()
    sessions = []

    for line in sessions_file.read_text().splitlines():
        try:
            session = json.loads(line)
            if session.get("timestamp", "") >= cutoff:
                sessions.append(session)
        except json.JSONDecodeError:
            continue

    if not sessions:
        return metrics

    total = len(sessions)
    successes = sum(1 for s in sessions if s.get("status") == "success")
    corrections = sum(s.get("correction_count", 0) for s in sessions)
    failures = sum(s.get("failure_count", 0) for s in sessions)
    satisfactions = [s.get("satisfaction", 3) for s in sessions if "satisfaction" in s]

    metrics["task_success_rate"] = successes / total if total > 0 else 1.0
    metrics["user_correction_rate"] = corrections / total if total > 0 else 0.0
    metrics["agent_failure_rate"] = failures / (total * 3) if total > 0 else 0.0  # avg 3 calls/session
    metrics["satisfaction_score"] = sum(satisfactions) / len(satisfactions) if satisfactions else 3.0

    return metrics


def evaluate_proposal(proposal: dict, metrics: dict, baseline: dict) -> str:
    """
    Evaluate whether a proposal should be kept or rolled back.

    Returns: "keep" | "observe" | "rollback"
    """
    triggers = []

    # Task success rate degradation
    if baseline.get("task_success_rate", 1.0) > 0:
        delta = (metrics["task_success_rate"] - baseline["task_success_rate"]) / baseline["task_success_rate"]
        if delta < -0.10:
            triggers.append(f"任务成功率下降 {abs(delta):.0%}")

    # User correction rate increase
    if baseline.get("user_correction_rate", 0.0) >= 0:
        if metrics["user_correction_rate"] > baseline.get("user_correction_rate", 0.0) * 1.20:
            triggers.append(f"用户纠正率上升")

    # Agent failure rate increase
    if baseline.get("agent_failure_rate", 0.0) >= 0:
        if metrics["agent_failure_rate"] > baseline.get("agent_failure_rate", 0.0) * 1.05:
            triggers.append(f"Agent 失败率上升")

    # Low satisfaction
    if metrics["satisfaction_score"] < 3.0:
        triggers.append(f"用户满意度 {metrics['satisfaction_score']:.1f}/5")

    if triggers:
        return "rollback"
    if all(metrics[k] == baseline.get(k, metrics[k]) for k in metrics):
        return "observe"
    return "keep"


def run_rollback_check(proposal_path: str, metrics_dir: str, history_path: str):
    """
    Main entry point — called by daemon.py or cron.

    Checks all proposals in observation window and takes action
    if thresholds are breached.
    """
    history = load_proposal_history(Path(history_path))

    for proposal in history:
        if proposal.get("status") != "observing":
            continue

        applied_at = datetime.fromisoformat(proposal["applied_at"])
        if datetime.now() - applied_at < timedelta(days=OBSERVATION_DAYS):
            continue  # Still in observation window

        # Collect metrics since application
        metrics = collect_metrics(proposal["id"], Path(metrics_dir))
        baseline = proposal.get("baseline_metrics", {})
        decision = evaluate_proposal(proposal, metrics, baseline)

        if decision == "rollback":
            proposal["status"] = "rolled_back"
            proposal["rolled_back_at"] = datetime.now().isoformat()
            proposal["rollback_reason"] = f"Metrics degraded after {OBSERVATION_DAYS}d observation"
            print(f"  ❌ Proposal {proposal['id']}: AUTO-ROLLBACK triggered")

            # Check circuit breaker
            recent_rollbacks = [
                p for p in history
                if p.get("status") == "rolled_back"
                and datetime.fromisoformat(p["rolled_back_at"]) > datetime.now() - timedelta(days=30)
            ]
            if len(recent_rollbacks) >= CIRCUIT_BREAKER_LIMIT:
                print(f"  🔴 Circuit breaker: {len(recent_rollbacks)} rollbacks in 30d")

        elif decision == "keep":
            proposal["status"] = "consolidated"
            proposal["consolidated_at"] = datetime.now().isoformat()
            print(f"  ✅ Proposal {proposal['id']}: consolidated")

        else:
            proposal["observation_extended"] = True
            print(f"  ⏳ Proposal {proposal['id']}: extending observation")

    save_proposal_history(Path(history_path), history)
    return history


# ── CLI interface (called by daemon.py) ─────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: rollback.py <proposal_path> <metrics_dir> <history_path>")
        sys.exit(1)

    run_rollback_check(sys.argv[1], sys.argv[2], sys.argv[3])
