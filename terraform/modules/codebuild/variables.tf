variable "ecr_repos" {
  type        = list(string)
  description = "List of ECR repository URLs"
}

variable "iam_role_arn" {
  type        = string
  description = "IAM role ARN for CodeBuild to assume"
}
