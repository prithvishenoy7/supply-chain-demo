# supply-chain-demo

End-to-end software supply chain security pipeline demonstrating:

- SBOM generation (Syft)
- Vulnerability scanning (Grype)
- Image signing with provenance (Cosign keyless)
- SLSA Build L3 provenance (slsa-github-generator)
- Admission policy enforcement (Kyverno)

## What this demonstrates

This repo shows how to make every artifact produced from source code verifiable: who built it, from what source, with what dependencies, and whether it was tampered with after build.

## Running locally

See `docs/local-setup.md` for kind cluster setup and policy deployment.
