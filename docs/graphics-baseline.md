# Graphics baseline (2026-09-23)

This baseline is a reproducible source and host test checkpoint, not a PS4 GPU measurement or an Unreal port.

## Pinned build input

`graphics.lock.json` pins OpenGNM stack `2de9fc54ca33b39baa0ace59c6b0059e5de94a63`, its four submodules, and the Vulkan and SPIR-V headers. The build candidate is the stack's `vulkan-ps4` submodule at `538732bedd7379c9f709b46da43d9eaea867e0e8`.

The earlier independent audit in `findings.md` used `vulkan-ps4` at `f4d940b723771b3fe637e8ac0704bb5d6ab19622`. It is **not** in the pinned build. The pinned source audit (`audit-stack-vulkan.json`) reports API expression `1,0,0`, one advertised device extension, no duplicate extension entries, and 29 textual unsupported result matches. The independent newer audit reported `1,1,0`, 35 extension entries including a duplicate, and 17 such text matches. These are source signals, not a comparison of working GPU capabilities.

## Verified locally

- `python3 tools/bootstrap_graphics.py --fetch` retrieved all pinned checkouts and `--check` confirmed their exact Git revisions.
- `python3 tools/run_host_graphics_tests.py` built the generic OpenGNM backend and passed all 88 upstream host tests.
- `python3 tools/audit_upstream.py .deps/graphics/opengnm-stack/vulkan-ps4` produced `audit-stack-vulkan.json` (save stdout to that file to reproduce it).

The host tests do not execute the Vulkan PS4 driver, shader compilation on the console, or a GPU workload. They leave `opengnm/config.mak` set to the generic platform and `libopengnm.a` built for the host. Before cross-building, select the Orbis configuration and rebuild that library as directed by the stack's `docs/build-guide.md`.

## Next hardware gate

Build OpenOrbis SDK tools and libraries, install Clang/LLD, CMake, llvm-ar and Python Mako, then build the pinned stack's Orbis OpenGNM, PSBC and Vulkan archives. `make -f probes/Makefile.orbis check` verifies these inputs; `self` requests an ELF and `eboot.bin`. This Makefile has **not** produced a PS4 binary in the current environment. The host lacks a built SDK and several build tools. Packaging an installable PKG and collecting the probe's JSON from a homebrew-capable PS4 remain separate tasks.
