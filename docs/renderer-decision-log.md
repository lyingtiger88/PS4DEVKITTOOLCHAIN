# Renderer Decision Log

## Decision 2026-10-02

**Status:** Open. No renderer has been selected for an engine integration.

### Candidate A: Vulkan over OpenGNM

Advantages to investigate:

- Higher-level API surface suitable for an engine RHI.
- Existing Vulkan ICD project in the OpenGNM ecosystem.
- Potentially smaller initial engine adaptation surface than a direct GNM implementation.

Risks:

- Vulkan feature/semantic coverage must be measured against the engine's actual RHI requirements.
- Shader, synchronization, descriptor, render-pass, memory and presentation behavior must be validated on PS4.
- Host compilation is not evidence of PS4 runtime compatibility.

### Candidate B: Dedicated GNM RHI

Advantages to investigate:

- Direct access to the platform's GNM-oriented abstraction.
- Avoids depending on Vulkan semantic translation where it is a poor fit.

Risks:

- Larger engine integration surface.
- More platform-specific renderer code.
- Requires explicit implementation and validation of engine-facing resource/state abstractions.

## Decision gate

Do not choose between A and B from source inspection alone.

The decision should be based on:

1. Unreal RHI feature inventory for the exact source revision being targeted.
2. Vulkan capability/correctness matrix results.
3. Shader compiler coverage.
4. Synchronization and presentation behavior.
5. Performance measurements on target hardware.
6. Amount of platform-specific code required for a minimal engine vertical slice.

## Explicit non-claims

This project does not currently claim:

- Unreal Engine running on PS4.
- Nanite support.
- Lumen support.
- Full Vulkan 1.x feature parity.
- Commercial game compatibility.
- Performance parity with Sony's official SDK.

Those are separate gates and require evidence.
