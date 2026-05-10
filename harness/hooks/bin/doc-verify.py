#!/usr/bin/env python3
"""
doc-verify.py — 文档验证器
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))

AGENT_DOC_TYPES = {
    "architect": "architecture",
    "product-manager": "prd",
    "tech-lead": "architecture",
    "code-reviewer": "review",
    "security-auditor": "review",
    "test": "test",
    "qa-tester": "test",
    "backend-dev": "implementation",
    "frontend-dev": "interactive",
    "database-dev": "implementation",
    "devops": "implementation",
    "verifier": "verification",
}

def get_session_id():
    try:
        sessions_file = PROJECT_ROOT / ".claude" / "data" / "sessions.jsonl"
        if sessions_file.exists():
            lines = sessions_file.read_text(encoding="utf-8").strip().splitlines()
            if lines:
                last_session = json.loads(lines[-1])
                return last_session.get("session_id", "unknown")
    except Exception:
        pass
    return os.environ.get("CLAUDE_SESSION_ID", datetime.now().strftime("%Y%m%d%H%M%S"))

def get_agents_from_session():
    agents = []
    try:
        agent_calls_file = PROJECT_ROOT / ".claude" / "data" / "agent_calls.jsonl"
        if agent_calls_file.exists():
            lines = agent_calls_file.read_text(encoding="utf-8").strip().splitlines()
            for line in lines:
                try:
                    data = json.loads(line)
                    agent = data.get("agent", "")
                    if agent and agent not in agents:
                        agents.append(agent)
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    return agents

def check_document_output(session_id, agent, doc_type):
    artifacts_dir = PROJECT_ROOT / "docs" / "artifacts"
    if not artifacts_dir.exists():
        return {"found": False, "files": []}
    matching_files = []
    prefix = f"{session_id}_{agent}_{doc_type}"
    try:
        for f in artifacts_dir.iterdir():
            if f.is_file() and f.name.startswith(prefix):
                matching_files.append(str(f.relative_to(PROJECT_ROOT)))
    except Exception:
        pass
    return {"found": len(matching_files) > 0, "files": matching_files}

def verify_documents():
    session_id = get_session_id()
    agents_used = get_agents_from_session()
    documents = []
    missing = []
    for agent in agents_used:
        doc_type = AGENT_DOC_TYPES.get(agent)
        if not doc_type:
            continue
        check_result = check_document_output(session_id, agent, doc_type)
        if check_result["found"]:
            documents.append({"agent": agent, "type": doc_type, "files": check_result["files"]})
        else:
            missing.append({"agent": agent, "required_type": doc_type, "suggestion": f"生成 {doc_type} 类型的文档"})
    status = "OK" if not missing else "WARNING"
    return {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "agents_used": agents_used,
        "documents": documents,
        "missing": missing,
        "status": status
    }

def main():
    try:
        report = verify_documents()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["missing"]:
            missing_agents = [m["agent"] for m in report["missing"]]
            print(f"Warning: 文档缺失: {', '.join(missing_agents)}", file=sys.stderr)
        return 0 if report["status"] == "OK" else 1
    except Exception as e:
        print(json.dumps({"error": str(e), "status": "ERROR"}))
        return 0

if __name__ == "__main__":
    sys.exit(main())
