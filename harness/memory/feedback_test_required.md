---
name: feedback_test_required
description: 实现功能后必须编写测试用例，确保回归验证和质量
metadata: 
  node_type: memory
  type: feedback
  priority: high
  tags: 
    - 测试
    - 质量
    - 开发规范
  originSessionId: 29727a4c-0ec2-4084-b7b7-015be249bd6c
---

# 测试用例要求

**规则**：实现功能后必须编写测试用例，确保回归验证和质量

**Why**：上次忘记为更新检测系统写测试用例，没有测试覆盖就无法保证质量，也无法进行回归测试。下次可能重蹈覆辙。

**How to apply**：
1. 实现任何功能（含新文件、新模块）
2. 必须在 `harness/tests/` 目录下创建对应的测试文件
3. 测试覆盖：单元测试（mock 外部依赖）+ 集成测试（真实场景）
4. 测试命令：`python3 -m pytest harness/tests/test_xxx.py -v`
5. 测试文件命名：`test_<module_name>.py`

**测试要求**：
- 每个公共函数必须有测试用例
- 边界情况必须覆盖（如空值、异常、网络失败）
- Shell 脚本必须测试语法、权限、执行结果
- 集成测试模拟真实用户场景