#!/usr/bin/env python3
"""
cache_manager.py — CHK Prompt 缓存管理器

管理 Prompt 缓存生命周期，实现知识预加载和上下文优化。

功能:
- 缓存命中统计
- 缓存失效检测
- 按场景选择加载内容
- 优先级管理（CLAUDE.md > Rules > Instinct > Knowledge Index）

缓存优先级（从高到低）:
1. 项目 CLAUDE.md (200 tokens)
2. 团队 Rules (3-5 个规则)
3. 本能记录 (前 20 条高置信度)
4. 知识库索引 (仅索引，不加载内容)
"""
import atexit
import json
import time
from typing import Optional

from ..paths import (
    ROOT, DATA_DIR, RULES_DIR, INSTINCT_FILE
)

# 缓存配置
CACHE_CONFIG = {
    "max_tokens": 500,           # 最大预加载 tokens（严格限制）
    "max_age_seconds": 3600,     # 缓存有效期 1 小时
    "preload_rules_count": 5,    # 预加载规则数
    "preload_instinct_count": 20, # 预加载本能记录数
}

# 缓存文件路径
CACHE_INDEX_FILE = DATA_DIR / "cache_index.json"
CACHE_STATS_FILE = DATA_DIR / "cache_stats.json"


class CacheStats:
    """缓存命中统计"""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.total_bytes = 0
        self.last_load_time = 0.0

    def record_hit(self, size_bytes: int):
        self.hits += 1
        self.total_bytes += size_bytes

    def record_miss(self):
        self.misses += 1

    def record_load(self, duration_ms: float):
        self.last_load_time = duration_ms

    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hit_rate(),
            "total_bytes": self.total_bytes,
            "last_load_time_ms": self.last_load_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CacheStats":
        stats = cls()
        stats.hits = data.get("hits", 0)
        stats.misses = data.get("misses", 0)
        stats.total_bytes = data.get("total_bytes", 0)
        stats.last_load_time = data.get("last_load_time_ms", 0.0)
        return stats


class CacheEntry:
    """缓存条目"""

    def __init__(self, key: str, content: str, priority: int = 1):
        self.key = key
        self.content = content
        self.priority = priority  # 1-5, 越高越重要
        self.created_at = time.time()
        self.last_accessed = self.created_at
        self.access_count = 0

    def is_expired(self, max_age: int = 3600) -> bool:
        """检查是否过期"""
        return (time.time() - self.created_at) > max_age

    def access(self):
        """记录访问"""
        self.last_accessed = time.time()
        self.access_count += 1

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "content": self.content[:200] + "..." if len(self.content) > 200 else self.content,
            "priority": self.priority,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
        }


class CacheManager:
    """Prompt 缓存管理器"""

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._stats = CacheStats()
        self._load_from_disk()
        # 注册进程退出时自动保存缓存
        atexit.register(self.flush)

    def _load_from_disk(self):
        """从磁盘加载缓存索引"""
        if CACHE_INDEX_FILE.exists():
            try:
                data = json.loads(CACHE_INDEX_FILE.read_text())
                for item in data.get("entries", []):
                    entry = CacheEntry(item["key"], item.get("content", ""), item.get("priority", 1))
                    entry.created_at = item.get("created_at", time.time())
                    entry.last_accessed = item.get("last_accessed", time.time())
                    entry.access_count = item.get("access_count", 0)
                    if not entry.is_expired(CACHE_CONFIG["max_age_seconds"]):
                        self._cache[item["key"]] = entry
            except (json.JSONDecodeError, OSError):
                pass

        if CACHE_STATS_FILE.exists():
            try:
                self._stats = CacheStats.from_dict(json.loads(CACHE_STATS_FILE.read_text()))
            except (json.JSONDecodeError, OSError):
                pass

    def _save_to_disk(self):
        """保存缓存索引到磁盘"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "entries": [
                {
                    "key": k,
                    "content": v.content,
                    "priority": v.priority,
                    "created_at": v.created_at,
                    "last_accessed": v.last_accessed,
                    "access_count": v.access_count,
                }
                for k, v in self._cache.items()
            ],
            "saved_at": time.time(),
        }
        CACHE_INDEX_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

        # 保存统计
        CACHE_STATS_FILE.write_text(json.dumps(self._stats.to_dict(), indent=2))

    def get(self, key: str) -> Optional[str]:
        """获取缓存内容"""
        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired(CACHE_CONFIG["max_age_seconds"]):
                entry.access()
                self._stats.record_hit(len(entry.content))
                return entry.content
            else:
                del self._cache[key]
        self._stats.record_miss()
        return None

    def set(self, key: str, content: str, priority: int = 1):
        """设置缓存"""
        self._cache[key] = CacheEntry(key, content, priority)

    def flush(self):
        """显式保存缓存到磁盘（供外部调用或进程退出时使用）"""
        self._save_to_disk()

    def invalidate(self, key: str):
        """使缓存失效"""
        if key in self._cache:
            del self._cache[key]
            self._save_to_disk()

    def get_preload_content(self) -> str:
        """
        获取预加载内容（按优先级排序）

        返回格式化的 Markdown 字符串，注入到上下文。
        """
        lines = ["\n# Preloaded Context\n"]

        # 1. 项目 CLAUDE.md
        claude_md = ROOT / "CLAUDE.md"
        if claude_md.exists():
            content = claude_md.read_text()
            # 限制 200 tokens
            lines.append(f"## Project Context\n{content[:600]}\n")

        # 2. 团队 Rules（优先级排序）
        if RULES_DIR.exists():
            rules = sorted(RULES_DIR.glob("*.md"))[:CACHE_CONFIG["preload_rules_count"]]
            for rule in rules:
                content = rule.read_text()
                lines.append(f"## Rule: {rule.stem}\n{content[:300]}\n")

        # 3. 高置信度本能记录
        instinct_content = self._load_instinct_preload()
        if instinct_content:
            lines.append(instinct_content)

        return "\n".join(lines)

    def _load_instinct_preload(self) -> Optional[str]:
        """加载本能记录预热内容"""
        if not INSTINCT_FILE.exists():
            return None

        try:
            data = json.loads(INSTINCT_FILE.read_text())
            records = data.get("records", []) if isinstance(data, dict) else data

            # 过滤高置信度记录
            high_conf = [r for r in records if isinstance(r, dict) and r.get("confidence", 0) >= 0.7]
            high_conf = sorted(high_conf, key=lambda x: x.get("confidence", 0), reverse=True)
            high_conf = high_conf[:CACHE_CONFIG["preload_instinct_count"]]

            if not high_conf:
                return None

            lines = ["## Recent Instincts\n"]
            for rec in high_conf:
                context = rec.get("context", {})
                correction = rec.get("correction", "")
                confidence = rec.get("confidence", 0)
                domain = context.get("domain", "unknown") if isinstance(context, dict) else "unknown"
                lines.append(f"- [{domain}] {correction[:100]} (conf: {confidence:.2f})")

            return "\n".join(lines)
        except (json.JSONDecodeError, OSError, KeyError):
            return None

    @property
    def stats(self) -> CacheStats:
        return self._stats


# 全局缓存管理器实例
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """获取全局缓存管理器"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def preload_knowledge() -> str:
    """
    预加载知识（供 Hook 调用）

    返回格式化的预加载内容。
    """
    manager = get_cache_manager()
    return manager.get_preload_content()


def main():
    """CLI 测试"""
    manager = get_cache_manager()
    print("Cache Manager Status:")
    print(f"  Entries: {len(manager._cache)}")
    print(f"  Hit Rate: {manager.stats.hit_rate():.1%}")
    print(f"  Total Hits: {manager.stats.hits}")
    print(f"  Total Misses: {manager.stats.misses}")
    print("\nPreload Content Preview:")
    print(manager.get_preload_content()[:500] + "...")


if __name__ == "__main__":
    main()