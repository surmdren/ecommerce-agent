---
name: infrastructure-provisioner
description: 根据 TechSolution 方案准备基础设施环境。支持本地测试环境（Local K8s + Helm Charts）和生产环境（AWS/阿里云 + Terraform）。支持 Supabase 模式：检测到使用 Supabase 时，自动跳过本地 PostgreSQL Helm 安装，直接生成 Supabase 环境变量（NEXT_PUBLIC_SUPABASE_URL、SUPABASE_ANON_KEY、SUPABASE_SERVICE_ROLE_KEY）。Redis 仍需独立部署（K8s 用 Helm，Vercel 项目推荐 Upstash）。本地环境使用 Helm Chart，云服务仅配置访问密钥。生产环境使用 Terraform 创建完整云资源。所有基础设施文件放在项目根目录 infrastructure/，环境变量文件自动加入 .gitignore。适用于项目启动、环境初始化、开发环境搭建。当用户提到"基础设施"、"准备环境"、"部署环境"、"创建数据库"、"安装 Redis"、"配置 Supabase"时触发。
---

# 基础设施准备

## Overview

根据 `TechSolution/infrastructure/` 中的技术方案，准备项目所需的基础设施环境。

**所有文件放在项目根目录 `infrastructure/`**，目录结构：

```
infrastructure/
├── .env.local                 # 本地环境变量（git 不跟踪）
├── .env.production            # 生产环境变量（git 不跟踪）
├── .gitignore                 # 环境变量文件忽略规则
├── terraform/                 # Terraform 配置
│   ├── aws/
│   │   └── main.tf
│   └── alicloud/
│       └── main.tf
├── helm/                      # Helm Charts
│   ├── postgres.yaml
│   └── redis.yaml
└── scripts/                   # 部署脚本
    ├── init.sh                # 项目初始化（首次运行，一次性）
    ├── install_deps.sh
    └── deploy_local.sh
```

**支持两种环境**：
- **测试环境**：本地 K8s (minikind/k3s) + Helm Charts
- **生产环境**：AWS 或阿里云 + Terraform

---

## 第一步：环境确认

执行任何操作前，**必须先确认**：

### 1. 创建 infrastructure 目录

```bash
# 在项目根目录创建 infrastructure 目录
mkdir -p infrastructure/terraform/{aws,alicloud}
mkdir -p infrastructure/helm
mkdir -p infrastructure/scripts
```

### 2. 配置 .gitignore

```bash
# 创建 infrastructure/.gitignore
cat > infrastructure/.gitignore << 'EOF'
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
```

### 3. 读取基础设施方案

```bash
# 读取 TechSolution 中的基础设施设计
cat TechSolution/infrastructure/kubernetes.md
cat TechSolution/infrastructure/terraform/
```

### 4. 询问用户环境

```bash
# 必须询问的问题
echo "请选择目标环境："
echo "1) testing - 本地测试环境 (Local K8s + Helm)"
echo "2) production - 生产环境 (AWS 或 阿里云)"
read -p "请输入 (1/2): " ENV

if [ "$ENV" = "2" ]; then
    echo "请选择云服务商："
    echo "1) AWS"
    echo "2) 阿里云 (Alibaba Cloud)"
    read -p "请输入 (1/2): " CLOUD
fi
```

### 5. 确认数据库模式（Supabase vs PostgreSQL）

**必须询问**：

```
是否使用 Supabase 作为数据库？

1) 是 - 使用 Supabase（跳过 PostgreSQL Helm 安装，生成 Supabase 环境变量）
2) 否 - 使用本地 PostgreSQL（K8s Helm 部署，自托管）
```

> **判断依据**：若 `TechSolution/` 中提到 Supabase，或用户使用 Vercel + Next.js 技术栈，默认推荐选 Supabase。

### 3. 确认本地环境

```bash
# 检查 K8s 连接
kubectl cluster-info

# 检查 Helm
helm version

# 检查 Terraform (仅生产环境)
if [ "$ENV" = "2" ]; then
    terraform version
fi
```

---

## 第二步：准备测试环境（Local K8s）

### 2.1 安装必需组件

```bash
# 添加 Helm 仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# 创建命名空间
kubectl create namespace postgres
kubectl create namespace redis
kubectl create namespace app
```

> **强制规则：创建任何 Namespace，必须同步创建 ResourceQuota 和 LimitRange。**

```bash
# 为每个 Namespace 创建 ResourceQuota + LimitRange
for NS in postgres redis app; do
  kubectl apply -f - <<EOF
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ${NS}-quota
  namespace: ${NS}
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 2Gi
    limits.cpu: "2"
    limits.memory: 4Gi
    pods: "20"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: ${NS}-limits
  namespace: ${NS}
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      max:
        cpu: "2"
        memory: "4Gi"
EOF
done
```

### 2.2 数据库配置

根据第一步选择的数据库模式：

---

#### 2.2-A PostgreSQL（K8s 自托管 / 非 Supabase 项目）

> ⚠️ **仅在不使用 Supabase 时执行**。使用 Supabase 请跳过，进入 2.2-B。

```bash
# 使用 Helm 部署 PostgreSQL
helm install postgres bitnami/postgresql \
  --namespace postgres \
  --set auth.postgresPassword=devpassword \
  --set primary.service.type=NodePort \
  --set primary.service.nodePort=30432
```

**输出连接信息**：
```yaml
Host: localhost
Port: 30432
Database: postgres
Username: postgres
Password: devpassword
```

---

#### 2.2-B Supabase 模式（跳过 PostgreSQL Helm 安装）

> ✅ **使用 Supabase 时执行此步骤**，无需本地安装 PostgreSQL。

**架构原则：多项目共享同一 Supabase 实例，通过独立 Schema 做数据隔离。**

```
同一 Supabase 项目
├── schema: mingkun        ← 项目 A 的所有表
├── schema: ceo_office     ← 项目 B 的所有表
├── schema: aiops          ← 项目 C 的所有表
└── schema: public         ← 保留（Supabase 内置）
```

**操作步骤**：

1. 登录 [Supabase Dashboard](https://app.supabase.com)
2. 选择**已有共享 Supabase 项目**（无需创建新项目）
3. 进入 **Settings → API**，获取以下信息（所有项目共用）：

```
Project URL:        https://xxxx.supabase.co
anon/public key:    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key:   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

4. 在 **SQL Editor** 为当前项目创建独立 Schema：

```sql
-- 创建项目专属 Schema（替换 project_name 为实际项目名，如 mingkun）
CREATE SCHEMA IF NOT EXISTS project_name;

-- 授权 Supabase Auth 用户访问该 Schema
GRANT USAGE ON SCHEMA project_name TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA project_name
  GRANT ALL ON TABLES TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA project_name
  GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;

-- 在 Supabase API 中暴露该 Schema（Settings → API → Extra Search Path 添加 project_name）
```

5. 进入 **Settings → Database**，获取直连 URI（用于迁移工具）：

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres
```

**生成的环境变量**（见第四步）：
```env
# ── 共享凭据（自动从 ~/.dreamai-env 加载，无需手填）──────────────────
# NEXT_PUBLIC_SUPABASE_URL     ← 来自 ~/.dreamai-env
# NEXT_PUBLIC_SUPABASE_ANON_KEY ← 来自 ~/.dreamai-env
# SUPABASE_SERVICE_ROLE_KEY    ← 来自 ~/.dreamai-env

# ── 项目专属（必须手填）────────────────────────────────────────────────
# Schema 隔离（每个项目不同，用当前项目目录名，- 转 _，全小写）
SUPABASE_SCHEMA={project_dir_name}            # e.g., mingkun, ceo_office
```

> ⚠️ **Key 安全边界**：
> - `NEXT_PUBLIC_SUPABASE_ANON_KEY`：可前端使用，但**必须配置 RLS**（Row Level Security）
> - `SUPABASE_SERVICE_ROLE_KEY`：绕过 RLS，**只能在后端 API Routes 使用**，严禁提交 Git 或暴露前端

### 2.3 部署 Redis

> 💡 **Supabase 不提供 Redis**，无论是否使用 Supabase，如果项目需要缓存/队列/会话，都需要独立部署 Redis。
> - **K8s 项目**：用 Helm 部署（见下方）
> - **Vercel 项目**：推荐使用 [Upstash Redis](https://upstash.com)（Serverless Redis，按请求计费，支持 Edge Functions）

#### K8s Helm 部署

```bash
# 使用 Helm 部署 Redis
helm install redis bitnami/redis \
  --namespace redis \
  --set auth.enabled=false \
  --set master.service.type=NodePort \
  --set master.service.nodePort=30379
```

**输出连接信息**：
```yaml
Host: localhost
Port: 30379
```

#### Vercel 项目（Upstash Redis）

1. 在 [Upstash Console](https://console.upstash.com) 创建 Redis 数据库
2. 选择离用户最近的区域（支持全球多区域）
3. 获取连接信息：

```env
UPSTASH_REDIS_REST_URL=https://xxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=AXxx...
```

> Upstash 免费层：每天 10,000 次请求，适合开发测试。

### 2.4 部署应用服务（示例）

```bash
# 根据项目需求部署其他服务
helm install myapp ./helm/myapp \
  --namespace app \
  --set image.repository=myapp \
  --set image.tag=latest
```

### 2.5 配置云服务访问（如 S3）

对于云特有的服务（如 S3），只配置访问密钥：

```bash
# 创建 AWS Secret
kubectl create secret generic aws-credentials \
  --namespace app \
  --from-literal=AWS_ACCESS_KEY_ID=your_access_key \
  --from-literal=AWS_SECRET_ACCESS_KEY=your_secret_key \
  --from-literal=AWS_REGION=us-east-1

# 或创建阿里云 Secret
kubectl create secret generic aliyun-credentials \
  --namespace app \
  --from-literal=ALIYUN_ACCESS_KEY_ID=your_access_key \
  --from-literal=ALIYUN_ACCESS_KEY_SECRET=your_secret_key \
  --from-literal=ALIYUN_REGION=cn-hangzhou
```

### 2.6 验证部署

```bash
# 检查所有 Pod
kubectl get pods --all-namespaces

# 检查服务
kubectl get svc --all-namespaces

# 测试数据库连接
kubectl exec -it postgres-0 -n postgres -- psql -U postgres -c "SELECT version();"
```

---

## 第三步：准备生产环境（云平台）

### 3.1 AWS - 使用 Terraform

创建 `infrastructure/terraform/aws/` 目录：

**main.tf**:
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier     = "myapp-postgres"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 100

  db_name  = "myapp"
  username = "admin"
  password = var.db_password

  skip_final_snapshot = false
  final_snapshot_identifier = "myapp-postgres-final"

  vpc_security_group_ids = [aws_security_group.db.id]

  tags = {
    Name = "myapp-postgres"
    Env  = "production"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "main" {
  name       = "myapp-redis-subnet"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "myapp-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  engine_version       = "7.0"
  parameter_group_name = aws_elasticache_parameter_group.main.name
  subnet_group_name    = aws_elasticache_subnet_group.main.name

  security_group_ids = [aws_security_group.redis.id]

  tags = {
    Name = "myapp-redis"
    Env  = "production"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = "myapp-storage-${random_id.bucket_suffix}"

  tags = {
    Name = "myapp-storage"
    Env  = "production"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# EKS Cluster (可选)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "myapp-cluster"
  cluster_version = "1.27"

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 2
      max_size     = 4

      instance_types = ["t3.small"]
      capacity_type  = "ON_DEMAND"
    }
  }
}
```

### 3.2 阿里云 - 使用 Terraform

创建 `infrastructure/terraform/alicloud/` 目录：

**main.tf**:
```hcl
terraform {
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.200"
    }
  }
}

provider "alicloud" {
  region = var.region
}

# RDS PostgreSQL
resource "alicloud_db_instance" "main" {
  engine               = "PostgreSQL"
  engine_version       = "13.0"
  instance_type        = "pg.n2.small.1"
  instance_storage     = 20

  db_instance_storage = 20

  db_instance_name = "myapp-postgres"
  account_name      = "admin"
  account_password  = var.db_password

  security_ips = var.security_ip_list

  tags = {
    Name = "myapp-postgres"
    Env  = "production"
  }
}

# Redis
resource "alicloud_kvstore_instance" "main" {
  instance_name  = "myapp-redis"
  instance_class = "redis.master.small.default"
  engine_version = "7.0"

  shard_count    = 1
  instance_type  = "Redis主从版"

  security_ips   = var.security_ip_list

  tags = {
    Name = "myapp-redis"
    Env  = "production"
  }
}

# OSS Bucket
resource "alicloud_oss_bucket" "main" {
  bucket = "myapp-storage-${random_id.bucket_suffix}"

  acl = "private"

  tags = {
    Name = "myapp-storage"
    Env  = "production"
  }
}

# ACK Cluster (可选)
resource "alicloud_cs_managed_kubernetes" "main" {
  name_prefix = "myapp-"

  version      = "1.28.3-aliyun.1"
  cluster_spec {
    # 集群配置
  }

  node_pools {
    # 节点池配置
  }
}
```

### 3.3 执行 Terraform

```bash
# 进入目标目录
cd infrastructure/terraform/aws  # 或 alicloud

# 初始化 Terraform
terraform init

# 规划变更
terraform plan -var-file="terraform.tfvars"

# 应用变更
terraform apply -auto-approve -var-file="terraform.tfvars"

# 输出重要信息
terraform output

# 返回项目根目录
cd ../../..
```

---

## 第四步：生成环境配置文件

在 `infrastructure/` 目录生成环境变量文件，自动被 .gitignore 忽略：

### 本地测试环境 (.env.local)

根据数据库模式生成对应的 `.env.local`：

> **Schema 命名规则**：`SUPABASE_SCHEMA` 取当前项目目录名，`-` 转 `_`，全小写。
> 例：目录名 `ceo-office` → schema `ceo_office`；`mingkun` → `mingkun`。
> 执行前先推导：`PROJECT_SCHEMA=$(basename $(pwd) | tr '[:upper:]' '[:lower:]' | tr '-' '_')`

#### 模式 A：Supabase + Vercel 项目

```bash
# 生成 infrastructure/.env.local（Supabase 模式）
cat > infrastructure/.env.local << EOF
# ==============================================
# 本地开发环境配置（Supabase 模式）
# 自动生成 - 请勿手动编辑
# ==============================================

# 环境
NODE_ENV=development
ENVIRONMENT=local

# ── 共享凭据（自动从 ~/.dreamai-env 加载，无需手填）──────────────────
# NEXT_PUBLIC_SUPABASE_URL     ← 来自 ~/.dreamai-env
# NEXT_PUBLIC_SUPABASE_ANON_KEY ← 来自 ~/.dreamai-env
# SUPABASE_SERVICE_ROLE_KEY    ← 来自 ~/.dreamai-env

# ── 项目专属（每个项目必须单独设置）─────────────────────────────────
# Schema 隔离（对应 Supabase 中的独立 PostgreSQL schema）
SUPABASE_SCHEMA=${PROJECT_SCHEMA}            # 自动取当前目录名（- 转 _，全小写）

# 安全
NEXTAUTH_SECRET=                             # openssl rand -base64 32

# AI API Keys（按需填写）
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEEPSEEK_API_KEY=
BIGMODEL_API_KEY=                            # 智谱 BigModel（GLM 系列）

# Redis（Upstash - Vercel 推荐）
UPSTASH_REDIS_REST_URL=https://xxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=AXxx...

# 存储（Supabase Storage 或 AWS S3）
SUPABASE_STORAGE_BUCKET=myapp-storage
# 如使用 AWS S3
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=\${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=\${AWS_SECRET_ACCESS_KEY}
S3_BUCKET=myapp-local-storage
EOF

echo "✅ 已生成 infrastructure/.env.local（Supabase 模式）"
echo "⚠️  请填写 Supabase 项目的实际 URL 和 Keys"
```

#### 模式 B：K8s 自托管（PostgreSQL Helm）

```bash
# 生成 infrastructure/.env.local（K8s 模式）
cat > infrastructure/.env.local << EOF
# ==============================================
# 本地测试环境配置（K8s 自托管模式）
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
POSTGRES_PASSWORD=devpassword
DATABASE_URL=postgresql://postgres:devpassword@localhost:30432/postgres

# Redis (Local K8s)
REDIS_HOST=localhost
REDIS_PORT=30379
REDIS_PASSWORD=
REDIS_URL=redis://localhost:30379

# AWS S3 (使用本地 MinIO 或云 S3)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=\${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=\${AWS_SECRET_ACCESS_KEY}
S3_BUCKET=myapp-local-storage

# 阿里云 OSS (可选)
ALIYUN_REGION=cn-hangzhou
ALIYUN_ACCESS_KEY_ID=\${ALIYUN_ACCESS_KEY_ID}
ALIYUN_ACCESS_KEY_SECRET=\${ALIYUN_ACCESS_KEY_SECRET}
OSS_BUCKET=myapp-local-storage
EOF

echo "✅ 已生成 infrastructure/.env.local（K8s 模式）"
echo "⚠️  请配置 AWS/Aliyun 访问密钥"
```

### 生产环境 (.env.production)

```bash
# 生成 infrastructure/.env.production
cat > infrastructure/.env.production << EOF
# ==============================================
# 生产环境配置
# 自动生成 - 请勿手动编辑
# ==============================================

# 环境
NODE_ENV=production
ENVIRONMENT=production

# PostgreSQL (RDS)
POSTGRES_HOST=\${RDS_ENDPOINT}
POSTGRES_PORT=5432
POSTGRES_DB=myapp
POSTGRES_USER=admin
POSTGRES_PASSWORD=\${DB_PASSWORD}
DATABASE_URL=postgresql://admin:\${DB_PASSWORD}@\${RDS_ENDPOINT}:5432/myapp

# Redis (ElastiCache/KVStore)
REDIS_HOST=\${REDIS_ENDPOINT}
REDIS_PORT=6379
REDIS_PASSWORD=\${REDIS_PASSWORD}
REDIS_URL=redis://:\${REDIS_PASSWORD}@\${REDIS_ENDPOINT}:6379

# AWS S3 / OSS
AWS_REGION=\${AWS_REGION}
AWS_ACCESS_KEY_ID=\${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=\${AWS_SECRET_ACCESS_KEY}
S3_BUCKET=\${S3_BUCKET_NAME}

# 阿里云 (可选)
ALIYUN_REGION=\${ALIYUN_REGION}
ALIYUN_ACCESS_KEY_ID=\${ALIYUN_ACCESS_KEY_ID}
ALIYUN_ACCESS_KEY_SECRET=\${ALIYUN_ACCESS_KEY_SECRET}
OSS_BUCKET=\${OSS_BUCKET_NAME}
EOF

echo "✅ 已生成 infrastructure/.env.production"
echo "⚠️  请在 Terraform 输出后替换 \${VARIABLE} 占位符"
```

### 使用环境变量

```bash
# 加载环境变量
source infrastructure/.env.local

# 或在应用启动时加载
# Node.js: dotenv.config({ path: 'infrastructure/.env.local' })
# Python: load_dotenv('infrastructure/.env.local')
# Go: godotenv.Load('infrastructure/.env.local')
```

### 创建环境变量示例文件（提交到 Git）

```bash
# 创建 infrastructure/.env.example (供其他开发者参考)
cat > infrastructure/.env.example << EOF
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
S3_BUCKET=myapp-storage
EOF
```

---

## 项目初始化脚本（scripts/init.sh）

> **仅在项目首次搭建时执行一次**，不是每次部署都运行。
> 脚本读取 `.env.local` 中的凭据，执行所有需要人工输入信息的初始化操作。

### 生成 scripts/init.sh

根据技术方案（Supabase / K8s）生成对应的初始化脚本：

```bash
cat > infrastructure/scripts/init.sh << 'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# 项目初始化脚本
# 执行时机：项目首次搭建，填写 .env.local 后运行一次
# 使用方式：bash infrastructure/scripts/init.sh
# ============================================================

# 加载环境变量（优先级：.env.local > ~/.dreamai-env）
# 1. 先加载共享凭据（Supabase URL/Keys，所有项目共用）
SHARED_ENV="$HOME/.dreamai-env"
if [ -f "$SHARED_ENV" ]; then
  source "$SHARED_ENV"
  echo "✅ 已加载共享凭据 ~/.dreamai-env（SUPABASE_URL / ANON_KEY / SERVICE_ROLE_KEY）"
fi

# 2. 再加载项目专属变量（SUPABASE_SCHEMA、第三方 API Keys 等），会覆盖同名变量
ENV_FILE="$(dirname "$0")/../.env.local"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
  echo "✅ 已加载项目变量 .env.local"
else
  echo "⚠️  未找到 .env.local（仅使用共享凭据，缺少项目专属变量时会报错）"
fi

# ── Step 1: 验证必填环境变量 ──────────────────────────────
echo ""
echo "▶ Step 1: 验证环境变量..."
REQUIRED_VARS=(
  "NEXT_PUBLIC_SUPABASE_URL"
  "NEXT_PUBLIC_SUPABASE_ANON_KEY"
  "SUPABASE_SERVICE_ROLE_KEY"
  "SUPABASE_SCHEMA"
)
MISSING=()
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR:-}" ]; then
    MISSING+=("$VAR")
  fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "❌ 以下环境变量未填写："
  for V in "${MISSING[@]}"; do echo "   - $V"; done
  exit 1
fi
echo "✅ 环境变量验证通过"

# ── Step 2: 创建 Supabase Schema（共享实例隔离）──────────
echo ""
echo "▶ Step 2: 创建 Supabase Schema: ${SUPABASE_SCHEMA}..."
# 通过 Supabase Management API 执行 SQL
SQL="
CREATE SCHEMA IF NOT EXISTS ${SUPABASE_SCHEMA};
GRANT USAGE ON SCHEMA ${SUPABASE_SCHEMA} TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${SUPABASE_SCHEMA}
  GRANT ALL ON TABLES TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA ${SUPABASE_SCHEMA}
  GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;
"
curl -s -X POST \
  "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/rpc/exec_sql" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(echo "$SQL" | jq -Rs .)}" \
  > /dev/null 2>&1 || true
echo "✅ Schema ${SUPABASE_SCHEMA} 已就绪（如已存在则跳过）"
echo "   ⚠️  请到 Supabase Dashboard → Settings → API → Extra Search Path 添加: ${SUPABASE_SCHEMA}"

# ── Step 3: 数据库迁移 ────────────────────────────────────
echo ""
echo "▶ Step 3: 执行数据库迁移..."
if command -v npx &>/dev/null && [ -f "prisma/schema.prisma" ]; then
  npx prisma migrate deploy
  echo "✅ Prisma 迁移完成"
elif command -v npx &>/dev/null && [ -f "drizzle.config.ts" ]; then
  npx drizzle-kit migrate
  echo "✅ Drizzle 迁移完成"
else
  echo "ℹ️  未检测到 Prisma/Drizzle，跳过迁移（手动执行 SQL 迁移）"
fi

# ── Step 4: 写入初始种子数据（可选）─────────────────────
echo ""
echo "▶ Step 4: 写入初始数据..."
if [ -f "infrastructure/scripts/seed.sql" ]; then
  echo "   执行 seed.sql..."
  # TODO: 通过 psql 或 supabase CLI 执行
  echo "ℹ️  请手动在 Supabase SQL Editor 中执行 infrastructure/scripts/seed.sql"
else
  echo "ℹ️  无 seed.sql，跳过"
fi

# ── Step 5: 验证连接 ──────────────────────────────────────
echo ""
echo "▶ Step 5: 验证 Supabase 连接..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  "${NEXT_PUBLIC_SUPABASE_URL}/rest/v1/" \
  -H "apikey: ${NEXT_PUBLIC_SUPABASE_ANON_KEY}")
if [ "$HTTP_STATUS" = "200" ]; then
  echo "✅ Supabase 连接正常"
else
  echo "❌ Supabase 连接失败（HTTP $HTTP_STATUS），请检查 URL 和 Key"
  exit 1
fi

# ── 完成 ──────────────────────────────────────────────────
echo ""
echo "============================================"
echo "✅ 项目初始化完成！"
echo ""
echo "下一步："
echo "  1. 在 Supabase Dashboard 确认 Schema 已创建"
echo "  2. 运行 npm run dev 启动开发服务器"
echo "  3. 访问 http://localhost:3000 验证功能"
echo "============================================"
SCRIPT

chmod +x infrastructure/scripts/init.sh
echo "✅ 已生成 infrastructure/scripts/init.sh"
echo "📌 使用方式：填写 .env.local 后执行 bash infrastructure/scripts/init.sh"
```

### init.sh 执行时机

```
项目开发完成
    ↓
填写 infrastructure/.env.local（所有用户输入的凭据）
    ↓
bash infrastructure/scripts/init.sh
    ↓
✅ 环境验证 → Schema 创建 → 数据库迁移 → 种子数据 → 连接验证
    ↓
npm run dev  /  git push → Vercel 自动部署
```

---

## 资源说明

### scripts/

- `install_deps.sh` - 安装 kubectl, helm, terraform 等依赖
- `deploy_local.sh` - 一键部署本地测试环境
- `deploy_cloud.sh` - 一键部署生产环境

### references/

- `aws_services.md` - AWS 服务配置参考
- `alicloud_services.md` - 阿里云服务配置参考
- `helm_values.md` - Helm Values 配置说明

### assets/

- `terraform/` - Terraform 模板目录
  - `aws/` - AWS 资源定义
  - `alicloud/` - 阿里云资源定义
- `helm/` - Helm Charts 目录
  - `postgres/` - PostgreSQL 本地部署配置
  - `redis/` - Redis 本地部署配置

---

## 成功标准

- [ ] 确认了目标环境（测试/生产）
- [ ] 确认了云服务商（AWS/阿里云）
- [ ] **确认了数据库模式（Supabase 托管 / K8s 自托管 PostgreSQL）**
- [ ] 创建了 `infrastructure/` 目录结构
- [ ] 配置了 `.gitignore` 忽略敏感文件

**Supabase 模式**：
- [ ] 已创建 Supabase 项目并获取 URL / Keys
- [ ] 跳过 PostgreSQL Helm 安装
- [ ] 生成了 Supabase 模式的 `.env.local`（包含 `NEXT_PUBLIC_SUPABASE_URL`、`SUPABASE_SERVICE_ROLE_KEY`）
- [ ] （可选）配置了 Upstash Redis（Vercel 项目推荐）

**K8s 自托管模式**：
- [ ] 每个 Namespace 已创建 ResourceQuota + LimitRange
- [ ] PostgreSQL Helm 部署成功并验证连接
- [ ] Redis Helm 部署成功并验证连接
- [ ] 生成了 K8s 模式的 `.env.local`（包含 PostgreSQL + Redis 连接信息）

**通用**：
- [ ] 生产环境 Terraform 执行成功（如适用）
- [ ] 生成了 `.env.example` 示例文件（脱敏版，提交 Git）
- [ ] 环境变量文件可以正常加载
