#!/usr/bin/env python3
"""
知识同步模块测试
"""
import sys
import unittest
from pathlib import Path

# 设置路径
_project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "harness" / "evolve-daemon"))

from memory_sync import (
    load_knowledge_base,
    generate_memory_summary,
    get_existing_sync_entries,
    sync_to_memory,
)


class TestMemorySync(unittest.TestCase):
    """知识同步模块测试"""

    def test_load_knowledge_base(self):
        """测试加载知识库"""
        entries = load_knowledge_base()
        self.assertIsInstance(entries, list)

    def test_generate_memory_summary(self):
        """测试生成记忆摘要"""
        entry = {
            "id": "test-001",
            "category": "security",
            "summary": "不要使用 eval，避免安全风险",
            "confidence": 0.85,
            "updated_at": "2026-05-17",
        }

        summary = generate_memory_summary(entry)
        self.assertIsInstance(summary, str)
        self.assertIn("knowledge/", summary)
        self.assertIn("0.85", summary)

    def test_sync_to_memory(self):
        """测试同步到 MEMORY.md"""
        result = sync_to_memory()
        self.assertIsInstance(result, dict)
        self.assertIn("synced", result)
        self.assertIn("skipped", result)
        self.assertIn("errors", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)