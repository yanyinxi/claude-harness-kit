# Capability Registry (语义化版)
> 自动生成于 2026-05-17 17:31:02
> 用途：AI 代码理解、模块调用、场景匹配

---

## 模块地图

| 模块 | 类型 | 一句话描述 | 场景 |
|------|------|-----------|------|
| `harness/_core/bump_version.py` | python | 智能版本管理系统 - 自动分析变更类型 | version |
| `harness/_core/cache_manager.py` | python | cache_manager. | memory/evolution |
| `harness/_core/config_loader.py` | python | ConfigLoader - 统一配置加载器 | config/cli/evolution |
| `harness/_core/exceptions.py` | python | 统一异常处理工具模块 | error |
| `harness/_core/instinct_engine.py` | python | instinct_engine. | memory/skill/agent |
| `harness/_core/instinct_reader.py` | python | 本能读取模块 - 从 instinct-record. | memory |
| `harness/_core/instinct_state.py` | python | 本能状态管理模块 - 跟踪当前会话已注入的本能 | memory |
| `harness/_core/keyword_matcher.py` | python | 关键词匹配模块 - 根据用户输入匹配相关记忆 | memory |
| `harness/_core/path_guard.py` | python | path_guard. | path/hook/config |
| `harness/_core/update_checker.py` | python | CHK 插件更新检测器 - 从 GitHub 获取最新版本并比较 | version |
| `harness/_core/version.py` | python | CHK 版本管理 - 从 version. | version |
| `harness/cli/capability-analyzer.py` | python | Capability Registry 分析器 v2 — 语义化输出 | skill/cli |
| `harness/cli/gc.py` | python | 知识垃圾回收 CLI — kit gc 命令。 | path/agent/cli |
| `harness/cli/generate_skill_index.py` | python | Generate INDEX. | skill/cli |
| `harness/cli/init.py` | python | kit init — 自动分析项目，生成高质量 CLAUDE.md 和 .cla | path/version/config |
| `harness/cli/instinct_cli.py` | python | instinct_cli. | memory/evolution/version |
| `harness/cli/migrate.py` | python | kit migrate — 项目迁移编排器。 | agent/cli |
| `harness/cli/mode.py` | python | chk mode — 切换 Claude Code 执行模式。 | agent/hook/config |
| `harness/cli/scan.py` | python | kit scan — 扫描多代码库目录，评估改造量。 | path/cli |
| `harness/cli/status.py` | python | kit status — 查看 Claude Harness Kit 当前状态。 | memory/hook/config |
| `harness/cli/sync.py` | python | kit sync — 从中央配置仓库同步团队共享规则。 | config/cli |
| `harness/evolve-daemon/agent_evolution.py` | python | Agent 维度进化策略 | agent/evolution |
| `harness/evolve-daemon/analyzer.py` | python | 数据分析器 — 聚合多会话数据，识别改进模式。 | agent/skill/evolution |
| `harness/evolve-daemon/apply_change.py` | python | 自动应用模块 — 根据 LLM 决策自动应用改动。 | memory/evolution |
| `harness/evolve-daemon/daemon.py` | python | 进化守护进程入口 — 支持外部触发和内置定时任务。 | memory/agent/config |
| `harness/evolve-daemon/effect_tracker.py` | python | 效果跟踪器 - 跟踪进化改进的有效性 | memory/agent/skill |
| `harness/evolve-daemon/evolve_dispatcher.py` | python | 进化分发器 — 8维度分析决策引擎 | memory/skill/evolution |
| `harness/evolve-daemon/extract_semantics.py` | python | 语义提取器封装 — 为 daemon.py 提供 analyze_session | memory/evolution/hook |
| `harness/evolve-daemon/generalize.py` | python | generalize. | evolution/error |
| `harness/evolve-daemon/instinct_updater.py` | python | Instinct 自动更新器 — 管理本能记录的完整生命周期。 | memory/evolution/error |
| `harness/evolve-daemon/integrated_evolution.py` | python | integrated_evolution. | hook/config/evolution |
| `harness/evolve-daemon/kb_shared.py` | python | kb_shared. | memory/config/cli |
| `harness/evolve-daemon/llm_decision.py` | python | LLM 决策引擎 — 用 LLM 分析会话数据，决定下一步行动。 | memory/evolution/config |
| `harness/evolve-daemon/memory_sync.py` | python | 知识同步模块 - 将进化系统产生的知识同步到 MEMORY. | memory/evolution |
| `harness/evolve-daemon/proposer.py` | python | 提案生成器 — 调用 Claude API 进行深度分析，生成结构化改进提案。 | memory/evolution/agent |
| `harness/evolve-daemon/rollback.py` | python | 自动回滚模块 — 观察期验证效果，自动回滚恶化的改动。 | memory/evolution/agent |
| `harness/evolve-daemon/rule_evolution.py` | python | Rule 维度进化策略 | evolution |
| `harness/evolve-daemon/scheduler.py` | python | 内置定时任务调度器 — 基于 APScheduler 实现异步定时触发。 | evolution/hook |
| `harness/evolve-daemon/skill_evolution.py` | python | Skill 维度进化策略 | skill/evolution |
| `harness/evolve-daemon/update_notifier.py` | python | CHK 插件更新通知器 - 管理更新通知状态，避免重复提示 | evolution |
| `harness/evolve-daemon/validator.py` | python | 数据验证器 — 验证 sessions.jsonl 格式，隔离异常数据。 | evolution/error |
| `harness/knowledge/doc_generator.py` | python | doc-generator. | agent/error |
| `harness/knowledge/knowledge_recommender.py` | python | Knowledge Recommender Engine — 知识推荐引擎 | memory/agent/skill |
| `harness/knowledge/lifecycle.py` | python | Knowledge Lifecycle Engine — 知识生命周期可执行引擎 | version/path/agent |
| `harness/paths.py` | python | paths. | memory/agent/config |
| `harness/tests/check_directory_and_safety.py` | python | 目录结构与安全全面测试套件 | memory/agent/cli |
| `harness/tests/graders/base.py` | python | LLM Grader 基类 | skill/agent/error |
| `harness/tests/graders/pass_at_k.py` | python | Pass@k 指标计算 | skill |
| `hooks/bin/agent-planning-check.sh` | shell | !/bin/bash Agent Planning Check - PreAge | path/agent/hook |
| `hooks/bin/agent-result-sync.sh` | shell | !/bin/bash Agent Result Sync - PostAgent | path/agent/hook |
| `hooks/bin/architecture-verify.sh` | shell | !/bin/bash architecture-verify.sh - 架构决策 | path/hook/error |
| `hooks/bin/check-update.sh` | shell | !/bin/bash ============================= | path/version/hook |
| `hooks/bin/checkpoint-auto-save.sh` | shell | !/bin/bash checkpoint-auto-save.sh — Pre | hook |
| `hooks/bin/checkpoint-verify.sh` | shell | !/bin/bash checkpoint-verify.sh - 验证 Che | path/hook/error |
| `hooks/bin/coverage-check.sh` | shell | !/bin/bash coverage-check.sh — 测试覆盖率门禁 当 | hook |
| `hooks/bin/doc-verify.sh` | shell | !/usr/bin/env bash doc-verify.sh - 文档验证器 | path/hook/error |
| `hooks/bin/ensure-settings.sh` | shell | !/bin/bash ============================= | hook/config |
| `hooks/bin/git-commit-check.sh` | shell | !/bin/bash git-commit-check.sh - 检查 Git  | hook/cli |
| `hooks/bin/log-utils.sh` | shell | !/bin/bash ============================= | path/hook/error |
| `hooks/bin/memory-cleanup.sh` | shell | !/bin/bash ============================= | memory/hook/cli |
| `hooks/bin/memory-inject.sh` | shell | !/bin/bash ============================= | memory/hook |
| `hooks/bin/notify.sh` | shell | !/bin/bash notify.sh - 飞书 Webhook 通知脚本 用 | hook/config/cli |
| `hooks/bin/observe.sh` | shell | !/bin/bash observe.sh — Hook 观测事件采集器（she | path/hook/error |
| `hooks/bin/quality-gate.sh` | shell | !/bin/bash quality-gate.sh — PostToolUse | hook/config/error |
| `hooks/bin/rate-limiter.sh` | shell | !/bin/bash rate-limiter.sh — Claude Code | hook |
| `hooks/bin/safety-check.sh` | shell | !/bin/bash safety-check.sh — PreToolUse  | hook/cli |
| `hooks/bin/security-auto-trigger.sh` | shell | !/bin/bash security-auto-trigger.sh — Po | hook |
| `hooks/bin/tdd-check.sh` | shell | !/bin/bash tdd-check.sh — PreToolUse Hoo | hook |
| `hooks/bin/update-registry-on-commit.sh` | shell | !/bin/bash ============================= | hook/cli |
| `hooks/bin/update-registry.sh` | shell | !/bin/bash ============================= | path/hook |
| `index.js` | javascript |  | - |

## 按场景分组

### 场景: AGENT

<!-- CAPABILITY:harness/_core/instinct_engine.py -->
#### `harness/_core/instinct_engine.py`

**一句话**: instinct_engine.
**类型**: python
**路径**: `harness/_core/instinct_engine.py`

**核心能力**:
  - `InstinctEngine`: 本能推理引擎...
  - `get_engine()`: 获取全局本能引擎...
  - `get_recommendations()`: 获取推荐（顶层函数）...
  - `update_confidence()`: 更新置信度（顶层函数）...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/gc.py -->
#### `harness/cli/gc.py`

**一句话**: 知识垃圾回收 CLI — kit gc 命令。
**类型**: python
**路径**: `harness/cli/gc.py`

**核心能力**:
  - `run_gc_agent()`: 通过 Claude Code CLI 调用 GC Agent...
  - `generate_fallback_report()`: 无 Claude Code 时生成基础扫描报告...
  - `main()`

<!-- CAPABILITY:harness/cli/migrate.py -->
#### `harness/cli/migrate.py`

**一句话**: kit migrate — 项目迁移编排器。
**类型**: python
**路径**: `harness/cli/migrate.py`

**核心能力**:
  - `validate_playbook()`: 验证 playbook 是否有效...
  - `generate_report()`: 生成迁移报告...
  - `main()`

<!-- CAPABILITY:harness/cli/mode.py -->
#### `harness/cli/mode.py`

**一句话**: chk mode — 切换 Claude Code 执行模式。
**类型**: python
**路径**: `harness/cli/mode.py`

**核心能力**:
  - `load_mode_template()`: 加载指定模式的 hook 配置模板...
  - `load_settings()`: 加载或初始化 settings.local.json...
  - `save_settings()`: 保存 settings.local.json...
  - `switch_mode()`: 切换到指定模式...
  - `show_current_mode()`: 显示当前模式...

<!-- CAPABILITY:harness/evolve-daemon/agent_evolution.py -->
#### `harness/evolve-daemon/agent_evolution.py`

**一句话**: Agent 维度进化策略
**类型**: python
**路径**: `harness/evolve-daemon/agent_evolution.py`

**核心能力**:
  - `evolve_agent()`
  - `_generate_agent_change()`

<!-- CAPABILITY:harness/evolve-daemon/analyzer.py -->
#### `harness/evolve-daemon/analyzer.py`

**一句话**: 数据分析器 — 聚合多会话数据，识别改进模式。
**类型**: python
**路径**: `harness/evolve-daemon/analyzer.py`

**核心能力**:
  - `_safe_div()`: 安全除法，避免除零...
  - `parse_iso_time()`: 解析 ISO 时间字符串，支持 Z 和时区后缀...
  - `aggregate_and_analyze()`
  - `_analyze_performance()`: 性能维度分析：
- 工具调用耗时统计
- 识别超时模式
- 统计平均响应时间...
  - `_analyze_interaction()`: 交互质量维度分析：
- 分析会话轮次
- 统计任务完成时间
- 用户满意度推断...

<!-- CAPABILITY:harness/evolve-daemon/daemon.py -->
#### `harness/evolve-daemon/daemon.py`

**一句话**: 进化守护进程入口 — 支持外部触发和内置定时任务。
**类型**: python
**路径**: `harness/evolve-daemon/daemon.py`

**核心能力**:
  - `handle_exception()`: 统一异常处理包装函数（本地定义避免循环依赖）...
  - `_stop_scheduler()`: 停止调度器（共享逻辑）...
  - `_save_state()`: 保存状态（共享逻辑）...
  - `graceful_shutdown()`: 优雅退出处理函数...
  - `graceful_restart()`: 优雅重启处理函数（SIGUSR1）...

<!-- CAPABILITY:harness/evolve-daemon/effect_tracker.py -->
#### `harness/evolve-daemon/effect_tracker.py`

**一句话**: 效果跟踪器 - 跟踪进化改进的有效性
**类型**: python
**路径**: `harness/evolve-daemon/effect_tracker.py`

**核心能力**:
  - `EffectTracker`: 效果跟踪器...
  - `main()`: 测试效果跟踪器...

<!-- CAPABILITY:harness/evolve-daemon/proposer.py -->
#### `harness/evolve-daemon/proposer.py`

**一句话**: 提案生成器 — 调用 Claude API 进行深度分析，生成结构化改进提案。
**类型**: python
**路径**: `harness/evolve-daemon/proposer.py`

**核心能力**:
  - `generate_proposal()`: 生成改进提案。调用 Claude API 进行深度分析。
底层使用 kb_shared.get_ll...
  - `_call_claude_api()`: 调用 Claude API — 优先使用统一 SDK 客户端，降级为 REST API...
  - `_generate_with_claude()`: 使用 Claude API 生成高质量提案...
  - `_generate_from_template()`: 降级：使用模板生成提案（无需 API Key）...
  - `_save_proposal()`: 保存提案文件...

<!-- CAPABILITY:harness/evolve-daemon/rollback.py -->
#### `harness/evolve-daemon/rollback.py`

**一句话**: 自动回滚模块 — 观察期验证效果，自动回滚恶化的改动。
**类型**: python
**路径**: `harness/evolve-daemon/rollback.py`

**核心能力**:
  - `load_proposal_history()`: 加载提案历史...
  - `save_proposal_history()`: 保存提案历史...
  - `collect_metrics()`
  - `evaluate_proposal()`: 评估是否应该保留或回滚。

返回: (decision, triggers) — decision ...
  - `check_circuit_breaker()`: 检查熔断器状态。

返回: (is_triggered, reason)...

<!-- CAPABILITY:harness/knowledge/doc_generator.py -->
#### `harness/knowledge/doc_generator.py`

**一句话**: doc-generator.
**类型**: python
**路径**: `harness/knowledge/doc_generator.py`

**核心能力**:
  - `DocMetadata`: 文档元数据...
  - `_log_error()`: 记录错误到 error.jsonl（复用现有系统）...
  - `_escape_html()`: HTML 转义...
  - `is_separator_row()`: 检测表格分隔行（|---|:| 格式）...
  - `_parse_markdown()`: Markdown 转 HTML（基础实现）...
  - `_get_default_template()`: 默认 HTML 模板...

<!-- CAPABILITY:harness/knowledge/knowledge_recommender.py -->
#### `harness/knowledge/knowledge_recommender.py`

**一句话**: Knowledge Recommender Engine — 知识推荐引擎
**类型**: python
**路径**: `harness/knowledge/knowledge_recommender.py`

**核心能力**:
  - `load_evolved_knowledge()`: 加载进化知识库 (JSONL 格式)...
  - `load_knowledge_base()`: 加载所有知识条目（双知识库合并）

知识库 1: harness/knowledge/ — 手工维护...
  - `load_instinct_usage()`: 从 instinct 数据读取历史使用频率...
  - `extract_keywords()`: 从文本中提取关键词（过滤停用词）...
  - `compute_score()`: 计算单条知识的推荐分数...

<!-- CAPABILITY:harness/knowledge/lifecycle.py -->
#### `harness/knowledge/lifecycle.py`

**一句话**: Knowledge Lifecycle Engine — 知识生命周期可执行引擎。
**类型**: python
**路径**: `harness/knowledge/lifecycle.py`

**核心能力**:
  - `load_lifecycle_config()`: 加载 lifecycle.yaml 配置，失败则使用内联默认值...
  - `check_maturity_promotion()`: 检查条目是否可以升级。
返回: "verified" | "proven" | None...
  - `apply_decay()`: 检查条目是否应该衰减降级。
返回: 目标成熟度 | None（无需降级）...
  - `promote_to_layer1()`: 跨项目提升：L3 → L1/L2。
生成提升提案到 proposals/ 目录。
返回: 提案文件路...
  - `cmd_check()`: 检查单条知识的成熟度和衰减状态...

<!-- CAPABILITY:harness/paths.py -->
#### `harness/paths.py`

**一句话**: paths.
**类型**: python
**路径**: `harness/paths.py`

**核心能力**:
  - `_project_root()`
  - `_plugin_root()`
  - `sessions_file()`
  - `errors_file()`
  - `errors_lock_file()`

<!-- CAPABILITY:harness/tests/check_directory_and_safety.py -->
#### `harness/tests/check_directory_and_safety.py`

**一句话**: 目录结构与安全全面测试套件
**类型**: python
**路径**: `harness/tests/check_directory_and_safety.py`

**核心能力**:
  - `ok()`
  - `fail()`
  - `test_harness_whitelist_subdirs()`: 正向: harness/ 下只允许白名单子目录...
  - `test_no_harness_nested()`: 安全: harness/ 下禁止嵌套另一个 harness/...
  - `test_no_code_in_claude_dir()`: 安全: .claude/ 下只允许 data/ 和 proposals/...

<!-- CAPABILITY:harness/tests/graders/base.py -->
#### `harness/tests/graders/base.py`

**一句话**: LLM Grader 基类
**类型**: python
**路径**: `harness/tests/graders/base.py`

**核心能力**:
  - `GradingResult`: 评分结果...
  - `BaseGrader`: 评分器基类...
  - `CodeQualityGrader`: 代码质量评分器...
  - `OutputQualityGrader`: 输出质量评分器...
  - `BehaviorGrader`: 行为评分器 - 验证 Agent/Skill 行为是否符合预期...

<!-- CAPABILITY:hooks/bin/agent-planning-check.sh -->
#### `hooks/bin/agent-planning-check.sh`

**一句话**: !/bin/bash Agent Planning Check - PreAgentCall Hook 验证多 Agent 任务分配合理性 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-planning-check.sh`

**核心能力**:
  - `log()`
  - `main()`

<!-- CAPABILITY:hooks/bin/agent-result-sync.sh -->
#### `hooks/bin/agent-result-sync.sh`

**一句话**: !/bin/bash Agent Result Sync - PostAgentCall Hook 同步 Agent 执行结果到 mailbox 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-result-sync.sh`

**核心能力**:
  - `log()`
  - `main()`

### 场景: CLI

<!-- CAPABILITY:harness/_core/config_loader.py -->
#### `harness/_core/config_loader.py`

**一句话**: ConfigLoader - 统一配置加载器
**类型**: python
**路径**: `harness/_core/config_loader.py`

**核心能力**:
  - `ConfigLoader`: 统一配置加载器...
  - `get_loader()`: 获取全局配置加载器实例

Args:
    project_root: 项目根目录

Return...
  - `reload()`: 重新加载全局配置...
  - `get_version()`: 获取 CHK 版本...
  - `get_config()`: 获取指定类型的配置...
  - `validate_all()`: 验证所有配置...

<!-- CAPABILITY:harness/cli/capability-analyzer.py -->
#### `harness/cli/capability-analyzer.py`

**一句话**: Capability Registry 分析器 v2 — 语义化输出
**类型**: python
**路径**: `harness/cli/capability-analyzer.py`

**核心能力**:
  - `SemanticAnalyzer`: 语义化分析器...
  - `generate_semantic_registry()`: 生成语义化注册表...
  - `main()`

<!-- CAPABILITY:harness/cli/gc.py -->
#### `harness/cli/gc.py`

**一句话**: 知识垃圾回收 CLI — kit gc 命令。
**类型**: python
**路径**: `harness/cli/gc.py`

**核心能力**:
  - `run_gc_agent()`: 通过 Claude Code CLI 调用 GC Agent...
  - `generate_fallback_report()`: 无 Claude Code 时生成基础扫描报告...
  - `main()`

<!-- CAPABILITY:harness/cli/generate_skill_index.py -->
#### `harness/cli/generate_skill_index.py`

**一句话**: Generate INDEX.
**类型**: python
**路径**: `harness/cli/generate_skill_index.py`

**核心能力**:
  - `generate_index()`
  - `main()`

<!-- CAPABILITY:harness/cli/migrate.py -->
#### `harness/cli/migrate.py`

**一句话**: kit migrate — 项目迁移编排器。
**类型**: python
**路径**: `harness/cli/migrate.py`

**核心能力**:
  - `validate_playbook()`: 验证 playbook 是否有效...
  - `generate_report()`: 生成迁移报告...
  - `main()`

<!-- CAPABILITY:harness/cli/scan.py -->
#### `harness/cli/scan.py`

**一句话**: kit scan — 扫描多代码库目录，评估改造量。
**类型**: python
**路径**: `harness/cli/scan.py`

**核心能力**:
  - `scan_directory()`: 扫描目录下所有项目...
  - `main()`

<!-- CAPABILITY:harness/cli/sync.py -->
#### `harness/cli/sync.py`

**一句话**: kit sync — 从中央配置仓库同步团队共享规则。
**类型**: python
**路径**: `harness/cli/sync.py`

**核心能力**:
  - `_hash_file()`: 计算文件 SHA256（用于增量同步）...
  - `find_root()`
  - `_get_default_source()`: 获取默认团队仓库 URL...
  - `sync_from_local()`: 从本地目录同步，返回同步统计...
  - `sync_from_git()`: 从 Git 仓库同步...

<!-- CAPABILITY:harness/evolve-daemon/kb_shared.py -->
#### `harness/evolve-daemon/kb_shared.py`

**一句话**: kb_shared.
**类型**: python
**路径**: `harness/evolve-daemon/kb_shared.py`

**核心能力**:
  - `_ensure_env_loaded()`: 从 Claude Code 配置自动加载环境变量（幂等，所有 LLM 模块共享）

自动读取 ~/....
  - `get_model()`: 获取统一模型（ANTHROPIC_MODEL），无则返回 None...
  - `get_haiku_model()`: 快速分类模型：有 ANTHROPIC_MODEL 用它，否则用默认 Haiku...
  - `get_sonnet_model()`: 深度分析模型：有 ANTHROPIC_MODEL 用它，否则用默认 Sonnet...
  - `get_llm_config()`: 统一 LLM 配置参数，所有模块引用此处...

<!-- CAPABILITY:harness/tests/check_directory_and_safety.py -->
#### `harness/tests/check_directory_and_safety.py`

**一句话**: 目录结构与安全全面测试套件
**类型**: python
**路径**: `harness/tests/check_directory_and_safety.py`

**核心能力**:
  - `ok()`
  - `fail()`
  - `test_harness_whitelist_subdirs()`: 正向: harness/ 下只允许白名单子目录...
  - `test_no_harness_nested()`: 安全: harness/ 下禁止嵌套另一个 harness/...
  - `test_no_code_in_claude_dir()`: 安全: .claude/ 下只允许 data/ 和 proposals/...

<!-- CAPABILITY:hooks/bin/git-commit-check.sh -->
#### `hooks/bin/git-commit-check.sh`

**一句话**: !/bin/bash git-commit-check.sh - 检查 Git 提交规范 从 general.md 提取有效类型 检查 git commit 命令 提取提交信息
**类型**: shell
**路径**: `hooks/bin/git-commit-check.sh`

<!-- CAPABILITY:hooks/bin/memory-cleanup.sh -->
#### `hooks/bin/memory-cleanup.sh`

**一句话**: !/bin/bash ============================================================ CHK 会话状态清理脚本  功能： - 清理当前会话的状
**类型**: shell
**路径**: `hooks/bin/memory-cleanup.sh`

**核心能力**:
  - `cleanup_current()`
  - `cleanup_all()`

<!-- CAPABILITY:hooks/bin/notify.sh -->
#### `hooks/bin/notify.sh`

**一句话**: !/bin/bash notify.sh - 飞书 Webhook 通知脚本 用法: ./notify.sh <type> <message> [title] 示例: ./notify.sh succ
**类型**: shell
**路径**: `hooks/bin/notify.sh`

**核心能力**:
  - `log_info()`
  - `log_error()`
  - `log_warn()`
  - `send_feishu_message()`
  - `main()`

<!-- CAPABILITY:hooks/bin/safety-check.sh -->
#### `hooks/bin/safety-check.sh`

**一句话**: !/bin/bash safety-check.sh — PreToolUse Hook: 阻止危险 Bash 命令 设计：永远 exit 0（Hook 失败不阻断工具调用），危险命令通过 hookS
**类型**: shell
**路径**: `hooks/bin/safety-check.sh`

**核心能力**:
  - `block()`

<!-- CAPABILITY:hooks/bin/update-registry-on-commit.sh -->
#### `hooks/bin/update-registry-on-commit.sh`

**一句话**: !/bin/bash ============================================================ Git Hook: 增量更新 Capability Re
**类型**: shell
**路径**: `hooks/bin/update-registry-on-commit.sh`

**核心能力**:
  - `check_code_changes()`
  - `get_changed_files()`
  - `needs_full_update()`
  - `update_registry()`
  - `show_help()`

### 场景: CONFIG

<!-- CAPABILITY:harness/_core/config_loader.py -->
#### `harness/_core/config_loader.py`

**一句话**: ConfigLoader - 统一配置加载器
**类型**: python
**路径**: `harness/_core/config_loader.py`

**核心能力**:
  - `ConfigLoader`: 统一配置加载器...
  - `get_loader()`: 获取全局配置加载器实例

Args:
    project_root: 项目根目录

Return...
  - `reload()`: 重新加载全局配置...
  - `get_version()`: 获取 CHK 版本...
  - `get_config()`: 获取指定类型的配置...
  - `validate_all()`: 验证所有配置...

<!-- CAPABILITY:harness/_core/path_guard.py -->
#### `harness/_core/path_guard.py`

**一句话**: path_guard.
**类型**: python
**路径**: `harness/_core/path_guard.py`

**核心能力**:
  - `PathGuard`: 路径守卫...
  - `validate_path_scope()`: 验证路径是否在白名单内（顶层函数，供 paths.py 调用）

Args:
    path: 待...
  - `check_access()`: 检查路径访问权限

Args:
    path: 待检查路径
    allowed_dirs: ...
  - `get_guard()`: 获取全局路径守卫...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/init.py -->
#### `harness/cli/init.py`

**一句话**: kit init — 自动分析项目，生成高质量 CLAUDE.md 和 .claude/ 配置。
**类型**: python
**路径**: `harness/cli/init.py`

**核心能力**:
  - `parse_package_json()`: 从 package.json 提取依赖和版本...
  - `parse_pom_xml()`: 从 pom.xml 提取关键依赖...
  - `parse_go_mod()`: 从 go.mod 提取依赖...
  - `discover_structure()`: 发现关键目录、入口文件、模块边界...
  - `extract_git_insights()`: 从 git log 提取最近的 fix/refactor 关键词热点...

<!-- CAPABILITY:harness/cli/mode.py -->
#### `harness/cli/mode.py`

**一句话**: chk mode — 切换 Claude Code 执行模式。
**类型**: python
**路径**: `harness/cli/mode.py`

**核心能力**:
  - `load_mode_template()`: 加载指定模式的 hook 配置模板...
  - `load_settings()`: 加载或初始化 settings.local.json...
  - `save_settings()`: 保存 settings.local.json...
  - `switch_mode()`: 切换到指定模式...
  - `show_current_mode()`: 显示当前模式...

<!-- CAPABILITY:harness/cli/status.py -->
#### `harness/cli/status.py`

**一句话**: kit status — 查看 Claude Harness Kit 当前状态。
**类型**: python
**路径**: `harness/cli/status.py`

**核心能力**:
  - `load_settings()`
  - `count_files()`
  - `main()`

<!-- CAPABILITY:harness/cli/sync.py -->
#### `harness/cli/sync.py`

**一句话**: kit sync — 从中央配置仓库同步团队共享规则。
**类型**: python
**路径**: `harness/cli/sync.py`

**核心能力**:
  - `_hash_file()`: 计算文件 SHA256（用于增量同步）...
  - `find_root()`
  - `_get_default_source()`: 获取默认团队仓库 URL...
  - `sync_from_local()`: 从本地目录同步，返回同步统计...
  - `sync_from_git()`: 从 Git 仓库同步...

<!-- CAPABILITY:harness/evolve-daemon/daemon.py -->
#### `harness/evolve-daemon/daemon.py`

**一句话**: 进化守护进程入口 — 支持外部触发和内置定时任务。
**类型**: python
**路径**: `harness/evolve-daemon/daemon.py`

**核心能力**:
  - `handle_exception()`: 统一异常处理包装函数（本地定义避免循环依赖）...
  - `_stop_scheduler()`: 停止调度器（共享逻辑）...
  - `_save_state()`: 保存状态（共享逻辑）...
  - `graceful_shutdown()`: 优雅退出处理函数...
  - `graceful_restart()`: 优雅重启处理函数（SIGUSR1）...

<!-- CAPABILITY:harness/evolve-daemon/integrated_evolution.py -->
#### `harness/evolve-daemon/integrated_evolution.py`

**一句话**: integrated_evolution.
**类型**: python
**路径**: `harness/evolve-daemon/integrated_evolution.py`

**核心能力**:
  - `collect_session_errors()`: 收集本会话的错误。
只收集最近 max_age_hours 小时内的新错误。...
  - `_extract_context()`: 从错误条目中提取上下文...
  - `run_session_evolution()`: 会话级进化主流程。

每次会话结束时调用。...
  - `_load_config()`: 加载配置...
  - `run_full_analysis()`: 不限制会话，强制分析所有未知错误...

<!-- CAPABILITY:harness/evolve-daemon/kb_shared.py -->
#### `harness/evolve-daemon/kb_shared.py`

**一句话**: kb_shared.
**类型**: python
**路径**: `harness/evolve-daemon/kb_shared.py`

**核心能力**:
  - `_ensure_env_loaded()`: 从 Claude Code 配置自动加载环境变量（幂等，所有 LLM 模块共享）

自动读取 ~/....
  - `get_model()`: 获取统一模型（ANTHROPIC_MODEL），无则返回 None...
  - `get_haiku_model()`: 快速分类模型：有 ANTHROPIC_MODEL 用它，否则用默认 Haiku...
  - `get_sonnet_model()`: 深度分析模型：有 ANTHROPIC_MODEL 用它，否则用默认 Sonnet...
  - `get_llm_config()`: 统一 LLM 配置参数，所有模块引用此处...

<!-- CAPABILITY:harness/evolve-daemon/llm_decision.py -->
#### `harness/evolve-daemon/llm_decision.py`

**一句话**: LLM 决策引擎 — 用 LLM 分析会话数据，决定下一步行动。
**类型**: python
**路径**: `harness/evolve-daemon/llm_decision.py`

**核心能力**:
  - `load_config()`: 加载配置（使用统一配置模块）...
  - `_default_config()`
  - `get_existing_targets()`: 获取 instinct 中已有的 target 列表...
  - `is_new_target()`: 判断是否是新 target（未在 instinct 中出现）...
  - `assess_risk()`: 评估风险等级（0.0 - 1.0）。

规则:
- 高风险模式（permission, securi...

<!-- CAPABILITY:harness/paths.py -->
#### `harness/paths.py`

**一句话**: paths.
**类型**: python
**路径**: `harness/paths.py`

**核心能力**:
  - `_project_root()`
  - `_plugin_root()`
  - `sessions_file()`
  - `errors_file()`
  - `errors_lock_file()`

<!-- CAPABILITY:hooks/bin/ensure-settings.sh -->
#### `hooks/bin/ensure-settings.sh`

**一句话**: !/bin/bash ============================================================ CHK 项目配置保障钩子 - UserPromptSub
**类型**: shell
**路径**: `hooks/bin/ensure-settings.sh`

<!-- CAPABILITY:hooks/bin/notify.sh -->
#### `hooks/bin/notify.sh`

**一句话**: !/bin/bash notify.sh - 飞书 Webhook 通知脚本 用法: ./notify.sh <type> <message> [title] 示例: ./notify.sh succ
**类型**: shell
**路径**: `hooks/bin/notify.sh`

**核心能力**:
  - `log_info()`
  - `log_error()`
  - `log_warn()`
  - `send_feishu_message()`
  - `main()`

<!-- CAPABILITY:hooks/bin/quality-gate.sh -->
#### `hooks/bin/quality-gate.sh`

**一句话**: !/bin/bash quality-gate.sh — PostToolUse Hook: 验证代码和配置文件格式 设计：永远 exit 0，格式错误警告但不阻断 加载共享日志工具
**类型**: shell
**路径**: `hooks/bin/quality-gate.sh`

**核心能力**:
  - `block_post()`
  - `_is_impl_file()`
  - `_scan_secrets()`
  - `_check_test_missing()`

### 场景: ERROR

<!-- CAPABILITY:harness/_core/exceptions.py -->
#### `harness/_core/exceptions.py`

**一句话**: 统一异常处理工具模块
**类型**: python
**路径**: `harness/_core/exceptions.py`

**核心能力**:
  - `handle_exception()`: 统一异常处理

Args:
    e: 异常对象
    context: 错误上下文描述
   ...
  - `safe_execute()`: 安全执行函数，捕获异常返回默认值

Args:
    func: 要执行的函数
    *args...
  - `safe_json_loads()`: 安全解析 JSON，捕获 json.JSONDecodeError

Args:
    data:...
  - `safe_file_read()`: 安全读取文件内容

Args:
    file_path: 文件路径
    encoding: ...
  - `safe_file_write()`: 安全写入文件内容

Args:
    file_path: 文件路径
    content: 要...

<!-- CAPABILITY:harness/evolve-daemon/generalize.py -->
#### `harness/evolve-daemon/generalize.py`

**一句话**: generalize.
**类型**: python
**路径**: `harness/evolve-daemon/generalize.py`

**核心能力**:
  - `_has_llm_access()`: 检查是否有 LLM 调用能力（代理或真实 API Key）...
  - `call_haiku()`: 用 Haiku 做简单判断（reuse/new）...
  - `call_sonnet()`: 用 Sonnet 做深度分析（新根因、merge 风险）...
  - `call_llm_fallback()`: 无 API Key 时的本地规则降级。
用硬编码的启发式规则判断 reuse / new。...
  - `build_step1_prompt()`: 构建第一步 prompt：批量关联分析...

<!-- CAPABILITY:harness/evolve-daemon/instinct_updater.py -->
#### `harness/evolve-daemon/instinct_updater.py`

**一句话**: Instinct 自动更新器 — 管理本能记录的完整生命周期。
**类型**: python
**路径**: `harness/evolve-daemon/instinct_updater.py`

**核心能力**:
  - `_parse_iso_safe()`: 安全解析 ISO 时间字符串，失败时返回默认值...
  - `load_instinct()`: 加载或初始化 instinct-record.json...
  - `save_instinct()`: 保存 instinct-record.json...
  - `time_decay_weight()`: 计算时间衰减权重。

公式: weight = 0.5 ^ (age_days / half_lif...
  - `apply_decay_to_all()`: 对所有非 seed 记录应用时间衰减。

规则:
- seed 记录不衰减
- reinforcem...

<!-- CAPABILITY:harness/evolve-daemon/validator.py -->
#### `harness/evolve-daemon/validator.py`

**一句话**: 数据验证器 — 验证 sessions.jsonl 格式，隔离异常数据。
**类型**: python
**路径**: `harness/evolve-daemon/validator.py`

**核心能力**:
  - `validate_session()`: 验证单个 session 的格式。

返回: (is_valid, error_message)...
  - `validate_sessions_file()`: 验证 sessions.jsonl 文件。

返回:
{
    "total": 100,
   ...
  - `clean_old_sessions()`: 清理超过指定天数的 session。

返回清理统计。...
  - `get_data_quality_stats()`: 统计数据质量。

返回:
{
    "total_sessions": 100,
    "ses...
  - `run_validation()`: 运行完整验证流程。...

<!-- CAPABILITY:harness/knowledge/doc_generator.py -->
#### `harness/knowledge/doc_generator.py`

**一句话**: doc-generator.
**类型**: python
**路径**: `harness/knowledge/doc_generator.py`

**核心能力**:
  - `DocMetadata`: 文档元数据...
  - `_log_error()`: 记录错误到 error.jsonl（复用现有系统）...
  - `_escape_html()`: HTML 转义...
  - `is_separator_row()`: 检测表格分隔行（|---|:| 格式）...
  - `_parse_markdown()`: Markdown 转 HTML（基础实现）...
  - `_get_default_template()`: 默认 HTML 模板...

<!-- CAPABILITY:harness/tests/graders/base.py -->
#### `harness/tests/graders/base.py`

**一句话**: LLM Grader 基类
**类型**: python
**路径**: `harness/tests/graders/base.py`

**核心能力**:
  - `GradingResult`: 评分结果...
  - `BaseGrader`: 评分器基类...
  - `CodeQualityGrader`: 代码质量评分器...
  - `OutputQualityGrader`: 输出质量评分器...
  - `BehaviorGrader`: 行为评分器 - 验证 Agent/Skill 行为是否符合预期...

<!-- CAPABILITY:hooks/bin/architecture-verify.sh -->
#### `hooks/bin/architecture-verify.sh`

**一句话**: !/bin/bash architecture-verify.sh - 架构决策步骤验证 检查是否涉及架构相关关键词 检查是否有决策记录目录 如果涉及架构但没有决策文件，提示警告
**类型**: shell
**路径**: `hooks/bin/architecture-verify.sh`

<!-- CAPABILITY:hooks/bin/checkpoint-verify.sh -->
#### `hooks/bin/checkpoint-verify.sh`

**一句话**: !/bin/bash checkpoint-verify.sh - 验证 Checkpoint 文件是否完整 检查备份目录是否存在 关键文件列表
**类型**: shell
**路径**: `hooks/bin/checkpoint-verify.sh`

<!-- CAPABILITY:hooks/bin/doc-verify.sh -->
#### `hooks/bin/doc-verify.sh`

**一句话**: !/usr/bin/env bash doc-verify.sh - 文档验证器 Shell 包装器 用于 Claude Code hook，自动检测插件根目录 自动检测插件根目录 优先级 1: 环境
**类型**: shell
**路径**: `hooks/bin/doc-verify.sh`

**核心能力**:
  - `detect_plugin_root()`

<!-- CAPABILITY:hooks/bin/log-utils.sh -->
#### `hooks/bin/log-utils.sh`

**一句话**: !/bin/bash ============================================================ CHK 共享日志工具 — 被其他 hook 脚本 sou
**类型**: shell
**路径**: `hooks/bin/log-utils.sh`

**核心能力**:
  - `_hook_log_init()`
  - `_hook_log_error()`
  - `_hook_log_warn()`
  - `_hook_log_info()`

<!-- CAPABILITY:hooks/bin/observe.sh -->
#### `hooks/bin/observe.sh`

**一句话**: !/bin/bash observe.sh — Hook 观测事件采集器（shell wrapper） 职责：调用 observe.py，永远 exit 0，零阻塞主流程  设计原则： 1. 永远 e
**类型**: shell
**路径**: `hooks/bin/observe.sh`

<!-- CAPABILITY:hooks/bin/quality-gate.sh -->
#### `hooks/bin/quality-gate.sh`

**一句话**: !/bin/bash quality-gate.sh — PostToolUse Hook: 验证代码和配置文件格式 设计：永远 exit 0，格式错误警告但不阻断 加载共享日志工具
**类型**: shell
**路径**: `hooks/bin/quality-gate.sh`

**核心能力**:
  - `block_post()`
  - `_is_impl_file()`
  - `_scan_secrets()`
  - `_check_test_missing()`

### 场景: EVOLUTION

<!-- CAPABILITY:harness/_core/cache_manager.py -->
#### `harness/_core/cache_manager.py`

**一句话**: cache_manager.
**类型**: python
**路径**: `harness/_core/cache_manager.py`

**核心能力**:
  - `CacheStats`: 缓存命中统计...
  - `CacheEntry`: 缓存条目...
  - `CacheManager`: Prompt 缓存管理器...
  - `get_cache_manager()`: 获取全局缓存管理器...
  - `preload_knowledge()`: 预加载知识（供 Hook 调用）

返回格式化的预加载内容。...
  - `main()`: CLI 测试...

<!-- CAPABILITY:harness/_core/config_loader.py -->
#### `harness/_core/config_loader.py`

**一句话**: ConfigLoader - 统一配置加载器
**类型**: python
**路径**: `harness/_core/config_loader.py`

**核心能力**:
  - `ConfigLoader`: 统一配置加载器...
  - `get_loader()`: 获取全局配置加载器实例

Args:
    project_root: 项目根目录

Return...
  - `reload()`: 重新加载全局配置...
  - `get_version()`: 获取 CHK 版本...
  - `get_config()`: 获取指定类型的配置...
  - `validate_all()`: 验证所有配置...

<!-- CAPABILITY:harness/cli/instinct_cli.py -->
#### `harness/cli/instinct_cli.py`

**一句话**: instinct_cli.
**类型**: python
**路径**: `harness/cli/instinct_cli.py`

**核心能力**:
  - `_get_chk_version()`
  - `load_records()`
  - `save_records()`
  - `confidence_label()`
  - `confidence_bar()`

<!-- CAPABILITY:harness/evolve-daemon/agent_evolution.py -->
#### `harness/evolve-daemon/agent_evolution.py`

**一句话**: Agent 维度进化策略
**类型**: python
**路径**: `harness/evolve-daemon/agent_evolution.py`

**核心能力**:
  - `evolve_agent()`
  - `_generate_agent_change()`

<!-- CAPABILITY:harness/evolve-daemon/analyzer.py -->
#### `harness/evolve-daemon/analyzer.py`

**一句话**: 数据分析器 — 聚合多会话数据，识别改进模式。
**类型**: python
**路径**: `harness/evolve-daemon/analyzer.py`

**核心能力**:
  - `_safe_div()`: 安全除法，避免除零...
  - `parse_iso_time()`: 解析 ISO 时间字符串，支持 Z 和时区后缀...
  - `aggregate_and_analyze()`
  - `_analyze_performance()`: 性能维度分析：
- 工具调用耗时统计
- 识别超时模式
- 统计平均响应时间...
  - `_analyze_interaction()`: 交互质量维度分析：
- 分析会话轮次
- 统计任务完成时间
- 用户满意度推断...

<!-- CAPABILITY:harness/evolve-daemon/apply_change.py -->
#### `harness/evolve-daemon/apply_change.py`

**一句话**: 自动应用模块 — 根据 LLM 决策自动应用改动。
**类型**: python
**路径**: `harness/evolve-daemon/apply_change.py`

**核心能力**:
  - `backup_file()`: 备份原文件到 backups_dir...
  - `restore_file()`: 从备份恢复文件...
  - `apply_text_change()`: 应用文本改动。

change 可以是：
1. 精确替换: "old_text -> new_tex...
  - `apply_change()`: 根据 decision 自动应用改动。

返回: True 成功，False 失败...
  - `_sync_to_memory()`: 同步知识到记忆系统...

<!-- CAPABILITY:harness/evolve-daemon/evolve_dispatcher.py -->
#### `harness/evolve-daemon/evolve_dispatcher.py`

**一句话**: 进化分发器 — 8维度分析决策引擎
**类型**: python
**路径**: `harness/evolve-daemon/evolve_dispatcher.py`

**核心能力**:
  - `get_dimension()`: 根据 target 前缀确定维度。

核心维度:
  agent:xxx → agent
  ski...
  - `_load_dimension_thresholds()`: 从 config.yaml 统一加载 8 个维度的进化阈值。

阈值定义在 config.yaml ...
  - `meets_threshold()`: 判断纠正次数是否达到维度阈值。

阈值从 config.yaml 的 thresholds.dime...
  - `build_decision()`: 为指定维度构建进化决策。

返回:
{
    "dimension": str,
    "tar...
  - `_agent_decision()`: Agent 维度进化策略...

<!-- CAPABILITY:harness/evolve-daemon/extract_semantics.py -->
#### `harness/evolve-daemon/extract_semantics.py`

**一句话**: 语义提取器封装 — 为 daemon.py 提供 analyze_session() API。
**类型**: python
**路径**: `harness/evolve-daemon/extract_semantics.py`

**核心能力**:
  - `extract_with_haiku()`: 调用 Claude Haiku 提取纠正上下文（统一 LLM 配置）。

底层使用 kb_share...
  - `analyze_session()`: 分析单个会话，提取语义并回填。

Args:
    session: 会话 dict（必须包含 s...
  - `analyze_sessions()`: 批量分析多个会话。

Returns: 每个会话的分析结果列表...
  - `_record_to_instinct()`: 将新发现的纠正模式记录到 instinct-record.json，返回 record_ids...
  - `main()`: CLI 测试入口...

<!-- CAPABILITY:harness/evolve-daemon/generalize.py -->
#### `harness/evolve-daemon/generalize.py`

**一句话**: generalize.
**类型**: python
**路径**: `harness/evolve-daemon/generalize.py`

**核心能力**:
  - `_has_llm_access()`: 检查是否有 LLM 调用能力（代理或真实 API Key）...
  - `call_haiku()`: 用 Haiku 做简单判断（reuse/new）...
  - `call_sonnet()`: 用 Sonnet 做深度分析（新根因、merge 风险）...
  - `call_llm_fallback()`: 无 API Key 时的本地规则降级。
用硬编码的启发式规则判断 reuse / new。...
  - `build_step1_prompt()`: 构建第一步 prompt：批量关联分析...

<!-- CAPABILITY:harness/evolve-daemon/instinct_updater.py -->
#### `harness/evolve-daemon/instinct_updater.py`

**一句话**: Instinct 自动更新器 — 管理本能记录的完整生命周期。
**类型**: python
**路径**: `harness/evolve-daemon/instinct_updater.py`

**核心能力**:
  - `_parse_iso_safe()`: 安全解析 ISO 时间字符串，失败时返回默认值...
  - `load_instinct()`: 加载或初始化 instinct-record.json...
  - `save_instinct()`: 保存 instinct-record.json...
  - `time_decay_weight()`: 计算时间衰减权重。

公式: weight = 0.5 ^ (age_days / half_lif...
  - `apply_decay_to_all()`: 对所有非 seed 记录应用时间衰减。

规则:
- seed 记录不衰减
- reinforcem...

<!-- CAPABILITY:harness/evolve-daemon/integrated_evolution.py -->
#### `harness/evolve-daemon/integrated_evolution.py`

**一句话**: integrated_evolution.
**类型**: python
**路径**: `harness/evolve-daemon/integrated_evolution.py`

**核心能力**:
  - `collect_session_errors()`: 收集本会话的错误。
只收集最近 max_age_hours 小时内的新错误。...
  - `_extract_context()`: 从错误条目中提取上下文...
  - `run_session_evolution()`: 会话级进化主流程。

每次会话结束时调用。...
  - `_load_config()`: 加载配置...
  - `run_full_analysis()`: 不限制会话，强制分析所有未知错误...

<!-- CAPABILITY:harness/evolve-daemon/llm_decision.py -->
#### `harness/evolve-daemon/llm_decision.py`

**一句话**: LLM 决策引擎 — 用 LLM 分析会话数据，决定下一步行动。
**类型**: python
**路径**: `harness/evolve-daemon/llm_decision.py`

**核心能力**:
  - `load_config()`: 加载配置（使用统一配置模块）...
  - `_default_config()`
  - `get_existing_targets()`: 获取 instinct 中已有的 target 列表...
  - `is_new_target()`: 判断是否是新 target（未在 instinct 中出现）...
  - `assess_risk()`: 评估风险等级（0.0 - 1.0）。

规则:
- 高风险模式（permission, securi...

<!-- CAPABILITY:harness/evolve-daemon/memory_sync.py -->
#### `harness/evolve-daemon/memory_sync.py`

**一句话**: 知识同步模块 - 将进化系统产生的知识同步到 MEMORY.
**类型**: python
**路径**: `harness/evolve-daemon/memory_sync.py`

**核心能力**:
  - `load_knowledge_base()`: 加载知识库...
  - `generate_memory_summary()`: 生成记忆摘要

Args:
    entry: 知识库条目

Returns:
    格式化的摘...
  - `get_existing_sync_entries()`: 获取已同步的条目 ID...
  - `sync_to_memory()`: 同步知识到 MEMORY.md

Args:
    max_entries: 最大同步条目数

R...
  - `main()`: 主入口...

<!-- CAPABILITY:harness/evolve-daemon/proposer.py -->
#### `harness/evolve-daemon/proposer.py`

**一句话**: 提案生成器 — 调用 Claude API 进行深度分析，生成结构化改进提案。
**类型**: python
**路径**: `harness/evolve-daemon/proposer.py`

**核心能力**:
  - `generate_proposal()`: 生成改进提案。调用 Claude API 进行深度分析。
底层使用 kb_shared.get_ll...
  - `_call_claude_api()`: 调用 Claude API — 优先使用统一 SDK 客户端，降级为 REST API...
  - `_generate_with_claude()`: 使用 Claude API 生成高质量提案...
  - `_generate_from_template()`: 降级：使用模板生成提案（无需 API Key）...
  - `_save_proposal()`: 保存提案文件...

<!-- CAPABILITY:harness/evolve-daemon/rollback.py -->
#### `harness/evolve-daemon/rollback.py`

**一句话**: 自动回滚模块 — 观察期验证效果，自动回滚恶化的改动。
**类型**: python
**路径**: `harness/evolve-daemon/rollback.py`

**核心能力**:
  - `load_proposal_history()`: 加载提案历史...
  - `save_proposal_history()`: 保存提案历史...
  - `collect_metrics()`
  - `evaluate_proposal()`: 评估是否应该保留或回滚。

返回: (decision, triggers) — decision ...
  - `check_circuit_breaker()`: 检查熔断器状态。

返回: (is_triggered, reason)...

<!-- CAPABILITY:harness/evolve-daemon/rule_evolution.py -->
#### `harness/evolve-daemon/rule_evolution.py`

**一句话**: Rule 维度进化策略
**类型**: python
**路径**: `harness/evolve-daemon/rule_evolution.py`

**核心能力**:
  - `evolve_rule()`
  - `_generate_rule_change()`

<!-- CAPABILITY:harness/evolve-daemon/scheduler.py -->
#### `harness/evolve-daemon/scheduler.py`

**一句话**: 内置定时任务调度器 — 基于 APScheduler 实现异步定时触发。
**类型**: python
**路径**: `harness/evolve-daemon/scheduler.py`

**核心能力**:
  - `SchedulerManager`: 调度器管理器...
  - `parse_interval()`: 解析间隔字符串，返回秒数。

支持格式：
  - "30 seconds" / "30 s"
  -...
  - `run_evolution_cycle()`: 执行一次完整的进化周期...
  - `get_last_evolution_time()`: 获取上次进化的时间...
  - `check_heartbeat()`: 心跳检测：检查是否需要触发进化

返回：
    {
        "healthy": True...
  - `main()`

<!-- CAPABILITY:harness/evolve-daemon/skill_evolution.py -->
#### `harness/evolve-daemon/skill_evolution.py`

**一句话**: Skill 维度进化策略
**类型**: python
**路径**: `harness/evolve-daemon/skill_evolution.py`

**核心能力**:
  - `evolve_skill()`
  - `_generate_skill_change()`

<!-- CAPABILITY:harness/evolve-daemon/update_notifier.py -->
#### `harness/evolve-daemon/update_notifier.py`

**一句话**: CHK 插件更新通知器 - 管理更新通知状态，避免重复提示
**类型**: python
**路径**: `harness/evolve-daemon/update_notifier.py`

**核心能力**:
  - `UpdateState`: 更新通知状态...
  - `UpdateNotifier`: 更新通知器...
  - `get_notifier()`: 获取全局通知器实例...
  - `format_update_notification()`: 格式化更新通知消息

格式参考 Claude Code 升级提示风格：

╔════════════...
  - `run_update_check()`: 执行完整的更新检查流程

Returns:
    更新通知消息（如果有更新且应该通知），否则返回空...
  - `main()`: 主入口...

<!-- CAPABILITY:harness/evolve-daemon/validator.py -->
#### `harness/evolve-daemon/validator.py`

**一句话**: 数据验证器 — 验证 sessions.jsonl 格式，隔离异常数据。
**类型**: python
**路径**: `harness/evolve-daemon/validator.py`

**核心能力**:
  - `validate_session()`: 验证单个 session 的格式。

返回: (is_valid, error_message)...
  - `validate_sessions_file()`: 验证 sessions.jsonl 文件。

返回:
{
    "total": 100,
   ...
  - `clean_old_sessions()`: 清理超过指定天数的 session。

返回清理统计。...
  - `get_data_quality_stats()`: 统计数据质量。

返回:
{
    "total_sessions": 100,
    "ses...
  - `run_validation()`: 运行完整验证流程。...

### 场景: HOOK

<!-- CAPABILITY:harness/_core/path_guard.py -->
#### `harness/_core/path_guard.py`

**一句话**: path_guard.
**类型**: python
**路径**: `harness/_core/path_guard.py`

**核心能力**:
  - `PathGuard`: 路径守卫...
  - `validate_path_scope()`: 验证路径是否在白名单内（顶层函数，供 paths.py 调用）

Args:
    path: 待...
  - `check_access()`: 检查路径访问权限

Args:
    path: 待检查路径
    allowed_dirs: ...
  - `get_guard()`: 获取全局路径守卫...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/mode.py -->
#### `harness/cli/mode.py`

**一句话**: chk mode — 切换 Claude Code 执行模式。
**类型**: python
**路径**: `harness/cli/mode.py`

**核心能力**:
  - `load_mode_template()`: 加载指定模式的 hook 配置模板...
  - `load_settings()`: 加载或初始化 settings.local.json...
  - `save_settings()`: 保存 settings.local.json...
  - `switch_mode()`: 切换到指定模式...
  - `show_current_mode()`: 显示当前模式...

<!-- CAPABILITY:harness/cli/status.py -->
#### `harness/cli/status.py`

**一句话**: kit status — 查看 Claude Harness Kit 当前状态。
**类型**: python
**路径**: `harness/cli/status.py`

**核心能力**:
  - `load_settings()`
  - `count_files()`
  - `main()`

<!-- CAPABILITY:harness/evolve-daemon/extract_semantics.py -->
#### `harness/evolve-daemon/extract_semantics.py`

**一句话**: 语义提取器封装 — 为 daemon.py 提供 analyze_session() API。
**类型**: python
**路径**: `harness/evolve-daemon/extract_semantics.py`

**核心能力**:
  - `extract_with_haiku()`: 调用 Claude Haiku 提取纠正上下文（统一 LLM 配置）。

底层使用 kb_share...
  - `analyze_session()`: 分析单个会话，提取语义并回填。

Args:
    session: 会话 dict（必须包含 s...
  - `analyze_sessions()`: 批量分析多个会话。

Returns: 每个会话的分析结果列表...
  - `_record_to_instinct()`: 将新发现的纠正模式记录到 instinct-record.json，返回 record_ids...
  - `main()`: CLI 测试入口...

<!-- CAPABILITY:harness/evolve-daemon/integrated_evolution.py -->
#### `harness/evolve-daemon/integrated_evolution.py`

**一句话**: integrated_evolution.
**类型**: python
**路径**: `harness/evolve-daemon/integrated_evolution.py`

**核心能力**:
  - `collect_session_errors()`: 收集本会话的错误。
只收集最近 max_age_hours 小时内的新错误。...
  - `_extract_context()`: 从错误条目中提取上下文...
  - `run_session_evolution()`: 会话级进化主流程。

每次会话结束时调用。...
  - `_load_config()`: 加载配置...
  - `run_full_analysis()`: 不限制会话，强制分析所有未知错误...

<!-- CAPABILITY:harness/evolve-daemon/scheduler.py -->
#### `harness/evolve-daemon/scheduler.py`

**一句话**: 内置定时任务调度器 — 基于 APScheduler 实现异步定时触发。
**类型**: python
**路径**: `harness/evolve-daemon/scheduler.py`

**核心能力**:
  - `SchedulerManager`: 调度器管理器...
  - `parse_interval()`: 解析间隔字符串，返回秒数。

支持格式：
  - "30 seconds" / "30 s"
  -...
  - `run_evolution_cycle()`: 执行一次完整的进化周期...
  - `get_last_evolution_time()`: 获取上次进化的时间...
  - `check_heartbeat()`: 心跳检测：检查是否需要触发进化

返回：
    {
        "healthy": True...
  - `main()`

<!-- CAPABILITY:hooks/bin/agent-planning-check.sh -->
#### `hooks/bin/agent-planning-check.sh`

**一句话**: !/bin/bash Agent Planning Check - PreAgentCall Hook 验证多 Agent 任务分配合理性 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-planning-check.sh`

**核心能力**:
  - `log()`
  - `main()`

<!-- CAPABILITY:hooks/bin/agent-result-sync.sh -->
#### `hooks/bin/agent-result-sync.sh`

**一句话**: !/bin/bash Agent Result Sync - PostAgentCall Hook 同步 Agent 执行结果到 mailbox 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-result-sync.sh`

**核心能力**:
  - `log()`
  - `main()`

<!-- CAPABILITY:hooks/bin/architecture-verify.sh -->
#### `hooks/bin/architecture-verify.sh`

**一句话**: !/bin/bash architecture-verify.sh - 架构决策步骤验证 检查是否涉及架构相关关键词 检查是否有决策记录目录 如果涉及架构但没有决策文件，提示警告
**类型**: shell
**路径**: `hooks/bin/architecture-verify.sh`

<!-- CAPABILITY:hooks/bin/check-update.sh -->
#### `hooks/bin/check-update.sh`

**一句话**: !/bin/bash ============================================================ CHK 插件更新检查钩子 - UserPromptSub
**类型**: shell
**路径**: `hooks/bin/check-update.sh`

**核心能力**:
  - `log_info()`
  - `should_check()`
  - `get_local_version()`
  - `get_remote_version()`
  - `version_lt()`

<!-- CAPABILITY:hooks/bin/checkpoint-auto-save.sh -->
#### `hooks/bin/checkpoint-auto-save.sh`

**一句话**: !/bin/bash checkpoint-auto-save.sh — PreToolUse Hook: 检测 /compact 并自动保存 checkpoint 设计：永远 exit 0，chec
**类型**: shell
**路径**: `hooks/bin/checkpoint-auto-save.sh`

<!-- CAPABILITY:hooks/bin/checkpoint-verify.sh -->
#### `hooks/bin/checkpoint-verify.sh`

**一句话**: !/bin/bash checkpoint-verify.sh - 验证 Checkpoint 文件是否完整 检查备份目录是否存在 关键文件列表
**类型**: shell
**路径**: `hooks/bin/checkpoint-verify.sh`

<!-- CAPABILITY:hooks/bin/coverage-check.sh -->
#### `hooks/bin/coverage-check.sh`

**一句话**: !/bin/bash coverage-check.sh — 测试覆盖率门禁 当测试覆盖率低于阈值时阻断提交 支持多种覆盖率报告格式 pytest-cov XML
**类型**: shell
**路径**: `hooks/bin/coverage-check.sh`

**核心能力**:
  - `find_coverage_report()`
  - `check_coverage()`

<!-- CAPABILITY:hooks/bin/doc-verify.sh -->
#### `hooks/bin/doc-verify.sh`

**一句话**: !/usr/bin/env bash doc-verify.sh - 文档验证器 Shell 包装器 用于 Claude Code hook，自动检测插件根目录 自动检测插件根目录 优先级 1: 环境
**类型**: shell
**路径**: `hooks/bin/doc-verify.sh`

**核心能力**:
  - `detect_plugin_root()`

<!-- CAPABILITY:hooks/bin/ensure-settings.sh -->
#### `hooks/bin/ensure-settings.sh`

**一句话**: !/bin/bash ============================================================ CHK 项目配置保障钩子 - UserPromptSub
**类型**: shell
**路径**: `hooks/bin/ensure-settings.sh`

<!-- CAPABILITY:hooks/bin/git-commit-check.sh -->
#### `hooks/bin/git-commit-check.sh`

**一句话**: !/bin/bash git-commit-check.sh - 检查 Git 提交规范 从 general.md 提取有效类型 检查 git commit 命令 提取提交信息
**类型**: shell
**路径**: `hooks/bin/git-commit-check.sh`

<!-- CAPABILITY:hooks/bin/log-utils.sh -->
#### `hooks/bin/log-utils.sh`

**一句话**: !/bin/bash ============================================================ CHK 共享日志工具 — 被其他 hook 脚本 sou
**类型**: shell
**路径**: `hooks/bin/log-utils.sh`

**核心能力**:
  - `_hook_log_init()`
  - `_hook_log_error()`
  - `_hook_log_warn()`
  - `_hook_log_info()`

<!-- CAPABILITY:hooks/bin/memory-cleanup.sh -->
#### `hooks/bin/memory-cleanup.sh`

**一句话**: !/bin/bash ============================================================ CHK 会话状态清理脚本  功能： - 清理当前会话的状
**类型**: shell
**路径**: `hooks/bin/memory-cleanup.sh`

**核心能力**:
  - `cleanup_current()`
  - `cleanup_all()`

<!-- CAPABILITY:hooks/bin/memory-inject.sh -->
#### `hooks/bin/memory-inject.sh`

**一句话**: !/bin/bash ============================================================ CHK 记忆注入钩子 - UserPromptSubmi
**类型**: shell
**路径**: `hooks/bin/memory-inject.sh`

**核心能力**:
  - `log()`
  - `is_L0_injected()`
  - `mark_L0_injected()`
  - `read_memory_index()`
  - `read_high_confidence_instincts()`

<!-- CAPABILITY:hooks/bin/notify.sh -->
#### `hooks/bin/notify.sh`

**一句话**: !/bin/bash notify.sh - 飞书 Webhook 通知脚本 用法: ./notify.sh <type> <message> [title] 示例: ./notify.sh succ
**类型**: shell
**路径**: `hooks/bin/notify.sh`

**核心能力**:
  - `log_info()`
  - `log_error()`
  - `log_warn()`
  - `send_feishu_message()`
  - `main()`

<!-- CAPABILITY:hooks/bin/observe.sh -->
#### `hooks/bin/observe.sh`

**一句话**: !/bin/bash observe.sh — Hook 观测事件采集器（shell wrapper） 职责：调用 observe.py，永远 exit 0，零阻塞主流程  设计原则： 1. 永远 e
**类型**: shell
**路径**: `hooks/bin/observe.sh`

<!-- CAPABILITY:hooks/bin/quality-gate.sh -->
#### `hooks/bin/quality-gate.sh`

**一句话**: !/bin/bash quality-gate.sh — PostToolUse Hook: 验证代码和配置文件格式 设计：永远 exit 0，格式错误警告但不阻断 加载共享日志工具
**类型**: shell
**路径**: `hooks/bin/quality-gate.sh`

**核心能力**:
  - `block_post()`
  - `_is_impl_file()`
  - `_scan_secrets()`
  - `_check_test_missing()`

<!-- CAPABILITY:hooks/bin/rate-limiter.sh -->
#### `hooks/bin/rate-limiter.sh`

**一句话**: !/bin/bash rate-limiter.sh — Claude Code API Rate Limiter (Sliding Window) 设计：永远 exit 0，rate limit 超
**类型**: shell
**路径**: `hooks/bin/rate-limiter.sh`

**核心能力**:
  - `log_warn()`
  - `is_valid_json()`
  - `load_state()`
  - `save_state()`
  - `clean_old()`

<!-- CAPABILITY:hooks/bin/safety-check.sh -->
#### `hooks/bin/safety-check.sh`

**一句话**: !/bin/bash safety-check.sh — PreToolUse Hook: 阻止危险 Bash 命令 设计：永远 exit 0（Hook 失败不阻断工具调用），危险命令通过 hookS
**类型**: shell
**路径**: `hooks/bin/safety-check.sh`

**核心能力**:
  - `block()`

<!-- CAPABILITY:hooks/bin/security-auto-trigger.sh -->
#### `hooks/bin/security-auto-trigger.sh`

**一句话**: !/bin/bash security-auto-trigger.sh — PostToolUse Hook: 敏感文件修改时自动触发安全审查提示 设计：永远 exit 0，提示不阻断
**类型**: shell
**路径**: `hooks/bin/security-auto-trigger.sh`

<!-- CAPABILITY:hooks/bin/tdd-check.sh -->
#### `hooks/bin/tdd-check.sh`

**一句话**: !/bin/bash tdd-check.sh — PreToolUse Hook: TDD 阻断检查，实现文件写入前必须存在对应测试文件 设计：永远 exit 0（Hook 失败不阻断），TDD 违
**类型**: shell
**路径**: `hooks/bin/tdd-check.sh`

**核心能力**:
  - `_is_impl()`
  - `block()`

<!-- CAPABILITY:hooks/bin/update-registry-on-commit.sh -->
#### `hooks/bin/update-registry-on-commit.sh`

**一句话**: !/bin/bash ============================================================ Git Hook: 增量更新 Capability Re
**类型**: shell
**路径**: `hooks/bin/update-registry-on-commit.sh`

**核心能力**:
  - `check_code_changes()`
  - `get_changed_files()`
  - `needs_full_update()`
  - `update_registry()`
  - `show_help()`

<!-- CAPABILITY:hooks/bin/update-registry.sh -->
#### `hooks/bin/update-registry.sh`

**一句话**: !/bin/bash ============================================================ 更新 Capability Registry  用法： 
**类型**: shell
**路径**: `hooks/bin/update-registry.sh`

### 场景: MEMORY

<!-- CAPABILITY:harness/_core/cache_manager.py -->
#### `harness/_core/cache_manager.py`

**一句话**: cache_manager.
**类型**: python
**路径**: `harness/_core/cache_manager.py`

**核心能力**:
  - `CacheStats`: 缓存命中统计...
  - `CacheEntry`: 缓存条目...
  - `CacheManager`: Prompt 缓存管理器...
  - `get_cache_manager()`: 获取全局缓存管理器...
  - `preload_knowledge()`: 预加载知识（供 Hook 调用）

返回格式化的预加载内容。...
  - `main()`: CLI 测试...

<!-- CAPABILITY:harness/_core/instinct_engine.py -->
#### `harness/_core/instinct_engine.py`

**一句话**: instinct_engine.
**类型**: python
**路径**: `harness/_core/instinct_engine.py`

**核心能力**:
  - `InstinctEngine`: 本能推理引擎...
  - `get_engine()`: 获取全局本能引擎...
  - `get_recommendations()`: 获取推荐（顶层函数）...
  - `update_confidence()`: 更新置信度（顶层函数）...
  - `main()`: 测试...

<!-- CAPABILITY:harness/_core/instinct_reader.py -->
#### `harness/_core/instinct_reader.py`

**一句话**: 本能读取模块 - 从 instinct-record.
**类型**: python
**路径**: `harness/_core/instinct_reader.py`

**核心能力**:
  - `Instinct`: 本能数据结构...
  - `_load_instincts()`: 加载本能记录...
  - `get_high_confidence_instincts()`: 获取高置信度本能列表

Args:
    min_confidence: 最小置信度阈值，默认 0...
  - `format_instinct_for_injection()`: 格式化本能为注入文本

Args:
    instinct: 本能对象

Returns:
   ...
  - `format_all_instincts_for_injection()`: 格式化所有本能为注入文本

Args:
    instincts: 本能列表

Returns:
...
  - `get_instinct_stats()`: 获取本能统计信息...

<!-- CAPABILITY:harness/_core/instinct_state.py -->
#### `harness/_core/instinct_state.py`

**一句话**: 本能状态管理模块 - 跟踪当前会话已注入的本能
**类型**: python
**路径**: `harness/_core/instinct_state.py`

**核心能力**:
  - `SessionState`: 会话状态管理...
  - `get_session_state()`: 获取会话状态单例...
  - `cleanup_all_sessions()`: 清理所有会话状态...

<!-- CAPABILITY:harness/_core/keyword_matcher.py -->
#### `harness/_core/keyword_matcher.py`

**一句话**: 关键词匹配模块 - 根据用户输入匹配相关记忆
**类型**: python
**路径**: `harness/_core/keyword_matcher.py`

**核心能力**:
  - `match_keywords()`: 匹配用户输入中的关键词

Args:
    user_input: 用户输入文本

Returns...
  - `get_matching_files()`: 获取匹配的记忆文件列表

Args:
    categories: 匹配的类别列表

Return...
  - `format_matched_keywords()`: 格式化匹配结果为可读文本

Args:
    categories: 匹配的类别列表

Retur...
  - `check_and_match()`: 检查并匹配关键词，返回类别和文件

Args:
    user_input: 用户输入文本

Re...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/instinct_cli.py -->
#### `harness/cli/instinct_cli.py`

**一句话**: instinct_cli.
**类型**: python
**路径**: `harness/cli/instinct_cli.py`

**核心能力**:
  - `_get_chk_version()`
  - `load_records()`
  - `save_records()`
  - `confidence_label()`
  - `confidence_bar()`

<!-- CAPABILITY:harness/cli/status.py -->
#### `harness/cli/status.py`

**一句话**: kit status — 查看 Claude Harness Kit 当前状态。
**类型**: python
**路径**: `harness/cli/status.py`

**核心能力**:
  - `load_settings()`
  - `count_files()`
  - `main()`

<!-- CAPABILITY:harness/evolve-daemon/apply_change.py -->
#### `harness/evolve-daemon/apply_change.py`

**一句话**: 自动应用模块 — 根据 LLM 决策自动应用改动。
**类型**: python
**路径**: `harness/evolve-daemon/apply_change.py`

**核心能力**:
  - `backup_file()`: 备份原文件到 backups_dir...
  - `restore_file()`: 从备份恢复文件...
  - `apply_text_change()`: 应用文本改动。

change 可以是：
1. 精确替换: "old_text -> new_tex...
  - `apply_change()`: 根据 decision 自动应用改动。

返回: True 成功，False 失败...
  - `_sync_to_memory()`: 同步知识到记忆系统...

<!-- CAPABILITY:harness/evolve-daemon/daemon.py -->
#### `harness/evolve-daemon/daemon.py`

**一句话**: 进化守护进程入口 — 支持外部触发和内置定时任务。
**类型**: python
**路径**: `harness/evolve-daemon/daemon.py`

**核心能力**:
  - `handle_exception()`: 统一异常处理包装函数（本地定义避免循环依赖）...
  - `_stop_scheduler()`: 停止调度器（共享逻辑）...
  - `_save_state()`: 保存状态（共享逻辑）...
  - `graceful_shutdown()`: 优雅退出处理函数...
  - `graceful_restart()`: 优雅重启处理函数（SIGUSR1）...

<!-- CAPABILITY:harness/evolve-daemon/effect_tracker.py -->
#### `harness/evolve-daemon/effect_tracker.py`

**一句话**: 效果跟踪器 - 跟踪进化改进的有效性
**类型**: python
**路径**: `harness/evolve-daemon/effect_tracker.py`

**核心能力**:
  - `EffectTracker`: 效果跟踪器...
  - `main()`: 测试效果跟踪器...

<!-- CAPABILITY:harness/evolve-daemon/evolve_dispatcher.py -->
#### `harness/evolve-daemon/evolve_dispatcher.py`

**一句话**: 进化分发器 — 8维度分析决策引擎
**类型**: python
**路径**: `harness/evolve-daemon/evolve_dispatcher.py`

**核心能力**:
  - `get_dimension()`: 根据 target 前缀确定维度。

核心维度:
  agent:xxx → agent
  ski...
  - `_load_dimension_thresholds()`: 从 config.yaml 统一加载 8 个维度的进化阈值。

阈值定义在 config.yaml ...
  - `meets_threshold()`: 判断纠正次数是否达到维度阈值。

阈值从 config.yaml 的 thresholds.dime...
  - `build_decision()`: 为指定维度构建进化决策。

返回:
{
    "dimension": str,
    "tar...
  - `_agent_decision()`: Agent 维度进化策略...

<!-- CAPABILITY:harness/evolve-daemon/extract_semantics.py -->
#### `harness/evolve-daemon/extract_semantics.py`

**一句话**: 语义提取器封装 — 为 daemon.py 提供 analyze_session() API。
**类型**: python
**路径**: `harness/evolve-daemon/extract_semantics.py`

**核心能力**:
  - `extract_with_haiku()`: 调用 Claude Haiku 提取纠正上下文（统一 LLM 配置）。

底层使用 kb_share...
  - `analyze_session()`: 分析单个会话，提取语义并回填。

Args:
    session: 会话 dict（必须包含 s...
  - `analyze_sessions()`: 批量分析多个会话。

Returns: 每个会话的分析结果列表...
  - `_record_to_instinct()`: 将新发现的纠正模式记录到 instinct-record.json，返回 record_ids...
  - `main()`: CLI 测试入口...

<!-- CAPABILITY:harness/evolve-daemon/instinct_updater.py -->
#### `harness/evolve-daemon/instinct_updater.py`

**一句话**: Instinct 自动更新器 — 管理本能记录的完整生命周期。
**类型**: python
**路径**: `harness/evolve-daemon/instinct_updater.py`

**核心能力**:
  - `_parse_iso_safe()`: 安全解析 ISO 时间字符串，失败时返回默认值...
  - `load_instinct()`: 加载或初始化 instinct-record.json...
  - `save_instinct()`: 保存 instinct-record.json...
  - `time_decay_weight()`: 计算时间衰减权重。

公式: weight = 0.5 ^ (age_days / half_lif...
  - `apply_decay_to_all()`: 对所有非 seed 记录应用时间衰减。

规则:
- seed 记录不衰减
- reinforcem...

<!-- CAPABILITY:harness/evolve-daemon/kb_shared.py -->
#### `harness/evolve-daemon/kb_shared.py`

**一句话**: kb_shared.
**类型**: python
**路径**: `harness/evolve-daemon/kb_shared.py`

**核心能力**:
  - `_ensure_env_loaded()`: 从 Claude Code 配置自动加载环境变量（幂等，所有 LLM 模块共享）

自动读取 ~/....
  - `get_model()`: 获取统一模型（ANTHROPIC_MODEL），无则返回 None...
  - `get_haiku_model()`: 快速分类模型：有 ANTHROPIC_MODEL 用它，否则用默认 Haiku...
  - `get_sonnet_model()`: 深度分析模型：有 ANTHROPIC_MODEL 用它，否则用默认 Sonnet...
  - `get_llm_config()`: 统一 LLM 配置参数，所有模块引用此处...

<!-- CAPABILITY:harness/evolve-daemon/llm_decision.py -->
#### `harness/evolve-daemon/llm_decision.py`

**一句话**: LLM 决策引擎 — 用 LLM 分析会话数据，决定下一步行动。
**类型**: python
**路径**: `harness/evolve-daemon/llm_decision.py`

**核心能力**:
  - `load_config()`: 加载配置（使用统一配置模块）...
  - `_default_config()`
  - `get_existing_targets()`: 获取 instinct 中已有的 target 列表...
  - `is_new_target()`: 判断是否是新 target（未在 instinct 中出现）...
  - `assess_risk()`: 评估风险等级（0.0 - 1.0）。

规则:
- 高风险模式（permission, securi...

<!-- CAPABILITY:harness/evolve-daemon/memory_sync.py -->
#### `harness/evolve-daemon/memory_sync.py`

**一句话**: 知识同步模块 - 将进化系统产生的知识同步到 MEMORY.
**类型**: python
**路径**: `harness/evolve-daemon/memory_sync.py`

**核心能力**:
  - `load_knowledge_base()`: 加载知识库...
  - `generate_memory_summary()`: 生成记忆摘要

Args:
    entry: 知识库条目

Returns:
    格式化的摘...
  - `get_existing_sync_entries()`: 获取已同步的条目 ID...
  - `sync_to_memory()`: 同步知识到 MEMORY.md

Args:
    max_entries: 最大同步条目数

R...
  - `main()`: 主入口...

<!-- CAPABILITY:harness/evolve-daemon/proposer.py -->
#### `harness/evolve-daemon/proposer.py`

**一句话**: 提案生成器 — 调用 Claude API 进行深度分析，生成结构化改进提案。
**类型**: python
**路径**: `harness/evolve-daemon/proposer.py`

**核心能力**:
  - `generate_proposal()`: 生成改进提案。调用 Claude API 进行深度分析。
底层使用 kb_shared.get_ll...
  - `_call_claude_api()`: 调用 Claude API — 优先使用统一 SDK 客户端，降级为 REST API...
  - `_generate_with_claude()`: 使用 Claude API 生成高质量提案...
  - `_generate_from_template()`: 降级：使用模板生成提案（无需 API Key）...
  - `_save_proposal()`: 保存提案文件...

<!-- CAPABILITY:harness/evolve-daemon/rollback.py -->
#### `harness/evolve-daemon/rollback.py`

**一句话**: 自动回滚模块 — 观察期验证效果，自动回滚恶化的改动。
**类型**: python
**路径**: `harness/evolve-daemon/rollback.py`

**核心能力**:
  - `load_proposal_history()`: 加载提案历史...
  - `save_proposal_history()`: 保存提案历史...
  - `collect_metrics()`
  - `evaluate_proposal()`: 评估是否应该保留或回滚。

返回: (decision, triggers) — decision ...
  - `check_circuit_breaker()`: 检查熔断器状态。

返回: (is_triggered, reason)...

<!-- CAPABILITY:harness/knowledge/knowledge_recommender.py -->
#### `harness/knowledge/knowledge_recommender.py`

**一句话**: Knowledge Recommender Engine — 知识推荐引擎
**类型**: python
**路径**: `harness/knowledge/knowledge_recommender.py`

**核心能力**:
  - `load_evolved_knowledge()`: 加载进化知识库 (JSONL 格式)...
  - `load_knowledge_base()`: 加载所有知识条目（双知识库合并）

知识库 1: harness/knowledge/ — 手工维护...
  - `load_instinct_usage()`: 从 instinct 数据读取历史使用频率...
  - `extract_keywords()`: 从文本中提取关键词（过滤停用词）...
  - `compute_score()`: 计算单条知识的推荐分数...

<!-- CAPABILITY:harness/paths.py -->
#### `harness/paths.py`

**一句话**: paths.
**类型**: python
**路径**: `harness/paths.py`

**核心能力**:
  - `_project_root()`
  - `_plugin_root()`
  - `sessions_file()`
  - `errors_file()`
  - `errors_lock_file()`

<!-- CAPABILITY:harness/tests/check_directory_and_safety.py -->
#### `harness/tests/check_directory_and_safety.py`

**一句话**: 目录结构与安全全面测试套件
**类型**: python
**路径**: `harness/tests/check_directory_and_safety.py`

**核心能力**:
  - `ok()`
  - `fail()`
  - `test_harness_whitelist_subdirs()`: 正向: harness/ 下只允许白名单子目录...
  - `test_no_harness_nested()`: 安全: harness/ 下禁止嵌套另一个 harness/...
  - `test_no_code_in_claude_dir()`: 安全: .claude/ 下只允许 data/ 和 proposals/...

<!-- CAPABILITY:hooks/bin/memory-cleanup.sh -->
#### `hooks/bin/memory-cleanup.sh`

**一句话**: !/bin/bash ============================================================ CHK 会话状态清理脚本  功能： - 清理当前会话的状
**类型**: shell
**路径**: `hooks/bin/memory-cleanup.sh`

**核心能力**:
  - `cleanup_current()`
  - `cleanup_all()`

<!-- CAPABILITY:hooks/bin/memory-inject.sh -->
#### `hooks/bin/memory-inject.sh`

**一句话**: !/bin/bash ============================================================ CHK 记忆注入钩子 - UserPromptSubmi
**类型**: shell
**路径**: `hooks/bin/memory-inject.sh`

**核心能力**:
  - `log()`
  - `is_L0_injected()`
  - `mark_L0_injected()`
  - `read_memory_index()`
  - `read_high_confidence_instincts()`

### 场景: PATH

<!-- CAPABILITY:harness/_core/path_guard.py -->
#### `harness/_core/path_guard.py`

**一句话**: path_guard.
**类型**: python
**路径**: `harness/_core/path_guard.py`

**核心能力**:
  - `PathGuard`: 路径守卫...
  - `validate_path_scope()`: 验证路径是否在白名单内（顶层函数，供 paths.py 调用）

Args:
    path: 待...
  - `check_access()`: 检查路径访问权限

Args:
    path: 待检查路径
    allowed_dirs: ...
  - `get_guard()`: 获取全局路径守卫...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/gc.py -->
#### `harness/cli/gc.py`

**一句话**: 知识垃圾回收 CLI — kit gc 命令。
**类型**: python
**路径**: `harness/cli/gc.py`

**核心能力**:
  - `run_gc_agent()`: 通过 Claude Code CLI 调用 GC Agent...
  - `generate_fallback_report()`: 无 Claude Code 时生成基础扫描报告...
  - `main()`

<!-- CAPABILITY:harness/cli/init.py -->
#### `harness/cli/init.py`

**一句话**: kit init — 自动分析项目，生成高质量 CLAUDE.md 和 .claude/ 配置。
**类型**: python
**路径**: `harness/cli/init.py`

**核心能力**:
  - `parse_package_json()`: 从 package.json 提取依赖和版本...
  - `parse_pom_xml()`: 从 pom.xml 提取关键依赖...
  - `parse_go_mod()`: 从 go.mod 提取依赖...
  - `discover_structure()`: 发现关键目录、入口文件、模块边界...
  - `extract_git_insights()`: 从 git log 提取最近的 fix/refactor 关键词热点...

<!-- CAPABILITY:harness/cli/scan.py -->
#### `harness/cli/scan.py`

**一句话**: kit scan — 扫描多代码库目录，评估改造量。
**类型**: python
**路径**: `harness/cli/scan.py`

**核心能力**:
  - `scan_directory()`: 扫描目录下所有项目...
  - `main()`

<!-- CAPABILITY:harness/knowledge/lifecycle.py -->
#### `harness/knowledge/lifecycle.py`

**一句话**: Knowledge Lifecycle Engine — 知识生命周期可执行引擎。
**类型**: python
**路径**: `harness/knowledge/lifecycle.py`

**核心能力**:
  - `load_lifecycle_config()`: 加载 lifecycle.yaml 配置，失败则使用内联默认值...
  - `check_maturity_promotion()`: 检查条目是否可以升级。
返回: "verified" | "proven" | None...
  - `apply_decay()`: 检查条目是否应该衰减降级。
返回: 目标成熟度 | None（无需降级）...
  - `promote_to_layer1()`: 跨项目提升：L3 → L1/L2。
生成提升提案到 proposals/ 目录。
返回: 提案文件路...
  - `cmd_check()`: 检查单条知识的成熟度和衰减状态...

<!-- CAPABILITY:hooks/bin/agent-planning-check.sh -->
#### `hooks/bin/agent-planning-check.sh`

**一句话**: !/bin/bash Agent Planning Check - PreAgentCall Hook 验证多 Agent 任务分配合理性 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-planning-check.sh`

**核心能力**:
  - `log()`
  - `main()`

<!-- CAPABILITY:hooks/bin/agent-result-sync.sh -->
#### `hooks/bin/agent-result-sync.sh`

**一句话**: !/bin/bash Agent Result Sync - PostAgentCall Hook 同步 Agent 执行结果到 mailbox 获取插件根目录 主逻辑
**类型**: shell
**路径**: `hooks/bin/agent-result-sync.sh`

**核心能力**:
  - `log()`
  - `main()`

<!-- CAPABILITY:hooks/bin/architecture-verify.sh -->
#### `hooks/bin/architecture-verify.sh`

**一句话**: !/bin/bash architecture-verify.sh - 架构决策步骤验证 检查是否涉及架构相关关键词 检查是否有决策记录目录 如果涉及架构但没有决策文件，提示警告
**类型**: shell
**路径**: `hooks/bin/architecture-verify.sh`

<!-- CAPABILITY:hooks/bin/check-update.sh -->
#### `hooks/bin/check-update.sh`

**一句话**: !/bin/bash ============================================================ CHK 插件更新检查钩子 - UserPromptSub
**类型**: shell
**路径**: `hooks/bin/check-update.sh`

**核心能力**:
  - `log_info()`
  - `should_check()`
  - `get_local_version()`
  - `get_remote_version()`
  - `version_lt()`

<!-- CAPABILITY:hooks/bin/checkpoint-verify.sh -->
#### `hooks/bin/checkpoint-verify.sh`

**一句话**: !/bin/bash checkpoint-verify.sh - 验证 Checkpoint 文件是否完整 检查备份目录是否存在 关键文件列表
**类型**: shell
**路径**: `hooks/bin/checkpoint-verify.sh`

<!-- CAPABILITY:hooks/bin/doc-verify.sh -->
#### `hooks/bin/doc-verify.sh`

**一句话**: !/usr/bin/env bash doc-verify.sh - 文档验证器 Shell 包装器 用于 Claude Code hook，自动检测插件根目录 自动检测插件根目录 优先级 1: 环境
**类型**: shell
**路径**: `hooks/bin/doc-verify.sh`

**核心能力**:
  - `detect_plugin_root()`

<!-- CAPABILITY:hooks/bin/log-utils.sh -->
#### `hooks/bin/log-utils.sh`

**一句话**: !/bin/bash ============================================================ CHK 共享日志工具 — 被其他 hook 脚本 sou
**类型**: shell
**路径**: `hooks/bin/log-utils.sh`

**核心能力**:
  - `_hook_log_init()`
  - `_hook_log_error()`
  - `_hook_log_warn()`
  - `_hook_log_info()`

<!-- CAPABILITY:hooks/bin/observe.sh -->
#### `hooks/bin/observe.sh`

**一句话**: !/bin/bash observe.sh — Hook 观测事件采集器（shell wrapper） 职责：调用 observe.py，永远 exit 0，零阻塞主流程  设计原则： 1. 永远 e
**类型**: shell
**路径**: `hooks/bin/observe.sh`

<!-- CAPABILITY:hooks/bin/update-registry.sh -->
#### `hooks/bin/update-registry.sh`

**一句话**: !/bin/bash ============================================================ 更新 Capability Registry  用法： 
**类型**: shell
**路径**: `hooks/bin/update-registry.sh`

### 场景: SKILL

<!-- CAPABILITY:harness/_core/instinct_engine.py -->
#### `harness/_core/instinct_engine.py`

**一句话**: instinct_engine.
**类型**: python
**路径**: `harness/_core/instinct_engine.py`

**核心能力**:
  - `InstinctEngine`: 本能推理引擎...
  - `get_engine()`: 获取全局本能引擎...
  - `get_recommendations()`: 获取推荐（顶层函数）...
  - `update_confidence()`: 更新置信度（顶层函数）...
  - `main()`: 测试...

<!-- CAPABILITY:harness/cli/capability-analyzer.py -->
#### `harness/cli/capability-analyzer.py`

**一句话**: Capability Registry 分析器 v2 — 语义化输出
**类型**: python
**路径**: `harness/cli/capability-analyzer.py`

**核心能力**:
  - `SemanticAnalyzer`: 语义化分析器...
  - `generate_semantic_registry()`: 生成语义化注册表...
  - `main()`

<!-- CAPABILITY:harness/cli/generate_skill_index.py -->
#### `harness/cli/generate_skill_index.py`

**一句话**: Generate INDEX.
**类型**: python
**路径**: `harness/cli/generate_skill_index.py`

**核心能力**:
  - `generate_index()`
  - `main()`

<!-- CAPABILITY:harness/evolve-daemon/analyzer.py -->
#### `harness/evolve-daemon/analyzer.py`

**一句话**: 数据分析器 — 聚合多会话数据，识别改进模式。
**类型**: python
**路径**: `harness/evolve-daemon/analyzer.py`

**核心能力**:
  - `_safe_div()`: 安全除法，避免除零...
  - `parse_iso_time()`: 解析 ISO 时间字符串，支持 Z 和时区后缀...
  - `aggregate_and_analyze()`
  - `_analyze_performance()`: 性能维度分析：
- 工具调用耗时统计
- 识别超时模式
- 统计平均响应时间...
  - `_analyze_interaction()`: 交互质量维度分析：
- 分析会话轮次
- 统计任务完成时间
- 用户满意度推断...

<!-- CAPABILITY:harness/evolve-daemon/effect_tracker.py -->
#### `harness/evolve-daemon/effect_tracker.py`

**一句话**: 效果跟踪器 - 跟踪进化改进的有效性
**类型**: python
**路径**: `harness/evolve-daemon/effect_tracker.py`

**核心能力**:
  - `EffectTracker`: 效果跟踪器...
  - `main()`: 测试效果跟踪器...

<!-- CAPABILITY:harness/evolve-daemon/evolve_dispatcher.py -->
#### `harness/evolve-daemon/evolve_dispatcher.py`

**一句话**: 进化分发器 — 8维度分析决策引擎
**类型**: python
**路径**: `harness/evolve-daemon/evolve_dispatcher.py`

**核心能力**:
  - `get_dimension()`: 根据 target 前缀确定维度。

核心维度:
  agent:xxx → agent
  ski...
  - `_load_dimension_thresholds()`: 从 config.yaml 统一加载 8 个维度的进化阈值。

阈值定义在 config.yaml ...
  - `meets_threshold()`: 判断纠正次数是否达到维度阈值。

阈值从 config.yaml 的 thresholds.dime...
  - `build_decision()`: 为指定维度构建进化决策。

返回:
{
    "dimension": str,
    "tar...
  - `_agent_decision()`: Agent 维度进化策略...

<!-- CAPABILITY:harness/evolve-daemon/skill_evolution.py -->
#### `harness/evolve-daemon/skill_evolution.py`

**一句话**: Skill 维度进化策略
**类型**: python
**路径**: `harness/evolve-daemon/skill_evolution.py`

**核心能力**:
  - `evolve_skill()`
  - `_generate_skill_change()`

<!-- CAPABILITY:harness/knowledge/knowledge_recommender.py -->
#### `harness/knowledge/knowledge_recommender.py`

**一句话**: Knowledge Recommender Engine — 知识推荐引擎
**类型**: python
**路径**: `harness/knowledge/knowledge_recommender.py`

**核心能力**:
  - `load_evolved_knowledge()`: 加载进化知识库 (JSONL 格式)...
  - `load_knowledge_base()`: 加载所有知识条目（双知识库合并）

知识库 1: harness/knowledge/ — 手工维护...
  - `load_instinct_usage()`: 从 instinct 数据读取历史使用频率...
  - `extract_keywords()`: 从文本中提取关键词（过滤停用词）...
  - `compute_score()`: 计算单条知识的推荐分数...

<!-- CAPABILITY:harness/tests/graders/base.py -->
#### `harness/tests/graders/base.py`

**一句话**: LLM Grader 基类
**类型**: python
**路径**: `harness/tests/graders/base.py`

**核心能力**:
  - `GradingResult`: 评分结果...
  - `BaseGrader`: 评分器基类...
  - `CodeQualityGrader`: 代码质量评分器...
  - `OutputQualityGrader`: 输出质量评分器...
  - `BehaviorGrader`: 行为评分器 - 验证 Agent/Skill 行为是否符合预期...

<!-- CAPABILITY:harness/tests/graders/pass_at_k.py -->
#### `harness/tests/graders/pass_at_k.py`

**一句话**: Pass@k 指标计算
**类型**: python
**路径**: `harness/tests/graders/pass_at_k.py`

**核心能力**:
  - `PassAtKResult`: Pass@k 结果...
  - `EvaluationRunner`: 评估运行器 - 管理多轮评估...
  - `binomial()`: 计算二项式系数 C(n, k)...
  - `calculate_pass_at_k()`: 计算 pass@k 指标

pass@k = E[1 - C(n-c, k) / C(n, k)]
...
  - `calculate_confidence_interval()`: 计算 pass@k 的置信区间 (使用 bootstrap)

Args:
    results:...
  - `main()`: 命令行入口...

### 场景: VERSION

<!-- CAPABILITY:harness/_core/bump_version.py -->
#### `harness/_core/bump_version.py`

**一句话**: 智能版本管理系统 - 自动分析变更类型
**类型**: python
**路径**: `harness/_core/bump_version.py`

**核心能力**:
  - `read_version()`: 读取 version.json，返回版本数据（不含文件时返回默认值）...
  - `write_version()`: 保存版本数据到 version.json...
  - `get_git_diff_count()`: 获取自上次 git tag 后的提交数量（用于判断变更量）...
  - `analyze_commits()`: 分析最近 git 提交，自动判断版本升级类型

判断逻辑:
  - 包含 "break"/"majo...
  - `update_file()`: 更新单个文件中的版本号（字符串替换）

作用: 将文件中的旧版本号替换为新版本号
原理: 直接文本替...

<!-- CAPABILITY:harness/_core/update_checker.py -->
#### `harness/_core/update_checker.py`

**一句话**: CHK 插件更新检测器 - 从 GitHub 获取最新版本并比较
**类型**: python
**路径**: `harness/_core/update_checker.py`

**核心能力**:
  - `UpdateInfo`: 更新信息数据结构...
  - `get_local_version()`: 获取本地版本号...
  - `parse_version()`: 解析版本字符串，返回 (major, minor, patch) 元组

支持格式：
- "0.9....
  - `compare_versions()`: 比较两个版本号

返回：
- 1  if local > remote
- 0  if local ...
  - `get_remote_version()`: 从 GitHub 获取最新版本

返回：
- (version, release_url, rele...
  - `check_update()`: 检查插件更新

返回 UpdateInfo：
- has_update: 是否有新版本
- loca...

<!-- CAPABILITY:harness/_core/version.py -->
#### `harness/_core/version.py`

**一句话**: CHK 版本管理 - 从 version.
**类型**: python
**路径**: `harness/_core/version.py`

**核心能力**:
  - `_read_version_data()`: 读取版本数据（带缓存，避免重复 IO）...
  - `get_version()`: 获取当前版本...
  - `get_version_info()`: 获取版本信息 (major, minor, patch)...

<!-- CAPABILITY:harness/cli/init.py -->
#### `harness/cli/init.py`

**一句话**: kit init — 自动分析项目，生成高质量 CLAUDE.md 和 .claude/ 配置。
**类型**: python
**路径**: `harness/cli/init.py`

**核心能力**:
  - `parse_package_json()`: 从 package.json 提取依赖和版本...
  - `parse_pom_xml()`: 从 pom.xml 提取关键依赖...
  - `parse_go_mod()`: 从 go.mod 提取依赖...
  - `discover_structure()`: 发现关键目录、入口文件、模块边界...
  - `extract_git_insights()`: 从 git log 提取最近的 fix/refactor 关键词热点...

<!-- CAPABILITY:harness/cli/instinct_cli.py -->
#### `harness/cli/instinct_cli.py`

**一句话**: instinct_cli.
**类型**: python
**路径**: `harness/cli/instinct_cli.py`

**核心能力**:
  - `_get_chk_version()`
  - `load_records()`
  - `save_records()`
  - `confidence_label()`
  - `confidence_bar()`

<!-- CAPABILITY:harness/knowledge/lifecycle.py -->
#### `harness/knowledge/lifecycle.py`

**一句话**: Knowledge Lifecycle Engine — 知识生命周期可执行引擎。
**类型**: python
**路径**: `harness/knowledge/lifecycle.py`

**核心能力**:
  - `load_lifecycle_config()`: 加载 lifecycle.yaml 配置，失败则使用内联默认值...
  - `check_maturity_promotion()`: 检查条目是否可以升级。
返回: "verified" | "proven" | None...
  - `apply_decay()`: 检查条目是否应该衰减降级。
返回: 目标成熟度 | None（无需降级）...
  - `promote_to_layer1()`: 跨项目提升：L3 → L1/L2。
生成提升提案到 proposals/ 目录。
返回: 提案文件路...
  - `cmd_check()`: 检查单条知识的成熟度和衰减状态...

<!-- CAPABILITY:hooks/bin/check-update.sh -->
#### `hooks/bin/check-update.sh`

**一句话**: !/bin/bash ============================================================ CHK 插件更新检查钩子 - UserPromptSub
**类型**: shell
**路径**: `hooks/bin/check-update.sh`

**核心能力**:
  - `log_info()`
  - `should_check()`
  - `get_local_version()`
  - `get_remote_version()`
  - `version_lt()`

## 通用方法 ⭐

> 被 >= 2 处调用的方法，修改时需谨慎

*暂无通用方法*

## 模块详情 (按需加载)

> 以下内容通过 `memory-inject.sh` 按关键词加载

<!-- MODULE:harness/_core/bump_version.py -->
### `harness/_core/bump_version.py`

**类型**: python
**路径**: `harness/_core/bump_version.py`
**一句话**: 智能版本管理系统 - 自动分析变更类型

**使用场景**: `version`

**依赖**: `sys`, `json`, `subprocess`, `pathlib`, `datetime`

**函数**:
  - `read_version()`
    说明: 读取 version.json，返回版本数据（不含文件时返回默认值）
  - `write_version(data)`
    说明: 保存版本数据到 version.json
  - `get_git_diff_count()`
    说明: 获取自上次 git tag 后的提交数量（用于判断变更量）
  - `analyze_commits()`
    说明: 分析最近 git 提交，自动判断版本升级类型

判断逻辑:
  - 包含 "break"/"major" 关键字 → major (破坏性变更)
  - 包含 
  - `update_file(path, old_ver, new_ver)`
    说明: 更新单个文件中的版本号（字符串替换）

作用: 将文件中的旧版本号替换为新版本号
原理: 直接文本替换，匹配 old_ver 字符串
注意: 如果文件不存在或不
  - `generate_changelog(old_ver, new_ver, version_type)`
    说明: 生成 CHANGELOG 条目（Markdown 格式）

作用: 记录版本变更内容
原理: 读取新旧版本之间的 git 提交，生成变更列表
  - `smart_bump(force_type)`
    说明: 智能升级版本号

作用: 根据变更类型自动递增版本号
原理:
  - patch: 0.0.1 → 0.0.2
  - minor: 0.1.0 → 0.2.0
  - `main()`
    说明: 主入口: 解析命令行参数，执行版本升级

---

<!-- MODULE:harness/_core/cache_manager.py -->
### `harness/_core/cache_manager.py`

**类型**: python
**路径**: `harness/_core/cache_manager.py`
**一句话**: cache_manager.

**使用场景**: `memory`, `evolution`

**依赖**: `atexit`, `json`, `time`, `typing`, `paths`

**类**:
  - `CacheStats`
    方法: `__init__()`, `record_hit()`, `record_miss()`, `record_load()`, `hit_rate()`, `to_dict()`, `from_dict()`
  - `CacheEntry`
    方法: `__init__()`, `is_expired()`, `access()`, `to_dict()`
  - `CacheManager`
    方法: `__init__()`, `_load_from_disk()`, `_save_to_disk()`, `get()`, `set()`, `flush()`, `invalidate()`, `get_preload_content()`

**函数**:
  - `get_cache_manager()`
    说明: 获取全局缓存管理器
  - `preload_knowledge()`
    说明: 预加载知识（供 Hook 调用）

返回格式化的预加载内容。
  - `main()`
    说明: CLI 测试

---

<!-- MODULE:harness/_core/config_loader.py -->
### `harness/_core/config_loader.py`

**类型**: python
**路径**: `harness/_core/config_loader.py`
**一句话**: ConfigLoader - 统一配置加载器

**使用场景**: `config`, `cli`, `evolution`

**依赖**: `json`, `logging`, `pathlib`, `typing`

**类**:
  - `ConfigLoader`
    方法: `__init__()`, `get_config()`, `_load_core()`, `_load_daemon()`, `_load_hooks()`, `_load_cli()`, `_load_settings()`, `_load_package()`

**函数**:
  - `get_loader(project_root)`
    说明: 获取全局配置加载器实例

Args:
    project_root: 项目根目录

Returns:
    ConfigLoader 实例
  - `reload()`
    说明: 重新加载全局配置
  - `get_version()`
    说明: 获取 CHK 版本
  - `get_config(config_type)`
    说明: 获取指定类型的配置
  - `validate_all()`
    说明: 验证所有配置

---

<!-- MODULE:harness/_core/exceptions.py -->
### `harness/_core/exceptions.py`

**类型**: python
**路径**: `harness/_core/exceptions.py`
**一句话**: 统一异常处理工具模块

**使用场景**: `error`

**依赖**: `logging`, `typing`

**函数**:
  - `handle_exception(e, context, reraise, default_return, log_level)`
    说明: 统一异常处理

Args:
    e: 异常对象
    context: 错误上下文描述
    reraise: 是否重新抛出
    default_r
  - `safe_execute(func)`
    说明: 安全执行函数，捕获异常返回默认值

Args:
    func: 要执行的函数
    *args: 位置参数
    default: 失败时的默认返回值

  - `safe_json_loads(data, default, context)`
    说明: 安全解析 JSON，捕获 json.JSONDecodeError

Args:
    data: JSON 字符串
    default: 解析失败时的默
  - `safe_file_read(file_path, encoding, default, context)`
    说明: 安全读取文件内容

Args:
    file_path: 文件路径
    encoding: 编码格式
    default: 读取失败时的默认返回值

  - `safe_file_write(file_path, content, encoding, context)`
    说明: 安全写入文件内容

Args:
    file_path: 文件路径
    content: 要写入的内容
    encoding: 编码格式
    c
  - `safe_call_api(func)`
    说明: 安全调用 API 或外部服务，支持重试

Args:
    func: 要执行的函数
    *args: 位置参数
    default: 失败时的默认返

---

<!-- MODULE:harness/_core/instinct_engine.py -->
### `harness/_core/instinct_engine.py`

**类型**: python
**路径**: `harness/_core/instinct_engine.py`
**一句话**: instinct_engine.

**使用场景**: `memory`, `skill`, `agent`

**依赖**: `json`, `datetime`, `typing`, `paths`

**类**:
  - `InstinctEngine`
    方法: `__init__()`, `_load()`, `_save()`, `detect_scene()`, `get_recommendations()`, `update_confidence()`, `add_instinct()`, `format_as_context()`

**函数**:
  - `get_engine()`
    说明: 获取全局本能引擎
  - `get_recommendations(task)`
    说明: 获取推荐（顶层函数）
  - `update_confidence(instinct_id, delta)`
    说明: 更新置信度（顶层函数）
  - `main()`
    说明: 测试

---

<!-- MODULE:harness/_core/instinct_reader.py -->
### `harness/_core/instinct_reader.py`

**类型**: python
**路径**: `harness/_core/instinct_reader.py`
**一句话**: 本能读取模块 - 从 instinct-record.

**使用场景**: `memory`

**依赖**: `json`, `logging`, `dataclasses`, `datetime`, `pathlib`

**类**:
  - `Instinct`

**函数**:
  - `_load_instincts()`
    说明: 加载本能记录
  - `get_high_confidence_instincts(min_confidence)`
    说明: 获取高置信度本能列表

Args:
    min_confidence: 最小置信度阈值，默认 0.7

Returns:
    高置信度本能列表，按置信度
  - `format_instinct_for_injection(instinct)`
    说明: 格式化本能为注入文本

Args:
    instinct: 本能对象

Returns:
    格式化的注入文本
  - `format_all_instincts_for_injection(instincts)`
    说明: 格式化所有本能为注入文本

Args:
    instincts: 本能列表

Returns:
    格式化的注入文本
  - `get_instinct_stats()`
    说明: 获取本能统计信息
  - `_load_stats()`
    说明: 加载本能应用统计
  - `_save_stats(stats)`
    说明: 保存本能应用统计
  - `record_instinct_application(instinct_id, success)`
    说明: 记录本能应用结果（用于追踪成功率）

Args:
    instinct_id: 本能 ID
    success: 是否成功应用

Returns:
  
  - `get_application_stats()`
    说明: 获取本能应用成功率统计

Returns:
    {
        "total_apps": int,      # 总应用次数
        "tot
  - `format_application_stats()`
    说明: 格式化应用统计为可读文本

Returns:
    格式化的统计文本
  - `main()`
    说明: 主入口 - 测试用

---

<!-- MODULE:harness/_core/instinct_state.py -->
### `harness/_core/instinct_state.py`

**类型**: python
**路径**: `harness/_core/instinct_state.py`
**一句话**: 本能状态管理模块 - 跟踪当前会话已注入的本能

**使用场景**: `memory`

**依赖**: `json`, `os`, `datetime`, `pathlib`, `typing`

**类**:
  - `SessionState`
    方法: `__init__()`, `_get_session_id()`, `_load_state()`, `_save_state()`, `is_L0_injected()`, `mark_L0_injected()`, `is_instinct_injected()`, `mark_instinct_injected()`

**函数**:
  - `get_session_state()`
    说明: 获取会话状态单例
  - `cleanup_all_sessions()`
    说明: 清理所有会话状态

---

<!-- MODULE:harness/_core/keyword_matcher.py -->
### `harness/_core/keyword_matcher.py`

**类型**: python
**路径**: `harness/_core/keyword_matcher.py`
**一句话**: 关键词匹配模块 - 根据用户输入匹配相关记忆

**使用场景**: `memory`

**依赖**: `typing`

**函数**:
  - `match_keywords(user_input)`
    说明: 匹配用户输入中的关键词

Args:
    user_input: 用户输入文本

Returns:
    匹配的关键词类别列表
  - `get_matching_files(categories)`
    说明: 获取匹配的记忆文件列表

Args:
    categories: 匹配的类别列表

Returns:
    记忆文件路径列表
  - `format_matched_keywords(categories)`
    说明: 格式化匹配结果为可读文本

Args:
    categories: 匹配的类别列表

Returns:
    格式化文本
  - `check_and_match(user_input)`
    说明: 检查并匹配关键词，返回类别和文件

Args:
    user_input: 用户输入文本

Returns:
    (匹配的类别列表, 匹配的文件列表)
  - `main()`
    说明: 测试

---

<!-- MODULE:harness/_core/path_guard.py -->
### `harness/_core/path_guard.py`

**类型**: python
**路径**: `harness/_core/path_guard.py`
**一句话**: path_guard.

**使用场景**: `path`, `hook`, `config`

**依赖**: `os`, `re`, `typing`

**类**:
  - `PathGuard`
    方法: `__init__()`, `_compile_patterns()`, `is_dangerous_path()`, `is_dangerous_command()`, `_in_allowed_dir()`, `validate_path()`, `validate_command()`

**函数**:
  - `validate_path_scope(path, allowed_dirs)`
    说明: 验证路径是否在白名单内（顶层函数，供 paths.py 调用）

Args:
    path: 待验证路径
    allowed_dirs: 允许目录列表

  - `check_access(path, allowed_dirs)`
    说明: 检查路径访问权限

Args:
    path: 待检查路径
    allowed_dirs: 允许目录列表

Returns:
    True 如果有权
  - `get_guard()`
    说明: 获取全局路径守卫
  - `main()`
    说明: 测试

---

<!-- MODULE:harness/_core/update_checker.py -->
### `harness/_core/update_checker.py`

**类型**: python
**路径**: `harness/_core/update_checker.py`
**一句话**: CHK 插件更新检测器 - 从 GitHub 获取最新版本并比较

**使用场景**: `version`

**依赖**: `json`, `logging`, `subprocess`, `sys`, `urllib.request`

**类**:
  - `UpdateInfo`

**函数**:
  - `get_local_version()`
    说明: 获取本地版本号
  - `parse_version(version_str)`
    说明: 解析版本字符串，返回 (major, minor, patch) 元组

支持格式：
- "0.9.1" -> (0, 9, 1)
- "v0.9.1" -> 
  - `compare_versions(local, remote)`
    说明: 比较两个版本号

返回：
- 1  if local > remote
- 0  if local == remote
- -1 if local < remo
  - `get_remote_version()`
    说明: 从 GitHub 获取最新版本

返回：
- (version, release_url, release_notes)
- 失败时返回 ("0.0.0", "
  - `check_update()`
    说明: 检查插件更新

返回 UpdateInfo：
- has_update: 是否有新版本
- local_version: 本地版本
- remote_versi
  - `format_update_message(info)`
    说明: 格式化更新通知消息
  - `main()`
    说明: 主入口

---

<!-- MODULE:harness/_core/version.py -->
### `harness/_core/version.py`

**类型**: python
**路径**: `harness/_core/version.py`
**一句话**: CHK 版本管理 - 从 version.

**使用场景**: `version`

**依赖**: `json`, `functools`, `pathlib`

**函数**:
  - `_read_version_data()`
    说明: 读取版本数据（带缓存，避免重复 IO）
  - `get_version()`
    说明: 获取当前版本
  - `get_version_info()`
    说明: 获取版本信息 (major, minor, patch)

---

<!-- MODULE:harness/cli/capability-analyzer.py -->
### `harness/cli/capability-analyzer.py`

**类型**: python
**路径**: `harness/cli/capability-analyzer.py`
**一句话**: Capability Registry 分析器 v2 — 语义化输出

**使用场景**: `skill`, `cli`

**依赖**: `ast`, `json`, `os`, `re`, `sys`

**类**:
  - `SemanticAnalyzer`
    方法: `__init__()`, `scan()`, `_analyze_python()`, `_analyze_javascript()`, `_analyze_shell()`, `_extract_one_sentence()`, `_infer_scenarios()`, `analyze_common_methods()`

**函数**:
  - `generate_semantic_registry(analyzer, output_path)`
    说明: 生成语义化注册表
  - `main()`

---

<!-- MODULE:harness/cli/gc.py -->
### `harness/cli/gc.py`

**类型**: python
**路径**: `harness/cli/gc.py`
**一句话**: 知识垃圾回收 CLI — kit gc 命令。

**使用场景**: `path`, `agent`, `cli`

**依赖**: `json`, `subprocess`, `sys`, `datetime`, `pathlib`

**函数**:
  - `run_gc_agent(knowledge_dir, output_path)`
    说明: 通过 Claude Code CLI 调用 GC Agent
  - `generate_fallback_report(knowledge_dir, output_path, timestamp)`
    说明: 无 Claude Code 时生成基础扫描报告
  - `main()`

---

<!-- MODULE:harness/cli/generate_skill_index.py -->
### `harness/cli/generate_skill_index.py`

**类型**: python
**路径**: `harness/cli/generate_skill_index.py`
**一句话**: Generate INDEX.

**使用场景**: `skill`, `cli`

**依赖**: `pathlib`

**函数**:
  - `generate_index(skill_dir, data)`
  - `main()`

---

<!-- MODULE:harness/cli/init.py -->
### `harness/cli/init.py`

**类型**: python
**路径**: `harness/cli/init.py`
**一句话**: kit init — 自动分析项目，生成高质量 CLAUDE.md 和 .claude/ 配置。

**使用场景**: `path`, `version`, `config`

**依赖**: `os`, `re`, `sys`, `json`, `subprocess`

**函数**:
  - `parse_package_json(path)`
    说明: 从 package.json 提取依赖和版本
  - `parse_pom_xml(path)`
    说明: 从 pom.xml 提取关键依赖
  - `parse_go_mod(path)`
    说明: 从 go.mod 提取依赖
  - `discover_structure(root)`
    说明: 发现关键目录、入口文件、模块边界
  - `extract_git_insights(root)`
    说明: 从 git log 提取最近的 fix/refactor 关键词热点
  - `generate_claude_md(root, tech, structure)`
    说明: Map Not Manual 风格 — <100 行，含关键信息 + 指针
  - `create_skeleton(root)`
    说明: 创建 .claude/ 完整骨架
  - `validate_target_path(target)`
    说明: 验证并解析目标路径

检查:
- 路径是否存在
- 是否为目录
- 路径安全性（防止路径遍历攻击）

Args:
    target: 用户输入的目标路径，如
  - `main()`

---

<!-- MODULE:harness/cli/instinct_cli.py -->
### `harness/cli/instinct_cli.py`

**类型**: python
**路径**: `harness/cli/instinct_cli.py`
**一句话**: instinct_cli.

**使用场景**: `memory`, `evolution`, `version`

**依赖**: `sys`, `json`, `argparse`, `datetime`, `pathlib`

**函数**:
  - `_get_chk_version()`
  - `load_records()`
  - `save_records(data)`
  - `confidence_label(confidence)`
  - `confidence_bar(confidence, width)`
  - `cmd_status(args)`
  - `_time_ago(iso_str)`
  - `cmd_export(args)`
  - `cmd_import(args)`
  - `cmd_evolve(args)`
  - `cmd_add(args)`
  - `main()`

---

<!-- MODULE:harness/cli/migrate.py -->
### `harness/cli/migrate.py`

**类型**: python
**路径**: `harness/cli/migrate.py`
**一句话**: kit migrate — 项目迁移编排器。

**使用场景**: `agent`, `cli`

**依赖**: `argparse`, `sys`, `pathlib`, `datetime`

**函数**:
  - `validate_playbook(playbook_path)`
    说明: 验证 playbook 是否有效
  - `generate_report(project_dir, phases, output_path)`
    说明: 生成迁移报告
  - `main()`

---

<!-- MODULE:harness/cli/mode.py -->
### `harness/cli/mode.py`

**类型**: python
**路径**: `harness/cli/mode.py`
**一句话**: chk mode — 切换 Claude Code 执行模式。

**使用场景**: `agent`, `hook`, `config`

**依赖**: `json`, `os`, `shutil`, `sys`, `warnings`

**函数**:
  - `load_mode_template(mode_name)`
    说明: 加载指定模式的 hook 配置模板
  - `load_settings(root)`
    说明: 加载或初始化 settings.local.json
  - `save_settings(root, settings)`
    说明: 保存 settings.local.json
  - `switch_mode(mode_name, root)`
    说明: 切换到指定模式
  - `show_current_mode(root)`
    说明: 显示当前模式
  - `main()`

---

<!-- MODULE:harness/cli/scan.py -->
### `harness/cli/scan.py`

**类型**: python
**路径**: `harness/cli/scan.py`
**一句话**: kit scan — 扫描多代码库目录，评估改造量。

**使用场景**: `path`, `cli`

**依赖**: `json`, `os`, `sys`, `pathlib`, `datetime`

**函数**:
  - `scan_directory(base)`
    说明: 扫描目录下所有项目
  - `main()`

---

<!-- MODULE:harness/cli/status.py -->
### `harness/cli/status.py`

**类型**: python
**路径**: `harness/cli/status.py`
**一句话**: kit status — 查看 Claude Harness Kit 当前状态。

**使用场景**: `memory`, `hook`, `config`

**依赖**: `json`, `os`, `sys`, `pathlib`, `collections`

**函数**:
  - `load_settings(root)`
  - `count_files(pattern)`
  - `main()`

---

<!-- MODULE:harness/cli/sync.py -->
### `harness/cli/sync.py`

**类型**: python
**路径**: `harness/cli/sync.py`
**一句话**: kit sync — 从中央配置仓库同步团队共享规则。

**使用场景**: `config`, `cli`

**依赖**: `argparse`, `hashlib`, `os`, `sys`, `datetime`

**函数**:
  - `_hash_file(path)`
    说明: 计算文件 SHA256（用于增量同步）
  - `find_root()`
  - `_get_default_source()`
    说明: 获取默认团队仓库 URL
  - `sync_from_local(source, root, dry_run)`
    说明: 从本地目录同步，返回同步统计
  - `sync_from_git(url, root, dry_run)`
    说明: 从 Git 仓库同步
  - `_print_stats(stats)`
    说明: 打印同步统计
  - `main()`

---

<!-- MODULE:harness/evolve-daemon/agent_evolution.py -->
### `harness/evolve-daemon/agent_evolution.py`

**类型**: python
**路径**: `harness/evolve-daemon/agent_evolution.py`
**一句话**: Agent 维度进化策略

**使用场景**: `agent`, `evolution`

**依赖**: `json`, `datetime`, `pathlib`

**函数**:
  - `evolve_agent(target, corrections, config, root)`
  - `_generate_agent_change(agent_name, corrections)`

---

<!-- MODULE:harness/evolve-daemon/analyzer.py -->
### `harness/evolve-daemon/analyzer.py`

**类型**: python
**路径**: `harness/evolve-daemon/analyzer.py`
**一句话**: 数据分析器 — 聚合多会话数据，识别改进模式。

**使用场景**: `agent`, `skill`, `evolution`

**依赖**: `json`, `re`, `statistics`, `collections`, `datetime`

**函数**:
  - `_safe_div(numerator, denominator, default)`
    说明: 安全除法，避免除零
  - `parse_iso_time(ts)`
    说明: 解析 ISO 时间字符串，支持 Z 和时区后缀
  - `aggregate_and_analyze(sessions, config, root)`
  - `_analyze_performance(sessions)`
    说明: 性能维度分析：
- 工具调用耗时统计
- 识别超时模式
- 统计平均响应时间
  - `_analyze_interaction(sessions)`
    说明: 交互质量维度分析：
- 分析会话轮次
- 统计任务完成时间
- 用户满意度推断
  - `_analyze_security(sessions)`
    说明: 安全性维度分析：
- 统计危险操作拦截
- 分析权限请求合理性
- 检测敏感信息暴露模式
  - `_analyze_context(sessions, config, root)`
    说明: 上下文维度分析：
- 分析上下文切换频率
- 统计知识复用率
- 多轮对话连贯性
  - `_meets_safety_checks(config, correction_targets)`
    说明: 检查安全限制

---

<!-- MODULE:harness/evolve-daemon/apply_change.py -->
### `harness/evolve-daemon/apply_change.py`

**类型**: python
**路径**: `harness/evolve-daemon/apply_change.py`
**一句话**: 自动应用模块 — 根据 LLM 决策自动应用改动。

**使用场景**: `memory`, `evolution`

**依赖**: `json`, `re`, `sys`, `datetime`, `pathlib`

**函数**:
  - `backup_file(file_path, backups_dir, decision_id)`
    说明: 备份原文件到 backups_dir
  - `restore_file(backup_path, original_path)`
    说明: 从备份恢复文件
  - `apply_text_change(content, change)`
    说明: 应用文本改动。

change 可以是：
1. 精确替换: "old_text -> new_text"
2. 行追加: "append: content"
3
  - `apply_change(decision, root)`
    说明: 根据 decision 自动应用改动。

返回: True 成功，False 失败
  - `_sync_to_memory(decision, root)`
    说明: 同步知识到记忆系统
  - `record_proposal(decision, root, backup_path)`
    说明: 记录提案历史到 proposal_history.json
  - `_collect_baseline_metrics(root)`
    说明: 收集基线指标（用于后续验证对比）
  - `_update_instinct(decision, root)`
    说明: 更新 instinct 记录
  - `rollback_proposal(proposal_id, root, reason)`
    说明: 回滚指定提案。

返回: True 成功，False 失败
  - `consolidate_proposal(proposal_id, root)`
    说明: 固化提案（观察期通过）
  - `get_proposal_status(proposal_id, root)`
    说明: 获取提案状态

---

<!-- MODULE:harness/evolve-daemon/daemon.py -->
### `harness/evolve-daemon/daemon.py`

**类型**: python
**路径**: `harness/evolve-daemon/daemon.py`
**一句话**: 进化守护进程入口 — 支持外部触发和内置定时任务。

**使用场景**: `memory`, `agent`, `config`

**依赖**: `json`, `logging`, `os`, `signal`, `sys`

**函数**:
  - `handle_exception(e, context, reraise, default_return, log_level)`
    说明: 统一异常处理包装函数（本地定义避免循环依赖）
  - `_stop_scheduler()`
    说明: 停止调度器（共享逻辑）
  - `_save_state(signame, key)`
    说明: 保存状态（共享逻辑）
  - `graceful_shutdown(signum, frame)`
    说明: 优雅退出处理函数
  - `graceful_restart(signum, frame)`
    说明: 优雅重启处理函数（SIGUSR1）
  - `_health_check()`
    说明: 健康检查方法 - 检查进程状态和关键文件

返回:
    dict: 健康状态 {"healthy": bool, "checks": [...], "mes
  - `_ensure_config_backup(root)`
    说明: 确保配置文件已备份（共享逻辑）
  - `_backup_config(config_path, backup_dir, max_backups)`
    说明: 备份配置文件

参数:
    config_path: 配置文件路径
    backup_dir: 备份目录
    max_backups: 最大保留备份
  - `load_config()`
  - `load_new_sessions(data_dir, last_analyzed_id)`
    说明: 加载自上次分析以来的新会话
  - `check_thresholds(sessions, config, last_analyze_time)`
    说明: 检查是否满足触发条件
  - `run_analysis(config, root, sessions)`
    说明: 执行分析并生成提案（4维度进化闭环）
  - `_execute_auto_apply(decision, analysis, config, root)`
    说明: 执行 auto_apply 决策
  - `_execute_propose(decision, analysis, config, root)`
    说明: 执行 propose 决策
  - `_apply_file_change(target_file, suggested_change, config, root)`
    说明: 将改动应用到文件
  - `_record_rollback_to_instinct(proposal, root, reason, config)`
    说明: 将回滚事件记录到 instinct-record.json。

回滚被视为"负向验证"，降低关联本能的置信度，
同时更新知识库的置信度。
  - `run_rollback_check(config, root)`
    说明: 执行回滚检查：观察期到期的提案评估并回滚/固化。

返回检查结果。
  - `install_launchd(root)`
    说明: macOS: 生成 LaunchAgent plist 并安装
  - `main()`

---

<!-- MODULE:harness/evolve-daemon/effect_tracker.py -->
### `harness/evolve-daemon/effect_tracker.py`

**类型**: python
**路径**: `harness/evolve-daemon/effect_tracker.py`
**一句话**: 效果跟踪器 - 跟踪进化改进的有效性

**使用场景**: `memory`, `agent`, `skill`

**依赖**: `json`, `sys`, `datetime`, `pathlib`, `typing`

**类**:
  - `EffectTracker`
    方法: `__init__()`, `track()`, `_promote_instinct_confidence()`, `_update_kb_confidence()`, `run_test()`, `_has_execution_env()`, `_shadow_test()`, `_real_task_test()`

**函数**:
  - `main()`
    说明: 测试效果跟踪器

---

<!-- MODULE:harness/evolve-daemon/evolve_dispatcher.py -->
### `harness/evolve-daemon/evolve_dispatcher.py`

**类型**: python
**路径**: `harness/evolve-daemon/evolve_dispatcher.py`
**一句话**: 进化分发器 — 8维度分析决策引擎

**使用场景**: `memory`, `skill`, `evolution`

**依赖**: `json`, `sys`, `pathlib`, `datetime`, `harness.paths`

**函数**:
  - `get_dimension(target)`
    说明: 根据 target 前缀确定维度。

核心维度:
  agent:xxx → agent
  skill:xxx → skill
  rule:xxx  → r
  - `_load_dimension_thresholds()`
    说明: 从 config.yaml 统一加载 8 个维度的进化阈值。

阈值定义在 config.yaml 的 thresholds.dimensions 块中，
所有
  - `meets_threshold(dimension, count)`
    说明: 判断纠正次数是否达到维度阈值。

阈值从 config.yaml 的 thresholds.dimensions 块读取，统一管理。
  - `build_decision(dimension, target, analysis, config, root)`
    说明: 为指定维度构建进化决策。

返回:
{
    "dimension": str,
    "target": str,
    "target_file": 
  - `_agent_decision(target, pattern_key, examples, analysis, config)`
    说明: Agent 维度进化策略
  - `_skill_decision(target, pattern_key, examples, analysis, config)`
    说明: Skill 维度进化策略
  - `_rule_decision(target, pattern_key, examples, analysis, config)`
    说明: Rule 维度进化策略
  - `_instinct_decision(target, pattern_key, examples, analysis, config)`
    说明: Instinct 维度进化策略
  - `_performance_decision(target, pattern_key, examples, analysis, config)`
    说明: 性能维度进化策略

分析内容:
- 工具调用耗时
- 超时模式识别
- 慢工具优化建议
  - `_interaction_decision(target, pattern_key, examples, analysis, config)`
    说明: 交互质量维度进化策略

分析内容:
- 会话轮次
- 任务完成时间
- 用户满意度推断
  - `_security_decision(target, pattern_key, examples, analysis, config)`
    说明: 安全性维度进化策略

分析内容:
- 危险操作拦截
- 权限请求合理性
- 敏感信息暴露检测
  - `_context_decision(target, pattern_key, examples, analysis, config)`
    说明: 上下文维度进化策略

分析内容:
- 上下文切换频率
- 知识复用率
- 多轮对话连贯性
  - `dispatch_evolution(analysis, config, root, sessions)`
    说明: 统一进化信号处理器 — 8维度分发。

4个核心维度: agent, skill, rule, instinct
4个扩展维度: performance, in
  - `_dispatch_extended_dimensions(analysis, instinct_ids)`
    说明: 处理4个扩展维度的进化决策

这些维度不依赖于 correction_hotspots，而是直接分析其数据
  - `main()`
    说明: CLI 测试入口

---

<!-- MODULE:harness/evolve-daemon/extract_semantics.py -->
### `harness/evolve-daemon/extract_semantics.py`

**类型**: python
**路径**: `harness/evolve-daemon/extract_semantics.py`
**一句话**: 语义提取器封装 — 为 daemon.py 提供 analyze_session() API。

**使用场景**: `memory`, `evolution`, `hook`

**依赖**: `json`, `sys`, `pathlib`, `kb_shared`, `harness.paths`

**函数**:
  - `extract_with_haiku(session)`
    说明: 调用 Claude Haiku 提取纠正上下文（统一 LLM 配置）。

底层使用 kb_shared.get_llm_config()，所有 LLM 调用路径
  - `analyze_session(session, root)`
    说明: 分析单个会话，提取语义并回填。

Args:
    session: 会话 dict（必须包含 session_id）
    root: 项目根目录

Re
  - `analyze_sessions(sessions, root)`
    说明: 批量分析多个会话。

Returns: 每个会话的分析结果列表
  - `_record_to_instinct(corrections, root)`
    说明: 将新发现的纠正模式记录到 instinct-record.json，返回 record_ids
  - `main()`
    说明: CLI 测试入口

---

<!-- MODULE:harness/evolve-daemon/generalize.py -->
### `harness/evolve-daemon/generalize.py`

**类型**: python
**路径**: `harness/evolve-daemon/generalize.py`
**一句话**: generalize.

**使用场景**: `evolution`, `error`

**依赖**: `json`, `os`, `pathlib`, `kb_shared`

**函数**:
  - `_has_llm_access()`
    说明: 检查是否有 LLM 调用能力（代理或真实 API Key）
  - `call_haiku(system, user, config)`
    说明: 用 Haiku 做简单判断（reuse/new）
  - `call_sonnet(system, user, config)`
    说明: 用 Sonnet 做深度分析（新根因、merge 风险）
  - `call_llm_fallback(user, errors)`
    说明: 无 API Key 时的本地规则降级。
用硬编码的启发式规则判断 reuse / new。
  - `build_step1_prompt(errors, kb)`
    说明: 构建第一步 prompt：批量关联分析
  - `build_step2_prompt(error, kb_entry)`
    说明: 构建第二步 prompt：新根因深度分析
  - `build_step3_prompt(kb_entries, merged_pattern)`
    说明: 构建第三步 prompt：merge 风险评估
  - `process_errors(errors, root, config)`
    说明: 处理一批错误的完整流程。

返回：每个错误的处理结果
[
  {
    "error_index": 0,
    "action": "reuse" | "
  - `_do_reuse(result, error, root)`
    说明: 执行 reuse：追加更新后的知识到 knowledge_base.jsonl（避免全量重写）
  - `_do_merge(kb_entries, merged_pattern, risk, root)`
    说明: 执行 merge：合并多个知识为一个更通用的
  - `_do_new(result, error, root)`
    说明: 创建新知识

---

<!-- MODULE:harness/evolve-daemon/instinct_updater.py -->
### `harness/evolve-daemon/instinct_updater.py`

**类型**: python
**路径**: `harness/evolve-daemon/instinct_updater.py`
**一句话**: Instinct 自动更新器 — 管理本能记录的完整生命周期。

**使用场景**: `memory`, `evolution`, `error`

**依赖**: `json`, `sys`, `datetime`, `pathlib`, `typing`

**函数**:
  - `_parse_iso_safe(ts, default)`
    说明: 安全解析 ISO 时间字符串，失败时返回默认值
  - `load_instinct(root)`
    说明: 加载或初始化 instinct-record.json
  - `save_instinct(instinct, root)`
    说明: 保存 instinct-record.json
  - `time_decay_weight(created_at, last_reinforced, half_life_days)`
    说明: 计算时间衰减权重。

公式: weight = 0.5 ^ (age_days / half_life_days)

例如: 90 天后权重为 0.5, 180
  - `apply_decay_to_all(instinct, config)`
    说明: 对所有非 seed 记录应用时间衰减。

规则:
- seed 记录不衰减
- reinforcement_count >= 3 的记录半衰期延长 50%
- 
  - `add_pattern(pattern, correction, root_cause, confidence, source)`
    说明: 向 instinct-record.json 添加一条记录，返回记录 ID。
  - `promote_confidence(record_id, delta, root)`
    说明: 增加已有记录的置信度（用于观察期后的升级）。
同时增加 reinforcement_count 和 last_reinforced_at。
  - `demote_confidence(record_id, delta, root)`
    说明: 降低已有记录的置信度（用于回滚场景）。
  - `reinforce_pattern(pattern_id, delta, root)`
    说明: 验证成功后增强置信度（alias for promote_confidence）。
  - `get_patterns_by_source(source, root)`
    说明: 获取指定来源的所有 pattern
  - `get_high_confidence_patterns(threshold, root)`
    说明: 获取高置信度的 pattern（用于指导决策）
  - `increment_applied_count(record_id, root)`
    说明: 增加 applied_count 计数
  - `link_instinct_to_target(record_id, target_file, root)`
    说明: 将 instinct 记录与目标文件关联
  - `find_instinct_by_target(target_file, root)`
    说明: 根据 target_file 查找 instinct 记录

---

<!-- MODULE:harness/evolve-daemon/integrated_evolution.py -->
### `harness/evolve-daemon/integrated_evolution.py`

**类型**: python
**路径**: `harness/evolve-daemon/integrated_evolution.py`
**一句话**: integrated_evolution.

**使用场景**: `hook`, `config`, `evolution`

**依赖**: `json`, `os`, `sys`, `datetime`, `pathlib`

**函数**:
  - `collect_session_errors(max_age_hours)`
    说明: 收集本会话的错误。
只收集最近 max_age_hours 小时内的新错误。
  - `_extract_context(entry)`
    说明: 从错误条目中提取上下文
  - `run_session_evolution(max_errors, max_age_hours)`
    说明: 会话级进化主流程。

每次会话结束时调用。
  - `_load_config()`
    说明: 加载配置
  - `run_full_analysis()`
    说明: 不限制会话，强制分析所有未知错误

---

<!-- MODULE:harness/evolve-daemon/kb_shared.py -->
### `harness/evolve-daemon/kb_shared.py`

**类型**: python
**路径**: `harness/evolve-daemon/kb_shared.py`
**一句话**: kb_shared.

**使用场景**: `memory`, `config`, `cli`

**依赖**: `json`, `os`, `uuid`, `datetime`, `pathlib`

**函数**:
  - `_ensure_env_loaded()`
    说明: 从 Claude Code 配置自动加载环境变量（幂等，所有 LLM 模块共享）

自动读取 ~/.claude/settings.json 的 env 配置，
  - `get_model()`
    说明: 获取统一模型（ANTHROPIC_MODEL），无则返回 None
  - `get_haiku_model()`
    说明: 快速分类模型：有 ANTHROPIC_MODEL 用它，否则用默认 Haiku
  - `get_sonnet_model()`
    说明: 深度分析模型：有 ANTHROPIC_MODEL 用它，否则用默认 Sonnet
  - `get_llm_config()`
    说明: 统一 LLM 配置参数，所有模块引用此处
  - `create_llm_client()`
    说明: 创建统一的 LLM 客户端。

⚠️ 已废弃：进化系统的 LLM 任务应由 Claude Code 会话中的 Agent 执行，
不再独立配置 Anthropi
  - `_find_root()`
    说明: 向上查找项目根目录。

项目根 = 含 .claude/ 的目录。
特殊处理：从 harness/evolve-daemon/ 内运行时，向上找到真正的根。
  - `_evolve_dir()`
    说明: 获取 harness/evolve-daemon/ 目录路径。

从 kb_shared.py 所在位置推导，确保无论从哪个 cwd 调用都正确。
  - `_knowledge_dir()`
    说明: 返回统一的知识库目录（harness/knowledge/evolved/）
  - `_get_paths()`
    说明: 延迟导入 paths 模块，避免循环导入
  - `now_iso()`
  - `hours_ago(hours)`
  - `days_ago(days)`
  - `load_sessions(data_dir)`
    说明: 读取 sessions.jsonl，统一所有模块的会话加载逻辑
  - `read_jsonl(path)`
    说明: 读取 JSONL 文件，返回 list[dict]（跳过损坏行）
  - `append_jsonl(path, entry)`
    说明: 追加一条到 JSONL 文件
  - `write_jsonl(path, entries)`
    说明: 原子写入整个 JSONL 文件（先写临时文件再 rename，防止并发冲突）
  - `read_json(path)`
    说明: 读取 JSON 文件
  - `write_json(path, data)`
    说明: 写入 JSON 文件
  - `load_knowledge_base(root)`
    说明: 加载所有知识库条目
  - `load_active_kb(root)`
    说明: 加载活跃知识（未被 superseded）
  - `save_kb_entry(entry, root)`
    说明: 追加一条知识到知识库
  - `update_kb_all(entries, root)`
    说明: 重写整个知识库
  - `find_kb_by_id(kb_id, root)`
    说明: 根据 ID 查找知识
  - `find_kb_by_pattern(pattern, root)`
    说明: 根据 error_type 查找知识
  - `find_kb_by_dimension(dimension, target, root)`
    说明: 根据维度 + target 查找知识
  - `update_kb_confidence(kb_id, outcome, root)`
    说明: 根据测试结果更新知识置信度。
唯一来源：自动化测试。
  - `_track_effect(kb_id, outcome, root)`
    说明: 写入 effect_tracking.jsonl（使用统一路径常量避免重复拼接）
  - `should_auto_apply(entry)`
    说明: 判断知识是否应该自动应用。
返回: (should_apply, reason)
  - `is_covered_by_kb(correction_text, root)`
    说明: 检查纠正是否已被知识库覆盖（语义相似度检查）。
优先用 LLM 做语义匹配，fallback 到字符串包含匹配。
返回: (is_covered, matche
  - `_semantic_match(text, kb)`
    说明: 用 LLM 做语义相似度匹配。
返回匹配的 KB 条目 ID，或 None。
  - `should_activate(entry)`
    说明: 判断 unconfirmed 知识是否可以激活
  - `deprecate_knowledge(kb_id, reason, root)`
    说明: 将知识降级为 deprecated
  - `reactivate_knowledge(kb_id, root)`
    说明: 将 deprecated 知识重新激活（用新证据）
  - `check_merge_cooldown(kb_ids, hours)`
    说明: 检查这组 kb_ids 是否处于 merge abort 冷却期。
返回: True = 在冷却期内，不能 merge；False = 可以 merge
  - `record_merge_abort(kb_ids, reason)`
    说明: 记录 merge abort
  - `clear_expired_cooldown(hours)`
    说明: 清理过期的 abort 记录
  - `notify_llm_failure(error, context, notify_url)`
    说明: LLM 调用失败时发送飞书通知。
通知后系统继续自动运行（零人工）。
  - `decay_knowledge(root)`
    说明: 定期知识衰减。
- 30 天未验证的知识：置信度缓慢下降
- 衰退后成功率 < 70%：标记为 deprecated
  - `migrate_from_instinct(root)`
    说明: 从 instinct-record.json 迁移数据到 knowledge_base.jsonl。
只迁移活跃的（source != seed）记录。
  - `generate_kb_id()`
    说明: 生成知识库 ID
  - `create_new_knowledge(error, analysis, reasoning_chain, root_cause_category, abstraction_level)`
    说明: 创建新知识条目
  - `get_kb_stats(root)`
    说明: 获取知识库统计
  - `print_kb_stats(root)`
    说明: 打印知识库统计

---

<!-- MODULE:harness/evolve-daemon/llm_decision.py -->
### `harness/evolve-daemon/llm_decision.py`

**类型**: python
**路径**: `harness/evolve-daemon/llm_decision.py`
**一句话**: LLM 决策引擎 — 用 LLM 分析会话数据，决定下一步行动。

**使用场景**: `memory`, `evolution`, `config`

**依赖**: `json`, `logging`, `sys`, `pathlib`, `datetime`

**函数**:
  - `load_config()`
    说明: 加载配置（使用统一配置模块）
  - `_default_config()`
  - `get_existing_targets(instinct)`
    说明: 获取 instinct 中已有的 target 列表
  - `is_new_target(target, instinct)`
    说明: 判断是否是新 target（未在 instinct 中出现）
  - `assess_risk(analysis, config)`
    说明: 评估风险等级（0.0 - 1.0）。

规则:
- 高风险模式（permission, security, auth）→ 1.0
- 多文件修改 → 0.8
-
  - `call_claude_api(system_prompt, user_message, config)`
    说明: 调用 Claude API（统一 LLM 配置）
  - `decide_action(sessions, analysis, config)`
    说明: LLM 决策主函数。

返回:
{
    "action": "auto_apply" | "propose" | "skip",
    "reason":
  - `_rule_based_decision(analysis, config)`
    说明: 规则引擎降级决策
  - `_check_circuit_breaker(config)`
    说明: 检查熔断器状态。

检测条件（任一触发即熔断）：
1. 同一目标连续被拒绝次数 >= max_consecutive_rejects
2. 每周回滚次数 >= 
  - `get_decision_stats(history_file)`
    说明: 获取决策统计

---

<!-- MODULE:harness/evolve-daemon/memory_sync.py -->
### `harness/evolve-daemon/memory_sync.py`

**类型**: python
**路径**: `harness/evolve-daemon/memory_sync.py`
**一句话**: 知识同步模块 - 将进化系统产生的知识同步到 MEMORY.

**使用场景**: `memory`, `evolution`

**依赖**: `json`, `logging`, `datetime`, `pathlib`, `typing`

**函数**:
  - `load_knowledge_base()`
    说明: 加载知识库
  - `generate_memory_summary(entry)`
    说明: 生成记忆摘要

Args:
    entry: 知识库条目

Returns:
    格式化的摘要文本
  - `get_existing_sync_entries()`
    说明: 获取已同步的条目 ID
  - `sync_to_memory(max_entries)`
    说明: 同步知识到 MEMORY.md

Args:
    max_entries: 最大同步条目数

Returns:
    同步结果统计
  - `main()`
    说明: 主入口

---

<!-- MODULE:harness/evolve-daemon/proposer.py -->
### `harness/evolve-daemon/proposer.py`

**类型**: python
**路径**: `harness/evolve-daemon/proposer.py`
**一句话**: 提案生成器 — 调用 Claude API 进行深度分析，生成结构化改进提案。

**使用场景**: `memory`, `evolution`, `agent`

**依赖**: `json`, `logging`, `sys`, `pathlib`, `datetime`

**函数**:
  - `generate_proposal(analysis, config, root)`
    说明: 生成改进提案。调用 Claude API 进行深度分析。
底层使用 kb_shared.get_llm_config()，所有 LLM 调用路径统一。
  - `_call_claude_api(model, system_prompt, user_message, max_tokens, temperature)`
    说明: 调用 Claude API — 优先使用统一 SDK 客户端，降级为 REST API
  - `_generate_with_claude(analysis, config, root)`
    说明: 使用 Claude API 生成高质量提案
  - `_generate_from_template(analysis, config, root)`
    说明: 降级：使用模板生成提案（无需 API Key）
  - `_save_proposal(content, analysis, config, root)`
    说明: 保存提案文件
  - `_record_to_instinct(analysis, proposal_path, confidence, source, root)`
    说明: 将提案内容记录到 instinct-record.json
  - `mark_proposal_accepted(proposal_path, root)`
    说明: 人工 accept 提案后调用 — 升级 instinct confidence 至 0.9。
用法: python3 -c "from evolve_daem

---

<!-- MODULE:harness/evolve-daemon/rollback.py -->
### `harness/evolve-daemon/rollback.py`

**类型**: python
**路径**: `harness/evolve-daemon/rollback.py`
**一句话**: 自动回滚模块 — 观察期验证效果，自动回滚恶化的改动。

**使用场景**: `memory`, `evolution`, `agent`

**依赖**: `json`, `sys`, `datetime`, `pathlib`, `typing`

**函数**:
  - `load_proposal_history(history_file)`
    说明: 加载提案历史
  - `save_proposal_history(history_file, history)`
    说明: 保存提案历史
  - `collect_metrics(root, observation_days)`
  - `evaluate_proposal(proposal, metrics, baseline, config)`
    说明: 评估是否应该保留或回滚。

返回: (decision, triggers) — decision 是 "keep" | "rollback" | "obser
  - `check_circuit_breaker(history, config)`
    说明: 检查熔断器状态。

返回: (is_triggered, reason)
  - `execute_rollback(proposal, root, config)`
    说明: 执行回滚
  - `consolidate_proposal(proposal, root)`
    说明: 固化提案
  - `run_rollback_check(root, config)`
    说明: 检查所有提案，执行回滚或固化。

返回检查结果。
  - `get_proposal_health(proposal_id, root, config)`
    说明: 获取单个提案的健康状态
  - `_promote_instinct_on_observation(proposal, root)`
    说明: 观察期通过后：增强 instinct 置信度 + 关联 target_file。
同时更新知识库的置信度。
  - `_demote_instinct_on_rollback(proposal, root)`
    说明: 回滚成功后：降低 instinct 置信度 + 移除 target_file 关联。
与 _promote_instinct_on_observation 对称

---

<!-- MODULE:harness/evolve-daemon/rule_evolution.py -->
### `harness/evolve-daemon/rule_evolution.py`

**类型**: python
**路径**: `harness/evolve-daemon/rule_evolution.py`
**一句话**: Rule 维度进化策略

**使用场景**: `evolution`

**依赖**: `json`, `datetime`, `pathlib`

**函数**:
  - `evolve_rule(target, corrections, config, root)`
  - `_generate_rule_change(rule_name, corrections)`

---

<!-- MODULE:harness/evolve-daemon/scheduler.py -->
### `harness/evolve-daemon/scheduler.py`

**类型**: python
**路径**: `harness/evolve-daemon/scheduler.py`
**一句话**: 内置定时任务调度器 — 基于 APScheduler 实现异步定时触发。

**使用场景**: `evolution`, `hook`

**依赖**: `argparse`, `json`, `logging`, `os`, `signal`

**类**:
  - `SchedulerManager`
    方法: `__new__()`, `__init__()`, `load_config()`, `is_available()`, `is_running()`, `get_data_dir()`, `start()`, `_heartbeat_check()`

**函数**:
  - `parse_interval(interval_str)`
    说明: 解析间隔字符串，返回秒数。

支持格式：
  - "30 seconds" / "30 s"
  - "30 minutes" / "30 m"
  - "2 
  - `run_evolution_cycle()`
    说明: 执行一次完整的进化周期
  - `get_last_evolution_time(data_dir)`
    说明: 获取上次进化的时间
  - `check_heartbeat(config, data_dir)`
    说明: 心跳检测：检查是否需要触发进化

返回：
    {
        "healthy": True/False,
        "reason": str,
  - `main()`

---

<!-- MODULE:harness/evolve-daemon/skill_evolution.py -->
### `harness/evolve-daemon/skill_evolution.py`

**类型**: python
**路径**: `harness/evolve-daemon/skill_evolution.py`
**一句话**: Skill 维度进化策略

**使用场景**: `skill`, `evolution`

**依赖**: `json`, `datetime`, `pathlib`

**函数**:
  - `evolve_skill(target, corrections, config, root)`
  - `_generate_skill_change(skill_name, corrections)`

---

<!-- MODULE:harness/evolve-daemon/update_notifier.py -->
### `harness/evolve-daemon/update_notifier.py`

**类型**: python
**路径**: `harness/evolve-daemon/update_notifier.py`
**一句话**: CHK 插件更新通知器 - 管理更新通知状态，避免重复提示

**使用场景**: `evolution`

**依赖**: `json`, `logging`, `sys`, `dataclasses`, `datetime`

**类**:
  - `UpdateState`
  - `UpdateNotifier`
    方法: `__init__()`, `_get_data_dir()`, `_get_state_file()`, `_load_state()`, `_save_state()`, `should_notify()`, `mark_notified()`, `get_state()`

**函数**:
  - `get_notifier()`
    说明: 获取全局通知器实例
  - `format_update_notification(local, remote, release_url)`
    说明: 格式化更新通知消息

格式参考 Claude Code 升级提示风格：

╔══════════════════════════════════════════
  - `run_update_check()`
    说明: 执行完整的更新检查流程

Returns:
    更新通知消息（如果有更新且应该通知），否则返回空字符串
  - `main()`
    说明: 主入口

---

<!-- MODULE:harness/evolve-daemon/validator.py -->
### `harness/evolve-daemon/validator.py`

**类型**: python
**路径**: `harness/evolve-daemon/validator.py`
**一句话**: 数据验证器 — 验证 sessions.jsonl 格式，隔离异常数据。

**使用场景**: `evolution`, `error`

**依赖**: `json`, `logging`, `sys`, `datetime`, `pathlib`

**函数**:
  - `validate_session(session)`
    说明: 验证单个 session 的格式。

返回: (is_valid, error_message)
  - `validate_sessions_file(sessions_file, quarantine_dir)`
    说明: 验证 sessions.jsonl 文件。

返回:
{
    "total": 100,
    "valid": 98,
    "invalid": 2
  - `clean_old_sessions(sessions_file, max_age_days)`
    说明: 清理超过指定天数的 session。

返回清理统计。
  - `get_data_quality_stats(sessions_file)`
    说明: 统计数据质量。

返回:
{
    "total_sessions": 100,
    "sessions_with_agents": 80,
    "s
  - `run_validation(root, config)`
    说明: 运行完整验证流程。

---

<!-- MODULE:harness/knowledge/doc_generator.py -->
### `harness/knowledge/doc_generator.py`

**类型**: python
**路径**: `harness/knowledge/doc_generator.py`
**一句话**: doc-generator.

**使用场景**: `agent`, `error`

**依赖**: `argparse`, `json`, `os`, `re`, `shutil`

**类**:
  - `DocMetadata`

**函数**:
  - `_log_error(phase, error_msg, file_path, recoverable)`
    说明: 记录错误到 error.jsonl（复用现有系统）
  - `_escape_html(text)`
    说明: HTML 转义
  - `is_separator_row(cells)`
    说明: 检测表格分隔行（|---|:| 格式）
  - `_parse_markdown(md_content)`
    说明: Markdown 转 HTML（基础实现）
  - `_get_default_template()`
    说明: 默认 HTML 模板
  - `convert(md_file, doc_type, output_dir, metadata, add_timestamp)`
    说明: 将 Markdown 文件转换为 HTML

Args:
    md_file: Markdown 文件路径
    doc_type: 文档类型
    o
  - `batch_convert(md_files, output_dir, doc_type)`
    说明: 批量转换（并行处理）
  - `session_wrap(session_id, agents, output_dir, docs)`
    说明: 生成会话总结 HTML

Args:
    session_id: 会话 ID
    agents: 使用的 Agent 列表
    output_dir
  - `archive_document(source, doc_type)`
    说明: 归档文档到按月组织的目录

Args:
    source: 源文件路径
    doc_type: 文档类型

Returns:
    归档后的文件路径
  - `async_archive(source, doc_type)`
    说明: 异步归档，不阻塞主流程
  - `main()`

---

<!-- MODULE:harness/knowledge/knowledge_recommender.py -->
### `harness/knowledge/knowledge_recommender.py`

**类型**: python
**路径**: `harness/knowledge/knowledge_recommender.py`
**一句话**: Knowledge Recommender Engine — 知识推荐引擎

**使用场景**: `memory`, `agent`, `skill`

**依赖**: `hashlib`, `json`, `math`, `re`, `sys`

**函数**:
  - `load_evolved_knowledge()`
    说明: 加载进化知识库 (JSONL 格式)
  - `load_knowledge_base()`
    说明: 加载所有知识条目（双知识库合并）

知识库 1: harness/knowledge/ — 手工维护的专家知识
知识库 2: harness/knowledge
  - `load_instinct_usage()`
    说明: 从 instinct 数据读取历史使用频率
  - `extract_keywords(text)`
    说明: 从文本中提取关键词（过滤停用词）
  - `compute_score(entry, keywords, usage_weight)`
    说明: 计算单条知识的推荐分数
  - `filter_lifecycle(entries, allow_draft)`
    说明: 过滤掉 lifecycle 为 draft 的条目（除非显式允许）
  - `recommend(entries, keywords, target_types, usage_weight, top_n)`
    说明: 通用推荐：按关键词 + 类型过滤 + 排序
  - `_preview_content(content)`
    说明: 生成内容摘要（取前 120 字符）
  - `recommend_by_task(task)`
    说明: 基于任务描述推荐知识
  - `recommend_by_skill(skill_name)`
    说明: 基于当前 Skill 推荐相关知识
  - `recommend_by_failure(failure_text)`
    说明: 基于错误/失败模式推荐 pitfall 知识
  - `recommend_by_agent(agent_type)`
    说明: 基于当前 Agent 类型推荐相关指导
  - `generate_recommendations(task, skill, agent, failure)`
    说明: 聚合所有场景的推荐，生成完整推荐报告
  - `save_recommendations(data)`
    说明: 保存推荐结果到 JSON 文件
  - `format_as_context(recs, title)`
    说明: 将推荐结果格式化为可注入上下文的 Markdown
  - `cmd_recommend(args)`
    说明: recommend 子命令
  - `cmd_inject()`
    说明: inject 子命令 — 输出推荐上下文（供 SessionStart Hook 调用）。
读取上次推荐结果，格式化为 Markdown 注入。
  - `cmd_status()`
    说明: status 子命令 — 输出推荐引擎状态
  - `main()`

---

<!-- MODULE:harness/knowledge/lifecycle.py -->
### `harness/knowledge/lifecycle.py`

**类型**: python
**路径**: `harness/knowledge/lifecycle.py`
**一句话**: Knowledge Lifecycle Engine — 知识生命周期可执行引擎。

**使用场景**: `version`, `path`, `agent`

**依赖**: `json`, `sys`, `datetime`, `pathlib`

**函数**:
  - `load_lifecycle_config()`
    说明: 加载 lifecycle.yaml 配置，失败则使用内联默认值
  - `check_maturity_promotion(entry, config)`
    说明: 检查条目是否可以升级。
返回: "verified" | "proven" | None
  - `apply_decay(entry, config)`
    说明: 检查条目是否应该衰减降级。
返回: 目标成熟度 | None（无需降级）
  - `promote_to_layer1(entry, knowledge_dir, config)`
    说明: 跨项目提升：L3 → L1/L2。
生成提升提案到 proposals/ 目录。
返回: 提案文件路径 | None
  - `cmd_check(knowledge_file)`
    说明: 检查单条知识的成熟度和衰减状态
  - `cmd_decay(knowledge_dir, dry_run)`
    说明: 扫描目录下所有知识文件，执行衰减检查

Args:
    knowledge_dir: 知识目录路径
    dry_run: 为 True 时仅预览不写入
  - `cmd_promote(knowledge_dir)`
    说明: 检查跨项目提升机会
  - `main()`

---

<!-- MODULE:harness/paths.py -->
### `harness/paths.py`

**类型**: python
**路径**: `harness/paths.py`
**一句话**: paths.

**使用场景**: `memory`, `agent`, `config`

**依赖**: `os`, `pathlib`

**函数**:
  - `_project_root()`
  - `_plugin_root()`
  - `sessions_file()`
  - `errors_file()`
  - `errors_lock_file()`
  - `failures_file()`
  - `agent_calls_file()`
  - `skill_calls_file()`
  - `analysis_state_file()`
  - `proposal_history_file()`
  - `observations_file()`
  - `obs_errors_file()`
  - `validate_paths(project_root)`
    说明: 验证 CHK 系统关键路径是否存在，启动时健康检查。

检查 8 个关键目录和 3 个关键数据文件，返回详细诊断结果。
适用于：CI 检查、启动自检、调试路径问
  - `warn_missing_paths(project_root)`
    说明: 返回缺失路径的警告信息列表，轻量级健康检查。

参数:
    project_root: 项目根目录，默认使用 ROOT

返回:
    list: 警告字
  - `find_root(start)`
    说明: 向上查找包含 .claude 目录的项目根目录。

优先级:
  1. 环境变量 CLAUDE_PROJECT_DIR
  2. start 目录向上遍历
  
  - `setup_syspath(root)`
    说明: 统一设置 sys.path，确保 harness 包可导入。

在所有入口点（CLI、Hook 脚本、测试）的最顶部调用此函数，
替代分散的 sys.path.

---

<!-- MODULE:harness/tests/check_directory_and_safety.py -->
### `harness/tests/check_directory_and_safety.py`

**类型**: python
**路径**: `harness/tests/check_directory_and_safety.py`
**一句话**: 目录结构与安全全面测试套件

**使用场景**: `memory`, `agent`, `cli`

**依赖**: `json`, `os`, `sys`, `tempfile`, `pathlib`

**函数**:
  - `ok(msg)`
  - `fail(msg)`
  - `test_harness_whitelist_subdirs()`
    说明: 正向: harness/ 下只允许白名单子目录
  - `test_no_harness_nested()`
    说明: 安全: harness/ 下禁止嵌套另一个 harness/
  - `test_no_code_in_claude_dir()`
    说明: 安全: .claude/ 下只允许 data/ 和 proposals/
  - `test_claude_data_subdirs()`
    说明: 边界: .claude/data/ 只允许已知文件
  - `test_path_constants_no_instinct()`
    说明: 反向: paths.py 不再导出 instinct 路径常量
  - `test_instinct_in_memory()`
    说明: 正向: instinct-record.json 在 memory/ 目录
  - `test_knowledge_dirs_exist()`
    说明: 正向: 知识库子目录都存在（evolved 由运行时自动创建，测试时确保有基础目录）
  - `test_knowledge_json_schema()`
    说明: 边界: 知识 JSON 文件有正确的 frontmatter
  - `test_knowledge_manual_symlink_gone()`
    说明: 反向: knowledge/manual 符号链接已删除
  - `test_all_hook_scripts_exist()`
    说明: 正向: hooks.json 引用的脚本都存在
  - `test_underscore_naming_collect_hooks()`
    说明: 边界: collect_*.py hook 脚本统一 underscore 命名（migration 规范）
  - `test_path_traversal_protection()`
    说明: 安全: 路径常量计算应防止 ../ 遍历
  - `test_collect_error_sanitization()`
    说明: 安全: collect_error.py 正确脱敏敏感信息
  - `test_collect_error_no_secret_in_error()`
    说明: 安全: 错误收集不泄露敏感信息
  - `test_corrupted_jsonl_handled()`
    说明: 异常: 损坏的 JSONL 文件不导致程序崩溃
  - `test_empty_knowledge_dir()`
    说明: 边界: 空的 knowledge 目录不导致崩溃
  - `test_instinct_record_schema()`
    说明: 正向: instinct-record.json schema 正确
  - `test_instinct_record_uuid_unique()`
    说明: 正向: instinct 记录 ID 唯一
  - `test_all_agents_have_frontmatter()`
    说明: 正向: 所有 Agent 文件有 frontmatter
  - `test_all_skills_have_frontmatter()`
    说明: 正向: 所有 Skill 文件有 frontmatter
  - `test_no_empty_subdirs()`
    说明: 边界: harness/ 下无空目录
  - `test_cli_gc_nonexistent_project()`
    说明: 异常: gc 对不存在的目录不崩溃
  - `test_knowledge_recommender_missing_evolved_dir()`
    说明: 边界: evolved/ 目录不存在时优雅降级

---

<!-- MODULE:harness/tests/graders/base.py -->
### `harness/tests/graders/base.py`

**类型**: python
**路径**: `harness/tests/graders/base.py`
**一句话**: LLM Grader 基类

**使用场景**: `skill`, `agent`, `error`

**依赖**: `json`, `abc`, `dataclasses`, `typing`, `os`

**类**:
  - `GradingResult`
  - `BaseGrader`
    方法: `__init__()`, `grade()`, `call_llm()`, `_fallback_grading()`, `parse_json_response()`
  - `CodeQualityGrader`
    方法: `grade()`
  - `OutputQualityGrader`
    方法: `grade()`
  - `BehaviorGrader`
    方法: `grade()`

---

<!-- MODULE:harness/tests/graders/pass_at_k.py -->
### `harness/tests/graders/pass_at_k.py`

**类型**: python
**路径**: `harness/tests/graders/pass_at_k.py`
**一句话**: Pass@k 指标计算

**使用场景**: `skill`

**依赖**: `math`, `json`, `typing`, `dataclasses`

**类**:
  - `PassAtKResult`
  - `EvaluationRunner`
    方法: `__init__()`, `run_round()`, `get_aggregate_results()`

**函数**:
  - `binomial(n, k)`
    说明: 计算二项式系数 C(n, k)
  - `calculate_pass_at_k(results, k_values)`
    说明: 计算 pass@k 指标

pass@k = E[1 - C(n-c, k) / C(n, k)]

其中:
- n = 总尝试次数
- c = 通过次数
- 
  - `calculate_confidence_interval(results, confidence, n_bootstrap)`
    说明: 计算 pass@k 的置信区间 (使用 bootstrap)

Args:
    results: 测试结果列表
    confidence: 置信度 (默
  - `main()`
    说明: 命令行入口

---

<!-- MODULE:hooks/bin/agent-planning-check.sh -->
### `hooks/bin/agent-planning-check.sh`

**类型**: shell
**路径**: `hooks/bin/agent-planning-check.sh`
**一句话**: !/bin/bash Agent Planning Check - PreAgentCall Hook 验证多 Agent 任务分配合理性 获取插件根目录 主逻辑

**使用场景**: `path`, `agent`, `hook`

**函数**:
  - `log()`
  - `main()`

---

<!-- MODULE:hooks/bin/agent-result-sync.sh -->
### `hooks/bin/agent-result-sync.sh`

**类型**: shell
**路径**: `hooks/bin/agent-result-sync.sh`
**一句话**: !/bin/bash Agent Result Sync - PostAgentCall Hook 同步 Agent 执行结果到 mailbox 获取插件根目录 主逻辑

**使用场景**: `path`, `agent`, `hook`

**函数**:
  - `log()`
  - `main()`

---

<!-- MODULE:hooks/bin/architecture-verify.sh -->
### `hooks/bin/architecture-verify.sh`

**类型**: shell
**路径**: `hooks/bin/architecture-verify.sh`
**一句话**: !/bin/bash architecture-verify.sh - 架构决策步骤验证 检查是否涉及架构相关关键词 检查是否有决策记录目录 如果涉及架构但没有决策文件，提示警告

**使用场景**: `path`, `hook`, `error`

---

<!-- MODULE:hooks/bin/check-update.sh -->
### `hooks/bin/check-update.sh`

**类型**: shell
**路径**: `hooks/bin/check-update.sh`
**一句话**: !/bin/bash ============================================================ CHK 插件更新检查钩子 - UserPromptSub

**使用场景**: `path`, `version`, `hook`

**函数**:
  - `log_info()`
  - `should_check()`
  - `get_local_version()`
  - `get_remote_version()`
  - `version_lt()`
  - `show_update_notification()`
  - `main()`

---

<!-- MODULE:hooks/bin/checkpoint-auto-save.sh -->
### `hooks/bin/checkpoint-auto-save.sh`

**类型**: shell
**路径**: `hooks/bin/checkpoint-auto-save.sh`
**一句话**: !/bin/bash checkpoint-auto-save.sh — PreToolUse Hook: 检测 /compact 并自动保存 checkpoint 设计：永远 exit 0，chec

**使用场景**: `hook`

---

<!-- MODULE:hooks/bin/checkpoint-verify.sh -->
### `hooks/bin/checkpoint-verify.sh`

**类型**: shell
**路径**: `hooks/bin/checkpoint-verify.sh`
**一句话**: !/bin/bash checkpoint-verify.sh - 验证 Checkpoint 文件是否完整 检查备份目录是否存在 关键文件列表

**使用场景**: `path`, `hook`, `error`

---

<!-- MODULE:hooks/bin/coverage-check.sh -->
### `hooks/bin/coverage-check.sh`

**类型**: shell
**路径**: `hooks/bin/coverage-check.sh`
**一句话**: !/bin/bash coverage-check.sh — 测试覆盖率门禁 当测试覆盖率低于阈值时阻断提交 支持多种覆盖率报告格式 pytest-cov XML

**使用场景**: `hook`

**函数**:
  - `find_coverage_report()`
  - `check_coverage()`

---

<!-- MODULE:hooks/bin/doc-verify.sh -->
### `hooks/bin/doc-verify.sh`

**类型**: shell
**路径**: `hooks/bin/doc-verify.sh`
**一句话**: !/usr/bin/env bash doc-verify.sh - 文档验证器 Shell 包装器 用于 Claude Code hook，自动检测插件根目录 自动检测插件根目录 优先级 1: 环境

**使用场景**: `path`, `hook`, `error`

**函数**:
  - `detect_plugin_root()`

---

<!-- MODULE:hooks/bin/ensure-settings.sh -->
### `hooks/bin/ensure-settings.sh`

**类型**: shell
**路径**: `hooks/bin/ensure-settings.sh`
**一句话**: !/bin/bash ============================================================ CHK 项目配置保障钩子 - UserPromptSub

**使用场景**: `hook`, `config`

---

<!-- MODULE:hooks/bin/git-commit-check.sh -->
### `hooks/bin/git-commit-check.sh`

**类型**: shell
**路径**: `hooks/bin/git-commit-check.sh`
**一句话**: !/bin/bash git-commit-check.sh - 检查 Git 提交规范 从 general.md 提取有效类型 检查 git commit 命令 提取提交信息

**使用场景**: `hook`, `cli`

---

<!-- MODULE:hooks/bin/log-utils.sh -->
### `hooks/bin/log-utils.sh`

**类型**: shell
**路径**: `hooks/bin/log-utils.sh`
**一句话**: !/bin/bash ============================================================ CHK 共享日志工具 — 被其他 hook 脚本 sou

**使用场景**: `path`, `hook`, `error`

**函数**:
  - `_hook_log_init()`
  - `_hook_log_error()`
  - `_hook_log_warn()`
  - `_hook_log_info()`

---

<!-- MODULE:hooks/bin/memory-cleanup.sh -->
### `hooks/bin/memory-cleanup.sh`

**类型**: shell
**路径**: `hooks/bin/memory-cleanup.sh`
**一句话**: !/bin/bash ============================================================ CHK 会话状态清理脚本  功能： - 清理当前会话的状

**使用场景**: `memory`, `hook`, `cli`

**函数**:
  - `cleanup_current()`
  - `cleanup_all()`

---

<!-- MODULE:hooks/bin/memory-inject.sh -->
### `hooks/bin/memory-inject.sh`

**类型**: shell
**路径**: `hooks/bin/memory-inject.sh`
**一句话**: !/bin/bash ============================================================ CHK 记忆注入钩子 - UserPromptSubmi

**使用场景**: `memory`, `hook`

**函数**:
  - `log()`
  - `is_L0_injected()`
  - `mark_L0_injected()`
  - `read_memory_index()`
  - `read_high_confidence_instincts()`
  - `match_keywords()`
  - `inject_capability_registry()`
  - `main()`
  - `cleanup()`
  - `show_help()`

---

<!-- MODULE:hooks/bin/notify.sh -->
### `hooks/bin/notify.sh`

**类型**: shell
**路径**: `hooks/bin/notify.sh`
**一句话**: !/bin/bash notify.sh - 飞书 Webhook 通知脚本 用法: ./notify.sh <type> <message> [title] 示例: ./notify.sh succ

**使用场景**: `hook`, `config`, `cli`

**函数**:
  - `log_info()`
  - `log_error()`
  - `log_warn()`
  - `send_feishu_message()`
  - `main()`

---

<!-- MODULE:hooks/bin/observe.sh -->
### `hooks/bin/observe.sh`

**类型**: shell
**路径**: `hooks/bin/observe.sh`
**一句话**: !/bin/bash observe.sh — Hook 观测事件采集器（shell wrapper） 职责：调用 observe.py，永远 exit 0，零阻塞主流程  设计原则： 1. 永远 e

**使用场景**: `path`, `hook`, `error`

---

<!-- MODULE:hooks/bin/quality-gate.sh -->
### `hooks/bin/quality-gate.sh`

**类型**: shell
**路径**: `hooks/bin/quality-gate.sh`
**一句话**: !/bin/bash quality-gate.sh — PostToolUse Hook: 验证代码和配置文件格式 设计：永远 exit 0，格式错误警告但不阻断 加载共享日志工具

**使用场景**: `hook`, `config`, `error`

**函数**:
  - `block_post()`
  - `_is_impl_file()`
  - `_scan_secrets()`
  - `_check_test_missing()`

---

<!-- MODULE:hooks/bin/rate-limiter.sh -->
### `hooks/bin/rate-limiter.sh`

**类型**: shell
**路径**: `hooks/bin/rate-limiter.sh`
**一句话**: !/bin/bash rate-limiter.sh — Claude Code API Rate Limiter (Sliding Window) 设计：永远 exit 0，rate limit 超

**使用场景**: `hook`

**函数**:
  - `log_warn()`
  - `is_valid_json()`
  - `load_state()`
  - `save_state()`
  - `clean_old()`
  - `count_from_state()`
  - `build_new_state()`

---

<!-- MODULE:hooks/bin/safety-check.sh -->
### `hooks/bin/safety-check.sh`

**类型**: shell
**路径**: `hooks/bin/safety-check.sh`
**一句话**: !/bin/bash safety-check.sh — PreToolUse Hook: 阻止危险 Bash 命令 设计：永远 exit 0（Hook 失败不阻断工具调用），危险命令通过 hookS

**使用场景**: `hook`, `cli`

**函数**:
  - `block()`

---

<!-- MODULE:hooks/bin/security-auto-trigger.sh -->
### `hooks/bin/security-auto-trigger.sh`

**类型**: shell
**路径**: `hooks/bin/security-auto-trigger.sh`
**一句话**: !/bin/bash security-auto-trigger.sh — PostToolUse Hook: 敏感文件修改时自动触发安全审查提示 设计：永远 exit 0，提示不阻断

**使用场景**: `hook`

---

<!-- MODULE:hooks/bin/tdd-check.sh -->
### `hooks/bin/tdd-check.sh`

**类型**: shell
**路径**: `hooks/bin/tdd-check.sh`
**一句话**: !/bin/bash tdd-check.sh — PreToolUse Hook: TDD 阻断检查，实现文件写入前必须存在对应测试文件 设计：永远 exit 0（Hook 失败不阻断），TDD 违

**使用场景**: `hook`

**函数**:
  - `_is_impl()`
  - `block()`

---

<!-- MODULE:hooks/bin/update-registry-on-commit.sh -->
### `hooks/bin/update-registry-on-commit.sh`

**类型**: shell
**路径**: `hooks/bin/update-registry-on-commit.sh`
**一句话**: !/bin/bash ============================================================ Git Hook: 增量更新 Capability Re

**使用场景**: `hook`, `cli`

**函数**:
  - `check_code_changes()`
  - `get_changed_files()`
  - `needs_full_update()`
  - `update_registry()`
  - `show_help()`
  - `main()`

---

<!-- MODULE:hooks/bin/update-registry.sh -->
### `hooks/bin/update-registry.sh`

**类型**: shell
**路径**: `hooks/bin/update-registry.sh`
**一句话**: !/bin/bash ============================================================ 更新 Capability Registry  用法： 

**使用场景**: `path`, `hook`

---

<!-- MODULE:index.js -->
### `index.js`

**类型**: javascript
**路径**: `index.js`
**一句话**: 

**函数**:
  - `ensureBypassPermissions()`
  - `ensureProjectPermissions()`
  - `getVersion()`
  - `loadAgents()`
  - `loadSkills()`
  - `loadRules()`
  - `loadCommands()`
  - `getPluginInfo()`

---

## 搜索索引

> 用于按需加载匹配

- **harness/_core/bump_version.py**: bump core version.py version harness
- **harness/_core/cache_manager.py**: memory CacheEntry manager.py core CacheManager cache CacheStats evolution harness
- **harness/_core/config_loader.py**: config cli core ConfigLoader evolution loader.py harness
- **harness/_core/exceptions.py**: error core exceptions.py harness
- **harness/_core/instinct_engine.py**: memory agent engine.py skill core instinct InstinctEngine harness
- **harness/_core/instinct_reader.py**: memory core instinct reader.py Instinct harness
- **harness/_core/instinct_state.py**: memory state.py core instinct SessionState harness
- **harness/_core/keyword_matcher.py**: memory matcher.py core keyword harness
- **harness/_core/path_guard.py**: config core path PathGuard hook guard.py harness
- **harness/_core/update_checker.py**: checker.py core update UpdateInfo version harness
- **harness/_core/version.py**: version.py version core harness
- **harness/cli/capability-analyzer.py**: cli skill capability-analyzer.py SemanticAnalyzer harness
- **harness/cli/gc.py**: agent cli gc.py path harness
- **harness/cli/generate_skill_index.py**: cli skill generate index.py harness
- **harness/cli/init.py**: config cli path version init.py harness
- **harness/cli/instinct_cli.py**: memory version cli.py cli instinct evolution harness
- **harness/cli/migrate.py**: migrate.py agent cli harness
- **harness/cli/mode.py**: agent config cli mode.py hook harness
- **harness/cli/scan.py**: path scan.py cli harness
- **harness/cli/status.py**: status.py memory config cli hook harness
- **harness/cli/sync.py**: config cli sync.py harness
- **harness/evolve-daemon/agent_evolution.py**: agent evolution.py evolve-daemon evolution harness
- **harness/evolve-daemon/analyzer.py**: agent skill evolve-daemon evolution analyzer.py harness
- **harness/evolve-daemon/apply_change.py**: memory change.py apply evolve-daemon evolution harness
- **harness/evolve-daemon/daemon.py**: memory daemon.py agent config evolve-daemon harness
- **harness/evolve-daemon/effect_tracker.py**: tracker.py memory agent skill EffectTracker effect evolve-daemon harness
- **harness/evolve-daemon/evolve_dispatcher.py**: memory skill dispatcher.py evolve evolve-daemon evolution harness
- **harness/evolve-daemon/extract_semantics.py**: memory extract evolve-daemon harness evolution hook semantics.py
- **harness/evolve-daemon/generalize.py**: generalize.py error evolve-daemon evolution harness
- **harness/evolve-daemon/instinct_updater.py**: memory error instinct evolve-daemon evolution updater.py harness
- **harness/evolve-daemon/integrated_evolution.py**: config integrated evolution.py evolve-daemon evolution hook harness
- **harness/evolve-daemon/kb_shared.py**: memory config cli kb shared.py evolve-daemon harness
- **harness/evolve-daemon/llm_decision.py**: memory config evolve-daemon decision.py evolution llm harness
- **harness/evolve-daemon/memory_sync.py**: memory sync.py evolve-daemon evolution harness
- **harness/evolve-daemon/proposer.py**: memory agent proposer.py evolve-daemon evolution harness
- **harness/evolve-daemon/rollback.py**: memory rollback.py agent evolve-daemon evolution harness
- **harness/evolve-daemon/rule_evolution.py**: rule evolution.py evolve-daemon evolution harness
- **harness/evolve-daemon/scheduler.py**: scheduler.py SchedulerManager evolve-daemon evolution hook harness
- **harness/evolve-daemon/skill_evolution.py**: skill evolution.py evolve-daemon evolution harness
- **harness/evolve-daemon/update_notifier.py**: notifier.py update UpdateNotifier evolve-daemon evolution UpdateState harness
- **harness/evolve-daemon/validator.py**: error validator.py evolve-daemon evolution harness
- **harness/knowledge/doc_generator.py**: agent generator.py DocMetadata error doc knowledge harness
- **harness/knowledge/knowledge_recommender.py**: memory agent skill knowledge recommender.py harness
- **harness/knowledge/lifecycle.py**: lifecycle.py agent path version knowledge harness
- **harness/paths.py**: memory agent config harness paths.py
- **harness/tests/check_directory_and_safety.py**: and memory agent cli directory tests check safety.py harness
- **harness/tests/graders/base.py**: base.py GradingResult agent skill tests graders BaseGrader error CodeQualityGrader BehaviorGrader OutputQualityGrader harness
- **harness/tests/graders/pass_at_k.py**: pass at skill tests graders k.py EvaluationRunner PassAtKResult harness
- **hooks/bin/agent-planning-check.sh**: agent agent-planning-check.sh bin hooks hook path
- **hooks/bin/agent-result-sync.sh**: agent agent-result-sync.sh bin hooks hook path
- **hooks/bin/architecture-verify.sh**: architecture-verify.sh error bin hooks hook path
- **hooks/bin/check-update.sh**: bin hooks version hook path check-update.sh
- **hooks/bin/checkpoint-auto-save.sh**: bin hooks hook checkpoint-auto-save.sh
- **hooks/bin/checkpoint-verify.sh**: checkpoint-verify.sh error bin hooks hook path
- **hooks/bin/coverage-check.sh**: bin hooks hook coverage-check.sh
- **hooks/bin/doc-verify.sh**: error doc-verify.sh bin hooks hook path
- **hooks/bin/ensure-settings.sh**: config ensure-settings.sh bin hooks hook
- **hooks/bin/git-commit-check.sh**: cli bin hooks hook git-commit-check.sh
- **hooks/bin/log-utils.sh**: log-utils.sh error bin hooks hook path
- **hooks/bin/memory-cleanup.sh**: memory memory-cleanup.sh cli bin hooks hook
- **hooks/bin/memory-inject.sh**: memory memory-inject.sh bin hooks hook
- **hooks/bin/notify.sh**: config cli notify.sh bin hooks hook
- **hooks/bin/observe.sh**: error observe.sh bin hooks hook path
- **hooks/bin/quality-gate.sh**: config quality-gate.sh error bin hooks hook
- **hooks/bin/rate-limiter.sh**: bin hooks rate-limiter.sh hook
- **hooks/bin/safety-check.sh**: cli safety-check.sh bin hooks hook
- **hooks/bin/security-auto-trigger.sh**: bin hooks hook security-auto-trigger.sh
- **hooks/bin/tdd-check.sh**: bin hooks tdd-check.sh hook
- **hooks/bin/update-registry-on-commit.sh**: cli bin hooks update-registry-on-commit.sh hook
- **hooks/bin/update-registry.sh**: update-registry.sh bin hooks hook path
- **index.js**: index.js