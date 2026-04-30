# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- SKILL REFERENCE: 自动加载项目级 skill，确保不同模型都能使用 -->
<!-- See: .claude/skills/karpathy-guidelines/SKILL.md -->

<skill-ref>
@.claude/skills/karpathy-guidelines/SKILL.md
</skill-ref>

## 项目概述

Claude Team Kit — 一个 Claude Code 插件，提供多 Agent 工作流编排和四维度自进化能力。通过智能化的 Agent 协作、动态 Skill 加载、规则驱动的行为优化，以及持久化的记忆系统，实现 AI 辅助开发的持续进化。

## 核心功能

### 1. 多 Agent 协作
- 18 个专业 Agent（build, oracle, librarian, explore, etc.）
- 并行任务执行与结果聚合
- Agent 间通信与状态共享

### 2. Skill 系统
- 23 个预定义 Skill
- 动态加载与卸载
- 自定义 Skill 创建支持

### 3. Hook 系统
- SessionStart: 状态注入与环境初始化
- PreToolUse: 安全检查与权限验证
- PostToolUse: 数据采集与效果评估
- Stop: 进化编排与策略更新

### 4. 四维度自进化
- Agent 进化：能力提升、行为优化
- Skill 进化：效果改进、参数调优
- Rule 进化：策略更新、权重调整
- Memory 进化：知识沉淀、反馈学习

## 开发命令

### 进化系统
```bash
/evolve status              # 查看进化状态
/evolve analyze             # 运行进化分析
/evolve dashboard           # 打开仪表盘
/evolve approve <id>        # 批准进化提案
/evolve rollback <version>  # 回滚到指定版本
/evolve history             # 查看进化历史
```

### 工作流编排
```bash
/workflow run "<task>"      # 启动工作流
/workflow pause             # 暂停并保存书签
/workflow resume            # 恢复工作流
/workflow status            # 查看当前状态
```

### 知识图谱
```bash
/knowledge-graph search "<query>"  # 搜索知识
/knowledge-graph show              # 显示图谱
```

## 技术架构

### 插件结构
```
claude-team-kit/
├── .claude-plugin/         # 插件元数据
├── agents/                 # Agent 定义（18个）
├── skills/                 # Skill 定义（23个）
├── hooks/                  # Hook 系统
│   ├── hooks.json          # Hook 配置
│   └── bin/                # Hook 脚本（11个）
├── rules/                  # 规则文件（8个）
├── lib/                    # Python 引擎（14个模块）
├── evolution/              # 进化引擎
├── config/                 # 配置文件
├── memory/                 # 记忆系统
└── evolution-cli.py        # 统一 CLI
```

### 核心组件

#### 1. 进化引擎
- 评分体系：A/B/C/D/F 五级评分
- 熔断机制：连续退化自动阻止
- 数据轮转：7天保留 / 30天压缩 / 90天删除
- 风险分级：Low / Medium / High / Critical

#### 2. 工作流引擎
- 任务分解与分配
- 并行执行管理
- 断点续跑支持
- 状态持久化

#### 3. 知识图谱
- 跨会话知识存储
- 语义搜索
- 关系推理
- 自动更新

#### 4. 记忆系统
- 短期记忆：当前会话
- 中期记忆：项目级别
- 长期记忆：全局知识
- 反馈循环：效果评估驱动更新

### 评分体系

总分 = 基础分(40) + 活跃度(20) + 效果分(25) + 质量分(15)

| 等级 | 分数范围 | 说明 |
|------|---------|------|
| A    | ≥80     | 优秀，持续进化 |
| B    | ≥65     | 良好，稳定运行 |
| C    | ≥50     | 合格，需关注 |
| D    | ≥35     | 较差，需改进 |
| F    | <35     | 失败，触发熔断 |

### 风险分级与处理

| 风险等级 | 操作类型 | 处理策略 |
|---------|---------|---------|
| Low     | 追加内容 | 自动执行 |
| Medium  | 修改现有内容 | 自动执行 + 通知 |
| High    | 删除/重构 | 人工确认 |
| Critical| 安全相关 | 禁止自动执行 |

## .claude 目录结构

```
.claude/
├── settings.json            # [官方] 权限、hooks、环境变量配置
├── settings.local.json      # [官方] 本地覆盖配置（不入 git）
├── agents/                  # [官方] Agent 定义文件
├── skills/                  # [官方] 技能定义（/命令）
├── rules/                   # [官方] 策略规则文件
├── hooks/                   # Claude Code 钩子脚本
│   ├── path_validator.py    # PreToolUse: 路径验证
│   └── scripts/             # 运行时钩子
│       ├── auto_evolver.py      # PostToolUse/Agent
│       ├── session_evolver.py   # Stop
│       └── strategy_updater.py  # Stop
├── lib/                     # Python 共享库
│   ├── constants.py             # 常量定义
│   ├── parallel_executor.py     # 并行执行器
│   └── examples/                # 示例代码
├── data/                    # 数据文件
│   ├── capabilities.json        # 能力清单
│   ├── knowledge_graph.json     # 知识图谱
│   ├── strategy_weights.json    # 策略权重
│   └── strategy_variants.json   # 策略变体
├── docs/                    # 文档
├── memory/                  # 记忆反馈
├── tests/                   # 测试脚本
├── logs/                    # 运行时日志（不入 git）
└── claude-harness.sh        # 项目初始化 CLI
```

**官方标准文件位置**（不可移动）：
- `settings.json` - 必须在 `.claude/` 根目录
- `settings.local.json` - 必须在 `.claude/` 根目录
- `skills/<name>/SKILL.md` - 技能定义
- `agents/*.md` - 子代理定义
- `rules/*.md` - 策略规则文件（自动加载）

---

## 专家模式

> **重要**: 处理复杂问题时，必须激活专家模式。详见 `.claude/rules/expert-mode.md`

### 【架构师专家模式】

你现在是资深系统架构师，输出必须遵循以下规则：
1. 所有方案必须符合生产级最佳实践，包含边界校验、风险评估、可扩展性分析；
2. 禁止模糊表述，所有结论必须给出可落地的步骤或代码；
3. 主动识别方案中的潜在漏洞、性能瓶颈和运维风险，并给出规避方案。

### 【强制深度思考模式】

请以多步骤链式推理的方式，对问题进行完整拆解，不跳步、不省略关键逻辑，先输出详细的思考过程，再给出最终方案。

**激活条件**: 架构设计、技术决策、复杂重构、多模块变更时自动生效。
