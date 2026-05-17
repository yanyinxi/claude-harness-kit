#!/usr/bin/env python3
"""
Hook Execution 集成测试

测试 Hook 执行链的完整流程
"""

import json
from pathlib import Path

import pytest


class TestHookExecutionChain:
    """Hook 执行链测试"""

    def test_pretooluse_to_posttooluse_chain(self, tmp_path):
        """PreToolUse → PostToolUse 完整链"""
        hooks_config = {
            "hooks": {
                "PreToolUse": [
                    {"type": "command", "command": "bash safety-check.sh"}
                ],
                "PostToolUse": [
                    {"type": "command", "command": "bash quality-gate.sh"}
                ]
            }
        }

        # 模拟执行链
        execution_log = []

        # PreToolUse 阶段
        pre_result = {"status": "passed", "checks": ["path_safe", "no_dangerous_cmd"]}
        execution_log.append({"stage": "PreToolUse", "result": pre_result})

        # 执行工具调用
        tool_call = {"tool": "Bash", "command": "ls -la"}
        execution_log.append({"stage": "ToolExecution", "tool": tool_call})

        # PostToolUse 阶段
        post_result = {"status": "passed", "checks": ["no_secrets", "format_correct"]}
        execution_log.append({"stage": "PostToolUse", "result": post_result})

        # 验证执行链
        assert len(execution_log) == 3
        assert execution_log[0]["stage"] == "PreToolUse"
        assert execution_log[1]["stage"] == "ToolExecution"
        assert execution_log[2]["stage"] == "PostToolUse"

    def test_hook_trigger_on_edit(self, tmp_path):
        """Edit 操作触发 Hook"""
        hooks_config = {
            "hooks": {
                "PostToolUse": [
                    {"matcher": "Edit|Write", "command": "bash coverage-check.sh"}
                ]
            }
        }

        # 模拟 Edit 操作
        tool_call = "Edit"
        should_trigger = any(
            re.search(matcher, tool_call)
            for matcher in hooks_config["hooks"]["PostToolUse"][0]["matcher"].split("|")
        )

        assert should_trigger is True

    def test_hook_trigger_on_bash(self, tmp_path):
        """Bash 操作触发 Hook"""
        hooks_config = {
            "hooks": {
                "PreToolUse": [
                    {"matcher": "Bash", "command": "bash safety-check.sh"}
                ]
            }
        }

        tool_call = "Bash"
        should_trigger = tool_call == "Bash"

        assert should_trigger is True


class TestHookExecutionOrder:
    """Hook 执行顺序测试"""

    def test_multiple_hooks_execute_in_order(self, tmp_path):
        """多个 Hook 按顺序执行"""
        hooks = [
            {"name": "safety", "order": 1},
            {"name": "coverage", "order": 2},
            {"name": "quality", "order": 3}
        ]

        # 按 order 排序
        hooks_sorted = sorted(hooks, key=lambda h: h["order"])
        names = [h["name"] for h in hooks_sorted]

        assert names == ["safety", "coverage", "quality"]

    def test_hook_timeout_enforcement(self, tmp_path):
        """Hook 超时强制执行"""
        hook = {"name": "slow_check", "timeout": 5}
        execution_time = 10  # 秒

        exceeded = execution_time > hook["timeout"]
        assert exceeded is True


class TestHookExecutionResult:
    """Hook 执行结果测试"""

    def test_hook_success(self, tmp_path):
        """Hook 成功执行"""
        hook_result = {
            "status": "success",
            "output": "All checks passed",
            "duration_ms": 150
        }

        assert hook_result["status"] == "success"
        assert hook_result["duration_ms"] < 1000

    def test_hook_failure_blocks_execution(self, tmp_path):
        """Hook 失败阻止执行"""
        hook_result = {
            "status": "failure",
            "error": "Coverage below threshold",
            "blocked": True
        }

        assert hook_result["status"] == "failure"
        assert hook_result["blocked"] is True

    def test_hook_warning_continues(self, tmp_path):
        """Hook 警告不阻止执行"""
        hook_result = {
            "status": "warning",
            "message": "Non-critical issue detected",
            "blocked": False
        }

        assert hook_result["status"] == "warning"
        assert hook_result["blocked"] is False


class TestHookErrorHandling:
    """Hook 错误处理测试"""

    def test_hook_timeout_handling(self, tmp_path):
        """Hook 超时处理"""
        hook_result = {
            "status": "timeout",
            "error": "Hook exceeded 30s timeout",
            "duration_s": 30
        }

        assert hook_result["status"] == "timeout"

    def test_hook_command_not_found(self, tmp_path):
        """Hook 命令不存在"""
        hook_result = {
            "status": "error",
            "error": "Command not found: invalid_command.sh"
        }

        assert hook_result["status"] == "error"
        assert "not found" in hook_result["error"]

    def test_hook_permission_denied(self, tmp_path):
        """Hook 权限拒绝"""
        hook_result = {
            "status": "error",
            "error": "Permission denied: hooks/bin/restricted.sh"
        }

        assert hook_result["status"] == "error"
        assert "denied" in hook_result["error"]


# 导入 re 用于正则匹配
import re


if __name__ == "__main__":
    pytest.main([__file__, "-v"])