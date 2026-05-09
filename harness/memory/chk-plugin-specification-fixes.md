---
name: chk-plugin-specification-fixes
description: CHK 插件规范修复记录：hooks.json扁平化、Agent添加id、Rule添加name、清理非标准字段
type: project
originSessionId: 228b2daa-751a-42da-a4cf-6f555913678c
---
# CHK 插件规范修复记录 (2026-05-09)

## 背景

通过对比 Claude Code 官方插件规范，发现 CHK 项目存在多个结构性问题，已全部修复。

## 已修复问题

### 1. Hooks.json 结构错误 (P0)
- **问题**: 使用了多余的嵌套层级 `{ "hooks": { "Event": [{ "hooks": [...] }] } }`
- **修复**: 改为扁平结构 `{ "hooks": { "Event": [{ "type": "command", ... }] } }`
- **文件**: `harness/hooks/hooks.json`

### 2. Agent 缺少 id 字段 (P0)
- **问题**: Agent 文件缺少完整的插件内 ID
- **修复**: 为所有 22 个 Agent 添加 `id: claude-harness-kit:<agent-name>`
- **文件**: `harness/agents/*.md`

### 3. Rule 缺少 name 字段 (P0)
- **问题**: Rule 文件 YAML frontmatter 缺少 `name` 字段
- **修复**: 为所有 6 个 Rule 添加 `name` 字段（与文件名一致）
- **文件**: `harness/rules/*.md`

### 4. SKILL.md 非标准字段清理 (P1)
- **问题**: SKILL.md 包含非 Claude Code 标准字段
- **修复**: 移除以下字段：
  - `disable-model-invocation`
  - `user-invocable`
  - `allowed-tools`
  - `context`
  - `agent`
- **文件**: `harness/skills/*/SKILL.md`

## 验证结果
- 所有 183 个测试通过
- shellcheck 检查通过
- ruff 静态分析通过

## 规范要点

### Agent 文件结构
```yaml
---
id: claude-harness-kit:<agent-name>  # 完整ID
name: <agent-name>
description: ...
tools: [Read, Write, ...]
disallowed-tools: [...]
model: sonnet
permissionMode: default
context: main|fork
---
```

### Rule 文件结构
```yaml
---
name: <rule-name>      # 必须，与文件名一致
scope: global|project
---
```

### Hooks.json 结构
```json
{
  "hooks": {
    "EventName": [
      { "matcher": "ToolName", "type": "command", "command": "...", "timeout": 5 }
    ]
  }
}
```

## 重要提醒
下次遇到插件规范相关问题，优先检查：
1. Hooks.json 是否扁平结构
2. Agent 是否包含完整 id
3. Rule 是否包含 name
4. SKILL.md 是否包含非标准字段