"""CHK (Claude Harness Kit) — 内部引擎包

本包包含 CHK 插件的所有 Python 运行时逻辑：
  paths         — 全局路径配置中枢
  _core         — 核心基础设施（版本管理、缓存、路径守卫、本能引擎）
  evolve-daemon — 自动进化守护进程（分析→提案→应用→回滚）
  knowledge     — 双知识库推荐引擎（手工 + 进化）
  cli           — CLI 工具和执行模式管理

使用方式:
  from harness.paths import HARNESS_DIR, EVOLVE_DIR
  from harness._core.exceptions import handle_exception
"""
