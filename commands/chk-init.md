---
description: "分析当前项目，生成 CLAUDE.md + .claude/ 配置"
argument-hint: "[project-path]"
---

# CHK Init

分析当前项目，生成高质量 CLAUDE.md 和 .claude/ 配置。

## 功能

1. 扫描项目结构，识别技术栈 + 版本号
2. 发现关键目录和入口文件
3. 从 git log 提取常见模式和陷阱
4. 生成 Map Not Manual 风格 CLAUDE.md（<100 行）
5. 创建 .claude/ 目录骨架

## 执行

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/harness/cli/init.py "$ARGUMENTS"
```

如果未指定路径，使用当前目录。