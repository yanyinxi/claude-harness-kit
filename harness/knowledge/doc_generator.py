#!/usr/bin/env python3
"""
doc-generator.py — 文档生成器核心

功能:
  - Markdown 转 HTML 转换
  - 会话总结 HTML 生成
  - 批量文档转换
  - 错误记录到 error.jsonl

使用方法:
  python3 doc-generator.py convert <md-file> --type <doc-type> --output <dir>
  python3 doc-generator.py session-wrap --session-id <id> --agents <agents> --output <dir>
  python3 doc-generator.py batch <dir>
"""
import argparse
import json
import os
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 全局常量 ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
DOCS_DIR = PROJECT_ROOT / "docs"
ARTIFACTS_DIR = DOCS_DIR / "artifacts"
ARCHIVES_DIR = DOCS_DIR / "archives"

# 文档类型映射
DOC_TYPE_MAP = {
    "architecture": "架构设计",
    "prd": "产品需求",
    "review": "审查报告",
    "test": "测试报告",
    "implementation": "实现报告",
    "verification": "验证报告",
}

# CSS 样式（暗色主题）
BASE_CSS = """
:root {
    --bg-primary: #0f1419;
    --bg-secondary: #1a2332;
    --bg-card: #1e2a3a;
    --border: #2d3f5a;
    --text-primary: #e8eaed;
    --text-secondary: #9aa0a6;
    --accent: #4fc3f7;
    --accent-success: #81c784;
    --accent-warning: #ffb74d;
    --accent-danger: #ef5350;
    --code-bg: #1a1f29;
}
"""

# 模板缓存
_template_cache: dict[str, str] = {}


# ── 数据类 ─────────────────────────────────────────────────────────────────────

@dataclass
class DocMetadata:
    """文档元数据"""
    doc_type: str
    title: str
    agent_name: str
    session_id: str
    created_at: str
    source_file: Optional[str] = None


# ── 错误记录 ───────────────────────────────────────────────────────────────────

def _log_error(
    phase: str,
    error_msg: str,
    file_path: Optional[str] = None,
    recoverable: bool = True,
    **context
):
    """记录错误到 error.jsonl（复用现有系统）"""
    try:
        from error_writer import write_error, build_error_record, ErrorType

        record = build_error_record(
            error_type=ErrorType.TOOL_FAILURE,
            error_message=error_msg,
            source=f"knowledge/doc-generator.py:{phase}",
            context={
                "phase": phase,
                "file": file_path,
                "recoverable": recoverable,
                **context
            }
        )
        write_error(record)
    except Exception:
        # fallback: 简化版错误写入
        root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
        error_file = root / ".claude" / "data" / "error.jsonl"
        try:
            with open(error_file, "a", encoding="utf-8") as f:
                record = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "doc-generator-error",
                    "phase": phase,
                    "error": error_msg,
                    "source": f"knowledge/doc-generator.py:{phase}",
                    "file": file_path,
                    "recoverable": recoverable,
                    **context
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception:
            pass  # 静默失败


# ── 核心函数 ───────────────────────────────────────────────────────────────────

def _escape_html(text: str) -> str:
    """HTML 转义"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def is_separator_row(cells: list[str]) -> bool:
    """检测表格分隔行（|---|:| 格式）"""
    if not cells:
        return False
    return all(
        re.match(r"^:?-+:?$", c.strip().replace(" ", "")) or c.strip() == ""
        for c in cells
    )


def _parse_markdown(md_content: str) -> str:
    """Markdown 转 HTML（基础实现）"""
    lines = md_content.split("\n")
    html_parts: list[str] = []
    in_code_block = False
    in_table = False
    list_buffer: list[str] = []

    def flush_list():
        nonlocal list_buffer
        if list_buffer:
            html_parts.append("<ul>" + "".join(list_buffer) + "</ul>")
            list_buffer = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith("```"):
            if not in_code_block:
                flush_list()
                in_code_block = True
                lang = line.strip()[3:].strip().lower()
                html_parts.append(f'<pre><code class="language-{lang}">')
            else:
                in_code_block = False
                html_parts.append("</code></pre>")
            i += 1
            continue

        if in_code_block:
            html_parts.append(_escape_html(line))
            i += 1
            continue

        # 标题
        if match := re.match(r"^(#{1,6})\s+(.+)$", line):
            flush_list()
            level = len(match.group(1))
            text = match.group(2)
            html_parts.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # 表格开始
        if "|" in line and line.strip().startswith("|"):
            flush_list()
            if not in_table:
                in_table = True
                html_parts.append('<table class="markdown-table"><thead><tr>')
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if is_separator_row(cells):
                # 分隔行
                if in_table:
                    html_parts.append("</thead><tbody>")
                i += 1
                continue
            html_parts.append("<th>" + "</th><th>".join(cells) + "</th>")
            i += 1
            continue

        # 表格行
        if in_table and "|" in line:
            cells = [c.strip() for c in line.split("|") if c.strip()]
            html_parts.append("<tr><td>" + "</td><td>".join(cells) + "</td></tr>")
            i += 1
            continue

        # 表格结束
        if in_table and "|" not in line:
            flush_list()
            html_parts.append("</tbody></table>")
            in_table = False
            continue

        # 列表
        if match := re.match(r"^(\s*)[-*]\s+(.+)$", line):
            indent = len(match.group(1)) // 2
            text = match.group(2)
            list_buffer.append(f'<li class="level-{indent}">{text}</li>')
            i += 1
            continue

        # 有序列表
        if match := re.match(r"^(\s*)\d+\.\s+(.+)$", line):
            indent = len(match.group(1)) // 2
            text = match.group(2)
            list_buffer.append(f'<li class="level-{indent}">{text}</li>')
            i += 1
            continue

        # 刷新列表（遇到非列表行）
        if list_buffer:
            flush_list()

        # 水平线
        if re.match(r"^---+$", line.strip()):
            html_parts.append("<hr>")
            i += 1
            continue

        # 加粗和斜体（移到 blockquote 提取后处理，避免重复应用）
        # 先检测 blockquote，提取内容并应用 inline 格式，再包裹
        processed = line

        # 引用块：先提取内容，再应用 inline 格式，最后包裹 blockquote
        if processed.strip().startswith(">"):
            inner = processed.lstrip(">").strip()
            inner = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", inner)
            inner = re.sub(r"\*(.+?)\*", r"<em>\1</em>", inner)
            inner = re.sub(r"`(.+?)`", r"<code>\1</code>", inner)
            inner = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2">\1</a>', inner)
            html_parts.append(f"<blockquote>{inner}</blockquote>")
        else:
            # 非 blockquote 行：应用 inline 格式
            processed = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", processed)
            processed = re.sub(r"\*(.+?)\*", r"<em>\1</em>", processed)
            processed = re.sub(r"`(.+?)`", r"<code>\1</code>", processed)
            processed = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2">\1</a>', processed)
            if processed.strip():
                html_parts.append(f"<p>{processed}</p>")

        i += 1

    # 关闭未关闭的元素
    if list_buffer:
        flush_list()
    if in_table:
        html_parts.append("</tbody></table>")

    return "\n".join(html_parts)


def _get_default_template() -> str:
    """默认 HTML 模板"""
    css = BASE_CSS
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <style>
        """ + css + """
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; padding: 2rem; background: var(--bg-primary); color: var(--text-primary); }
        .container { max-width: 900px; margin: 0 auto; }
        header { background: var(--bg-card); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border: 1px solid var(--border); }
        header h1 { margin: 0 0 0.5rem 0; color: var(--accent); }
        .meta { display: flex; gap: 1rem; align-items: center; color: var(--text-secondary); font-size: 0.9rem; }
        .tag { background: var(--accent); color: var(--bg-primary); padding: 0.2rem 0.6rem; border-radius: 4px; font-weight: 500; }
        main { background: var(--bg-card); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border); }
        main h1, main h2, main h3 { color: var(--accent); margin-top: 1.5rem; }
        main h1:first-child, main h2:first-child { margin-top: 0; }
        main table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
        main th, main td { border: 1px solid var(--border); padding: 0.5rem; text-align: left; }
        main th { background: var(--bg-secondary); }
        main pre { background: var(--code-bg); padding: 1rem; border-radius: 8px; overflow-x: auto; }
        main code { background: var(--code-bg); padding: 0.2rem 0.4rem; border-radius: 4px; }
        main blockquote { border-left: 4px solid var(--accent); margin: 1rem 0; padding: 0.5rem 1rem; background: var(--bg-secondary); }
        main ul, main ol { padding-left: 1.5rem; }
        main li { margin: 0.3rem 0; }
        footer { text-align: center; margin-top: 2rem; color: var(--text-secondary); font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>__TITLE__</h1>
            <div class="meta">
                <span class="tag">__DOCTYPE__</span>
                <span class="agent">__AGENT__</span>
                <span class="date">__CREATED__</span>
            </div>
        </header>
        <main>
            __CONTENT__
        </main>
        <footer>
            CHK Document | Generated by Claude Code
        </footer>
    </div>
</body>
</html>"""


def convert(
    md_file: Path,
    doc_type: str,
    output_dir: Path,
    metadata: Optional[DocMetadata] = None,
    add_timestamp: bool = False
) -> Optional[Path]:
    """
    将 Markdown 文件转换为 HTML

    Args:
        md_file: Markdown 文件路径
        doc_type: 文档类型
        output_dir: 输出目录
        metadata: 文档元数据
        add_timestamp: 是否在输出文件名中添加时间戳

    Returns:
        生成的 HTML 文件路径，失败返回 None
    """
    start_time = datetime.now()

    try:
        # 读取 Markdown
        if not md_file.exists():
            _log_error(
                phase="read",
                error_msg=f"文件不存在: {md_file}",
                file_path=str(md_file),
                recoverable=False
            )
            return None
        md_content = md_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        _log_error(
            phase="read",
            error_msg=f"文件不存在: {md_file}",
            file_path=str(md_file),
            recoverable=False
        )
        return None
    except Exception as e:
        _log_error(
            phase="read",
            error_msg=f"读取 Markdown 失败: {e}",
            file_path=str(md_file),
            recoverable=False
        )
        return None

    try:
        # 解析 Markdown
        html_content = _parse_markdown(md_content)

        # 获取模板
        template = _get_default_template()

        # 准备元数据
        if metadata is None:
            metadata = DocMetadata(
                doc_type=doc_type,
                title=md_file.stem,
                agent_name="unknown",
                session_id="",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                source_file=str(md_file)
            )

        # 填充模板
        html = template
        html = html.replace("__TITLE__", _escape_html(metadata.title))
        html = html.replace("__DOCTYPE__", DOC_TYPE_MAP.get(doc_type, doc_type))
        html = html.replace("__CREATED__", metadata.created_at)
        html = html.replace("__CONTENT__", html_content)
        html = html.replace("__AGENT__", metadata.agent_name)

        # 确保输出目录存在
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成输出文件名
        if add_timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"{md_file.stem}_{timestamp}.html"
        else:
            output_file = output_dir / f"{md_file.stem}.html"

        # 写入 HTML
        output_file.write_text(html, encoding="utf-8")

        # 记录性能指标
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        if elapsed > 100:
            _log_error(
                phase="convert",
                error_msg=f"转换超时 ({elapsed:.0f}ms > 100ms)",
                file_path=str(md_file),
                recoverable=True
            )

        return output_file

    except Exception as e:
        _log_error(
            phase="convert",
            error_msg=f"Markdown 转 HTML 失败: {e}",
            file_path=str(md_file),
            recoverable=True
        )
        return None


def batch_convert(
    md_files: list[Path],
    output_dir: Path,
    doc_type: str = "implementation"
) -> list[Path]:
    """批量转换（并行处理）"""
    if not md_files:
        return []

    # 使用进程池并行处理
    max_workers = min(4, os.cpu_count() or 2)
    results: list[Path] = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(convert, f, doc_type, output_dir)
            for f in md_files
        ]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    return results


def session_wrap(
    session_id: str,
    agents: list[str],
    output_dir: Path,
    docs: Optional[list[Path]] = None
) -> Optional[Path]:
    """
    生成会话总结 HTML

    Args:
        session_id: 会话 ID
        agents: 使用的 Agent 列表
        output_dir: 输出目录
        docs: 相关文档路径列表

    Returns:
        生成的 HTML 文件路径
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        # 收集文档内容
        doc_contents: list[dict] = []
        if docs:
            for doc in docs:
                if doc.exists() and doc.suffix in [".md", ".html"]:
                    doc_contents.append({
                        "name": doc.stem,
                        "type": doc.suffix.lstrip("."),
                        "content": doc.read_text(encoding="utf-8")[:500]
                    })

        # 生成会话总结
        summary_html = f"""
        <div class="session-summary">
            <h2>会话总结</h2>
            <div class="session-meta">
                <p><strong>会话 ID:</strong> {session_id}</p>
                <p><strong>参与 Agent:</strong> {", ".join(agents)}</p>
                <p><strong>生成时间:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            <h3>文档产出</h3>
            <ul class="doc-list">
                {"".join(f'<li><a href="{d["name"]}.{d["type"]}">{d["name"]}</a> ({d["type"]})</li>' for d in doc_contents) or "<li>无文档产出</li>"}
            </ul>
        </div>
        """

        # 构建完整 HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>会话总结 - {session_id}</title>
    <style>
        {BASE_CSS}
        body {{ padding: 2rem; background: var(--bg-primary); color: var(--text-primary); }}
        .session-summary {{ max-width: 800px; margin: 0 auto; }}
        .session-meta {{ background: var(--bg-card); padding: 1rem; border-radius: 8px; border: 1px solid var(--border); }}
        .doc-list {{ list-style: none; padding: 0; }}
        .doc-list li {{ padding: 0.5rem; border-bottom: 1px solid var(--border); }}
        .doc-list li a {{ color: var(--accent); }}
    </style>
</head>
<body>
    <div class="session-summary">
        {summary_html}
    </div>
</body>
</html>"""

        # 输出文件
        output_file = output_dir / f"session_{session_id}_{datetime.now().strftime('%Y%m%d')}.html"
        output_file.write_text(html, encoding="utf-8")

        return output_file

    except Exception as e:
        _log_error(
            phase="session-wrap",
            error_msg=f"会话总结生成失败: {e}",
            file_path=str(session_id),
            recoverable=True
        )
        return None


def archive_document(source: Path, doc_type: str) -> Optional[Path]:
    """
    归档文档到按月组织的目录

    Args:
        source: 源文件路径
        doc_type: 文档类型

    Returns:
        归档后的文件路径
    """
    try:
        now = datetime.now()
        archive_dir = ARCHIVES_DIR / f"{now.year}-{now.month:02d}" / doc_type
        archive_dir.mkdir(parents=True, exist_ok=True)

        dest = archive_dir / source.name
        shutil.copy2(source, dest)
        return dest

    except Exception as e:
        _log_error(
            phase="archive",
            error_msg=f"文档归档失败: {e}",
            file_path=str(source),
            recoverable=True
        )
        return None


def async_archive(source: Path, doc_type: str):
    """异步归档，不阻塞主流程"""
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(archive_document, source, doc_type)
    executor.shutdown(wait=False)  # 任务提交后立即关闭，避免资源泄漏


# ── CLI 入口 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="文档生成器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # convert 命令
    convert_parser = subparsers.add_parser("convert", help="转换单个 Markdown 文件")
    convert_parser.add_argument("md_file", type=Path, help="Markdown 文件路径")
    convert_parser.add_argument("--type", "-t", default="implementation", help="文档类型")
    convert_parser.add_argument("--output", "-o", type=Path, default=ARTIFACTS_DIR, help="输出目录")
    convert_parser.add_argument("--title", help="文档标题")
    convert_parser.add_argument("--agent", help="Agent 名称")
    convert_parser.add_argument("--session", help="会话 ID")

    # session-wrap 命令
    wrap_parser = subparsers.add_parser("session-wrap", help="生成会话总结")
    wrap_parser.add_argument("--session-id", required=True, help="会话 ID")
    wrap_parser.add_argument("--agents", required=True, help="Agent 列表（逗号分隔）")
    wrap_parser.add_argument("--output", "-o", type=Path, default=ARTIFACTS_DIR, help="输出目录")
    wrap_parser.add_argument("--docs", type=Path, nargs="*", help="相关文档路径")

    # batch 命令
    batch_parser = subparsers.add_parser("batch", help="批量转换目录")
    batch_parser.add_argument("dir", type=Path, help="包含 Markdown 文件的目录")
    batch_parser.add_argument("--output", "-o", type=Path, default=ARTIFACTS_DIR, help="输出目录")
    batch_parser.add_argument("--type", "-t", default="implementation", help="文档类型")
    batch_parser.add_argument("--recursive", "-r", action="store_true", help="递归处理子目录")

    args = parser.parse_args()

    if args.command == "convert":
        metadata = DocMetadata(
            doc_type=args.type,
            title=args.title or args.md_file.stem,
            agent_name=args.agent or "unknown",
            session_id=args.session or "",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source_file=str(args.md_file)
        )
        result = convert(args.md_file, args.type, args.output, metadata)

        if result:
            print(json.dumps({
                "success": True,
                "output": str(result),
                "archived": bool(archive_document(result, args.type))
            }))
        else:
            print(json.dumps({"success": False, "error": "转换失败"}))
            sys.exit(1)

    elif args.command == "session-wrap":
        agents_list = [a.strip() for a in args.agents.split(",")]
        result = session_wrap(args.session_id, agents_list, args.output, args.docs)

        if result:
            print(json.dumps({"success": True, "output": str(result)}))
        else:
            print(json.dumps({"success": False, "error": "会话总结生成失败"}))
            sys.exit(1)

    elif args.command == "batch":
        # 收集 Markdown 文件
        if args.recursive:
            md_files = list(args.dir.rglob("*.md"))
        else:
            md_files = list(args.dir.glob("*.md"))

        if not md_files:
            print(json.dumps({"success": False, "error": "未找到 Markdown 文件"}))
            sys.exit(1)

        results = batch_convert(md_files, args.output, args.type)
        print(json.dumps({
            "success": True,
            "total": len(md_files),
            "converted": len(results),
            "outputs": [str(r) for r in results]
        }))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()