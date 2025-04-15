resource "aws_ssm_parameter" "microservices_iam_role" {
  name  = "/microservices/iam_role_arn"
  type  = "String"
  value = aws_iam_role.codebuild_role.arn
}

resource "aws_iam_role_policy_attachment" "alb_permissions" {
  role       = var.eks_node_role_name
  policy_arn = "arn:aws:iam::aws:policy/ElasticLoadBalancingFullAccess"
}

resource "aws_iam_role_policy_attachment" "shield_permissions" {
  role       = var.eks_node_role_name
  policy_arn = "arn:aws:iam::aws:policy/AWSShieldReadOnlyAccess"
}
