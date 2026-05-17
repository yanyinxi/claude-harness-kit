# CHK 测试架构落地执行计划

> **版本**: v1.0
> **日期**: 2026-05-17
> **目标**: Bug逃逸率 <2%，测试覆盖率 95%，稳定性 98%

---

## 零、测试配置文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `pytest.ini` | pytest 配置 | 测试路径、标记、选项 |
| `.coveragerc` | 覆盖率配置 | 源码目录、排除项、报告格式 |
| `package.json` | npm 脚本 | 测试命令快捷入口 |

**配置文件说明**:

```ini
# pytest.ini
[pytest]
testpaths = harness/tests
addopts = -v --tb=short --strict-markers
```

```ini
# .coveragerc
[run]
source = harness
branch = True
omit = */tests/* */__pycache__/*

[report]
show_missing = True
precision = 2
```

**提交到 git**: 是，这些是项目标准配置，确保本地和 CI/CD 一致。

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CHK 测试质量体系                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │  测试分层   │    │  CI/CD流水线 │    │  监控体系   │                 │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤                 │
│  │ Unit (50%)  │    │   GitHub     │    │  错误监控   │                 │
│  │ Integration │───▶│  Actions    │───▶│  生产环境   │                 │
│  │ Contract    │    │  workflows  │    │  + 灰度发布 │                 │
│  │ E2E (10%)   │    │             │    │             │                 │
│  └─────────────┘    └─────────────┘    └─────────────┘                 │
│         │                  │                   │                        │
│         ▼                  ▼                   ▼                        │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    三层强制执行机制                         │       │
│  │  Layer 1: CLAUDE.md 文档层  →  Layer 2: Hooks自动化  →  Layer 3: CI/CD │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    通知体系                                  │       │
│  │  飞书 Webhook  ──────  Release通知 ──────  失败告警         │       │
│  └─────────────────────────────────────────────────────────────┘       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 二、测试分层详情

### 2.1 端到端测试 (E2E Tests) - 50%

| 测试场景 | 描述 |
|---------|------|
| `test_chk_init_workflow` | 完整初始化工作流 |
| `test_agent_execution` | Agent 执行链路 |
| `test_skill_chaining` | Skill 链式调用 |
| `test_full_integration` | 完整用户场景覆盖 |
| `test_release_pipeline` | 发布流程端到端 |

### 2.2 集成测试 (Integration Tests) - 30%

| 场景 | 验证内容 |
|------|---------|
| Evolution Pipeline | session → analyze → propose → apply |
| Hook Execution | PreToolUse → PostToolUse 链 |
| Knowledge Flow | session → instinct → knowledge |
| CLI Pipeline | init → mode → scan |

### 2.3 单元测试 (Unit Tests) - 10%

| 模块 | 测试范围 | 目标覆盖率 |
|------|---------|-----------|
| `harness/_core/` | ConfigLoader, CacheManager, PathGuard | 95% |
| `harness/cli/` | init, mode, scan, gc, status | 95% |
| `harness/evolve-daemon/` | daemon, analyzer, proposer, validator | 95% |
| `harness/memory/` | memory system | 90% |
| `harness/knowledge/` | knowledge base | 90% |

### 2.4 契约测试 (Contract Tests) - 10%

验证接口契约稳定性：

- **Agent 契约**: 22 个 Agent 文件格式验证
- **Skill 契约**: 38 个 Skill 格式验证
- **Hook 契约**: hooks.json 配置验证

---

## 三、CI/CD 流水线

### 3.1 GitHub Actions 工作流

```yaml
# 触发条件
触发:
  - push: main, develop
  - pull_request
  - release: published
  - workflow_dispatch (手动)

# 流水线阶段
jobs:
  1. lint          # 静态检查 (30s)
  2. unit-tests    # 单元测试 (并行 3模块, 2min)
  3. contract     # 契约测试 (30s)
  4. integration  # 集成测试 (1min)
  5. e2e          # E2E测试 (2min)
  6. quality-gate # 质量门禁汇总

# 总执行时间目标: < 5min
```

### 3.2 发布工作流

```yaml
on:
  release:
    types: [published]

jobs:
  1. pre-release-check    # 全量测试
  2. version-consistency  # 版本一致性
  3. changelog-generate   # 生成 ChangeLog
  4. notify               # 飞书通知
```

---

## 四、监控与灰度发布

### 4.1 错误监控系统

```
┌─────────────────────────────────────────────────────────────┐
│                    错误监控架构                            │
├─────────────────────────────────────────────────────────────┤
│  hooks/bin/collect_error.py                                │
│       ↓                                                    │
│  错误日志写入 harness/memory/errors/                       │
│       ↓                                                    │
│  evolve-daemon 分析错误模式                                │
│       ↓                                                    │
│  自动生成 Bug 测试用例                                      │
│       ↓                                                    │
│  回归测试套件                                               │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 灰度发布策略

```
┌─────────────────────────────────────────────────────────────┐
│                    灰度发布流程                            │
├─────────────────────────────────────────────────────────────┤
│  v1.0.0  ──▶  10% 用户  ──▶  50% 用户  ──▶  100%           │
│              │                  │               │            │
│              ▼                  ▼               ▼            │
│         监控错误率          错误率 < 1%     错误率 < 0.5%  │
│         问题回滚           继续扩大        全量发布        │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 快速回滚机制

- 回滚命令: `git revert HEAD && git push`
- 回滚时间目标: < 5 分钟
- 配合 GitHub Releases 可快速回退版本

---

## 五、通知体系

### 5.1 通知触发条件

| 事件 | 通知内容 | 渠道 |
|------|---------|------|
| Release 发布成功 | 版本号 + ChangeLog | 飞书 Webhook |
| 测试失败 | 失败测试 + 原因 | 飞书 Webhook |
| CI/CD 状态变更 | 构建状态 | GitHub Status |
| Bug 逃逸检测 | Bug 描述 + 影响范围 | 飞书 Webhook |

### 5.2 飞书通知配置

```bash
# hooks/bin/notify.sh
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL}"
```

---

## 六、规范执行机制

### 6.1 三层强制执行

```
Layer 1: CLAUDE.md 文档
├── AI 每次任务前读取
├── 测试规范 + 开发规范
└── Bug 修复流程

Layer 2: Hooks 自动化
├── PreToolUse: 安全检查
├── PostToolUse: 质量门禁
└── 覆盖率检查

Layer 3: CI/CD 阻断
├── PR 必须通过全量测试
├── 覆盖率 < 95% 阻断合并
└── Bug 逃逸自动记录
```

### 6.2 TDD 开发流程

```
┌─────────────────────────────────────────────────────────────┐
│                    TDD 开发流程                            │
├─────────────────────────────────────────────────────────────┤
│  RED  ──▶  GREEN  ──▶  REFACTOR                           │
│    │         │            │                               │
│    ▼         ▼            ▼                               │
│  编写失败   写代码通过    重构                             │
│  测试用例   测试          + 优化                           │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 反馈循环机制

```
用户纠正 → 本能记录 → 置信度累积 → 自动优化
     │         │           │
     └─────────┴───────────┘
           写入 memory/
                 │
                 ▼
         evolve-daemon 分析
                 │
                 ▼
         更新 CLAUDE.md 或自动修复
```

---

## 七、关键指标

| 指标 | 当前 | Week 4 | Month 2 | Month 6 |
|------|------|--------|---------|---------|
| 测试覆盖率 | 30% | 60% | 85% | **95%** |
| Bug逃逸率 | 44% | 20% | 10% | **<2%** |
| CI/CD 自动化 | 无 | 完整 | 完整 | 完整 |
| 通知覆盖 | 无 | 飞书 | 飞书+邮件 | **飞书+告警** |
| 监控覆盖 | 无 | 基础 | 完整 | **生产监控** |

---

## 八、分阶段实施计划

### Phase 1: 基础测试结构 (Week 1-2)
- [ ] 创建测试目录结构
- [ ] 完善 conftest.py fixtures
- [ ] 单元测试覆盖 _core, cli 模块
- [ ] 覆盖率目标: 60%

### Phase 2: 契约测试 + CI/CD (Week 3-4)
- [ ] Agent/Skill/Hook 契约测试
- [ ] GitHub Actions 工作流配置
- [ ] 质量门禁配置
- [ ] 覆盖率目标: 85%

### Phase 3: 监控 + 通知 (Month 2)
- [ ] 错误监控系统完善
- [ ] 飞书通知集成
- [ ] 灰度发布机制
- [ ] 覆盖率目标: 92%

### Phase 4: 完善 + 优化 (Month 3-6)
- [ ] E2E 测试完善
- [ ] LLM-as-Judge 评分系统
- [ ] Property-based Testing
- [ ] 覆盖率目标: 95%

---

## 九、需要创建的文件清单

### 9.1 目录结构
```
harness/tests/
├── unit/_core/
├── unit/cli/
├── unit/evolve-daemon/
├── integration/
├── contracts/agents/
├── contracts/skills/
├── contracts/hooks/
├── e2e/
├── graders/
├── regression/
└── fixtures/
```

### 9.2 新建文件

**配置文件**:
- `pytest.ini`
- `.coveragerc`
- `harness/tests/__init__.py`

**契约测试**:
- `harness/tests/contracts/agents/test_agent_contracts.py`
- `harness/tests/contracts/skills/test_skill_contracts.py`
- `harness/tests/contracts/hooks/test_hook_contracts.py`

**单元测试**:
- `harness/tests/unit/_core/test_config_loader.py`
- `harness/tests/unit/_core/test_cache_manager.py`
- `harness/tests/unit/_core/test_path_guard.py`
- `harness/tests/unit/cli/test_init.py`
- `harness/tests/unit/cli/test_mode.py`
- `harness/tests/unit/evolve-daemon/test_analyzer.py`
- `harness/tests/unit/evolve-daemon/test_proposer.py`

**集成测试**:
- `harness/tests/integration/test_evolution_pipeline.py`
- `harness/tests/integration/test_hook_execution.py`

**E2E 测试**:
- `harness/tests/e2e/test_full_workflow.py`
- `harness/tests/e2e/test_agent_execution.py`

**Grader 系统**:
- `harness/tests/graders/__init__.py`
- `harness/tests/graders/base.py`
- `harness/tests/graders/code_quality_grader.py`
- `harness/tests/graders/pass_at_k.py`

**回归测试**:
- `harness/tests/regression/test_bug_fixes.py`

**CI/CD**:
- `.github/workflows/test.yml`
- `.github/workflows/release.yml`

**Hooks**:
- `hooks/bin/notify.sh`
- `hooks/bin/coverage-check.sh`
- `hooks/bin/quality-gate.sh`

**修改文件**:
- `CLAUDE.md` — 添加测试规范
- `package.json` — 更新测试脚本
- `hooks/hooks.json` — 添加强制钩子

---

## 十、验证方案

### 10.1 本地验证
```bash
# 运行全量测试
npm test

# 运行覆盖率检查
pytest --cov=harness --cov-fail-under=95 -v

# 质量门禁
bash hooks/bin/quality-gate.sh
```

### 10.2 CI/CD 验证
```bash
# GitHub Actions 自动触发
# PR 必须通过全部测试
# 覆盖率 < 95% 阻断合并
```

### 10.3 发布验证
```bash
# 创建 GitHub Release
# 验证自动触发全量测试
# 验证飞书通知收到
```

---

## 十一、附录

### A. 测试命名约定
- `test_<模块名>_<功能名>.py`
- 测试类: `Test<ClassName>`
- 测试函数: `test_<功能描述>`

### B. 测试金字塔 (中文含义)

```
        ┌─────────────────┐
        │     E2E         │  端到端测试 (End-to-End)
        │   完整工作流    │  模拟真实用户操作，覆盖全链路
        ├─────────────────┤
        │  Integration    │  集成测试
        │   多模块协作    │  验证多个模块协同工作
        ├─────────────────┤
        │     Unit        │  单元测试
        │    单模块       │  验证每个模块独立正确性
        ├─────────────────┤
        │   Contract     │  契约测试
        │    接口契约    │  验证 Agent/Skill/Hook 接口稳定性
        └─────────────────┘
```

| 类型 | 中文名 | 比例 | 特点 |
|------|--------|------|------|
| E2E | 端到端测试 | 50% | 完整工作流，模拟真实用户 |
| Integration | 集成测试 | 30% | 多模块协作验证 |
| Unit | 单元测试 | 10% | 单模块正确性 |
| Contract | 契约测试 | 10% | 接口稳定性 |

### C. Bug 逃逸率定义
```
Bug逃逸率 = (生产环境Bug数 / 总发布功能数) × 100%
目标: < 2%
```

### D. 版本发布测试概述要求 (强制)

**每次创建 GitHub Release 时，必须在 Release Notes 中包含测试简要概述**：

```markdown
## 测试概述

| 测试类型 | 数量 | 覆盖率 |
|---------|------|--------|
| 单元测试 | XX | XX% |
| 集成测试 | XX | - |
| E2E测试 | XX | - |
| 契约测试 | XX | - |
| 回归测试 | XX | - |

**总覆盖率**: XX%
**测试执行时间**: XXs
```

**获取测试数据命令**:
```bash
# 获取测试数量
pytest harness/tests/ --collect-only -q

# 获取覆盖率
pytest harness/tests/ --cov=harness --cov-report=term

# 快速版本
pytest harness/tests/ --cov=harness -q
```