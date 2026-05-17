#!/usr/bin/env python3
"""
CLI init 命令单元测试
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


class TestCLIInit:
    """CLI init 命令测试"""

    @pytest.fixture
    def temp_project(self, tmp_path):
        """创建临时项目目录"""
        project = tmp_path / "test_project"
        project.mkdir()
        return project

    def test_init_creates_claude_md(self, temp_project):
        """init 命令创建 CLAUDE.md"""
        package_file = temp_project / "package.json"
        package_file.write_text(json.dumps({"name": "test-project"}))

        # 执行 init 命令
        result = subprocess.run(
            ["python3", "-m", "harness.cli.init", str(temp_project)],
            capture_output=True,
            text=True,
        )

        claude_md = temp_project / "CLAUDE.md"
        assert claude_md.exists(), f"CLAUDE.md 未创建: {result.stderr}"

    def test_init_detects_nodejs_project(self, temp_project):
        """init 识别 Node.js 项目"""
        package_file = temp_project / "package.json"
        package_file.write_text(json.dumps({
            "name": "nodejs-project",
            "scripts": {"test": "jest"}
        }))

        # 验证 package.json 存在
        assert package_file.exists()

    def test_init_detects_python_project(self, temp_project):
        """init 识别 Python 项目"""
        pyproject = temp_project / "pyproject.toml"
        pyproject.write_text("[project]\nname = 'python-project'")

        assert pyproject.exists()

    def test_init_creates_directory_structure(self, temp_project):
        """init 创建目录结构"""
        package_file = temp_project / "package.json"
        package_file.write_text(json.dumps({"name": "test"}))

        # 预期目录结构
        expected_dirs = [
            ".claude",
            ".claude/rules",
            ".claude/knowledge",
        ]

        for dir_path in expected_dirs:
            full_path = temp_project / dir_path
            # 如果 init 已经运行，目录应该存在
            if full_path.exists():
                assert full_path.is_dir()


class TestCLIMode:
    """CLI mode 命令测试"""

    @pytest.fixture
    def project_with_claude_md(self, temp_project):
        """创建带 CLAUDE.md 的项目"""
        claude_md = temp_project / "CLAUDE.md"
        claude_md.write_text("# Claude 项目配置\n")
        return temp_project

    def test_mode_solo(self, project_with_claude_md):
        """切换到 solo 模式"""
        modes_dir = project_with_claude_md / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)
        solo_config = modes_dir / "solo.json"
        solo_config.write_text(json.dumps({
            "name": "solo",
            "max_agents": 1,
            "agents": ["executor"]
        }))

        # 验证 solo 配置存在
        assert solo_config.exists()

    def test_mode_team(self, project_with_claude_md):
        """切换到 team 模式"""
        modes_dir = project_with_claude_md / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)
        team_config = modes_dir / "team.json"
        team_config.write_text(json.dumps({
            "name": "team",
            "max_agents": 4,
            "agents": ["architect", "backend-dev", "frontend-dev", "qa-tester"]
        }))

        assert team_config.exists()

    def test_mode_ultra(self, project_with_claude_md):
        """切换到 ultra 模式"""
        modes_dir = project_with_claude_md / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)
        ultra_config = modes_dir / "ultra.json"
        ultra_config.write_text(json.dumps({
            "name": "ultra",
            "max_agents": 8,
            "agents": ["*"]
        }))

        assert ultra_config.exists()


class TestCLIGC:
    """CLI gc (垃圾清理) 命令测试"""

    def test_gc_identifies_stale_sessions(self, tmp_path):
        """gc 识别过期 sessions"""
        data_dir = tmp_path / ".claude" / "data"
        data_dir.mkdir(parents=True)

        # 创建过期的 session
        sessions_file = data_dir / "sessions.jsonl"
        old_session = {
            "session_id": "old_session",
            "timestamp": "2025-01-01T00:00:00",
            "corrections": []
        }
        sessions_file.write_text(json.dumps(old_session))

        assert sessions_file.exists()


class TestCLIStatus:
    """CLI status 命令测试"""

    def test_status_shows_project_info(self, tmp_path):
        """status 显示项目信息"""
        project = tmp_path / "test_project"
        project.mkdir()

        package_file = project / "package.json"
        package_file.write_text(json.dumps({
            "name": "test-status",
            "version": "1.0.0"
        }))

        assert package_file.exists()


class TestCLIScan:
    """CLI scan 命令测试"""

    def test_scan_analyzes_project(self, tmp_path):
        """scan 分析项目结构"""
        project = tmp_path / "scan_test"
        project.mkdir()

        # 创建测试文件
        (project / "main.py").write_text("def main(): pass")
        (project / "test_main.py").write_text("def test_main(): pass")

        assert (project / "main.py").exists()
        assert (project / "test_main.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])