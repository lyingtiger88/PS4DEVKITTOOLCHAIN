# PS4DEVKITTOOLCHAIN — executable roadmap v2
Date: 2026-10-02

This roadmap separates reproducible research from upstream adoption. No Unreal compatibility claim is made until the required hardware gates pass.

## Track A — Reproducible baseline
### A0 Source and license gate
- Keep exact upstream commits in lock files.
- Record licenses and redistribution boundaries.
- Keep any licensed Unreal source outside this public repository.
Pass: clean reproducible checkout and documented source boundary.

### A1 Toolchain gate
- Build OpenOrbis from the selected release/source revision.
- Verify clang, lld, llvm-ar, CMake, Make, Python and Mako.
- Produce a machine-readable toolchain manifest.
Pass: a clean machine can reproduce the cross compiler and linker inputs.

### A2 Graphics stack gate
- Build opengnm for generic and Orbis.
- Build opengnm-psbc host and Orbis libraries.
- Build vulkan-ps4.
- Build at least triangle/cube examples.
Pass: all intended artifacts exist and link without manual source edits.

### A3 Hardware probe gate
Run probes/vulkan_capabilities.c on real PS4 hardware and save model, firmware, API version, limits, features, memory heaps, extensions and format capabilities.
Pass: stable enumeration and JSON output on supported test hardware.

### A4 Graphics correctness gate
Test triangle, textured cube, vertex/index buffers, uniform/storage resources, depth, render target, texture upload/readback, mipmaps, blending, MSAA if exposed, synchronization, asynchronous upload, presentation, shader variants and compute dispatch.
Pass: repeatable visual/CRC checks, no GPU hangs, and documented unsupported cases.

## Track B — Upstream convergence
### B0 Revision comparison
Compare the locked stack against current upstream component revisions: API coverage, build requirements, shader compiler changes, Vulkan extensions, unsupported paths, hardware validation evidence and ABI/layout changes.
Pass: migration report exists before changing graphics.lock.json.
### B1 Upgrade candidate
Create a separate lockfile candidate. Never silently replace the proven baseline.
Pass: host tests and source audit pass on the candidate.
### B2 Hardware revalidation
Repeat the capability and graphics matrices against the candidate.
Pass: no regression in the previous graphics matrix.
### B3 Adopt or reject
Promote the candidate only if it improves required functionality without breaking the baseline.

## Track C — Runtime services
Build native tests for controller, audio, filesystem, save data, threads, atomics, TLS, timers, memory, module loading, logging and crash reporting. Add networking only if the target game needs it.
Pass: each required service works on hardware and has a deterministic smoke test.

## Track D — Unreal feasibility
### D0 Select exact Unreal source
Choose one licensed source revision and one small owned sample project. Record UE commit, compiler, host OS, PS4 model/firmware, graphics stack revision and shader compiler revision.
### D1 RHI audit
Build a requirement matrix: UE operation -> Vulkan call/extension -> PS4 driver support -> test result -> workaround. Do not start with a generic UE5 feature list.
### D2 Platform layer
Implement only the surface required to boot: platform macros, target rules, compiler/linker rules, paths/files, memory, threads, timing, logging, input and audio.
Pass: minimal UE program reaches the main loop.
### D3 Shader/cook path
Map UE shader permutation -> SPIR-V -> PS4 shader binary -> reflection/resource bindings.
Pass: default material plus representative variants survive a clean cook and render correctly.
### D4 Minimal renderer
Start with one view, opaque material, depth, basic lighting, static mesh, texture and UI/debug text. Explicitly exclude unverified advanced features.
Pass: packaged minimal UE scene renders repeatedly on hardware.
### D5 Packaging
Automate source/build -> cook -> stage -> executable -> PKG -> deploy -> logs.
Pass: one command reproduces an installable package.

## Track E — Game vertical slice
Use one small owned test game. Required: boot, menu, input, one level, character/controller, static meshes, textures/materials, audio, save/load, pause and clean shutdown.
Pass: playable loop survives restart and repeated runs.

## Track F — Performance and stability
Measure base PS4 and PS4 Pro where applicable: CPU/GPU frame time, memory, peak allocations, shader compile time, load time, draw/dispatch count, command-buffer pressure, stalls, crashes and long-session stability.
Pass: extended test run meets documented budgets.

## Track G — Feature expansion
Only after Track F: more materials, skeletal animation, particles, post processing, streaming, larger scenes, asynchronous loading and networking if required.
Each feature gets its own hardware test before integration.

## Track H — Advanced renderer decision
If Vulkan semantics and performance are sufficient, continue Vulkan RHI adaptation. If gaps are localized, add compatibility layers. If fundamental Vulkan/RHI assumptions fail, estimate a dedicated GNM RHI. This is a measured engineering decision.

## Definition of done
1. Exact UE source and dependencies pinned.
2. Native toolchain reproducible.
3. Platform layer boots.
4. Shader cooking works.
5. Renderer passes graphics matrix.
6. Asset cooking works from clean state.
7. Packaging automated.
8. Real game scene playable.
9. Base hardware meets documented budgets.
10. Extended play stable.

## Immediate execution order
1. Reproduce toolchain.
2. Build pinned stack.
3. Cross-build and package capability probe.
4. Run on PS4.
5. Execute graphics matrix.
6. Compare current upstream and create upgrade candidate.
7. Re-run hardware matrix.
8. Build runtime-service harness.
9. Select UE source revision.
10. Audit Vulkan RHI.
11. Implement minimal platform target.
12. Implement shader/cook bridge.
13. Boot minimal UE scene.
14. Package/deploy automatically.
15. Add game vertical slice.
16. Profile and optimize.
17. Expand features one gate at a time.