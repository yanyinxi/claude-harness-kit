#!/usr/bin/env python3
"""
instinct_engine.py — CHK 本能推理引擎

从本能记录推断当前场景，动态调整 Agent/Skill 推荐。

功能:
- 本能推理：从历史本能记录推断当前场景
- 动态推荐：根据上下文推荐 Agent/Skill
- 置信度更新：实时更新本能置信度
- 场景匹配：识别任务类型匹配本能

使用方式:
    from instinct_engine import get_recommendations, update_confidence
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# 路径配置
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import INSTINCT_FILE, MEMORY_DIR


class InstinctEngine:
    """本能推理引擎"""

    # 场景关键词映射
    SCENE_KEYWORDS = {
        "backend": ["api", "service", "controller", "endpoint", "rest", "backend"],
        "frontend": ["ui", "component", "react", "vue", "angular", "css", "html"],
        "database": ["sql", "migration", "table", "index", "query", "database"],
        "devops": ["docker", "kubernetes", "ci", "cd", "deploy", "pipeline"],
        "security": ["auth", "authenticate", "permission", "security", "jwt", "token"],
        "testing": ["test", "unit", "integration", "mock", "assert"],
        "performance": ["performance", "optimize", "cache", "memory", "speed"],
        "refactor": ["refactor", "cleanup", "improve", "restructure"],
    }

    # Agent 场景映射
    AGENT_SCENE_MAP = {
        "backend": "backend-dev",
        "frontend": "frontend-dev",
        "database": "database-dev",
        "devops": "devops",
        "security": "security-auditor",
        "testing": "qa-tester",
        "performance": "architect",
        "refactor": "code-reviewer",
    }

    # Skill 场景映射
    SKILL_SCENE_MAP = {
        "backend": "api-designer",
        "frontend": "karpathy-guidelines",
        "database": "database-designer",
        "devops": "docker-essentials",
        "security": "security-audit",
        "testing": "tdd",
        "performance": "performance",
        "refactor": "code-quality",
    }

    def __init__(self):
        self._instincts: list[dict] = []
        self._load()

    def _load(self):
        """加载本能记录"""
        if INSTINCT_FILE.exists():
            try:
                data = json.loads(INSTINCT_FILE.read_text())
                self._instincts = data.get("records", []) if isinstance(data, dict) else data
            except (json.JSONDecodeError, OSError):
                self._instincts = []

    def _save(self):
        """保存本能记录"""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "evolution": {
                "version": "3.0",
                "last_updated": datetime.now().isoformat(),
                "confidence_threshold": 0.7,
            },
            "records": self._instincts,
        }
        INSTINCT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def detect_scene(self, task: str) -> str:
        """
        从任务描述检测场景

        Args:
            task: 任务描述

        Returns:
            场景类型 (backend/frontend/database/...)
        """
        task_lower = task.lower()
        scores: dict[str, int] = {}

        for scene, keywords in self.SCENE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in task_lower)
            if score > 0:
                scores[scene] = score

        if scores:
            return max(scores, key=scores.get)
        return "backend"  # 默认

    def get_recommendations(self, task: str) -> dict:
        """
        获取基于本能的推荐

        Args:
            task: 任务描述

        Returns:
            推荐结果 {agents: [], skills: [], instincts: []}
        """
        scene = self.detect_scene(task)

        # 1. 基于场景推荐 Agent/Skill
        agents = [self.AGENT_SCENE_MAP.get(scene, "executor")]
        skills = [self.SKILL_SCENE_MAP.get(scene, "karpathy-guidelines")]

        # 2. 查找相关本能记录
        relevant_instincts = []
        for instinct in self._instincts:
            if isinstance(instinct, dict):
                context = instinct.get("context", {})
                domain = context.get("domain", "") if isinstance(context, dict) else ""
                if domain == scene or domain in task.lower():
                    relevant_instincts.append({
                        "correction": instinct.get("correction", ""),
                        "confidence": instinct.get("confidence", 0),
                        "domain": domain,
                    })

        return {
            "scene": scene,
            "agents": agents,
            "skills": skills,
            "instincts": relevant_instincts[:5],
        }

    def update_confidence(self, instinct_id: str, delta: float) -> bool:
        """
        更新本能置信度

        Args:
            instinct_id: 本能 ID
            delta: 置信度变化量

        Returns:
            True 如果更新成功
        """
        for instinct in self._instincts:
            if isinstance(instinct, dict) and instinct.get("id") == instinct_id:
                current = instinct.get("confidence", 0.5)
                instinct["confidence"] = min(1.0, max(0.0, current + delta))
                instinct["updated_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False

    def add_instinct(self, domain: str, correction: str, context: str) -> str:
        """
        添加新本能记录

        Args:
            domain: 领域
            correction: 纠正内容
            context: 上下文

        Returns:
            新本能 ID
        """
        instinct_id = f"instinct_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        instinct = {
            "id": instinct_id,
            "type": "pattern_correction",
            "context": {"domain": domain, "trigger": context},
            "correction": correction,
            "confidence": 0.3,  # 新记录从 0.3 开始
            "created_at": datetime.now().isoformat(),
            "times_observed": 1,
        }
        self._instincts.append(instinct)
        self._save()
        return instinct_id

    def format_as_context(self) -> str:
        """
        格式化为上下文注入字符串

        Returns:
            Markdown 格式的本能上下文
        """
        if not self._instincts:
            return ""

        # 获取高置信度记录
        high_conf = [i for i in self._instincts
                     if isinstance(i, dict) and i.get("confidence", 0) >= 0.7]
        high_conf = sorted(high_conf, key=lambda x: x.get("confidence", 0), reverse=True)[:10]

        if not high_conf:
            return ""

        lines = ["\n## Relevant Instincts\n"]
        for instinct in high_conf:
            if isinstance(instinct, dict):
                ctx = instinct.get("context", {})
                domain = ctx.get("domain", "unknown") if isinstance(ctx, dict) else "unknown"
                correction = instinct.get("correction", "")
                confidence = instinct.get("confidence", 0)
                lines.append(f"- [{domain}] {correction[:80]} (conf: {confidence:.2f})")

        return "\n".join(lines)


# 全局引擎实例
_engine: Optional[InstinctEngine] = None


def get_engine() -> InstinctEngine:
    """获取全局本能引擎"""
    global _engine
    if _engine is None:
        _engine = InstinctEngine()
    return _engine


def get_recommendations(task: str) -> dict:
    """获取推荐（顶层函数）"""
    return get_engine().get_recommendations(task)


def update_confidence(instinct_id: str, delta: float) -> bool:
    """更新置信度（顶层函数）"""
    return get_engine().update_confidence(instinct_id, delta)


def main():
    """测试"""
    engine = get_engine()

    # 测试场景检测
    tests = [
        "实现用户登录 API",
        "添加 React 组件",
        "优化数据库查询性能",
        "修复安全漏洞",
        "编写单元测试",
    ]

    print("Instinct Engine Tests:")
    for task in tests:
        recs = engine.get_recommendations(task)
        print(f"  Task: {task}")
        print(f"    Scene: {recs['scene']}")
        print(f"    Agents: {recs['agents']}")
        print(f"    Skills: {recs['skills']}")
        print()


if __name__ == "__main__":
    main()