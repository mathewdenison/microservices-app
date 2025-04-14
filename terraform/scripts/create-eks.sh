#!/bin/bash
set -euo pipefail

CLUSTER_NAME="microservices-cluster-ohio"
REGION="us-east-2"
NODEGROUP_NAME="default"
NODE_TYPE="t3.medium"
NODES=2

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Fetch private subnet IDs from Terraform
echo "Fetching private subnet IDs from Terraform..."
PRIVATE_SUBNETS=$(terraform output -json private_subnet_ids | jq -r '.[]' | paste -sd "," -)
echo "Using private subnets: \$PRIVATE_SUBNETS"

# Check if cluster already exists
if eksctl get cluster --region "\$REGION" --name "\$CLUSTER_NAME" &>/dev/null; then
  echo "EKS cluster \$CLUSTER_NAME already exists. Skipping creation."
else
  eksctl create cluster \
    --name "\$CLUSTER_NAME" \
    --region "\$REGION" \
    --nodegroup-name "\$NODEGROUP_NAME" \
    --node-type "\$NODE_TYPE" \
    --nodes "\$NODES" \
    --managed \
    --with-oidc \
    --ssh-access=false \
    --vpc-private-subnets "\$PRIVATE_SUBNETS"
fi

# Create IAM service account for AWS Load Balancer Controller
echo "Creating IAM service account for AWS Load Balancer Controller..."
eksctl create iamserviceaccount \
  --cluster "\$CLUSTER_NAME" \
  --region "\$REGION" \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn arn:aws:iam::\$ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts \
  --approve
