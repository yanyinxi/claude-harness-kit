#!/usr/bin/env python3
"""
test_chk_commands.py — CHK CLI 命令全面测试

测试所有 /chk-* 命令至少 3 遍，发现并修复 bug。
"""
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
os.chdir(PROJECT_ROOT)


def run_cmd(cmd: list[str], times: int = 3) -> list[tuple[int, str, str]]:
    """运行命令多次，返回每次的结果"""
    results = []
    for i in range(times):
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        results.append((result.returncode, result.stdout, result.stderr))
    return results


def test_kit_help():
    """测试 kit help 命令"""
    results = run_cmd(["bash", "harness/cli/kit.sh", "help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] kit help 返回非零: {err}"
        assert "kit" in out, f"[{i+1}] help 输出缺少 'kit'"
    print("✅ kit help 通过")


def test_chk_help():
    """测试 chk help 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk help 返回非零: {err}"
        assert "chk" in out, f"[{i+1}] help 输出缺少 'chk'"
    print("✅ chk help 通过")


def test_kit_gc():
    """测试 kit gc 命令（知识垃圾回收）"""
    results = run_cmd(["bash", "harness/cli/kit.sh", "gc"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] kit gc 返回非零: {err}"
        # gc.py 已修复，现在应该正常输出
    print("✅ kit gc 通过")


def test_chk_gc():
    """测试 chk gc 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "gc"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk gc 返回非零: {err}"
    print("✅ chk gc 通过")


def test_kit_status():
    """测试 kit status 命令"""
    results = run_cmd(["python3", "harness/cli/status.py"])
    for i, (code, out, err) in enumerate(results):
        # status.py 可能因为缺少某些文件而返回非零，但不应该崩溃
        assert "Traceback" not in err, f"[{i+1}] status.py 崩溃: {err}"
    print("✅ kit status 通过（无崩溃）")


def test_chk_status():
    """测试 chk status 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "status"])
    for i, (code, out, err) in enumerate(results):
        assert "Traceback" not in err, f"[{i+1}] chk status 崩溃: {err}"
    print("✅ chk status 通过（无崩溃）")


def test_kit_mode():
    """测试 kit mode 命令"""
    results = run_cmd(["bash", "harness/cli/kit.sh", "mode"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] kit mode 返回非零: {err}"
    print("✅ kit mode 通过")


def test_chk_mode():
    """测试 chk mode 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "mode"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk mode 返回非零: {err}"
    print("✅ chk mode 通过")


def test_chk_solo():
    """测试 chk solo 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "solo", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk solo 返回非零: {err}"
    print("✅ chk solo 通过")


def test_chk_team():
    """测试 chk team 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "team", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk team 返回非零: {err}"
    print("✅ chk team 通过")


def test_chk_auto():
    """测试 chk auto 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "auto", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk auto 返回非零: {err}"
    print("✅ chk auto 通过")


def test_chk_ultra():
    """测试 chk ultra 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "ultra", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk ultra 返回非零: {err}"
    print("✅ chk ultra 通过")


def test_chk_pipeline():
    """测试 chk pipeline 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "pipeline", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk pipeline 返回非零: {err}"
    print("✅ chk pipeline 通过")


def test_chk_ralph():
    """测试 chk ralph 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "ralph", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk ralph 返回非零: {err}"
    print("✅ chk ralph 通过")


def test_chk_ccg():
    """测试 chk ccg 命令"""
    results = run_cmd(["bash", "harness/cli/chk.sh", "ccg", "--help"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] chk ccg 返回非零: {err}"
    print("✅ chk ccg 通过")


def test_python_gc():
    """直接测试 gc.py"""
    results = run_cmd(["python3", "harness/cli/gc.py"])
    for i, (code, out, err) in enumerate(results):
        assert code == 0, f"[{i+1}] gc.py 返回非零: {err}"
        assert "Traceback" not in err, f"[{i+1}] gc.py 崩溃: {err}"
        assert "✅ 漂移报告已生成" in out, f"[{i+1}] gc.py 输出异常: {out}"
    print("✅ python gc.py 直接执行通过")


def test_instinct_cli():
    """测试 instinct_cli.py"""
    results = run_cmd(["python3", "harness/cli/instinct_cli.py", "list"])
    for i, (code, out, err) in enumerate(results):
        assert "Traceback" not in err, f"[{i+1}] instinct_cli.py 崩溃: {err}"
    print("✅ instinct_cli 通过（无崩溃）")


if __name__ == "__main__":
    tests = [
        test_kit_help,
        test_chk_help,
        test_kit_gc,
        test_chk_gc,
        test_kit_status,
        test_chk_status,
        test_kit_mode,
        test_chk_mode,
        test_chk_solo,
        test_chk_team,
        test_chk_auto,
        test_chk_ultra,
        test_chk_pipeline,
        test_chk_ralph,
        test_chk_ccg,
        test_python_gc,
        test_instinct_cli,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            print(f"运行 {test.__name__}...")
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"测试结果: {passed} 通过, {failed} 失败")
    sys.exit(0 if failed == 0 else 1)