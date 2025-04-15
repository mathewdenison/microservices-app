#!/bin/bash
set -e

echo "⛳ Initializing Terraform..."
cd terraform
terraform init
terraform apply -auto-approve
cd ..

echo "⚙️ Updating kubeconfig..."
aws eks update-kubeconfig --region us-east-2 --name microservices-cluster-ohio

echo "📦 Creating ServiceAccount if missing..."
kubectl get sa microservice-sqs -n default || kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: microservice-sqs
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: $(aws ssm get-parameter --name "/microservices/iam_role_arn" --with-decryption --query "Parameter.Value" --output text)
EOF

echo "✅ Bootstrap complete!"
