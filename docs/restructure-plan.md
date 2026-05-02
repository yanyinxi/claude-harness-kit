# CHK 目录结构重构方案

> 目标：将项目目录结构对齐 Claude Code 官方规范，CHK 扩展能力统一收敛到 `harness/` 扩展目录；建立全局路径配置体系，根治硬编码路径问题。

**状态**：v2.0 — 待评审
**作者**：Claude Code
**日期**：2026-05-02

---

## 背景与动机（Why）

### B.1 当前目录结构的问题不只是"乱"

根目录平铺 9 个扩展目录，表面是命名混乱，深层是**架构失焦**：无法区分 Claude Code 官方标准与 CHK 自研扩展。后果：

- **升级脆弱**：Claude Code 升级 `.claude/` 规范时，CHK 自己的 `rules/`、`knowledge/`、`tests/` 会被混淆或覆盖
- **插件边界模糊**：`package.json` 的 `files[]` 无法准确描述"什么是 CHK"，发布后用户拿到的是一团目录而非可理解的模块
- **新人门槛高**：无法一眼看出哪些是官方约定、哪些是 CHK 特色，需要大量 tribal knowledge

### B.2 硬编码路径是技术债的根源

CHK 有 **42 个 Python 文件**，其中 **19 个包含硬编码路径**，典型问题：

| 问题类型 | 出现次数 | 代表案例 | 风险 |
|----------|----------|----------|------|
| 硬编码绝对路径 | 1 处 | `generate_skill_index.py` line 6 的 `/Users/yanyinxi/...` | 换机器即坏 |
| 硬编码 `.claude` 目录名 | 50+ 处 | 所有 hooks 和 daemon 文件 | 重命名需改 19 个文件 |
| JSONL 文件名散落 | 7 个文件名散落 8+ 文件 | `sessions.jsonl`、`error.jsonl` 等 | 重命名需改 8+ 文件 |
| Hook 源映射硬编码 | 1 处 | `collect_error.py` 的 `_HOOK_SOURCE_MAP` | 结构一变即失效 |
| instinct 位置不一致 | 2 处 | `instinct_cli.py` 在 `agents/instinct`，`instinct_updater.py` 在 `evolve-daemon` 同级 | 数据丢失风险 |
| API URL 硬编码 | 2 处 | `"https://api.anthropic.com/v1/messages"` | 无法切换端点/测试环境 |

**根本原因**：没有统一的配置层。每个模块各自为政，自己定义自己的路径常量。

### B.3 为什么现有方案不够

CHK 已有 `evolve-daemon/config.yaml`，但只服务 daemon，覆盖不了：

- Hook 脚本（`hooks/bin/`）在 config.yaml 之外
- CLI 工具（`cli/`）在 config.yaml 之外
- `_HOOK_SOURCE_MAP` 在代码里而不是配置文件

需要一个**全局统一**的配置层，覆盖**所有 Python 模块**，无论它们在哪个子目录。

---

## 一、现状分析

### 1.1 当前目录结构（全量盘点）

```
项目根目录/
├── .claude/                    ← 官方标准 ✅ 已对齐
│   ├── settings.json           ← 官方配置
│   ├── settings.local.json     ← 本地覆盖
│   ├── data/                   ← 运行时日志（session、error、agent调用）
│   ├── knowledge/              ← 知识库（decision、guideline、pitfall、process）
│   ├── tests/                  ← Claude Code 项目级测试
│   └── proposals/              ← Evolve Daemon 提案输出目录
│
├── .claude-plugin/             ← 官方插件元数据 ✅ 已对齐
│   ├── plugin.json             ← 插件声明（name、version、slashCommands）
│   └── marketplace.json        ← 市场发布元数据
│
├── index.js                    ← MCP Server 入口
├── package.json                ← NPM 包（files[] 列出分发文件）
├── CLAUDE.md                   ← 项目入口说明
├── README.md
├── .claudeignore               ← Claude Code 扫描排除
├── .gitignore
│
├── agents/                    ← ❌ 根目录 — CHK 扩展
│   ├── architect.md ... gc.md
│   └── instinct/instinct-record.json
│
├── skills/                    ← ❌ 根目录 — CHK 扩展（35 个 skills）
│   ├── SKILL.md / INDEX.md
│   ├── database-designer/
│   └── [其他 34 个 skill...]
│
├── hooks/                     ← ❌ 根目录 — CHK 扩展
│   ├── hooks.json            ← Hook 配置
│   └── bin/                   ← 19 个 Hook 脚本
│
├── rules/                     ← ❌ 根目录 — CHK 扩展（6 个规则）
│
├── memory/                    ← ❌ 根目录 — CHK 扩展（记忆/反馈）
│
├── knowledge/                 ← ❌ 根目录 — CHK 扩展（与 .claude/knowledge/ 重复）
│   ├── lifecycle.py / .yaml
│   └── project/ / team/
│
├── tests/                     ← ❌ 根目录 — CHK 测试（与 .claude/tests/ 部分重复）
│
├── docs/                      ← ❌ 根目录 — CHK 文档（设计/架构文档）
│
├── evolve-daemon/             ← ❌ 根目录 — CHK 扩展（独立守护进程）
│
└── cli/                       ← ❌ 根目录 — CHK CLI 工具（19 个工具 + 8 个 mode 配置）
```

### 1.2 核心问题

| 问题 | 说明 |
|------|------|
| **根目录混乱** | `agents/`、`skills/`、`hooks/`、`rules/`、`memory/`、`tests/`、`docs/`、`evolve-daemon/`、`cli/` 全部平铺在根目录，无法区分官方标准和 CHK 扩展 |
| **官方边界模糊** | Claude Code 官方约定的 `.claude/` 内只有 `settings`、`data`、`knowledge`、`rules`、`tests`；CHK 在根目录又放了一套 `rules/`、`knowledge/`、`tests/`，造成重复和混淆 |
| **插件分发结构不清晰** | `package.json` 的 `files[]` 列出 `agents/`、`skills/`、`hooks/`、`rules/` 在根目录，但这些应该属于插件范围，不应在根目录 |
| **knowledge 重复** | 存在 `.claude/knowledge/` 和 `knowledge/` 两个知识库，前者是官方结构，后者是 CHK 扩展但命名冲突 |
| **目录职责不清** | `cli/`、`evolve-daemon/`、`docs/` 这些项目级工具和文档没有统一归口 |

### 1.3 根目录文件一览（需确认是否保留）

| 文件 | 是否属于 Claude Code 官方 | 决策 |
|------|--------------------------|------|
| `index.js` | MCP Server，第三方扩展机制 | 保留在根目录 |
| `package.json` | NPM 标准 | 保留在根目录 |
| `marketplace.json` | CHK 市场清单 | 移到 `harness/marketplace.json` |
| `CLAUDE.md` | 官方入口文档（也接受在根目录） | 保留在根目录 |
| `README.md` | 项目说明 | 保留在根目录 |
| `.mcp.json` | MCP Server 配置 | 移到 `harness/.mcp.json` |
| `.claudeignore` | 官方约定 | 保留在根目录 |
| `.gitignore` | Git 标准 | 保留在根目录 |

---

## 二、目标结构

### 2.1 总体布局

```
项目根目录/
├── .claude/                    ← 【官方标准】不动，保持 Claude Code 规范
│   ├── settings.json
│   ├── settings.local.json
│   ├── data/                   ← 运行时日志（session、error、failures）
│   ├── knowledge/              ← 知识库（decision、guideline、pitfall、process、model）
│   ├── tests/                  ← Claude Code 项目级测试
│   └── proposals/              ← Evolve Daemon 提案输出
│
├── .claude-plugin/             ← 【官方插件元数据】不动
│   ├── plugin.json
│   └── marketplace.json
│
├── harness/                    ← 【新增】CHK 统一扩展目录
│   ├── docs/                  ← 设计/架构文档
│   ├── evolve-daemon/          ← 守护进程
│   ├── instinct/              ← 本能记录
│   ├── memory/                 ← 记忆/反馈系统
│   ├── rules/                  ← CHK 扩展规则
│   ├── skills/                 ← 35 个 CHK Skills
│   ├── agents/                 ← 22 个 CHK Agents（含 instinct/）
│   ├── hooks/                  ← Hook 配置 + 脚本
│   ├── knowledge/              ← CHK 知识库（与 .claude/knowledge/ 并列）
│   ├── tests/                  ← CHK 测试套件
│   ├── cli/                    ← CHK CLI 工具 + modes/
│   └── paths.py                ← 【新增】全局路径配置服务
│
├── index.js                    ← MCP Server（第三方扩展机制）
├── package.json
├── CLAUDE.md
├── README.md
├── .claudeignore
└── .gitignore
```

### 2.2 目录职责映射表

| 目标路径 | 来源 | 说明 |
|----------|------|------|
| `harness/agents/` | `agents/` | 22 个 Agent 定义 + instinct 子目录 |
| `harness/skills/` | `skills/` | 35 个 Skill（含 database-designer 等大型 skill） |
| `harness/hooks/` | `hooks/` | `hooks.json` + `bin/`（19 个脚本） |
| `harness/rules/` | `rules/` | 6 个 CHK 扩展规则 |
| `harness/memory/` | `memory/` | 记忆/反馈记录 |
| `harness/knowledge/` | `knowledge/` | CHK 知识库（生命周期、team、project wiki） |
| `harness/tests/` | `tests/` | CHK 测试套件（test_cli.py 等） |
| `harness/docs/` | `docs/` | 设计/架构文档 |
| `harness/evolve-daemon/` | `evolve-daemon/` | 守护进程 + templates |
| `harness/cli/` | `cli/` | CLI 工具 + modes/ 配置 |
| `harness/marketplace.json` | `marketplace.json` | CHK 市场清单 |
| `harness/.mcp.json` | `.mcp.json` | MCP Server 配置 |

### 2.3 架构原则

为什么这样划分：

| 原则 | 说明 | 收益 |
|------|------|------|
| **官方边界不可逾越** | `.claude/` 和 `.claude-plugin/` 是 Claude Code 规范，不碰 | 跟随官方升级，零兼容成本 |
| **扩展收敛单一入口** | 所有 CHK 扩展在 `harness/` 下 | 边界清晰、可独立打包分发 |
| **配置先行代码后** | 路径在 `config.yaml` 中声明，代码只读不写 | 未来目录重命名只需改一处 |
| **相对路径优先** | 代码用 `__file__` / `CLAUDE_PROJECT_DIR` 计算路径，不硬编码绝对路径 | 换机器、换目录皆可运行 |
| **环境变量兜底** | `CLAUDE_PROJECT_DIR` / `CLAUDE_PLUGIN_ROOT` 为运行时覆盖提供入口 | 支持多项目、多环境配置 |

---

## 三、全局路径配置体系设计

### 3.1 核心问题抽象

硬编码路径的本质是**紧耦合**：模块与路径值耦合在一起，导致目录结构一变，全量代码皆动。

解法是引入**配置层**：

```
配置层（YAML + 环境变量）
         ↓ 读取
    路径服务层（paths.py）
         ↓ 提供
   所有 Python 模块（读路径，不写路径）
```

### 3.2 路径服务层：`harness/paths.py`

**设计位置**：`harness/paths.py`

**设计原则**：

1. **单一来源**：所有路径常量只在这里定义一次
2. **配置驱动**：路径写在 YAML 中或由 `__file__` 推导，Python 只负责读取和计算
3. **兼容环境变量**：支持 `CLAUDE_PROJECT_DIR` / `CLAUDE_PLUGIN_ROOT` 运行时覆盖
4. **类型安全**：返回 `pathlib.Path` 对象而非字符串，减少拼接错误

**文件内容**：

```python
#!/usr/bin/env python3
"""
paths.py — CHK 全局路径配置服务

所有 Python 模块通过 from paths import * 获取路径常量。
任何目录结构变更只需要修改此文件。

使用方式:
  import sys
  sys.path.insert(0, str(Path(__file__).resolve().parent))
  from paths import ROOT, CLAUDE_DIR, DATA_DIR, SKILLS_DIR, ...

设计原则:
  - 环境变量 CLAUDE_PROJECT_DIR 优先于源码位置
  - 所有路径返回 pathlib.Path 对象
  - 文件路径用函数（lazy）而非常量，避免模块加载顺序问题
"""

import os
from pathlib import Path

# ════════════════════════════════════════════════════════════════════
# Layer 1: 源码位置（最低优先级）
# ════════════════════════════════════════════════════════════════════

_SCRIPT_LOCATION = Path(__file__).resolve().parent  # = harness/

# ════════════════════════════════════════════════════════════════════
# Layer 2: 环境变量（可覆盖）
# ════════════════════════════════════════════════════════════════════

def _project_root() -> Path:
    """项目根目录 — 环境变量优先，否则基于 __file__ 推断"""
    env_root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if env_root:
        return Path(env_root)
    # 推导：harness/ → 项目根目录
    return _SCRIPT_LOCATION.parent


def _plugin_root() -> Path:
    """插件根目录 — 环境变量优先，否则等于 _project_root()"""
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if env_root:
        return Path(env_root)
    return _project_root()


# ════════════════════════════════════════════════════════════════════
# Layer 3: 目录名常量（允许重命名 .claude 等目录名）
# ════════════════════════════════════════════════════════════════════

DIR_CLAUDE = ".claude"
DIR_DATA = "data"
DIR_PROPOSALS = "proposals"
DIR_HOOKS = "hooks"
DIR_HOOKS_BIN = "bin"
DIR_SKILLS = "skills"
DIR_AGENTS = "agents"
DIR_RULES = "rules"
DIR_MEMORY = "memory"
DIR_KNOWLEDGE = "knowledge"
DIR_TESTS = "tests"
DIR_DOCS = "docs"
DIR_INSTINCT = "instinct"
DIR_CLI = "cli"
DIR_CLI_MODES = "modes"

# ════════════════════════════════════════════════════════════════════
# Layer 4: JSONL 数据文件名常量（允许重命名日志文件）
# ════════════════════════════════════════════════════════════════════

FILE_SESSIONS = "sessions.jsonl"
FILE_ERRORS = "error.jsonl"
FILE_ERRORS_LOCK = "error.jsonl.lock"
FILE_FAILURES = "failures.jsonl"
FILE_AGENT_CALLS = "agent_calls.jsonl"
FILE_SKILL_CALLS = "skill_calls.jsonl"
FILE_OBSERVATIONS = "observations.jsonl"
FILE_OBS_ERRORS = "observe_errors.log"
FILE_ANALYSIS_STATE = "analysis_state.json"
FILE_INSTINCT_RECORD = "instinct-record.json"
FILE_SETTINGS_LOCAL = "settings.local.json"
FILE_LIFECYCLE_YAML = "lifecycle.yaml"

# API 端点常量
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# ════════════════════════════════════════════════════════════════════
# Layer 5: 路径常量
# ════════════════════════════════════════════════════════════════════

ROOT = _project_root()
PLUGIN_ROOT = _plugin_root()

# .claude/ 体系（官方标准）
CLAUDE_DIR = ROOT / DIR_CLAUDE
DATA_DIR = CLAUDE_DIR / DIR_DATA
PROPOSALS_DIR = CLAUDE_DIR / DIR_PROPOSALS
RATE_LIMITS_DIR = DATA_DIR / "rate-limits"
WORKTREES_DIR = DATA_DIR / "worktrees"

# .claude/data/*.jsonl 文件（懒访问函数，每次重新构建 Path）
def sessions_file() -> Path: return DATA_DIR / FILE_SESSIONS
def errors_file() -> Path: return DATA_DIR / FILE_ERRORS
def errors_lock_file() -> Path: return DATA_DIR / FILE_ERRORS_LOCK
def failures_file() -> Path: return DATA_DIR / FILE_FAILURES
def agent_calls_file() -> Path: return DATA_DIR / FILE_AGENT_CALLS
def skill_calls_file() -> Path: return DATA_DIR / FILE_SKILL_CALLS
def analysis_state_file() -> Path: return DATA_DIR / FILE_ANALYSIS_STATE

# 插件根体系（CHK 扩展）
SKILLS_DIR = PLUGIN_ROOT / DIR_SKILLS
AGENTS_DIR = PLUGIN_ROOT / DIR_AGENTS
RULES_DIR = PLUGIN_ROOT / DIR_RULES
HOOKS_DIR = PLUGIN_ROOT / DIR_HOOKS
HOOKS_BIN_DIR = HOOKS_DIR / DIR_HOOKS_BIN
MEMORY_DIR = PLUGIN_ROOT / DIR_MEMORY
KNOWLEDGE_DIR = PLUGIN_ROOT / DIR_KNOWLEDGE
TESTS_DIR = PLUGIN_ROOT / DIR_TESTS
DOCS_DIR = PLUGIN_ROOT / DIR_DOCS
INSTINCT_DIR = PLUGIN_ROOT / DIR_INSTINCT
CLI_DIR = PLUGIN_ROOT / DIR_CLI
CLI_MODES_DIR = CLI_DIR / DIR_CLI_MODES
EVOLVE_DIR = PLUGIN_ROOT / "evolve-daemon"
EVOLVE_TEMPLATES_DIR = EVOLVE_DIR / "templates"
EVOLVE_CONFIG_FILE = EVOLVE_DIR / "config.yaml"

# instinct-record.json 文件（统一位置，解决 instinct_cli 和 instinct_updater 不一致问题）
INSTINCT_FILE = INSTINCT_DIR / FILE_INSTINCT_RECORD

# cli 内部
LIFECYCLE_YAML = KNOWLEDGE_DIR / FILE_LIFECYCLE_YAML
SETTINGS_LOCAL = CLAUDE_DIR / FILE_SETTINGS_LOCAL

# ════════════════════════════════════════════════════════════════════
# Hook 脚本名映射（替换 collect_error.py 的 _HOOK_SOURCE_MAP）
# ════════════════════════════════════════════════════════════════════

HOOK_SCRIPTS = {
    "safety-check.sh": HOOKS_BIN_DIR / "safety-check.sh",
    "quality-gate.sh": HOOKS_BIN_DIR / "quality-gate.sh",
    "tdd-check.sh": HOOKS_BIN_DIR / "tdd-check.sh",
    "rate-limiter.sh": HOOKS_BIN_DIR / "rate-limiter.sh",
    "collect-failure.py": HOOKS_BIN_DIR / "collect-failure.py",
    "collect-agent.py": HOOKS_BIN_DIR / "collect-agent.py",
    "collect-skill.py": HOOKS_BIN_DIR / "collect-skill.py",
    "collect-session.py": HOOKS_BIN_DIR / "collect-session.py",
    "output-secret-filter.py": HOOKS_BIN_DIR / "output-secret-filter.py",
    "observe.sh": HOOKS_BIN_DIR / "observe.sh",
    "checkpoint-auto-save.sh": HOOKS_BIN_DIR / "checkpoint-auto-save.sh",
    "worktree-sync.sh": HOOKS_BIN_DIR / "worktree-sync.sh",
    "worktree-cleanup.sh": HOOKS_BIN_DIR / "worktree-cleanup.sh",
    "context-injector.py": HOOKS_BIN_DIR / "context-injector.py",
    "extract-semantics.py": HOOKS_BIN_DIR / "extract-semantics.py",
}

# ════════════════════════════════════════════════════════════════════
# 导出（from paths import * 时可见）
# ════════════════════════════════════════════════════════════════════

__all__ = [
    # 目录名常量
    "DIR_CLAUDE", "DIR_DATA", "DIR_PROPOSALS", "DIR_HOOKS", "DIR_HOOKS_BIN",
    "DIR_SKILLS", "DIR_AGENTS", "DIR_RULES", "DIR_MEMORY", "DIR_KNOWLEDGE",
    "DIR_TESTS", "DIR_DOCS", "DIR_INSTINCT", "DIR_CLI", "DIR_CLI_MODES",
    # JSONL 文件名常量
    "FILE_SESSIONS", "FILE_ERRORS", "FILE_ERRORS_LOCK", "FILE_FAILURES",
    "FILE_AGENT_CALLS", "FILE_SKILL_CALLS", "FILE_OBSERVATIONS",
    "FILE_OBS_ERRORS", "FILE_ANALYSIS_STATE", "FILE_INSTINCT_RECORD",
    "FILE_SETTINGS_LOCAL", "FILE_LIFECYCLE_YAML",
    # API 端点
    "ANTHROPIC_API_URL",
    # 路径对象
    "ROOT", "PLUGIN_ROOT",
    "CLAUDE_DIR", "DATA_DIR", "PROPOSALS_DIR", "RATE_LIMITS_DIR", "WORKTREES_DIR",
    "SKILLS_DIR", "AGENTS_DIR", "RULES_DIR", "HOOKS_DIR", "HOOKS_BIN_DIR",
    "MEMORY_DIR", "KNOWLEDGE_DIR", "TESTS_DIR", "DOCS_DIR", "INSTINCT_DIR",
    "CLI_DIR", "CLI_MODES_DIR", "EVOLVE_DIR", "EVOLVE_TEMPLATES_DIR", "EVOLVE_CONFIG_FILE",
    "INSTINCT_FILE", "LIFECYCLE_YAML", "SETTINGS_LOCAL",
    # 方法（lazy 文件路径）
    "sessions_file", "errors_file", "errors_lock_file", "failures_file",
    "agent_calls_file", "skill_calls_file", "analysis_state_file",
    # Hook 映射
    "HOOK_SCRIPTS",
]
```

### 3.3 为什么这样设计

| 设计决策 | 为什么 | 如果未来目录变 |
|----------|--------|----------------|
| `DIR_CLAUDE = ".claude"` 作为常量 | `.claude` 字符串在 19 个文件里出现 50+ 次，改名成本高 | 只改常量值，全量代码生效 |
| `ROOT` 用环境变量优先 | 允许外部注入路径，适合测试和 CI | 测试可以 mock 环境变量 |
| 文件路径用函数而非常量 | 避免模块加载时路径尚未初始化 | 无影响 |
| `HOOK_SCRIPTS` 用 `dict` | hook 数量可能变化，且需要 Path 对象 | 加一个 key 即可 |
| `__all__` 显式导出 | 控制 `from paths import *` 的命名空间 | 防止意外导入 |
| 不在 `paths.py` 中 import 其他 CHK 模块 | 避免循环依赖；paths 是最底层模块 | 无影响 |

### 3.4 使用方式

```python
# 旧写法（硬编码）
from pathlib import Path
SKILLS_DIR = Path("/Users/yanyinxi/工作/code/github/claude-harness-kit/skills")

# 新写法（统一配置）
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # 添加 harness/ 到 sys.path
from paths import SKILLS_DIR

# 旧写法（散落 JSONL 文件名）
sessions_file = data_dir / "sessions.jsonl"

# 新写法（统一来源）
from paths import sessions_file, DATA_DIR
sessions = sessions_file()
```

### 3.5 需要迁移的具体文件清单

| 文件 | 旧写法 | 新写法 |
|------|--------|--------|
| `cli/generate_skill_index.py` | `Path("/Users/yanyinxi/工作/...")` | `from paths import SKILLS_DIR` |
| `evolve-daemon/daemon.py` | inline fallback config 中硬编码 `".claude/data"` | 读 `paths.DATA_DIR` |
| `evolve-daemon/proposer.py` | `"https://api.anthropic.com/..."` 硬编码 | `from paths import ANTHROPIC_API_URL` |
| `hooks/bin/collect_error.py` | `_HOOK_SOURCE_MAP` dict | `from paths import HOOK_SCRIPTS` |
| `hooks/bin/observe.py` | `PLUGIN_ROOT / ".claude" / "homunculus"` | `from paths import OBS_DIR`（新增） |
| `cli/instinct_cli.py` | `Path(__file__).parent.parent / "agents" / "instinct"` | `from paths import INSTINCT_DIR` |
| `evolve-daemon/instinct_updater.py` | `Path(__file__).parent.parent / "instinct"` | `from paths import INSTINCT_DIR` |
| `cli/mode.py` | `Path(__file__).parent / "modes"` | `from paths import CLI_MODES_DIR` |
| `knowledge/lifecycle.py` | `Path(__file__).parent / "lifecycle.yaml"` | `from paths import LIFECYCLE_YAML` |

---

## 四、详细技术方案

### 4.1 执行顺序

**正确顺序：路径重构先于目录迁移**

```
Step P.1 — 创建 harness/paths.py（路径服务层）
Step P.2 — 所有 Python 模块改用 paths.py（不移动目录，路径不变）
Step P.3 — 执行目录迁移（git mv）
Step P.4 — 验证
```

原因：paths.py 中 `PLUGIN_ROOT` 基于 `__file__` 推导，迁移前后路径值不变。先改 import 语句，目录迁移后自然指向新位置。

### 4.2 Phase 0：准备阶段

**Step 0.1** 备份 `.gitignore`

**Step 0.2** 更新 `.gitignore`

```gitignore
# harness 运行时数据
harness/.claude/data/rate-limits/
harness/.claude/data/worktrees/
harness/.claude/data/error.jsonl
harness/.claude/data/error.jsonl.lock
harness/.claude/data/failures.jsonl
```

**Step 0.3** 更新 `.claudeignore`

```claudeignore
harness/.claude/data/
harness/node_modules/
harness/__pycache__/
```

### 4.3 Phase P：路径重构

**Step P.1** 创建 `harness/paths.py`（内容见 3.2 节）

**Step P.2–P.7** 逐个修改 Python 文件的 import 语句

### 4.4 Phase M：目录迁移

**Step M.1** 创建 `harness/` 及所有子目录

```bash
mkdir -p harness/{docs,evolve-daemon/templates,instinct,memory,rules,skills,agents/instinct,hooks/bin,knowledge/{project,team/biz-wiki,team/tech-wiki},tests,cli/modes}
```

**Step M.2** 使用 `git mv` 迁移所有目录（保留 Git 历史）

```bash
git mv agents harness/agents
git mv skills harness/skills
git mv hooks harness/hooks
git mv rules harness/rules
git mv memory harness/memory
git mv knowledge harness/knowledge
git mv tests harness/tests
git mv docs harness/docs
git mv evolve-daemon harness/evolve-daemon
git mv cli harness/cli
git mv marketplace.json harness/
git mv .mcp.json harness/
```

## 附录 D：Per-Module Config YAML 体系设计

### D.1 设计原则

| 原则 | 说明 |
|------|------|
| **分层覆盖** | 全局配置 < 模块配置 < 环境变量 < CLI 参数 |
| **零妥协** | 每个模块行为参数必须进 YAML，禁止硬编码 |
| **懒加载** | 仅在使用时才 resolve path，import 时不触发 |
| **类型安全** | 所有配置项有类型声明和校验 |
| **可回滚** | 每步改完立刻 commit + 跑测试 |

### D.2 ConfigLoader 基类

```python
# harness/_core/config_loader.py
from pathlib import Path
from typing import Any, Optional, TypeVar
import yaml, os

T = TypeVar("T", bound="BaseConfig")

class BaseConfig:
    DEFAULTS: dict = {}
    _cache: Optional[dict] = None

    @classmethod
    def load(cls, harness_root: Optional[Path] = None) -> dict:
        if cls._cache:
            return cls._cache
        base = cls.DEFAULTS.copy()
        path = cls._config_path(harness_root)
        if path and path.exists():
            with open(path) as f:
                user = yaml.safe_load(f) or {}
            base = cls._merge(base, user)
        base = cls._apply_env(base)
        cls._cache = base
        return base

    @classmethod
    def _config_path(cls, harness_root) -> Optional[Path]:
        return None

    @classmethod
    def _merge(cls, base: dict, override: dict) -> dict:
        result = base.copy()
        for k, v in override.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = cls._merge(result[k], v)
            else:
                result[k] = v
        return result

    @classmethod
    def _apply_env(cls, cfg: dict) -> dict:
        for key in list(cfg.keys()):
            env_key = f"{cls._env_prefix()}_{key.upper()}"
            if env_key in os.environ:
                cfg[key] = os.environ[env_key]
        return cfg

    @classmethod
    def _env_prefix(cls) -> str:
        return "CHK"
```

### D.3 paths.py 全局路径配置

```python
# harness/_core/paths.py
"""
Harness 全局路径配置层。

优先顺序（高→低）:
  1. 环境变量 CLAUDE_HARNESS_ROOT（显式注入）
  2. --harness-root CLI 参数（运行时覆盖）
  3. 源码定位（__file__ / WORKDIR 检测）
  4. DEFAULTS（硬编码兜底）
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

_DIR_CLAUDE     = ".claude"
_DIR_DATA      = f"{_DIR_CLAUDE}/data"
_DIR_KNOWLEDGE = f"{_DIR_CLAUDE}/knowledge"
_DIR_RULES     = f"{_DIR_CLAUDE}/rules"
_DIR_AGENTS    = f"{_DIR_CLAUDE}/agents"
_DIR_SKILLS    = f"{_DIR_CLAUDE}/skills"
_DIR_HOOKS     = f"{_DIR_CLAUDE}/hooks"
_DIR_COMMANDS  = f"{_DIR_CLAUDE}/commands"
_DIR_TESTS     = f"{_DIR_CLAUDE}/tests"

DIR_CLAUDE     = Path(_DIR_CLAUDE)
DIR_DATA       = Path(_DIR_DATA)
DIR_KNOWLEDGE  = Path(_DIR_KNOWLEDGE)
DIR_RULES      = Path(_DIR_RULES)
DIR_AGENTS     = Path(_DIR_AGENTS)
DIR_SKILLS     = Path(_DIR_SKILLS)
DIR_HOOKS      = Path(_DIR_HOOKS)
DIR_COMMANDS   = Path(_DIR_COMMANDS)
DIR_TESTS      = Path(_DIR_TESTS)

FILE_SESSIONS  = DIR_DATA / "sessions.jsonl"
FILE_ERRORS    = DIR_DATA / "errors.jsonl"
FILE_SETTINGS  = DIR_CLAUDE / "settings.json"
FILE_SLOCAL   = DIR_CLAUDE / "settings.local.json"

_harness_root: Optional[Path] = None

def set_harness_root(path: Path):
    global _harness_root
    _harness_root = path.resolve()

def get_harness_root() -> Path:
    if _harness_root:
        return _harness_root
    root = os.environ.get("CLAUDE_HARNESS_ROOT")
    if root:
        return Path(root).resolve()
    try:
        return Path(__file__).parent.parent.resolve()
    except NameError:
        return Path.cwd()

def path(name: str) -> Path:
    return get_harness_root() / name

def resolve(*parts) -> Path:
    return get_harness_root() / "/".join(parts)
```

### D.4 各模块 Config YAML 完整设计

---

#### D.4.1 evolve-daemon/config.yaml

```yaml
# 自动进化 Daemon 配置
# 对应原：evolve-daemon/daemon.py（hardcoded 内联配置）

daemon:
  schedule: "*/30 * * * *"       # cron 表达式，daemon 调度周期
  idle_trigger_minutes: 120      # 空闲触发阈值（分钟）
  extract_timeout_seconds: 5     # pattern extract 超时

paths:
  proposals_dir: ".claude/proposals"
  backups_dir: ".claude/data/backups"
  data_dir: ".claude/data"
  instinct_dir: "instinct"
  rules_dir: "rules"
  skills_dir: "skills"
  agents_dir: "agents"

thresholds:
  min_failure_count: 5          # 最小失败次数
  min_failure_rate: 0.5         # 最小失败率
  min_failure_type_count: 3     # 最小失败类型数
  min_new_sessions: 2           # 最小新 session 数
  min_same_pattern_corrections: 3  # 最小同 pattern 纠错数
  max_hours_since_last_analyze: 6   # 最大分析间隔

observation:
  days: 7                       # 观察期天数
  check_interval_hours: 24      # 检查间隔
  metrics:
    min_success_rate: 0.8
    max_failure_rate_delta: 0.1
    max_correction_rate: 0.2

decision:
  enabled: true
  auto_apply_threshold: 0.8     # 自动应用阈值
  high_risk_threshold: 0.5
  require_human_review:
    - security
    - permission
    - new_target
    - multi_file
  risk_rules:
    high_risk_patterns:
      - permission
      - credential
      - security
      - auth
    low_risk_patterns:
      - comment
      - format
      - typo
      - docs
      - example

safety:
  max_proposals_per_day: 3
  auto_close_days: 7
  breaker:
    max_consecutive_rejects: 3
    max_rollbacks_per_week: 5
    pause_days: 30

rollback:
  auto_enabled: true
  observe_before_rollback_hours: 24
  triggers:
    - success_rate_decreased
    - correction_rate_increased
    - failure_count_increased
    - user_feedback_negative

notification:
  enabled: false
  channels:
    email:
      enabled: false
      smtp_host: "smtp.example.com"
      smtp_port: 587
      to_addresses:
        - "admin@example.com"

claude_api:
  analyze_model: "claude-sonnet-4-6"
  analyze_temperature: 0.3
  analyze_max_tokens: 4096
  decide_model: "claude-sonnet-4-6"
  decide_temperature: 0.2
  decide_max_tokens: 2048
  extract_model: "claude-haiku-4-5"
  extract_temperature: 0.1
  extract_max_tokens: 512

decay:
  half_life_days: 90
  decay_floor: 0.1
  max_confidence: 0.95
  min_reinforcement: 3
  reinforcement_bonus: 0.05

validation:
  enabled: true
  max_age_days: 90
  quarantine_malformed: true
```

**ConfigLoader 实现**：

```python
# harness/evolve-daemon/config.py
from harness._core.config_loader import BaseConfig

class EvolveConfig(BaseConfig):
    _module = "evolve-daemon"

    DEFAULTS = {
        "daemon": {"schedule": "*/30 * * * *", "idle_trigger_minutes": 120,
                   "extract_timeout_seconds": 5},
        "paths": {"proposals_dir": ".claude/proposals", "data_dir": ".claude/data",
                  "backups_dir": ".claude/data/backups", "instinct_dir": "instinct",
                  "rules_dir": "rules", "skills_dir": "skills", "agents_dir": "agents"},
        "thresholds": {"min_failure_count": 5, "min_failure_rate": 0.5,
                       "min_failure_type_count": 3, "min_new_sessions": 2,
                       "min_same_pattern_corrections": 3,
                       "max_hours_since_last_analyze": 6},
        "observation": {"days": 7, "check_interval_hours": 24,
                        "metrics": {"min_success_rate": 0.8,
                                    "max_failure_rate_delta": 0.1,
                                    "max_correction_rate": 0.2}},
        "decision": {"enabled": True, "auto_apply_threshold": 0.8,
                     "high_risk_threshold": 0.5,
                     "require_human_review": ["security","permission","new_target","multi_file"],
                     "risk_rules": {"high_risk_patterns":["permission","credential","security","auth"],
                                    "low_risk_patterns":["comment","format","typo","docs","example"]}},
        "safety": {"max_proposals_per_day": 3, "auto_close_days": 7,
                   "breaker": {"max_consecutive_rejects": 3,
                               "max_rollbacks_per_week": 5, "pause_days": 30}},
        "rollback": {"auto_enabled": True, "observe_before_rollback_hours": 24,
                     "triggers": ["success_rate_decreased","correction_rate_increased",
                                  "failure_count_increased","user_feedback_negative"]},
        "notification": {"enabled": False,
                         "channels": {"email": {"enabled": False, "smtp_host": "smtp.example.com",
                                                 "smtp_port": 587,
                                                 "to_addresses": ["admin@example.com"]}}},
        "claude_api": {"analyze_model": "claude-sonnet-4-6", "analyze_temperature": 0.3,
                       "analyze_max_tokens": 4096, "decide_model": "claude-sonnet-4-6",
                       "decide_temperature": 0.2, "decide_max_tokens": 2048,
                       "extract_model": "claude-haiku-4-5", "extract_temperature": 0.1,
                       "extract_max_tokens": 512},
        "decay": {"half_life_days": 90, "decay_floor": 0.1, "max_confidence": 0.95,
                  "min_reinforcement": 3, "reinforcement_bonus": 0.05},
        "validation": {"enabled": True, "max_age_days": 90, "quarantine_malformed": True},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "evolve-daemon" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_EVOLVE"
```

---

#### D.4.2 hooks/config.yaml

```yaml
# Hooks 配置
# 对应原：hooks/hooks.json（仅 trigger 列表，无行为参数）

execution:
  max_retries: 3
  timeout_seconds: 30
  shell: "/bin/bash"             # 或 /bin/zsh
  tracing: true
  error_output_dir: ".claude/data/errors"

source_map:
  pre_prompt:   "hooks/bin/pre_prompt.py"
  post_execute: "hooks/bin/post_execute.py"
  error:        "hooks/bin/collect_error.py"
  observe:     "hooks/bin/observe.py"
  evolve:      "hooks/bin/evolve.py"

tracing:
  enabled: true
  format: "jsonl"
  output_dir: ".claude/data/traces"

error_handling:
  collect_full_traceback: true
  anonymize_paths: true          # 路径脱敏（去掉用户 home 目录前缀）
  max_traceback_lines: 50

hooks:
  pre_prompt:
    enabled: true
    priority: 100
  post_execute:
    enabled: true
    priority: 50
  error:
    enabled: true
    priority: 200
  observe:
    enabled: true
    priority: 150
  evolve:
    enabled: false              # 默认关闭，用户开启后启用
    priority: 10
```

**ConfigLoader 实现**：

```python
# harness/hooks/config.py
from harness._core.config_loader import BaseConfig

class HooksConfig(BaseConfig):
    _module = "hooks"

    DEFAULTS = {
        "execution": {"max_retries": 3, "timeout_seconds": 30,
                      "shell": "/bin/bash", "tracing": True,
                      "error_output_dir": ".claude/data/errors"},
        "source_map": {"pre_prompt": "hooks/bin/pre_prompt.py",
                       "post_execute": "hooks/bin/post_execute.py",
                       "error": "hooks/bin/collect_error.py",
                       "observe": "hooks/bin/observe.py",
                       "evolve": "hooks/bin/evolve.py"},
        "tracing": {"enabled": True, "format": "jsonl",
                    "output_dir": ".claude/data/traces"},
        "error_handling": {"collect_full_traceback": True,
                           "anonymize_paths": True,
                           "max_traceback_lines": 50},
        "hooks": {"pre_prompt": {"enabled": True, "priority": 100},
                  "post_execute": {"enabled": True, "priority": 50},
                  "error": {"enabled": True, "priority": 200},
                  "observe": {"enabled": True, "priority": 150},
                  "evolve": {"enabled": False, "priority": 10}},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "hooks" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_HOOKS"
```

---

#### D.4.3 rules/config.yaml

```yaml
# Rules 配置
# 对应原：无（rules/ 下仅 .md 规则文件，无行为控制）

search:
  recurse: true
  include_hidden: false
  file_patterns: ["*.md"]
  max_depth: 3

loading:
  cache_enabled: true
  cache_ttl_seconds: 300
  merge_strategy: "prepend"      # prepend | append | override

priority_groups:
  security: 100
  quality-gates: 80
  general: 50
  collaboration: 30
  expert-mode: 20

format:
  encoding: "utf-8"
  strip_yaml_frontmatter: true
```

**ConfigLoader 实现**：

```python
# harness/rules/config.py
from harness._core.config_loader import BaseConfig

class RulesConfig(BaseConfig):
    _module = "rules"

    DEFAULTS = {
        "search": {"recurse": True, "include_hidden": False,
                   "file_patterns": ["*.md"], "max_depth": 3},
        "loading": {"cache_enabled": True, "cache_ttl_seconds": 300,
                    "merge_strategy": "prepend"},
        "priority_groups": {"security": 100, "quality-gates": 80,
                            "general": 50, "collaboration": 30,
                            "expert-mode": 20},
        "format": {"encoding": "utf-8", "strip_yaml_frontmatter": True},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "rules" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_RULES"
```

---

#### D.4.4 skills/config.yaml

```yaml
# Skills 配置
# 对应原：cli/generate_skill_index.py（硬编码 SKILLS_DIR）

paths:
  skills_dir: "skills"
  index_template: "skills/INDEX.md"

generation:
  auto_generate_index: false     # 每次 skills/ 变更是否重新生成 INDEX.md
  overwrite_existing: true

skill_registry:
  cache_enabled: true
  cache_ttl_seconds: 600
  validate_triggers: true        # 校验每个 skill 是否有 trigger 声明
```

**ConfigLoader 实现**：

```python
# harness/skills/config.py
from harness._core.config_loader import BaseConfig

class SkillsConfig(BaseConfig):
    _module = "skills"

    DEFAULTS = {
        "paths": {"skills_dir": "skills",
                  "index_template": "skills/INDEX.md"},
        "generation": {"auto_generate_index": False,
                       "overwrite_existing": True},
        "skill_registry": {"cache_enabled": True, "cache_ttl_seconds": 600,
                           "validate_triggers": True},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "skills" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_SKILLS"
```

---

#### D.4.5 agents/config.yaml

```yaml
# Agents 配置

paths:
  agents_dir: "agents"
  default_agent_dir: "agents"

loading:
  cache_enabled: true
  cache_ttl_seconds: 600
  merge_system_prompt: true

defaults:
  model: "claude-sonnet-4-6"
  temperature: 0.3
  max_tokens: 4096
  timeout_seconds: 120
```

**ConfigLoader 实现**：

```python
# harness/agents/config.py
from harness._core.config_loader import BaseConfig

class AgentsConfig(BaseConfig):
    _module = "agents"

    DEFAULTS = {
        "paths": {"agents_dir": "agents", "default_agent_dir": "agents"},
        "loading": {"cache_enabled": True, "cache_ttl_seconds": 600,
                    "merge_system_prompt": True},
        "defaults": {"model": "claude-sonnet-4-6", "temperature": 0.3,
                     "max_tokens": 4096, "timeout_seconds": 120},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "agents" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_AGENTS"
```

---

#### D.4.6 context/config.yaml

```yaml
# Context 管理配置
# 对应原：cli/（无配置层）

compaction:
  strategy: "hybrid"              # hybrid | aggressive | conservative
  max_tokens: 150000
  preserve_session_boundary: true

injection:
  order: "rules,skills,agents,instinct"  # 注入顺序
  max_total_chars: 30000
  encoding: "utf-8"

memory:
  max_entries: 1000
  ttl_days: 90
  eviction_policy: "lru"
```

**ConfigLoader 实现**：

```python
# harness/context/config.py
from harness._core.config_loader import BaseConfig

class ContextConfig(BaseConfig):
    _module = "context"

    DEFAULTS = {
        "compaction": {"strategy": "hybrid", "max_tokens": 150000,
                      "preserve_session_boundary": True},
        "injection": {"order": "rules,skills,agents,instinct",
                      "max_total_chars": 30000, "encoding": "utf-8"},
        "memory": {"max_entries": 1000, "ttl_days": 90,
                   "eviction_policy": "lru"},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "context" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_CONTEXT"
```

---

#### D.4.7 instinct/config.yaml

```yaml
# Instinct 配置
# 对应原：evolve-daemon/instinct_updater.py（硬编码内联配置）

decay:
  half_life_days: 90
  decay_floor: 0.1
  reinforcement_bonus: 0.05
  max_confidence: 0.95
  min_reinforcement: 3

confidence:
  initial: 0.3
  promotion_delta: 0.1
  demotion_delta: 0.1
  seed_override: 1.0             # seed 记录初始置信度

lifecycle:
  auto_prune_days: 180           # 自动清理超过 N 天的已衰减记录
  quarantine_malformed: true

paths:
  instinct_dir: "instinct"
  record_file: "instinct/instinct-record.json"
```

**ConfigLoader 实现**：

```python
# harness/instinct/config.py
from harness._core.config_loader import BaseConfig

class InstinctConfig(BaseConfig):
    _module = "instinct"

    DEFAULTS = {
        "decay": {"half_life_days": 90, "decay_floor": 0.1,
                  "reinforcement_bonus": 0.05, "max_confidence": 0.95,
                  "min_reinforcement": 3},
        "confidence": {"initial": 0.3, "promotion_delta": 0.1,
                       "demotion_delta": 0.1, "seed_override": 1.0},
        "lifecycle": {"auto_prune_days": 180, "quarantine_malformed": True},
        "paths": {"instinct_dir": "instinct",
                  "record_file": "instinct/instinct-record.json"},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "instinct" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_INSTINCT"
```

---

#### D.4.8 memory/config.yaml

```yaml
# Memory 配置
# 对应原：memory/（无配置层）

persistence:
  max_memory_size_kb: 5120       # 单个 memory 文件最大 5MB
  index_max_lines: 200
  auto_snapshot: true
  snapshot_interval_minutes: 30

memory:
  types:
    - user
    - feedback
    - project
    - reference

paths:
  memory_dir: "memory"
  index_file: "memory/MEMORY.md"
```

**ConfigLoader 实现**：

```python
# harness/memory/config.py
from harness._core.config_loader import BaseConfig

class MemoryConfig(BaseConfig):
    _module = "memory"

    DEFAULTS = {
        "persistence": {"max_memory_size_kb": 5120, "index_max_lines": 200,
                        "auto_snapshot": True,
                        "snapshot_interval_minutes": 30},
        "memory": {"types": ["user", "feedback", "project", "reference"]},
        "paths": {"memory_dir": "memory",
                  "index_file": "memory/MEMORY.md"},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "memory" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_MEMORY"
```

---

#### D.4.9 prompts/config.yaml

```yaml
# Prompts 配置
# 对应原：无配置层

paths:
  prompts_dir: "prompts"

generation:
  max_length: 2000
  include_examples: true
  variable_syntax: "{{var}}"

context_injection:
  enabled: true
  max_depth: 3
  exclude_patterns: ["node_modules/**", ".git/**"]
```

**ConfigLoader 实现**：

```python
# harness/prompts/config.py
from harness._core.config_loader import BaseConfig

class PromptsConfig(BaseConfig):
    _module = "prompts"

    DEFAULTS = {
        "paths": {"prompts_dir": "prompts"},
        "generation": {"max_length": 2000, "include_examples": True,
                       "variable_syntax": "{{var}}"},
        "context_injection": {"enabled": True, "max_depth": 3,
                              "exclude_patterns": ["node_modules/**", ".git/**"]},
    }

    @classmethod
    def _config_path(cls, harness_root=None):
        from harness._core import paths
        root = harness_root or paths.get_harness_root()
        return root / "harness" / "prompts" / "config.yaml"

    @classmethod
    def _env_prefix(cls):
        return "CHK_PROMPTS"
```

---

#### D.4.10 harness/config.yaml（全局配置）

```yaml
# Harness 全局配置
# 所有模块共享的顶级配置

paths:
  harness_root: null              # 如果为 null，使用源码定位
  claude_dir: ".claude"

core:
  debug_mode: false
  trace_all: false

plugins:
  auto_discover: true
  enabled: ["*"]                 # "*" 表示全部启用
  disabled: []
```

### D.5 ConfigValidator 启动校验

```python
# harness/_core/config_validator.py
"""启动时校验所有 YAML 配置文件的有效性"""
import sys
from pathlib import Path

class ValidationError(Exception):
    pass

def validate_all_configs(harness_root: Path):
    """在 daemon 启动时调用，校验所有模块 config.yaml"""
    modules = ["evolve-daemon","hooks","rules","skills","agents",
               "context","instinct","memory","prompts"]
    errors = []
    for mod in modules:
        cfg_path = harness_root / "harness" / mod / "config.yaml"
        if not cfg_path.exists():
            errors.append(f"[{mod}] config.yaml not found")
            continue
        try:
            import yaml
            with open(cfg_path) as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                errors.append(f"[{mod}] config.yaml must be a dict")
        except yaml.YAMLError as e:
            errors.append(f"[{mod}] YAML parse error: {e}")
    if errors:
        raise ValidationError("\n".join(errors))

# 在 daemon.py 启动时调用:
# validate_all_configs(paths.get_harness_root())
```

### D.6 配置优先级速查表

| 优先级 | 来源 | 示例 |
|--------|------|------|
| 1（最高） | CLI 参数 | `--harness-root /path/to/harness` |
| 2 | 环境变量 | `CHK_EVOLVE_DAEMON_SCHEDULE=*/15 * * * *` |
| 3 | 模块 config.yaml | `evolve-daemon/config.yaml` |
| 4 | 全局 harness.yaml | `harness/harness.yaml` |
| 5（最低） | DEFAULTS | `BaseConfig.DEFAULTS` 硬编码兜底 |

### D.7 迁移策略

**Phase 1：创建 `_core` 基础设施**
1. 创建 `harness/_core/paths.py` — 全局路径服务
2. 创建 `harness/_core/config_loader.py` — ConfigLoader 基类
3. 创建 `harness/_core/config_validator.py` — 启动校验

**Phase 2：各模块配置文件**
4. 为每个模块创建 `config.yaml` + `config.py`
5. 用 grep 替换硬编码路径为 `Config.get("key")` 调用
6. 每个模块改完后立即 commit

**Phase 3：清理**
7. 删除所有被 `config.py` 替代的硬编码内联配置
8. 跑测试套件验证
9. 提交 final commit

**关键原则**：
- 每步改完即 commit，不批量提交
- 用 `git mv` 保留文件历史
- 每个模块配置文件至少包含 DEFAULTS，即使 YAML 文件不存在也能正常工作
- ConfigLoader 永远先 fallback 到 DEFAULTS，YAML 不存在或解析失败不崩溃**Step M.3** 更新 `package.json` 的 `files` 数组

```json
{
  "files": [
    ".claude-plugin/",
    "harness/",
    "CLAUDE.md",
    "README.md",
    "package.json"
  ]
}
```

### 4.5 Phase V：验证

**Step V.1** 运行测试套件

```bash
npm test
```

**Step V.2** Claude Code 加载验证

**Step V.3** MCP Server 启动验证

**Step V.4** Evolve Daemon 启动验证

---

## 五、涉及改动点全清单

### 5.1 文件系统操作

| 序号 | 操作 | 源路径 | 目标路径 |
|------|------|--------|----------|
| 1 | 创建 | (新) | `harness/paths.py` |
| 2 | 迁移 | `agents/` | `harness/agents/` |
| 3 | 迁移 | `skills/` | `harness/skills/` |
| 4 | 迁移 | `hooks/` | `harness/hooks/` |
| 5 | 迁移 | `rules/` | `harness/rules/` |
| 6 | 迁移 | `memory/` | `harness/memory/` |
| 7 | 迁移 | `knowledge/` | `harness/knowledge/` |
| 8 | 迁移 | `tests/` | `harness/tests/` |
| 9 | 迁移 | `docs/` | `harness/docs/` |
| 10 | 迁移 | `evolve-daemon/` | `harness/evolve-daemon/` |
| 11 | 迁移 | `cli/` | `harness/cli/` |
| 12 | 迁移 | `marketplace.json` | `harness/marketplace.json` |
| 13 | 迁移 | `.mcp.json` | `harness/.mcp.json` |

### 5.2 Python 模块路径引用更新

| 序号 | 文件 | 改动 |
|------|------|------|
| 1 | `cli/generate_skill_index.py` | 改用 `paths.SKILLS_DIR` |
| 2 | `evolve-daemon/daemon.py` | 改用 `paths.DATA_DIR` 等 |
| 3 | `evolve-daemon/proposer.py` | 改用 `paths.ANTHROPIC_API_URL` |
| 4 | `evolve-daemon/instinct_updater.py` | 改用 `paths.INSTINCT_DIR` |
| 5 | `hooks/bin/collect_error.py` | 改用 `paths.HOOK_SCRIPTS` |
| 6 | `hooks/bin/observe.py` | 改用 `paths.OBS_DIR`（新增） |
| 7 | `cli/instinct_cli.py` | 改用 `paths.INSTINCT_DIR` |
| 8 | `cli/mode.py` | 改用 `paths.CLI_MODES_DIR` |
| 9 | `knowledge/lifecycle.py` | 改用 `paths.LIFECYCLE_YAML` |

---

## 六、风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| **路径引用遗漏** | 部分脚本中的硬编码路径未更新 | Phase V 的完整验证步骤；逐文件 grep |
| **`${CLAUDE_PLUGIN_ROOT}` 行为变化** | 迁移后 `CLAUDE_PLUGIN_ROOT` 指向 `harness/` | 验证 `plugin.json` 约定；在 `hooks.json` 中显式使用相对路径 |
| **循环依赖** | `paths.py` 意外 import 了依赖它的模块 | `paths.py` 设计为纯底层，不 import 任何 CHK 模块 |
| **instinct 数据丢失** | instinct_cli 和 instinct_updater 指向不同目录 | 迁移前先统一目录，再执行迁移 |

---

## 七、路径迁移后的好处总结

| 问题 | 重构前 | 重构后 |
|------|--------|--------|
| `.claude` 目录名出现 50+ 次 | 19 个文件各写各的 | 一个常量，grep 即得全量 |
| instinct 位置不一致 | 两个模块指向不同目录 | 统一 `INSTINCT_DIR`，一个常量定义 |
| `sessions.jsonl` 散落 8+ 文件 | 每个文件自己定义字符串 | 一个 `FILE_SESSIONS` 常量 |
| 硬编码绝对路径 | `generate_skill_index.py` 换机器即坏 | 基于 `__file__` 计算 |
| Hook 源映射硬编码 | `_HOOK_SOURCE_MAP` 字典在代码里 | `paths.py` 的 `HOOK_SCRIPTS` 字典 |
| API URL 硬编码 | 两个文件各写各的 | `ANTHROPIC_API_URL` 常量 |
| 未来目录重命名 | 需改 19 个文件 | 只需改 `paths.py` 一个文件 |

### 核心收益

- **可演进性**：目录结构变更从"灾难性变更"变成"配置文件修改"
- **可测试性**：测试可以 mock `CLAUDE_PROJECT_DIR` 环境变量，用临时目录运行测试
- **可发现性**：新贡献者想知道"数据文件存在哪里"，看 `paths.py` 即可
- **可迁移性**：每次目录迁移只需改 `paths.py` 一个文件 + `git mv`

---

## 八、执行检查清单

```
[ ] Step P.1 — 创建 harness/paths.py
[ ] Step P.2 — 迁移 cli/generate_skill_index.py 使用 paths.py
[ ] Step P.3 — 迁移 evolve-daemon/*.py 使用 paths.py
[ ] Step P.4 — 迁移 hooks/bin/*.py 使用 paths.py
[ ] Step P.5 — 迁移 cli/*.py 使用 paths.py
[ ] Step P.6 — 迁移 knowledge/lifecycle.py 使用 paths.py
[ ] Step P.7 — 统一 instinct 位置（instinct_cli 和 instinct_updater 指向同一目录）
[ ] Step P.8 — grep 验证：无硬编码路径残留
[ ] Step M.1 — 备份 .gitignore
[ ] Step M.2 — 更新 .gitignore
[ ] Step M.3 — 更新 .claudeignore
[ ] Step M.4 — git mv 所有扩展目录到 harness/
[ ] Step M.5 — 更新 package.json files[]
[ ] Step V.1 — npm test
[ ] Step V.2 — Claude Code 加载验证
[ ] Step V.3 — MCP Server 启动验证
[ ] Step V.4 — Evolve Daemon 启动验证
[ ] Step V.5 — grep 验证：无遗漏的旧路径引用
```

---

## 附录 A：Grep 验证命令

```bash
# 验证根目录无旧目录残留
for dir in agents skills hooks rules memory knowledge tests docs evolve-daemon cli; do
  [ -d "$dir" ] && echo "❌ 残留目录: $dir" || echo "✅ 已迁移: $dir"
done

# 验证 harness 目录存在
for dir in agents skills hooks rules memory knowledge tests docs evolve-daemon cli; do
  [ -d "harness/$dir" ] && echo "✅ harness/$dir 存在" || echo "❌ harness/$dir 缺失"
done

# 验证旧路径无残留引用
grep -rn "'/agents/" --include="*.py" . | grep -v harness
grep -rn "'/skills/" --include="*.py" . | grep -v harness
grep -rn '"\./agents/' --include="*.py" . | grep -v harness
```

## 附录 B：Git mv 推荐操作

```bash
# 使用 git mv 保留历史
git mv agents harness/agents
git mv skills harness/skills
git mv hooks harness/hooks
git mv rules harness/rules
git mv memory harness/memory
git mv knowledge harness/knowledge
git mv tests harness/tests
git mv docs harness/docs
git mv evolve-daemon harness/evolve-daemon
git mv cli harness/cli
git mv marketplace.json harness/
git mv .mcp.json harness/
```
