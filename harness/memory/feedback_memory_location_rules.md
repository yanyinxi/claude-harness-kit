---
name: feedback_memory_location_rules
description: 记忆文件存放位置规则：项目记忆放 harness/memory/，跨项目记忆放 .claude/projects/.../memory/
type: feedback
---

# 记忆文件存放位置规则

## 问题
多次出现记忆文件放错目录的情况：项目相关的记忆放到了 `.claude/` 全局目录，而不是 `harness/memory/` 项目目录。

## 原因
混淆了两个不同的记忆位置：
1. `.claude/projects/<hash>/memory/` — Claude Code 全局记忆（跨项目通用）
2. `harness/memory/` — CHK 项目本地记忆（仅本项目）

## 存放规则

### 放 harness/memory/ 的内容
- 项目特有的知识、经验、决策
- 只与当前项目相关的反馈记录
- CHK 特有的规范、陷阱、模式

### 放 .claude/projects/<hash>/memory/ 的内容
- 跨项目通用规则
- Claude Code 全局使用习惯
- 与特定项目无关的通用知识

## 验证清单

写记忆文件前必须确认：
1. [ ] 这个知识是项目特有的还是通用的？
2. [ ] 路径是否在项目目录 `/Users/yanyinxi/工作/code/github/claude-harness-kit/` 下？
3. [ ] 如果在项目下，应该放 `harness/memory/`，而不是 `.claude/`

## 快速判断

```
这个记忆只跟 CHK 项目有关吗？
  → 是 → harness/memory/<name>.md
  → 否 → .claude/projects/<hash>/memory/<name>.md
```

## 为什么这样设计

- `harness/memory/` 是版本控制的，项目成员共享
- `.claude/` 是本地配置，不应包含项目特定内容
- 项目知识应该随项目走，而不是随用户走

## 历史教训

- 2026-05-09：创建了 `chk-plugin-specification-fixes.md` 到错误位置
- 解决方案：立即移动到 `harness/memory/`