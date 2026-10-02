# Cross-build validation

This gate verifies that a pinned OpenOrbis release can produce a PS4-targeted homebrew executable from the toolchain's own Linux sample.

## Evidence boundary

- **SOURCE:** OpenOrbis v0.5.4 release metadata and its documented `samples/hello_world` build flow.
- **CROSS:** GitHub Actions successfully downloads the pinned release, verifies its SHA-256, invokes the Linux sample Makefile, and produces `eboot.bin` plus the intermediate ELF.
- **PS4:** not established by this gate. The generated binary must still be installed and executed on an actual PS4 before runtime claims are made.
- **GRAPHICS:** not established by this gate. `hello_world` is a CPU/runtime smoke test, not a GPU test.

The v0.5.4 release currently exposes `toolchain-llvm-18.tar.gz`; the workflow pins both the version and its published SHA-256 rather than silently consuming a moving `latest` asset.

## Why this comes before OpenGNM/Vulkan

A working cross-build removes one major unknown: whether the repository can produce a PS4-targeted executable with the OpenOrbis toolchain in a reproducible CI environment. Only after that should we spend time cross-building OpenGNM, PSBC, and vulkan-ps4.

## Next gates

1. Cross-build a minimal OpenGNM-linked graphics sample.
2. Cross-build the shader compiler/runtime components needed by the Vulkan ICD.
3. Produce a graphics sample package.
4. Install and execute it on the target PS4.
5. Capture firmware version, process exit state, console logs, and graphics test results.
