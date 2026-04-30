#!/usr/bin/env python3
"""
Instinct 自动更新器 — proposal 被 accept 或 extract_semantics 发现模式时写入 instinct-record.json。
"""
import json
import uuid
from datetime import datetime
from pathlib import Path


def load_instinct() -> dict:
    """加载或初始化 instinct-record.json"""
    path = Path(__file__).parent.parent / "instinct" / "instinct-record.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"description": "Instinct System", "version": 1, "records": []}


def save_instinct(data: dict):
    """保存 instinct-record.json"""
    path = Path(__file__).parent.parent / "instinct" / "instinct-record.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_pattern(
    pattern: str,
    correction: str,
    root_cause: str = "",
    confidence: float = 0.3,
    source: str = "auto-detected",
) -> str:
    """向 instinct-record.json 添加一条记录，返回记录 ID"""
    instinct = load_instinct()

    record_id = f"auto-{uuid.uuid4().hex[:8]}"
    record = {
        "id": record_id,
        "pattern": pattern,
        "context": "",
        "correction": correction,
        "root_cause": root_cause,
        "confidence": confidence,
        "applied_count": 0,
        "source": source,
        "created_at": datetime.now().isoformat(),
    }

    instinct.setdefault("records", []).append(record)
    save_instinct(instinct)
    return record_id


def promote_confidence(record_id: str, delta: float = 0.1):
    """增加已有记录的置信度（用于观察期后的升级）"""
    instinct = load_instinct()
    for rec in instinct.get("records", []):
        if rec.get("id") == record_id:
            rec["confidence"] = min(1.0, rec.get("confidence", 0.3) + delta)
            save_instinct(instinct)
            return