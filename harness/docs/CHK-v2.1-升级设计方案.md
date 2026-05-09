# CHK v2.1 升级设计方案

> 基于 Claude Code 官方生态 + 标杆项目对标分析

## 执行摘要

通过深度研究 Claude Code 官方架构（四层扩展机制：MCP→Plugin→Skill→Hook）、标杆项目（superpowers/oh-my-claudecode/everything-claude-code/context-cascade）以及 CHK 自身源码，识别出 **5 大升级方向、14 项具体改进**，目标是将 CHK 从"功能完整"提升到"生态领先"。

---

## 一、生态研究总结

### 1.1 Claude Code 官方架构（四层扩展机制）

```
Layer 1: MCP Servers     ← 外部工具集成（数据库查询、浏览器控制）
Layer 2: Plugins         ← 组件包（Skills + Hooks + MCP 配置）
Layer 3: Skills          ← 领域能力（Markdown 定义，三级渐进加载）
Layer 4: Hooks           ← 确定性拦截器（exit 0/1/2）
```

**关键洞察**：
- **Skills 三级渐进加载**：L1(metadata, ~100 tokens) → L2(body, <5k) → L3(refs, on-demand)。Claude Code 只在触发时加载完整 Skill body，节省上下文窗口
- **Hooks 是唯一强制层**：exit 0=放行, 1=硬失败, 2=阻断/警告。CLAUDE.md 和 Rules 只是"建议"（~70% 遵守率）
- **Plugin 懒加载**：Skill 描述在会话启动加载，完整 body 只在调用时加载，Hook 脚本永远不会被 Claude 同时看到

### 1.2 标杆项目对标

| 项目 | Stars | 核心特色 | CHK 可借鉴 |
|------|-------|---------|-----------|
| **superpowers** | ~169K | Git worktree 隔离 + TDD 强制 + 4 阶段工作流 + 14 Skills | Worktree 隔离机制、Plan→Execute 强制流程 |
| **oh-my-claudecode** | — | Magic Words 触发（ultrawork/prowork）、9 Skills + 7 Agents | 自然语言触发词、智能委托路由 |
| **everything-claude-code** | ~169K | 183 Skills + 48 Agents + AgentShield + Instinct Learning | 安全扫描器、 instinct 置信度系统 |
| **context-cascade** | — | 嵌套插件架构 PLAYBOOKS→SKILLS→AGENTS→COMMANDS，省 90% 上下文 | 渐进式上下文加载 |
| **ensemble** | — | 24 包模块化、分层架构（core/workflow/framework） | 模块化分包发布 |

### 1.3 生态系统规模（2026 Q2）

- 282,325+ 组件，13,151+ 作者，每周 2,069 个新插件
- Skills 占 57.2%，Commands 占 20.6%，Agents 占 17.0%
- **Hooks 仅占 2.4%**，MCP 仅占 2.5%——这是 CHK 的巨大机会（CHK 已经有 33 个 Hooks）
- 最成功的插件都是**多组件捆绑**（Skills + Agents + Hooks + Commands），而非单功能工具

---

## 二、CHK 现状 SWOT 分析

### 2.1 优势（Strengths）

1. **完整的自进化闭环**：从数据收集 → 分析 → 决策 → 执行 → 评估 → 回滚，业界少有的真正 OODA 循环
2. **双知识库设计**：手工知识保证准确性，进化知识自动捕捉团队模式
3. **多层安全机制**：预防（safety-check）→ 强制（tdd-check）→ 门禁（quality-gate）→ 过滤（secret-filter）→ 回滚（rollback）
4. **7 种执行模式**：覆盖 solo→team→ultra→ralph→ccg→auto→gc 全场景
5. **Hook 数量领先**：33 个 Hooks 覆盖 9 种事件类型，远超生态平均水平

### 2.2 劣势（Weaknesses）

1. **缺少 Git Worktree 隔离**：superpowers 的核心优势，CHK 完全没有
2. **Skill 没有渐进加载**：所有 Skill 内容在会话启动就加载，浪费上下文窗口
3. **缺少自然语言触发**：没有 Magic Words / 快捷命令，用户需要记住具体模式名称
4. **没有 AgentShield 安全扫描**：everything-claude-code 有专门的安全审计能力
5. **上下文管理粗糙**：没有 PLAYBOOK→SKILL→AGENT 的嵌套加载机制
6. **进化系统强依赖 API**：无 API Key 时降级为本地启发式，效果大打折扣
7. **缺少可视化界面**：所有数据在 JSONL 中，没有 Web UI 或 CLI 图表

### 2.3 机会（Opportunities）

1. **Hooks 是生态洼地**：Hooks 仅占生态 2.4%，CHK 有 33 个 Hooks 是核心竞争力
2. **自进化是差异化**：没有任何标杆项目有类似 CHK 的完整进化闭环
3. **中文生态空白**：所有标杆项目都是英文，中文团队市场巨大
4. **Claude Code Kairos 前瞻**：Anthropic 正在开发主动 Agent 模式（SleepTool、CronCreateTool、PushNotificationTool），CHK 的进化系统天然适配

### 2.4 威胁（Threats）

1. **标杆项目体量碾压**：superpowers 169K stars，生态规模效应显著
2. **Claude Code 原生功能增强**：如果官方推出内置编排/进化，插件价值被稀释
3. **Plugin 供应链风险**：生态中已出现 plugin-canary 安全审计工具，说明恶意插件已出现

---

## 三、设计方案：5 大升级方向

### 方向 1：引入 Git Worktree 隔离（借鉴 superpowers）

**现状**：CHK 的 orchestrator.md 提到 "Git worktree 隔离的 → 总是可并行"，但**没有实际实现**。

**设计**：

```
/chk worktree create <task-name>    # 创建隔离工作树
/chk worktree execute <task-name>   # 在隔离环境中执行
/chk worktree merge <task-name>     # 合并回主分支
/chk worktree list                  # 列出所有工作树
/chk worktree cleanup               # 清理已完成的工作树
```

**实现细节**：

1. **worktree-create.sh**（新 Hook）：
   - 基于主分支创建 `worktree/<task-name>` 分支
   - 在 `.claude/worktrees/` 下创建工作树目录
   - 自动复制 `.claude/` 配置到工作树

2. **worktree-sync.sh**（增强现有 Hook）：
   - 会话开始时同步主分支最新代码
   - 冲突时自动 rebase

3. **orchestrator.md 更新**：
   - 并行任务自动创建工作树
   - 串行任务在主分支执行
   - 冲突检测矩阵增加 "worktree 隔离" 维度

**价值**：
- 彻底消除并行 Agent 的文件冲突
- 失败任务可独立回滚，不影响主分支
- 多个功能可并行开发，互不干扰

---

### 方向 2：Skill 渐进式加载（借鉴 context-cascade + Claude Code 官方）

**现状**：CHK 的 Skill 是完整 Markdown 文件，会话启动时全部加载。index.js 的 `loadSkills()` 只是返回目录路径，Claude Code 可能在启动时读取所有 SKILL.md。

**设计**：

引入 **PLAYBOOK → SKILL → AGENT → COMMAND** 四级嵌套架构：

```
Level 1: PLAYBOOK（剧本）
  - 只加载元数据：name + description + trigger_words
  - ~100 tokens
  - 例如："backend-api-development", "frontend-refactor"

Level 2: SKILL（技能）
  - 触发时加载完整 SKILL.md
  - < 5k tokens
  - 例如：testing, debugging, api-designer

Level 3: AGENT（代理）
  - 需要时动态加载 Agent 定义
  - 例如：architect, backend-dev, code-reviewer

Level 4: COMMAND（命令）
  - 具体执行指令
  - 例如：/chk init, /chk status, /chk gc
```

**实现细节**：

1. **重构 Skill 目录结构**：

```
skills/
├── backend-api/              # PLAYBOOK
│   ├── PLAYBOOK.md           # L1: 元数据 + trigger words
│   ├── skills/               # L2: 关联 Skills
│   │   ├── api-designer/
│   │   ├── testing/
│   │   └── debugging/
│   └── agents/               # L3: 关联 Agents
│       ├── architect.md
│       └── backend-dev.md
```

2. **更新 index.js**：
   - `loadSkills()` 改为返回 L1 元数据
   - 新增 `loadSkillBody(skillName)` 按需加载完整内容
   - 新增 `loadPlaybooks()` 返回剧本列表

3. **触发词系统**（借鉴 oh-my-claudecode Magic Words）：
   ```yaml
   # PLAYBOOK.md frontmatter
   ---
   name: backend-api
   triggers: ["开发API", "接口设计", "后端开发", "api development"]
   description: 后端 API 开发全流程（设计→实现→测试→文档）
   skills: [api-designer, testing, debugging]
   agents: [architect, backend-dev, code-reviewer]
   ---
   ```

**价值**：
- 节省 60-80% 上下文窗口
- 自然语言触发，降低使用门槛
- 场景化组合 Skills + Agents

---

### 方向 3：AgentShield 安全扫描器（借鉴 everything-claude-code）

**现状**：CHK 有 `safety-check.sh` 拦截危险命令，但**缺少对配置本身的安全审计**。

**设计**：

```
/chk audit          # 全面安全审计
/chk audit --config # 审计配置文件
/chk audit --hooks  # 审计 hook 脚本
/chk audit --agents # 审计 agent 定义
```

**实现细节**：

1. **agent-shield Skill**（已有，需增强）：
   - 扫描 `.claude/settings*.json` 中的危险配置
   - 扫描 hooks 脚本中的数据外泄风险
   - 扫描 Agent 定义中的权限过度授权
   - 扫描 Skill 中的 allowed-tools 是否合理

2. **安全规则库**：
   ```yaml
   # 审计规则示例
   - id: SEC-001
     name: "Plugin Root 泄露"
     pattern: "CLAUDE_PLUGIN_ROOT.*Users.*"
     severity: high
     fix: "使用 ${CLAUDE_PLUGIN_ROOT} 变量替代硬编码路径"

   - id: SEC-002
     name: "过度权限授予"
     pattern: 'defaultMode: "bypassPermissions"'
     severity: medium
     fix: "使用具体权限列表替代通配符"

   - id: SEC-003
     name: "API Key 硬编码"
     pattern: "(sk-ant-|sk-)[a-zA-Z0-9]{20,}"
     severity: critical
     fix: "使用环境变量存储 API Key"

   - id: SEC-004
     name: "Webhook URL 泄露"
     pattern: "https://(open\.)?feishu\.cn/.*hook"
     severity: high
     fix: "使用环境变量存储 Webhook URL"
   ```

3. **Stop Hook 集成**：
   - 会话结束时自动运行安全扫描
   - 发现问题时阻止会话关闭，提示用户处理

**价值**：
- 主动发现配置漏洞
- 防止敏感信息泄露
- 建立安全基线

---

### 方向 4：进化系统增强（前瞻性设计，适配 Kairos）

**现状**：CHK 进化系统依赖 analyzer → dispatcher → proposer → apply/rollback 流程，但**全是被动触发**（等待用户会话数据积累）。

**设计**：引入**主动进化**模式，适配 Claude Code 未来的 Kairos（主动 Agent）能力：

```
被动进化（现有）          主动进化（新增）
    ↓                         ↓
sessions.jsonl          定时扫描代码库
    ↓                         ↓
analyzer.py             检测代码异味/技术债务
    ↓                         ↓
evolve_dispatcher.py    自动生成修复提案
    ↓                         ↓
apply/rollback          用户审查后自动应用
```

**实现细节**：

1. **定时进化任务**（利用现有 scheduler.py）：
   ```python
   # 新增进化类型
   EVOLUTION_TYPES = {
       "session_based": "现有：基于会话数据",
       "code_smell": "新增：基于代码异味扫描",
       "dependency": "新增：基于依赖更新",
       "security": "新增：基于安全漏洞扫描",
   }
   ```

2. **代码异味检测器**（新模块）：
   - 使用 `radon`（圈复杂度）、`bandit`（安全）、`vulture`（死代码）
   - 扫描结果写入 `evolution/code-smells.jsonl`
   - 触发知识库进化提案

3. **依赖进化**（新模块）：
   - 监控 `package.json`, `requirements.txt`, `go.mod`
   - 检测过时依赖、安全漏洞（集成 Snyk/Dependabot 数据）
   - 自动生成升级提案

4. **Kairos 适配层**（预留）：
   ```python
   # 当 Claude Code 支持 SleepTool / CronCreateTool 时
   if KAIROS_AVAILABLE:
       schedule_background_evolution(interval="daily")
       push_notification_on_critical_finding()
   ```

**价值**：
- 从"被动学习"升级为"主动发现"
- 提前发现技术债务，避免积累
- 为未来 Kairos 模式预留接口

---

### 方向 5：CLI 可视化与状态面板（填补体验空白）

**现状**：所有数据在 JSONL 文件中，用户需要 `cat` 或 `jq` 查看。

**设计**：

```
chk status              # 总览面板
chk status --knowledge  # 知识库统计
chk status --evolution  # 进化历史时间线
chk status --agents     # Agent 使用热力图
chk status --errors     # 错误模式分析
chk status --session    # 当前会话详情
```

**实现细节**：

1. **终端可视化**（使用 `rich` 或 `textual`）：
   ```python
   # 知识库统计面板
   ┌─────────────────────────────────────────────┐
   │  CHK 知识库状态                              │
   ├─────────────────────────────────────────────┤
   │  手工知识: 52 条                             │
   │  进化知识: 47 条  (active: 38, deprecated: 9)│
   │  本月新增: 12 条                             │
   │  平均置信度: 0.72                            │
   └─────────────────────────────────────────────┘

   # Agent 使用热力图
   architect      ████████████ 87%
   backend-dev    ████████░░░░ 62%
   code-reviewer  ██████░░░░░░ 48%
   ralph          ████░░░░░░░░ 31%
   ```

2. **Web UI（可选，基于 Streamlit）**：
   - `harness/dashboard/` 目录
   - 知识库浏览器（搜索、过滤、编辑）
   - 进化历史时间线（可交互）
   - 会话统计图表（折线图、饼图）

3. **Markdown 报告生成**：
   ```bash
   chk report --weekly    # 生成本周报告
   chk report --evolution # 生成进化报告
   ```

**价值**：
- 降低数据查看门槛
- 帮助团队管理者了解 AI 使用情况
- 发现使用模式，优化资源配置

---

## 四、实施路线图

### Phase 1：基础加固（2 周）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| Skill 渐进式加载架构重构 | P0 | 3 天 |
| Git Worktree 隔离机制 | P0 | 3 天 |
| AgentShield 安全扫描器增强 | P1 | 2 天 |
| CLI 状态面板（基础版） | P1 | 2 天 |

### Phase 2：能力升级（4 周）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| PLAYBOOK 剧本系统 | P0 | 5 天 |
| Magic Words 自然语言触发 | P0 | 3 天 |
| 主动进化（代码异味扫描） | P1 | 5 天 |
| Web UI 仪表板（Streamlit） | P2 | 5 天 |
| 依赖进化模块 | P2 | 3 天 |

### Phase 3：生态扩展（持续）

| 任务 | 优先级 | 工作量 |
|------|--------|--------|
| Kairos 适配层预留 | P2 | 2 天 |
| 多项目知识共享 | P2 | 5 天 |
| 社区知识市场 | P3 | 持续 |
| 性能基准测试 | P2 | 3 天 |

---

## 五、关键设计决策

### 决策 1：Worktree 隔离是可选还是强制？

**结论**：可选，默认启用。

- `solo` 模式：禁用 worktree（零开销）
- `team` / `ultra` 模式：自动启用 worktree 隔离
- 用户可通过 `chk config set worktree.enabled false` 关闭

### 决策 2：渐进加载与向后兼容

**结论**：向后兼容，渐进迁移。

- 现有 Skill 目录结构不变
- 新增 `PLAYBOOK.md` 是可选的
- 没有 PLAYBOOK 的 Skill 仍然全量加载
- 过渡期 3 个月，逐步迁移

### 决策 3：安全扫描器 false positive 处理

**结论**：分级处理，不阻断。

- `critical` 级别：阻止会话关闭，必须处理
- `high` 级别：警告，记录到 error.jsonl
- `medium/low` 级别：仅记录，不影响流程
- 支持 `.chk-audit-ignore` 文件忽略特定规则

### 决策 4：主动进化 vs 被动进化

**结论**：并行运行，互补。

- 被动进化：用户会话驱动（现有）
- 主动进化：定时任务驱动（新增）
- 两者共享同一个 knowledge_base.jsonl
- 主动进化提案标注来源 `source: "auto-scan"`

---

## 六、预期效果

| 指标 | 当前 | v2.1 目标 |
|------|------|----------|
| 上下文节省 | 0% | 60-80%（渐进加载） |
| 并行冲突率 | ~15% | < 2%（worktree 隔离） |
| 安全漏洞发现 | 被动 | 主动扫描 |
| 用户使用门槛 | 高（需记命令） | 低（自然语言触发） |
| 数据可视化 | 无 | CLI + Web UI |
| Skill 数量 | 35+ | 50+（含 PLAYBOOK） |

---

## 附录 A：参考资料

1. [Claude Code Plugin Ecosystem Overview](https://www.eesel.ai/blog/claude-code-plugin)
2. [oh-my-claudecode Architecture](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/docs/ARCHITECTURE.md)
3. [Superpowers Plugin Tutorial](https://namiru.ai/blog/superpowers-plugin-for-claude-code-the-complete-tutorial)
4. [Context Cascade Nested Plugin Architecture](https://github.com/DNYoussef/context-cascade)
5. [Claude Code Hooks Complete Guide](https://www.getaiperks.com/en/articles/claude-code-hooks)
6. [Claude Code Architecture Analysis](https://bits-bytes-nn.github.io/insights/agentic-ai/2026/03/31/claude-code-architecture-analysis.html)

---

*设计方案版本: v1.0*
*基于 CHK v0.7.0 + Claude Code 生态 2026 Q2 研究*
