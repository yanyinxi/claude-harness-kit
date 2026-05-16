#!/bin/bash
# coverage-check.sh — 测试覆盖率门禁
# 当测试覆盖率低于阈值时阻断提交

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
MIN_COVERAGE="${COVERAGE_THRESHOLD:-80}"

# 支持多种覆盖率报告格式
find_coverage_report() {
    local dir="$1"
    # pytest-cov XML
    if [[ -f "$dir/coverage.xml" ]]; then
        echo "xml:$dir/coverage.xml"
        return 0
    fi
    # Jest/JSON
    if [[ -f "$dir/coverage/coverage-summary.json" ]]; then
        echo "json:$dir/coverage/coverage-summary.json"
        return 0
    fi
    # Go coverage
    if [[ -f "$dir/cover.out" ]]; then
        echo "go:$dir/cover.out"
        return 0
    fi
    return 1
}

check_coverage() {
    local report
    report=$(find_coverage_report "$PROJECT_DIR")
    [[ -z "$report" ]] && exit 0  # 无覆盖率报告，跳过

    local type="${report%%:*}"
    local path="${report#*:}"

    case "$type" in
        xml)
            COVERAGE=$(grep -oP 'line coverage="\K[0-9.]+' "$path" 2>/dev/null | head -1)
            ;;
        json)
            COVERAGE=$(python3 -c "import json; d=json.load(open('$path')); print(d.get('total',{}).get('pct',0))" 2>/dev/null)
            ;;
        go)
            COVERAGE=$(go tool cover -func="$path" 2>/dev/null | grep total | awk '{print $3}' | tr -d '%')
            ;;
    esac

    if [[ -n "$COVERAGE" ]]; then
        if (( $(echo "$COVERAGE < $MIN_COVERAGE" | bc -l 2>/dev/null || echo "0") )); then
            echo "❌ 测试覆盖率 ${COVERAGE}% 低于阈值 ${MIN_COVERAGE}%"
            echo "   请添加或完善测试用例"
            exit 1
        else
            echo "✓ 测试覆盖率 ${COVERAGE}% (阈值: ${MIN_COVERAGE}%)"
        fi
    fi
}

# 仅在提交时检查（git commit 触发）
if [[ -n "${GIT_COMMIT:-}" ]] || git rev-parse --verify HEAD >/dev/null 2>&1; then
    check_coverage
fi

exit 0