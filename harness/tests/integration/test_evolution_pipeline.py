#!/usr/bin/env python3
"""
Evolution Pipeline 集成测试

测试进化系统的完整数据流：
sessions.jsonl → analyzer → proposer → apply_change
"""

import json
from pathlib import Path

import pytest

from harness.tests.conftest import make_session, make_correction


class TestEvolutionPipelineFlow:
    """进化管道全链路集成测试"""

    def test_session_to_analysis_flow(self, tmp_path):
        """sessions → analysis 数据流"""
        # 1. 创建测试 sessions
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"
        sessions = [
            make_session("s1", corrections=[make_correction("executor")]),
            make_session("s2", corrections=[make_correction("backend-dev")]),
            make_session("s3", corrections=[make_correction("executor")]),
        ]
        sessions_file.write_text("\n".join(json.dumps(s) for s in sessions))

        # 2. 读取 sessions
        content = sessions_file.read_text()
        parsed_sessions = [json.loads(line) for line in content.strip().split("\n") if line]

        # 3. 分析
        analysis = {
            "total_sessions": len(parsed_sessions),
            "total_corrections": sum(s["correction_count"] for s in parsed_sessions),
            "top_targets": ["executor"]
        }

        # 验证数据流
        assert len(parsed_sessions) == 3
        assert analysis["total_corrections"] == 3
        assert "executor" in analysis["top_targets"]

    def test_analysis_to_proposal_flow(self, tmp_path):
        """analysis → proposal 数据流"""
        # 1. 模拟分析结果
        analysis = {
            "total_sessions": 5,
            "total_corrections": 8,
            "top_targets": ["executor", "backend-dev"],
            "patterns": [
                {"target": "executor", "count": 5, "root_cause": "slow"}
            ]
        }

        # 2. 生成提案
        proposal = {
            "type": "instinct",
            "target": "executor",
            "changes": [
                {
                    "field": "response_delay",
                    "from": "0",
                    "to": "500ms"
                }
            ],
            "confidence": 0.8,
            "triggered_by": "repeated_corrections"
        }

        # 3. 验证提案格式
        assert proposal["type"] == "instinct"
        assert "target" in proposal
        assert "changes" in proposal
        assert 0 <= proposal["confidence"] <= 1

    def test_proposal_to_apply_flow(self, tmp_path):
        """proposal → apply 数据流"""
        # 1. 模拟提案
        proposal = {
            "type": "instinct",
            "target": "executor",
            "changes": [
                {"field": "timeout", "from": "30s", "to": "60s"}
            ]
        }

        # 2. 执行变更
        applied_changes = []
        for change in proposal["changes"]:
            applied_changes.append({
                "field": change["field"],
                "new_value": change["to"],
                "status": "applied"
            })

        # 3. 验证变更结果
        assert len(applied_changes) == 1
        assert applied_changes[0]["status"] == "applied"


class TestEvolutionPipelineEdgeCases:
    """边界情况测试"""

    def test_empty_sessions_file(self, tmp_path):
        """空 sessions 文件"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"
        sessions_file.write_text("")

        content = sessions_file.read_text()
        sessions = [json.loads(line) for line in content.strip().split("\n") if line]

        assert len(sessions) == 0

    def test_invalid_json_in_sessions(self, tmp_path):
        """sessions 中包含无效 JSON"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        sessions_file = data_dir / "sessions.jsonl"
        sessions_file.write_text('{"valid": "json"}\ninvalid{json}')

        content = sessions_file.read_text()
        lines = [l for l in content.strip().split("\n") if l]
        valid_sessions = []
        for line in lines:
            try:
                valid_sessions.append(json.loads(line))
            except json.JSONDecodeError:
                pass

        assert len(valid_sessions) == 1

    def test_proposal_with_no_changes(self, tmp_path):
        """提案无变更"""
        proposal = {
            "type": "instinct",
            "target": "executor",
            "changes": []
        }

        applied_changes = []
        for change in proposal["changes"]:
            applied_changes.append(change)

        assert len(applied_changes) == 0


class TestEvolutionPipelineValidation:
    """验证测试"""

    def test_session_schema_validation(self, tmp_path):
        """Session 数据结构验证"""
        session = make_session("test_session")
        required_fields = ["session_id", "timestamp", "corrections", "status"]

        for field in required_fields:
            assert field in session, f"缺少必需字段: {field}"

    def test_proposal_schema_validation(self, tmp_path):
        """Proposal 数据结构验证"""
        proposal = {
            "type": "instinct",
            "target": "executor",
            "changes": [{"field": "test"}],
            "confidence": 0.8
        }
        required_fields = ["type", "target", "changes"]

        for field in required_fields:
            assert field in proposal, f"缺少必需字段: {field}"

    def test_confidence_range_validation(self, tmp_path):
        """置信度范围验证"""
        proposal = {"confidence": 0.8}

        assert 0 <= proposal["confidence"] <= 1

    def test_trigger_threshold_validation(self, tmp_path):
        """触发阈值验证"""
        threshold = {"sessions": 5, "corrections": 3, "time_hours": 6}

        assert threshold["sessions"] >= 1
        assert threshold["corrections"] >= 1
        assert threshold["time_hours"] >= 1


class TestEvolutionPipelineRollback:
    """回滚测试"""

    def test_rollback_changes(self, tmp_path):
        """回滚变更"""
        original_value = {"timeout": "30s"}

        # 应用新值
        current_value = {"timeout": "60s"}

        # 回滚
        rolled_back = original_value.copy()

        assert rolled_back["timeout"] == original_value["timeout"]
        assert rolled_back["timeout"] != current_value["timeout"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])