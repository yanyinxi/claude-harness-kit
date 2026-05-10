---
name: changes
scope: global
description: 变更追踪协议 — 需求变更→代码变更的全流程留痕
---

# Changes Management — 变更追踪协议

## 1. 变更分类

| 级别 | 说明 | 影响范围 | 评审要求 |
|------|------|----------|----------|
| L0 | 文本/注释/文档变更 | 无代码影响 | 可直接提交 |
| L1 | 单文件/单模块修改 | 微小风险 | 自我评审 |
| L2 | 多模块/接口变更 | 中等风险 | 同行评审 |
| L3 | 架构/核心逻辑变更 | 高风险 | 团队评审 |

## 2. 变更检测触发条件

以下情况**必须**创建 CHANGES 记录：
- 一次性修改 **5+ 文件**
- 涉及核心模块：`auth/`、`payment/`、`security/`、`database/`
- API 接口签名变更（请求/响应结构）
- 数据库 Schema 变更（DDL）
- 配置文件格式变更（影响运行时行为）
- 依赖版本变更（package.json/requirements.txt）

## 3. 变更记录格式

每个需求变更在 `harness/changes/` 下创建独立目录：

```
harness/changes/
└── YYYY-MM-DD-[short-desc]/
    ├── CHANGE.md          # 变更描述
    ├── review-001.md      # 评审记录（版本递增）
    ├── code-diff.md       # 代码变更摘要
    └── rollback.md        # 回滚方案
```

### CHANGE.md 模板

```markdown
# 变更记录: [简短描述]

## 变更类型
- 级别: L1/L2/L3
- 影响范围: [具体模块]

## 变更原因
[为什么需要这个变更]

## 涉及文件
- [文件列表]

## 回滚方案
[如何回滚]

## 验证方式
[如何验证变更正确]
```

## 4. 变更流程

```
需求提出 → 评估级别 → 创建 CHANGE.md → 评审 → 代码实现 → 验证 → 合并
```

### L0: 直接提交
```
git commit -m "docs: 更新 README"
```

### L1: 自我评审
```
harness/changes/YYYY-MM-DD-ticket-001/CHANGE.md 创建
git commit 后自检
```

### L2: 同行评审
```
1. 创建 CHANGE.md + review-001.md
2. 关联 PR Reviewer
3. review-002.md, review-003.md 递增
4. 评审通过后合并
```

### L3: 团队评审
```
1. 完整 CHANGES 目录创建
2. 架构评审会议
3. 代码评审（Claude Code）
4. 回滚演练
5. 上线后 24h 监控
```

## 5. 反模式（禁止）

| 禁止 | 正确做法 |
|------|----------|
| 无记录直接提交 | CHANGES 记录先行 |
| 跨越大版本直接修改 | 走变更评审流程 |
| 不测试直接上线 | CI 检查 + 手动验证 |
| 变更后不更新知识库 | 更新对应 knowledge 条目 |
| 删除 CHANGES 目录 | 保留作为历史参考 |

## 6. 关联机制

### 与 Git 工作流关联
- 分支命名: `changes/YYYY-MM-DD-short-desc`
- Commit 消息: 引用 CHANGE.md 编号

### 与 Skills 关联
- `git-master` Skill: 变更记录检查
- `code-reviewer` Agent: L2+ 变更必须评审
- `ship` Skill: 发布前验证 CHANGES 完整性

### 与 Hooks 关联
- `git-commit-check.sh`: 检测变更文件数量超阈值时触发
- `quality-gate.sh`: 检测核心模块变更时增强检查