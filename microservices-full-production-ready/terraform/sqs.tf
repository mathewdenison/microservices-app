resource "aws_iam_role" "eks_sqs_access" {
  name = "eks-sqs-role"
  assume_role_policy = data.aws_iam_policy_document.eks_assume_role.json
}

data "aws_iam_policy_document" "eks_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "sqs_policy" {
  name   = "EKS_SQS_Access_Policy"
  policy = data.aws_iam_policy_document.sqs_access.json
}

data "aws_iam_policy_document" "sqs_access" {
  statement {
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = [
      aws_sqs_queue.request_queue.arn,
      aws_sqs_queue.response_queue.arn
    ]
  }
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.eks_sqs_access.name
  policy_arn = aws_iam_policy.sqs_policy.arn
}

resource "aws_sqs_queue" "request_queue" {
  name = "request-queue"
}

resource "aws_sqs_queue" "response_queue" {
  name = "response-queue"
}

output "request_queue_url" {
  value = aws_sqs_queue.request_queue.id
}

output "response_queue_url" {
  value = aws_sqs_queue.response_queue.id
}

output "iam_role_arn" {
  value = aws_iam_role.eks_sqs_access.arn
}