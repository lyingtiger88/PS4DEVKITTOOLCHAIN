# PS4 Unreal OpenOrbis feasibility lab

This repository is the first engineering stage toward running a licensed Unreal game as PS4 homebrew. It is **not** an Unreal platform target, a playable port, or a PlayStation Store publishing path.

The OpenOrbis source is pinned as a Git submodule at `OpenOrbis-PS4-Toolchain/`; its exact revision is recorded in [`docs/dependencies.md`](docs/dependencies.md). GitHub displays a submodule as a link to the upstream commit. To obtain all its source files locally, clone with `--recurse-submodules`.

The current repository is an integration and feasibility workspace. See [`docs/build-layout.md`](docs/build-layout.md) for the distinction between preserving OpenOrbis's internal paths and creating a reproducible build of a modified toolchain.

```sh
git clone --recurse-submodules https://github.com/lyingtiger88/PS4DEVKITTOOLCHAIN.git
```

## Why start here?

OpenOrbis builds PS4 homebrew. The separate OpenGNM stack supplies a GNM library, a shader compiler, and a Vulkan translation layer. The upstream `vulkan-ps4` README describes a Vulkan 1.0 implementation, while its current source reports Vulkan 1.1 and contains unsupported or stub paths. API names and a triangle demonstration do not establish compatibility with Unreal's renderer. We will measure the actual capabilities before choosing whether to adapt Unreal's Vulkan RHI or write a PS4 RHI.

## What is in this repository?

- `tools/audit_upstream.py`: repeatable source snapshot of advertised API version, device extensions, duplicate extension declarations, and explicit unsupported paths. This is a source audit, **not** a hardware test.
- `probes/vulkan_capabilities.c`: a Vulkan program that prints the device's advertised version, extensions, selected features, limits, memory heaps, and texture/depth format support as JSON. Its output must be collected from PS4 hardware to evaluate the PS4 driver. Running it on a PC only validates the probe.
- `docs/roadmap.md`: evidence gates and staged Unreal integration plan.
- `docs/findings.md`: findings tied to upstream commit IDs, with unresolved claims identified.

## Reproduce the source audit

```sh
git clone https://github.com/PS4-OpenGNM/vulkan-ps4.git third_party/vulkan-ps4
python3 tools/audit_upstream.py third_party/vulkan-ps4 > audit.json
```

The graphics driver checkout is deliberately excluded from this repository. Record its exact commit alongside every audit.

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
