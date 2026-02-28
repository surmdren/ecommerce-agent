# Alibaba Cloud Infrastructure - Terraform Configuration
# 根据项目需求调整参数

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

# Variables
variable "region" {
  description = "Alibaba Cloud region"
  type    = string
  default = "cn-hangzhou"
}

variable "db_password" {
  description = "Database password"
  type      = string
  sensitive = true
}

variable "security_ip_list" {
  description = "Allowed IP addresses for security groups"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Resource: RDS PostgreSQL
resource "alicloud_db_instance" "main" {
  engine               = "PostgreSQL"
  engine_version       = "13.0"
  instance_type        = "pg.n2.small.1"
  instance_storage     = 20

  db_instance_storage = 20

  db_instance_name = var.db_name
  account_name      = "admin"
  account_password  = var.db_password

  security_ips = var.security_ip_list

  tags {
    Name = "${var.project_name}-postgres"
    Env  = var.environment
  }
}

# Resource: Redis (KVStore)
resource "alicloud_kvstore_instance" "main" {
  instance_name  = "${var.project_name}-redis"
  instance_class = "redis.master.small.default"
  engine_version = "7.0"

  shard_count    = 1
  instance_type  = "Redis主从版"

  security_ips   = var.security_ip_list

  tags {
    Name = "${var.project_name}-redis"
    Env  = var.environment
  }
}

# Resource: OSS Bucket
resource "alicloud_oss_bucket" "main" {
  bucket = "${var.project_name}-storage-${random_id.bucket_suffix}"

  acl = "private"

  tags = {
    Name = "${var.project_name}-storage"
    Env  = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Project variables
variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment (testing/production)"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

# Outputs
output "rds_endpoint" {
  description = "RDS connection string"
  value       = "${alicloud_db_instance.main.connection_string}"
}

output "redis_endpoint" {
  description = "Redis connection string"
  value       = "${alicloud_kvstore_instance.main.connection_domain}"
}

output "oss_bucket_name" {
  description = "OSS bucket name"
  value       = alicloud_oss_bucket.main.bucket
}
