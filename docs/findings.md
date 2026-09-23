# Findings at project start (2026-09-23)

Upstream revisions inspected:

- OpenOrbis-PS4-Toolchain `0a1aaf9dd4a92695538bdeb09fb056d06dd11725`
- opengnm-stack `2de9fc54ca33b39baa0ace59c6b0059e5de94a63`
- `vulkan-ps4` `f4d940b723771b3fe637e8ac0704bb5d6ab19622`

OpenOrbis documents itself as a homebrew toolchain and places final GPU rendering support on its v0.7 roadmap. The separate OpenGNM stack documents hardware smoke tests and a shader compiler triangle test. Those are useful starting evidence, but do not validate an Unreal game.

The inspected `vulkan-ps4` source defines `VK_PS4_API_VERSION` as `VK_MAKE_VERSION(1, 1, 0)` even though its README calls it a Vulkan 1.0 ICD. It also has explicitly unsupported paths and conditional shader stub mode when `libpsbc` is missing. Device extensions must be inspected together with corresponding reported features and working entry points. The audit tool records these issues without guessing which guarded paths an Unreal build reaches.

The source audit at this revision counted 35 advertised device extension entries, including a duplicate `VK_KHR_CREATE_RENDERPASS_2_EXTENSION_NAME`, and 17 textual matches for unsupported feature/format results. These counts are signals for review rather than a compatibility verdict. See `docs/audit-2026-09-23.json`.

The capability probe compiles on a Linux host with Vulkan headers and a loader. This workspace's host returned `VK_ERROR_INCOMPATIBLE_DRIVER` from `vkCreateInstance`, so there is no host runtime measurement, and no PS4 measurement has yet been performed.

UE's current Linux requirements mention a modern Vulkan driver; high-end rendering features have additional feature requirements. A PS4 homebrew Vulkan driver cannot be assumed to meet the same requirements. The specific Unreal version and target rendering profile remain unselected.

## Primary references

- https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain
- https://github.com/PS4-OpenGNM/opengnm-stack
- https://github.com/PS4-OpenGNM/vulkan-ps4
- https://github.com/PS4-OpenGNM/opengnm-psbc
- https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine
- https://www.unrealengine.com/eula/unreal
