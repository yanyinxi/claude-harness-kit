# Claude Harness Kit (CHK)

> 让 AI 真正"看懂"你的代码库 — Claude Code 插件，安装即用

[![Version](https://img.shields.io/badge/CHK-v0.10.0-blue)](#)
[![Platform](https://img.shields.io/badge/Platform-Claude%20Code%20Plugin-green)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 环境要求

### 必需

| 软件 | 版本要求 | 检查命令 | 未满足时的自动处理 |
|------|----------|----------|-------------------|
| **Node.js** | >= 18 | `node --version` | 安装脚本会提示 |
| **Git** | >= 2.27 | `git --version` | 安装脚本会尝试使用替代方案 |
| **npm** | 随 Node.js 自带 | `npm --version` | 随 Node.js 安装 |
| **Claude Code** | 最新版 | `claude --version` | 从 [claude.ai/code](https://claude.ai/code) 下载 |


### 环境检查命令

```bash
# 一键检查所有依赖
node --version && git --version && claude --version
```

---

## 安装

### 一键安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/yanyinxi/claude-harness-kit.git
cd claude-harness-kit

# 2. 运行安装脚本（自动检测网络状态）
./install.sh
```

安装脚本会：
- ✅ 检测环境并自动选择最优安装方式
- ✅ 清理旧配置避免冲突
- ✅ 添加 marketplace 并安装插件
- ✅ 提供详细的成功/失败信息

### 安装模式本质区别

| 模式 | 命令 | 数据源 | 离线可用 | 更新方式 | 适用场景 |
|------|------|--------|----------|----------|----------|
| **自动模式** | `./install.sh`（默认） | 自动检测 | 降级可用 | 取决于检测结果 | 日常使用（推荐） |
| **本地模式** | `./install.sh --local` | 本地项目目录 | ✅ | 手动 `git pull` | 内网开发、调试、本地修改即时生效 |
| **GitHub 模式** | `./install.sh --github` | 远程克隆 | ❌ | `claude plugins update` | 分享给他人、正式安装 |

**技术细节**：
- **本地模式**：`claude plugins marketplace add` 参数为本地路径，Claude Code 直接从指定目录加载插件文件
- **GitHub 模式**：`claude plugins marketplace add` 参数为 Git URL，Claude Code 会克隆到 `~/.claude/plugins/` 目录，类似 npm 从 registry 安装
- **自动模式**：先尝试连接 GitHub，连通则用 GitHub 模式，不通则自动降级到本地模式


### 验证安装

```bash
# 查看插件状态
claude plugins list

# 应该看到：
# ❯ chk@chk-marketplace
#   Version: 0.10.0
#   Scope: user
#   Status: ✔ enabled
```

### 卸载

```bash
claude plugin uninstall chk --scope user
```

---

## 5 分钟体验

```bash
cd /path/to/your-project   # 进入你的项目
claude                     # 启动 Claude Code
```

在聊天框输入：

```
/chk-init                  # 让 AI 先认识你的项目（首次必做）

/chk-team 实现用户登录功能  # 完整开发流程：需求→设计→编码→测试→审查
```

---

## 命令速查

| 场景 | 命令 | 示例 | 说明 |
|------|------|------|------|
| 初始化项目 | `/chk-init` | `/chk-init` | 让 AI 认识你的项目结构和规范 |
| 开发新功能 | `/chk-team <需求>` | `/chk-team 实现用户权限管理` | 5 阶段流程：需求→设计→编码→测试→审查 |
| 快速修 Bug | `/chk-auto <问题>` | `/chk-auto 修复登录页密码错误不提示` | 全自动端到端，5 分钟搞定 Bug |
| 批量重构 | `/chk-ultra <目标>` | `/chk-ultra 把 30 个文件的 console.log 改成 logging` | 3-5 个 Agent 并行，加速大规模修改 |
| 核心代码（不能出错）| `/chk-ralph <需求>` | `/chk-ralph 实现支付回调验签` | TDD 强制模式，不通过测试不停止 |
| 审查代码 | `/chk-ccg <内容>` | `/chk-ccg 审查这次 PR 的改动` | Claude + Codex + Gemini 三方独立审查 |
| 数据库迁移 | `/chk-pipeline <目标>` | `/chk-pipeline 把 user 表拆成 user + profile` | 严格阶段顺序，上一步输出喂下一步 |
| 简单问答 | `/chk-solo <问题>` | `/chk-solo 这个项目的缓存怎么设计的` | 直接对话，零开销，不用 Agent |
| 查看状态 | `/chk-status` | `/chk-status` | 查看当前模式、Hooks、知识库状态 |
| 清理过期知识 | `/chk-gc` | `/chk-gc` | 扫描上下文，清理漂移和过期的知识 |

**场景选择指南**：

```
简单 ───────────────────────────────────────────────→ 复杂

/chk-solo   /chk-auto   /chk-team   /chk-ultra   /chk-ralph
简单问答    快速修Bug    新功能开发   批量重构      零容忍
```

---

## CHK vs 原生 Claude Code

| 痛点 | 原生 | CHK |
|------|------|-----|
| 新会话要重复描述项目 | 每次说"这是 Spring Boot 项目…" | 自动注入，零配置 |
| 多 Agent 不可用 | 只能串行 | 22 Agent 并行，冲突自动规避 |
| 错误反复犯 | 纠正 100 次，犯错 100 次 | 进化闭环，同错不重现 |
| 团队输出不一致 | 每人风格各异 | 统一 Agent/Skill/Rules 规范 |
| 无安全门禁 | 危险操作无拦截 | Deny-First，自动拦截 |

---

## 核心能力

- **22 个 Agent**：architect / backend-dev / frontend-dev / code-reviewer / security-auditor / qa-tester …
- **36 个 Skill**：testing / tdd / debugging / api-designer / database-designer / performance …
- **8 种模式**：Solo → Auto → Team → Ultra → Pipeline → Ralph → CCG → Default
- **自动进化**：用户纠正 → 置信度累积 → 自动优化 Agent/Skill/Rule

### 不为人知的技术细节

#### 🎯 自动进化系统
- **双知识库闭环**：手工知识（专家经验）+ 进化知识（从使用中学习）自动合并
- **8 维度分析**：agent、skill、rule、instinct 基础 4 维 + performance、interaction、security、context 扩展 4 维
- **效果跟踪**：每个改进都会追踪有效性，防止负面优化（类似 ML 的 reward shaping）

#### 🧠 本能系统
- 监听用户纠正/确认/拒绝，自动记录到本能记录
- 置信度动态演化：低置信度仅建议，高置信度自动应用
- 跨会话记忆：一次学会，终身受益

#### 🛡️ 安全守卫
- **path_guard.py**：所有危险操作必须过守卫，防止 rm -rf 等灾难性命令
- **熔断机制**：进化失败自动回滚，保证系统稳定性
- **白名单目录**：`.claude/` 目录只允许运行时数据，禁止代码文件

#### ⚡ 性能优化
- **Prompt 缓存**：相同上下文复用缓存，减少 token 消耗
- **并行执行**：ultra 模式支持 3-5 Agent 同时工作
- **增量进化**：只分析新会话，不重复处理历史数据

#### 🔧 Claude Code 原生集成
- 完全遵循 Claude Code 官方插件规范（agents/skills/hooks 在根目录）
- 支持 hooks.json 配置 35+ 钩子脚本
- 通过斜杠命令直接触发功能

---

## 目录结构

```
claude-harness-kit/
├── .claude-plugin/       # 插件元数据
│   ├── plugin.json        # 插件清单
│   ├── marketplace.json   # 市场配置
│   └── hooks/             # Hook 配置
├── agents/                # 22 个 Agent 定义 — AI 的角色分工
├── skills/                # 36 个 Skill 规范 — AI 的工作流程
├── commands/              # 斜杠命令
├── hooks/                 # 自动化钩子脚本
├── harness/               # CHK 内部模块
│   ├── evolve-daemon/     # 自动进化引擎 — 越用越聪明
│   ├── knowledge/         # 双知识库 — 专家知识 + 进化知识
│   ├── memory/            # 记忆系统 — 团队经验自动积累
│   ├── rules/             # 团队规范 — 统一输出标准
│   └── cli/               # CHK 命令行工具
├── index.js               # 插件入口
└── package.json
```

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `Plugin not found` | Git 版本不支持 sparse checkout | 更新 Git >= 2.27 或使用手动安装 |
| 装完不生效 | Claude Code 未重启 | 重启 Claude Code 或重新打开终端 |
| 找不到命令 | 命令未加载 | 重新运行 `./install.sh` |
| `Permission denied` | 权限不足 | 检查 Claude Code 权限设置 |
| Node 版本过低 | Node.js 版本老旧 | `brew install node` 或从 nodejs.org 下载 |

### 强制重装

```bash
# 1. 卸载插件
claude plugins uninstall chk --scope user

# 2. 清理配置
rm -rf ~/.claude/plugins/cache/chk*

# 3. 重新安装
./install.sh
```

---

## 常见问题

**Q: 和 Claude Code 冲突吗？**
> 不冲突。CHK 是插件，补充了上下文、协作、进化能力。

**Q: 团队都要装吗？**
> 负责人装一次，成员 `claude plugins install chk` 即可。

**Q: 会自动改我的代码吗？**
> 不会。安全模块锁定，高风险变更需人工审批。

**Q: 装完不生效？**
> 重启 Claude Code，或 `claude plugins update claude-harness-kit`。

---

## 自动更新

CHK 插件支持自动更新检测，当有新版本发布时会主动提醒你安装。

### 版本检测时机

| 时机 | 说明 |
|------|------|
| **首次使用** | 每天首次启动 Claude Code 时自动检查 |
| **手动检查** | 运行 `/chk-status` 命令时会检查 |
| **冷却机制** | 检测间隔 24 小时，避免频繁打扰 |

### 更新通知示例

发现新版本时，你会看到类似提示：

```
╔════════════════════════════════════════════════════════════╗
║  🔔 CHK 插件更新可用                                       ║
╠════════════════════════════════════════════════════════════╣
║  当前版本: 0.9.1                                           ║
║  最新版本: 0.10.0                                          ║
╠════════════════════════════════════════════════════════════╣
║  更新命令: claude plugins update chk                       ║
╚════════════════════════════════════════════════════════════╝
```

### 更新命令

```bash
# 更新到最新版本
claude plugins update chk

# 或在 Claude Code 中输入
/update
```

### 关闭自动检测

如需关闭自动更新检测，在 `.claude/settings.local.json` 中添加：

```json
{
  "CHK": {
    "auto_update": false
  }
}
```

### 技术原理

- 通过 `UserPromptSubmit` 钩子在用户发送消息时触发检查
- 使用 GitHub Releases API 获取最新版本
- 版本比较使用 Semver 规范
- 通知状态保存在 `.claude/data/update_state.json`

---

## 版本历史

| 版本 | 日期 | 改动 |
|------|------|------|
| v0.10.0 | 2026-05-16 | 插件名简化（chk）、一键安装脚本、自动进化系统增强、不为人知的技术细节文档 |
| v0.9.1 | 2026-05-16 | Claude Code 官方规范合规、目录结构重构、8 种执行模式 |
| v0.9.0 | 2026-04 | 初始发布，22 Agent + 36 Skill |

---

MIT License