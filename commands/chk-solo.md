---
description: "Solo 模式 — 直接对话，不用 Agent，零开销"
argument-hint: "[prompt]"
---

# Solo Mode

直接对话模式，无需 Agent 介入。适用于简单问答和快速修改。

## 使用场景

- 简单问答
- 小改动
- 快速查看/解释代码

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py solo
```

之后可以追加 prompt 参数进行对话。