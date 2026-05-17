---
name: feedback_e2e_test_required
description: 新功能/模块必须包含 E2E 测试，包含完整的端到端工作流验证
metadata:
  type: feedback
  created: 2026-05-17
  confidence: 0.8
  source: 项目实践总结
---

# E2E 测试强制要求

## 为什么必须做 E2E 测试

1. **单元测试不等于正确**：模块独立测试通过不代表整体可用
2. **真实用户场景**：E2E 模拟用户完整操作流程
3. **接口集成验证**：确保模块之间正确协作

## 测试金字塔（必须遵守）

```
┌─────────────────────────────────────────────────┐
│         端到端测试 (E2E) — 50%                   │
│   完整工作流，模拟真实用户操作                    │
├─────────────────────────────────────────────────┤
│         集成测试 (Integration) — 30%            │
│   多模块协作验证                                │
├─────────────────────────────────────────────────┤
│         单元测试 (Unit) — 10%                   │
│   单模块独立正确性                              │
└─────────────────────────────────────────────────┘
```

## E2E 测试检查项

| 检查项 | 要求 |
|--------|------|
| 测试文件位置 | `harness/tests/e2e/test_*.py` |
| 覆盖完整工作流 | 用户输入 → 系统处理 → 预期输出 |
| 会话隔离 | 使用唯一 session_id，避免状态污染 |
| 测试轮数 | ≥3 轮验证结果一致 |
| 失败信息 | 明确指出哪个检查失败 |

## 记忆系统 E2E 测试示例

```python
# harness/tests/e2e/test_memory_e2e.py
class TestMemoryE2E(unittest.TestCase):
    def test_l0_first_injection(self):
        """L0 层首次注入"""
        session_id = f"e2e-{uuid.uuid4()}"
        result = run_memory_inject(session_id)

        # 验证输出包含 L0 内容
        self.assertIn("【项目记忆】", result.stdout)

        # 验证状态文件创建
        state_file = data_dir / f".memory_session_{session_id}.json"
        self.assertTrue(state_file.exists())
```

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 输出为空 | session 状态残留，L0 不注入 | 使用唯一 session_id |
| 测试不稳定 | 共享状态污染 | 每个测试清理环境 |
| 遗漏 E2E | 只做单元测试 | 强制检查 `harness/tests/e2e/` |

## 验证命令

```bash
# 运行所有测试
python3 -m pytest harness/tests/ -v

# 仅运行 E2E
python3 -m pytest harness/tests/e2e/ -v

# 记忆系统 E2E
python3 -m pytest harness/tests/e2e/test_memory_e2e.py -v
```

## 触发时机

- 新功能开发完成后
- 模块集成前
- 发布前回归测试

## 相关文件

- `harness/tests/e2e/test_memory_e2e.py` — 记忆系统 E2E 测试
- `harness/tests/test_full_memory_loop.py` — 记忆闭环测试
- `skills/continuous-learning-v2/SKILL.md` — 测试要求说明