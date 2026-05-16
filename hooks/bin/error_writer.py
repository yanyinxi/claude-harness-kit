#!/usr/bin/env python3
"""
error_writer.py — CHK 错误日志写入器

将错误信息写入 .claude/data/error.jsonl，支持高并发和并发安全。

功能:
- 追加写入 error.jsonl（每行一条 JSON）
- 文件锁防止并发写入冲突
- 自动创建目录和文件
- 支持多种输入格式（JSON dict、纯文本）
"""
import fcntl
import json
import os
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Union


class ErrorType(Enum):
    """错误类型枚举"""
    TOOL_FAILURE = "tool_failure"
    COMMAND_ERROR = "command_error"
    SESSION_ERROR = "session_error"
    HOOK_ERROR = "hook_error"
    UNKNOWN = "unknown"


def get_project_root() -> Path:
    """获取项目根目录"""
    root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if root:
        return Path(root)
    return Path(__file__).resolve().parents[3]


def get_error_log_path(project_root: Optional[Path] = None) -> Path:
    """获取错误日志文件路径"""
    if project_root is None:
        project_root = get_project_root()
    # 兼容字符串输入
    if isinstance(project_root, str):
        project_root = Path(project_root)
    error_dir = project_root / ".claude" / "data"
    error_dir.mkdir(parents=True, exist_ok=True)
    return error_dir / "error.jsonl"


def _get_session_id(project_root: Optional[Path] = None) -> str:
    """获取当前会话 ID（如果环境变量未设置，则使用项目目录名作为 fallback）"""
    sid = os.environ.get("CLAUDE_SESSION_ID", "")
    if not sid and project_root:
        # fallback: 使用临时目录名作为 session_id
        sid = f"test-{project_root.name}"
    return sid


def build_error_record(
    error_type: Union[str, ErrorType] = "unknown",
    error_message: str = "",
    source: str = "",
    tool: Optional[str] = None,
    session_id: Optional[str] = None,
    tool_input: Optional[dict] = None,
    **kwargs,
) -> dict:
    """构建错误记录

    Args:
        error_type: 错误类型（tool_failure, command_error, session_error, hook_error, unknown）
        error_message: 错误消息
        source: 错误来源（文件名:行号）
        tool: 工具名称
        session_id: 会话 ID
        tool_input: 工具输入数据（用于调试）
    """
    if isinstance(error_type, ErrorType):
        error_type = error_type.value

    record = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "error": error_message,
        "source": source,
        "session_id": session_id or _get_session_id(),
    }
    if tool:
        record["tool"] = tool
    if tool_input:
        # 截断过长的 tool_input（限制为 500 字符）
        input_str = json.dumps(tool_input, ensure_ascii=False)
        if len(input_str) > 500:
            tool_input = {"_truncated": True, "_preview": input_str[:497] + "..."}
        record["context"] = {"tool_input": tool_input}
    return record


def write_error(
    record: dict,
    project_root: Optional[Path] = None,
    use_lock: bool = True,
) -> bool:
    """
    追加写入错误日志

    Args:
        record: 错误记录字典
        project_root: 项目根目录
        use_lock: 是否使用文件锁（高并发时建议开启）

    Returns:
        True 成功，False 失败
    """
    log_path = get_error_log_path(project_root)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(record, ensure_ascii=False) + "\n"

    try:
        if use_lock:
            with open(log_path, "a", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    f.write(line)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        else:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line)
        return True
    except OSError:
        return False


def get_chk_version() -> str:
    """获取 CHK 版本号"""
    try:
        root = get_project_root()
        version_file = root / "harness" / "_core" / "version.json"
        if version_file.exists():
            data = json.loads(version_file.read_text())
            return data.get("version", "unknown")
    except Exception:
        pass
    return "unknown"


def main():
    """CLI 入口：从命令行或 stdin 读取错误信息"""
    # 默认：空记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "error_type": "unknown",
        "error": "",
        "source": "",
        "session_id": _get_session_id(),
    }

    # 解析参数
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("-t", "--type"):
            record["error_type"] = sys.argv[i + 1]
            i += 2
        elif arg in ("-m", "--message"):
            record["error"] = sys.argv[i + 1]
            i += 2
        elif arg in ("-s", "--source"):
            record["source"] = sys.argv[i + 1]
            i += 2
        elif arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            # 第一个未知参数作为错误消息
            record["error"] = arg
            i += 1

    # 如果没有提供错误消息，尝试从 stdin 读取
    if not record["error"]:
        try:
            data = sys.stdin.read().strip()
            if data:
                # 尝试解析 JSON
                try:
                    info = json.loads(data)
                    record.update(info)
                except json.JSONDecodeError:
                    # 纯文本作为错误消息
                    record["error"] = data
        except KeyboardInterrupt:
            pass

    # 写入日志
    success = write_error(record)
    if success:
        print(f"✅ 错误已记录: {record['error_type']} - {record['error'][:50]}...", file=sys.stderr)
    else:
        print("❌ 写入错误日志失败", file=sys.stderr)
        sys.exit(1)


def _sanitize_tool_input(data: dict, max_length: int = 500) -> dict:
    """清理工具输入中的敏感信息和截断过长数据

    Args:
        data: 原始工具输入
        max_length: 单个字段最大长度

    Returns:
        清理后的数据
    """
    sensitive_keys = {"api_key", "password", "secret", "token", "credential"}
    sensitive_patterns = ["sk-", "sk_", "api_key", "secret", "password", "token", "credential"]
    result = {}
    for k, v in data.items():
        key_lower = k.lower()
        # 检查 key 是否敏感
        if any(sk in key_lower for sk in sensitive_keys):
            result[k] = "[REDACTED]"
        # 检查 value 是否包含敏感模式
        elif isinstance(v, str) and any(p in v.lower() for p in sensitive_patterns):
            result[k] = "[REDACTED]"
        elif isinstance(v, str) and len(v) > max_length:
            result[k] = v[:max_length] + "..."
        else:
            result[k] = v
    return result


if __name__ == "__main__":
    main()