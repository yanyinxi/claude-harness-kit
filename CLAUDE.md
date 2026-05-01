# CLAUDE.md

本文件为 Claude Code 提供项目上下文指导。

<!-- 由 kit init 生成于 2026-05-01 — 人工补充 TODO 项 -->

## 技术栈
- 语言/构建: Node.js / npm/yarn/pnpm

## 构建命令
```bash
npm install   # 安装依赖
npm test      # 运行测试
npm build     # 构建
```

## 关键路径
- `tests/` — 测试目录

### 入口文件
- `index.js`

### 模块
- `agents/`
- `cli/`
- `docs/`
- `evolve-daemon/`
- `hooks/`
- `instinct/`
- `knowledge/`
- `memory/`
- `rules/`
- `skills/`

## 架构约定
<!-- TODO: 补充项目架构模式、分层约定、命名规范 -->

## 已知陷阱
<!-- TODO: 补充已知的坑、历史遗留问题、易错点 -->

## 相关知识
- 项目知识: `.claude/knowledge/INDEX.md`
- 团队规范: `.claude/rules/`
- 设计文档: `docs/`