output "vpc_id" {
  description = "The ID of the created VPC"
  value       = module.vpc.vpc_id
}

output "vpc_subnet_ids" {
  description = "Private subnet IDs for EKS cluster"
  value = module.pvc.private_subnets
}
