output "ecr_repo_urls" {
  description = "ECR repository URLs"
  value = [
    aws_ecr_repository.request_service.repository_url,
    aws_ecr_repository.ai_processing_service.repository_url,
    aws_ecr_repository.response_formatting_service.repository_url,
    aws_ecr_repository.frontend.repository_url
  ]
}
