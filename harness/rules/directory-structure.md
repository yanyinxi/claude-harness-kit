---
name: directory-structure
scope: global
description: 代码目录结构规范 — 定义哪些目录可以/禁止创建文件
---

# Directory Structure Rules — 目录结构契约

> **强制规范**: LLM 创建任何文件前，必须检查此规则。
> 违反以下规则的文件创建将被阻止。

## 目录结构定义

```
项目根/
├── .claude/              ❌ 禁止 LLM 创建文件（运行时数据目录）
│   ├── data/             ❌ 仅运行时写入
│   ├── proposals/        ❌ 仅运行时写入
│   └── settings.json     ❌ 配置由工具管理
│
├── harness/              ✅ 主代码目录
│   ├── _core/            ✅ 核心库
│   ├── agents/           ✅ Agent 定义
│   ├── cli/              ✅ CLI 工具
│   ├── docs/             ✅ 设计文档
│   ├── evolve-daemon/    ✅ 进化系统
│   │   ├── *.py          ✅ Python 模块
│   │   └── templates/    ✅ 模板文件
│   ├── hooks/            ✅ Hook 配置和脚本
│   │   ├── bin/          ✅ Hook 脚本
│   │   └── hooks.json    ✅ 配置
│   ├── knowledge/        ✅ 知识库
│   │   ├── decision/     ✅ ADR
│   │   ├── guideline/    ✅ 开发规范
│   │   ├── pitfall/      ✅ 已知陷阱
│   │   ├── process/      ✅ 操作流程
│   │   ├── model/        ✅ 数据模型
│   │   └── evolved/      ✅ 进化生成知识
│   ├── memory/           ✅ 记忆系统（v3.0 合并）
│   │   ├── instinct-record.json  ✅ 本能记录
│   │   ├── feedback_*.md          ✅ 用户反馈
│   │   └── reference_*.md         ✅ 参考文档
│   ├── rules/            ✅ 团队规范
│   ├── skills/           ✅ Skill 定义
│   ├── tests/            ✅ 测试套件
│   └── paths.py          ✅ 路径常量定义
│
├── memory/               ❌ 项目根禁止 memory/（应在 harness/ 下）
│
├── tests/                 ❌ 项目根禁止 tests/（应在 harness/ 下）
│
├── docs/                 ✅ 项目文档（独立于 harness/）
│
└── 其他目录              ⚠️ 创建前需确认
```

## 关键规则

### 1. 本能记录文件位置（CRITICAL）

| 文件 | 正确位置 | 错误位置 |
|------|----------|----------|
| instinct-record.json | `harness/memory/instinct-record.json` | `memory/instinct-record.json` |

**原因**: CLAUDE.md 明确规定记忆系统在 `harness/memory/` 下。
项目根的 `memory/` 是历史遗留/错误创建。

### 2. 路径获取规范

所有 Python 模块应使用统一路径函数：

```python
# ✅ 正确：从 _find_root.py 导入
from harness._find_root import get_instinct_path, get_memory_dir

# ✅ 正确：从 kb_shared.py 导入常量
from harness.evolve_daemon.kb_shared import INSTINCT_PATH

# ❌ 错误：硬编码路径
path = Path("memory/instinct-record.json")
path = Path("/Users/xxx/...")

# ❌ 错误：使用项目根 memory/
path = find_root() / "memory" / "instinct-record.json"  # 少了 "harness"
```

### 3. 禁止创建的位置

| 目录 | 原因 | 替代方案 |
|------|------|----------|
| `.claude/` | 运行时数据，仅工具写入 | 无 |
| 项目根 `memory/` | 应在 `harness/memory/` | 使用 `_find_root.py` 路径 |
| `hooks/` (项目根) | 应使用 `harness/hooks/` | 通过 hooks.json 配置 |
| `node_modules/` | 依赖目录 | npm install |
| `__pycache__/` | Python 缓存 | .gitignore |

### 4. 允许创建的位置

| 目录 | 条件 |
|------|------|
| `harness/*/` | 已有白名单子目录内 |
| `docs/` | 项目文档 | 
| `.claude/data/` | 运行时数据（通过工具） |

## 违反检测

```bash
# 检查项目根是否有 memory/ 目录
ls -la memory/ 2>/dev/null && echo "❌ 项目根 memory/ 应迁移到 harness/memory/"

# 检查 .claude/ 下是否有代码文件
find .claude -name "*.py" -o -name "*.js" | grep -v "settings.json" && echo "❌ .claude/ 仅允许数据文件"
```

## 违规处理

1. **创建前**: 检查目标目录是否在白名单内
2. **创建后发现**: 迁移到正确位置，更新路径引用
3. **持续违规**: 触发本能记录，降低置信度

## 历史遗留问题

以下文件需要迁移：

| 错误位置 | 正确位置 | 状态 |
|----------|----------|------|
| `memory/instinct-record.json` | `harness/memory/instinct-record.json` | ✅ 已修复 |
| `tests/` (项目根) | `harness/tests/` | ⚠️ 尚未迁移 |

**重要**: 项目根 `tests/` 目录仅作规范说明，实际存在待清理。

---

**最后更新**: 2026-05-10
**维护者**: CHK Team