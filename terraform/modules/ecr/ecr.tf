resource "aws_ecr_repository" "request_service" {
  name = "request-service"
}

resource "aws_ecr_repository" "ai_processing_service" {
  name = "ai-processing-service"
}

resource "aws_ecr_repository" "response_formatting_service" {
  name = "response-formatting-service"
}

resource "aws_ecr_repository" "frontend" {
  name = "frontend"
}