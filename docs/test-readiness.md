# Test readiness

This repository is now at the first executable validation stage.

## Host test

The CI workflow builds `probes/vulkan_capabilities.c` against the Linux Vulkan loader, executes it, and stores the JSON result as a workflow artifact.

A successful host run proves only that the probe can execute against the CI host Vulkan implementation. It does **not** prove OpenOrbis, vulkan-ps4, or PS4 compatibility.

## PS4 test

The PS4 gate starts only after a cross-built probe is produced with the pinned OpenOrbis toolchain. The same probe should then be run on real hardware and its JSON captured as evidence.

Required evidence:

1. exact Git revisions of the toolchain and graphics stack;
2. PS4 firmware version;
3. probe stdout JSON;
4. exit status;
5. test matrix results for device creation, resources, shaders, pipeline/draw, synchronization, and presentation.

The current repository does not contain a PS4 hardware result, so the PS4 gate remains **NOT TESTED**.

## Acceptance rule

Do not mark a graphics capability as validated from source inspection or a host run. A PS4 result requires execution on the target hardware.
