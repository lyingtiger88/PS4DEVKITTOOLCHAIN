# Graphics Validation Matrix

This matrix defines the minimum evidence required before selecting Vulkan-over-GNM as the renderer path for an eventual engine target.

## Evidence classes

| Class | Meaning |
|---|---|
| SOURCE | Static source inspection only |
| HOST | Host execution without PS4 hardware |
| CROSS | PS4-target compilation/linking |
| PS4 | Execution and measurement on real PS4 hardware |
| INTEGRATED | Result accepted into the project's pinned baseline |

## Test levels

| ID | Test | Expected evidence | Why it matters |
|---|---|---|---|
| GFX-01 | Vulkan instance creation | CROSS + PS4 | Loader/ICD boot |
| GFX-02 | Physical-device enumeration | PS4 | Real capability surface |
| GFX-03 | RGBA8 image allocation | PS4 | Baseline render target |
| GFX-04 | Depth buffer allocation | PS4 | Depth testing |
| GFX-05 | Vertex/index upload | PS4 | Resource transfer path |
| GFX-06 | Basic VS+PS draw | PS4 | End-to-end graphics |
| GFX-07 | Depth-tested cube | PS4 | State and depth correctness |
| GFX-08 | Render-to-texture | PS4 | Offscreen rendering |
| GFX-09 | Texture sampling | PS4 | Descriptor/resource path |
| GFX-10 | BC texture formats | PS4 | Common game texture path |
| GFX-11 | Uniform/storage buffers | PS4 | Engine constant/data path |
| GFX-12 | Pipeline barriers | PS4 | Synchronisation correctness |
| GFX-13 | Multiple render targets | PS4 | Deferred/advanced paths |
| GFX-14 | Compute dispatch | PS4 | Non-graphics workloads |
| GFX-15 | Readback/upload round trip | PS4 | CPU/GPU synchronization |
| GFX-16 | Presentation / VideoOut | PS4 | Visible frame delivery |
| GFX-17 | Shader compile matrix | CROSS + PS4 | Shader toolchain coverage |
| GFX-18 | Device-loss/error paths | PS4 | Stability and recovery |

## Capability probe

The existing `probes/vulkan_capabilities.c` should be treated as the authoritative probe format for this project. It must be cross-built and run on the target before its output is used as a hardware capability claim.

## Acceptance rule

A renderer path is not considered engine-ready because a triangle renders. The minimum vertical slice is:

**device → resources → shader → pipeline → draw → depth → texture → synchronization → presentation**

Any failed item must record the firmware, build revision, test binary, and failure output.
