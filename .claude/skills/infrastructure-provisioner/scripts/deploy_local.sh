#!/bin/bash
# 一键部署本地测试环境 (Local K8s)
# 用法: ./scripts/deploy_local.sh [项目名称] [postgres密码]

set -e

# 从项目根目录执行
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

PROJECT_NAME=${1:-myapp}
POSTGRES_PASSWORD=${2:-devpassword}
REDIS_PASSWORD=${3:-""}

echo "=== 部署本地测试环境: $PROJECT_NAME ==="
echo "项目根目录: $PROJECT_ROOT"

# 创建 infrastructure 目录
echo "1. 创建 infrastructure 目录..."
mkdir -p "$PROJECT_ROOT/infrastructure/terraform"
mkdir -p "$PROJECT_ROOT/infrastructure/helm"
mkdir -p "$PROJECT_ROOT/infrastructure/scripts"

# 创建 .gitignore
echo "2. 配置 .gitignore..."
cat > "$PROJECT_ROOT/infrastructure/.gitignore" << 'EOF'
# 环境变量文件（包含敏感信息）
.env.local
.env.production
.env.*.local

# Terraform 状态文件
*.tfstate
*.tfstate.*
*.tfvars
!example.tfvars

# Terraform 缓存
.terraform/
.terraform.lock.hcl
EOF

# 检查 K8s 连接
echo "3. 检查 K8s 连接..."
if ! kubectl cluster-info &> /dev/null; then
    echo "错误: 无法连接到 Kubernetes 集群"
    echo "请确保本地 K8s (minikube/k3s) 正在运行"
    exit 1
fi

# 检查 Helm
echo "4. 检查 Helm..."
if ! command -v helm &> /dev/null; then
    echo "错误: helm 未安装"
    exit 1
fi

# 添加 Helm 仓库
echo "5. 添加 Helm 仓库..."
helm repo add bitnami https://charts.bitnami.com/bitnami &> /dev/null || true
helm repo update &> /dev/null || true

# 创建命名空间
echo "6. 创建命名空间..."
kubectl create namespace postgres --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace redis --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace app --dry-run=client -o yaml | kubectl apply -f -

# 部署 PostgreSQL
echo "7. 部署 PostgreSQL..."
if helm status postgres -n postgres &> /dev/null; then
    helm upgrade postgres bitnami/postgresql \
        --namespace postgres \
        --set auth.postgresPassword="$POSTGRES_PASSWORD" \
        --set primary.service.type=NodePort \
        --set primary.service.nodePort=30432
else
    helm install postgres bitnami/postgresql \
        --namespace postgres \
        --set auth.postgresPassword="$POSTGRES_PASSWORD" \
        --set primary.service.type=NodePort \
        --set primary.service.nodePort=30432
fi

# 部署 Redis
echo "8. 部署 Redis..."
if [ -z "$REDIS_PASSWORD" ]; then
    AUTH_ENABLED=false
    REDIS_PASS=""
else
    AUTH_ENABLED=true
    REDIS_PASS="$REDIS_PASSWORD"
fi

if helm status redis -n redis &> /dev/null; then
    helm upgrade redis bitnami/redis \
        --namespace redis \
        --set auth.enabled=$AUTH_ENABLED \
        --set auth.password="$REDIS_PASS" \
        --set master.service.type=NodePort \
        --set master.service.nodePort=30379
else
    helm install redis bitnami/redis \
        --namespace redis \
        --set auth.enabled=$AUTH_ENABLED \
        --set auth.password="$REDIS_PASS" \
        --set master.service.type=NodePort \
        --set master.service.nodePort=30379
fi

# 等待 Pod 就绪
echo "9. 等待 Pod 就绪..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n postgres --timeout=300s || true
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=redis -n redis --timeout=300s || true

# 生成环境变量文件
echo "10. 生成环境变量文件..."
cat > "$PROJECT_ROOT/infrastructure/.env.local" << EOF
# ==============================================
# 本地测试环境配置
# 自动生成 - 请勿手动编辑
# ==============================================

# 环境
NODE_ENV=development
ENVIRONMENT=local

# PostgreSQL (Local K8s)
POSTGRES_HOST=localhost
POSTGRES_PORT=30432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
DATABASE_URL=postgresql://postgres:$POSTGRES_PASSWORD@localhost:30432/postgres

# Redis (Local K8s)
REDIS_HOST=localhost
REDIS_PORT=30379
REDIS_PASSWORD=$REDIS_PASSWORD
REDIS_URL=redis://localhost:30379

# AWS S3 (如需使用云 S3)
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=\${AWS_ACCESS_KEY_ID}
# AWS_SECRET_ACCESS_KEY=\${AWS_SECRET_ACCESS_KEY}
# S3_BUCKET=$PROJECT_NAME-local-storage

# 阿里云 OSS (可选)
# ALIYUN_REGION=cn-hangzhou
# ALIYUN_ACCESS_KEY_ID=\${ALIYUN_ACCESS_KEY_ID}
# ALIYUN_ACCESS_KEY_SECRET=\${ALIYUN_ACCESS_KEY_SECRET}
# OSS_BUCKET=$PROJECT_NAME-local-storage
EOF

# 生成示例文件
cat > "$PROJECT_ROOT/infrastructure/.env.example" << EOF
# 环境变量示例文件
# 复制此文件为 .env.local 并填写实际值

# 环境
NODE_ENV=development

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=30432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
DATABASE_URL=postgresql://postgres:your_password_here@localhost:30432/postgres

# Redis
REDIS_HOST=localhost
REDIS_PORT=30379
REDIS_PASSWORD=
REDIS_URL=redis://localhost:30379

# AWS S3
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
S3_BUCKET=$PROJECT_NAME-storage
EOF

# 输出连接信息
echo ""
echo "=== 部署完成 ==="
echo ""
echo "📁 生成的文件:"
echo "   - infrastructure/.env.local      (本地环境变量，已加入 .gitignore)"
echo "   - infrastructure/.env.example    (环境变量示例)"
echo "   - infrastructure/.gitignore      (忽略敏感文件)"
echo ""
echo "PostgreSQL 连接信息:"
echo "  Host: localhost"
echo "  Port: 30432"
echo "  Database: postgres"
echo "  Username: postgres"
echo "  Password: $POSTGRES_PASSWORD"
echo ""
echo "Redis 连接信息:"
echo "  Host: localhost"
echo "  Port: 30379"
echo "  Password: ${REDIS_PASSWORD:-无}"
echo ""
echo "加载环境变量:"
echo "   source infrastructure/.env.local"
echo ""
echo "测试连接:"
echo "   kubectl exec -it postgres-0 -n postgres -- psql -U postgres -c 'SELECT version();'"
echo ""
echo "查看所有服务:"
echo "   kubectl get svc --all-namespaces"
echo ""
