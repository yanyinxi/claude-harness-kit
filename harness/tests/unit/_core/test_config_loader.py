#!/usr/bin/env python3
"""
ConfigLoader 单元测试

测试配置加载器的所有功能
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# 导入被测试模块
from harness._core.config_loader import ConfigLoader, get_loader, get_version, get_config


class TestConfigLoaderInit:
    """ConfigLoader 初始化测试"""

    def test_default_project_root(self):
        """默认使用项目根目录"""
        loader = ConfigLoader()
        assert loader.project_root.exists()
        assert (loader.project_root / "harness").exists()

    def test_custom_project_root(self, tmp_path):
        """支持自定义项目根目录"""
        loader = ConfigLoader(tmp_path)
        assert loader.project_root == tmp_path

    def test_cache_initialized(self):
        """缓存初始化为空"""
        loader = ConfigLoader()
        assert loader._cache == {}
        assert loader._version is None


class TestConfigLoaderGetConfig:
    """配置获取测试"""

    def test_load_core_config(self, tmp_path):
        """加载核心配置"""
        # 创建测试 version.json
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0", "version_info": [1, 0, 0]}')

        loader = ConfigLoader(tmp_path)
        config = loader.get_config("core")
        assert config["version"] == "1.0.0"
        assert config["version_info"] == [1, 0, 0]

    def test_load_missing_core_returns_defaults(self, tmp_path):
        """缺失配置文件使用默认值"""
        loader = ConfigLoader(tmp_path)
        config = loader.get_config("core")
        assert config["version"] == "0.0.0"
        assert config["version_info"] == [0, 0, 0]

    def test_load_package_json(self, tmp_path):
        """加载 package.json"""
        pkg_file = tmp_path / "package.json"
        pkg_file.write_text('{"name": "test-pkg", "version": "2.0.0"}')

        loader = ConfigLoader(tmp_path)
        config = loader.get_config("package")
        assert config["name"] == "test-pkg"
        assert config["version"] == "2.0.0"

    def test_load_missing_package_returns_defaults(self, tmp_path):
        """缺失 package.json 使用默认值"""
        loader = ConfigLoader(tmp_path)
        config = loader.get_config("package")
        assert config == {}

    def test_load_settings_with_override(self, tmp_path):
        """settings.local.json 覆盖 settings.json"""
        # 创建默认 settings
        settings = tmp_path / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text('{"model": "opus", "theme": "dark"}')

        # 创建本地覆盖
        local = tmp_path / ".claude" / "settings.local.json"
        local.write_text('{"theme": "light"}')

        loader = ConfigLoader(tmp_path)
        config = loader.get_config("settings")
        assert config["model"] == "opus"
        assert config["theme"] == "light"

    def test_load_hooks_config(self, tmp_path):
        """加载 hooks 配置"""
        hooks_file = tmp_path / "harness" / "hooks" / "hooks.json"
        hooks_file.parent.mkdir(parents=True)
        hooks_file.write_text('{"hooks": {"PreToolUse": []}}')

        loader = ConfigLoader(tmp_path)
        config = loader.get_config("hooks")
        assert "hooks" in config
        assert config["hooks"]["PreToolUse"] == []

    def test_unsupported_config_type_raises(self, tmp_path):
        """不支持的配置类型抛出异常"""
        loader = ConfigLoader(tmp_path)
        with pytest.raises(ValueError, match="Unsupported config type"):
            loader.get_config("invalid_type")


class TestConfigLoaderCache:
    """缓存测试"""

    def test_cache_reuse(self, tmp_path):
        """配置缓存复用"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)

        # 第一次加载
        config1 = loader.get_config("core", use_cache=True)
        # 第二次加载应使用缓存
        config2 = loader.get_config("core", use_cache=True)
        assert config1 is config2

    def test_bypass_cache(self, tmp_path):
        """绕过缓存强制重新加载"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)

        config1 = loader.get_config("core", use_cache=True)
        config2 = loader.get_config("core", use_cache=False)
        assert config1 is not config2
        assert config1["version"] == config2["version"]

    def test_reload_specific_config(self, tmp_path):
        """重载指定配置"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)
        loader.get_config("core", use_cache=True)

        # 修改文件
        version_file.write_text('{"version": "2.0.0"}')

        # 不重载，不应更新
        config1 = loader.get_config("core", use_cache=True)
        assert config1["version"] == "1.0.0"

        # 重载后应更新
        loader.reload("core")
        config2 = loader.get_config("core", use_cache=True)
        assert config2["version"] == "2.0.0"

    def test_reload_all_config(self, tmp_path):
        """重载全部配置"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)
        loader.get_config("core", use_cache=True)

        # 重载全部
        loader.reload()
        assert loader._cache == {}
        assert loader._version is None


class TestConfigLoaderVersion:
    """版本相关测试"""

    def test_get_version_from_package(self, tmp_path):
        """优先从 package.json 获取版本"""
        pkg_file = tmp_path / "package.json"
        pkg_file.write_text('{"version": "1.2.3"}')

        loader = ConfigLoader(tmp_path)
        assert loader.get_version() == "1.2.3"

    def test_get_version_from_core(self, tmp_path):
        """从 version.json 获取版本"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "2.0.0"}')

        # 不创建 package.json
        loader = ConfigLoader(tmp_path)
        assert loader.get_version() == "2.0.0"

    def test_get_version_fallback(self, tmp_path):
        """版本不存在时回退到 0.0.0"""
        loader = ConfigLoader(tmp_path)
        assert loader.get_version() == "0.0.0"

    def test_get_version_info(self, tmp_path):
        """获取版本信息列表"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version_info": [3, 1, 2]}')

        loader = ConfigLoader(tmp_path)
        assert loader.get_version_info() == [3, 1, 2]

    def test_get_version_info_fallback(self, tmp_path):
        """版本信息不存在时回退"""
        loader = ConfigLoader(tmp_path)
        assert loader.get_version_info() == [0, 0, 0]


class TestConfigLoaderCLIMode:
    """CLI 模式测试"""

    def test_get_cli_mode(self, tmp_path):
        """获取指定 CLI 模式"""
        modes_dir = tmp_path / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)
        (modes_dir / "solo.json").write_text('{"agents": ["executor"], "max_agents": 1}')

        loader = ConfigLoader(tmp_path)
        mode = loader.get_cli_mode("solo")
        assert mode["agents"] == ["executor"]
        assert mode["max_agents"] == 1

    def test_get_nonexistent_cli_mode(self, tmp_path):
        """获取不存在的模式返回 None"""
        loader = ConfigLoader(tmp_path)
        assert loader.get_cli_mode("nonexistent") is None

    def test_get_all_cli_modes(self, tmp_path):
        """获取所有可用模式"""
        modes_dir = tmp_path / "harness" / "cli" / "modes"
        modes_dir.mkdir(parents=True)
        (modes_dir / "solo.json").write_text('{}')
        (modes_dir / "team.json").write_text('{}')

        loader = ConfigLoader(tmp_path)
        modes = loader.get_all_cli_modes()
        assert "solo" in modes
        assert "team" in modes


class TestConfigLoaderDaemon:
    """Daemon 配置测试"""

    def test_get_daemon_config(self, tmp_path):
        """获取 daemon 配置"""
        config_file = tmp_path / "harness" / "evolve-daemon" / "config.yaml"
        config_file.parent.mkdir(parents=True)
        config_file.write_text('daemon:\n  mode: "scheduler"\n  scheduler_interval: "1 hour"\n')

        loader = ConfigLoader(tmp_path)
        daemon = loader.get_daemon_config()
        assert daemon["mode"] == "scheduler"
        assert daemon["scheduler_interval"] == "1 hour"

    def test_get_daemon_config_key(self, tmp_path):
        """获取 daemon 特定配置项"""
        config_file = tmp_path / "harness" / "evolve-daemon" / "config.yaml"
        config_file.parent.mkdir(parents=True)
        config_file.write_text('daemon:\n  mode: "both"\n')

        loader = ConfigLoader(tmp_path)
        mode = loader.get_daemon_config("mode")
        assert mode == "both"

    def test_get_daemon_config_default(self, tmp_path):
        """daemon 配置不存在使用默认值"""
        loader = ConfigLoader(tmp_path)
        daemon = loader.get_daemon_config()
        assert daemon["mode"] == "both"
        assert daemon["scheduler_interval"] == "30 minutes"


class TestConfigLoaderValidate:
    """配置验证测试"""

    def test_validate_all(self, tmp_path):
        """验证所有配置"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)
        results = loader.validate_all()

        assert "core" in results
        assert results["core"]["status"] == "ok"
        assert results["core"]["exists"] is True


class TestConfigLoaderClearCache:
    """清空缓存测试"""

    def test_clear_cache(self, tmp_path):
        """清空所有缓存"""
        version_file = tmp_path / "harness" / "_core" / "version.json"
        version_file.parent.mkdir(parents=True)
        version_file.write_text('{"version": "1.0.0"}')

        loader = ConfigLoader(tmp_path)
        loader.get_config("core")

        assert len(loader._cache) > 0
        loader.clear_cache()
        assert loader._cache == {}
        assert loader._version is None


class TestGlobalFunctions:
    """全局便捷函数测试"""

    def test_get_version_function(self):
        """get_version() 全局函数"""
        version = get_version()
        assert isinstance(version, str)

    def test_get_config_function(self):
        """get_config() 全局函数"""
        config = get_config("core")
        assert isinstance(config, dict)

    def test_get_loader_singleton(self, tmp_path):
        """get_loader() 单例模式"""
        loader1 = get_loader(tmp_path)
        loader2 = get_loader(tmp_path)
        assert loader1 is loader2


class TestConfigLoaderRepr:
    """__repr__ 测试"""

    def test_repr(self, tmp_path):
        """repr 输出正确"""
        loader = ConfigLoader(tmp_path)
        repr_str = repr(loader)
        assert "ConfigLoader" in repr_str
        assert str(tmp_path) in repr_str


class TestConfigLoaderMerge:
    """字典合并测试"""

    def test_merge_simple(self):
        """简单字典合并"""
        loader = ConfigLoader()
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = loader._merge(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_nested(self):
        """嵌套字典合并"""
        loader = ConfigLoader()
        base = {"outer": {"a": 1, "b": 2}}
        override = {"outer": {"b": 3, "c": 4}}
        result = loader._merge(base, override)
        assert result["outer"] == {"a": 1, "b": 3, "c": 4}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])