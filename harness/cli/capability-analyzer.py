#!/usr/bin/env python3
"""
Capability Registry 分析器 v2 — 语义化输出

功能：
  - 扫描 harness/ 下所有 Python/JS 文件
  - 提取 class/function 定义
  - 分析 import/require 依赖
  - 识别通用方法（被 >= 2 处引用）
  - 生成语义化注册表（AI 易懂，按需加载友好）

设计原则：
  - 一句话描述：让 AI 快速理解模块是做什么的
  - 核心能力：功能清单，不是函数列表
  - 使用场景：解决"什么时候用"的问题
  - 典型用法：代码示例，直接可用
  - 方法速查：快速检索

按需加载：
  - 每个模块都有锚点 (### module-name)
  - L0 概览只显示模块名和一句话
  - 按需加载时只注入相关章节
"""
import ast
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class SemanticAnalyzer:
    """语义化分析器"""

    # 场景关键词映射：帮助 AI 理解"什么时候用"
    SCENARIO_PATTERNS = {
        "config": ["配置", "settings", "config", "加载配置"],
        "memory": ["记忆", "memory", "本能", "instinct"],
        "hook": ["hook", "钩子", "触发", "拦截"],
        "evolution": ["进化", "evolve", "优化", "改进"],
        "cli": ["命令行", "cli", "命令", "脚本"],
        "agent": ["agent", "代理", "执行"],
        "skill": ["skill", "技能", "能力"],
        "path": ["路径", "path", "目录"],
        "version": ["版本", "version", "升级"],
        "error": ["错误", "error", "异常", "验证"],
    }

    def __init__(self, root: Path):
        self.root = root
        self.modules = {}
        self.function_calls = defaultdict(list)
        self.module_relationships = defaultdict(set)  # module -> {deps}

    def scan(self):
        """扫描所有文件"""
        for py_file in self.root.glob("harness/**/*.py"):
            if "test" in py_file.name.lower() or py_file.name.startswith("_"):
                continue
            self._analyze_python(py_file)

        for js_file in self.root.glob("**/*.js"):
            if "test" in js_file.name.lower():
                continue
            self._analyze_javascript(js_file)

        for sh_file in self.root.glob("hooks/bin/*.sh"):
            if sh_file.name.startswith("_"):
                continue
            self._analyze_shell(sh_file)

    def _analyze_python(self, file_path: Path):
        """分析 Python 文件"""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
        except Exception:
            return

        module_name = str(file_path.relative_to(self.root))

        # 提取 docstring 作为描述
        docstring = ast.get_docstring(tree) or ""
        one_sentence = self._extract_one_sentence(docstring)

        # 分析类
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        args = [a.arg for a in item.args.args]
                        methods.append({
                            "name": item.name,
                            "args": args,
                            "doc": ast.get_docstring(item) or ""
                        })

                classes.append({
                    "name": node.name,
                    "methods": methods,
                    "doc": ast.get_docstring(node) or ""
                })

        # 分析顶层函数
        functions = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in node.args.args]
                functions.append({
                    "name": node.name,
                    "args": args,
                    "doc": ast.get_docstring(node) or ""
                })

        # 分析 import
        imports = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                imports.extend([n.name for n in node.names])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)

        # 推断场景
        scenarios = self._infer_scenarios(module_name, docstring, classes, functions)

        self.modules[module_name] = {
            "type": "python",
            "path": module_name,
            "one_sentence": one_sentence,
            "docstring": docstring,
            "classes": classes,
            "functions": functions,
            "imports": imports[:10],  # 限制数量
            "scenarios": scenarios,
            "content": content
        }

    def _analyze_javascript(self, file_path: Path):
        """分析 JavaScript 文件"""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return

        module_name = str(file_path.relative_to(self.root))

        # 提取注释作为描述
        lines = content.split("\n")
        doc_lines = []
        for line in lines[:20]:
            if line.strip().startswith("//") or line.strip().startswith("/*"):
                doc_lines.append(line.strip().lstrip("//").lstrip("/*").strip())

        one_sentence = " ".join(doc_lines[:3])[:100] if doc_lines else "JavaScript 模块"

        # 提取函数
        functions = re.findall(r'function\s+(\w+)\s*\([^)]*\)', content)

        # 推断场景
        scenarios = self._infer_scenarios(module_name, " ".join(doc_lines), [], [])

        self.modules[module_name] = {
            "type": "javascript",
            "path": module_name,
            "one_sentence": one_sentence,
            "docstring": " ".join(doc_lines),
            "classes": [],
            "functions": [{"name": f, "args": [], "doc": ""} for f in functions],
            "imports": [],
            "scenarios": scenarios,
            "content": content
        }

    def _analyze_shell(self, file_path: Path):
        """分析 Shell 脚本"""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return

        module_name = str(file_path.relative_to(self.root))

        # 提取描述
        lines = content.split("\n")
        description = ""
        for line in lines[:15]:
            if line.strip().startswith("#"):
                description += line.strip().lstrip("#").strip() + " "

        # 提取函数
        functions = re.findall(r'^function\s+(\w+)|^(\w+)\s*\(\s*\)\s*\{', content, re.MULTILINE)
        functions = [f[0] or f[1] for f in functions]

        # 推断场景
        scenarios = self._infer_scenarios(module_name, description, [], [])

        self.modules[module_name] = {
            "type": "shell",
            "path": module_name,
            "one_sentence": description.strip()[:100],
            "docstring": description,
            "classes": [],
            "functions": [{"name": f, "args": [], "doc": ""} for f in functions],
            "imports": [],
            "scenarios": scenarios,
            "content": content
        }

    def _extract_one_sentence(self, docstring: str) -> str:
        """从 docstring 提取一句话描述"""
        if not docstring:
            return "模块功能未定义"
        # 取第一行或第一句
        first_line = docstring.split("\n")[0].strip()
        if first_line.endswith(("。", ".", "：", ":")):
            return first_line
        # 取到第一个句号
        for sep in ["。", ".", "：", ":"]:
            if sep in first_line:
                return first_line.split(sep)[0] + sep
        return first_line[:80]

    def _infer_scenarios(self, module_name: str, docstring: str, classes: list, functions: list) -> list:
        """推断使用场景"""
        text = f"{module_name} {docstring} " + " ".join([
            c["name"] + " " + c["doc"] for c in classes
        ]) + " " + " ".join([f["name"] for f in functions])

        matched = []
        for scenario, keywords in self.SCENARIO_PATTERNS.items():
            for kw in keywords:
                if kw.lower() in text.lower():
                    matched.append(scenario)
                    break
        return list(set(matched))[:3]

    def analyze_common_methods(self):
        """分析通用方法（被多处调用）"""
        # 构建函数调用图
        call_counts = defaultdict(set)

        for module_name, info in self.modules.items():
            content = info.get("content", "")
            if not content:
                continue

            # 收集所有函数名
            all_funcs = set()
            for cls in info.get("classes", []):
                all_funcs.add(cls["name"])
                for m in cls.get("methods", []):
                    all_funcs.add(m["name"])
            for func in info.get("functions", []):
                all_funcs.add(func["name"])

            # 扫描调用
            for func_name in all_funcs:
                # 简单的字符串匹配（不精确但够用）
                if re.search(rf'\b{func_name}\s*\(', content):
                    call_counts[(module_name, func_name)].add(module_name)

        # 筛选通用方法
        common = []
        for (module, func), callers in call_counts.items():
            if len(callers) >= 2:
                common.append({
                    "module": module,
                    "func": func,
                    "callers": list(callers),
                    "count": len(callers)
                })

        return sorted(common, key=lambda x: x["count"], reverse=True)


def generate_semantic_registry(analyzer: SemanticAnalyzer, output_path: Path):
    """生成语义化注册表"""

    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =====================
    # 头部
    # =====================
    lines.append("# Capability Registry (语义化版)")
    lines.append(f"> 自动生成于 {timestamp}")
    lines.append("> 用途：AI 代码理解、模块调用、场景匹配")
    lines.append("")
    lines.append("---\n")

    # =====================
    # L0: 模块地图
    # =====================
    lines.append("## 模块地图\n")
    lines.append("| 模块 | 类型 | 一句话描述 | 场景 |")
    lines.append("|------|------|-----------|------|")

    # 按场景分组
    by_scenario = defaultdict(list)
    for name, info in analyzer.modules.items():
        for sc in info.get("scenarios", []):
            by_scenario[sc].append((name, info))

    for name, info in sorted(analyzer.modules.items()):
        scenarios = "/".join(info.get("scenarios", [])) or "-"
        lines.append(f"| `{name}` | {info['type']} | {info['one_sentence'][:40]} | {scenarios} |")

    lines.append("")

    # =====================
    # L1: 按场景分组
    # =====================
    lines.append("## 按场景分组\n")

    for scenario, modules in sorted(by_scenario.items()):
        lines.append(f"### 场景: {scenario.upper()}\n")
        for name, info in sorted(modules, key=lambda x: x[0]):
            # 锚点标记（用于按需加载）
            lines.append(f"<!-- CAPABILITY:{name} -->")
            lines.append(f"#### `{name}`")
            lines.append("")
            lines.append(f"**一句话**: {info['one_sentence']}")
            lines.append(f"**类型**: {info['type']}")
            lines.append(f"**路径**: `{info['path']}`")

            # 核心能力
            if info.get("classes") or info.get("functions"):
                lines.append("")
                lines.append("**核心能力**:")
                for cls in info.get("classes", []):
                    if cls["doc"]:
                        lines.append(f"  - `{cls['name']}`: {cls['doc'][:60]}...")
                    else:
                        lines.append(f"  - `{cls['name']}`")

                for func in info.get("functions", [])[:5]:  # 只显示前5个
                    if func["doc"]:
                        lines.append(f"  - `{func['name']}()`: {func['doc'][:50]}...")
                    else:
                        lines.append(f"  - `{func['name']}()`")

            lines.append("")

    # =====================
    # L2: 通用方法
    # =====================
    lines.append("## 通用方法 ⭐\n")
    lines.append("> 被 >= 2 处调用的方法，修改时需谨慎\n")

    common_methods = analyzer.analyze_common_methods()

    if common_methods:
        lines.append("| 方法 | 模块 | 调用次数 | 调用方 |")
        lines.append("|------|------|----------|--------|")
        for item in common_methods[:20]:
            callers = ", ".join([f"`{c}`" for c in item["callers"][:3]])
            if len(item["callers"]) > 3:
                callers += f" (+{len(item['callers']) - 3})"
            lines.append(f"| `{item['func']}` | `{item['module']}` | {item['count']} | {callers} |")
    else:
        lines.append("*暂无通用方法*")

    lines.append("")

    # =====================
    # L3: 模块详情（按需加载）
    # =====================
    lines.append("## 模块详情 (按需加载)\n")
    lines.append("> 以下内容通过 `memory-inject.sh` 按关键词加载\n")

    for name, info in sorted(analyzer.modules.items()):
        lines.append(f"<!-- MODULE:{name} -->")
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"**类型**: {info['type']}")
        lines.append(f"**路径**: `{info['path']}`")
        lines.append(f"**一句话**: {info['one_sentence']}")
        lines.append("")

        # 场景
        if info.get("scenarios"):
            lines.append("**使用场景**: " + ", ".join([f"`{s}`" for s in info["scenarios"]]))
            lines.append("")

        # 依赖
        if info.get("imports"):
            lines.append("**依赖**: " + ", ".join([f"`{i}`" for i in info["imports"][:5]]))
            lines.append("")

        # 类详情
        if info.get("classes"):
            lines.append("**类**:")
            for cls in info["classes"]:
                lines.append(f"  - `{cls['name']}`")
                if cls.get("methods"):
                    methods_str = ", ".join([f"`{m['name']}()`" for m in cls["methods"][:8]])
                    lines.append(f"    方法: {methods_str}")
            lines.append("")

        # 函数详情
        if info.get("functions"):
            lines.append("**函数**:")
            for func in info["functions"]:
                args_str = ", ".join(func["args"][:5]) if func["args"] else ""
                lines.append(f"  - `{func['name']}({args_str})`")
                if func.get("doc"):
                    lines.append(f"    说明: {func['doc'][:80]}")
            lines.append("")

        lines.append("---\n")

    # =====================
    # 搜索索引
    # =====================
    lines.append("## 搜索索引\n")
    lines.append("> 用于按需加载匹配\n")

    for name, info in sorted(analyzer.modules.items()):
        keywords = name.replace("/", " ").replace("_", " ").split()
        keywords.extend(info.get("scenarios", []))
        keywords.extend([c["name"] for c in info.get("classes", [])])
        keywords = " ".join(set(keywords))
        lines.append(f"- **{name}**: {keywords}")

    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ 已生成: {output_path}")
    print(f"  - 模块数: {len(analyzer.modules)}")
    print(f"  - 通用方法: {len(common_methods)} 个")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Capability Registry 分析器 v2")
    parser.add_argument("--root", type=str, default=".", help="项目根目录")
    parser.add_argument("--output", type=str, default=".claude/knowledge/capability-registry.md",
                        help="输出文件路径")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = root / args.output

    print("开始语义化分析...")

    analyzer = SemanticAnalyzer(root)
    analyzer.scan()

    print(f"  发现 {len(analyzer.modules)} 个模块")

    generate_semantic_registry(analyzer, output)

    print("完成!")


if __name__ == "__main__":
    main()