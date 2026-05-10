#!/usr/bin/env python3
"""
doc-generator 测试文件

测试覆盖:
1. Markdown 转 HTML 转换
2. 文档类型映射
3. 错误处理
4. 批量转换
5. 会话总结生成
"""
import tempfile
import os
from pathlib import Path
from datetime import datetime

import pytest

# 导入被测模块（先检查是否存在）
try:
    from doc_generator import (
        convert,
        batch_convert,
        session_wrap,
        archive_document,
        _parse_markdown,
        _escape_html,
        DocMetadata,

        DOC_TYPE_MAP,
    )
except ImportError:
    pytest.skip("doc-generator.py 未实现，跳过测试", allow_module_level=True)


class TestMarkdownParsing:
    """Markdown 解析测试"""

    def test_parse_headings(self):
        """测试标题解析"""
        md = "# 主标题\n## 二级标题\n### 三级标题"
        html = _parse_markdown(md)
        assert "<h1>主标题</h1>" in html
        assert "<h2>二级标题</h2>" in html
        assert "<h3>三级标题</h3>" in html

    def test_parse_code_block(self):
        """测试代码块解析"""
        md = '```python\nprint("hello")\n```'
        html = _parse_markdown(md)
        assert "<pre><code" in html
        assert "print(&quot;hello&quot;)" in html

    def test_parse_table(self):
        """测试表格解析"""
        md = """| 列1 | 列2 |
|------|------|
| 值1  | 值2  |"""
        html = _parse_markdown(md)
        assert "<table" in html
        assert "<th>列1</th>" in html
        assert "<td>值1</td>" in html

    def test_parse_list(self):
        """测试列表解析"""
        md = "- 项目1\n- 项目2\n- 项目3"
        html = _parse_markdown(md)
        assert "<li" in html
        assert "项目1" in html

    def test_parse_bold_italic(self):
        """测试加粗和斜体"""
        md = "**加粗** 和 *斜体* 和 `代码`"
        html = _parse_markdown(md)
        assert "<strong>加粗</strong>" in html
        assert "<em>斜体</em>" in html
        assert "<code>代码</code>" in html

    def test_parse_link(self):
        """测试链接解析"""
        md = "[链接文本](https://example.com)"
        html = _parse_markdown(md)
        assert '<a href="https://example.com">链接文本</a>' in html

    def test_parse_blockquote(self):
        """测试引用块"""
        md = "> 引用文本"
        html = _parse_markdown(md)
        assert "<blockquote>引用文本</blockquote>" in html


class TestHtmlEscape:
    """HTML 转义测试"""

    def test_escape_ampersand(self):
        assert _escape_html("A & B") == "A &amp; B"

    def test_escape_lt_gt(self):
        assert _escape_html("<tag>") == "&lt;tag&gt;"

    def test_escape_quotes(self):
        assert _escape_html('"quoted"') == "&quot;quoted&quot;"


class TestConvert:
    """转换功能测试"""

    @pytest.fixture
    def temp_md_file(self):
        """创建临时 Markdown 文件"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# 测试文档\n\n这是测试内容。\n\n```python\nprint('hello')\n```")
            return Path(f.name)

    @pytest.fixture
    def temp_output_dir(self):
        """创建临时输出目录"""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        # 清理
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_convert_basic(self, temp_md_file, temp_output_dir):
        """基本转换测试"""
        result = convert(temp_md_file, "implementation", temp_output_dir)

        assert result is not None
        assert result.exists()
        assert result.suffix == ".html"

        content = result.read_text(encoding="utf-8")
        assert "<h1>测试文档</h1>" in content
        assert "这是测试内容" in content

    def test_convert_with_metadata(self, temp_md_file, temp_output_dir):
        """带元数据转换测试"""
        metadata = DocMetadata(
            doc_type="review",
            title="审查报告",
            agent_name="code-reviewer",
            session_id="test-session-123",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        result = convert(temp_md_file, "review", temp_output_dir, metadata)

        assert result is not None
        content = result.read_text(encoding="utf-8")
        assert "审查报告" in content
        assert "code-reviewer" in content

    def test_convert_invalid_file(self, temp_output_dir):
        """无效文件处理"""
        invalid_file = Path("/nonexistent/file.md")
        result = convert(invalid_file, "implementation", temp_output_dir)
        assert result is None

    def test_output_dir_creation(self, temp_md_file, temp_output_dir):
        """输出目录自动创建"""
        nested_dir = temp_output_dir / "nested" / "path"
        result = convert(temp_md_file, "implementation", nested_dir)

        assert result is not None
        assert nested_dir.exists()


class TestBatchConvert:
    """批量转换测试"""

    @pytest.fixture
    def temp_md_files(self):
        """创建多个临时 Markdown 文件"""
        files = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(3):
                p = Path(tmpdir) / f"doc{i}.md"
                p.write_text(f"# 文档 {i}\n\n内容 {i}", encoding="utf-8")
                files.append(p)
            yield files

    @pytest.fixture
    def temp_output_dir(self):
        """创建临时输出目录"""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_batch_convert(self, temp_md_files, temp_output_dir):
        """批量转换测试"""
        results = batch_convert(temp_md_files, temp_output_dir, "implementation")

        assert len(results) == 3
        for r in results:
            assert r.exists()
            assert r.suffix == ".html"

    def test_batch_empty_list(self, temp_output_dir):
        """空列表处理"""
        results = batch_convert([], temp_output_dir, "implementation")
        assert results == []


class TestSessionWrap:
    """会话总结测试"""

    @pytest.fixture
    def temp_output_dir(self):
        """创建临时输出目录"""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_session_wrap_basic(self, temp_output_dir):
        """基本会话总结测试"""
        result = session_wrap(
            session_id="test-session-001",
            agents=["architect", "backend-dev", "code-reviewer"],
            output_dir=temp_output_dir
        )

        assert result is not None
        assert result.exists()
        content = result.read_text(encoding="utf-8")
        assert "test-session-001" in content
        assert "architect" in content
        assert "backend-dev" in content

    def test_session_wrap_with_docs(self, temp_output_dir):
        """带文档的会话总结测试"""
        # 创建临时文档
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            doc_path = Path(f.name)
            f.write("# 测试文档\n\n文档内容")

        try:
            result = session_wrap(
                session_id="test-session-002",
                agents=["backend-dev"],
                output_dir=temp_output_dir,
                docs=[doc_path]
            )

            assert result is not None
            content = result.read_text(encoding="utf-8")
            assert "测试文档" in content
        finally:
            doc_path.unlink(missing_ok=True)


class TestArchiveDocument:
    """文档归档测试"""

    @pytest.fixture
    def temp_source_file(self):
        """创建临时源文件"""
        tmpdir = tempfile.mkdtemp()
        source = Path(tmpdir) / "test-doc.html"
        source.write_text("<html>test</html>", encoding="utf-8")
        yield source
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_archive_document(self, temp_source_file):
        """归档功能测试"""
        # 设置项目根目录
        os.environ["CLAUDE_PROJECT_DIR"] = tempfile.mkdtemp()
        Path(os.environ["CLAUDE_PROJECT_DIR"])

        result = archive_document(temp_source_file, "implementation")

        assert result is not None
        assert result.exists()
        # 验证按月组织
        now = datetime.now()
        assert f"{now.year}-{now.month:02d}" in str(result)

        # 清理
        import shutil
        shutil.rmtree(os.environ["CLAUDE_PROJECT_DIR"], ignore_errors=True)


class TestDocTypeMap:
    """文档类型映射测试"""

    def test_doc_type_mapping(self):
        """测试文档类型映射"""
        assert "architecture" in DOC_TYPE_MAP
        assert "prd" in DOC_TYPE_MAP
        assert "review" in DOC_TYPE_MAP
        assert DOC_TYPE_MAP["architecture"] == "架构设计"


class TestErrorHandling:
    """错误处理测试"""

    def test_missing_error_file(self, tmp_path):
        """缺失错误文件时的处理"""
        # 设置不存在的 .claude/data 目录
        os.environ["CLAUDE_PROJECT_DIR"] = str(tmp_path / "nonexistent")
        # 应该不抛出异常，静默失败
        from doc_generator import _log_error
        # 不应抛出异常
        _log_error(phase="test", error_msg="test error")


class TestCliInterface:
    """CLI 接口测试"""

    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """创建临时项目目录"""
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        docs_dir = project_dir / "docs"
        docs_dir.mkdir()
        artifacts_dir = docs_dir / "artifacts"
        artifacts_dir.mkdir()
        claude_data = project_dir / ".claude" / "data"
        claude_data.mkdir(parents=True)
        os.environ["CLAUDE_PROJECT_DIR"] = str(project_dir)
        yield project_dir

    def test_convert_command(self, temp_project_dir):
        """测试 convert 命令"""
        # 创建测试 Markdown 文件
        md_file = temp_project_dir / "test.md"
        md_file.write_text("# 测试\n\n内容", encoding="utf-8")

        # 运行 convert 命令
        from doc_generator import main
        import sys

        old_argv = sys.argv
        try:
            sys.argv = [
                "doc-generator.py", "convert",
                str(md_file),
                "--type", "implementation",
                "--output", str(temp_project_dir / "docs" / "artifacts")
            ]
            # 应该不抛出异常
            main()
        finally:
            sys.argv = old_argv

    def test_batch_command(self, temp_project_dir):
        """测试 batch 命令"""
        from doc_generator import main
        import sys

        # 创建多个 Markdown 文件
        for i in range(2):
            (temp_project_dir / f"doc{i}.md").write_text(f"# Doc {i}", encoding="utf-8")

        old_argv = sys.argv
        try:
            sys.argv = [
                "doc-generator.py", "batch",
                str(temp_project_dir),
                "--output", str(temp_project_dir / "docs" / "artifacts")
            ]
            main()
        finally:
            sys.argv = old_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])