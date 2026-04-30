---
scope: global
---

# Multi-Agent Collaboration Protocol — 多 Agent 协作契约

## 1. 并行执行铁律

### 1.1 并行条件

| 场景 | 可否并行 | 条件 |
|------|:--:|------|
| 探索/分析多个维度 | ✅ | 只看不写 |
| 修改不同文件 | ✅ | 文件集不重叠 |
| 不同审查维度 | ✅ | 独立审查 |
| 修改同一文件 | ❌ | 合并为同一任务 |
| 有依赖的任务 | ❌ | 先完成依赖方 |
| 审查和修复 | ❌ | 先审查完再修复 |

### 1.2 冲突检测（派发并行 Agent 前必须执行）

派发前先列出每个 Agent 将修改的文件，检查重叠：

```
任务 A: files=[a.java, b.java]
任务 B: files=[c.vue, d.vue]
→ A ∩ B = ∅ → 可并行
```

如果文件重叠 → 合并任务或串行化。

### 1.3 并行分析 / 串行修复

```
✅ 正确: explore + codebase-analyzer + impact-analyzer 并行
         → 汇总结果
         → 按依赖顺序串行修复

❌ 错误: 把所有 Agent 都并行，不考虑依赖
```

## 2. 信息同步协议

### 2.1 文件交接制 — 不依赖上下文传递状态

每个阶段的产出写入文件，下一阶段读取文件：

```
[分析阶段] → research/summary.md
[设计阶段] → plan/architecture.md
[实现阶段] → output/task_*.md
[审查阶段] → review/report.md
```

**规则**: 跨阶段状态**必须**写入文件。上下文可能被压缩，文件不会丢失。

### 2.2 Mailbox — Agent 间通信

并行 Agent 之间发现需要协同的信息，写入 mailbox/ 目录：

```
mailbox/to_frontend.md  ← backend-dev 通知 API 字段变更
mailbox/to_backend.md   ← frontend-dev 通知需要新接口
```

**协议**:
- Agent 启动时先读 mailbox/ 检查是否有给自己的消息
- Agent 发现需要通知其他 Agent 时写 mailbox/
- 消息格式: 时间 + 来源 + 内容 + 影响范围
- 消息状态: unread → read → resolved

### 2.3 Checkpoint — 压缩安全

每完成一个阶段，写入 checkpoint:

```
.compact/
├── current_phase.md     # "Phase 3: Implement, Task 2/4"
├── completed.md         # - [x] Task 1: xxx
├── pending.md           # - [ ] Task 3: xxx
└── recovery.md          # 如何从当前状态恢复
```

`/compact` 后，从 checkpoint 文件恢复进度。

## 3. 并行模式库

### 模式 1: 三路并行分析（研究文档 92% 缓存最优）

```
同一 response 同时发出:
  Agent(explore, "搜索相关代码和调用链", background)
  Agent(codebase-analyzer, "分析模块结构", background)
  Agent(impact-analyzer, "评估影响范围", background)
→ 所有 Agent 继承相同缓存前缀 → 92% 复用率
```

### 模式 2: 前后端并行开发（需契约前置）

```
Step 1 (串行): architect 定义 API 契约 → api-contract.md
Step 2 (并行): backend-dev + frontend-dev 同时实现
  两端都以 api-contract.md 为准
  后端: 返回字段 = contract 定义的字段名 + camelCase
  前端: 不使用 ?? fallback 写法（那说明契约断了）
```

### 模式 3: 多角度并行审查

```
同一 response 同时发出:
  Agent(code-reviewer, "5 维度审查", background)
  Agent(qa-tester, "测试覆盖审查", background)
  Agent(security-auditor, "安全审查", background)  ← 仅安全相关
→ 汇总 3 份报告 → 差异项人工判断
```

### 模式 4: Ralph 自修复循环

```
Agent(ralph, "实现 + 测试 → 失败 → 修复 → 重测", background=false)
最多 5 轮自动修复
```

## 4. 错误处理

### 4.1 Agent 失败

```
Agent 返回 error → 
  工具失败 → 重试 1 次（换参数）
  超时 → 拆分任务
  逻辑错误 → 根因分析 → 修复 → 重新派发
  连续 3 次失败 → 人工介入
```

### 4.2 并行 Agent 部分失败

```
Task A ✅, Task B ❌, Task C ✅
  → 保留 A、C 的产出
  → 修复 B 的根因
  → 仅重派 B
  → 全部通过 → 继续
```

## 5. Anti-Patterns（禁止）

| 禁止 | 原因 | 正确做法 |
|------|------|---------|
| 有依赖的任务并行 | 重复工作 | 串行化依赖 |
| 改同一文件的 Agent 并行 | 冲突 | 合并或串行 |
| 上下文依赖记忆传递状态 | 压缩丢失 | 状态写入文件 |
| 无契约前后端并行 | 字段不一致 | 先定契约再并行 |
| 审查和修复同时进行 | 修复基础不稳 | 先审查完再修复 |
| 不设超时等待 | 无限等待 | 每个 Agent 给预估时间 |
