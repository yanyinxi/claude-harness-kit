---
name: checkpoint
description: 任务状态快照管理命令，支持保存、列出、恢复、对比和删除检查点。在上下文压缩（/compact）前或阶段切换时使用，防止工作进度丢失。
user-invocable: true
---

# /checkpoint — 任务状态快照管理

## 概述

/checkpoint 管理任务状态快照，用于：
- `/compact` 前保存进度
- 阶段切换时保存中间状态
- 恢复到之前的工作点
- 对比不同版本的差异

## 子命令

### /checkpoint save [name]

保存当前任务状态到检查点文件。

```
/checkpoint save
/checkpoint save feature-auth   # 自定义名称
```

**保存内容：**
- 最近 10 轮对话摘要
- 打开的文件列表及修改位置
- 当前 TodoList 状态
- CLAUDE.md 中记录的进度（checkbox 格式）

**输出文件：** `.claude/checkpoints/<name>-<timestamp>.json`

### /checkpoint list

列出所有检查点。

```
/checkpoint list
```

**输出示例：**
```
检查点列表 (.claude/checkpoints/):

  [P0-TASK-001] feature-auth-20260501-143022  5 分钟前
  [P0-TASK-002] feature-auth-20260501-142800  25 分钟前
```

### /checkpoint restore <name>

恢复到指定检查点。

```
/checkpoint restore feature-auth-20260501-143022
```

**流程：**
1. 读取检查点 JSON
2. 恢复 TodoList 状态
3. 输出摘要供人工确认
4. 提示用户重新读取关键文件

### /checkpoint diff <name-a> <name-b>

对比两个检查点的差异。

```
/checkpoint diff feature-auth-20260501-143022 feature-auth-20260501-142800
```

**输出：** 变更摘要（新增文件、删除文件、进度差异）

### /checkpoint delete <name>

删除指定检查点。

```
/checkpoint delete feature-auth-20260501-142800
```

### /checkpoint auto-save [on|off]

开关自动保存模式。开启后，每次 `/compact` 时自动保存检查点。

```
/checkpoint auto-save on
/checkpoint auto-save off
/checkpoint auto-save status
```

## 实现细节

**存储位置：** `.claude/checkpoints/`
**文件格式：** JSON，包含：
- `timestamp`: ISO 8601 时间戳
- `name`: 检查点名称
- `conversation_summary`: 最后 N 轮摘要
- `open_files`: 文件列表
- `todo_state`: TodoWrite 快照
- `checkpoint_note`: 用户备注（可选）

**自动触发：** `hooks/bin/checkpoint-auto-save.sh` 在检测到 `/compact` 时自动保存

## 示例工作流

```
# 开始功能开发
> /checkpoint save feature-user-auth

# ... 做了很多工作 ...

# 上下文快满时
> /compact
  → 自动保存检查点

# 继续工作，发现走错方向
> /checkpoint list
  → 找到之前的检查点

> /checkpoint restore feature-user-auth
  → 恢复到之前状态
```

## 与 /compact 的关系

- `/compact` 触发上下文压缩
- 自动执行 `/checkpoint save`（如果 auto-save 开启）
- 恢复后需要重新读取检查点中的文件路径

## Red Flags

- 没有保存检查点就执行 `/compact`
- 检查点文件已损坏（JSON 无效）
- 恢复到过旧的检查点（与当前代码不同步）