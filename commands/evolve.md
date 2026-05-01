---
name: evolve
description: >
  本能进化系统管理命令。查看本能状态、确认/拒绝提案、
  导出导入本能记录、触发进化分析。
  触发词：/evolve、evolve、本能、instinct、进化
user-invocable: true
---

# /evolve — 本能进化系统管理

## 概述

`/evolve` 是本能系统的用户交互界面，让用户可以：
- 查看积累的本能记录和置信度分布
- 确认或拒绝本能提案
- 导出/导入本能到其他项目
- 触发进化分析（聚类 → 建议创建 Skill）

## 子命令

### /evolve status

显示本能系统当前状态。

```
/evolve status
/evolve status --domain testing    # 按领域过滤
```

**输出示例**：
```
🦁 Instinct System — 12 records
   🟢 AUTO (≥0.9):      3  (已验证本能)
   🟡 PROPOSAL (≥0.5): 6  (提案本能)
   🔴 OBSERVE (<0.5):   3  (观测本能)

📂 Domain breakdown:

  🔧 TESTING (4 records)
    ██████████ 0.95 🟢 已验证本能 — mock axios in tests
    ████████░░ 0.85 🟡 提案本能  — use userEvent over fireEvent
    █████░░░░░ 0.50 🔴 观测本能  — skip shallow rendering

  🔒 SECURITY (2 records)
    ██████████ 0.98 🟢 已验证本能 — validate JWT expiration
    ███████░░░ 0.70 🟡 提案本能  — check CORS origin

  📦 API (3 records)
    ██████████ 0.92 🟢 已验证本能 — paginate list endpoints
    ████░░░░░░ 0.40 🔴 观测本能  — retry with exponential backoff
    █████░░░░░ 0.50 🔴 观测本能  — cache GET responses
```

### /evolve list

按领域列出本能。

```
/evolve list
/evolve list --domain testing      # 只显示 testing 领域
/evolve list --min-confidence 0.7  # 只显示 ≥0.7 置信度的
```

### /evolve confirm \<proposal-id\>

确认本能提案，将置信度提升到 0.9（已验证）。

```
/evolve confirm abc123
evolve confirm abc123 --domain security  # 同时标记领域
```

**效果**：
- 置信度从 0.3-0.9 提升到 0.9
- 状态从 PROPOSAL → AUTO
- meta.updated 时间戳更新

### /evolve reject \<proposal-id\>

拒绝本能提案，降低置信度。

```
/evolve reject abc123
evolve reject abc123 --reason "too specific to this codebase"
```

**效果**：
- 置信度降低 0.2
- 若置信度 < 0.1，从记录中移除
- 可选记录拒绝原因到进化日志

### /evolve export

导出本能记录到可分享文件。

```
/evolve export                          # 导出全部（markdown）
/evolve export --format json           # JSON 格式
/evolve export --min-confidence 0.7   # 只导出已验证的
/evolve export --project my-team        # 添加项目标识
```

**输出文件**：`.claude/evolve/export-<timestamp>.json`

### /evolve import \<file\>

从文件导入本能记录。

```
/evolve import .claude/evolve/export-20260501.json
```

**导入规则**：
- 跳过已存在的 ID（按本能 ID 去重）
- 追加新记录
- 显示导入统计

### /evolve evolve [--dry-run]

触发进化分析（聚类 + 置信度升级）。

```
/evolve evolve                    # 执行进化
/evolve evolve --dry-run         # 仅预览，不修改
```

**进化分析逻辑**：

1. **聚类分析**：同一领域 ≥2 条本能 → 建议创建 Skill
2. **置信度升级**：eval_count ≥3 且置信度 <0.9 → +0.1
3. **自然衰减**：last_triggered 超过 30 天无触发 → -0.05

**Dry Run 输出示例**：
```
🔬 Instinct Evolution — Dry Run

Analyzing 12 instincts across 4 domains...

📊 Confidence upgrades (eval_count ≥3):
  • mock axios in tests: 0.70 → 0.80 🟡→🟡
  • validate JWT: 0.85 → 0.95 🟡→🟢 (will be AUTO!)

🎯 Skill creation proposals:
  • TESTING domain: 4 records, avg_conf=0.80
    → CREATE_SKILL: testing-best-practices (PROPOSED)
  • SECURITY domain: 2 records, avg_conf=0.84
    → CREATE_SKILL: security-patterns (PROPOSED)

⚠️ Natural decay (30d inactive):
  • skip shallow rendering: 0.50 → 0.45 🔴

Run /evolve evolve to apply these changes.
```

## 本能生命周期

```
OBSERVE (0.0-0.5)
    ↓ eval_count ≥ 1，置信度提升
PROPOSAL (0.5-0.9)
    ↓ eval_count ≥ 3 或用户 confirm
AUTO (0.9-1.0)
    ↓ 30 天无触发
自然衰减 → PROPOSAL
```

## 置信度演化规则

| 触发事件 | 置信度变化 |
|---------|---------|
| eval_count += 1 | +0.1（最高 0.9） |
| 用户 confirm | 直接设为 0.9 |
| 用户 reject | -0.2（最低移除） |
| 30 天无触发 | -0.05（最低 0.1） |
| 本能被用于 Skill 创建 | 标记为 "superseded" |

## 与 instinct-record.json 的关系

本能记录存储在 `agents/instinct/instinct-record.json`：

```json
{
  "records": [
    {
      "id": "abc123",
      "domain": "testing",
      "trigger": "mock axios in tests",
      "pattern": "jest.mock('axios')",
      "confidence": 0.85,
      "eval_count": 2,
      "created": "2026-05-01T00:00:00Z",
      "last_triggered": "2026-05-01T12:00:00Z",
      "source": "continuous-learning"
    }
  ],
  "meta": {
    "version": "1.0",
    "updated": "2026-05-01T12:00:00Z"
  }
}
```

## 使用场景

```
# 新项目初始化
> /evolve import team-instincts.json
  → 导入团队级本能

# 开发过程中
> /evolve confirm abc123
  → 确认一个有效的本能

# 会话结束时
> /evolve evolve --dry-run
  → 预览进化建议

# 长期使用
> /evolve status
  → 查看积累效果
```

## Red Flags

- 从不运行 `/evolve confirm`
- 从不运行 `/evolve evolve`
- 本能记录超过 100 条但无一条达到 AUTO 级别
- 导入本能但不审查