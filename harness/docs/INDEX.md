# CHK 文档索引

## 一、架构设计

| 文件 | 说明 |
|------|------|
| `architecture-v2.md` | CHK 架构设计 v2 |
| `evolve-daemon-design.md` | 自动进化守护进程设计 |
| `restructure-plan.md` | 目录重构计划 |

## 二、功能设计

| 文件 | 说明 |
|------|------|
| `auto-evolve-v2-design.md` | 自动进化 v2 设计 |
| `memory-evolution-integration.md` | 记忆系统与进化系统整合方案 |
| `directory-structure-and-migration-plan.md` | 目录结构与迁移计划 |

## 三、研究文档

| 文件 | 说明 |
|------|------|
| `research-claude-code-internals.md` | Claude Code 内部机制研究 |
| `test-report-v0.9.1.md` | v0.9.1 测试报告 |

---

## 记忆系统与进化系统整合

详见 `memory-evolution-integration.md`

### 核心组件

| 组件 | 文件 |
|------|------|
| 本能读取 | `harness/_core/instinct_reader.py` |
| 本能状态 | `harness/_core/instinct_state.py` |
| 关键词匹配 | `harness/_core/keyword_matcher.py` |
| 记忆注入 | `hooks/bin/memory-inject.sh` |
| 知识同步 | `harness/evolve-daemon/memory_sync.py` |
| 状态清理 | `hooks/bin/memory-cleanup.sh` |

### 数据流

```
用户工作 → 进化系统分析 → 知识固化 → 同步到 MEMORY.md
    ↓                                        ↓
observe.sh 捕获 ──→ instinct-record.json ──→ memory-inject 注入
    ↓                                              ↓
用户感知"✓已记录"                              AI 上下文
```