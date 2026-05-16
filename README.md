# Claude Harness Kit (CHK)

> 让 AI 真正"看懂"你的代码库 — Claude Code 插件，安装即用

[![Version](https://img.shields.io/badge/CHK-v0.9.0-blue)](#)
[![Platform](https://img.shields.io/badge/Platform-Claude%20Code%20Plugin-green)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 痛点 & 目标

**AI 写代码不慢，但"不懂你的项目"是致命的**：每次新会话要重新描述项目 → 团队 20 人输出风格各异 → 纠正过的错反复犯 → 100+ 存量代码库没人敢让 AI 碰。

**CHK 解决的就是这个**：让 AI 一进会话就懂项目，22 个 Agent 并行协作，错误自动进化不重现。目标是把 20 人团队 + 100+ 代码库的 AI 开发效率提升 **2.5x**。

---

## 安装

```bash
# 1. 克隆
git clone https://github.com/yanyinxi/claude-harness-kit.git
cd claude-harness-kit

# 2. 一键安装
bash ./harness/cli/install.sh

# 3. 验证
claude plugins list
# 看到 ✔ claude-harness-kit 即成功


### 卸载插件（如果不想用了执行下面命令）
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
├── agents/        # 22 个 Agent 定义 — AI 的角色分工
├── skills/        # 36 个 Skill 规范 — AI 的工作流程
├── hooks/         # SessionStart/Stop 等自动化钩子
├── harness/
│   ├── evolve-daemon/  # 自动进化引擎 — 越用越聪明
│   ├── knowledge/      # 双知识库 — 专家知识 + 进化知识
│   ├── memory/         # 记忆系统 — 团队经验自动积累
│   ├── rules/          # 团队规范 — 统一输出标准
│   └── cli/            # kit 命令行工具
├── index.js       # 插件入口
└── package.json
```

---

## FAQ

**Q: 和 Claude Code 冲突吗？**
> 不冲突。CHK 是插件，补充了上下文、协作、进化能力。

**Q: 团队都要装吗？**
> 负责人装一次，成员 `claude plugins install claude-harness-kit` 即可。

**Q: 会自动改我的代码吗？**
> 不会。安全模块锁定，高风险变更需人工审批。

**Q: 装完不生效？**
> 重启 Claude Code，或 `claude plugins update claude-harness-kit`。

---

## 故障排查

| 问题 | 解决 |
|------|------|
| `Plugin not found` | `claude plugins marketplace add --scope local $(pwd)` 然后重装 |
| 装完不生效 | 重启 Claude Code |
| 找不到 chk 命令 | 重新执行 `bash ./harness/cli/install.sh` |

---

MIT License
