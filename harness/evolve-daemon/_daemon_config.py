#!/usr/bin/env python3
"""
统一配置加载模块
所有 evolve-daemon 子模块的 load_config() 统一入口
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

# ── Claude Code 配置自动加载（延迟） ─────────────────────────────────────────

_env_loaded = False


def _ensure_env_loaded():
    """从 Claude Code 配置自动加载环境变量"""
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True
    settings_path = Path.home() / ".claude" / "settings.json"
    if not settings_path.exists():
        return
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        for key, value in settings.get("env", {}).items():
            os.environ.setdefault(key, str(value))
    except (json.JSONDecodeError, OSError):
        pass


_ensure_env_loaded()


# ── 各模块默认配置 ────────────────────────────────────────────────────────────

_DEFAULT_CONFIGS: Dict[str, Dict[str, Any]] = {
    "daemon": {
        "daemon": {
            "mode": "external",
            "scheduler_interval": "30 minutes",
            "schedule": "*/30 * * * *",
            "idle_trigger_minutes": 120,
            "extract_timeout_seconds": 5,
        },
        "thresholds": {
            "min_new_sessions": 1,
            "min_same_pattern_corrections": 2,
            "max_hours_since_last_analyze": 6,
        },
        "safety": {
            "max_proposals_per_day": 3,
            "auto_close_days": 7,
            "breaker": {"max_consecutive_rejects": 3, "pause_days": 30},
        },
        "paths": {
            "data_dir": ".claude/data",
            "proposals_dir": ".claude/proposals",
            "skills_dir": "skills",
            "agents_dir": "agents",
            "rules_dir": "rules",
            "instinct_dir": "memory",
        },
    },
    "apply_change": {
        "paths": {
            "data_dir": ".claude/data",
            "proposals_dir": ".claude/proposals",
            "skills_dir": "skills",
            "agents_dir": "agents",
            "rules_dir": "rules",
            "instinct_dir": "memory",
            "backups_dir": ".claude/data/backups",
        },
        "observation": {"days": 7},
        "safety": {
            "breaker": {"max_consecutive_rejects": 3, "pause_days": 30},
        },
    },
    "llm_decision": {
        "decision": {
            "enabled": True,
            "auto_apply_threshold": 0.8,
            "high_risk_threshold": 0.5,
        },
        "claude_api": {
            "decide_model": os.environ.get("ANTHROPIC_MODEL") or "claude-sonnet-4-6-20250514",
            "decide_max_tokens": 2048,
            "decide_temperature": 0.2,
        },
        "paths": {
            "data_dir": ".claude/data",
            "proposals_dir": ".claude/proposals",
            "skills_dir": "skills",
            "agents_dir": "agents",
            "rules_dir": "rules",
            "instinct_dir": "memory",
        },
        "safety": {
            "breaker": {"max_consecutive_rejects": 3, "pause_days": 30},
        },
    },
    "validator": {
        "validation": {
            "enabled": True,
            "quarantine_malformed": True,
            "max_age_days": 90,
        },
    },
    "instinct_updater": {
        "decay": {
            "half_life_days": 90,
            "decay_floor": 0.1,
            "min_reinforcement": 3,
            "reinforcement_bonus": 0.05,
            "max_confidence": 0.95,
        },
    },
    "rollback": {
        "observation": {
            "days": 7,
            "check_interval_hours": 24,
        },
        "safety": {
            "breaker": {
                "max_consecutive_rejects": 3,
                "pause_days": 30,
                "max_rollbacks_per_week": 5,
            },
        },
        "paths": {
            "data_dir": ".claude/data",
        },
    },
    "scheduler": {
        "daemon": {
            "mode": "external",
            "scheduler_interval": "30 minutes",
            "run_on_startup": False,
            "heartbeat_check_minutes": 180,
            "auto_start_on_install": True,
        },
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    """深度合并两个字典，override 覆盖 base"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(module: Optional[str] = None) -> dict:
    """
    统一配置加载入口。

    用法：
        from evolve_daemon_config import load_config

        # 加载 daemon 配置（默认）
        config = load_config("daemon")

        # 加载所有模块配置（合并版）
        config = load_config()

        # 加载单个模块配置（带 yaml 覆盖）
        config = load_config("apply_change")

    逻辑：
    1. 如果 module 指定，读取该模块目录下的 config.yaml，存在则与默认配置深度合并
    2. 如果 module 为 None，返回包含所有模块默认配置的字典
    3. yaml 不可用时自动回退到纯默认配置
    """
    if module is None:
        # 返回所有模块的默认配置
        return {k: v for k, v in _DEFAULT_CONFIGS.items()}

    defaults = _DEFAULT_CONFIGS.get(module, {})
    config_path = Path(__file__).parent / "config.yaml"

    if not config_path.exists():
        return defaults

    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        return _deep_merge(defaults, user_config)
    except ImportError:
        return defaults
    except Exception:
        return defaults


# ── 兼容性别名（各模块原有接口）───────────────────────────────────────────────

def _default_config():
    """向后兼容：返回 daemon 默认配置（负载最重的模块）"""
    return load_config("daemon")


# ── 便捷访问器 ───────────────────────────────────────────────────────────────

def get(module: str, key: str, default=None):
    """快速获取配置值: get("daemon", "thresholds.min_new_sessions")"""
    config = load_config(module)
    keys = key.split(".")
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
            if value is None:
                return default
        else:
            return default
    return value if value is not None else default