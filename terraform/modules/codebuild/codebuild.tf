resource "aws_iam_role" "codebuild_service_role" {
  name = "CodeBuildServiceRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "codebuild.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "codebuild_policy_attachment" {
  role       = aws_iam_role.codebuild_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_codebuild_project" "build_project" {
  name          = "MicroservicesBuildProject"
  service_role  = aws_iam_role.codebuild_service_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:6.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true

    environment_variable {
      name  = "AWS_REGION"
      value = "us-east-2"
    }

    environment_variable {
      name  = "ECR_URI"
      value = "883640716669.dkr.ecr.us-east-2.amazonaws.com"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "codepipeline/buildspec.yaml"
  }
}

resource "aws_codebuild_project" "deploy_project" {
  name         = "MicroservicesDeployProject"
  service_role = aws_iam_role.codebuild_service_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:6.0"
    type         = "LINUX_CONTAINER"
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "codepipeline/deployspec.yaml"
  }
}
