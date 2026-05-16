#!/bin/bash
# quality-gate.sh — PostToolUse Hook: 验证代码和配置文件格式
# 设计：永远 exit 0，格式错误警告但不阻断
set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

INPUT=$(cat 2>/dev/null) || INPUT=""
[[ -z "$INPUT" ]] && exit 0

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null) || { exit 0; }

[[ -z "$FILE_PATH" ]] && exit 0

block_post() {
    local reason="$1"
    echo -e "$reason" >&2
    exit 2
}

# bash 3.2 (macOS) uses first char of RHS as regex delimiter.
# [[ $f =~ /test/ ]] → delimiter "/", regex "test/" (not "/test/")
# [[ $f =~ /\. ]]   → delimiter "/", regex "\." (ok, matches literal dot)
# But [[ $f =~ \. ]] → delimiter ".", regex "" (empty) → matches EVERYTHING!
# Fix: use glob patterns for simple prefix/suffix matching, regex only for =~.
_is_impl_file() {
    local f="$1"
    # Use glob matching (no regex, no delimiter issue)
    case "$f" in
        */test/*|*/test|test/*|*/tests/*|*/tests|tests/*) return 1 ;;
        */__tests__/*|*/__tests__) return 1 ;;
        */spec/*|*/spec|spec/*|*/specs/*|*/specs|specs/*) return 1 ;;
        */docs/*|*/docs|docs/*|*/doc/*|*/doc|doc/*) return 1 ;;
        *.json|*.yaml|*.yml|*.md|*.txt|*.csv) return 1 ;;
        *.test.*|*.spec.*|*.config.*) return 1 ;;
        *_test.py|test_*.py|*_spec.py|*_spec.rb) return 1 ;;
    esac
    # Hidden files/dirs (use regex with "/" as delimiter to safely match "/.")
    [[ "$f" =~ /\. ]] && return 1
    [[ "$f" =~ ^\. ]] && return 1
    # Impl file → trigger test suggestion
    return 0
}

# ── Secret 扫描 (阿里 Harness 核心规则) ──
_scan_secrets() {
    # 扫描常见 secret 模式
    local patterns=(
        "api[_-]?key"
        "secret[_-]?key"
        "password\s*="
        "token\s*="
        "bearer\s+[A-Za-z0-9]{20,}"
        "sk-[A-Za-z0-9]{20,}"
        "ghp_[A-Za-z0-9]{20,}"
    )

    for pattern in "${patterns[@]}"; do
        if grep -Ei "$pattern" "$FILE_PATH" 2>/dev/null | grep -v "^#" | grep -v "//" | grep -v "^\s*#" | grep -v "example" | grep -v "test" | grep -v "mock" | grep -v "placeholder" >/dev/null; then
            echo "⚠️ 检测到疑似 Secret 模式 ($pattern) 在: $FILE_PATH"
            echo "   请使用环境变量或 .env 文件管理敏感信息"
        fi
    done
}

# ── 测试先行检测（建议，不阻断）──
_check_test_missing() {
    local staged_files
    staged_files=$(git -C "$PROJECT_DIR" diff --cached --name-only 2>/dev/null) || staged_files=""
    local test_in_staged=0
    for f in $staged_files; do
        # Use glob patterns for test file detection (avoid bash 3.2 delimiter bugs)
        case "$f" in
            *.test.*|*.spec.*|*/test/*|*/__tests__/*) test_in_staged=1; break ;;
        esac
    done
    [[ "$test_in_staged" -eq 0 ]] && echo "💡 建议: 实现文件 $FILE_PATH 已变更，但未检测到对应测试文件变更。请确认是否需要添加测试。"
}

# ── JSON 文件格式验证 ──
if [[ "$FILE_PATH" =~ \.json$ ]]; then
    if ! python3 -m json.tool "$FILE_PATH" > /dev/null 2>&1; then
        block_post "❌ JSON 格式错误：$FILE_PATH\n请检查是否有语法错误（多余逗号、非法注释等）"
    fi
fi

# ── project_standards.md 验证 ──
if [[ "$FILE_PATH" == *"project_standards.md"* ]]; then
    VERIFY_SCRIPT="$PROJECT_DIR/.claude/tests/test_parallelism_protocol.py"
    [[ -f "$VERIFY_SCRIPT" ]] && echo "ℹ️ project_standards.md 已变更，建议运行验证测试"
fi

# ── Agent 文件格式验证（警告不阻断）──
if [[ "$FILE_PATH" == *"agents/"* ]] && [[ "$FILE_PATH" =~ \.md$ ]]; then
    grep -q "^description:" "$FILE_PATH" 2>/dev/null || echo "⚠️ Agent 文件缺少 description 字段：$FILE_PATH"
    grep -q "^tools:" "$FILE_PATH" 2>/dev/null || echo "⚠️ Agent 文件缺少 tools 字段：$FILE_PATH"
fi

# ── Skill 文件格式验证（警告不阻断）──
if [[ "$FILE_PATH" == *"skills/"* ]] && [[ "$FILE_PATH" =~ \.md$ ]]; then
    grep -q "^---" "$FILE_PATH" 2>/dev/null || echo "⚠️ Skill 文件缺少 frontmatter：$FILE_PATH"
fi

# ── Secret 扫描 ──
if _is_impl_file "$FILE_PATH"; then
    _scan_secrets
fi

# ── Python 语法检查 ──
if [[ "$FILE_PATH" =~ \.py$ ]] && [[ -f "$FILE_PATH" ]]; then
    if ! python3 -m py_compile "$FILE_PATH" 2>/dev/null; then
        block_post "❌ Python 语法错误：$FILE_PATH"
    fi
fi

# ── 测试先行检测 ──
if _is_impl_file "$FILE_PATH" && git -C "$PROJECT_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    _check_test_missing
fi

exit 0