# Local Setup

Demonstrates the full supply chain security pipeline locally: build the image, run it through the pipeline, and verify that the Kyverno admission policy rejects unsigned images and admits signed ones.

## Prerequisites

- Docker Desktop (running)
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation): `brew install kind`
- [kubectl](https://kubernetes.io/docs/tasks/tools/): `brew install kubectl`
- [cosign](https://docs.sigstore.dev/cosign/system_config/installation/): `brew install cosign`
- [kyverno CLI](https://kyverno.io/docs/kyverno-cli/) (optional, for local policy testing): `brew install kyverno`

## 1. Create a local cluster

```bash
kind create cluster --name supply-chain-demo
kubectl cluster-info --context kind-supply-chain-demo
```

## 2. Install Kyverno

```bash
kubectl create -f https://github.com/kyverno/kyverno/releases/download/v1.13.4/install.yaml
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=kyverno \
  -n kyverno \
  --timeout=120s
```

## 3. Apply the admission policy

```bash
kubectl apply -f policy/require-signed-images.yaml
kubectl get clusterpolicy require-signed-images
```

Expected: policy in `Ready` state.

## 4. Verify the policy blocks unsigned images

```bash
kubectl run unsigned-test \
  --image=nginx:latest \
  --restart=Never
```

Expected: admission denied — error references `require-signed-images` Kyverno policy.

## 5. Verify the policy admits the signed image

Get the latest digest from a recent pipeline run:

```bash
# Note: cosign triangulate was removed in cosign v2.
# The digest is best obtained from the GitHub Actions run output.
# Alternatively, inspect the run logs or use:
# cosign describe <image>@<sha>
```

Then run the signed image:

```bash
kubectl run signed-test \
  --image=ghcr.io/prithvishenoy7/supply-chain-demo@<digest> \
  --restart=Never
```

Expected: pod created successfully.

## 6. Verify the image signature independently

```bash
cosign verify \
  --certificate-identity="https://github.com/prithvishenoy7/supply-chain-demo/.github/workflows/supply-chain.yml@refs/heads/main" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/prithvishenoy7/supply-chain-demo@<digest>
```

Expected: JSON output confirming the signature and GitHub Actions identity.

## 7. Tear down

```bash
kind delete cluster --name supply-chain-demo
```
