#!/usr/bin/env python3
"""
path_guard.py — CHK 路径守卫模块

强制验证路径访问权限，防止越界操作。

功能:
- 路径白名单验证
- 危险路径拦截
- 跨项目隔离
- 目录访问控制

危险路径模式（自动拒绝）:
- / 系统根目录
- ~/.ssh/ 密钥目录
- 生产环境配置目录

使用方式:
    from path_guard import validate_path, is_dangerous, check_access
"""
import os
import re
from typing import Optional

# 危险路径模式（正则）
DANGEROUS_PATTERNS = [
    r"^/$",                          # 根目录 /
    r"^/etc/ssh",                    # SSH 配置
    r"^/root/\.ssh",                # root SSH 密钥
    r"^/var/lib/mysql",             # MySQL 数据
    r"^/usr/local/bin",              # 系统 bin
    r"\.ssh/authorized_keys",       # SSH 授权密钥
    r"password\.json$",              # 密码文件
    r"\.env\.prod$",                 # 生产环境配置
]

# 危险命令模式
DANGEROUS_COMMANDS = [
    r"rm\s+-rf\s+/",                # 删根
    r"dd\s+if=.*of=/dev/",          # 磁盘写入
    r">\s*/etc/",                   # 修改系统配置
    r"chmod\s+-R\s+777",            # 开放 777 权限
]


class PathGuard:
    """路径守卫"""

    def __init__(self, allowed_dirs: Optional[list[str]] = None):
        """
        初始化路径守卫

        Args:
            allowed_dirs: 允许访问的目录白名单
        """
        self.allowed_dirs = allowed_dirs or []
        self._compile_patterns()

    def _compile_patterns(self):
        """编译危险模式"""
        self._dangerous_path_re = [
            re.compile(p, re.IGNORECASE) for p in DANGEROUS_PATTERNS
        ]
        self._dangerous_cmd_re = [
            re.compile(p, re.IGNORECASE) for p in DANGEROUS_COMMANDS
        ]

    def is_dangerous_path(self, path: str) -> bool:
        """
        检查路径是否危险

        Args:
            path: 待检查路径

        Returns:
            True 如果路径危险
        """
        abs_path = os.path.realpath(path)  # 解析符号链接，防止路径穿越

        # 检查危险模式
        for pattern in self._dangerous_path_re:
            if pattern.search(abs_path):
                return True

        # 检查是否在允许目录内
        if self.allowed_dirs and not self._in_allowed_dir(abs_path):
            return True

        return False

    def is_dangerous_command(self, command: str) -> bool:
        """
        检查命令是否危险

        Args:
            command: 待检查命令

        Returns:
            True 如果命令危险
        """
        for pattern in self._dangerous_cmd_re:
            if pattern.search(command):
                return True
        return False

    def _in_allowed_dir(self, abs_path: str) -> bool:
        """检查路径是否在允许目录内（使用 os.sep 防止 /tmp-foo 被 /tmp 误匹配）"""
        for allowed in self.allowed_dirs:
            allowed_abs = os.path.abspath(allowed)
            if abs_path == allowed_abs or abs_path.startswith(allowed_abs + os.sep):
                return True
        return False

    def validate_path(self, path: str) -> tuple[bool, Optional[str]]:
        """
        验证路径是否可访问

        Args:
            path: 待验证路径

        Returns:
            (is_valid, error_message)
        """
        if self.is_dangerous_path(path):
            return False, f"路径不在允许范围内或属于危险路径: {path}"

        return True, None

    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """
        验证命令是否安全

        Args:
            command: 待验证命令

        Returns:
            (is_valid, error_message)
        """
        if self.is_dangerous_command(command):
            return False, f"危险命令: {command[:50]}..."

        return True, None


def validate_path_scope(path: str, allowed_dirs: list[str] | None = None) -> bool:
    """
    验证路径是否在白名单内（顶层函数，供 paths.py 调用）

    Args:
        path: 待验证路径
        allowed_dirs: 允许目录列表

    Returns:
        True 如果在白名单内
    """
    guard = PathGuard(allowed_dirs)
    return not guard.is_dangerous_path(path)


def check_access(path: str, allowed_dirs: list[str] | None = None) -> bool:
    """
    检查路径访问权限

    Args:
        path: 待检查路径
        allowed_dirs: 允许目录列表

    Returns:
        True 如果有权限
    """
    if allowed_dirs is None:
        allowed_dirs = [os.getcwd()]

    guard = PathGuard(allowed_dirs)
    is_valid, _ = guard.validate_path(path)
    return is_valid


# 全局守卫实例
_guard: Optional[PathGuard] = None


def get_guard() -> PathGuard:
    """获取全局路径守卫"""
    global _guard
    if _guard is None:
        _guard = PathGuard()
    return _guard


def main():
    """测试"""
    guard = PathGuard(allowed_dirs=["/Users/yanyinxi/工作/code/github"])

    # 测试危险路径
    tests = [
        ("/Users/yanyinxi/工作/code/github/claude-harness-kit/index.js", True),
        ("/etc/passwd", False),
        ("/Users/yanyinxi/.ssh/id_rsa", False),
        ("/tmp/test", True),
    ]

    print("Path Guard Tests:")
    for path, expected in tests:
        is_valid, error = guard.validate_path(path)
        status = "✓" if is_valid == expected else "✗"
        print(f"  {status} {path[:50]}: valid={is_valid}, expected={expected}")


if __name__ == "__main__":
    main()