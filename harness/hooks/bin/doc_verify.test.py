#!/usr/bin/env python3
"""
doc_verify.py 测试
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_doc_verify_import():
    """测试 doc_verify.py 可以正常导入"""
    try:
        import doc_verify  # noqa: F401
        print("✓ doc_verify 模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ doc_verify 模块导入失败: {e}")
        return False


def test_doc_verify_function():
    """测试 verify_documents 函数"""
    try:
        import doc_verify  # noqa: F401
        result = doc_verify.verify_documents()
        assert isinstance(result, dict), "应返回 dict"
        assert "status" in result, "应包含 status 字段"
        print("✓ verify_documents 函数正常")
        return True
    except Exception as e:
        print(f"✗ verify_documents 函数失败: {e}")
        return False


if __name__ == "__main__":
    tests = [test_doc_verify_import, test_doc_verify_function]
    passed = sum(1 for t in tests if t())
    print(f"\n结果: {passed}/{len(tests)} 通过")
    sys.exit(0 if passed == len(tests) else 1)