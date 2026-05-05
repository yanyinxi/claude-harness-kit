#!/usr/bin/env python3
"""
_load_env.py — 统一环境变量加载模块

所有入口脚本统一导入此模块，确保 .env 在任何入口下都能被加载。
放在任意 .py 同级目录下，通过相对路径自动查找。
"""
import os
from pathlib import Path

_loaded = False


def load_env():
    """从 .env 文件加载环境变量（幂等调用，首次生效）"""
    global _loaded
    if _loaded:
        return
    _loaded = True

    # 向上查找 .env（支持从任意子目录调用）
    cursor = Path(__file__).resolve().parent
    for _ in range(5):  # 最多向上5层
        env_file = cursor / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip()
                    if key and value and value != "sk-ant-your-key-here":
                        os.environ.setdefault(key, value)
            break
        parent = cursor.parent
        if parent == cursor:
            break
        cursor = parent


load_env()
