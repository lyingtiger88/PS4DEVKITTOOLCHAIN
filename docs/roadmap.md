# Development gates

The target is an optimized, usable Unreal game build on PS4 homebrew hardware. The stages below are **gates**, not claims of implementation. Pin the exact Unreal and upstream commits before engine integration.

The detailed component inventory and first vertical slice are in [`unreal-ps4-execution-requirements.md`](unreal-ps4-execution-requirements.md).

| Gate | Deliverable | Pass condition |
| --- | --- | --- |
| 0. Source and licensing | Source audit, dependency revisions, code sharing policy | Reproducible audit; no restricted source or SDK in this public repo |
| 1. Hardware capabilities | `vulkan_capabilities` PS4 JSON plus console model and firmware | Real hardware output, stable device enumeration, truthful extensions/features |
| 2. Graphics correctness | Textured cube, depth, render target, shader variants, asynchronous upload, frame capture | Repeatable visual checks on base PS4 and Pro; no GPU hangs |
| 3. Runtime | Controller, audio, filesystem, threading, memory, clocks, save data | Minimal native homebrew app exercises each service on console |
| 4. Unreal feasibility | A specific licensed UE source version and an unmodified sample game's dependency graph | Engine build requirements documented against actual graphics and runtime capabilities |
| 5. Engine prototype | Build toolchain, platform abstraction, shader pipeline, rendering bridge | A packaged minimal UE scene renders and receives input on PS4 |
| 6. Game quality | Representative game scene, profiling, regression suite | Defined frame time and memory budgets pass on base PS4, with stable extended play |

## Architecture choice after Gate 2

Test an adaptation of Unreal's existing Vulkan RHI first, because `vulkan-ps4` already presents a Vulkan interface. Treat this as a hypothesis. If its semantics, supported extensions, or performance do not meet the selected Unreal version, estimate a dedicated GNM RHI against the measured gaps. Do not create an empty RHI module merely to label the project a port.

For the first Unreal scene, disable features requiring unsupported capabilities. The rendering feature set and its performance budget depend on the measured hardware and a selected engine version. No Nanite, Lumen, or general UE5 compatibility claim is made here.

## Next executable work

1. Run `tools/audit_upstream.py` for pinned upstream revisions and attach the resulting report to a development issue.
2. Cross-compile the Vulkan probe against the exact OpenGNM stack and run it on actual PS4 hardware. A host run validates only the probe.
3. Add a GPU test app for texture upload, depth attachment, offscreen pass, and readback, recording expected images and failure modes.
4. Select the Unreal version and a small, owned test project; compare its actual required Vulkan calls and runtime services to the results.
