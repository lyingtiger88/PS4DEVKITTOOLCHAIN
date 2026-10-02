# GPT-5.6 Luna Research Lane

This branch is an isolated research lane for the PS4DEVKITTOOLCHAIN project.

## Isolation rule

- Do not merge this branch automatically.
- Do not modify another agent's branch.
- Treat `main` as the integration baseline.
- Before every new work block, inspect open PRs and branch heads for possible overlap.
- Hardware-gated claims must remain explicitly marked until a real PS4 run produces evidence.

## Scope for this lane

1. Reproducibility and provenance.
2. Graphics capability and correctness test design.
3. Upstream OpenGNM/OpenOrbis convergence analysis.
4. Unreal feasibility gates, without assuming a specific Unreal source revision.
5. Host-side validation that can be automated without PS4 hardware.

## Current external evidence

As of 2026-10-02, upstream OpenGNM documents 207+ GNM functions, an OpenOrbis-compatible build, generic host testing, and an Orbis backend. The upstream umbrella stack documents Vulkan 1.0 over OpenGNM and a PS4 shader compiler based on Mesa/NIR/ACO. These are upstream claims and are not treated as validation of this repository's pinned baseline until reproduced locally and, where required, on PS4 hardware.

## Evidence policy

Every gate should distinguish:

- **SOURCE**: inferred from source inspection.
- **HOST**: reproduced on a development machine.
- **CROSS**: reproduced with the OpenOrbis target toolchain.
- **PS4**: observed on actual PS4 hardware.
- **INTEGRATED**: accepted into the project's chosen baseline.

No lower evidence class is silently promoted to a higher one.
