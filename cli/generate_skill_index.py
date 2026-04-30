#!/usr/bin/env python3
"""
Skill INDEX.md 自动生成脚本。

从每个 Skill 的 SKILL.md 提取标题 + 第一段描述，生成 ~50 tokens 的渐进索引。
kit init 时调用，或独立运行: python3 cli/generate_skill_index.py <skills-dir>
"""
import re
import sys
from pathlib import Path


SKILL_MARKDOWN_TEMPLATE = """# {name} — 技能索引

> 自动生成 by kit init — 不要手动编辑此文件

## 概览
{description}

## 触发场景
{trigger}

## 相关规则
{related_rules}
"""


def extract_skill_meta(skill_dir: Path) -> dict:
    """从 SKILL.md 提取元信息"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {}

    text = skill_md.read_text(encoding="utf-8")

    # 提取标题（第一个 # 后面）
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else skill_dir.name

    # 提取第一段（非空正文段落，在 frontmatter 之后）
    lines = text.splitlines()
    # 跳过 frontmatter
    idx = 0
    if lines and lines[0].strip() == "---":
        idx = 1
        while idx < len(lines) and lines[idx].strip() != "---":
            idx += 1
        idx += 1

    # 找第一段非空文字
    description = ""
    for i in range(idx, min(idx + 20, len(lines))):
        line = lines[i].strip()
        if line and not line.startswith("#") and len(line) > 20:
            # 取第一段，限制 tokens
            description = line[:200]
            break

    return {
        "name": title,
        "description": description or "无描述",
        "dir": skill_dir.name,
    }


def generate_skill_index(skills_dir: Path) -> int:
    """为所有 skill 目录生成 INDEX.md"""
    count = 0
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith("."):
            continue

        meta = extract_skill_meta(skill_dir)
        index_path = skill_dir / "INDEX.md"

        # 估算 tokens（粗略：中文 ~2 chars/token，英文 ~4 chars/token）
        desc = meta.get("description", "")
        desc_tokens = len(desc) // 2

        content = f"# {meta.get('name', skill_dir.name)} — 技能索引\n\n"
        content += f"> {meta.get('description', '无描述')}\n"
        content += f"\n**目录**: `{meta.get('dir', skill_dir.name)}`\n"
        content += f"\n*自动生成 · {desc_tokens} tokens*\n"

        index_path.write_text(content, encoding="utf-8")
        count += 1

    return count


def main():
    skills_dir = Path(__file__).parent.parent / "skills"
    if len(sys.argv) > 1:
        skills_dir = Path(sys.argv[1])

    if not skills_dir.exists():
        print(f"错误: 目录不存在 {skills_dir}")
        sys.exit(1)

    count = generate_skill_index(skills_dir)
    print(f"✅ 已生成 {count} 个 Skill INDEX.md")


if __name__ == "__main__":
    main()