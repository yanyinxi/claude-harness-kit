#!/bin/bash
set -euo pipefail
# TDD 阻断检查 — 实现文件写入前必须存在对应测试文件
# Claude Code PreToolUse Hook (仅 ralph/pipeline 模式启用)

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# 只处理 Write/Edit
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
    exit 0
fi
[[ -z "$FILE_PATH" ]] && exit 0

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# 判断是否为实现代码
_is_impl() {
    local f="$1"
    # 排除非代码路径
    [[ "$f" =~ /\. ]] && return 1
    # 排除常见非实现文件
    [[ "$f" =~ \.json$ ]] && return 1
    [[ "$f" =~ \.ya?ml$ ]] && return 1
    [[ "$f" =~ \.md$ ]] && return 1
    [[ "$f" =~ \.txt$ ]] && return 1
    [[ "$f" =~ \.csv$ ]] && return 1
    [[ "$f" =~ \.css$ ]] && return 1
    [[ "$f" =~ \.html$ ]] && return 1
    [[ "$f" =~ \.svg$ ]] && return 1
    [[ "$f" =~ /docs/ ]] && return 1
    [[ "$f" =~ /README ]] && return 1
    # 排除已是测试文件
    [[ "$f" =~ \.test\. ]] && return 1
    [[ "$f" =~ \.spec\. ]] && return 1
    [[ "$f" =~ /test/ ]] && return 1
    [[ "$f" =~ /__tests__/ ]] && return 1
    [[ "$f" =~ /spec/ ]] && return 1
    # 实现代码路径
    [[ "$f" =~ \.(java|ts|tsx|js|jsx|py|go|rs|rb|php|swift|kt|scala|cs|c|cpp|h)$ ]] && return 0
    return 1
}

_is_impl "$FILE_PATH" || exit 0

# 白名单：配置/生成文件
WHITELIST_DIRS=("migrations/" "db/migrate/" "generated/" "proto/" "vendor/" "third_party/")
for d in "${WHITELIST_DIRS[@]}"; do
    [[ "$FILE_PATH" == *"$d"* ]] && exit 0
done

block() {
    local reason="$1"
    python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': sys.argv[1]
    }
}, ensure_ascii=False))
" "$reason"
    exit 2
}

# 查找对应测试文件
IMP_FILE="$FILE_PATH"
BASENAME=$(basename "$IMP_FILE")
NAME="${BASENAME%.*}"
DIR=$(dirname "$IMP_FILE")

# 候选测试路径
CANDIDATES=()

# 同目录下的 .test.* / .spec.*
CANDIDATES+=("$DIR/$NAME.test.${BASENAME##*.}")
CANDIDATES+=("$DIR/$NAME.spec.${BASENAME##*.}")

# src/main → src/test (Java)
if [[ "$DIR" == *"/main/"* ]]; then
    TEST_DIR="${DIR/main/test}"
    CANDIDATES+=("$TEST_DIR/${NAME}Test.${BASENAME##*.}")
fi

# src/ → __tests__/ (JS/TS)
PROJECT_REL="${IMP_FILE#./}"
CANDIDATES+=("__tests__/${NAME}.test.${BASENAME##*.}")
CANDIDATES+=("tests/${NAME}_test.${BASENAME##*.}")

# 检查任一候选存在
for candidate in "${CANDIDATES[@]}"; do
    if [[ -f "$candidate" ]]; then
        exit 0  # 测试文件存在 → 放行
    fi
done

# 检查 git staged 中是否有测试文件
if git -C "$PROJECT_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    STAGED=$(git -C "$PROJECT_DIR" diff --cached --name-only 2>/dev/null || echo "")
    for f in $STAGED; do
        if [[ "$f" =~ \.test\. ]] || [[ "$f" =~ \.spec\. ]] || [[ "$f" =~ /test/ ]]; then
            exit 0  # 有测试文件变更 → 放行
        fi
    done
fi

block "测试先行: 实现文件 \"${FILE_PATH}\" 没有对应的测试文件。\n请先创建测试文件（如 ${CANDIDATES[0]} 或 ${CANDIDATES[1]}），确保测试失败后，再编写实现代码。\n\nTDD 流程: RED（写失败测试）→ GREEN（让测试通过）→ REFACTOR（优化结构）"
