#!/usr/bin/env python3
"""
collect_error.py — CHK 错误日志收集 Hook

监控 chk 执行过程中的错误，记录到 .claude/data/error.jsonl

触发时机: PostToolUse 或 Error 事件
输入: 通过环境变量或 stdin 接收错误信息
输出: 追加写入 error.jsonl
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """获取项目根目录"""
    root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if root:
        return Path(root)
    # 默认：此脚本的父目录的父目录
    return Path(__file__).resolve().parent.parent.parent


def get_error_log_path() -> Path:
    """获取错误日志文件路径"""
    root = get_project_root()
    error_dir = root / ".claude" / "data"
    error_dir.mkdir(parents=True, exist_ok=True)
    return error_dir / "error.jsonl"


def build_error_record(
    error_type: str = "unknown",
    error_message: str = "",
    source: str = "",
    tool: Optional[str] = None,
    session_id: Optional[str] = None,
    tool_input: Optional[dict] = None,
    **kwargs,
) -> dict:
    """构建错误记录"""
    record = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "error": error_message,
        "source": source,
        "session_id": session_id or "",
        "context": {},
        "metadata": {},
    }
    if tool:
        record["tool"] = tool
    if tool_input:
        record["context"]["tool_input"] = tool_input
    # 合并其他元数据
    for k, v in kwargs.items():
        if k not in record:
            record["metadata"][k] = v
    return record


def write_error(record: dict, project_root: Optional[Path] = None) -> bool:
    """追加写入错误日志"""
    if project_root is None:
        project_root = get_project_root()

    log_path = project_root / ".claude" / "data" / "error.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def collect_from_env() -> Optional[dict]:
    """从环境变量收集错误信息"""
    error_msg = os.environ.get("CLAUDE_ERROR_MESSAGE", "")
    if not error_msg:
        return None

    return build_error_record(
        error_type=os.environ.get("CLAUDE_ERROR_TYPE", "unknown"),
        error_message=error_msg,
        source=os.environ.get("CLAUDE_ERROR_SOURCE", ""),
        tool=os.environ.get("CLAUDE_TOOL_NAME", None),
        session_id=os.environ.get("CLAUDE_SESSION_ID", None),
    )


def collect_from_stdin() -> Optional[dict]:
    """从 stdin 读取错误信息（JSON 格式）"""
    try:
        data = sys.stdin.read()
        if not data.strip():
            return None
        # 尝试解析 JSON
        info = json.loads(data)
        # 清理敏感信息
        tool_input = info.get("tool_input")
        if tool_input:
            tool_input = _sanitize_tool_input(tool_input)
        return build_error_record(
            error_type=info.get("type", "tool_failure"),
            error_message=info.get("error", info.get("message", "")),
            source=info.get("source", "hooks/bin/collect_error.py"),
            tool=info.get("tool", info.get("tool_name", None)),
            session_id=info.get("session_id", None),
            tool_input=tool_input,
        )
    except (json.JSONDecodeError, KeyboardInterrupt):
        return None


def _sanitize_tool_input(data: dict, max_length: int = 500) -> dict:
    """清理工具输入中的敏感信息和截断过长数据"""
    sensitive_keys = {"api_key", "password", "secret", "token", "credential"}
    sensitive_patterns = ["sk-", "sk_", "api_key", "secret", "password", "token", "credential"]
    result = {}
    for k, v in data.items():
        key_lower = k.lower()
        if any(sk in key_lower for sk in sensitive_keys):
            result[k] = "[REDACTED]"
        elif isinstance(v, str) and any(p in v.lower() for p in sensitive_patterns):
            result[k] = "[REDACTED]"
        elif isinstance(v, str) and len(v) > max_length:
            result[k] = v[:max_length] + "..."
        else:
            result[k] = v
    return result


def collect_tool_failure(error_message: str, tool_name: str = "") -> bool:
    """收集工具调用失败的快捷方法"""
    record = build_error_record(
        error_type="tool_failure",
        error_message=error_message,
        tool=tool_name or "unknown",
        session_id=os.environ.get("CLAUDE_SESSION_ID", ""),
    )
    return write_error(record)


def main():
    """主入口"""
    # 尝试从多个来源收集错误信息
    record = None

    # 1. 从环境变量
    record = collect_from_env()

    # 2. 从 stdin
    if not record:
        record = collect_from_stdin()

    # 3. 如果都没有，记录一个占位（方便调试）
    if not record:
        print("⚠️  未检测到错误信息，跳过记录", file=sys.stderr)
        # 输出空 JSON 表示无错误记录
        print(json.dumps({"status": "skipped", "message": "no error data"}))
        sys.exit(0)

    # 写入日志
    success = write_error(record)
    if success:
        # 输出 JSON 结果到 stdout（供测试捕获）
        print(json.dumps({"status": "ok", "collected": True, "record": record}))
    else:
        print(json.dumps({"status": "error", "collected": False, "message": "写入失败"}))
        sys.exit(1)


if __name__ == "__main__":
    main()