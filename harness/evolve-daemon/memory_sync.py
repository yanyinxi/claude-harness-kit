#!/usr/bin/env python3
"""
知识同步模块 - 将进化系统产生的知识同步到 MEMORY.md

功能：
- 监听 knowledge_base.jsonl 变化
- 生成 MEMORY.md 摘要
- 追加到 MEMORY.md

使用方式：
  from harness.evolve_daemon.memory_sync import sync_to_memory, generate_memory_summary
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# 统一 sys.path 设置
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(_project_root))

logger = logging.getLogger(__name__)

# MEMORY.md 路径
MEMORY_FILE = _project_root / "harness" / "memory" / "MEMORY.md"

# 知识库文件
KNOWLEDGE_BASE_FILE = _project_root / "harness" / "knowledge" / "knowledge_base.jsonl"

# 最大同步条目数
MAX_SYNC_ENTRIES = 50


def load_knowledge_base() -> list[dict]:
    """加载知识库"""
    if not KNOWLEDGE_BASE_FILE.exists():
        logger.warning(f"知识库文件不存在: {KNOWLEDGE_BASE_FILE}")
        return []

    entries = []
    try:
        with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except OSError as e:
        logger.error(f"读取知识库失败: {e}")

    return entries


def generate_memory_summary(entry: dict) -> str:
    """
    生成记忆摘要

    Args:
        entry: 知识库条目

    Returns:
        格式化的摘要文本
    """
    kb_id = entry.get("id", "")
    summary = entry.get("summary", entry.get("root_cause", ""))[:50]
    confidence = entry.get("confidence", 0)
    category = entry.get("category", "unknown")
    updated_at = entry.get("updated_at", datetime.now().strftime("%Y-%m-%d"))

    # 获取源文件
    source_file = f"knowledge/{category}/{kb_id}.md"

    return f"| `{source_file}` | {summary}... | {confidence:.2f} | {updated_at} |"


def get_existing_sync_entries() -> set:
    """获取已同步的条目 ID"""
    if not MEMORY_FILE.exists():
        return set()

    existing = set()
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # 解析已同步的条目（格式：| `knowledge/xxx`）
            import re
            matches = re.findall(r'`(knowledge/[^`]+)`', content)
            existing.update(matches)
    except OSError:
        pass

    return existing


def sync_to_memory(max_entries: int = MAX_SYNC_ENTRIES) -> dict:
    """
    同步知识到 MEMORY.md

    Args:
        max_entries: 最大同步条目数

    Returns:
        同步结果统计
    """
    result = {
        "synced": 0,
        "skipped": 0,
        "errors": [],
    }

    # 加载知识库
    entries = load_knowledge_base()
    if not entries:
        logger.info("知识库为空，无需同步")
        return result

    # 获取已同步的条目
    existing = get_existing_sync_entries()

    # 过滤需要同步的条目（按 updated_at 降序）
    entries_to_sync = []
    for entry in entries:
        source_file = f"knowledge/{entry.get('category', 'unknown')}/{entry.get('id', '')}.md"
        if source_file not in existing:
            entries_to_sync.append(entry)

    # 限制数量
    entries_to_sync = entries_to_sync[:max_entries]

    if not entries_to_sync:
        logger.info("所有知识已同步，无需更新")
        return result

    # 读取 MEMORY.md
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError as e:
        logger.error(f"读取 MEMORY.md 失败: {e}")
        result["errors"].append(str(e))
        return result

    # 查找插入位置（## 三、进化知识 部分之后）
    insert_marker = "## 三、进化知识"
    insert_pos = content.find(insert_marker)

    if insert_pos == -1:
        # 如果没有找到，追加到文件末尾
        insert_pos = len(content)
    else:
        # 找到标记后的第一个空行之后
        insert_pos = content.find("\n\n", insert_pos)
        if insert_pos == -1:
            insert_pos = len(content)

    # 生成新的条目
    new_entries = []
    for entry in entries_to_sync:
        try:
            summary = generate_memory_summary(entry)
            new_entries.append(summary)
            result["synced"] += 1
        except Exception as e:
            result["errors"].append(str(e))
            result["skipped"] += 1

    # 构建新内容
    if new_entries:
        header = f"""
## 三、进化知识（自动生成）

| 来源文件 | 知识摘要 | 置信度 | 更新时间 |
|---------|---------|--------|----------|
"""
        entries_text = "\n".join(new_entries) + "\n"

        new_content = content[:insert_pos] + header + entries_text + content[insert_pos:]

        # 写回 MEMORY.md
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"同步成功: {result['synced']} 条")
        except OSError as e:
            logger.error(f"写入 MEMORY.md 失败: {e}")
            result["errors"].append(str(e))

    return result


def main():
    """主入口"""
    print("=== 知识同步模块测试 ===\n")

    result = sync_to_memory()
    print(f"同步结果: {result}")


if __name__ == "__main__":
    main()