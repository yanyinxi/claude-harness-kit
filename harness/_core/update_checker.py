#!/usr/bin/env python3
"""
CHK 插件更新检测器 - 从 GitHub 获取最新版本并比较

主要功能：
- get_local_version() → 从 version.json 读取本地版本
- get_remote_version() → 从 GitHub API 获取远程版本
- check_update() → 比较版本，返回更新状态

使用方式：
  python3 -m harness._core.update_checker        # 检查更新
  python3 -m harness._core.update_checker test  # 测试连接
"""
import json
import logging
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# 统一 sys.path 设置
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

logger = logging.getLogger(__name__)

# GitHub 仓库信息
GITHUB_REPO = "yanyinxi/claude-harness-kit"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_TAGS_URL = f"https://api.github.com/repos/{GITHUB_REPO}/tags"


@dataclass
class UpdateInfo:
    """更新信息数据结构"""
    has_update: bool
    local_version: str
    remote_version: str
    release_url: str = ""
    release_notes: str = ""
    error: Optional[str] = None


def get_local_version() -> str:
    """获取本地版本号"""
    try:
        from harness._core.version import get_version
        return get_version()
    except Exception:
        # 备用方案：直接读取 version.json
        version_json = Path(__file__).parent / "version.json"
        if version_json.exists():
            data = json.loads(version_json.read_text(encoding="utf-8"))
            return data.get("version", "0.0.0")
        return "0.0.0"


def parse_version(version_str: str) -> tuple:
    """
    解析版本字符串，返回 (major, minor, patch) 元组

    支持格式：
    - "0.9.1" -> (0, 9, 1)
    - "v0.9.1" -> (0, 9, 1)
    - "0.9.1-beta" -> (0, 9, 1)  # 忽略预发布标签
    """
    # 去除 'v' 前缀
    version_str = version_str.lstrip('v')
    # 只保留 semver 主版本号
    parts = version_str.split('-')[0].split('.')
    try:
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return (major, minor, patch)
    except (ValueError, IndexError):
        return (0, 0, 0)


def compare_versions(local: str, remote: str) -> int:
    """
    比较两个版本号

    返回：
    - 1  if local > remote
    - 0  if local == remote
    - -1 if local < remote
    """
    local_info = parse_version(local)
    remote_info = parse_version(remote)

    if local_info > remote_info:
        return 1
    elif local_info < remote_info:
        return -1
    else:
        return 0


def get_remote_version() -> tuple[str, str, str]:
    """
    从 GitHub 获取最新版本

    返回：
    - (version, release_url, release_notes)
    - 失败时返回 ("0.0.0", "", "")
    """
    import ssl

    # 备用方案 1：使用 curl（更可靠的环境兼容性）
    try:
        import subprocess
        result = subprocess.run(
            [
                "curl", "-s", "--max-time", "10",
                "-H", "Accept: application/vnd.github+json",
                "-H", "User-Agent: CHK-Update-Checker/1.0",
                GITHUB_API_URL
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            tag_name = data.get("tag_name", "")
            html_url = data.get("html_url", "")
            body = data.get("body", "")[:500]
            return (tag_name, html_url, body)
    except Exception as e:
        logger.debug(f"Curl 方式获取版本失败: {e}")

    # 备用方案 2：使用本地 git tags
    try:
        import subprocess
        result = subprocess.run(
            ["git", "tag", "--sort=-version:refname"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            tags = result.stdout.strip().split("\n")
            for tag in tags:
                # 跳过 semver 预发布标签以外的其他标签
                if tag.startswith("v") or tag[0].isdigit():
                    return (tag, f"https://github.com/{GITHUB_REPO}/releases/tag/{tag}", "")
    except Exception as e:
        logger.debug(f"Git tag 方式获取版本失败: {e}")

    # 备用方案 3：创建 SSL 上下文重试
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "CHK-Update-Checker/1.0",
            }
        )

        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            data = json.loads(response.read().decode('utf-8'))
            tag_name = data.get("tag_name", "")
            html_url = data.get("html_url", "")
            body = data.get("body", "")[:500]
            return (tag_name, html_url, body)
    except Exception as e:
        logger.debug(f"SSL 重试也失败: {e}")

    return ("0.0.0", "", "")


def check_update() -> UpdateInfo:
    """
    检查插件更新

    返回 UpdateInfo：
    - has_update: 是否有新版本
    - local_version: 本地版本
    - remote_version: 远程版本
    - release_url: Release URL
    - release_notes: 更新日志摘要
    """
    local_version = get_local_version()

    try:
        remote_version, release_url, release_notes = get_remote_version()

        comparison = compare_versions(local_version, remote_version)
        has_update = comparison < 0  # 本地 < 远程

        return UpdateInfo(
            has_update=has_update,
            local_version=local_version,
            remote_version=remote_version,
            release_url=release_url,
            release_notes=release_notes[:200] if release_notes else "",
        )

    except Exception as e:
        return UpdateInfo(
            has_update=False,
            local_version=local_version,
            remote_version="未知",
            error=str(e),
        )


def format_update_message(info: UpdateInfo) -> str:
    """格式化更新通知消息"""
    if info.error:
        return f"[CHK 更新检查失败: {info.error}]"

    if not info.has_update:
        return ""  # 无更新时不显示消息

    lines = [
        "",
        "=" * 50,
        "🔔 CHK 插件更新可用",
        "=" * 50,
        f"当前版本: {info.local_version}",
        f"最新版本: {info.remote_version}",
        "",
        "更新命令:",
        "  claude plugins update chk",
        "",
    ]

    if info.release_notes:
        lines.extend([
            "更新内容:",
            f"  {info.release_notes[:100]}...",
            "",
        ])

    if info.release_url:
        lines.append(f"详情: {info.release_url}")

    lines.append("=" * 50)

    return "\n".join(lines)


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description="CHK 插件更新检测器")
    parser.add_argument("action", nargs="?", default="check", help="操作: check/test")
    args = parser.parse_args()

    if args.action == "test":
        print("测试 GitHub 连接...")
        version, url, notes = get_remote_version()
        print(f"最新版本: {version}")
        print(f"Release URL: {url}")
        return

    # 默认执行检查
    info = check_update()

    if info.has_update:
        message = format_update_message(info)
        print(message)
    else:
        print(f"[CHK] 当前版本 {info.local_version} 已是最新")


if __name__ == "__main__":
    main()