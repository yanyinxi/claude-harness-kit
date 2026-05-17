#!/bin/bash
# ============================================================
# 更新 Capability Registry
#
# 用法：
#   ./update-registry.sh           # 增量更新
#   ./update-registry.sh --force   # 强制全量更新
#   ./update-registry.sh --check   # 检查是否有变更
# ============================================================

set -uo pipefail

# 获取项目根目录（从 hooks/bin/ 回退两级）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ANALYZER_SCRIPT="$PROJECT_ROOT/harness/cli/capability-analyzer.py"

case "${1:-}" in
    --force|-f)
        echo "强制全量更新..."
        python3 "$ANALYZER_SCRIPT" --root "$PROJECT_ROOT"
        ;;
    --check|-c)
        echo "检查变更..."
        if git diff --name-only 2>/dev/null | grep -qE "^(harness|hooks|agents|skills)"; then
            echo "有变更，将触发更新"
        else
            echo "无相关变更"
        fi
        ;;
    --help|-h)
        echo "Usage: $0 [--force|--check]"
        ;;
    *)
        echo "增量更新..."
        python3 "$ANALYZER_SCRIPT" --root "$PROJECT_ROOT"
        ;;
esac