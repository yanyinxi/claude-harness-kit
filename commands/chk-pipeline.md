---
description: "Pipeline 模式 — 严格阶段顺序，上一步输出喂下一步"
argument-hint: "[prompt]"
---

# Pipeline Mode

严格阶段顺序模式，上一步输出喂下一步。适用于数据库迁移等需要严格顺序的场景。

## 适用场景

- 数据库迁移
- 依赖链式任务
- 逐步验证流程

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py pipeline
```

之后描述要执行的 pipeline 任务。