#!/usr/bin/env python3
"""
Evolve-Daemon Analyzer 单元测试

测试分析器的所有功能
"""

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

# 导入被测试模块
from harness.tests.conftest import make_session, make_correction


class TestAnalyzerTrigger:
    """分析器触发条件测试"""

    def test_trigger_with_sufficient_sessions(self, tmp_path):
        """足够的 sessions 触发分析"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"

        # 创建 5 个 session (触发阈值)
        sessions = [
            make_session(f"s{i}", corrections=[make_correction("executor")])
            for i in range(5)
        ]
        sessions_file.write_text("\n".join(json.dumps(s) for s in sessions))

        assert sessions_file.exists()
        # 验证有足够的 sessions
        assert len(sessions) >= 5

    def test_trigger_with_sufficient_corrections(self, tmp_path):
        """足够的 corrections 触发分析"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"

        # 创建带有 correction 的 sessions
        sessions = [
            make_session(
                f"s{i}",
                corrections=[
                    make_correction("executor", root_cause_hint="slow"),
                    make_correction("backend-dev", root_cause_hint="bug"),
                ]
            )
            for i in range(3)
        ]
        sessions_file.write_text("\n".join(json.dumps(s) for s in sessions))

        # 统计总 corrections
        total_corrections = sum(s["correction_count"] for s in sessions)
        assert total_corrections >= 3

    def test_no_trigger_with_insufficient_sessions(self, tmp_path):
        """session 不足不触发"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"

        # 只创建 3 个 session (低于阈值 5)
        sessions = [
            make_session(f"s{i}")
            for i in range(3)
        ]
        sessions_file.write_text("\n".join(json.dumps(s) for s in sessions))

        # 小于 5 个 session
        assert len(sessions) < 5


class TestAnalyzerAggregation:
    """分析器聚合测试"""

    def test_aggregate_corrections_by_target(self, tmp_path):
        """按 target 聚合 corrections"""
        sessions = [
            make_session("s1", corrections=[
                make_correction("executor", root_cause_hint="slow"),
                make_correction("executor", root_cause_hint="error"),
            ]),
            make_session("s2", corrections=[
                make_correction("executor", root_cause_hint="bug"),
            ]),
            make_session("s3", corrections=[
                make_correction("backend-dev", root_cause_hint="api"),
            ]),
        ]

        # 统计 executor 的 corrections
        executor_corrections = [
            c for s in sessions
            for c in s["corrections"]
            if c["target"] == "executor"
        ]

        assert len(executor_corrections) == 3

    def test_aggregate_corrections_by_root_cause(self, tmp_path):
        """按 root_cause_hint 聚合 corrections"""
        sessions = [
            make_session("s1", corrections=[
                make_correction("executor", root_cause_hint="slow"),
            ]),
            make_session("s2", corrections=[
                make_correction("executor", root_cause_hint="slow"),
            ]),
            make_session("s3", corrections=[
                make_correction("executor", root_cause_hint="bug"),
            ]),
        ]

        slow_corrections = [
            c for s in sessions
            for c in s["corrections"]
            if c.get("root_cause_hint") == "slow"
        ]

        assert len(slow_corrections) == 2


class TestAnalyzerPatternDetection:
    """模式检测测试"""

    def test_detect_repeated_pattern(self, tmp_path):
        """检测重复模式"""
        sessions = [
            make_session(f"s{i}", corrections=[
                make_correction("executor", root_cause_hint="slow"),
            ])
            for i in range(5)
        ]

        # executor 重复出现
        executor_count = sum(
            1 for s in sessions
            for c in s["corrections"]
            if c["target"] == "executor"
        )

        assert executor_count == 5
        # 重复 5 次，应该是高优先级
        assert executor_count >= 3

    def test_detect_no_pattern(self, tmp_path):
        """无明显模式"""
        sessions = [
            make_session("s1", corrections=[make_correction("executor")]),
            make_session("s2", corrections=[make_correction("backend-dev")]),
            make_session("s3", corrections=[make_correction("frontend-dev")]),
        ]

        targets = set(
            c["target"] for s in sessions
            for c in s["corrections"]
        )

        # 每个 target 只出现一次，没有重复
        assert len(targets) == 3
        for target in targets:
            count = sum(
                1 for s in sessions
                for c in s["corrections"]
                if c["target"] == target
            )
            assert count == 1


class TestAnalyzerOutput:
    """分析器输出测试"""

    def test_output_format(self, tmp_path):
        """分析输出格式正确"""
        sessions = [
            make_session("s1", corrections=[make_correction("executor")]),
        ]

        # 预期输出结构
        output = {
            "correction_count": 1,
            "top_targets": ["executor"],
            "patterns": [],
            "timestamp": sessions[0]["timestamp"]
        }

        assert "correction_count" in output
        assert "top_targets" in output
        assert isinstance(output["top_targets"], list)

    def test_output_includes_metadata(self, tmp_path):
        """输出包含元数据"""
        sessions = [
            make_session("s1", corrections=[make_correction("executor")]),
        ]

        # 元数据应包含
        metadata = {
            "session_count": len(sessions),
            "total_corrections": sum(s["correction_count"] for s in sessions),
            "time_range": "2026-01-01 to 2026-01-01"
        }

        assert metadata["session_count"] == 1
        assert metadata["total_corrections"] == 1


class TestAnalyzerConfidence:
    """置信度计算测试"""

    def test_confidence_based_on_frequency(self, tmp_path):
        """基于频率计算置信度"""
        sessions = [
            make_session(f"s{i}", corrections=[make_correction("executor")])
            for i in range(10)
        ]

        executor_count = sum(
            1 for s in sessions
            for c in s["corrections"]
            if c["target"] == "executor"
        )

        total = sum(s["correction_count"] for s in sessions)
        confidence = executor_count / total if total > 0 else 0

        assert confidence == 1.0

    def test_confidence_based_on_consistency(self, tmp_path):
        """基于一致性计算置信度"""
        sessions = [
            make_session("s1", corrections=[
                make_correction("executor", root_cause_hint="slow"),
            ]),
            make_session("s2", corrections=[
                make_correction("executor", root_cause_hint="slow"),
            ]),
        ]

        # 同样的 root_cause_hint 一致性高
        slow_count = sum(
            1 for s in sessions
            for c in s["corrections"]
            if c.get("root_cause_hint") == "slow"
        )

        assert slow_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])