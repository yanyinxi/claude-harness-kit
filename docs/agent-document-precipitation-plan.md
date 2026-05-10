# Agent 文档沉淀方案 — 完整设计文档

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-10 | 初始版本 |
| v1.1 | 2026-05-10 | 添加通用插件设计、错误记录、性能优化要求 |
| v1.2 | 2026-05-10 | 补充双向交互能力、可视化编辑器、SVG图表、探索网络模式（基于 Thariq HTML Effectiveness 文章） |

---

## 一、问题背景

### 1.1 用户诉求

用户反馈：CHK 项目从需求、架构、开发各阶段都没有文档沉淀，各 Agent 没有文档输出。

**核心需求**：
1. 每次沉淀都需要做成 HTML
2. 页面要美观
3. 逻辑要简单清晰
4. 结构要完整，一看就懂

### 1.2 发现的问题

| 问题 | 描述 | 影响 |
|------|------|------|
| **开发类 Agent 无文档要求** | 8 个 Agent（backend-dev, frontend-dev, database-dev, devops, executor, ralph, migration-dev, qa-tester）完全没有文档产出要求 | 大量工作没有沉淀 |
| **security-auditor 工具缺失** | 有报告格式定义，但缺少 Write 工具 | 无法保存报告 |
| **文档目录不统一** | 不同 Agent 输出到不同位置（output/、docs/、.claude/session-wrap/） | 难以查找 |
| **格式不统一** | session-wrap 输出 .md，不是 HTML | 不满足需求 |
| **缺少转换机制** | 没有 Markdown → HTML 自动转换管道 | 无法生成 HTML |

### 1.3 设计约束

#### 1.3.1 通用插件设计 ⭐

**核心原则**：这是 Claude Code 插件，会被多个团队、多人、多个项目使用。

**要求**：
- 生成的文档必须保存到**当前项目目录**内（`docs/`，不是插件目录）
- 插件本身只包含代码和模板，不存储用户数据
- 每个项目有独立的文档沉淀空间

```
# 插件安装后，在任意项目中使用
$ cd /path/to/project-a
$ claude --plugin chk  # 插件加载
# 生成文档 → /path/to/project-a/docs/artifacts/

$ cd /path/to/project-b
$ claude --plugin chk  # 插件加载
# 生成文档 → /path/to/project-b/docs/artifacts/
```

**实现方式**：
```python
# 所有路径基于 PROJECT_ROOT（当前项目根目录）
PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
DOCS_DIR = PROJECT_ROOT / "docs"  # 用户项目的 docs 目录
```

#### 1.3.2 错误记录 ⭐

**复用现有系统**：
- 位置：`.claude/data/error.jsonl`
- 格式：与现有错误收集系统一致

**错误类型**：
1. Markdown 读取失败
2. HTML 模板加载失败
3. 文档转换异常
4. 目录创建失败
5. Hook 脚本执行失败

**错误记录格式**：
```json
{
  "timestamp": "2026-05-10T12:00:00",
  "type": "doc-generator-error",
  "phase": "convert|verify|wrap",
  "error": "错误描述",
  "file": "相关文件路径",
  "stack": "堆栈信息",
  "recoverable": true,
  "context": {
    "session_id": "xxx",
    "agent": "xxx",
    "doc_type": "xxx"
  }
}
```

**复用机制**：
```python
# harness/hooks/bin/collect_error.py 已有错误收集逻辑
# doc-generator.py 和 doc-verify.py 复用同一逻辑

def log_error(error_data: dict):
    """将错误记录到 error.jsonl，复用现有系统"""
    error_file = PROJECT_ROOT / ".claude" / "data" / "error.jsonl"
    with open(error_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(error_data, ensure_ascii=False) + "\n")
```

#### 1.3.3 性能优化 ⭐

**目标**：文档生成不应成为执行瓶颈

**优化策略**：

| 场景 | 优化方案 | 预期效果 |
|------|---------|---------|
| 单文件转换 | 懒加载模板，按需加载 | 减少内存占用 |
| 批量转换 | 并行处理（multiprocessing）| 提升 3-5x 速度 |
| 会话收尾 | 异步归档，不阻塞主流程 | 零感知延迟 |
| 模板渲染 | 缓存已解析的模板 | 减少重复解析 |
| HTML 输出 | 最小化 DOM 操作 | 加快渲染 |

**性能指标**：
- 单文件转换：< 100ms
- 批量转换（10 个文件）：< 500ms
- 会话收尾 HTML 生成：< 200ms（异步）

**实现**：
```python
# 批量转换使用进程池
from concurrent.futures import ProcessPoolExecutor

def batch_convert(md_files: list[Path], output_dir: Path, doc_type: str):
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(convert_single, f, output_dir, doc_type) for f in md_files]
        return [f.result() for f in futures]
```

**监控**：
- 转换时间写入日志
- 超过阈值时记录 WARNING 到 error.jsonl

---

## 二、全局思考

### 2.1 LLM vs 人类理解力

| 视角 | 更适合的格式 | 原因 |
|------|-------------|------|
| **LLM 处理** | Markdown | 训练数据中大量使用，符号明确，token 更少，结构清晰 |
| **人类阅读** | HTML | 页面美观，样式丰富，可直接浏览器打开 |

### 2.1.1 HTML 的独特优势（基于 Thariq 研究）

Thariq (@trq212) 在《Using Claude Code: The Unreasonable Effectiveness of HTML》中指出，HTML 相比 Markdown 有以下独特优势：

| 优势 | 说明 | CHK 落地方式 |
|------|------|--------------|
| **信息密度** | 表格、SVG、代码高亮、动态交互 | 新增 interactive 类型 |
| **视觉清晰** | 移动端自适应、选项卡导航、插图 | 模板内置响应式设计 |
| **双向交互** | 滑块、旋钮、按钮 | 新增 editor 类型 |
| **易于分享** | S3 链接分享，任何设备可看 | 统一输出到 docs/artifacts/ |
| **数据摄取** | 处理海量上下文 | MCP 集成 |

**核心洞察**：HTML 让人重新回到人机协同的循环中，而不是任由 AI 自己盲目做决定。

**设计决策**：
- LLM 内部传递：保持 **Markdown**（效率高、结构清晰）
- 人类可读输出：生成 **HTML**（页面美观、可浏览器查看）

### 2.2 22 个 Agent 分类分析

| 类别 | Agent 列表 | 文档产出现状 |
|------|-----------|-------------|
| **战略设计** | architect, product-manager, tech-lead | 部分有输出规范 |
| **分析研究** | explore, codebase-analyzer, impact-analyzer, oracle | 无文档产出要求 |
| **开发执行** | backend-dev, frontend-dev, database-dev, devops, executor, ralph | **无文档产出要求** |
| **审查验证** | code-reviewer, security-auditor, qa-tester, test, verifier | 有报告模板但未强制 |
| **编排管理** | orchestrator, learner, gc | 无文档产出要求 |

### 2.3 现有资源盘点

| 组件 | 位置 | 功能 | 状态 |
|------|------|------|------|
| knowledge_recommender.py | harness/knowledge/ | 知识推荐引擎 | ✅ 完整 |
| lifecycle.py | harness/knowledge/ | 生命周期管理 | ✅ 完整 |
| session-wrap SKILL | harness/skills/session-wrap/ | 5阶段收尾流程 | ✅ 完整 |
| gc.py | harness/evolve-daemon/ | 知识垃圾回收 | ✅ 完整 |
| web-knowledge-architecture.html | docs/ | HTML 架构图 | ✅ 静态参考 |
| requirement-analysis SKILL | harness/skills/ | PRD 模板 | ✅ 完整 |
| architecture-design SKILL | harness/skills/ | 架构设计模板 | ✅ 完整 |

---

## 三、技术方案

### 3.0 核心场景设计（基于 Thariq 研究）

#### 3.0.1 需求、计划与探索（Specs, Planning & Exploration）

**场景**：多方案对比、视觉草图、实施计划

**Prompt 示例**：
```markdown
我还没想好新手引导页面要什么风格。
请生成 6 种截然不同的方案——在布局、语气和信息密度上做出差异——
并把它们放在同一个 HTML 文件的网格布局里，方便并排对比。
请在每个方案旁清晰标注所做的取舍权衡。
```

```markdown
请在一个 HTML 文件里创建一份详尽的实施计划。
画一些视觉草图展示数据流向，补充核心代码片段。
排版要清晰，让人容易消化理解。
```

**适用场景**：
- 探索一段代码的其他实现方式
- 并行探索多种视觉设计方案

#### 3.0.2 代码审查与理解（Code Review & Understanding）

**场景**：Diff 渲染、页边注释、流程图

**Prompt 示例**：
```markdown
帮我审查这个 PR，生成一个 HTML 制品来解释它的逻辑。
我对数据流和背压逻辑不太熟悉，请重点剖析这部分。
渲染出真实的代码差异，加上行内注释。
根据严重程度对问题进行颜色编码，加上视觉图表。
```

**适用场景**：
- 创建 PR 的说明文档
- 审查同事或 AI 提交的 PR
- 快速理解代码库中的某个复杂主题

#### 3.0.3 设计与原型（Design & Prototypes）

**场景**：交互动画、参数微调

**Prompt 示例**：
```markdown
我想为结账按钮做个交互原型：点击时播放动画，然后变成紫色。
请生成一个带滑块的 HTML，让我能反复测试不同参数。
提供一个"复制"按钮，一键复制完美参数。
```

**适用场景**：
- 创建设计系统的组件资产
- 直观地微调 UI 组件细节
- 制作充满乐趣的动画交互原型

#### 3.0.4 报告、研究与学习（Reports, Research & Learning）

**场景**：深度报告、SVG 图表、幻灯片

**Prompt 示例**：
```markdown
我一直搞不懂限流器是怎么工作的。
请阅读相关代码，生成一个单页 HTML 讲解文档：
包含令牌桶数据流向图、3-4段带注释的代码片段、"常见陷阱"部分。
请尽情使用 SVG 绘制图表。
```

```markdown
请生成一份本周工作汇报，格式为幻灯片/Deck。
使用 SVG 绘制图表，排版要精美。
```

**适用场景**：
- 总结某个复杂功能的工作原理
- 向别人通俗解释一个晦涩概念
- 给老板生成工作汇报
- 给领导层出具故障复盘报告

#### 3.0.5 自定义编辑界面（Custom Editing Interfaces）

**场景**：拖拽排序、表单编辑、实时预览

**Prompt 示例**：
```markdown
我需要重新梳理 30 个任务单的优先级。
请做成一个 HTML，把每个任务做成可拖拽卡片，
分"现在/接下来/以后/砍掉"四个栏目。
加一个"复制为 Markdown"按钮导出结果。
```

```markdown
请做一个左右对照的编辑器：
左边是可编辑的提示词模板，变量槽要高亮；
右边放 3 个示例输入源，修改左边时右边实时渲染最终效果。
加上字符和 Token 计数器，以及一键复制按钮。
```

**适用场景**：
- 对任务、测试用例、用户反馈进行排序/分类
- 编辑功能开关、环境变量等复杂配置
- 借助实时预览功能调优提示词
- 为长文档、录音文稿添加批注

#### 3.0.6 探索网络模式（Exploration Network）

**场景**：多文档关联、头脑风暴、方案演进

**工作流**：
```
头脑风暴（HTML1）→ 方案选择（HTML2）→ 深入设计（HTML3）→ 实施计划（HTML4）
```

**特点**：
- 多文档交织的思考网络
- 文档间跳转链接
- 探索历史索引

**实现方式**：
```html
<nav class="explorer-nav">
  <a href="brainstorm.html">💡 头脑风暴</a>
  <a href="design-v2.html">🎨 方案选择</a>
  <a href="plan-final.html">📋 实施计划</a>
</nav>
```

### 3.1 整体架构

```
Agent 执行完成
     ↓
生成 Markdown 文档（强制）
     ↓
调用 doc-generator.py 转换为 HTML
     ↓
输出到 docs/artifacts/ (直接查看) ← 项目内目录
     ↓
同时归档到 docs/archives/ (按月组织)
     ↓
Stop Hook 触发 doc-verify.py 验证完整性
     ↓
错误记录到 .claude/data/error.jsonl
     ↓
进化系统统计文档产出健康状态
```

### 3.1.1 项目隔离设计

```
/path/to/project-a/          # 用户项目 A
├── docs/                    # 用户自己的文档目录
│   ├── artifacts/           # Agent 生成的 HTML
│   └── archives/            # 按月归档
└── .claude/                 # 用户项目数据
    └── data/
        └── error.jsonl      # 错误记录

/path/to/project-b/          # 用户项目 B（完全隔离）
├── docs/
│   ├── artifacts/
│   └── archives/
└── .claude/
    └── data/
        └── error.jsonl

~/.claude/plugins/chk/       # 插件本身（无用户数据）
├── harness/
└── hooks/
```

### 3.2 Phase 1: 基础设施

#### 3.2.1 创建 doc-generator.py

**位置**：`harness/knowledge/doc-generator.py`

**核心功能**：
1. `convert` — 将 Markdown 转换为 HTML
2. `session-wrap` — 生成会话总结 HTML
3. `batch` — 批量转换目录下所有 Markdown
4. **`interactive` ⭐** — 生成带交互元素的 HTML
5. **`editor` ⭐** — 生成可视化编辑器 HTML
6. **`explorer` ⭐** — 生成探索网络 HTML

**命令行接口**：
```bash
# 转换单个文件
python3 doc-generator.py convert <md-file> --type <doc-type> --output <dir>

# 生成交互式页面
python3 doc-generator.py interactive --name "动画调整" --params "speed,easing,color"

# 生成编辑器页面
python3 doc-generator.py editor --mode "kanban" --items 30

# 生成探索网络
python3 doc-generator.py explorer --docs "brainstorm,design,plan"

# 会话收尾
python3 doc-generator.py session-wrap --session-id <id> --agents <agents> --output <dir>

# 批量转换
python3 doc-generator.py batch <dir>
```

**错误处理（复用现有系统）**：
```python
# 错误记录到 .claude/data/error.jsonl
def log_error(error_type: str, phase: str, error_msg: str, context: dict):
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "phase": phase,
        "error": error_msg,
        "recoverable": True,
        "context": context
    }
    error_file = PROJECT_ROOT / ".claude" / "data" / "error.jsonl"
    with open(error_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(error_entry, ensure_ascii=False) + "\n")
```

**性能优化**：
```python
# 1. 懒加载模板（按需加载）
def load_template(template_name: str) -> str:
    if template_name not in _template_cache:
        template_path = TEMPLATE_DIR / f"{template_name}.html"
        if template_path.exists():
            _template_cache[template_name] = template_path.read_text(encoding="utf-8")
    return _template_cache.get(template_name, _get_default_template())

# 2. 批量转换并行处理
from concurrent.futures import ProcessPoolExecutor

def batch_convert(md_files: list[Path], output_dir: Path, doc_type: str):
    with ProcessPoolExecutor(max_workers=min(4, os.cpu_count())) as executor:
        futures = [executor.submit(convert_single, f, output_dir, doc_type) for f in md_files]
        return [f.result() for f in futures]

# 3. 异步归档（会话收尾）
def async_archive(source: Path, dest: Path):
    """异步归档，不阻塞主流程"""
    ThreadPoolExecutor().submit(shutil.copy2, source, dest)
```

**文档类型映射**：
| doc-type | 说明 | 模板 | 特色 |
|---------|------|------|------|
| architecture | 架构设计文档 | architecture.html | SVG 架构图 |
| prd | 产品需求文档 | prd.html | 移动端自适应 |
| review | 审查报告（code-review, security） | review.html | Diff 渲染 + 颜色编码 |
| test | 测试报告 | test.html | 图表统计 |
| implementation | 实现报告 | implementation.html | 代码片段高亮 |
| verification | 验证报告 | verification.html | 状态指示器 |
| **interactive** | 参数调整、方案对比 | interactive.html | **滑块、旋钮、选择器** |
| **editor** | 任务排序、配置编辑 | editor.html | **拖拽卡片、表单、导出按钮** |
| **explorer** | 方案探索、多文档关联 | explorer.html | **导航索引、文档跳转** |

#### 3.2.2 创建 HTML 模板

**位置**：`harness/knowledge/_templates/`

| 模板文件 | 用途 |
|---------|------|
| base.html | 基础模板（所有类型的父模板） |
| architecture.html | 架构设计专用 |
| prd.html | PRD 专用 |
| review.html | 审查报告专用 |
| test.html | 测试报告专用 |
| implementation.html | 实现报告专用 |
| **interactive.html** | 交互式参数调整（滑块、旋钮） | ⭐ 新增 |
| **editor.html** | 可视化编辑器（拖拽、表单） | ⭐ 新增 |
| **explorer.html** | 探索网络（多文档导航） | ⭐ 新增 |

**设计风格**：
- 暗色主题（#0f1419 背景）
- 主色调：蓝色 #4fc3f7
- 简洁卡片式布局
- 代码块语法高亮
- 表格自适应宽度

### 3.3 Phase 2: Agent 改造

#### 需要文档输出的 12 个 Agent

| Agent | 必须产出 | 类型 | 输出路径 | 交互能力 |
|-------|---------|------|---------|---------|
| architect | 架构设计文档 | architecture | docs/artifacts/ | SVG 架构图 |
| product-manager | PRD 文档 | prd | docs/artifacts/ | 移动端自适应 |
| code-reviewer | 审查报告 | **review** | docs/artifacts/ | **Diff 渲染、颜色编码** |
| security-auditor | 安全审查报告 | **review** | docs/artifacts/ | **严重程度颜色编码** |
| test | 测试报告 | test | docs/artifacts/ | 图表统计 |
| qa-tester | 测试报告 | test | docs/artifacts/ | 图表统计 |
| backend-dev | 实现报告 | implementation | docs/artifacts/ | 代码高亮 |
| frontend-dev | 实现报告 | **interactive** | docs/artifacts/ | **滑块调参** |
| database-dev | 迁移报告 | implementation | docs/artifacts/ | 流程图 |
| devops | 部署报告 | implementation | docs/artifacts/ | 状态指示器 |
| verifier | 验证报告 | verification | docs/artifacts/ | 状态指示器 |
| tech-lead | 技术设计文档 | architecture | docs/artifacts/ | SVG 架构图 |

#### 统一的文档产出指令（添加到每个 Agent 的 .md 文件末尾）

```markdown
## 文档产出要求 ⭐

完成工作后，**必须**生成并保存文档：

1. 文档类型：`<type>`
2. 输出路径：`docs/artifacts/<session-id>_<agent-name>_<type>.md`
3. **必须调用** doc-generator 转换为 HTML：
   ```bash
   python3 harness/knowledge/doc-generator.py convert \
     docs/artifacts/<name>.md --type <type> --output docs/artifacts/
   ```

### 交互式文档建议

根据场景需要，可以生成带交互能力的 HTML：

| 场景 | 推荐类型 | 交互能力 |
|------|---------|---------|
| 参数调优 | `interactive` | 滑块、旋钮、复制按钮 |
| 方案对比 | `interactive` | 选择器、网格布局 |
| 任务排序 | `editor` | 拖拽卡片、导出按钮 |
| 配置编辑 | `editor` | 表单、依赖校验、导出差异 |
| 方案探索 | `explorer` | 导航索引、文档跳转 |

### 输出流程

1. **生成文档内容** — 使用对应的文档模板
2. **保存 Markdown** — Write 到 docs/artifacts/
3. **调用文档生成器** — Bash 命令转换 HTML
4. **验证输出** — 确认 HTML 文件已生成
5. **（可选）添加交互** — 如需交互能力，调用 interactive/editor/explorer 模式
```

### 3.4 Phase 3: Hook 验证

#### 3.4.1 修改 hooks.json

在 Stop Hook 中添加文档验证：
```json
"Stop": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/bin/doc-verify.py",
        "timeout": 10
      },
      {
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/bin/collect_session.py",
        "timeout": 10
      }
    ]
  }
]
```

#### 3.4.2 创建 doc-verify.py

**位置**：`harness/hooks/bin/doc-verify.py`

**功能**：
1. 读取本次会话的 Agent 调用记录（从 agent_calls.jsonl）
2. 检查各 Agent 是否有对应文档输出
3. 缺失则输出 WARNING（不阻断流程）
4. 输出结构化 JSON 报告

**错误处理**：
```python
# 错误记录到 .claude/data/error.jsonl
try:
    sessions = get_session_data()
except Exception as e:
    log_error("doc-verify-error", "read-session", str(e), {
        "session_id": session_id
    })
    sessions = {}  # fallback
```

**输出格式**：
```json
{
  "session_id": "xxx",
  "timestamp": "2026-05-10T12:00:00",
  "agents_used": ["architect", "backend-dev", "code-reviewer"],
  "documents": [
    {"agent": "architect", "type": "architecture", "files": ["docs/artifacts/xxx.md"]}
  ],
  "missing": [
    {"agent": "backend-dev", "required_type": "implementation"}
  ],
  "status": "WARNING"
}
```

### 3.5 Phase 4: session-wrap 集成

**修改**：`harness/skills/session-wrap/SKILL.md`

在 Phase 4 执行流程中添加 HTML 生成：
```markdown
## Phase 4：执行选中项 + 文档生成

1. 文档更新
2. 自动化建议
3. 经验记录
4. **生成会话总结 HTML** ⭐

执行：
```bash
python3 harness/knowledge/doc-generator.py session-wrap \
  --session-id <session-id> \
  --agents <agents-used> \
  --output docs/artifacts/
```

这会自动：
- 收集所有 Agent 的文档输出
- 合并为会话总结 Markdown
- 转换为 HTML 并应用样式
- 归档到 docs/archives/
```

### 3.6 Phase 5: 进化系统集成

#### 3.6.1 修改 daemon.py

在 run_analysis() 之前添加文档检查：
```python
def run_analysis(config: dict, root: Path, sessions: list[dict]):
    # 1. 检查文档产出
    doc_check_result = check_document_completeness(sessions, root)
    if doc_check_result.get("missing"):
        print(f"📄 文档沉淀检查: {len(doc_check_result['missing'])} 项缺失")
        # 可选：生成文档缺失提案
```

#### 3.6.2 添加每日健康检查任务

```json
{
  "name": "document-health-check",
  "cron": "0 3 * * *",
  "task": "检查文档产出健康状态",
  "actions": [
    "扫描 docs/artifacts/ 目录",
    "统计各 Agent 文档产出频率",
    "检测长期无产出的 Agent",
    "报告到 effect_tracking.jsonl"
  ]
}
```

---

## 四、目录结构

```
docs/
├── archives/                    # 归档文档（按月组织）
│   └── <year>-<month>/
│       ├── architecture/
│       ├── prd/
│       ├── review/
│       ├── test/
│       ├── implementation/
│       └── verification/
├── artifacts/                   # HTML 产物（可直接查看）
│   └── <session-id>-<type>-<timestamp>.html
├── _templates/                  # HTML 模板
│   ├── base.html
│   ├── architecture.html
│   ├── prd.html
│   ├── review.html
│   ├── test.html
│   ├── implementation.html
│   ├── interactive.html          # ⭐ 交互式模板
│   ├── editor.html               # ⭐ 编辑器模板
│   ├── explorer.html              # ⭐ 探索网络模板
│   └── _components.html          # ⭐ 通用组件库
└── index.html                    # 文档索引页面（可选）
```

---

## 五、HTML 模板设计

### 5.0 交互元素设计（基于 Thariq 最佳实践）

#### 5.0.1 滑块组件（Range Slider）

```html
<div class="control-group">
  <label class="control-label" for="speed">
    <span class="control-title">动画速度</span>
    <span class="control-value" id="speed-value">300ms</span>
  </label>
  <input type="range" id="speed" min="50" max="1000" value="300" step="50"
         class="range-slider">
</div>
```

#### 5.0.2 复制按钮（Copy Button）

```html
<button class="copy-btn" onclick="copyToClipboard(getParams())">
  <span class="icon">📋</span> 复制参数
</button>

<script>
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('已复制到剪贴板');
  });
}
</script>
```

#### 5.0.3 拖拽卡片（Draggable Cards）

```html
<div class="kanban-board">
  <div class="kanban-column" data-column="now">
    <h3>现在</h3>
    <div class="card draggable" draggable="true" data-id="task-1">
      任务卡片
    </div>
  </div>
  <!-- Next, Later, Cut columns -->
</div>
```

#### 5.0.4 颜色编码（Color Coding by Severity）

```html
<style>
.severity-critical { background: #ef5350; }
.severity-high { background: #ff7043; }
.severity-medium { background: #ffb74d; }
.severity-low { background: #81c784; }
</style>
```

#### 5.0.5 实时预览（Live Preview）

```html
<div class="split-editor">
  <div class="editor-left">
    <textarea id="template-input" oninput="updatePreview()"></textarea>
  </div>
  <div class="editor-right">
    <div id="preview-output"></div>
  </div>
</div>
```

#### 5.0.6 导出按钮类型

| 类型 | 用途 | 示例 |
|------|------|------|
| 复制为 Markdown | 排序结果导出 | `## 任务清单\n- [x] ...` |
| 复制为 JSON | 配置导出 | `{"key": "value"}` |
| 复制差异 | 仅变更部分 | `key: new_value` |
| 复制为 Prompt | 参数导出 | `Set speed=300ms, easing=ease-out` |

### 5.1 基础样式（base.html）

```css
:root {
  --bg-primary: #0f1419;
  --bg-secondary: #1a2332;
  --bg-card: #1e2a3a;
  --border: #2d3f5a;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --accent: #4fc3f7;
  --accent-success: #81c784;
  --accent-warning: #ffb74d;
  --accent-danger: #ef5350;
}
```

### 5.2 页面结构

```
┌─────────────────────────────────────────┐
│  Header                                 │
│  ┌─────────────────────────────────┐    │
│  │ 标题                    Agent标签│    │
│  │ 时间戳                         │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│  Content                                │
│  ┌─────────────────────────────────┐    │
│  │                                 │    │
│  │  Markdown 转换的内容             │    │
│  │                                 │    │
│  │  代码块、表格、列表              │    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│  Footer                                 │
│  CHK Document | Generated by CLAUDE     │
└─────────────────────────────────────────┘
```

---

## 六、TODO 清单

### Phase 1: 基础设施

| # | 任务 | 状态 | 文件 |
|---|------|------|------|
| 1 | 创建 doc-generator.py（含 interactive/editor/explorer 模式） | ⬜ | harness/knowledge/doc-generator.py |
| 2 | 创建 base.html 模板 | ⬜ | harness/knowledge/_templates/base.html |
| 3 | 创建 architecture.html 模板 | ⬜ | harness/knowledge/_templates/architecture.html |
| 4 | 创建 prd.html 模板 | ⬜ | harness/knowledge/_templates/prd.html |
| 5 | 创建 review.html 模板 | ⬜ | harness/knowledge/_templates/review.html |
| 6 | 创建 test.html 模板 | ⬜ | harness/knowledge/_templates/test.html |
| 7 | 创建 implementation.html 模板 | ⬜ | harness/knowledge/_templates/implementation.html |
| 8 | **创建 interactive.html 模板** ⭐ | ⬜ | **滑块、旋钮、选择器组件** |
| 9 | **创建 editor.html 模板** ⭐ | ⬜ | **拖拽卡片、表单、导出按钮** |
| 10 | **创建 explorer.html 模板** ⭐ | ⬜ | **探索网络导航组件** |
| 11 | 创建 _components.html（通用交互组件库）| ⬜ | **可复用组件** |

### Phase 2: Agent 改造

| # | Agent | 状态 |
|---|-------|------|
| 12 | architect | ⬜ |
| 13 | product-manager | ⬜ |
| 14 | tech-lead | ⬜ |
| 15 | code-reviewer | ⬜ |
| 16 | security-auditor | ⬜ |
| 17 | test | ⬜ |
| 18 | qa-tester | ⬜ |
| 19 | backend-dev | ⬜ |
| 20 | frontend-dev | ⬜ |
| 21 | database-dev | ⬜ |
| 22 | devops | ⬜ |
| 23 | verifier | ⬜ |

### Phase 3: Hook 验证

| # | 任务 | 状态 | 文件 |
|---|------|------|------|
| 24 | 创建 doc-verify.py | ⬜ | harness/hooks/bin/doc-verify.py |
| 25 | 更新 hooks.json | ⬜ | harness/hooks/hooks.json |

### Phase 4: session-wrap 集成

| # | 任务 | 状态 | 文件 |
|---|------|------|------|
| 26 | 修改 session-wrap SKILL | ⬜ | harness/skills/session-wrap/SKILL.md |

### Phase 5: 进化系统集成

| # | 任务 | 状态 | 文件 |
|---|------|------|------|
| 27 | 集成文档检查到 daemon.py | ⬜ | harness/evolve-daemon/daemon.py |

---

## 七、关键文件清单

### 新建文件

| 文件 | 用途 | ⭐新增 |
|------|------|--------|
| `harness/knowledge/doc-generator.py` | Markdown → HTML 转换器核心 | 含 interactive/editor/explorer 模式 |
| `harness/knowledge/_templates/base.html` | 基础 HTML 模板 | |
| `harness/knowledge/_templates/architecture.html` | 架构设计模板 | SVG 架构图 |
| `harness/knowledge/_templates/prd.html` | PRD 模板 | |
| `harness/knowledge/_templates/review.html` | 审查报告模板 | Diff 渲染、颜色编码 |
| `harness/knowledge/_templates/test.html` | 测试报告模板 | |
| `harness/knowledge/_templates/implementation.html` | 实现报告模板 | |
| `harness/knowledge/_templates/interactive.html` | 交互式模板 | ⭐ 滑块、旋钮、选择器 |
| `harness/knowledge/_templates/editor.html` | 编辑器模板 | ⭐ 拖拽卡片、表单 |
| `harness/knowledge/_templates/explorer.html` | 探索网络模板 | ⭐ 导航索引 |
| `harness/knowledge/_templates/_components.html` | 通用交互组件库 | ⭐ 可复用组件 |
| `harness/hooks/bin/doc-verify.py` | 文档验证器 | |

### 修改文件

| 文件 | 修改内容 |
|------|---------|
| `harness/hooks/hooks.json` | 添加 Stop Hook 文档验证 |
| `harness/skills/session-wrap/SKILL.md` | 添加 HTML 生成指令 |
| `harness/evolve-daemon/daemon.py` | 添加文档检查节点 |
| 12 个 Agent 定义文件 | 添加强制文档输出指令 |

### Agent 定义文件列表

```
harness/agents/architect.md
harness/agents/product-manager.md
harness/agents/tech-lead.md
harness/agents/code-reviewer.md
harness/agents/security-auditor.md
harness/agents/test.md
harness/agents/qa-tester.md
harness/agents/backend-dev.md
harness/agents/frontend-dev.md
harness/agents/database-dev.md
harness/agents/devops.md
harness/agents/verifier.md
```

---

## 八、验证方法

1. 运行一个完整的 Team 模式会话
2. 检查 `docs/artifacts/` 是否生成 HTML 文件
3. 检查 `docs/archives/` 是否有按月归档的文档
4. 验证各 Agent 的文档输出是否完整
5. 检查进化系统的文档健康报告

---

## 九、风险与备选方案

| 风险 | 缓解措施 |
|------|---------|
| Agent "忘记"输出文档 | Hook 层强制验证 + WARNING 提醒 |
| Markdown → HTML 转换失败 | fallback 到基础模板，保持可用；错误记录到 error.jsonl |
| 文档产出影响执行效率 | 异步归档，不阻塞主流程；并行处理批量转换 |
| 目录创建失败 | 自动创建父目录；错误记录到 error.jsonl |
| 跨项目使用插件 | 强制使用 PROJECT_ROOT，文档保存在用户项目内 |

### 九.1 错误恢复机制

```python
# 任何阶段出错，记录到 error.jsonl 并继续执行
def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_error(
            error_type="doc-system-error",
            phase=func.__name__,
            error_msg=str(e),
            context={"args": str(args)}
        )
        return None  # fallback 返回 None，不阻断流程
```

### 九.2 项目隔离验证

```python
# 确保文档只写入用户项目目录
PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
DOCS_DIR = PROJECT_ROOT / "docs"

# 安全检查：禁止写入插件目录
if str(DOCS_DIR).startswith(str(PLUGIN_ROOT)):
    raise SecurityError("禁止写入插件目录")
```

---

## 十、FAQ（常见问题解答）

### 10.1 HTML vs Markdown 效率

| 问题 | 回答 |
|------|------|
| Token 效率？ | 确实更费，但 1M 上下文下可忽略。信息密度和阅读率更重要。 |
| 生成速度？ | 比 Markdown 慢 2-4 倍，但物超所值。 |
| 什么时候用 Markdown？ | 仅用于 LLM 内部传递（效率高）。人类输出统一用 HTML。 |

### 10.2 版本控制

| 问题 | 回答 |
|------|------|
| HTML Diff 很乱？ | **最大痛点**。缓解方案：分离数据层（JSON）和展示层（HTML）。 |
| 如何追踪变更？ | 使用 `docs/artifacts/` 作为快照，原始数据存入 JSON。 |
| Git 提交？ | 提交 Markdown 原稿，HTML 作为制品不上传 Git。 |

### 10.3 设计一致性

| 问题 | 回答 |
|------|------|
| 风格不统一？ | 先生成一个"设计系统 HTML"作为参考模板。 |
| 怎么用公司品牌？ | 让 Claude 扫描现有代码库，生成专属设计系统文件。 |

### 10.4 简化 Prompt 指南

**直接说需求，不需要复杂设置**：
```markdown
"生成一个 HTML 制品，展示我的代码差异"
"做一个拖拽卡片排序界面"
"创建一个交互式限流器讲解页面"
```

---

## 十一、依赖关系

```
Phase 1 (基础设施)
    ↓
    ├─ doc-generator.py
    └─ HTML 模板
          ↓
Phase 2 (Agent 改造) ← 依赖 Phase 1
    ↓
Phase 3 (Hook 验证) ← 依赖 Phase 1
    ↓
Phase 4 (session-wrap) ← 依赖 Phase 1
    ↓
Phase 5 (进化集成) ← 依赖 Phase 3
```

---

**最后更新**: 2026-05-10
**方案版本**: v1.2
**状态**: 待 review

## 十二、参考资源

| 资源 | 链接 | 说明 |
|------|------|------|
| Thariq 原文 | https://x.com/trq212/status/2052809885763747935 | Twitter 原文 |
| 示例展示 | https://thariqs.github.io/html-effectiveness/ | 大量 HTML 示例 |
| baoyu 翻译 | https://baoyu.io/translations/2026-05-08/trq212-status-2052809885763747935 | 中文翻译 |