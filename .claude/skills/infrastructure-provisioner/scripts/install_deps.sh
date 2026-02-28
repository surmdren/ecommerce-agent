#!/bin/bash
# 安装基础设施准备所需的依赖

set -e

echo "=== 安装基础设施准备依赖 ==="

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux"* ]]; then
    OS="linux"
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

# 安装 kubectl
echo "1. 安装 kubectl..."
if ! command -v kubectl &> /dev/null; then
    if [ "$OS" = "macos" ]; then
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    else
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    fi
fi
kubectl version --client --short | head -1

# 安装 Helm
echo "2. 安装 Helm..."
if ! command -v helm &> /dev/null; then
    if [ "$OS" = "macos" ]; then
        brew install helm
    else
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    fi
fi
helm version --short

# 安装 Terraform
echo "3. 安装 Terraform..."
if ! command -v terraform &> /dev/null; then
    if [ "$OS" = "macos" ]; then
        brew install terraform
    else
        wget -O- https://apt.releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip > /tmp/terraform.zip
        unzip /tmp/terraform.zip -d /usr/local/bin
    fi
fi
terraform version | head -1

# 安装 minikind (可选)
echo "4. minikind (可选)..."
if ! command -v minikind &> /dev/null; then
    echo "minikind 未安装，如需本地 K8s 请访问: https://minikube.sigs.k8s.io/docs/"
fi

echo ""
echo "=== 依赖安装完成 ==="
