module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "20.8.3"

  cluster_name    = "microservices-cluster-ohio"
  cluster_version = "1.27"

  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  enable_irsa = true

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]
      min_size       = 1
      max_size       = 3
      desired_size   = 2
    }
  }

  manage_aws_auth_configmap = true
  aws_auth_roles = [
    {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/eks-sqs-role"
      username = "eks-sqs-role"
      groups   = ["system:masters"]
    }
  ]
}

data "aws_caller_identity" "current" {}
