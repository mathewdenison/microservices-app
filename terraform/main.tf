terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7.1"
    }
  }

  required_version = ">= 1.3.0"
}

provider "aws" {
  region = "us-east-2"
}

# VPC module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.19.0"

  name = "microservices-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-2a", "us-east-2b", "us-east-2c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}

# SQS Module
module "sqs" {
  source = "./modules/sqs"
  vpc_id = module.vpc.vpc_id
}

# ECR Module
module "ecr" {
  source = "./modules/ecr"
}

# CodeBuild Module
module "codebuild" {
  source       = "./modules/codebuild"
  ecr_repos    = module.ecr.ecr_repo_urls
  iam_role_arn = module.sqs.iam_role_arn
}

# Run eksctl to create the EKS cluster
resource "null_resource" "eksctl_create_eks" {
  provisioner "local-exec" {
    command = "${path.module}/scripts/create-eks.sh"
  }

  triggers = {
    always_run = timestamp()
    subnet_ids = join(",", module.vpc.private_subnets)
  }
}

# Update kubeconfig AFTER the cluster is created
resource "null_resource" "update_kubeconfig" {
  depends_on = [null_resource.eksctl_create_eks]

  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --region us-east-2 --name microservices-cluster-ohio"
  }
}


provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
