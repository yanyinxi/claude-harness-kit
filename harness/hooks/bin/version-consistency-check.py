#!/usr/bin/env python3
"""
版本一致性检查器

作用: 在 git commit 前自动运行，确保所有文件的 version 字段一致
原理: 从 harness/_core/version.json 读取标准版本，逐个检查其他文件
目的: 防止版本号不一致导致发布问题

使用:
  python3 version-consistency-check.py    # 手动检查
  (通常由 git pre-commit hook 自动调用)

检查的文件:
  - package.json
  - package-lock.json
  - index.js
  - .claude-plugin/plugin.json
  - harness/marketplace.json
  - .claude-plugin/marketplace.json
"""
import json
import subprocess
import sys
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────────────────────────
# 从 version.json 读取标准版本
# 注意: 脚本位于 harness/hooks/bin/，需要向上 4 层才能到达项目根目录
# bin -> hooks -> harness -> 项目根目录
SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parent.parent.parent.parent
VERSION_JSON = ROOT / "harness" / "_core" / "version.json"

# 备用路径（如果在 harness/_core/ 下找不到）
if not VERSION_JSON.exists():
    VERSION_JSON = ROOT / "_core" / "version.json"

# 安全检查: 确保 version.json 存在
if not VERSION_JSON.exists():
    print(f"❌ version.json not found at {VERSION_JSON}")
    sys.exit(1)

# 需要检查版本一致性的文件列表
# 注意: 这些文件需要在 bump_version.py 的 UPDATE_FILES 中保持同步
VERSION_FILES = [
    "package.json",
    "package-lock.json",
    "index.js",
    ".claude-plugin/plugin.json",
    "harness/marketplace.json",
    ".claude-plugin/marketplace.json",
]


def get_standard_version() -> str:
    """获取标准版本号（从 version.json）"""
    if not VERSION_JSON.exists():
        print(f"❌ {VERSION_JSON} 不存在")
        sys.exit(1)
    data = json.loads(VERSION_JSON.read_text())
    return data.get("version", "unknown")


def find_version_in_dict(obj) -> str | None:
    """在字典中递归查找 version 字段

    作用: 支持嵌套的 version 字段（如 metadata.version）
    原因: marketplace.json 的版本在 metadata 嵌套对象中
    """
    if isinstance(obj, dict):
        if "version" in obj:
            return obj["version"]
        # 搜索常见嵌套路径
        for key in ["metadata", "info", "package"]:
            if key in obj and isinstance(obj[key], dict):
                v = find_version_in_dict(obj[key])
                if v:
                    return v
    return None


def get_file_version(path: Path) -> str | None:
    """从单个文件中提取 version 字段

    作用: 解析不同类型文件的版本号
    支持:
      - JSON 文件: 支持顶层和嵌套的 version 字段
      - JS 文件: 支持 module.exports.version、exports.version 等格式
    返回: 版本号字符串，解析失败返回 None
    """
    if not path.exists():
        return None
    try:
        content = path.read_text()

        # JSON 文件解析
        if path.suffix == ".json":
            parsed = json.loads(content)
            return find_version_in_dict(parsed)

        # JS 文件解析（使用正则表达式匹配多种格式）
        elif path.suffix == ".js":
            import re
            # 匹配模式:
            #   module.exports.version = "1.0.0"
            #   exports.version = "1.0.0"
            #   version: "1.0.0"
            patterns = [
                r'module\.exports\.version\s*=\s*["\']([^"\']+)["\']',
                r'exports\.version\s*=\s*["\']([^"\']+)["\']',
                r'version:\s*["\']([^"\']+)["\']',
            ]
            for pattern in patterns:
                m = re.search(pattern, content)
                if m:
                    return m.group(1)
        return None
    except Exception:
        return None


def check_versions() -> bool:
    """检查所有文件版本是否与标准版本一致

    作用: 遍历 VERSION_FILES 列表，逐个检查版本号
    返回: True 表示全部一致，False 表示存在不一致
    """
    standard = get_standard_version()
    print(f"📦 标准版本: {standard}\n")

    mismatches = []
    for rel_path in VERSION_FILES:
        path = ROOT / rel_path
        ver = get_file_version(path)

        if ver is None:
            # 文件不存在或无法解析
            print(f"  ⚠️  {rel_path:<35} (文件不存在或无法解析)")
        elif ver == standard:
            # 版本一致
            print(f"  ✅ {rel_path:<35} v{ver}")
        else:
            # 版本不一致
            print(f"  ❌ {rel_path:<35} v{ver} (应为 v{standard})")
            mismatches.append(rel_path)

    print()
    if mismatches:
        # 存在不一致，打印修复提示
        print(f"❌ 版本不一致！以下 {len(mismatches)} 个文件需要同步：")
        for f in mismatches:
            print(f"   - {f}")
        print(f"\n💡 运行以下命令修复：")
        print(f"   cd {ROOT}")
        print(f"   python harness/_core/bump_version.py auto")
        return False

    print("✅ 所有文件版本一致")
    return True


def main():
    """主入口: 检查版本一致性并返回退出码"""
    # 检查是否在 git 工作目录中
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode != 0:
        # 不在 git 仓库中，跳过检查
        sys.exit(0)

    # 执行版本检查
    if not check_versions():
        sys.exit(1)


if __name__ == "__main__":
    main()