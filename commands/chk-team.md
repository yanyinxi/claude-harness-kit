---
description: "Team 模式 — 默认模式，5 阶段流程（功能开发）"
argument-hint: "[prompt]"
---

# Team Mode

多 Agent 协作开发模式，5 阶段流程。适用于日常功能开发。

## 阶段流程

1. **需求分析** — 理解需求，拆解任务
2. **架构设计** — 制定技术方案
3. **并行开发** — 多 Agent 同时工作
4. **代码审查** — 质量检查
5. **集成测试** — 验证功能

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py team
```

之后描述要开发的功能。