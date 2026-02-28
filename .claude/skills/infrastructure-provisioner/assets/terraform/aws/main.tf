# AWS Infrastructure - Terraform Configuration
# 根据项目需求调整参数

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

# Variables
variable "aws_region" {
  description = "AWS region"
  type    = string
  default = "us-east-1"
}

variable "db_password" {
  description = "Database password"
  type      = string
  sensitive = true
}

variable "subnet_ids" {
  description = "VPC subnet IDs"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "security_ip_list" {
  description = "Allowed IP addresses for security groups"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Resource: RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-postgres"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"

  db_name  = var.db_name
  username = "admin"
  password = var.db_password

  skip_final_snapshot         = false
  final_snapshot_identifier = "${var.project_name}-postgres-final"

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  tags = {
    Name = "${var.project_name}-postgres"
    Env  = var.environment
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-subnet-group"
  subnet_ids = var.subnet_ids
  tags = {
    Name = "${var.project_name}-subnet-group"
  }
}

# Resource: ElastiCache Redis
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-redis-subnet"
  subnet_ids = var.subnet_ids
}

resource "aws_elasticache_parameter_group" "main" {
  family = "redis7"
  name   = "${var.project_name}-redis-params"

  parameter {
    name  = "cluster-enabled"
    value = "yes"
  }
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  engine_version       = "7.0"
  parameter_group_name = aws_elasticache_parameter_group.main.name
  subnet_group_name    = aws_elasticache_subnet_group.main.name

  security_group_ids = [aws_security_group.redis.id]

  tags = {
    Name = "${var.project_name}-redis"
    Env  = var.environment
  }
}

# Resource: S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = "${var.project_name}-storage-${random_id.bucket_suffix}"

  tags = {
    Name = "${var.project_name}-storage"
    Env  = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Security Groups
resource "aws_security_group" "db" {
  name        = "${var.project_name}-db-sg"
  description = "Security group for RDS"
  vpc_id      = var.vpc_id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.security_ip_list
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-db-sg"
  }
}

resource "aws_security_group" "redis" {
  name        = "${var.project_name}-redis-sg"
  description = "Security group for ElastiCache"
  vpc_id      = var.vpc_id

  ingress {
    description = "Redis"
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = var.security_ip_list
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-redis-sg"
  }
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
  description = "RDS endpoint"
  value       = aws_db_instance.main.endpoint
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_cluster.main.cluster_address
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.main.bucket
}
