# CLAUDE.md

<!-- 由 chk-init 生成于 2026-05-03 — 基于项目分析 -->
<!-- CHK Version: 0.9.0 -->

## 项目概览

**CHK (Claude Harness Kit)** — 团队级 AI 驾驭工具包，让 AI 真正"看懂"你的代码库。
Human steers, Agents execute. 多 Agent 协作、通用 Skills、持续进化。

## 技术栈
- 语言/构建: Node.js >=18 / npm
- 插件入口: `index.js`
- 配置文件: `package.json` (version: 0.9.0)
- 安装方式: `claude plugins install`

## 构建命令
```bash
npm install   # 安装依赖
npm test      # 运行测试 (200+ 测试)
```

## 插件目录结构 (Claude Code 官方规范)

```
claude-harness-kit/
├── index.js                 # 插件入口
├── package.json             # npm 包配置
├── agents/                  # 22 个 Agent 定义 (*.md)
├── skills/                  # 36 个 Skill 目录
├── hooks/                   # Hook 配置和脚本
│   ├── hooks.json           # Hook 触发规则
│   └── bin/                 # Hook 脚本 (35 个)
├── commands/                # 斜杠命令
│
├── harness/                 # CHK 内部模块
│   ├── _core/               # 核心库 (版本、缓存、路径守卫、本能引擎)
│   │   ├── cache_manager.py  # Prompt 缓存管理
│   │   ├── path_guard.py     # 路径安全守卫
│   │   ├── instinct_engine.py # 本能推理引擎
│   │   └── ...
│   ├── cli/                 # CLI 工具 + modes/
│   ├── docs/                # 设计文档
│   ├── evolve-daemon/       # 自动进化守护进程 (18 模块)
│   │   ├── daemon.py            # 守护进程主循环
│   │   ├── evolve_dispatcher.py # 8 维度决策分发
│   │   ├── analyzer.py          # 会话聚合分析
│   │   ├── rollback.py          # 自动回滚 + 熔断
│   │   └── config.yaml          # 统一进化配置
│   ├── knowledge/           # 知识推荐引擎
│   │   ├── knowledge_recommender.py # 双知识库推荐
│   │   ├── lifecycle.py           # 知识生命周期
│   │   ├── decision/              # 架构决策记录 (ADR)
│   │   ├── guideline/             # 开发规范
│   │   ├── pitfall/               # 已知陷阱
│   │   ├── process/               # 操作流程
│   │   ├── model/                 # 数据模型
│   │   └── evolved/               # 进化生成的知识
│   ├── memory/              # 记忆系统
│   │   ├── instinct-record.json   # 本能记录 (v3.0)
│   │   └── *.json                 # 用户反馈积累
│   ├── rules/               # 扩展规则 (8 个)
│   └── tests/               # 测试套件 (200+ 测试)
│
├── .claude/                 # Claude Code 运行时数据
│   └── data/
│       ├── sessions.jsonl
│       ├── error.jsonl
│       └── ...
└── .claude-plugin/
    └── plugin.json          # 插件元数据
```

## 安装与更新

### 一键安装（推荐）
```bash
# 在项目目录下运行
./install.sh

# 或手动指定模式
./install.sh --local   # 本地目录模式（离线可用）
./install.sh --github  # GitHub 模式（需要网络）
```

### 手动安装
```bash
# 1. 添加本地目录为插件市场
claude plugins marketplace add /path/to/claude-harness-kit

# 2. 安装插件
claude plugins install claude-harness-kit --scope user
```

### 从插件市场安装
```bash
# 从 GitHub 安装（需要网络）
claude plugins install yanyinxi/claude-harness-kit
```

### 更新
```bash
# 更新插件
claude plugins update claude-harness-kit

# 查看插件状态
claude plugins list
```

### 卸载
```bash
claude plugins uninstall claude-harness-kit
```

## 进化系统架构 (双知识库闭环)

```
sessions.jsonl
       ↓
analyzer.py (会话聚合分析)
       ↓
daemon.py (调度 + 执行)
       ↓
┌──────────────────────────────────────────────────────────┐
│  知识生成流                                              │
│  integrated_evolution.py → knowledge_base.jsonl         │
│                                    ↓                    │
│                              进化知识库 (45 条) ←────────┤
└──────────────────────────────────────────────────────────┘
                                    ↓
                      knowledge_recommender.py
                     (双知识库合并: 手工 + 进化)
                                    ↓
                      context_injector.py (注入上下文)
                                    ↓
                         ← 推荐给用户

┌──────────────────────────────────────────────────────────┐
│  效果跟踪流                                              │
│  PostToolUseSuccess → collect_success.py → effect_tracker│
│                                                      ↓   │
│  effect_tracking.jsonl ←───────────── 验证改进有效性     │
└──────────────────────────────────────────────────────────┘
```

### 8 分析维度
- 基础 4 维: agent, skill, rule, instinct
- 扩展 4 维: performance, interaction, security, context

### 双知识库
| 知识库 | 路径 | 内容 |
|--------|------|------|
| 手工维护 | `harness/knowledge/decision/`, `guideline/`, `pitfall/`, `process/`, `model/` | 专家知识 |
| 进化生成 | `harness/knowledge/evolved/` | 学习知识 |

## 核心功能

### 8 种执行模式 (通过 /chk 调用)
- `solo` — 直接对话，零开销
- `auto` — 全自动端到端，5 分钟搞定 Bug
- `team` — 多 Agent 协作开发（默认）
- `ultra` — 极限并行 (3-5 Agent)
- `pipeline` — 严格阶段顺序，TaskFile 协议
- `ralph` — TDD 强制模式，不通过测试不停止
- `ccg` — Claude + Codex + Gemini 三方独立审查
- `default` — 兼容旧名，等同 team 模式

### 22 个 Agent
architect, backend-dev, code-reviewer, codebase-analyzer, database-dev, devops, executor, explore, frontend-dev, gc, impact-analyzer, learner, migration-dev, oracle, orchestrator, product-manager, qa-tester, ralph, security-auditor, tech-lead, test, verifier

### 36 个 Skill
涵盖: testing, debugging, tdd, security-review, architecture-design, api-designer, migration, database-designer, ml-engineer, data-engineer, sre, performance, mobile-dev, iac, docker-essentials, lark-* (飞书全家桶), wechat-*, xiaohongshu-*, 等

## 入口文件
- `index.js` — 插件主入口，暴露 agents/skills/rules
- `harness/cli/` — 命令行入口

## 已知陷阱
- Agent/Skill/Hooks 在插件根目录（符合 Claude Code 官方规范），不使用软链接
- `.claude/` 只允许运行时数据（sessions.jsonl、error.jsonl 等），禁止代码文件
- `harness/` 下只允许白名单子目录（见 `harness/docs/directory-structure-and-migration-plan.md`）
- Python hook 脚本统一 underscore 命名（`collect_agent.py`），Shell hook 统一 hyphen 命名
- 所有改动必须遵循 Claude Code 官方文档规范

## 相关知识
- 项目知识: `harness/knowledge/` (decision/, guideline/, pitfall/, process/, model/)
- 团队规范: `harness/rules/`
- 设计文档: `harness/docs/`
- 进化数据: `harness/knowledge/evolved/`
- 本能记录: `harness/memory/instinct-record.json`

## Allowed Requests

### 允许的操作
- 读取和分析项目文件 (`Read`, `Glob`, `Grep`)
- 运行测试套件 (`npm test`)
- 安装依赖 (`npm install`)
- 执行 Claude Code 插件命令
- 使用 `/team` 系列命令切换执行模式

### 限制的操作
- 禁止直接修改 `.claude/` 目录下的运行时数据
- 禁止修改 `harness/memory/instinct-record.json`（由进化系统自动管理）
- 禁止删除 `harness/knowledge/` 目录下的手工知识库文件
- 危险操作（Bash rm -rf、磁盘写入等）必须通过 path_guard.py 验证

## Guidelines

### 开发准则
1. **中文注释**: 所有代码必须写中文注释
2. **遵循规范**: 所有改动必须遵循 Claude Code 官方文档规范
3. **Agent 优先**: 复杂任务优先使用多 Agent 协作
4. **文件交接**: 跨阶段状态必须写入文件，不依赖上下文传递
5. **质量门禁**: 提交前必须通过 code-reviewer 审查

### 安全准则
1. **路径守卫**: 修改系统目录前必须通过 path_guard.py 验证
2. **凭证保护**: 禁止在代码中硬编码凭证
3. **权限最小化**: 仅请求完成任务所需的最小权限

### 进化准则
1. **观察学习**: 监听用户纠正，自动记录到本能系统
2. **效果验证**: 改进后必须验证有效性，防止负面优化
3. **置信度升级**: 低置信度仅建议，高置信度自动应用

## Trunk Check

### 分支保护规则
- `master` 分支: 禁止直接推送，必须通过 PR 合并
- `develop` 分支: 允许特性分支合并，需至少 1 个 approval
- 临时分支: 开发完成后删除

### 提交规范
- 遵循 Conventional Commits 格式: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- 提交前运行 `npm test` 确保测试通过
- 包含 CHANGELOG 自动生成

### 代码审查
- 所有 PR 必须经过 code-reviewer 审查
- 安全相关变更必须经过 security-auditor 审查
- 架构变更必须经过 architect 评审

## Commands

### 核心命令
| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `/chk-team` | 切换到 Team 模式（默认） | 新功能开发、需求分析、架构设计 |
| `/chk-auto` | 切换到 Autopilot 模式 | 快速修 Bug、根因明确的简单问题 |
| `/chk-ultra` | 切换到 Ultrawork 模式 | 批量重构、大规模修改 |
| `/chk-ralph` | 切换到 Ralph TDD 模式 | 核心代码、支付/安全等零容忍场景 |
| `/chk-pipeline` | 切换到 Pipeline 模式 | 数据库迁移、严格阶段依赖的任务 |
| `/chk-ccg` | 切换到 CCG 审查模式 | 重要 PR、需要三方独立审查 |
| `/chk-solo` | 切换到 Solo 直接对话模式 | 简单问答、知识查询、零开销对话 |

### 开发命令
| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `/chk-init` | 初始化项目分析 | 首次使用 CHK 时让 AI 认识项目 |
| `/chk-gc` | 知识垃圾回收 | 清理过期的上下文和漂移知识 |
| `/chk-status` | 查看 CHK 状态 | 查看当前模式、Hooks、知识库状态 |

### 工具命令
| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `/tdd` | 激活 TDD 开发流程 | 测试驱动开发、确保测试先行 |
| `/council` | 激活四声部决策模式 | 复杂架构决策、多角度方案评审 |
| `/gate-guard` | 激活架构守卫检查 | 高风险变更前的安全拦截 |
| `/ship` | 执行发布前检查清单 | 功能完成后的质量门禁 |
| `/debugging` | 进入调试模式 | 排查问题、系统性根因分析 |

### 管理命令
| 命令 | 描述 | 适用场景 |
|------|------|----------|
| `/chk-evolve` | 查看进化系统状态 | 了解 CHK 自我优化进展 |
| `/chk-instinct` | 查看本能记录 | 查看已学习的经验教训 |
| `/chk-knowledge` | 查看知识库推荐 | 获取项目相关的最佳实践 |