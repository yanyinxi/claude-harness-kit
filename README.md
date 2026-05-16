# Claude Harness Kit (CHK)

> 让 AI 真正"看懂"你的代码库 — Claude Code 插件，安装即用

[![Version](https://img.shields.io/badge/CHK-v0.9.1-blue)](#)
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

### 可选（增强功能）

| 软件 | 用途 | 检查命令 |
|------|------|----------|
| Python 3 | 进化系统、Hook 脚本 | `python3 --version` |
| Homebrew (macOS) | 快速安装依赖 | `brew --version` |

### 环境检查命令

```bash
# 一键检查所有依赖
node --version && git --version && claude --version
```

---

## 安装

### 方式一：一键安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/yanyinxi/claude-harness-kit.git
cd claude-harness-kit

# 2. 运行安装脚本（自动检查环境、解决依赖）
bash ./harness/cli/install.sh
```

安装脚本会：
- ✅ 检查 Node.js、Git、npm 版本
- ✅ 自动选择最优安装方式（GitHub/marketplace/手动）
- ✅ 复制 Skills 到 `~/.claude/skills/`
- ✅ 安装推荐 MCP 工具（filesystem、playwright）
- ✅ 验证插件状态

### 方式二：手动安装

```bash
# 1. 确保 Claude Code 已安装
claude --version

# 2. 通过 GitHub 安装
claude plugin install yanyinxi/claude-harness-kit --scope user

# 3. 验证
claude plugins list
```

### 方式三：通过 marketplace

```bash
# 1. 添加本地 marketplace
claude plugins marketplace add --scope user /path/to/claude-harness-kit

# 2. 安装
claude plugin install claude-harness-kit --scope user

# 3. 验证
claude plugins list
```

### 验证安装

```bash
# 查看插件状态
claude plugins list

# 应该看到：
# ❯ claude-harness-kit@claude-harness-kit
#   Version: 0.9.1
#   Status: ✔ enabled
```

### 卸载

```bash
claude plugin uninstall claude-harness-kit --scope user
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

| 场景 | 命令 | 示例 |
|------|------|------|
| 初始化项目 | `/chk-init` | `/chk-init` |
| 开发新功能 | `/chk-team <需求>` | `/chk-team 实现用户权限管理` |
| 快速修 Bug | `/chk-auto <问题>` | `/chk-auto 修复登录页密码错误不提示` |
| 批量重构 | `/chk-ultra <目标>` | `/chk-ultra 把 30 个文件的 console.log 改成 logging` |
| 核心代码（不能出错）| `/chk-ralph <需求>` | `/chk-ralph 实现支付回调验签` |
| 审查代码 | `/chk-ccg <内容>` | `/chk-ccg 审查这次 PR 的改动` |
| 数据库迁移 | `/chk-pipeline <目标>` | `/chk-pipeline 把 user 表拆成 user + profile` |
| 简单问答 | `/chk-solo <问题>` | `/chk-solo 这个项目的缓存怎么设计的` |
| 查看状态 | `/chk-status` | `/chk-status` |
| 清理过期知识 | `/chk-gc` | `/chk-gc` |

**场景选择指南**：

```
复杂程度低 ────────────────────────────────────────→ 复杂程度高

/chk-solo       /chk-auto      /chk-team     /chk-ultra     /chk-ralph
（简单问答）     （快速修Bug）   （新功能开发）  （批量重构）    （零容忍）
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
│   └── cli/               # kit 命令行工具
├── index.js               # 插件入口
└── package.json
```

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `Plugin not found` | Git 版本不支持 sparse checkout | 更新 Git >= 2.27 或使用手动安装 |
| 装完不生效 | Claude Code 未重启 | 重启 Claude Code 或重新打开终端 |
| 找不到 chk 命令 | Skills 未复制 | 重新执行 `bash ./harness/cli/install.sh` |
| `Permission denied` | 权限不足 | 检查 Claude Code 权限设置 |
| Node 版本过低 | Node.js 版本老旧 | `brew install node` 或从 nodejs.org 下载 |

### 强制重装

```bash
# 1. 卸载插件
claude plugin uninstall claude-harness-kit --scope user

# 2. 清理配置
rm -rf ~/.claude/plugins/cache/claude-harness-kit

# 3. 重新安装
bash ./harness/cli/install.sh
```

---

## 常见问题

**Q: 和 Claude Code 冲突吗？**
> 不冲突。CHK 是插件，补充了上下文、协作、进化能力。

**Q: 团队都要装吗？**
> 负责人装一次，成员 `claude plugin install yanyinxi/claude-harness-kit` 即可。

**Q: 会自动改我的代码吗？**
> 不会。安全模块锁定，高风险变更需人工审批。

**Q: 装完不生效？**
> 重启 Claude Code，或 `claude plugins update claude-harness-kit`。

---

## 版本历史

| 版本 | 日期 | 改动 |
|------|------|------|
| v0.9.1 | 2026-05-16 | Claude Code 官方规范合规、目录结构重构、8 种执行模式 |
| v0.9.0 | 2026-04 | 初始发布，22 Agent + 36 Skill |

---

MIT License