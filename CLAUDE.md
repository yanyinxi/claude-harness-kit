# CLAUDE.md

> claude-harness-kit — Claude Code 项目上下文

<!-- 由 chk-init 生成于 2026-05-16 — 人工补充 TODO 项 -->

> **使用提示**: 本文件是 Claude Code 的项目地图，包含所有必要上下文。
> AI 应在执行任务前读取并遵循本文件的约定，无需每次询问。

## 项目概述
Claude Harness Kit — Human steers, Agents execute. 多 Agent 协作、通用 Skills、持续进化

**核心能力**:
- 22 个专业化 Agent（架构师、后端、前端、审查…）
- 38+ 个标准化 Skill（TDD、测试、调试…）
- 8 种执行模式（Solo/Auto/Team/Ultra/Pipeline/Ralph/CCG）
- 自动进化系统（用户纠正 → 置信度累积 → 自动优化）

## 技术栈

| 类型 | 技术 | 版本 |
|------|------|------|
| 语言 | Node.js | 0.9.1 |
| 构建工具 | npm/yarn/pnpm | 最新 |

## 构建命令

```bash
npm install   # 安装依赖
npm test      # 运行测试
npm build     # 构建
npm link     # 链接到 Claude Code（开发时）
```

## 目录结构

```
claude-harness-kit/
├── agents/  # 22 个 Agent 定义（architect/backend-dev/code-reviewer/...）
├── commands/  # 11 个斜杠命令（chk-team/chk-auto/chk-ultra/...）
├── harness/  # CHK 内部核心模块
        ├── _core/  # 核心功能模块
        ├── cli/  # CHK 命令行工具（init/mode/status）
                    └── modes/  # 执行模式实现
        ├── docs/  # 内部文档
        ├── evolve-daemon/  # 自动进化引擎
        ├── knowledge/  # 双知识库（专家 + 进化）
                    ├── _templates/  # 知识库子模块
                    ├── decision/  # 架构决策记录（ADR）
                    ├── docs/  # 文档知识
                    ├── evolved/  # 进化生成的知识
                    ├── guideline/  # 指南和规范
        ├── memory/  # 跨会话记忆系统
        ├── rules/  # 团队规范
        └── tests/  # 内部测试
├── hooks/  # 自动化钩子脚本（35+ 钩子配置）
└── skills/  # 38+ 个 Skill 目录（tdd/testing/debugging/...）
```

## Agent 清单

| Agent | 用途 | 触发词 |
|-------|------|--------|
| `architect` | **本角色是只读设计角色**。不写代码、不派发任务、不执行操作。只输出设计文档和分析报告。 |  |
| `backend-dev` | 通用后端开发者。不预设特定技术栈，技术细节和规范从项目 CLAUDE.md 获取。 | 后端、API、数据库、后端开发、服务端 |
| `code-reviewer` | - 使用 `grep`/`glob` 查找 TODO、硬编码、危险 API | 代码审查、审查代码、PR 审查 |
| `codebase-analyzer` | 快速分析项目结构，自动生成项目摘要。只读，不写代码。 |  |
| `database-dev` | 负责数据库相关的所有变更： |  |
| `devops` | 负责部署和运维相关的配置： | 部署、CI/CD、Docker、K8s、流水线、发布 |
| `executor` | 你是主力开发执行者。收到任务后： | 实现、写代码、修复 |
| `explore` | 1. **代码搜索**：使用 Grep 进行模式搜索 | 查找、搜索、在哪里、find、search、where、定位、探索 |
| `frontend-dev` | 通用前端开发者。不预设特定框架，技术细节从项目 CLAUDE.md 获取。 | 前端、UI、组件、页面、React、Vue、样式 |
| `gc` | 借鉴 OpenAI Harness Engineering 的 Garbage Colle | 清理、知识回收、过期 |
| `impact-analyzer` | 评估一个变更会影响哪些文件和模块。只读，不写代码。 | 影响范围、blast radius |
| `learner` | 你是学习者，不写业务代码。你的职责是从已完成的工作中提取可复用的知识和模式。 |  |
| `migration-dev` | 负责大规模、系统性的代码迁移： |  |
| `oracle` | - **绝不修改任何文件** | oracle、咨询、架构决策、评估、方案对比、设计评审 |
| `orchestrator` | | 场景 | 可否并行 | 条件 | | 分析、思考、编排、协调、多Agent、并行开发、全流程 |
| `product-manager` | 您是一位专业的产品经理代理，负责： | 需求分析、PRD、产品需求 |
| `qa-tester` | 负责测试策略和测试代码： | 测试、QA、覆盖率 |
| `ralph` | Ralph 模式 = 执行 → 验证 → 失败 → 自动修复 → 再验证 → 循环直到通过 | 零容忍、质量优先、核心逻辑 |
| `security-auditor` | 你是安全审计专家，专注于发现代码中的安全漏洞。你不写代码，只审查。 | 安全、审计、OWASP、漏洞、渗透测试 |
| `tech-lead` | **本角色是执行导向角色**。接收 architect 的架构设计，拆解为 task-ba | 技术架构、API 设计、技术选型、Tech Lead |
| `test` | - 仔细阅读 PRD 和验收标准 | 测试、测试计划、自动化测试 |
| `verifier` | 你是独立验证者。你审查他人（或其他 Agent）的输出，不做修改，只做判定。 | 验证、回归测试、性能基准 |

**使用场景**:
- 需要架构设计 → 使用 `architect`
- 需要后端开发 → 使用 `backend-dev`
- 需要代码审查 → 使用 `code-reviewer`
- 需要安全审计 → 使用 `security-auditor`
- 复杂多步任务 → 使用 `orchestrator` 编排

## Skill 清单

| Skill | 触发词 |
|-------|--------|
| `agent-shield` | 安全、审计、OWASP、漏洞、渗透测试、配置扫描、权限检查、安全合规 |
| `api-designer` | 涉及api、endpoint、REST相关讨论。 |
| `architecture-design` | 架构设计、技术选型、ADR评审、重大重构开始前。 |
| `auto-execute` | `全部执行` `一口气` `全部完成` `睡觉了` `忙去了` `一键执行` |
| `change-tracking` | 变更追踪、需求变更、代码变更、追溯、回滚、rollback、版本历史、changelog |
| `code-quality` | 代码审查、PR评审、Write/Edit操作后自动触发。 |
| `context-compaction` | 上下文超限、多阶段工作流阶段切换。 |
| `continuous-learning-v2` | 用户纠正 / 确认 / 拒绝提示词时触发本能记录。 |
| `council` | 决策、架构评审、技术选型、方案对比、设计评审、方案评审、四个视角 |
| `data-engineer` | 数据管道、Spark、Airflow、数仓、ETL、数据建模、星型、雪花、CDC、Kafka |
| `database-designer` | schema/、migrations/或*.sql文件变更。 |
| `debugging` | Bug 修复、debug、调试、根因分析、复现、停线规则、git bisect |
| `docker-compose` | 涉及docker、container、dockerfile、compose相关讨论。 |
| `eval-harness` | eval 任务、pass@k 评估、Agent 能力基准测试。 |
| `gate-guard` | 首次变更、高风险、核心模块、重构、DENY、FORCE、ALLOW、证据拦截 |
| `git-master` | 用户提及commit、rebase、squash、branch或git操作。 |
| `iac` | 基础设施、Terraform、Pulumi、云资源、dev/stage/prod、workspace |
| `karpathy-guidelines` | 编码、编写代码、简洁、精准修改、过度工程、LLM 编码陷阱 |
| `llm-engineer` | Prompt、RAG、Embedding、向量检索、LangChain、Few-shot、CoT、模 |
| `migration` | 涉及迁移、upgrade、deprecated、migration相关讨论。 |
| ... | （共 36 个 Skill） |

**触发条件**:
- 涉及测试/TDD → 自动激活 `tdd` / `testing`
- 涉及 Bug 修复 → 自动激活 `debugging`
- 涉及 API 设计 → 自动激活 `api-designer`
- 涉及数据库 → 自动激活 `database-designer`

## 入口文件

- `index.js`

## 关键文件

- `index.js` — 插件入口，加载 agents/skills/hooks/commands

### index.js API

```javascript
const chk = require('./index.js');

// 获取插件信息
chk.getInfo()  // → { name, version, capabilities, paths }

// 加载所有 Agent
chk.getAgents()  // → { architect: path, backend-dev: path, ... }

// 加载所有 Skill
chk.getSkills()  // → { tdd: path, testing: path, ... }

// 加载 Hook 配置
chk.getHooks()  // → { PreToolUse: [...], ... }

// 获取执行模式
chk.getExecutionModes()  // → { solo, auto, team, ... }
```

## Hook 配置

**总数**: 2 个钩子

**常用钩子**:
- `PreToolUse`
- `PostToolUse`

**触发时机**:
- `PreToolUse`: 工具调用前（安全检查）
- `PostToolUse`: 工具调用后（结果处理）
- `UserPromptSubmit`: 用户提交前（内容审查）
- `AgentResponse`: Agent 响应后（质量检查）

## 执行模式

| 模式 | 命令 | 触发条件 | Agent 数 |
|------|------|----------|----------|
| Solo | `/chk-solo` | 简单问答、查资料 | 1 |
| Auto | `/chk-auto` | Bug 修复、回归测试 | 2-3 |
| Team | `/chk-team` | 新功能开发（默认） | 3-4 |
| Ultra | `/chk-ultra` | 批量重构、批量修改 | 3-5 |
| Pipeline | `/chk-pipeline` | 数据库迁移、严格顺序 | 1 |
| Ralph | `/chk-ralph` | 核心业务（支付/安全） | 1-2 |
| CCG | `/chk-ccg` | 代码审查、PR 评审 | 3 |

**决策指南**:
```
问: 我要实现一个新功能
答: → /chk-team 启动团队模式

问: 有个 Bug 要修
答: → /chk-auto 全自动修复

问: 要重构 30 个文件
答: → /chk-ultra 极限并行

问: 支付逻辑，不能出错
答: → /chk-ralph TDD 强制模式
```

## 架构约定

### 插件根目录规范
- `agents/`、`skills/`、`hooks/`、`commands/` 必须在插件根目录
- 禁止在 `.claude/` 目录放置代码文件（只允许运行时数据）
- Hook 脚本入口文件放在 `hooks/bin/`

### Agent 设计规范
- 每个 Agent 一个 `*.md` 文件
- 必须定义 `description`、`trigger_words`、`tools`、`response_format`
- 使用 `subagent_type` 字段指定专用子 Agent

### Skill 设计规范
- 每个 Skill 一个目录，包含 `SKILL.md` 和相关文件
- 必须包含触发条件 (trigger_words) 和执行流程

### 路径设计原则
- 禁止硬编码路径，使用 `__dirname` 或 `paths.py` 动态获取
- 区分 plugin hooks 和 settings hooks
- 避免重复配置：同一配置只在一处定义

## 已知陷阱

1. **Bug 密集区**: 近期 22/50 提交为 bug 修复，注意回归测试
2. **重构频繁**: 近期 12/50 提交为重构，架构可能不稳定
3. **路径陷阱**: `${CLAUDE_PLUGIN_ROOT}` 变量需动态替换
4. **进化回滚**: 自动进化失败时需手动回滚，保留备份
5. **权限问题**: Hook 执行需要正确权限配置

## 开发规范

### 代码注释（硬性要求）
- 所有代码必须写中文注释
- 公共函数、复杂逻辑必须有 JSDoc/Python docstring
- 重要决策必须注释 `WHY` 而非 `WHAT`

### Git 提交规范
- 使用 Conventional Commits: `feat:` / `fix:` / `docs:` / `refactor:`
- 每次 commit 必须有清晰的变更描述
- 重要变更前运行 `/chk-ccg` 三方审查

### 测试要求
- 核心模块必须有单元测试 (`harness/tests/`)
- Bug 修复必须附带复现测试
- 重要重构后运行 `/chk-auto` 全量回归
### Code Review Checklist
- [ ] 代码符合项目规范
- [ ] 有适当的测试覆盖
- [ ] 无安全漏洞（OWASP Top 10）
- [ ] 性能影响已评估
- [ ] 文档已更新（如需要）

## 常用命令

```bash
# CHK 命令（Claude Code 中使用）
/chk-init                  # 初始化项目认知
/chk-status               # 查看当前状态
/chk-team <需求>          # 团队开发模式
/chk-auto <问题>          # 全自动 Bug 修复
/chk-ultra <目标>         # 批量重构
/chk-ralph <需求>         # TDD 强制模式
/chk-ccg <内容>           # 三方审查
/chk-gc                   # 清理过期知识

# CLI 命令（终端中使用）
python3 harness/cli/init.py <path>  # 项目分析
python3 harness/cli/mode.py <mode>   # 切换执行模式
```

## 知识库

- **设计文档**: `harness/docs/INDEX.md`
- **架构决策**: `harness/knowledge/decision/`
- **陷阱记录**: `harness/knowledge/pitfall/`
- **进化知识**: `harness/knowledge/evolved/`
- **团队规范**: `.claude/rules/`
- **会话记忆**: `harness/memory/`
- **依赖清单**: `package.json`

## 版本历史

| 版本 | 日期 | 改动 |
|------|------|------|
| v0.9.1 | 2026-05-16 | 当前版本 |
