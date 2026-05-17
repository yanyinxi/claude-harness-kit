# CHK 记忆系统与进化系统整合方案

> 目标：连接记忆系统与进化系统，实现"越用越聪明"的自动化闭环

## 重要发现（Claude Code 官方规范）

| 发现 | 内容 |
|------|------|
| **async 参数** | ✅ 官方支持，示例：`"async": false` |
| **optional 参数** | ❌ 未找到官方支持，建议不使用 |
| **会话 ID** | ✅ `CLAUDE_CODE_SESSION_ID` 环境变量可用 |
| **timeout** | ✅ 官方支持 |

**hooks.json 官方配置格式**：
```json
{
  "$schema": "https://claude.com/docs/claude-code/hooks",
  "hooks": {
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 ...",
        "timeout": 5,
        "async": false
      }]
    }]
  }
}
```

## 一、背景与目标

### 1.1 问题描述

当前 CHK 存在两个独立系统：

| 系统 | 定位 | 数据流 |
|------|------|--------|
| **进化系统** (evolve-daemon) | 自动化改进引擎 | sessions.jsonl → 分析 → 提案 → 应用 |
| **记忆系统** (memory-inject.sh) | 上下文参考层 | MEMORY.md → 注入 → 对话 |

**问题**：两个系统数据断裂，进化产生的知识无法通过记忆系统传递给 AI。

### 1.2 整合目标

```
┌─────────────────────────────────────────────────────────────────┐
│                     CHK 整合后的闭环系统                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   【用户工作】                                                   │
│       ↓                                                         │
│   sessions.jsonl / error.jsonl ──→ 进化系统分析                   │
│       ↓                                       ↓                  │
│   用户纠正 (observe.sh) ──→ 置信度演化 ──→ 知识固化               │
│       ↓                                       ↓                  │
│   knowledge_base.jsonl ─────────────────→ 记忆系统同步          │
│       ↓                                       ↓                  │
│   MEMORY.md 更新 ──→ memory-inject.sh ──→ AI 上下文              │
│       ↓                                                        │
│   AI 应用新知识 ──→ 验证成功 ──→ 置信度提升 ──→ 循环              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、核心设计决策（已确认）

| 决策 | 选择 | 理由 |
|------|------|------|
| **同步时机** | 立即同步 | 新知识生成后立即可用，用户立即感知 |
| **同步内容** | 只同步摘要 | 保持 MEMORY.md 简洁，避免文件膨胀 |
| **本能注入阈值** | confidence >= 0.7 | 高置信度更可靠，避免误导 |
| **验证后处理** | 自动更新 | 进化系统已有验证机制，无需重复人工确认 |

---

## 三、实现步骤（TODO 清单）

### Phase 1: 本能记录读取（优先级 P0）

**目标**：memory-inject.sh 读取 instinct-record.json 高置信度本能

#### TODO 1.1: 创建本能读取模块

- [ ] **文件**: `harness/_core/instinct_reader.py`
- **功能**:
  - 读取 instinct-record.json
  - 过滤 confidence >= 0.7 的本能
  - 生成注入文本（带置信度标注）

```python
# 核心函数
def get_high_confidence_instincts(min_confidence: float = 0.7) -> list[dict]:
    """获取高置信度本能列表"""

def format_instinct_for_injection(instinct: dict) -> str:
    """格式化本能为注入文本"""
```

#### TODO 1.2: 更新 memory-inject.sh

- [ ] **文件**: `hooks/bin/memory-inject.sh`
- **修改**:
  - 调用 instinct_reader.py 读取本能
  - 在输出中添加【本能记录】段落
  - 会话级状态管理（首次注入 L0，后续关键词匹配）

#### TODO 1.3: 添加本能状态管理

- [ ] **文件**: `harness/_core/instinct_state.py`
- **功能**:
  - 跟踪当前会话已注入的本能
  - 避免重复注入相同本能

#### TODO 1.4: 编写测试

- [ ] **文件**: `harness/tests/test_instinct_reader.py`
- **测试用例**:
  - 读取本能记录
  - 过滤阈值
  - 格式化输出

---

### Phase 2: 进化知识同步（优先级 P1）

**目标**：进化系统产生知识后，同步到 MEMORY.md

#### TODO 2.1: 创建知识同步模块

- [ ] **文件**: `harness/evolve-daemon/memory_sync.py`
- **功能**:
  - 监听 knowledge_base.jsonl 变化
  - 生成 MEMORY.md 摘要
  - 追加到 MEMORY.md

```python
# 核心函数
def sync_to_memory(kb_entry: dict, memory_md: Path) -> bool:
    """同步知识到 MEMORY.md"""

def generate_memory_summary(kb_entry: dict) -> str:
    """生成记忆摘要"""
    # 输出格式：| knowledge_{id}.md | 知识摘要 | confidence: 0.85 |
```

#### TODO 2.2: 集成到进化系统

- [ ] **文件**: `harness/evolve-daemon/apply_change.py`
- **修改**:
  - 在知识固化成功后调用 memory_sync.py
  - 传递知识条目和摘要

#### TODO 2.3: 更新 MEMORY.md 格式

- [ ] **文件**: `harness/memory/MEMORY.md`
- **修改**:
  - 添加"## 三、进化知识"部分
  - 格式：表格，包含知识文件、摘要、置信度

```markdown
## 三、进化知识（自动生成）

| 来源文件 | 知识摘要 | 置信度 | 更新时间 |
|---------|---------|--------|----------|
| `knowledge_evolved/xxx.md` | 修复了 xxx 问题... | 0.85 | 2026-05-17 |
```

#### TODO 2.4: 编写测试

- [ ] **文件**: `harness/tests/test_memory_sync.py`
- **测试用例**:
  - 知识同步
  - MEMORY.md 格式验证
  - 重复同步处理

---

### Phase 3: 用户感知增强（优先级 P2）

**目标**：用户知道自己的纠正是否被捕获

#### TODO 3.1: 添加捕获通知

- [ ] **文件**: `hooks/bin/memory-inject.sh`
- **修改**:
  - 在输出中添加【本次捕获】段落（如果有新知识）

```bash
# 示例输出
══════════════════════════════════════════════════════════════
【项目记忆】harness/memory/ — 来自 CHK 记忆系统
══════════════════════════════════════════════════════════════

## 一、开发行为准则

...

──────────────────────────────────────────────────────────────
【本次捕获】✓ 已记录到记忆系统
  • 用户纠正：不要用 eval，用 json.loads
──────────────────────────────────────────────────────────────
```

#### TODO 3.2: 添加通知状态文件

- [ ] **文件**: `.claude/data/.capture_notifications.json`
- **功能**:
  - 记录本次会话捕获的知识
  - 用户可查看 `/chk-capture` 查看历史

---

### Phase 4: 会话状态管理（优先级 P2）

**目标**：记忆注入只在会话首次输入时触发 L0，后续关键词匹配 L1

#### TODO 4.1: 重写 memory-inject.sh

- [ ] **文件**: `hooks/bin/memory-inject.sh`（重写）
- **新逻辑**:
  ```bash
  # 1. 获取会话 ID
  SESSION_ID=${CLAUDE_SESSION_ID:-$(date +%s)}

  # 2. 检查状态文件
  STATE_FILE=".claude/data/.memory_session_${SESSION_ID}.json"

  if [ -f "$STATE_FILE" ]; then
    # 已注入 L0，检查关键词匹配 L1
    check_keyword_match
  else
    # 首次注入 L0
    inject_L0
    create_state_file
  fi
  ```

#### TODO 4.2: 添加关键词匹配逻辑

- [ ] **文件**: `harness/_core/keyword_matcher.py`
- **功能**:
  - 定义关键词映射
  - 返回匹配的记忆文件列表

```python
KEYWORD_MAP = {
    "testing": ["测试", "test", "pytest", "单元测试"],
    "refactor": ["重构", "refactor", "优化代码"],
    "security": ["安全", "security", "漏洞", "审计"],
    "git": ["git", "commit", "branch", "merge"],
    "api": ["api", "接口", "endpoint", "rest"],
}
```

#### TODO 4.3: 状态文件清理

- [ ] **文件**: `hooks/bin/memory-cleanup.sh`
- **功能**:
  - 会话结束时清理状态文件
  - 或次日首次启动时清理所有状态

---

### Phase 5: 验证与文档（优先级 P3）

#### TODO 5.1: 更新进化系统文档

- [ ] **文件**: `harness/docs/INDEX.md`
- **添加**:
  - 记忆系统整合说明
  - 数据流图

#### TODO 5.2: 更新 MEMORY.md 说明

- [ ] **文件**: `harness/memory/MEMORY.md`
- **添加**:
  - 进化知识部分说明
  - 置信度说明

#### TODO 5.3: 端到端测试

- [ ] **文件**: `harness/tests/test_full_memory_loop.py`
- **测试场景**:
  1. 用户纠正 → 观察 → 本能记录
  2. 本能置信度提升 → 达到 0.7
  3. memory-inject 注入本能
  4. AI 应用本能 → 验证成功
  5. 知识同步到 MEMORY.md

---

## 四、文件修改清单

| 文件 | 操作 | Phase | 优先级 |
|------|------|-------|--------|
| `harness/_core/instinct_reader.py` | 新建 | P0 | P0 |
| `harness/_core/instinct_state.py` | 新建 | P0 | P0 |
| `harness/_core/keyword_matcher.py` | 新建 | P2 | P2 |
| `harness/evolve-daemon/memory_sync.py` | 新建 | P1 | P1 |
| `hooks/bin/memory-inject.sh` | 重写 | P0/P2 | P0 |
| `hooks/bin/memory-cleanup.sh` | 新建 | P2 | P2 |
| `harness/evolve-daemon/apply_change.py` | 修改 | P1 | P1 |
| `harness/memory/MEMORY.md` | 修改 | P1/P3 | P1 |
| `harness/tests/test_instinct_reader.py` | 新建 | P0 | P0 |
| `harness/tests/test_memory_sync.py` | 新建 | P1 | P1 |
| `harness/tests/test_full_memory_loop.py` | 新建 | P3 | P3 |

---

## 五、数据流图

```
┌─────────────────────────────────────────────────────────────────┐
│                         Phase 0: 本能读取                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   instinct-record.json                                          │
│        ↓                                                        │
│   instinct_reader.py (过滤 >=0.7)                               │
│        ↓                                                        │
│   memory-inject.sh ──→ AI 上下文                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         Phase 1: 知识同步                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   knowledge_base.jsonl (新知识)                                  │
│        ↓                                                        │
│   memory_sync.py (生成摘要)                                      │
│        ↓                                                        │
│   MEMORY.md (追加)                                              │
│        ↓                                                        │
│   下次会话注入到 AI 上下文                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         Phase 2: 用户感知                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   observe.sh (捕获纠正)                                          │
│        ↓                                                        │
│   capture_notifications.json                                     │
│        ↓                                                        │
│   memory-inject.sh (显示捕获状态)                                 │
│        ↓                                                        │
│   用户看到"✓ 已记录"                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 六、验证测试场景

### 场景 1: 本能注入

```bash
# 准备：instinct-record.json 有 confidence=0.75 的本能
# 期望：memory-inject.sh 输出高置信度本能
bash hooks/bin/memory-inject.sh
# 检查输出包含【本能记录】
```

### 场景 2: 知识同步

```bash
# 准备：knowledge_base.jsonl 有新知识
# 操作：运行 apply_change 成功应用知识
# 期望：MEMORY.md 追加了新条目
grep "knowledge_evolved" harness/memory/MEMORY.md
```

### 场景 3: 用户感知

```bash
# 操作：触发 observe.sh（用户纠正）
# 期望：memory-inject.sh 输出"✓ 已记录到记忆系统"
```

### 场景 4: 会话状态

```bash
# 首次输入：触发 L0 注入
# 第二次输入：触发关键词匹配 L1
# 第三次输入（无关键词）：无注入
```

---

## 七、风险与回退

| 风险 | 缓解措施 |
|------|----------|
| MEMORY.md 膨胀 | 只同步摘要，定期归档旧条目 |
| 本能误注入 | 阈值 0.7（高置信度） |
| 循环依赖 | 进化系统不依赖 memory-inject |
| 测试覆盖不足 | 端到端测试覆盖完整闭环 |

**回退方案**：
- 如需禁用记忆注入，在 hooks.json 中注释 memory-inject.sh
- 如需禁用知识同步，在 config.yaml 中设置 `memory_sync.enabled: false`