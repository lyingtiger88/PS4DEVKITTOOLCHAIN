# PS4 Unreal OpenOrbis feasibility lab

This repository is the first engineering stage toward running a licensed Unreal game as PS4 homebrew. It is **not** an Unreal platform target, a playable port, or a PlayStation Store publishing path.

The OpenOrbis source is pinned as a Git submodule at `OpenOrbis-PS4-Toolchain/`; its exact revision is recorded in [`docs/dependencies.md`](docs/dependencies.md). GitHub displays a submodule as a link to the upstream commit. To obtain all its source files locally, clone with `--recurse-submodules`.

The current repository is an integration and feasibility workspace. See [`docs/build-layout.md`](docs/build-layout.md) for the distinction between preserving OpenOrbis's internal paths and creating a reproducible build of a modified toolchain.

```sh
git clone --recurse-submodules https://github.com/lyingtiger88/PS4DEVKITTOOLCHAIN.git
```

## Why start here?

OpenOrbis builds PS4 homebrew. The separate OpenGNM stack supplies a GNM library, a shader compiler, and a Vulkan translation layer. The pinned stack's `vulkan-ps4` source reports Vulkan 1.0 and contains unsupported or stub paths; a newer driver revision audited independently reports Vulkan 1.1. These are different revisions. API names and a triangle demonstration do not establish compatibility with Unreal's renderer. We will measure the actual capabilities before choosing whether to adapt Unreal's Vulkan RHI or write a PS4 RHI.

## What is in this repository?

- `tools/audit_upstream.py`: repeatable source snapshot of advertised API version, device extensions, duplicate extension declarations, and explicit unsupported paths. This is a source audit, **not** a hardware test.
- `probes/vulkan_capabilities.c`: a Vulkan program that prints the device's advertised version, extensions, selected features, limits, memory heaps, and texture/depth format support as JSON. Its output must be collected from PS4 hardware to evaluate the PS4 driver. Running it on a PC only validates the probe.
- `docs/roadmap.md`: evidence gates and staged Unreal integration plan.
- `docs/unreal-ps4-execution-requirements.md`: component inventory from Unreal build and shader cooking through packaging and hardware tests.
- `docs/findings.md`: findings tied to upstream commit IDs, with unresolved claims identified.
- `graphics.lock.json` and `tools/bootstrap_graphics.py`: pinned, repeatable checkout of OpenGNM and its header dependencies.
- `probes/Makefile.orbis`: preliminary cross-build path for a PS4 probe ELF and `eboot.bin`, pending a built SDK and hardware verification.
- `docs/graphics-baseline.md`: exact graphics revisions, host test evidence, and current cross-build blockers.

## Reproduce the source audit

```sh
git clone https://github.com/PS4-OpenGNM/vulkan-ps4.git third_party/vulkan-ps4
python3 tools/audit_upstream.py third_party/vulkan-ps4 > audit.json
```

The graphics driver checkout is deliberately excluded from this repository. Record its exact commit alongside every audit. The committed `docs/audit-stack-vulkan.json` captures the **pinned stack** driver; `docs/audit-2026-09-23.json` captures the separately audited newer driver.

## Fetch the pinned graphics sources

```sh
python3 tools/bootstrap_graphics.py --fetch
python3 tools/bootstrap_graphics.py --preflight
python3 tools/run_host_graphics_tests.py
```

The checkout is stored in `.deps/graphics/opengnm-stack/` and excluded from Git. Its submodules and Vulkan/SPIR-V headers use the exact revisions in `graphics.lock.json`. Fetching source does not install an OpenOrbis SDK or run a PS4 build. The preflight report shows missing build tools and SDK artifacts on the current machine.

The host test command builds the generic OpenGNM backend and runs its upstream tests. It does not exercise the PS4 GPU. Its test linker places the math library after the static OpenGNM archive, working around the upstream Makefile's host link ordering without changing vendor code.

Host tests leave OpenGNM configured and built for the generic backend. Before a PS4 probe build, select `config.orbis.mak` and rebuild `libopengnm.a` for Orbis using the pinned stack's build guide. `make -f probes/Makefile.orbis check` checks the Orbis configuration and archive member.

After building OpenGNM, `opengnm-psbc`, and `vulkan-ps4` for Orbis following their pinned upstream instructions and installing a built OpenOrbis SDK, the cross-build path for the capability probe is:

```sh
export OO_PS4_TOOLCHAIN=/path/to/built/OpenOrbis-PS4-Toolchain
make -f probes/Makefile.orbis check
make -f probes/Makefile.orbis self
```

This produces an ELF and `eboot.bin` in `build/orbis-probe/`; an installable PKG and a successful PS4 runtime test are still separate milestones.

## Build the probe on a PC

Requires CMake, a C compiler, Vulkan headers, and the Vulkan loader. For example:

```sh
cmake -S . -B build -DVULKAN_HEADERS_DIR=/path/to/Vulkan-Headers/include
cmake --build build
./build/vulkan_capabilities > host-capabilities.json
```

If CMake is unavailable, a direct compiler invocation also works on a Linux host with the shared Vulkan loader installed:

```sh
cc -std=c11 -Wall -Wextra -Werror -I /path/to/Vulkan-Headers/include \
  probes/vulkan_capabilities.c -lvulkan -o vulkan_capabilities
```

A host must also have a usable Vulkan ICD to run it; a loader alone is insufficient.

**PC output is not PS4 evidence.** To run on PS4, compile `probes/vulkan_capabilities.c` with OpenOrbis and link against the matching `vulkan-ps4`, OpenGNM, and shader compiler build as documented by those projects. The PS4 toolchain, a homebrew-capable test console, and a real GPU run are needed. Cross-compiling alone is insufficient.

## Repository boundaries

Do not commit Unreal Engine source, Sony SDK files, firmware dumps, keys, or proprietary game assets here. Engine patches, if developed, should live in a separately access-controlled Epic-authorized fork. This repository can contain original interface code, measurement tools, and instructions. Review Epic's current license before sharing any integration code derived from the engine.

This work targets homebrew testing. Official PS4 distribution requires the platform holder's publishing process.
