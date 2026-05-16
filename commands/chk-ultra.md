---
description: "Ultrawork 模式 — 极限并行，3-5 个 Agent 同时工作"
argument-hint: "[prompt]"
---

# Ultra Mode

极限并行模式，3-5 个 Agent 同时工作。适用于批量代码改造。

## 适用场景

- 大规模重构
- 多模块并行开发
- 时间敏感任务

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py ultra
```

之后描述要执行的任务。