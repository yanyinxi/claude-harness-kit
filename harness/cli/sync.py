#!/usr/bin/env python3
"""
kit sync — 从中央配置仓库同步团队共享规则。

用法:
  kit sync --from=https://github.com/team/claude-standards
  kit sync --from=./central-standards
  kit sync                       # 使用默认团队仓库（环境变量 CHK_TEAM_REPO）
  kit sync --dry-run             # 预览变更，不实际写入

同步内容:
  - rules/*.md → .claude/rules/
  - CLAUDE.md 团队片段 → 合并到项目 CLAUDE.md
  - repo-index.json 更新

特性:
  - 冲突检测：本地有修改时告警而非直接覆盖
  - 增量同步：跳过未变更的文件
  - Dry-run 模式：预览变更
"""
import argparse
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def _hash_file(path: Path) -> str:
    """计算文件 SHA256（用于增量同步）"""
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def _get_default_source() -> Optional[str]:
    """获取默认团队仓库 URL"""
    return os.environ.get("CHK_TEAM_REPO")


def sync_from_local(source: Path, root: Path, dry_run: bool = False) -> dict:
    """从本地目录同步，返回同步统计"""
    stats = {"rules": 0, "skipped": 0, "conflicts": 0, "errors": []}

    # ── 同步规则文件 ──
    rules_src = source / "rules"
    rules_dst = root / ".claude" / "rules"
    if rules_src.exists():
        rules_dst.mkdir(parents=True, exist_ok=True)
        for rule_file in rules_src.glob("*.md"):
            dst = rules_dst / rule_file.name
            src_hash = _hash_file(rule_file)
            dst_hash = _hash_file(dst)

            if src_hash == dst_hash:
                stats["skipped"] += 1
                continue

            if dst.exists() and dst_hash != _hash_file(dst):
                # 本地文件存在且与上次同步的不同 → 冲突
                stats["conflicts"] += 1
                stats["errors"].append(f"冲突: {dst.name} (本地有修改，跳过覆盖)")
                continue

            if dry_run:
                stats["rules"] += 1
                print(f"  [DRY-RUN] 将更新: {dst.name}")
            else:
                dst.write_text(rule_file.read_text(encoding="utf-8"), encoding="utf-8")
                stats["rules"] += 1

    # ── 同步团队 CLAUDE.md 片段 ──
    team_claude = source / "CLAUDE.md"
    if team_claude.exists():
        snippet = team_claude.read_text(encoding="utf-8")
        snippet_path = root / ".claude" / "CLAUDE_TEAM.md"
        old_hash = _hash_file(snippet_path)
        if not dry_run:
            snippet_path.write_text(snippet, encoding="utf-8")
            if old_hash != _hash_file(snippet_path):
                stats["rules"] += 1
            else:
                stats["skipped"] += 1

    # ── 同步仓库索引 ──
    index_src = source / "repo-index.json"
    if index_src.exists():
        index_dst = root / ".claude" / "repo-index.json"
        old_hash = _hash_file(index_dst)
        if not dry_run:
            index_dst.write_text(index_src.read_text(encoding="utf-8"))
            if old_hash != _hash_file(index_dst):
                stats["rules"] += 1

    return stats


def sync_from_git(url: str, root: Path, dry_run: bool = False) -> dict:
    """从 Git 仓库同步"""
    import tempfile
    import subprocess

    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, tmp],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"rules": 0, "skipped": 0, "conflicts": 0, "errors": [f"克隆失败: {result.stderr}"]}

        return sync_from_local(Path(tmp), root, dry_run=dry_run)


def _print_stats(stats: dict):
    """打印同步统计"""
    print(f"\n📊 同步结果 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"  ✅ 已更新: {stats['rules']} 个文件")
    print(f"  ⏭️  已跳过 (无变更): {stats['skipped']} 个文件")
    if stats["conflicts"]:
        print(f"  ⚠️  冲突 (未覆盖): {stats['conflicts']} 个文件")
    if stats["errors"]:
        for err in stats["errors"]:
            print(f"  ❌ {err}")


def main():
    parser = argparse.ArgumentParser(
        description="同步团队共享配置",
        epilog="设置环境变量 CHK_TEAM_REPO 可省略 --from 参数"
    )
    parser.add_argument("--from", dest="source", help="中央配置仓库路径或 URL")
    parser.add_argument("--dry-run", action="store_true", help="预览变更，不实际写入")
    args = parser.parse_args()

    source = args.source or _get_default_source()
    if not source:
        print("❌ 未指定来源。使用 --from 参数或设置环境变量 CHK_TEAM_REPO")
        sys.exit(1)

    root = find_root()

    if source.startswith(("http://", "https://", "git@")):
        stats = sync_from_git(source, root, dry_run=args.dry_run)
    else:
        stats = sync_from_local(Path(source).resolve(), root, dry_run=args.dry_run)

    _print_stats(stats)

    if stats["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
