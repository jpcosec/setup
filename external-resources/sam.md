---
# Human-readable name of the resource
name: SAM - Sovereign Agent Mesh
# Official docs or repository URL
page: https://github.com/google/sam/
# true | false — whether the resource is installed locally
installed: false
# Local install path or install command; set when installed is true
install_path: null
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:sam
- layer:runtime
- topic:agent-networking
---

# SAM - Sovereign Agent Mesh

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Zero-config, zero-trust P2P network for autonomous AI agents (Apache-2.0, not an officially supported Google product). Lightweight sam-node clients self-discover over libp2p; sam-router relays the data plane; sam-control-plane holds identity registry, policies and grants. Ed25519 root key custody, OIDC via your own IdP, cryptographically attested label gates (e.g. jurisdiction: eu), local node veto policies; MCP sidecar routing and an A2A bridge.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed. Quick start is one-liner install + adding the sam-mesh skill so an agent discovers and calls tools across the mesh; public testnets (bananas/hub.sam-mesh.dev) are no-SLA testbeds; real deployment via the sam-mesh Helm chart on your own Kubernetes.

## Status

_How it is currently working; keep empty when not installed._



## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._
