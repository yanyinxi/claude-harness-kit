#!/bin/bash
# notify.sh - 飞书 Webhook 通知脚本
# 用法: ./notify.sh <type> <message> [title]
# 示例: ./notify.sh success "测试通过" "CHK 通知"

set -e

# 配置
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
REPO_NAME="${GITHUB_REPOSITORY:-claude-harness-kit}"
REPO_URL="${GITHUB_SERVER_URL:-https://github.com}/$REPO_NAME"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 发送飞书消息
send_feishu_message() {
    local type="$1"
    local message="$2"
    local title="${3:-CHK 通知}"
    local color="$4"

    if [ -z "$FEISHU_WEBHOOK_URL" ]; then
        log_warn "FEISHU_WEBHOOK_URL 未设置，跳过飞书通知"
        log_info "消息内容: $message"
        return 0
    fi

    # 根据类型设置颜色和表情
    case "$type" in
        success)
            local emoji="✅"
            local color_code="green"
            ;;
        failure)
            local emoji="❌"
            local color_code="red"
            ;;
        warning)
            local emoji="⚠️"
            local color_code="yellow"
            ;;
        info)
            local emoji="ℹ️"
            local color_code="blue"
            ;;
        *)
            local emoji="📢"
            local color_code="blue"
            ;;
    esac

    # 构建消息内容
    local content='{"msg_type":"post","content":{"post":{"zh_cn":{"title":"'"$emoji $title"'","content":[[{"tag":"text","text":"'"$message"'"}]]}}}}'

    # 发送请求
    local response
    response=$(curl -s -X POST "$FEISHU_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$content" 2>&1) || true

    if echo "$response" | grep -q '"code":0'; then
        log_info "飞书通知发送成功"
    else
        log_warn "飞书通知发送失败: $response"
    fi
}

# 主函数
main() {
    local type="${1:-info}"
    local message="${2:-}"
    local title="${3:-CHK 通知}"

    if [ -z "$message" ]; then
        log_error "消息内容不能为空"
        echo "用法: $0 <type> <message> [title]"
        echo "type: success|failure|warning|info"
        exit 1
    fi

    log_info "发送通知: [$type] $message"
    send_feishu_message "$type" "$message" "$title"
}

# 如果被直接调用，执行主函数
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi