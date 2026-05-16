---
description: "知识垃圾回收 — 扫描 .claude/knowledge/ 生成漂移报告"
---

# CHK GC

知识垃圾回收，扫描 .claude/knowledge/ 目录，生成漂移和过时内容报告。

## 功能

1. 扫描知识库目录
2. 识别过时内容
3. 检测漂移
4. 生成清理建议

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/gc.py
```