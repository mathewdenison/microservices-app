terraform {
  backend "s3" {
    bucket         = "ai-proj-bucket"
    key            = "terraform/us-east-2/microservices-app.tfstate"
    region         = "us-east-2"
    encrypt        = true
  }
}
