# Requirements for an Unreal game to run as PS4 homebrew

Status: engineering plan, not an implemented PS4 Unreal target. Baseline as of 2026-09-23. Select an exact Unreal source revision and game test project before making compatibility claims.

## End-to-end path

Unreal source and game code → UnrealBuildTool PS4 homebrew target → OpenOrbis cross-compiler and C++ runtime → PS4 executable → Unreal shader format and content cooker → staged game assets → PKG → real PS4 homebrew test environment. At runtime, Unreal's platform layer supplies operating-system services; its rendering interface uses a verified GPU backend such as an adapted Vulkan RHI over `vulkan-ps4`, or a new GNM backend if the Vulkan route fails its tests.

The Unreal Launcher binary does not provide this target. Epic's packaging documentation requires a source build for console development, and the custom target proposed here requires independent implementation. The publicly available OpenOrbis source is not an Unreal integration.

## Required components and evidence

| Layer | Work required | Gate demonstrating it works |
| --- | --- | --- |
| Version and access | Pin licensed UE source revision, game revision, PS4 model/firmware and all graphics/toolchain commits. Keep Epic source out of this public repo. | Reproducible version manifest and a small owned Unreal test project. |
| Cross-build and C++ runtime | Verify compiler ABI, linker, C++ standard library, exceptions/RTTI policy, TLS, atomics, thread primitives, allocation and third-party libraries for the selected UE version. | Minimal UE `Core`/game code links and starts, with no unresolved runtime symbols. |
| Unreal target | Implement UnrealBuildTool platform/compiler/SDK registration, target rules, macros and build configurations. | `UnrealBuildTool` builds a minimal program for the new target without hand-editing generated commands. |
| Platform abstraction | Implement startup/exit, memory, threads and synchronization, timers, logging, filesystem and paths, dynamic modules or a static-link alternative, crash reporting, input and audio. | A native platform harness passes each subsystem check on hardware; then a headless UE program reaches its main loop. |
| Graphics backend | Validate `vulkan-ps4` device creation, WSI/presentation, command queues, descriptors, resource barriers, render targets, formats, synchronization and GPU memory. Adapt Unreal's Vulkan RHI only if semantics and performance pass; otherwise scope a dedicated GNM RHI. | Textured 3D scene with depth, offscreen pass, upload/readback and repeatable frames on base PS4. |
| Shader toolchain | Map UE shader formats and permutation inputs to supported SPIR-V, `opengnm-psbc` binaries or another verified path; preserve reflection/resource bindings and cook shader libraries on the host. | A default material and representative material variants render correctly after a fresh cook without runtime fallback stubs. |
| Asset cooking | Register a target platform and texture/audio formats; cook maps, Blueprint content, shaders and package data for this target. | An independently cooked level loads after clearing editor caches. |
| Staging and packaging | Add Unreal AutomationTool build/cook/stage logic, create PS4 executable and PKG with metadata/assets, and support deployment/log collection. | One repeatable command creates an installable PKG; install, boot and asset load work on console. |
| Game services | Integrate controller, audio output, save/load and any actual game requirements such as network or user profiles. | A small playable interaction survives restart and save/load on hardware. |
| Quality and optimization | Profile CPU/GPU frame time, memory, load time, shader stalls and crashes; set budgets for the real scene and base PS4. | Extended play and regression tests meet documented targets on the slowest supported console. |

## Current evidence and gaps

- OpenOrbis builds PS4 homebrew components but does not provide an Unreal target. Its source checkout alone is not the prebuilt SDK.
- OpenGNM documents hardware triangle and shader tests. That validates a narrow graphics path, not Unreal's renderer or its full resource model.
- The inspected `vulkan-ps4` revision `f4d940b7` advertises Vulkan 1.1 and several extensions, but contains explicit unsupported paths. Without `libpsbc`, its shader path can retain raw SPIR-V in a mode that its own source says will not run on the real GPU. Its README's broad API claims and host tests are not a substitute for an on-console conformance/scene test.
- UE's modern rendering features have additional GPU and driver requirements. Do not assume Nanite, Lumen, hardware ray tracing, virtual shadow maps, or a particular frame rate on this stack. Start with a deliberately small rendering profile.
- The existing repository has a source audit and a capabilities probe. It has **not** built Unreal, produced a PS4 Unreal package, or run the probe on a PS4.

## First vertical slice

1. Build the pinned OpenOrbis and OpenGNM stack reproducibly from intended local source, including the real shader compiler. Verify a native 3D example on PS4.
2. Run `probes/vulkan_capabilities.c` on PS4 and record real extensions, formats, limits and firmware. Test a textured cube, depth, render-to-texture, buffer uploads, barriers and presentation through `vulkan-ps4`.
3. Pin one UE source version and audit that version's Vulkan RHI calls/features, build prerequisites and platform services against measured driver behavior. Make a written Vulkan-versus-GNM decision.
4. Implement only the platform, shader and cooking pieces needed to boot a single minimal UE map, then add input and audio. Expand features based on the actual game's needs.

## Source and license boundary

The Unreal EULA controls distribution of Unreal source and engine tools and lists license compatibility restrictions. OpenOrbis's repository is GPL-3.0; OpenGNM components have their own licenses. A review of the particular headers, linked libraries and redistribution model is needed before combining or publishing artifacts. Do not assume that merely invoking a GPL compiler applies GPL terms to a game's output, or that every possible combination is permitted.

## Primary references

- https://dev.epicgames.com/documentation/unreal-engine/packaging-your-project
- https://dev.epicgames.com/documentation/unreal-engine/shader-development-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine
- https://www.unrealengine.com/eula/unreal
- https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain
- https://github.com/PS4-OpenGNM/opengnm-stack
- https://github.com/PS4-OpenGNM/vulkan-ps4
- https://github.com/PS4-OpenGNM/opengnm-psbc
