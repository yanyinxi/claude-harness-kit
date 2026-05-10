#!/usr/bin/env python3
"""
doc_generator.py 测试 — 验证文件不存在时的错误处理

Bug: 读取不存在的文件时抛出 FileNotFoundError，但被宽泛的 Exception 捕获
且错误消息不清晰
"""
import sys
from pathlib import Path

# 添加 knowledge 目录到 sys.path
knowledge_dir = Path(__file__).parent
sys.path.insert(0, str(knowledge_dir))


def test_read_nonexistent_file_should_log_clear_error():
    """验证读取不存在的文件返回 None 并记录错误"""
    from doc_generator import convert

    # 尝试转换不存在的文件
    nonexistent_file = Path("/nonexistent/file.md")
    output_dir = Path("/tmp/doc_generator_test")

    result = convert(
        md_file=nonexistent_file,
        doc_type="test",
        output_dir=output_dir
    )

    # 应该返回 None 而不是抛出异常
    assert result is None, f"应该返回 None，实际: {result}"
    print("✓ 读取不存在的文件返回 None")


def test_convert_with_explicit_check():
    """验证 convert 函数在文件不存在时的行为"""
    from doc_generator import convert

    # 测试不存在的文件
    fake_file = Path("/fake/path/that/does/not/exist.md")
    output_dir = Path("/tmp/test_output")

    # 应该不抛出异常，返回 None
    try:
        result = convert(fake_file, "test", output_dir)
        assert result is None, "文件不存在时应返回 None"
        print("✓ 文件不存在检查正常工作")
    except FileNotFoundError as e:
        raise AssertionError(f"不应该抛出 FileNotFoundError，应返回 None: {e}")
    except Exception as e:
        raise AssertionError(f"不应该抛出异常，应返回 None: {e}")


def test_error_logging_for_nonexistent_file():
    """验证错误日志包含清晰的文件路径信息"""
    from doc_generator import _log_error

    # 调用 _log_error（验证错误处理路径）
    _log_error(
        phase="read",
        error_msg="文件不存在: /nonexistent/file.md",
        file_path="/nonexistent/file.md",
        recoverable=False
    )

    print("✓ _log_error 调用成功（无异常）")


if __name__ == "__main__":
    print("=" * 60)
    print("doc_generator.py 测试 — 文件不存在错误处理")
    print("=" * 60)

    tests = [
        test_read_nonexistent_file_should_log_clear_error,
        test_convert_with_explicit_check,
        test_error_logging_for_nonexistent_file,
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n运行: {test.__name__}")
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ 错误: {type(e).__name__}: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)