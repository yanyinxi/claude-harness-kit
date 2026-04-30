# Claude Harness Kit

Claude Code 团队级 AI 驾驭工具包 — Human steers, Agents execute.

借鉴 OpenAI Harness Engineering 方法论，提供多 Agent 协作、通用 Skills/Rules、知识生命周期管理、持续进化能力。

## 快速开始

```bash
# 克隆插件
git clone https://github.com/yanyinxi/claude-harness-kit.git

# 注册为 Claude Code 插件
claude plugins install /path/to/claude-harness-kit

# 初始化新项目
./cli/kit.sh init

# 扫描存量项目
./cli/kit.sh scan --repo /path/to/project
```

## 目录结构

```
claude-harness-kit/
├── agents/                  # 22 个通用 Agent
├── skills/                  # 19 个通用 Skill
├── rules/                   # 6 条通用规则
├── hooks/                   # 7 个 Hook 事件 + 8 脚本
├── knowledge/               # 知识生命周期系统
├── evolve-daemon/           # 进化守护进程
├── cli/                     # 命令行工具
├── docs/                    # 设计文档
└── .claude-plugin/          # 插件元数据
```

## 核心能力

### 多 Agent 并行编排
- 冲突检测矩阵 (A ∩ B = ∅ → 可并行)
- TaskFile 协议 (阶段间文件交接)
- Mailbox 机制 (Agent 间通信)
- Checkpoint 系统 (上下文压缩恢复)

### 5 阶段执行流
Research(并行分析) → Plan(串行设计) → Implement(并行编码) → Verify(并行审查+串行修复) → Ship(交付)

### 持续进化
- Instinct System: 用户纠正 → 置信度累积 (0.3→0.5→0.7→0.9)
- evolve-daemon: 数据采集 → 语义提取 → 分析 → 提案 → 应用
- 进化回滚: 7 天观察期 + 自动熔断
- 知识生命周期: draft → verified → proven，自动衰减

### 安全保障
- Deny-First: 安全拦截优先于功能放行
- 审查 Agent 只读: code-reviewer / security-auditor / oracle
- PreToolUse 危险命令拦截

## 测试

```bash
# 并行协议验证 (7 套件)
python3 .claude/tests/test_parallelism_protocol.py

# 全链路进化测试 (18 套件)
python3 .claude/tests/test_full_link_evolution.py
```

## License

MIT
