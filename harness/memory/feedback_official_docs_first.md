---
name: feedback_official_docs_first
description: 遇到复杂问题必须联网搜索官方文档，不能自己瞎想，一切遵循 Claude Code 官方规范，避免重复造轮子
metadata:
  type: feedback
  priority: high
  tags: [开发规范, 官方文档, Claude Code]
---

# 官方文档优先原则

**规则**：遇到复杂问题必须联网搜索 Claude Code 官方文档，不能自己瞎想

**Why**：之前设计 hooks.json 时自己假设了 async/optional 参数，但 Claude Code 官方可能不支持，导致方案不可行。

**How to apply**：
1. 遇到 Hook 配置、插件开发、Agent/Skill 设计等问题
2. 先搜索 Claude Code 官方文档（docs.anthropic.com）
3. 确认官方支持后再实现
4. 避免重复造轮子，优先使用官方方案

**官方文档入口**：
- https://code.claude.com/docs/zh-CN/goal
- https://code.claude.com/docs/zh-CN/best-practices
- https://code.claude.com/docs/zh-CN/agents
- https://docs.anthropic.com/zh-CN/docs/claude-code/overview
- https://docs.anthropic.com/zh-CN/docs/claude-code/hooks
- https://code.claude.com/docs/zh-CN/hooks-guide
- https://docs.anthropic.com/zh-CN/docs/claude-code/plugins
- https://code.claude.com/docs/zh-CN/worktrees
- https://code.claude.com/docs/zh-CN/whats-new
- https://code.claude.com/docs/zh-CN/cli-reference
- https://code.claude.com/docs/zh-CN/settings
- https://code.claude.com/docs/zh-CN/admin-setup

**已知官方特性**：
- Hook matcher 支持: Bash, Write, Edit, Read, Grep, NotTools, WebFetch, WebSearch, AskUserQuestion, Agent, TaskCreate, TaskGet, TaskList, TaskUpdate, ExitPlanMode
- Hook timeout 参数支持
- 暂不确定 async/optional 是否官方支持（需验证）