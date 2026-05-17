#!/usr/bin/env python3
"""
关键词匹配模块 - 根据用户输入匹配相关记忆

功能：
- 定义关键词映射
- 返回匹配的记忆文件列表
- 支持中英文关键词

使用方式：
  from harness._core.keyword_matcher import match_keywords, get_matching_files
"""
from typing import Optional

# 关键词映射表
KEYWORD_MAP = {
    "testing": [
        "测试", "test", "pytest", "单元测试", "集成测试", "e2e",
        "测试用例", "测试驱动", "test case", "test driven"
    ],
    "refactor": [
        "重构", "refactor", "优化代码", "代码重构", "重写",
        "clean code", "clean up", "代码优化"
    ],
    "security": [
        "安全", "security", "漏洞", "审计", "注入", "xss",
        "sql注入", "csrf", "认证", "授权", "permission"
    ],
    "git": [
        "git", "commit", "branch", "merge", "rebase", "stash",
        "版本控制", "分支", "合并", "提交"
    ],
    "api": [
        "api", "接口", "endpoint", "rest", "graphql", "crud",
        "http", "请求", "响应"
    ],
    "database": [
        "数据库", "database", "sql", "mongodb", "postgres", "mysql",
        "查询", "索引", "migration"
    ],
    "docker": [
        "docker", "container", "镜像", "container", "k8s", "kubernetes",
        "pod", "deployment"
    ],
    "performance": [
        "性能", "performance", "优化", "慢", "bottleneck", "缓存",
        "cache", "async", "并行"
    ],
    "debugging": [
        "debug", "调试", "bug", "错误", "异常", "crash",
        "stack", "trace", "复现"
    ],
    "tdd": [
        "tdd", "测试驱动", "test driven", "red green", "红绿重构",
        "单元测试", "覆盖率"
    ],
    "agent": [
        "agent", "智能体", "多agent", "并行", "协作",
        "orchestrat", "编排"
    ],
}

# 关键词对应的记忆文件
KEYWORD_FILES = {
    "testing": "harness/memory/feedback_test_required.md",
    "refactor": "harness/memory/refactor-guidelines.md",
    "security": "harness/memory/security-rules.md",
    "git": "harness/memory/git-workflow.md",
    "api": "harness/memory/api-design-guidelines.md",
    "database": "harness/memory/database-patterns.md",
    "docker": "harness/memory/docker-best-practices.md",
    "performance": "harness/memory/performance-optimization.md",
    "debugging": "harness/memory/debugging-patterns.md",
    "tdd": "harness/memory/tdd-workflow.md",
    "agent": "harness/memory/agent-collaboration.md",
}


def match_keywords(user_input: str) -> list[str]:
    """
    匹配用户输入中的关键词

    Args:
        user_input: 用户输入文本

    Returns:
        匹配的关键词类别列表
    """
    if not user_input:
        return []
    user_input_lower = user_input.lower()
    matched = []

    for category, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword.lower() in user_input_lower:
                if category not in matched:
                    matched.append(category)
                break

    return matched


def get_matching_files(categories: list[str]) -> list[str]:
    """
    获取匹配的记忆文件列表

    Args:
        categories: 匹配的类别列表

    Returns:
        记忆文件路径列表
    """
    files = []
    for category in categories:
        if category in KEYWORD_FILES:
            files.append(KEYWORD_FILES[category])
    return files


def format_matched_keywords(categories: list[str]) -> str:
    """
    格式化匹配结果为可读文本

    Args:
        categories: 匹配的类别列表

    Returns:
        格式化文本
    """
    if not categories:
        return ""

    lines = [
        "",
        "──────────────────────────────────────────────────────────────",
        f"【关键词匹配】检测到 {len(categories)} 个相关领域",
        "",
    ]

    for cat in categories:
        # 获取关键词描述
        keywords = KEYWORD_MAP.get(cat, [])
        keywords_text = ", ".join(keywords[:3])

        lines.append(f"  📌 {cat.upper()}")
        lines.append(f"     关键词: {keywords_text}")
        lines.append("")

    lines.append("──────────────────────────────────────────────────────────────")

    return "\n".join(lines)


def check_and_match(user_input: str) -> tuple[list[str], list[str]]:
    """
    检查并匹配关键词，返回类别和文件

    Args:
        user_input: 用户输入文本

    Returns:
        (匹配的类别列表, 匹配的文件列表)
    """
    categories = match_keywords(user_input)
    files = get_matching_files(categories)
    return categories, files


def main():
    """测试"""
    print("=== 关键词匹配测试 ===\n")

    test_inputs = [
        "帮我写个单元测试",
        "这个代码需要重构一下",
        "发现了一个安全漏洞",
        "帮我提交代码",
        "今天天气怎么样",
    ]

    for inp in test_inputs:
        categories, files = check_and_match(inp)
        print(f"输入: {inp}")
        print(f"  匹配: {categories if categories else '无'}")
        print(f"  文件: {files}")
        print()


if __name__ == "__main__":
    main()