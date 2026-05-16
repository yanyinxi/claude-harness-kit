---
description: "Ralph 模式 — TDD 强制，不通过不停止"
argument-hint: "[prompt]"
---

# Ralph Mode

Ralph TDD 强制模式，实现代码必须先有测试，不通过不停止。

## 适用场景

- 支付/安全关键代码
- 需要高测试覆盖率
- TDD 实践

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/mode.py ralph
```

之后描述要 TDD 开发的功能。