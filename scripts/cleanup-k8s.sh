#!/bin/bash
set -e

echo "🔥 Cleaning up stuck frontend ingress..."
kubectl patch ingress frontend -n default -p '{"metadata":{"finalizers":[]}}' --type=merge || true
kubectl delete ingress frontend -n default --ignore-not-found=true
helm uninstall frontend -n default || true
