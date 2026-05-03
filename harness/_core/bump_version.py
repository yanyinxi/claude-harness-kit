#!/usr/bin/env python3
"""
智能版本管理系统 - 自动分析变更类型

作用: 集中管理项目版本号，确保所有文件同步更新
原理: 所有文件的 version 字段从 harness/_core/version.json 读取，
      通过 bump_version.py 升级时自动同步到其他文件

使用:
  python bump_version.py auto     # 自动分析提交类型并升级
  python bump_version.py patch    # 手动指定为 patch 版本
  python bump_version.py minor    # 手动指定为 minor 版本
  python bump_version.py major    # 手动指定为 major 版本
"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# version.json 位置（相对于此脚本）
VERSION_JSON = Path(__file__).parent / "version.json"
# CHANGELOG 文件位置
CHANGELOG_FILE = Path(__file__).parent.parent.parent / "CHANGELOG.md"

# 需要同步版本的文件列表（统一从 version.json 读取）
# 注意: 每次升级版本时，这些文件都会被更新
UPDATE_FILES = [
    "package.json",
    "package-lock.json",
    "index.js",
    ".claude-plugin/plugin.json",
    "harness/marketplace.json",
    ".claude-plugin/marketplace.json",
]

VERSION_TYPES = {
    "patch": {"emoji": "🔧", "description": "Bug fixes"},
    "minor": {"emoji": "✨", "description": "New features"},
    "major": {"emoji": "💥", "description": "Breaking changes"},
}


def read_version() -> dict:
    """读取 version.json，返回版本数据（不含文件时返回默认值）"""
    if not VERSION_JSON.exists():
        return {"version": "0.0.0", "version_info": [0, 0, 0], "name": "unknown"}
    return json.loads(VERSION_JSON.read_text())


def write_version(data: dict):
    """保存版本数据到 version.json"""
    VERSION_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def get_git_diff_count() -> int:
    """获取自上次 git tag 后的提交数量（用于判断变更量）"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, cwd=VERSION_JSON.parent.parent.parent
        )
        last_tag = result.stdout.strip()
        if last_tag:
            count = subprocess.run(
                ["git", "rev-list", f"{last_tag}..HEAD", "--count"],
                capture_output=True, text=True, cwd=VERSION_JSON.parent.parent.parent
            )
            return int(count.stdout.strip()) if count.returncode == 0 else 0
    except Exception:
        pass
    return 0


def analyze_commits() -> dict:
    """分析最近 git 提交，自动判断版本升级类型

    判断逻辑:
      - 包含 "break"/"major" 关键字 → major (破坏性变更)
      - 包含 "feat"/"feature"/"new" 关键字 → minor (新功能)
      - 包含 "fix"/"bug" 关键字 → patch (修复)
      - 默认 → patch

    返回: {"type": "patch|minor|major", "reason": "判断原因"}
    """
    root = VERSION_JSON.parent.parent.parent

    try:
        # 获取最近10条提交信息
        result = subprocess.run(
            ["git", "log", "-10", "--pretty=format:%s"],
            capture_output=True, text=True, cwd=root
        )
        commits = result.stdout.strip().split("\n") if result.returncode == 0 else []

        # 检查是否包含破坏性变更关键字
        has_breaking = any(w in c.lower() for c in commits for w in ["break", "major", "破坏"])
        if has_breaking:
            return {"type": "major", "reason": "Breaking changes detected in commits"}

        # 检查是否包含新功能关键字
        has_feature = any(w in c.lower() for c in commits for w in ["feat", "feature", "new", "功能"])
        if has_feature:
            return {"type": "minor", "reason": "New features detected in commits"}

        # 检查是否包含修复关键字
        has_fix = any(w in c.lower() for c in commits for w in ["fix", "bug", "修复"])
        if has_fix:
            return {"type": "patch", "reason": "Bug fixes detected in commits"}

    except Exception:
        pass

    # 默认 patch 更新
    return {"type": "patch", "reason": "Default: patch update"}


def update_file(path: Path, old_ver: str, new_ver: str):
    """更新单个文件中的版本号（字符串替换）

    作用: 将文件中的旧版本号替换为新版本号
    原理: 直接文本替换，匹配 old_ver 字符串
    注意: 如果文件不存在或不含旧版本号则跳过
    """
    if not path.exists():
        print(f"  [SKIP] {path} not found")
        return
    content = path.read_text()
    if old_ver in content:
        path.write_text(content.replace(old_ver, new_ver))
        print(f"  [UPDATE] {path}")


def generate_changelog(old_ver: str, new_ver: str, version_type: str) -> str:
    """生成 CHANGELOG 条目（Markdown 格式）

    作用: 记录版本变更内容
    原理: 读取新旧版本之间的 git 提交，生成变更列表
    """
    root = VERSION_JSON.parent.parent.parent
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        # 获取新旧版本之间的提交（用版本号作为参考点）
        result = subprocess.run(
            ["git", "log", f"{old_ver}..HEAD", "--oneline"],
            capture_output=True, text=True, cwd=root
        )
        commits = result.stdout.strip().split("\n") if result.returncode == 0 else []
        # 最多取前 10 条
        commits = [c for c in commits if c][:10]
    except Exception:
        commits = []

    # 格式化为 Markdown 列表
    changes = "\n".join(f"- {c}" for c in commits) if commits else "- (no commits)"

    return f"""## {new_ver} ({date}) {VERSION_TYPES[version_type]['emoji']}

**Type:** {version_type} - {VERSION_TYPES[version_type]['description']}

### Changes
{changes}

"""


def smart_bump(force_type: str = None) -> dict:
    """智能升级版本号

    作用: 根据变更类型自动递增版本号
    原理:
      - patch: 0.0.1 → 0.0.2
      - minor: 0.1.0 → 0.2.0
      - major: 1.0.0 → 2.0.0

    Args:
        force_type: 强制指定版本类型（可选，默认自动分析）
    Returns:
        包含 old_ver, new_ver, type, reason, data 的字典
    """
    data = read_version()
    old_ver = data["version"]
    major, minor, patch = data["version_info"]

    # 确定版本类型
    if force_type:
        # 手动指定类型
        version_type = force_type
        reason = f"Manual: {force_type} forced"
    else:
        # 自动分析
        analysis = analyze_commits()
        version_type = analysis["type"]
        reason = analysis["reason"]

    # 递增版本号
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    new_ver = f"{major}.{minor}.{patch}"

    # 更新内存中的版本数据
    data["version"] = new_ver
    data["version_info"] = [major, minor, patch]
    data["last_bump"] = datetime.now().isoformat()
    data["last_type"] = version_type

    return {
        "old_ver": old_ver,
        "new_ver": new_ver,
        "type": version_type,
        "reason": reason,
        "data": data
    }


def main():
    """主入口: 解析命令行参数，执行版本升级"""
    data = read_version()
    old_ver = data.get("version", "0.0.0")

    # 无参数时显示帮助信息
    if len(sys.argv) < 2:
        print(f"📦 Current version: {old_ver}")
        print(f"\n📖 Usage:")
        print(f"  python bump_version.py auto      # Auto-detect (smart)")
        print(f"  python bump_version.py patch     # Bug fixes")
        print(f"  python bump_version.py minor     # New features")
        print(f"  python bump_version.py major    # Breaking changes")

        # 显示智能分析结果（不实际升级）
        analysis = analyze_commits()
        print(f"\n🤖 Smart analysis:")
        print(f"  Suggested: {analysis['type']} ({analysis['reason']})")

        # 显示 git 统计
        diff_count = get_git_diff_count()
        if diff_count > 0:
            print(f"  Commits since last tag: {diff_count}")
        return

    # 解析命令
    arg = sys.argv[1].lower()
    if arg == "auto":
        result = smart_bump()
    elif arg in ["major", "minor", "patch"]:
        result = smart_bump(force_type=arg)
    else:
        print(f"Invalid: {arg}")
        sys.exit(1)

    # 提取结果
    old_ver = result["old_ver"]
    new_ver = result["new_ver"]
    version_type = result["type"]
    reason = result["reason"]
    data = result["data"]

    # 输出升级信息
    print(f"\n🚀 Version: {old_ver} → {new_ver}")
    print(f"   Type: {VERSION_TYPES[version_type]['emoji']} {version_type}")
    print(f"   Reason: {reason}")

    # 1. 保存到 version.json
    write_version(data)
    print(f"\n📝 Updated version.json")

    # 2. 同步到其他文件
    print(f"\n📄 Updating files:")
    root = Path(__file__).parent.parent.parent
    for rel_path in UPDATE_FILES:
        update_file(root / rel_path, old_ver, new_ver)

    # 3. 生成 changelog
    changelog_entry = generate_changelog(old_ver, new_ver, version_type)
    print(f"\n📒 Changelog entry:")
    print(changelog_entry)

    print(f"\n✅ Done: {new_ver}")


if __name__ == "__main__":
    main()