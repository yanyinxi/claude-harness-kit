---
name: change-tracking
description: 变更追踪 — 需求变更→代码变更的全流程留痕管理
trigger: "变更|changes|追溯|追踪|回滚|版本"
---

# Change Tracking Skill — 变更追踪管理

## 1. 触发场景

当用户提到以下关键词时激活：
- "变更"、"changes"、"追溯"、"追踪"
- "回滚"、"rollback"
- "版本"、"version history"
- "需求变更"、"代码变更"

## 2. 变更级别评估

### 快速评估矩阵

| 条件 | 级别 |
|------|------|
| 1-2 文件修改，无核心模块 | L0 |
| 3-5 文件修改 | L1 |
| 5+ 文件 OR 核心模块变更 | L2 |
| 架构/多模块/接口签名变更 | L3 |

### 触发规则

```
L0: 可直接提交
L1: 创建 CHANGE.md
L2: 创建 CHANGE.md + review-001.md
L3: 创建完整 CHANGES 目录 + 架构评审
```

## 3. 变更记录创建流程

### Step 1: 评估变更级别

```
分析用户需求 → 确定变更类型 → 评估影响范围
```

### Step 2: 创建变更目录

```bash
# 格式: harness/changes/YYYY-MM-DD-[short-desc]
mkdir -p "harness/changes/$(date +%Y-%m-%d)-[ticket-id]"
```

### Step 3: 生成 CHANGE.md

```markdown
# 变更记录: [ticket-id]

## 元信息
- 创建时间: $(date "+%Y-%m-%d %H:%M")
- 变更级别: L1/L2/L3
- 负责人: [用户名]

## 变更内容
[用户描述的变更需求]

## 影响范围
- 模块: [受影响的模块]
- 文件: [文件列表]

## 评审记录
review-001.md, review-002.md... (版本递增)

## 回滚方案
[如何回滚]

## 验证清单
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动验证完成
```

### Step 4: 关联评审

对于 L2+ 变更：
1. 创建 `review-001.md`
2. 提交 code-reviewer 评审
3. 根据反馈创建 `review-002.md`
4. 循环直到通过

### Step 5: 代码实现

遵循变更记录中定义的验证清单

### Step 6: 验证与合并

1. 运行测试验证
2. 更新 CHANGE.md（标记完成）
3. 合并分支

## 4. 回滚流程

### 触发条件
- 上线后发现严重 Bug
- 变更导致系统不稳定
- 回滚窗口内发现预期外行为

### 回滚步骤

```bash
# 1. 识别回滚版本
git log --oneline -10

# 2. 读取 rollback.md
cat harness/changes/[ticket-id]/rollback.md

# 3. 执行回滚
git revert [commit-hash]

# 4. 验证
[运行验证检查]

# 5. 更新 CHANGES 记录
# 在 rollback.md 中记录实际回滚情况
```

### 回滚后处理

1. 创建新的 CHANGES 记录（回滚修复）
2. 分析根因
3. 更新知识库（pitfall）
4. 复盘改进

## 5. 变更分析工具

### 影响范围分析

```python
# 使用 git diff 分析变更影响
def analyze_change_impact(files: list[str]) -> dict:
    """分析变更影响范围"""
    impact = {
        "core_modules": [],  # 核心模块
        "api_breaking": False,  # API 破坏性变更
        "schema_change": False,  # Schema 变更
        "config_change": False,  # 配置变更
    }

    for f in files:
        if any(x in f for x in ["auth", "payment", "security"]):
            impact["core_modules"].append(f)
        if "schema" in f or "migration" in f:
            impact["schema_change"] = True

    return impact
```

### 变更趋势分析

定期检查：
- 高频变更的文件（可能是耦合问题）
- 变更回滚率（质量指标）
- 变更平均修复时间

## 6. 与其他 Skill 的协同

### git-master
- 变更记录检查（变更前）
- 变更后自动创建 CHANGES 目录

### code-reviewer
- L2+ 变更必须触发评审
- 评审结果写入 review-N.md

### ship
- 发布前验证 CHANGES 完整性
- 检查所有 checklist 完成

### tdd
- 变更前先写测试
- 变更后验证测试覆盖

## 7. 最佳实践

### Do
- 变更前先评估级别
- L2+ 变更必须创建完整记录
- 回滚后更新知识库（避免同类问题）
- 定期回顾变更记录，优化流程

### Don't
- 禁止无记录直接提交 L2+ 变更
- 禁止删除 CHANGES 历史记录
- 禁止跳过评审流程