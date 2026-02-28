#!/bin/bash
# Project Manager Dispatcher
# 每 N 分钟检查 master-checklist，自动触发下一个待执行的 Phase
#
# 用法: bash setup_pm_cron.sh /path/to/project [interval_minutes]
# 默认每 10 分钟检查一次

PROJECT_DIR="${1:?请提供项目目录路径}"
INTERVAL="${2:-10}"
CHECKLIST="${PROJECT_DIR}/ProjectManager/master-checklist.md"
LOG="${PROJECT_DIR}/ProjectManager/pm.log"
DISPATCH_SCRIPT="${PROJECT_DIR}/ProjectManager/pm_dispatch.sh"

mkdir -p "${PROJECT_DIR}/ProjectManager"

# ── 生成调度脚本 ────────────────────────────────────────────────
cat > "${DISPATCH_SCRIPT}" << 'DISPATCH'
#!/bin/bash
set -euo pipefail

PROJECT_DIR="__PROJECT_DIR__"
CHECKLIST="${PROJECT_DIR}/ProjectManager/master-checklist.md"
LOG="${PROJECT_DIR}/ProjectManager/pm.log"
BLOCKED="${PROJECT_DIR}/ProjectManager/BLOCKED.md"
REQUIREMENTS="${PROJECT_DIR}/ProjectManager/initial-requirements.md"

timestamp() { date '+%Y-%m-%d %H:%M'; }
log() { echo "[$(timestamp)] $*" | tee -a "${LOG}"; }

# 标记 Phase 完成
mark_done() {
  local label="$1"
  sed -i.bak "s/^- \[ \] ${label}/- [x] ${label}/" "${CHECKLIST}"
  rm -f "${CHECKLIST}.bak"
  log "✅ ${label} 完成"
}

# 检查产物是否存在来判断 Phase 是否已完成
artifact_exists() { [[ -e "${PROJECT_DIR}/$1" ]]; }

# 执行 claude skill（非交互模式）
run_skill() {
  local prompt="$1"
  log "  → claude: ${prompt}"
  cd "${PROJECT_DIR}" && claude --print "${prompt}" 2>&1 | tee -a "${LOG}"
}

log "=== PM Dispatcher 运行 ==="

# 检查 checklist 是否存在
if [[ ! -f "${CHECKLIST}" ]]; then
  log "❌ master-checklist.md 不存在，退出"
  exit 0
fi

# 全部完成则退出
if ! grep -q "^- \[ \]" "${CHECKLIST}"; then
  log "🎉 所有 Phase 已完成！"
  PROJECT_NAME=$(basename "${PROJECT_DIR}")
  log "产品地址: https://${PROJECT_NAME}.wise-optics.com"
  # 自动取消 cron
  crontab -l 2>/dev/null | grep -v "pm_dispatch.sh" | crontab - 2>/dev/null || true
  log "Cron 已自动取消"
  exit 0
fi

# 找第一个未完成的 Phase
NEXT_LINE=$(grep "^- \[ \]" "${CHECKLIST}" | head -1)
# 提取 "Phase N" 或 "Phase Na/Nb" 标识
NEXT_LABEL=$(echo "${NEXT_LINE}" | sed 's/^- \[ \] //' | sed 's/:.*//')

log "🔄 下一步: ${NEXT_LABEL}"

cd "${PROJECT_DIR}" || exit 1
PROJECT_NAME=$(basename "${PROJECT_DIR}")

case "${NEXT_LABEL}" in

  "Phase 1"*)
    REQS=$(cat "${REQUIREMENTS}" 2>/dev/null || echo "见 PRD/requirements.md")
    run_skill "/requirement-detail ${REQS}"
    artifact_exists "PRD/requirements.md" && mark_done "Phase 1"
    ;;

  "Phase 2"*)
    run_skill "/tech-architecture 基于 PRD/requirements.md"
    artifact_exists "Architecture" && mark_done "Phase 2"
    ;;

  "Phase 3"*)
    run_skill "/tech-solution 基于 PRD/requirements.md 和 Architecture/"
    artifact_exists "TechSolution" && mark_done "Phase 3"
    ;;

  "Phase 4"*)
    run_skill "/ui-ux-pro-max 基于 PRD/requirements.md 定义设计系统规范（色彩/字体/组件/间距），输出到 Design/design-system.md"
    artifact_exists "Design/design-system.md" && mark_done "Phase 4"
    ;;

  "Phase 5"*)
    run_skill "/uiux-design 基于 PRD/requirements.md 和 Design/design-system.md，严格遵循设计系统，为每个功能模块生成详细页面设计规格"
    artifact_exists "Design/pages" && mark_done "Phase 5"
    ;;

  "Phase 6"*)
    run_skill "/dev-planner 基于 PRD/requirements.md 和 TechSolution/ 拆解开发模块"
    artifact_exists "DevPlan/checklist.md" && mark_done "Phase 6"
    ;;

  "Phase 7"*)
    # 按需执行：检查 TechSolution 是否包含外部服务
    if grep -rqiE "postgresql|redis|mongodb|mysql|elasticsearch" \
        "${PROJECT_DIR}/TechSolution/" 2>/dev/null; then
      run_skill "/infrastructure-provisioner 基于 TechSolution/ 准备本地 K8s 环境"
      artifact_exists "infrastructure" && mark_done "Phase 7"
    else
      sed -i.bak 's/^- \[ \] Phase 7/- [SKIP] Phase 7/' "${CHECKLIST}"
      rm -f "${CHECKLIST}.bak"
      log "[SKIP] Phase 7: TechSolution 无需外部基础设施"
    fi
    ;;

  "Phase 8a"*)
    run_skill "/dev-executor 读取 DevPlan/ 按模块逐个实现，严格 TDD（Red→Green→Refactor），单元测试覆盖率>80%，API测试禁止Mock，生成测试报告到 DevPlan/reports/"
    artifact_exists "DevPlan/reports" && mark_done "Phase 8a"
    ;;

  "Phase 8b"*)
    run_skill "/dev-autopilot 设置 30 分钟 cron，自动继续 DevPlan/ 中所有未完成模块"
    # dev-autopilot 负责其内部循环，PM 标记为已启动
    mark_done "Phase 8b"
    log "  ℹ️  dev-autopilot 已启动，内置 30 分钟 cron 持续推进"
    log "  ℹ️  PM cron 将在下次检查时验证 DevPlan 是否全部完成"
    # 如果 DevPlan 还未完成，下次 PM cron 会等待（Phase 9 未触发）
    ;;

  "Phase 9"*)
    # 前置检查：DevPlan 所有模块是否完成
    if grep -q "^\- \[ \]" "${PROJECT_DIR}/DevPlan/checklist.md" 2>/dev/null; then
      log "⏳ Phase 9 等待: DevPlan 模块尚未全部完成，本次跳过"
      exit 0
    fi
    run_skill "/release-qa 基于 PRD Architecture TechSolution DevPlan 做全面技术验收测试，禁止 Mock"
    artifact_exists "QA/release-qa-report.md" && mark_done "Phase 9"
    ;;

  "Phase 10"*)
    run_skill "/uat-testing 从用户视角执行 Playwright E2E 测试，验证核心业务路径"
    artifact_exists "UAT/uat-report.md" && mark_done "Phase 10"
    ;;

  "Phase 11"*)
    run_skill "/security-pentest 扫描 OWASP Top 10，生成安全报告到 Security/pentest-report.md"
    artifact_exists "Security/pentest-report.md" && mark_done "Phase 11"
    ;;

  "Phase 12"*)
    run_skill "/dev-deploy 构建镜像，推送仓库，部署到 K8s，验证健康检查"
    mark_done "Phase 12"
    ;;

  "Phase 13"*)
    # 纯 shell，不需要 Claude
    log "  执行 cloudflared tunnel 域名映射..."
    cloudflared tunnel list | grep -q "${PROJECT_NAME}" || \
      cloudflared tunnel create "${PROJECT_NAME}"
    TUNNEL_ID=$(cloudflared tunnel list | grep "${PROJECT_NAME}" | awk '{print $1}')
    cloudflared tunnel route dns "${TUNNEL_ID}" "${PROJECT_NAME}.wise-optics.com"
    cat > ~/.cloudflared/config.yml << EOF
tunnel: ${TUNNEL_ID}
credentials-file: ${HOME}/.cloudflared/${TUNNEL_ID}.json
ingress:
  - hostname: ${PROJECT_NAME}.wise-optics.com
    service: http://localhost:8080
  - service: http_status:404
EOF
    kubectl port-forward -n "${PROJECT_NAME}-prod-frontend" \
      svc/frontend 8080:80 &
    cloudflared tunnel --config ~/.cloudflared/config.yml \
      run "${TUNNEL_ID}" &
    mark_done "Phase 13"
    log "🌐 https://${PROJECT_NAME}.wise-optics.com 已上线"
    ;;

  *)
    log "⚠️  未识别的 Phase: ${NEXT_LABEL}"
    ;;

esac

log "=== Dispatch 结束 ==="
DISPATCH

# 替换项目路径占位符
sed -i.bak "s|__PROJECT_DIR__|${PROJECT_DIR}|g" "${DISPATCH_SCRIPT}"
rm -f "${DISPATCH_SCRIPT}.bak"
chmod +x "${DISPATCH_SCRIPT}"

# ── 注册 cron ──────────────────────────────────────────────────
CRON_ENTRY="*/${INTERVAL} * * * * bash ${DISPATCH_SCRIPT} >> ${LOG} 2>&1"
( crontab -l 2>/dev/null | grep -v "pm_dispatch.sh" ; echo "${CRON_ENTRY}" ) | crontab -

echo "✅ PM Dispatcher Cron 已设置"
echo "   项目:     ${PROJECT_DIR}"
echo "   间隔:     每 ${INTERVAL} 分钟"
echo "   调度脚本: ${DISPATCH_SCRIPT}"
echo "   日志:     ${LOG}"
echo ""
echo "实时监控: tail -f ${LOG}"
echo "查看进度: cat ${CHECKLIST}"
echo "取消 cron: crontab -l | grep -v pm_dispatch.sh | crontab -"
