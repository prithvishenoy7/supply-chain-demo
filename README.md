# supply-chain-demo

End-to-end software supply chain security pipeline. Every artifact produced from this repo is verifiable: what it contains (SBOM), whether it has known vulnerabilities (Grype), who built it and from what source (Cosign keyless + SLSA provenance), and whether it can run in a cluster without a valid signature (Kyverno).

## Pipeline

| Stage | Tool | What it produces |
|---|---|---|
| SBOM generation | Syft | `sbom.spdx.json` — full dependency inventory |
| Vulnerability scan | Grype | CVE report against SBOM; blocks on Critical |
| Image signing | Cosign (keyless) | Signature in Sigstore transparency log |
| Provenance | slsa-github-generator | SLSA Build L3 attestation |
| Admission control | Kyverno | Unsigned images rejected at cluster entry |

## Verify an image yourself

Get the digest from a recent [pipeline run](https://github.com/prithvishenoy7/supply-chain-demo/actions/workflows/supply-chain.yml), then:

```bash
# Verify Cosign signature
cosign verify \
  --certificate-identity="https://github.com/prithvishenoy7/supply-chain-demo/.github/workflows/supply-chain.yml@refs/heads/main" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/prithvishenoy7/supply-chain-demo@<digest>

# Verify SLSA provenance attestation
cosign verify-attestation \
  --type slsaprovenance \
  --certificate-identity-regexp="https://github.com/slsa-framework/slsa-github-generator" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  ghcr.io/prithvishenoy7/supply-chain-demo@<digest>
```

Both commands produce JSON output confirming the artifact's identity, build source, and provenance chain.

## Local policy enforcement

See [docs/local-setup.md](docs/local-setup.md) for step-by-step instructions to run a local kind cluster with Kyverno enforcing the signed-image admission policy.

## Why this exists

Built as a portfolio artifact while transitioning from automotive product cybersecurity (ISO 21434, UN R156 SBOM) into cloud-native supply chain security engineering. The pipeline applies the same artifact integrity principles I used in regulated automotive contexts — where a compromised firmware update carries physical risk — to a standard cloud-native delivery workflow.
