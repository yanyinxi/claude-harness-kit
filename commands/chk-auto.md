---
description: "Autopilot 模式 — 全自动端到端，5 分钟搞定 Bug"
argument-hint: "[prompt]"
---

# Auto Mode

Autopilot 模式，全自动修复 Bug，零干预。

## 适用场景

- 线上 Bug 需要快速修复
- 已知问题，根因明确
- 小改动，不需要设计评审

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py auto
```

之后描述要修复的问题。