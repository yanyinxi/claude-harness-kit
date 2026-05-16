#!/usr/bin/env python3
"""
kb_shared.py 测试 — 验证 INSTINCT_PATH 路径正确性

正确路径: harness/memory/instinct-record.json
错误路径: memory/instinct-record.json (项目根目录)
"""
import sys
from pathlib import Path

# 添加 parent 到 sys.path 以便导入 kb_shared
sys.path.insert(0, str(Path(__file__).parent))


def test_instinct_path_in_harness_memory():
    """验证 INSTINCT_PATH 在 harness/memory/ 下，而不是项目根 memory/"""
    from kb_shared import INSTINCT_PATH

    actual = Path(str(INSTINCT_PATH))

    # 检查路径必须包含 harness/memory/
    assert "harness" in str(actual) and "memory" in str(actual), \
        f"INSTINCT_PATH 应该在 harness/memory/ 下，实际: {actual}"
    assert actual.name == "instinct-record.json", f"文件名应为 instinct-record.json，实际: {actual.name}"

    print(f"✓ INSTINCT_PATH 正确: {actual}")
    return True


def test_instinct_path_not_in_root():
    """验证 INSTINCT_PATH 不在项目根目录"""
    from kb_shared import INSTINCT_PATH

    actual = Path(str(INSTINCT_PATH))

    # 验证路径包含 harness/memory/
    parts = actual.parts
    assert "harness" in parts, f"INSTINCT_PATH 应在 harness/ 下，实际: {actual}"
    assert "memory" in parts, f"INSTINCT_PATH 应在 memory/ 下，实际: {actual}"

    # 验证 harness 在 memory 之前
    harness_idx = parts.index("harness")
    memory_idx = parts.index("memory")
    assert harness_idx < memory_idx, "harness 应该在 memory 之前"

    print(f"✓ INSTINCT_PATH 结构正确: {'/'.join(parts)}")
    return True


def test_find_root_harness_structure():
    """验证 find_root 返回的项目结构"""
    from kb_shared import _find_root

    root = _find_root()

    # 项目根应该存在 harness/ 目录
    harness_dir = root / "harness"
    assert harness_dir.exists(), f"项目根 {root} 应有 harness/ 目录"

    # 项目根不应有 memory/ 目录（memory 在 harness/ 下）
    memory_in_root = root / "memory"
    if memory_in_root.exists():
        print(f"警告: 项目根有 memory/ 目录 {memory_in_root}，应迁移到 harness/memory/")

    print(f"✓ 项目根结构正确: {root}")
    print(f"  - harness/: {(root / 'harness').exists()}")
    print(f"  - harness/memory/: {(root / 'harness' / 'memory').exists()}")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("kb_shared.py 测试 — INSTINCT_PATH 路径验证")
    print("=" * 60)

    tests = [
        test_instinct_path_in_harness_memory,
        test_instinct_path_not_in_root,
        test_find_root_harness_structure,
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
            print(f"✗ 错误: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)