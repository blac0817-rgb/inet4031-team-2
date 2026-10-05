#!/usr/bin/env bash
set -euo pipefail

CLUSTER=myapp

# Create the cluster only if it doesn't already exist
if ! k3d cluster list "$CLUSTER" >/dev/null 2>&1; then
  k3d cluster create "$CLUSTER" --agents 2 \
    --port "8092:80@loadbalancer" \
    --k3s-arg "--disable=traefik@server:0" \
    --subnet 100.97.2.0/24
fi

# Write a kubeconfig for whoever runs this script
k3d kubeconfig merge "$CLUSTER" --kubeconfig-switch-context

kubectl get nodes
