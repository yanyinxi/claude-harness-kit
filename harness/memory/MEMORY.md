# Memory Index — CHK 项目核心记忆

## 一、开发行为准则（6条）

| 文件 | 核心要点 |
|------|----------|
| `feedback_use_agents_not_self.md` | 需求必须走Agent，除非单行fix/纯问答 |
| `feedback_verify_before_claiming_done.md` | 声明完成前必须用ls/git diff验证 |
| `feedback_deep_analysis_first_pass.md` | 分析必须一次穷尽，不逐层发现 |
| `feedback_file_write_parent_mkdir.md` | write前加 `path.parent.mkdir(parents=True)` |
| `feedback_settings_replace_all.md` | Edit工具用 `replace_all: true` |
| `feedback_memory_location_rules.md` | 项目记忆→harness/memory/，跨项目→.claude/ |

## 二、项目知识（4条）

| 文件 | 核心要点 |
|------|----------|
| `chk-plugin-specification-fixes.md` | 插件规范：hooks扁平化、Agent有id、Rule有name |
| `feedback_claude_code_official_first.md` | 官方能力优先，14个Hook事件、context/fork |
| `reference_claude_code_lib_import.md` | .claude/自动加入sys.path；三元else不能返回None |
| `code-comment-standards.md` | 代码必须中文注释：作用、原因、目的 |

## 记忆文件路径规则

```
这个记忆只跟CHK项目有关吗？
  → 是 → harness/memory/<name>.md
  → 否 → .claude/projects/<hash>/memory/<name>.md
```