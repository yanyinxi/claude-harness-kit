# Claude Harness Kit (CHK)

> **让 AI 真正"看懂"你的代码库 — 团队级 AI 驾驭工具包**
>
> CHK = Claude Harness Kit ，  使用CHK描述。

```
Human steers, Agents execute.
Context first, then reasoning.
Verify, then ship.
Evolve, don't just learn.
```

[![Version](https://img.shields.io/badge/CHK-v0.4-blue?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-Claude%20Code%20CLI-green?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

---

## 一句话定义

**CHK（ Claude Harness Kit）** 解决一个根本问题：AI Coding 工具在小项目上表现惊艳，但一到团队、大代码库、复杂任务就歇菜——因为 AI **根本不知道你的项目是什么**。

---

## 你是否也遇到过？

```
😫 每次新会话都要花 30 分钟介绍项目背景
😫 两个 Agent 同时改一个文件，代码全乱了
😫 AI 犯过的错，下次遇到照样犯
😫 团队 10 个人用 AI，输出质量参差不齐
😫 接手别人的代码库，AI 完全两眼一抹黑
```

这些问题，不是 AI 不够强——而是**缺乏上下文管理和协作基础设施**。

---

## 我们走过的三个阶段

这个问题不是凭空出现的，是我们团队在 AI 落地过程中，一步步踩过来的。

### 阶段一：Prompt Engineering（提示词阶段）

```
时间：2023-2024 年

状态：痴迷于写更好的 prompt
├── "你是一个资深 Java 工程师，熟悉 Spring Boot..."
├── "请用中文回答，代码要有注释..."
└── "遵循以下格式..."

遇到的问题：
├── prompt 越写越长，2000 tokens 都不够用
├── 不同人写的 prompt 质量参差不齐
├── 跨项目完全无法复用
└── 每次新会话都要把项目背景重新说一遍
```

**核心教训**：prompt 再好，也解决不了"AI 不知道我的项目"这个根本问题。

---

### 阶段二：Context Management（上下文管理阶段）

```
时间：2024 年

状态：意识到 prompt 只是表面，核心是上下文
├── 创建 CLAUDE.md 文件描述项目
├── 用 SessionStart Hook 注入项目上下文
└── 按需分层：个人 → 团队 → 项目

遇到的问题：
├── 上下文有了，但 Session 之间不持久
├── 多 Agent 同时工作，互相打架
├── 团队 20 个人，各用各的，没有统一规范
└── AI 犯过的错，下次照样犯，没有学习机制
```

**核心教训**：上下文解决了"让 AI 知道"，但解决不了"让 AI 持续进化"。

---

### 阶段三：Harness Engineering（驾驭阶段）

```
时间：2024-2025 年

借鉴 OpenAI Harness Engineering 方法论

不只是"给 AI 信息"，而是系统性地"驾驭 AI 行为"：

  ┌─────────────────────────────────────────┐
  │           Human steers,                  │
  │            Agents execute.               │
  │                                         │
  │  人是骑手，Agent 是马                    │
  │  Rule/Skill 是缰绳                       │
  │  不是让 AI 自由发挥，而是给它划好赛道     │
  └─────────────────────────────────────────┘

核心改变：
├── 22 个专业 Agent（架构师、开发、测试、审查...）
├── 19 个标准 Skill（如何做 TDD、如何设计 API...）
├── 6 条强制 Rules（协作协议、安全底线...）
├── 5 个 Hook 事件（上下文注入、安全拦截、质量门禁...）
└── 进化闭环（犯错 → 学习 → 固化，不再犯第二次）

这就是 CHK v0.4
```

---

## 换个方式用 AI

```
❌ 传统方式（AI 在黑暗中摸索）
   "这是一个 Spring Boot 项目，数据库用 PostgreSQL..."
   → 每一次会话重复一次
   → AI 输出质量依赖你描述得好不好

✅ CHK 方式（AI 一进来就懂）
   SessionStart Hook → 自动注入项目上下文
   → 第一次对话就是有效对话
   → 60x 上下文启动速度提升
```

---

## 核心能力一览

### 多 Agent 并行协作 — 不再"打架"

```
CHK 自动处理：

   ┌─ 冲突检测 ─────────────────────────────┐
   │  Agent A 要改 file.java                 │
   │  Agent B 也要改 file.java              │
   │  → 自动识别 → 强制串行                  │
   │  → 不会覆盖，不会冲突                  │
   └────────────────────────────────────────┘

   ┌─ 任务拆解 ─────────────────────────────┐
   │  "实现标签过滤"                         │
   │  → 自动拆成 5 个独立任务                 │
   │  → backend | frontend | database       │
   │  → 可以并行的并行，不能并行的串行         │
   └────────────────────────────────────────┘

   ┌─ 阶段交接 ─────────────────────────────┐
   │  研究 → 设计 → 实现 → 审查 → 交付        │
   │  产出物写文件，不丢在上下文里            │
   │  /compact 之后精确恢复                   │
   └────────────────────────────────────────┘
```

### 持续进化 — 犯过的错不再犯

```
❌ 没有进化（大多数工具）
   你纠正 AI → AI 记住了 → 下次还是犯错
   → 纠正 100 次，犯错 100 次

✅ CHK 进化闭环
   纠正 1 次 → instinct 记录（置信度 0.3）
   纠正 2 次 → 置信度 0.5，观察报告
   纠正 3 次 → 置信度 0.7，生成提案
   提案通过 → 自动修复 Skill/Rule
   7天验证 → 效果提升 → 固化
   → 同一个错，永远只犯一次
```

### 团队级规范 — 新人也能用好 AI

```
20 人团队：

   没有 CHK:
     张三用 AI → 代码风格 A
     李四用 AI → 代码风格 B
     王五用 AI → 没有测试覆盖
     → 输出质量参差不齐，全靠个人能力

   有 CHK:
     统一 22 个 Agent 定义
     统一 19 个 Skill 规范
     统一 6 条 Rules 约束
     kit sync 同步团队配置
     → 输出质量稳定可预期
```

---

## 快速开始

### 安装

#### Step 1: 克隆项目

```bash
git clone https://github.com/yanyinxi/claude-harness-kit.git
cd claude-harness-kit
```

#### Step 2: 添加本地插件市场

```bash
claude plugins marketplace add --scope local $(pwd)
```

#### Step 3: 安装插件

```bash
claude plugins install claude-harness-kit
```

#### Step 4: 验证

```bash
claude plugins list
# 应该看到: claude-harness-kit  enabled
```

---

### 使用

```bash
# 查看可用命令
./cli/kit.sh --help

# 初始化项目（生成 CLAUDE.md）
./cli/kit.sh init

# 标准开发流程
./cli/kit.sh dev "实现用户登录功能"

# 代码审查
./cli/kit.sh review

# 批量迁移
./cli/kit.sh migrate "升级 Spring Boot 2.x → 3.x"
```

---

### 第二部分：使用

#### 使用方式一：kit CLI 命令行（推荐新手）

**Step 1: 初始化一个存量项目**

```bash
cd /path/to/your-legacy-project

# 运行初始化，自动分析项目结构
./cli/kit.sh init
```

输出示例：

```
🔍 开始分析项目...
✅ 检测到技术栈: Spring Boot 3.2 + PostgreSQL + Vue 3
✅ 检测到构建工具: Maven
✅ 识别模块数: 12 个
✅ 关键路径: src/main/java/com/demo/

📄 生成文件:
   - CLAUDE.md (项目上下文, 150 行)
   - .claude/settings.json (Hook 配置)
   - .claude/knowledge/ (知识库目录)

🎉 初始化完成！重新启动 Claude Code 即可生效。
```

**Step 2: 启动标准开发流程**

```bash
./cli/kit.sh dev "实现用户登录功能"
```

输出示例：

```
┌─────────────────────────────────────────────────────────────┐
│  kit dev — 标准开发流程                                      │
│  任务: 实现用户登录功能                                      │
└─────────────────────────────────────────────────────────────┘

📋 Phase 1: 需求澄清
   ? Q1: 登录方式支持哪些？ (账号密码 / 手机验证码 / OAuth)
   ? Q2: 是否需要记住登录状态？
   ? Q3: 登录失败是否需要图形验证码？

📋 Phase 2: 架构设计
   → 生成 plan/architecture.md

📋 Phase 3: 并行实现
   → backend-dev | frontend-dev | database-dev

📋 Phase 4: 代码审查
   → code-reviewer + security-auditor

📋 Phase 5: 交付
   → git commit + push

总耗时: ~35 min
```

**Step 3: 代码审查**

```bash
# 审查当前分支的所有变更
./cli/kit.sh review

# 只审查特定文件
./cli/kit.sh review --files "src/service/AuthService.java"
```

**Step 4: 批量迁移（Java 8 → Java 17 为例）**

```bash
# 先扫描评估
./cli/kit.sh scan --repo /path/to/project

# 输出迁移评估报告：
# 技术栈: Java 8 + Spring Boot 2.5
# 改动量: High (需要改 45 个文件)
# 风险点: javax.* → jakarta.* 迁移
# 建议: 试点项目先跑一遍，积累迁移手册

# 启动迁移流程
./cli/kit.sh migrate "升级 Java 8 → Java 17 + Spring Boot 2.x → 3.x" \
  --repo /path/to/project \
  --mode autopilot
```

---

#### 使用方式二：Claude Code 内直接对话（适合深度用户）

在 Claude Code CLI 中（`claude` 命令），直接用自然语言指挥：

**场景 1: 启动多 Agent 并行分析**

```
你: 分析一下如何实现这个功能：用户可以给素材打标签

CHK: (自动启动 Orchestrator)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Phase 1: 并行研究开始

🔍 explore (Haiku) — 搜索相关代码
   → 找到 UserController, TagService, TagMapper
   → 现有标签表: user_tags, 关联表: user_tag_relation

🔍 codebase-analyzer (Haiku) — 分析模块结构
   → 用户模块: user-api → user-service → user-dal
   → 标签模块: tag-api → tag-service → tag-dal

🔍 impact-analyzer (Haiku) — 评估影响
   → 改动文件: 8 个
   → 风险等级: Medium
   → 建议: 先试点标签查询，验证后再加打标功能

📄 输出: research/summary.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**场景 2: 激活特定 Agent**

```
你: 使用 architect Agent 设计这个模块的架构

CHK: (切换到 architect Agent, 使用 Opus 模型)

# architect 输出:
## 模块架构设计: 用户标签系统

### 现状分析
- 现有: 用户表、标签表、关联表
- 缺失: 打标接口、标签查询接口

### 方案选择
方案 A: 独立标签服务
方案 B: 在用户服务内集成（推荐）

推荐理由: 标签是用户域的一部分，拆出去增加复杂度

### 数据模型
- UserTag: id, user_id, tag_id, created_at
- Tag: id, name, type, color

### API 设计
POST /api/users/{userId}/tags     # 打标
DELETE /api/users/{userId}/tags/{tagId}  # 取消打标
GET /api/users/{userId}/tags     # 查询标签

### 注意事项
⚠️ 需要考虑标签数量上限（建议 20 个）
⚠️ 需要考虑标签重复打标（幂等处理）
```

**场景 3: 切换执行模式**

```
你: 用 ralph 模式重写支付模块

CHK: (切换到 Ralph Mode)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐴 Ralph Mode: 不通过不停止
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 第 1 轮: 生成支付服务
   → 产出: PayService.java
   → 测试运行: ❌ 金额精度问题 (BigDecimal)

🔄 第 2 轮: 修复金额精度
   → 修复: amount.multiply(100).longValue()
   → 测试运行: ❌ 并发问题

🔄 第 3 轮: 添加分布式锁
   → 修复: RedissonLock beforePay()
   → 测试运行: ❌ 事务边界问题

🔄 第 4 轮: 调整事务传播
   → 修复: @Transactional(propagation=REQUIRES_NEW)
   → 测试运行: ❌ 幂等性问题

🔄 第 5 轮: 添加幂等 token
   → 修复: IdempotentTokenInterceptor
   → 测试运行: ✅

🔄 第 6 轮: 安全审查
   → security-auditor (Opus): ✅ SQL 注入检查通过
   → security-auditor (Opus): ✅ 金额篡改检查通过

🔄 第 7 轮: 最终验证
   → 全量测试: ✅ 45/45 通过
   → 性能测试: ✅ 1000 TPS
   → 安全测试: ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Ralph Mode 完成 (7 轮，全部通过)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**场景 4: 使用特定 Skill**

```
你: 使用 tdd skill 实现用户注册功能

CHK: (激活 tdd Skill，执行 TDD 流程)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 TDD 模式: Red → Green → Refactor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Step 1: 写一个失败的测试
   → UserServiceTest.register_success()
   → UserServiceTest.register_email_duplicate()
   → 测试编译失败（功能未实现）

🟢 Step 2: 让测试通过（最小化实现）
   → 实现 UserService.register()
   → 测试运行: ✅ 2/2 通过

🔵 Step 3: 重构
   → 提取 ValidationUtils
   → 添加参数校验
   → 测试运行: ✅ 2/2 通过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ TDD 完成
   - 测试数: 5 个
   - 覆盖率: 78%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

#### 使用方式三：7 种执行模式选型

| 场景 | 推荐模式 | 说明 |
|------|---------|------|
| 简单问答 | `Solo` | 直接对话，不用 Agent |
| 快速修复 Bug | `Autopilot` | 全自动端到端，5 分钟搞定 |
| 日常功能开发 | `Team` | 默认模式，5 阶段流程 |
| 批量代码改造 | `Ultrawork` | 极限并行，3-5 个 Agent 同时工作 |
| 数据库迁移 | `Pipeline` | 严格顺序，上一步输出喂下一步 |
| 支付/安全代码 | `Ralph` | 不通过不停止，持久环 |
| 关键架构决策 | `CCG` | Claude + Codex + Gemini 三方审查 |

切换模式：

```
你: 切换到 ultrawork 模式

你: 对这 20 个文件统一添加日志

CHK: (启动 Ultrawork Mode)
   → 分析 20 个文件
   → 拆成 4 组，每组 5 个文件
   → 派发 4 个并行 Agent
   → 汇总结果 → 报告
```

---

## 执行流程可视化

### 标准开发（Team 模式）

```
用户: "实现素材标签过滤"

┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Research (并行分析) — ~2 min                       │
│                                                             │
│   🔍 explore ──→ 找到相关代码和调用链                        │
│   🔍 analyzer ──→ 分析模块结构和依赖                        │
│   🔍 impact ────→ 评估变更影响范围                        │
│                                                             │
│   → research/summary.md                                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Plan (串行设计) — ~5 min                          │
│                                                             │
│   🏗️ architect (Opus) ──→ 架构设计                          │
│   📋 tech-lead (Opus) ──→ 技术评审                          │
│                                                             │
│   → plan/architecture.md                                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Implement (并行编码) — ~15 min                     │
│                                                             │
│   Task 1: backend ──→ Service 层逻辑         [并行]         │
│   Task 2: frontend ─→ 标签选择器组件       [并行]         │
│   Task 3: database ─→ 动态 SQL + 索引       [并行]         │
│                                                             │
│   → output/task_*.md                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Verify (并行审查) — ~10 min                        │
│                                                             │
│   🔍 code-reviewer ──→ 5 维度审查（正确性/性能/安全...）     │
│   🔍 qa-tester ──────→ 测试覆盖验证                         │
│   🔍 security ────────→ 安全审计（Opus）                    │
│                                                             │
│   → review/report.md                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: Ship (交付) — ~3 min                               │
│                                                             │
│   ✅ 最终验证 → ✅ 审查通过 → ✅ git commit + push            │
└─────────────────────────────────────────────────────────────┘

总耗时: ~35 min（传统串行方式: ~90 min）
```

---

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Harness Kit (CHK)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 4: 进化层  (让 AI 越来越聪明)                        │
│  ┌───────────┐  ┌────────────┐  ┌─────────────────────┐  │
│  │ Instinct  │  │ evolve-    │  │  Knowledge          │  │
│  │ System    │  │ daemon     │  │  Lifecycle          │  │
│  │ 0.3→0.9   │  │ 守护进程   │  │  draft→verified→   │  │
│  │ 置信度累积 │  │           │  │  proven 自动衰减     │  │
│  └───────────┘  └────────────┘  └─────────────────────┘  │
│                                                             │
│  Layer 3: 编排层  (多 Agent 协作)                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Orchestrator — 冲突检测 | 任务拆解 | 结果汇聚       │  │
│  │  7 种执行模式: Solo | Autopilot | Team | Ultrawork  │  │
│  │                 Pipeline | Ralph | CCG              │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 2: 能力层  (22 Agents + 19 Skills + 6 Rules)        │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Opus: architect | tech-lead | security-auditor     │  │
│  │  Sonnet: executor | backend | frontend | database   │  │
│  │          code-reviewer | qa-tester | ralph | ...     │  │
│  │  Haiku: explore | codebase-analyzer | impact-analyzer│  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 1: 上下文层  (让 AI 快速看懂项目)                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  4 级 CLAUDE.md: 个人 → 团队 → 项目 → 模块          │  │
│  │  Hook: SessionStart 自动注入项目上下文               │  │
│  │  Progressive: 3级索引节省 90% 上下文占用            │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 竞品对比

| 工具 | 多 Agent 协作 | 上下文管理 | 自动进化 | 团队规范 | 适合场景 |
|------|:-------------:|:---------:|:-------:|:-------:|---------|
| **CHK** | ✅ 完整协议 | ✅ 4级分层 | ✅ 闭环 | ✅ 完善 | **20+ 人团队** |
| everything-claude-code | ✅ 基础 | ⚠️ 分散 | ✅ Instinct | ✅ | 插件生态 |
| oh-my-claudecode | ✅ 7 模式 | ❌ | ✅ Learner | ❌ | 个人效率 |
| Superpowers | ❌ | ❌ | ❌ | ❌ | TDD 流程 |
| Claude Code 原生 | ❌ | ❌ | ❌ | ❌ | 个人小项目 |
| GitHub Copilot | ❌ | ❌ | ❌ | ❌ | IDE 辅助 |

### CHK 的独特价值

```
✅ 上下文启动: 30 分钟 → 30 秒 (60x)
✅ 开发效率: 复杂任务 2.5x 提升
✅ 错误率: 同一错误重复出现 40% → <5% (8x)
✅ 新人上手: 1 周 → 1 天 (7x)
✅ 审查覆盖: 30% → 100% (3.3x)
```

---

## 常见问题

**Q: 需要学习很多新东西吗？**
> 不用。安装后 `./cli/kit.sh init` 初始化项目，日常用 `./cli/kit.sh dev` 开发，和平时用 Claude Code 一样。

**Q: 和 Claude Code 原生冲突吗？**
> 不冲突。CHK 是插件，运行在 Claude Code 之上，补充了上下文、协作、进化能力。

**Q: 团队所有人都要安装吗？**
> 团队负责人安装一次，配置中央仓库，成员用 `kit sync` 同步即可。

**Q: 我的项目很小，需要 CHK 吗？**
> 如果是个人小项目，Claude Code 原生就够用了。CHK 适合需要多人协作、有大量存量代码、或需要持续维护的项目。

**Q: evolve-daemon 会自动修改我的代码吗？**
> 不会。安全模块（`rules/security.md`）被锁定，AI 不可修改。只有低风险变更才自动应用，高风险变更需要人工审批。

**Q: 安装时报错 "Plugin not found in any marketplace"？**
> 这是因为需要先添加插件市场。请使用「安装方式二：本地安装」的方式，先执行 `claude plugins marketplace add --scope local $(pwd)`，然后再安装。

**Q: 安装后不生效？**
> 请重启 Claude Code（退出后重新进入），或者尝试 `claude plugins update claude-harness-kit`。

**Q: 可以在 Windows 上使用吗？**
> CHK 主要面向 macOS 和 Linux。Windows 用户可以在 WSL2 环境下使用。

---

## 安装故障排查

| 问题 | 解决方案 |
|------|---------|
| `Plugin not found in marketplace` | 先运行 `claude plugins marketplace add --scope local /path/to/claude-harness-kit` |
| `marketplace.json not found` | 确保 marketplace.json 文件存在于 `.claude-plugin/` 目录下 |
| 插件已安装但不生效 | 重启 Claude Code，或运行 `claude plugins update claude-harness-kit` |
| 找不到 kit.sh 命令 | 确保在项目目录下运行，且文件有执行权限 `chmod +x ./cli/kit.sh` |

---

## 设计原则

```
1. Human steers, Agents execute
   → 人是骑手，Agent 是马，Rule/Skill 是缰绳

2. 上下文优先于推理
   → 与其让 AI 猜，不如告诉它

3. 安全优先于功能
   → Deny-First，危险命令直接拦截

4. 验证闭环优先于一次生成
   → Ralph Loop：不通过不停止

5. 渐进式复杂度
   → Solo → Team → Ultrawork → Ralph，按需引入
```

---

## License

MIT License

## 致谢

借鉴了以下优秀项目的设计理念：

| 来源 | 借鉴点 |
|------|--------|
| **OpenAI Harness Engineering** | Human steers, Agents execute / 知识生命周期 |
| **everything-claude-code** | 5 阶段编排 / Instinct v2 |
| **oh-my-claudecode** | 7 种执行模式 / Ralph Loop |
| **Superpowers** | 7 阶段工程流水线 / TDD 铁律 |
| **Claude Code 源码 (KAIROS)** | 后台 daemon / Prompt 缓存优化 |
| **Harness CI/CD** | AutoFix / AI 验证 + 自动回滚 |
