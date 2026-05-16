"""CHK 版本管理 - 从 version.json 读取"""
import json
from functools import lru_cache
from pathlib import Path

VERSION_JSON = Path(__file__).parent / "version.json"


@lru_cache(maxsize=1)
def _read_version_data():
    """读取版本数据（带缓存，避免重复 IO）"""
    if VERSION_JSON.exists():
        return json.loads(VERSION_JSON.read_text())
    return {}


def get_version() -> str:
    """获取当前版本"""
    return _read_version_data().get("version", "0.0.0")


def get_version_info() -> tuple:
    """获取版本信息 (major, minor, patch)"""
    return tuple(_read_version_data().get("version_info", [0, 0, 0]))


__version__ = get_version()
__version_info__ = get_version_info()