#!/usr/bin/env bash
#
# install-agent.sh — 单个角色一键安装脚本
#
# 用法：
#   bash <(curl -sL https://raw.githubusercontent.com/USER/REPO/main/install-agent.sh) 角色名称
#
# 示例：
#   bash <(curl -sL https://raw.githubusercontent.com/USER/REPO/main/install-agent.sh) 前端开发者
#
# 支持平台：Windows (Git Bash/WSL), macOS, Linux

set -euo pipefail

# --- 颜色 ---
if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[1;33m'
  RED=$'\033[0;31m'
  CYAN=$'\033[0;36m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  GREEN=''; YELLOW=''; RED=''; CYAN=''; BOLD=''; RESET=''
fi

ok()   { printf "${GREEN}[OK]${RESET} %s\n" "$*"; }
warn() { printf "${YELLOW}[!!]${RESET} %s\n" "$*"; }
err()  { printf "${RED}[ERR]${RESET} %s\n" "$*" >&2; }
info() { printf "${CYAN}[*]${RESET} %s\n" "$*"; }

# --- 配置 ---
REPO_URL="${REPO_URL:-https://raw.githubusercontent.com/你的用户名/你的仓库名/main}"
DEST_DIR="${HOME}/.openclaw/agency-agents"

# --- 帮助 ---
usage() {
  cat <<EOF
OpenClaw Agent 一键安装器

用法：
  $0 <角色名称>

示例：
  $0 前端开发者
  $0 小红书运营专家
  $0 "FPGA/ASIC 数字设计工程师"

支持的命令：
  list    列出所有可用角色
  help    显示此帮助信息

EOF
  exit 0
}

# --- 列出所有角色 ---
list_agents() {
  info "正在获取角色列表..."
  
  local index_url="${REPO_URL}/index.json"
  local index_content
  
  if command -v curl >/dev/null 2>&1; then
    index_content=$(curl -sL "$index_url" 2>/dev/null)
  elif command -v wget >/dev/null 2>&1; then
    index_content=$(wget -qO- "$index_url" 2>/dev/null)
  else
    err "需要 curl 或 wget"
    exit 1
  fi
  
  if [[ -z "$index_content" ]]; then
    err "无法获取角色列表，请检查网络连接"
    exit 1
  fi
  
  echo ""
  printf "${BOLD}可用角色列表：${RESET}\n"
  echo "$index_content" | tr -d '{}' | tr ',' '\n' | while read -r line; do
    local name category
    name=$(echo "$line" | cut -d'"' -f2)
    category=$(echo "$line" | cut -d'"' -f4)
    if [[ -n "$name" && -n "$category" ]]; then
      printf "  ${GREEN}%-25s${RESET} [%s]\n" "$name" "$category"
    fi
  done
  echo ""
  info "使用方法: $0 角色名称"
}

# --- 查找角色分类 ---
find_category() {
  local agent_name="$1"
  local index_url="${REPO_URL}/index.json"
  local index_content
  
  if command -v curl >/dev/null 2>&1; then
    index_content=$(curl -sL "$index_url" 2>/dev/null)
  elif command -v wget >/dev/null 2>&1; then
    index_content=$(wget -qO- "$index_url" 2>/dev/null)
  else
    err "需要 curl 或 wget"
    return 1
  fi
  
  if [[ -z "$index_content" ]]; then
    err "无法获取角色列表，请检查网络连接"
    return 1
  fi
  
  # 解析 JSON 查找分类（兼容无 jq 的环境）
  local category
  category=$(echo "$index_content" | grep -o "\"$agent_name\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | head -1 | sed 's/.*:[[:space:]]*"\([^"]*\)".*/\1/')
  
  if [[ -z "$category" ]]; then
    return 1
  fi
  
  echo "$category"
}

# --- 下载文件 ---
download_file() {
  local url="$1"
  local output="$2"
  
  if command -v curl >/dev/null 2>&1; then
    curl -sL "$url" -o "$output" 2>/dev/null
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$output" "$url" 2>/dev/null
  else
    return 1
  fi
}

# --- 安装角色 ---
install_agent() {
  local agent_name="$1"
  
  echo ""
  printf "${BOLD}========================================${RESET}\n"
  printf "${BOLD}  OpenClaw Agent 安装器${RESET}\n"
  printf "${BOLD}========================================${RESET}\n"
  echo ""
  
  info "角色名称: $agent_name"
  
  # 查找分类
  info "正在查找角色分类..."
  local category
  category=$(find_category "$agent_name")
  
  if [[ -z "$category" ]]; then
    err "未找到角色: $agent_name"
    echo ""
    info "运行 '$0 list' 查看所有可用角色"
    exit 1
  fi
  
  info "所属分类: $category"
  
  # 创建目标目录
  local agent_dir="${DEST_DIR}/${agent_name}"
  mkdir -p "$agent_dir"
  
  # 下载三个文件
  local base_url="${REPO_URL}/${category}/${agent_name}"
  
  info "正在下载配置文件..."
  
  if download_file "${base_url}/SOUL.md" "${agent_dir}/SOUL.md"; then
    ok "SOUL.md ✓"
  else
    err "下载 SOUL.md 失败"
    exit 1
  fi
  
  if download_file "${base_url}/AGENTS.md" "${agent_dir}/AGENTS.md"; then
    ok "AGENTS.md ✓"
  else
    err "下载 AGENTS.md 失败"
    exit 1
  fi
  
  if download_file "${base_url}/IDENTITY.md" "${agent_dir}/IDENTITY.md"; then
    ok "IDENTITY.md ✓"
  else
    err "下载 IDENTITY.md 失败"
    exit 1
  fi
  
  # 注册到 OpenClaw（如果命令存在）
  if command -v openclaw >/dev/null 2>&1; then
    info "正在注册到 OpenClaw..."
    openclaw agents add "$agent_name" --workspace "$agent_dir" --non-interactive 2>/dev/null || true
    ok "已注册到 OpenClaw"
    warn "运行 'openclaw gateway restart' 激活新智能体"
  fi
  
  echo ""
  printf "${GREEN}${BOLD}========================================${RESET}\n"
  printf "${GREEN}${BOLD}  安装成功！${RESET}\n"
  printf "${GREEN}${BOLD}========================================${RESET}\n"
  echo ""
  info "角色已安装到: $agent_dir"
  info "在 OpenClaw 中使用: @$agent_name"
  echo ""
}

# --- 入口 ---
main() {
  local agent_name="${1:-}"
  
  if [[ -z "$agent_name" ]]; then
    usage
  fi
  
  case "$agent_name" in
    help|--help|-h)
      usage
      ;;
    list|--list|-l)
      list_agents
      ;;
    *)
      install_agent "$agent_name"
      ;;
  esac
}

main "$@"