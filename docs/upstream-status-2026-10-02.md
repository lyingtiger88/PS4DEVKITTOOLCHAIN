# Upstream status checkpoint — 2026-10-02

This document records current upstream information discovered during research. It is intentionally separate from the pinned build inputs in `graphics.lock.json`.

## OpenOrbis

The upstream OpenOrbis repository currently describes itself as a PS4 homebrew toolchain containing headers, library stubs, and build tools. Its README still identifies debugger/VS integration and final GPU rendering support as roadmap work, rather than presenting OpenOrbis itself as an Unreal Engine platform target.

The practical consequence for this project is unchanged: OpenOrbis is the cross-build foundation, not the Unreal port.

## OpenGNM

Current upstream OpenGNM material describes a broader graphics stack than the revision pinned by this repository. The current project advertises a `sceGnm*` / `sceGpa*` compatibility layer, an Orbis backend, a generic host backend, PM4 packet generation, surface/AddrLib calculations, shader compilation support, and examples.

These current claims must not be retroactively applied to the pinned revision. The feasibility project should continue to treat its locked revisions as the reproducible experimental baseline and upgrade them only through a deliberate lockfile change followed by a fresh audit and host/console test cycle.

## Research implication

The next engineering decision is not yet "Vulkan versus GNM" in the abstract. It is:

1. reproduce the locked stack;
2. cross-build the capability probe;
3. collect real PS4 device properties and extension/feature results;
4. run a graphics correctness suite;
5. measure the Unreal version's actual Vulkan/RHI requirements;
6. only then choose between adapting Vulkan RHI and implementing a dedicated GNM path.

A newer upstream revision may reduce implementation work, but it does not remove the need for PS4 hardware evidence.

## Current blocker

The repository itself records that no PS4 binary has yet been produced by the preliminary probe path and that the host environment used for the baseline did not contain a built OpenOrbis SDK and all required cross-build inputs.

The next concrete milestone is therefore a reproducible Orbis toolchain build, followed by the capability probe on real hardware.

## Sources

- OpenOrbis PS4 Toolchain README: https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain
- OpenGNM current repository: https://github.com/PS4-OpenGNM/opengnm
- OpenGNM stack documentation: https://github.com/PS4-OpenGNM/opengnm-stack
