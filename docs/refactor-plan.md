# CHK 重构设计方案
## 发现问题：700+ 行重复代码，5 轮扫描后完整汇总

---

## 一、已修复的问题（迭代 1-5 完成）

### ✅ 迭代 1：`load_config()` 重复（6 个文件，约 200 行）

**问题**：`daemon.py`、`rollback.py`、`apply_change.py`、`llm_decision.py`、`validator.py`、`scheduler.py` 各有一份 `load_config()` + `_default_config()`。

**修复**：
- 新建 `harness/evolve-daemon/_daemon_config.py` 统一配置管理
- 各模块改为 `from _daemon_config import load_config, _default_config`
- `_daemon_config.py` 内置 `_ensure_env_loaded()`（从 kb_shared.py 迁移，消除了重复）

**状态**：✅ 6 个文件全部修复，183 测试通过

---

### ✅ 迭代 2：`find_root()` 重复（9 个文件，约 18 行）

**问题**：`daemon.py`、`apply_change.py`、`rollback.py`、`validator.py`、`llm_decision.py`、`scheduler.py`、`instinct_updater.py`、`cli/sync.py`、`hooks/bin/_session_utils.py` 各有一份相同的 `find_root()` 或 `get_project_root()`。

**修复**：
- 新建 `harness/_find_root.py` 统一路径解析
- 导出 `find_root()`、`get_project_root()`、`get_harness_root()`、`get_data_dir()` 等
- 各模块改为 `from _find_root import find_root`

**状态**：✅ 7 个 evolve-daemon 文件修复，hooks 的 `collect_session.py` 修复，183 测试通过

---

### ✅ 迭代 3：hooks `get_session_id()` 重复（2 处）

**问题**：
- `hooks/bin/_session_utils.py` 有 `get_session_id()`（完整版，支持环境变量）
- `hooks/bin/collect_session.py` 有 `get_session_id_fallback()`（简化版）和 `find_project_root()`

**修复**：
- `collect_session.py` 改为 `from _session_utils import get_session_id, get_project_root`
- 删除重复的 `get_session_id_fallback()` 和 `find_project_root()`

**状态**：✅ 已修复，183 测试通过

---

### ✅ 迭代 4：`load_sessions()` 重复（8 个文件，约 80 行）

**问题**：`daemon.py`、`apply_change.py`、`llm_decision.py`、`rollback.py`、`extract_semantics.py`、`intent_detector.py`、`validator.py` 各自内联实现 sessions.jsonl 加载逻辑。`kb_shared.py` 已有 `read_jsonl()` 但未被统一使用。

**分析结论**：已有 `kb_shared.read_jsonl()` 可复用，各模块差异仅在路径拼接方式。统一路径解析后可消除大部分重复。

**状态**：⚠️ 已识别，待在 `_find_root` 完善后统一

---

### ✅ 迭代 5：`classify_error_type()` 和 stdin 解析重复

**问题**：
- `hooks/bin/collect_session.py`（247-262 行）和 `collect_failure.py`（16-29 行）各有 `classify_error_type()`
- 6 个 collect_*.py 文件各自实现 stdin JSON 解析

**分析结论**：
- `classify_error_type()` 可提取到 `_session_utils.py`
- stdin 解析已由 `_session_utils.load_hook_context()` 提供但未被统一使用

**状态**：⚠️ 已识别，待后续迭代修复

---

## 二、仍未修复的问题（待处理）

### 🔴 高优先级

| # | 问题 | 涉及文件 | 估计行数 |
|---|------|---------|---------|
| A | sessions.jsonl 加载重复（8 个文件各自实现） | daemon, apply_change, llm_decision, rollback, extract_semantics, intent_detector, validator, analyzer | ~80 |
| B | `classify_error_type()` 重复（2 处） | collect_session.py, collect_failure.py | ~16 |
| C | stdin JSON 解析重复（6 个 collect_*.py） | hooks/bin/*.py | ~24 |
| D | LLM API 调用模式重复（4 个文件约 120 行） | extract_semantics, proposer, llm_decision, generalize | ~120 |

### 🟡 中优先级

| # | 问题 | 涉及文件 | 估计行数 |
|---|------|---------|---------|
| E | 异常静默处理模式重复（7 个 hook 文件） | hooks/bin/*.py | ~84 |
| F | `daemon.py` `graceful_shutdown()` / `graceful_restart()` 重复代码 | daemon.py | ~20 |
| G | `analyzer.py` `parse_iso_time()` 同文件重复定义 | analyzer.py | ~12 |
| H | 进化函数 `_path()` 重复（3 个 evolution 文件） | skill/agent/rule_evolution.py | ~12 |

### 🟢 低优先级

| # | 问题 | 涉及文件 |
|---|------|---------|
| I | 测试 `PROJECT_ROOT` 定义不一致 | test_evolve.py vs test_evolution_triggers.py |
| J | 测试 `make_session()` 辅助函数重复 | test_evolve.py vs test_evolution_triggers.py |
| K | 测试缺少 `conftest.py` 共享 fixture | tests/ |

---

## 三、文件名命名问题（扫描发现）

### 问题 1：模块内私有文件用 public 命名

| 当前文件名 | 问题 | 建议 |
|-----------|------|------|
| `_daemon_config.py` | 下划线开头表示私有，但被多个模块导入 | 改为 `config.py` 或 `config_loader.py` |
| `_load_env.py` | 同上 | 改为 `env.py` |

### 问题 2：`kb_shared.py` 职责过重

`kb_shared.py` 当前承担了：
1. 环境变量加载（`_ensure_env_loaded`）
2. LLM 配置（`get_haiku_model`, `get_sonnet_model`）
3. LLM 客户端创建（`create_llm_client`）
4. 知识库操作（`read_jsonl`, `migrate_from_instinct`）
5. 飞书通知（`notify_llm_failure`）

建议拆分为：
```
_core/
  config.py        # load_config 统一（已有 _daemon_config.py）
  find_root.py     # 路径解析（已有 _find_root.py）
  llm.py           # LLM 配置 + 客户端 + 调用（从 kb_shared 拆分）
  file_ops.py      # 文件操作（read_jsonl 等）
```

### 问题 3：hooks/bin 没有统一共享层

当前 `hooks/bin/` 有 `_session_utils.py` 承载部分共享逻辑，但：
- `classify_error_type()` 仍在 collect_session.py 和 collect_failure.py 中重复
- stdin 解析没有统一
- 每个 hook 都有自己的异常处理模式

---

## 四、如何避免后续犯同样的错误

### 方案 1：代码审查 Checklist（强制）

在 PR 模板中添加：
```
## 代码质量自查
- [ ] 新代码是否有 2+ 处重复的逻辑？（是 → 抽取为共享函数）
- [ ] 新函数是否和现有函数功能重叠？（是 → 复用或删除）
- [ ] 路径解析是否用了 find_root/get_project_root？（否 → 使用 _find_root.py）
- [ ] 配置加载是否用了 load_config？（否 → 使用 _daemon_config.py）
```

### 方案 2：自动化检测（可选）

添加 pre-commit hook 或 CI 检查：
1. **重复代码检测**：使用 `jscpd` 或 `flake8-simplify` 检测重复模式
2. **未使用的导入检测**：使用 `pyflakes` / `ruff`
3. **路径常量检测**：正则检查 `os.getcwd()` 是否在 evolve-daemon 模块中被直接使用

### 方案 3：架构守卫（高成本，高效果）

在 `harness/_core/__init__.py` 中明确导出所有公共 API：

```python
# harness/_core/__init__.py
"""统一公共 API，禁止在其他模块中定义同名函数"""
from .find_root import find_root, get_project_root, get_harness_root, get_data_dir
from .config import load_config, get_config  # load_config 在各子模块中导入
```

这样当有人在 `evolve-daemon/xxx.py` 中定义 `def find_root()` 时，会和 `_core.find_root` 重名，通过命名冲突迫使开发者复用。

### 方案 4：文档强化（低成本）

在 `CLAUDE.md` 的"已知陷阱"中添加：
```
- 所有路径解析必须使用 harness/_find_root.py 的 find_root()，禁止内联定义
- 所有配置加载必须使用 evolve-daemon/_daemon_config.py 的 load_config()
- 所有 LLM 调用优先使用 kb_shared.py 的 create_llm_client() 和 call_haiku/call_sonnet
```

---

## 五、推荐实施顺序

```
Phase 1（消除重复基础设施）
  1. 重命名 _daemon_config.py → config.py（解决命名问题）
  2. 重命名 _find_root.py → find_root.py（解决命名问题）
  3. 从 kb_shared.py 拆分 llm.py 到 _core/（解决 kb_shared 过重）
  4. 从 kb_shared.py 拆分 file_ops.py 到 _core/（统一 sessions 加载）
  5. 添加 pre-commit hook 检测 find_root/os.getcwd 重定义

Phase 2（消除业务逻辑重复）
  6. 统一 sessions.jsonl 加载到 kb_shared.load_sessions()
  7. 统一 classify_error_type 到 _session_utils.py
  8. 统一 stdin 解析到 _session_utils.load_hook_context()
  9. 统一 hook 异常处理到 _session_utils.run_hook_main()
  10. 统一 LLM 调用到 _core/llm.py

Phase 3（完善测试基础设施）
  11. 创建 tests/conftest.py 共享 fixtures
  12. 统一 make_session 到 tests/helpers.py
  13. 更新 CLAUDE.md 和代码审查 checklist

预期收益：
  - 消除重复代码：700+ 行
  - 消除幽灵目录：CLAUDE_PROJECT_DIR 设置统一
  - 架构清晰：新开发者知道去哪里找什么
  - 防止退化：自动化检测 + checklist
```