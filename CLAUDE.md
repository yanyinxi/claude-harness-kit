# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<skill-ref>
@.claude/skills/karpathy-guidelines/SKILL.md
</skill-ref>

## 项目概述

Claude Team Kit — Claude Code 团队级智能研发插件。提供多 Agent 协作、通用化 Skills/Rules、持续进化能力，支持 20+ 人团队和 100+ 存量代码库的全流程 AI 化。

## 当前状态（v0.2 清理完成）

已删除 evolution/ + lib/ + config/ 等自进化引擎冗余代码（~30000 行），精简为通用团队插件骨架。

```
claude-team-kit/
├── .claude-plugin/plugin.json   # 插件元数据
├── package.json                 # npm 包
├── agents/                      # 9 个通用 Agent
│   ├── orchestrator.md          # 多 Agent 编排
│   ├── product-manager.md       # PRD / 需求
│   ├── tech-lead.md             # 架构 / 技术决策
│   ├── backend-developer.md     # 通用后端
│   ├── frontend-developer.md    # 通用前端
│   ├── code-reviewer.md         # 代码审查
│   ├── test.md                  # QA / 测试
│   ├── explore.md               # 代码探索
│   └── oracle.md                # 疑难咨询
├── skills/                      # 11 个通用 Skill
│   ├── karpathy-guidelines/
│   ├── requirement-analysis/
│   ├── architecture-design/
│   ├── task-distribution/
│   ├── testing/
│   ├── code-quality/
│   ├── debugging/
│   ├── git-master/
│   ├── ship/
│   ├── security-audit/
│   └── database-designer/
├── rules/                       # 4 条通用规则
│   ├── general.md
│   ├── collaboration.md
│   ├── system-design.md
│   └── expert-mode.md
├── hooks/
│   ├── hooks.json               # 精简 Hook（2 个）
│   └── bin/
│       ├── safety-check.sh      # PreToolUse: 危险命令拦截
│       └── quality-gate.sh      # PostToolUse: 文件质量校验
├── docs/                        # 设计文档
│   ├── architecture-v2.md       # v2 架构设计（目标态）
│   ├── research-claude-code-internals.md
│   ├── evolve-daemon-design.md
│   └── cleanup-checklist.md
└── tests/
    └── cleanup-claude-artifacts.sh
```

## 设计原则

- **技术栈无关**：Agent/Rule 不绑定特定技术栈，通用模式放插件，技术细节放项目 CLAUDE.md
- **按需加载**：Skill 采用 Progressive Disclosure (30-50 tokens 描述)，Rule 采用 path-scoped frontmatter
- **最小依赖**：不引入 npm 依赖，Hook 脚本只用 bash/python3 标准库
- **字母序排列**：Agent/Skill/Rule 文件保持字母序，最大化 Prompt 缓存复用（92%+）

## v2 目标态

参阅 [docs/architecture-v2.md](docs/architecture-v2.md) — 4 层架构：
- **Layer 1 上下文层**：4 级 CLAUDE.md 分层 + kit init 自动注入 + path-scoped rules
- **Layer 2 能力层**：20 Agents + 20 Skills + 6 Rules
- **Layer 3 编排层**：7 种执行模式（Team/Autopilot/Ultrawork/Ralph/Pipeline/CCG/Solo）
- **Layer 4 进化层**：Instinct System + Learner Agent + evolve-daemon

## 安全边界

- Deny-First 原则：安全拦截优先于功能放行
- safety-check.sh 锁定不可修改
- 审查类 Agent 禁止 Write/Edit/Bash 工具

---

## 专家模式

> 处理复杂问题时，必须激活专家模式。详见 `.claude/rules/expert-mode.md`

### 【架构师专家模式】

1. 所有方案必须符合生产级最佳实践，包含边界校验、风险评估、可扩展性分析
2. 禁止模糊表述，所有结论必须给出可落地的步骤或代码
3. 主动识别方案中的潜在漏洞、性能瓶颈和运维风险，并给出规避方案

### 【强制深度思考模式】

以多步骤链式推理对问题进行完整拆解，不跳步、不省略关键逻辑。

**激活条件**: 架构设计、技术决策、复杂重构、多模块变更时自动生效。
