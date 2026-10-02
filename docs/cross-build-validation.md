# Cross-build and shadPS4 validation

This gate verifies that a pinned OpenOrbis release can produce a PS4-targeted homebrew executable from the toolchain's own Linux sample.

## Evidence boundary

- **SOURCE:** OpenOrbis v0.5.4 release metadata and its documented `samples/hello_world` build flow.
- **CROSS:** GitHub Actions downloads the pinned release, verifies its SHA-256, builds the sample, and produces `eboot.bin` plus the intermediate ELF.
- **EMULATOR:** shadPS4 is the execution target available to this project. A local shadPS4 run can provide runtime evidence without requiring physical PS4 hardware.
- **PS4-HARDWARE:** unavailable in this project and therefore never claimed.
- **GRAPHICS:** the hello_world sample is not a GPU validation. Graphics validation begins with an OpenGNM/Vulkan sample.

The project deliberately separates **CROSS** from **EMULATOR** evidence. A binary that cross-builds is not automatically proven runnable by shadPS4, and a binary that runs in shadPS4 is not automatically proven on physical PS4 hardware.

## shadPS4 execution path

Current shadPS4 documentation states that the emulator can boot a PS4 ELF directly, which is useful for development smoke tests.

For a locally built artifact, the basic test is:

`shadPS4 /path/to/hello_world.elf`

or, when testing the packaged application layout:

`shadPS4 /path/to/eboot.bin`

Record:

1. shadPS4 version/commit.
2. Host OS and CPU/GPU.
3. Exact artifact SHA-256.
4. Whether the process starts.
5. Whether the program reaches its expected runtime state.
6. shadPS4 console log.
7. Screenshot/video when graphical output exists.
8. Any missing firmware module or unsupported syscall/library message.

Do not label this result as **PS4 hardware validation**.

## Why this comes before OpenGNM/Vulkan

A reproducible cross-build removes the first major unknown. The next useful step is a graphics sample that exercises the actual PS4 graphics path, followed by execution in shadPS4.

## Next gates

1. Cross-build a minimal OpenGNM-linked graphics sample.
2. Cross-build the shader compiler/runtime components needed by the Vulkan ICD.
3. Produce a graphics sample package.
4. Boot the resulting ELF/eboot.bin in shadPS4 and capture logs/results.
5. Expand the graphics matrix: framebuffer, depth, texture sampling, render-to-texture, synchronization, presentation, and shader coverage.
6. Keep physical-PS4 execution as a future optional validation tier, not a project prerequisite.
