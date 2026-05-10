#!/usr/bin/env python3
"""
doc-verify.py — 文档验证 Hook (连字符版本别名)

验证会话期间创建/修改的文档完整性。
"""
import json
import sys
from pathlib import Path

# 添加 hooks/bin 到 sys.path
sys.path.insert(0, str(Path(__file__).parent))
from _session_utils import get_project_root, get_data_dir, load_hook_context, get_hook_event

def verify_documents():
    """验证会话期间创建的文档"""
    project_root = get_project_root()
    data_dir = get_data_dir(project_root)
    session_file = data_dir / ".session_injected.json"

    result = {
        "session_id": "",
        "timestamp": "",
        "agents_used": [],
        "documents": [],
        "missing": [],
        "status": "OK"
    }

    try:
        # 加载会话上下文
        context = load_hook_context()
        if context:
            result["session_id"] = context.get("session_id", "")

        from datetime import datetime
        result["timestamp"] = datetime.now().isoformat()

        # 读取 session_injected.json 获取文档信息
        if session_file.exists():
            session_data = json.loads(session_file.read_text(encoding="utf-8"))
            result["agents_used"] = session_data.get("agents", [])
            result["documents"] = session_data.get("docs_created", [])

            # 检查文档是否存在
            for doc in result["documents"]:
                doc_path = Path(doc)
                if not doc_path.exists():
                    result["missing"].append(doc)
                    result["status"] = "INCOMPLETE"

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)

    return result


def main():
    hook_event = get_hook_event()

    # 仅在 Stop 事件时执行
    if "Stop" not in hook_event and hook_event:
        print(json.dumps({"skipped": True, "reason": f"不是 Stop 事件: {hook_event}"}))
        return 0

    result = verify_documents()
    print(json.dumps(result, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
