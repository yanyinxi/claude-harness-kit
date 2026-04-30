"""性能测试 - 验证 skill 执行时间和资源消耗"""

import pytest
import time
from pathlib import Path

SKILL_NAME = "workflow-run"
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class TestPerformance:

    def test_skill_file_read_time(self):
        """验证 workflow-run 文件读取时间合理"""
        skill_file = PROJECT_ROOT / "skills" / SKILL_NAME / "SKILL.md"
        start = time.time()
        content = skill_file.read_text()
        duration = time.time() - start
        assert duration < 1.0, f"File read too slow: {{duration:.2f}}s"
        assert len(content) > 0, "Empty skill file"
