---
name: dev-deploy
description: 将应用部署到Kubernetes集群。构建容器镜像、推送到镜像仓库、更新K8s配置、执行数据库迁移、验证部署状态、回滚支持。适用于部署到AWS EKS、阿里云ACK、本地K8s。支持多环境部署（dev/staging/prod）。当用户提到"部署"、"发布"、"上线"、"deploy"、"K8s部署"时触发。
---

# Kubernetes 部署执行器

## Overview

将开发完成的应用自动部署到 Kubernetes 集群，包含：

```
1. 构建容器镜像 (Docker Build)
2. 推送镜像仓库 (ECR/ACR/Docker Hub)
3. 更新 K8s 配置 (Helm/Kubectl)
4. 执行数据库迁移
5. 滚动更新部署
6. 验证部署状态
7. 生成部署报告
```

## 部署架构

```
┌─────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                    │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Build & Push Image                      │
│  Frontend → ECR/frontend:tag                         │
│  Backend  → ECR/backend:tag                          │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                      │
│  ┌─────────────────────────────────────────────┐    │
│  │              Namespace: dev/staging/prod     │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐      │    │
│  │  │Frontend │  │Backend  │  │Worker   │      │    │
│  │  │Deployment│ │Deployment│ │Job/Cron  │      │    │
│  │  └─────────┘  └─────────┘  └─────────┘      │    │
│  │                                             │    │
│  │  ┌─────────┐  ┌─────────┐                  │    │
│  │  │Service  │  │Ingress  │                  │    │
│  │  └─────────┘  └─────────┘                  │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Database Migration                      │
│              (Prisma Migrate)                        │
└─────────────────────────────────────────────────────┘
```

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `环境` | ❌ | 部署环境：dev(默认)/staging/prod |
| `服务` | ❌ | 指定部署服务：frontend/backend/all(默认) |
| `回滚` | ❌ | 回滚到上一版本 |

## Instructions

你是一名【DevOps 工程师 + SRE】，拥有 8 年云原生部署经验。

### 工作流程

#### Step 1: 部署前检查

**1.1 读取项目配置**
```bash
# 读取基础设施配置
read TechSolution/infrastructure/kubernetes.md

# 读取开发进度
read DevPlan/checklist.md

# 读取项目配置
read package.json
```

**1.2 确认前置条件**

检查以下项目：
- [ ] 所有模块开发完成
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] E2E 测试通过
- [ ] Dockerfile 存在
- [ ] K8s 配置文件存在
- [ ] Kubectl 已配置
- [ ] 镜像仓库访问权限

**1.3 确认部署环境**

**Namespace 命名规范**（方案 C - 环境优先）:
```
格式: <project>-<env>-<component>
基础设施: <project>-<env>-infra

示例:
- myapp-dev-backend
- myapp-dev-frontend
- myapp-staging-backend
- myapp-staging-frontend
- myapp-prod-backend
- myapp-prod-frontend
- myapp-dev-infra
- myapp-prod-infra
```

| 环境 | 用途 | Backend Namespace | Frontend Namespace | Infra Namespace | 资源规格 |
|------|------|-------------------|--------------------|--------------------|----------|
| dev | 开发测试 | `{project}-dev-backend` | `{project}-dev-frontend` | `{project}-dev-infra` | 低配置 |
| staging | 预发布 | `{project}-staging-backend` | `{project}-staging-frontend` | `{project}-staging-infra` | 中等配置 |
| prod | 生产环境 | `{project}-prod-backend` | `{project}-prod-frontend` | `{project}-prod-infra` | 高配置 + HPA |

**优势**:
- ✅ 按环境管理（运维视角）
- ✅ 前后端隔离（独立 RBAC）
- ✅ 基础设施独立（数据库、Redis、消息队列）
- ✅ 便于环境级别的资源配额和网络策略

> **⚠️ 强制规则：创建 Namespace 时必须同步创建 ResourceQuota + LimitRange**，否则单个项目可能耗尽集群资源：
> ```bash
> # 创建 namespace
> kubectl create namespace ${PROJECT}-${ENV}-backend
>
> # 同步创建 ResourceQuota
> kubectl apply -f - <<EOF
> apiVersion: v1
> kind: ResourceQuota
> metadata:
>   name: quota
>   namespace: ${PROJECT}-${ENV}-backend
> spec:
>   hard:
>     requests.cpu: "1"
>     requests.memory: 2Gi
>     limits.cpu: "2"
>     limits.memory: 4Gi
>     pods: "10"
> ---
> apiVersion: v1
> kind: LimitRange
> metadata:
>   name: limits
>   namespace: ${PROJECT}-${ENV}-backend
> spec:
>   limits:
>     - type: Container
>       default: {cpu: "500m", memory: "512Mi"}
>       defaultRequest: {cpu: "100m", memory: "128Mi"}
> EOF
> ```

#### Step 2: 构建容器镜像

**2.1 确认 Dockerfile**

**Backend Dockerfile**:
```dockerfile
# Backend Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
# 非 root 用户运行（安全基线）
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Frontend Dockerfile**:
```dockerfile
# Frontend Dockerfile (Multi-stage)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**2.2 构建镜像**

```bash
# 设置版本标签
VERSION=$(git describe --tags --always)
IMAGE_TAG=${VERSION:-latest}

# Backend
docker build -t backend:${IMAGE_TAG} -f backend/Dockerfile .

# Frontend
docker build -t frontend:${IMAGE_TAG} -f frontend/Dockerfile .
```

**2.3 镜像标签规范**

```
{registry}/{project}/{service}:{version}

示例:
- ECR: 123456.dkr.ecr.us-east-1.amazonaws.com/myapp/backend:v1.0.0
- ACR: registry.cn-hangzhou.aliyuncs.com/myapp/backend:v1.0.0
```

#### Step 3: 推送镜像仓库

**3.1 AWS ECR**

```bash
# 登录 ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456.dkr.ecr.us-east-1.amazonaws.com

# 标记镜像
docker tag backend:${IMAGE_TAG} 123456.dkr.ecr.us-east-1.amazonaws.com/myapp/backend:${IMAGE_TAG}

# 推送镜像
docker push 123456.dkr.ecr.us-east-1.amazonaws.com/myapp/backend:${IMAGE_TAG}
```

**3.2 阿里云 ACR**

```bash
# 登录 ACR
docker login --username=xxx@aliyun.com registry.cn-hangzhou.aliyuncs.com

# 标记并推送
docker tag backend:${IMAGE_TAG} registry.cn-hangzhou.aliyuncs.com/myapp/backend:${IMAGE_TAG}
docker push registry.cn-hangzhou.aliyuncs.com/myapp/backend:${IMAGE_TAG}
```

#### Step 4: 更新 K8s 配置

**4.1 确认 K8s 资源配置**

**Backend ServiceAccount** (`backend/k8s/serviceaccount.yaml`):
```yaml
# 独立 ServiceAccount，避免使用 default SA（权限过宽）
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend-sa
  namespace: {{PROJECT}}-{{ENV}}-backend
automountServiceAccountToken: false  # 不自动挂载 token，除非需要访问 K8s API
```

**Backend Deployment** (`backend/k8s/deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: {{PROJECT}}-{{ENV}}-backend  # 格式: <project>-<env>-<component>
  labels:
    app: {{PROJECT}}
    component: backend
    env: {{ENV}}
spec:
  replicas: {{REPLICAS}}
  selector:
    matchLabels:
      app: {{PROJECT}}
      component: backend
      env: {{ENV}}
  template:
    metadata:
      labels:
        app: {{PROJECT}}
        component: backend
        env: {{ENV}}
        version: "{{VERSION}}"
    spec:
      serviceAccountName: backend-sa  # 使用独立 SA，不用 default
      securityContext:                 # Pod 级别：防止特权容器逃逸宿主机
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: backend
        image: {{IMAGE_REGISTRY}}/backend:{{VERSION}}
        ports:
        - containerPort: 3000
        securityContext:               # Container 级别
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Frontend Deployment** (`frontend/k8s/deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: {{PROJECT}}-{{ENV}}-frontend  # 格式: <project>-<env>-<component>
  labels:
    app: {{PROJECT}}
    component: frontend
    env: {{ENV}}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {{PROJECT}}
      component: frontend
      env: {{ENV}}
  template:
    metadata:
      labels:
        app: {{PROJECT}}
        component: frontend
        env: {{ENV}}
        version: "{{VERSION}}"
    spec:
      containers:
      - name: frontend
        image: {{IMAGE_REGISTRY}}/frontend:{{VERSION}}
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_API_URL
          value: "http://backend.{{PROJECT}}-{{ENV}}-backend.svc.cluster.local"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

**Backend Service** (`backend/k8s/service.yaml`):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: {{PROJECT}}-{{ENV}}-backend
  labels:
    app: {{PROJECT}}
    component: backend
    env: {{ENV}}
spec:
  type: ClusterIP
  selector:
    app: {{PROJECT}}
    component: backend
    env: {{ENV}}
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
```

**Frontend Service** (`frontend/k8s/service.yaml`):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: {{PROJECT}}-{{ENV}}-frontend
  labels:
    app: {{PROJECT}}
    component: frontend
    env: {{ENV}}
spec:
  type: ClusterIP
  selector:
    app: {{PROJECT}}
    component: frontend
    env: {{ENV}}
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
```

**Ingress** (`k8s/ingress.yaml`):
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: {{PROJECT}}-{{ENV}}-frontend  # 通常放在 frontend namespace
  labels:
    app: {{PROJECT}}
    env: {{ENV}}
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    # 允许跨 namespace 引用 backend service
    nginx.ingress.kubernetes.io/service-upstream: "true"
spec:
  rules:
  - host: {{DOMAIN}}
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            # 跨 namespace 引用，需要使用 ExternalName Service 或配置
            name: backend
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

**跨 Namespace 服务引用**（创建 ExternalName Service）:
```yaml
# 在 frontend namespace 中创建指向 backend 的引用
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: {{PROJECT}}-{{ENV}}-frontend
spec:
  type: ExternalName
  externalName: backend.{{PROJECT}}-{{ENV}}-backend.svc.cluster.local
  ports:
  - port: 80
```

**4.2 更新配置**

```bash
# 设置环境变量
export PROJECT=myapp  # 项目名称
export ENV=staging    # 环境: dev/staging/prod
export VERSION=$(git describe --tags --always)
export IMAGE_REGISTRY=123456.dkr.ecr.us-east-1.amazonaws.com/myapp

# 使用 envsubst 替换变量并部署到对应 namespace
envsubst < backend/k8s/deployment.yaml | kubectl apply -f -
envsubst < backend/k8s/service.yaml | kubectl apply -f -
envsubst < frontend/k8s/deployment.yaml | kubectl apply -f -
envsubst < frontend/k8s/service.yaml | kubectl apply -f -
envsubst < k8s/ingress.yaml | kubectl apply -f -
envsubst < k8s/external-name-service.yaml | kubectl apply -f -
```

#### Step 5: 执行数据库迁移

**5.1 创建 Migration Job**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate-${VERSION}
  namespace: ${PROJECT}-${ENV}-backend  # 在 backend namespace 中运行
  labels:
    app: ${PROJECT}
    component: backend
    env: ${ENV}
    job-type: migration
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: ${IMAGE_REGISTRY}/backend:${VERSION}
        command: ["npm", "run", "migrate:deploy"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: database-url
      restartPolicy: Never
  backoffLimit: 3
```

**5.2 执行迁移**

```bash
# 应用 Migration Job
envsubst < k8s/migration-job.yaml | kubectl apply -f -

# 等待迁移完成
kubectl wait --for=condition=complete --timeout=300s \
  job/db-migrate-${VERSION} -n ${PROJECT}-${ENV}-backend

# 检查迁移状态
kubectl logs job/db-migrate-${VERSION} -n ${PROJECT}-${ENV}-backend
```

#### Step 6: 滚动更新部署

**6.1 监控滚动更新**

```bash
# Watch rollout status
kubectl rollout status deployment/backend -n ${PROJECT}-${ENV}-backend
kubectl rollout status deployment/frontend -n ${PROJECT}-${ENV}-frontend

# 查看更新状态
kubectl get deployments -n ${PROJECT}-${ENV}-backend
kubectl get deployments -n ${PROJECT}-${ENV}-frontend

# 查看所有环境的部署状态
kubectl get deployments --all-namespaces -l app=${PROJECT},env=${ENV}
```

**6.2 验证健康检查**

```bash
# 检查 Pod 状态
kubectl get pods -n ${ENV}

# 查看日志
kubectl logs -f deployment/backend -n ${ENV}

# 检查事件
kubectl get events -n ${ENV} --sort-by='.lastTimestamp'
```

#### Step 7: 验证部署

**7.1 服务可用性检查**

```bash
# Port Forward 测试
kubectl port-forward -n ${ENV} svc/backend 8080:80

# 健康检查
curl http://localhost:8080/health
curl http://localhost:8080/ready

# API 测试
curl http://localhost:8080/api/health
```

**7.2 端到端验证**

```bash
# 获取 Ingress URL
kubectl get ingress -n ${ENV}

# 测试完整请求
curl https://${DOMAIN}/api/health
curl https://${DOMAIN}/
```

**7.3 监控指标**

```bash
# 查看资源使用
kubectl top pods -n ${ENV}
kubectl top nodes

# 查看 HPA 状态（如果配置）
kubectl get hpa -n ${ENV}
```

#### Step 8: 回滚策略（如果失败）

**8.1 查看部署历史**

```bash
kubectl rollout history deployment/backend -n ${ENV}
```

**8.2 回滚到上一版本**

```bash
# 回滚到上一版本
kubectl rollout undo deployment/backend -n ${ENV}
kubectl rollout undo deployment/frontend -n ${ENV}

# 回滚到指定版本
kubectl rollout undo deployment/backend -n ${ENV} --to-revision=3
```

**8.3 验证回滚**

```bash
# 确认回滚完成
kubectl rollout status deployment/backend -n ${ENV}

# 验证服务正常
curl https://${DOMAIN}/api/health
```

#### Step 9: 生成部署报告

```markdown
# 部署报告 - ${ENV}

## 目录

- [部署概览](#部署概览)
- [镜像信息](#镜像信息)
- [部署状态](#部署状态)
- [健康检查](#健康检查)
- [数据库迁移](#数据库迁移)
- [访问地址](#访问地址)
- [验证测试](#验证测试)
- [回滚计划](#回滚计划)
- [注意事项](#注意事项)

---

## 部署概览
- 部署环境: ${ENV}
- 部署时间: YYYY-MM-DD HH:mm:ss
- 版本: ${VERSION}
- 执行人: ${USER}

## 镜像信息
| 服务 | 镜像 | Tag |
|------|------|-----|
| Backend | ${IMAGE_REGISTRY}/backend | ${VERSION} |
| Frontend | ${IMAGE_REGISTRY}/frontend | ${VERSION} |

## 部署状态
| 资源 | 状态 | 副本数 |
|------|------|--------|
| backend | ✅ Running | 3/3 |
| frontend | ✅ Running | 2/2 |

## 健康检查
| 服务 | 健康检查 | 就绪检查 |
|------|---------|---------|
| backend | ✅ Pass | ✅ Pass |
| frontend | ✅ Pass | ✅ Pass |

## 数据库迁移
- 迁移版本: ${VERSION}
- 迁移状态: ✅ Success
- 迁移时间: XX 秒

## 访问地址
- 环境: ${ENV}
- 域名: ${DOMAIN}
- API: https://${DOMAIN}/api
- 前端: https://${DOMAIN}

## 验证测试
- [ ] API 健康检查通过
- [ ] 前端页面加载正常
- [ ] 数据库连接正常
- [ ] 核心功能验证通过

## 回滚计划
- 上一版本: ${PREV_VERSION}
- 回滚命令: `kubectl rollout undo deployment/backend -n ${ENV}`
- 回滚状态: 未执行

## 注意事项
- 监控告警配置已启用
- 日志聚合已配置
- 备份已完成
```

## Output

### 目录结构

```
infrastructure/
├── k8s/
│   ├── base/              # 基础配置
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── overlays/          # 环境配置
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── scripts/
│       ├── build.sh       # 构建脚本
│       ├── deploy.sh      # 部署脚本
│       └── rollback.sh    # 回滚脚本
└── reports/
    └── deployment-{ENV}-{VERSION}.md
```

## 多环境配置

使用 Kustomize 管理多环境：

**base/kustomization.yaml**:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml

images:
  - name: backend
    newName: ${IMAGE_REGISTRY}/backend
    newTag: ${VERSION}
  - name: frontend
    newName: ${IMAGE_REGISTRY}/frontend
    newTag: ${VERSION}
```

**overlays/dev/kustomization.yaml**:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# 注意：多 namespace 环境需要分别配置
namespace: myapp-dev-backend  # 为 backend 组件配置

resources:
  - ../../base

replicas:
- name: backend
  count: 1

patchesStrategicMerge:
- patch-dev.yaml
```

**overlays/dev-frontend/kustomization.yaml** (单独配置前端):
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: myapp-dev-frontend

resources:
  - ../../base/frontend

replicas:
- name: frontend
  count: 1

patchesStrategicMerge:
- patch-dev-frontend.yaml
```

**使用方式**:
```bash
# 部署到 dev
kubectl apply -k infrastructure/k8s/overlays/dev

# 部署到 staging
kubectl apply -k infrastructure/k8s/overlays/staging

# 部署到 prod
kubectl apply -k infrastructure/k8s/overlays/prod
```

## 安全配置

### Secrets 管理

**使用 K8s Secrets**:
```bash
# 为每个 namespace 创建 Secret
kubectl create secret generic backend-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=jwt-secret='...' \
  -n ${PROJECT}-${ENV}-backend

kubectl create secret generic frontend-secrets \
  --from-literal=api-key='...' \
  -n ${PROJECT}-${ENV}-frontend

# 使用 External Secrets Operator (推荐)
# 自动从 AWS Secrets Manager /阿里云 KMS 同步到各 namespace
```

### 镜像安全

```bash
# 镜像扫描
trivy image ${IMAGE_REGISTRY}/backend:${VERSION}

# 签名验证
cosign verify ${IMAGE_REGISTRY}/backend:${VERSION}
```

## 监控与告警

### Prometheus + Grafana

```yaml
# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend
  namespace: ${ENV}
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: http
    path: /metrics
```

### 健康检查端点

```typescript
// Backend health checks
app.get('/health', async (req, reply) => {
  // 简单存活检查
  return { status: 'ok' };
});

app.get('/ready', async (req, reply) => {
  // 就绪检查（检查依赖）
  const db = await prisma.$queryRaw`SELECT 1`;
  const redis = await cache.ping();
  if (db && redis) {
    return { status: 'ready', database: 'ok', cache: 'ok' };
  }
  throw new Error('Not ready');
});
```

## Examples

### 示例 1: 部署到开发环境
```bash
# 用户请求
请部署到开发环境

# Claude 执行流程
1. 检查前置条件
2. 构建镜像
3. 推送到 ECR
4. 更新 K8s 配置
5. 执行数据库迁移
6. 验证部署
7. 生成报告
```

### 示例 2: 部署到生产环境
```bash
# 用户请求
请部署到生产环境

# Claude 执行流程
1. 二次确认（生产环境）
2. 完整的健康检查
3. 数据库备份
4. 金丝雀部署（可选）
5. 全量部署
6. 监控验证
7. 生成发布报告
```

### 示例 3: 回滚
```bash
# 用户请求
部署有问题，请回滚

# Claude 执行流程
1. 查看当前状态
2. 分析失败原因
3. 执行回滚
4. 验证回滚成功
5. 生成回滚报告
```

## 适用场景

- 首次部署到 K8s
- 日常版本发布
- 紧急热修复部署
- 多环境部署
- 金丝雀/蓝绿部署

## 注意事项

1. **生产环境谨慎**: 部署前务必备份，建议先在 staging 验证
2. **数据库迁移**: 迁移脚本必须可回滚
3. **健康检查**: 确保健康检查端点正确配置
4. **资源限制**: 设置合理的资源 limits 和 requests
5. **监控告警**: 部署后关注监控指标
6. **回滚准备**: 始终准备回滚方案
7. **版本标签**: 使用语义化版本号，便于追溯
