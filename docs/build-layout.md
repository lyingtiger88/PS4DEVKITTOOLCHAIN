# Source layout and toolchain build

## Which layout must remain stable?

OpenOrbis's internal `include/`, `lib/`, `src/`, `bin/`, `scripts/`, `samples/`, and `link.x` paths matter because its examples and build tooling refer to them. The pinned submodule retains that complete internal tree. The parent repository may contain additional tooling around it without changing those paths.

The parent repository is **not yet a fork of the OpenOrbis toolchain**. Edits to OpenOrbis source in a submodule belong to that submodule's repository and cannot be developed as ordinary edits to the parent. For a maintained, modified core toolchain, create an owned fork/mirror of OpenOrbis with its source tree intact, then point the submodule at that fork or make the fork the main toolchain repository. Keep the feasibility code separate from core files.

## A source checkout is not a built SDK

At upstream commit `0a1aaf9dd4a92695538bdeb09fb056d06dd11725`, `build/build.sh` uses absolute paths such as `/OpenOrbis-PS4-Toolchain` and `/llvm-project`, removes work directories, and clones OpenOrbis, musl, and llvm-project from their remote repositories. Running it unchanged does not provide a reproducible build of local modifications in the pinned submodule. The upstream `Dockerfile` downloads a release archive rather than compiling the local source tree. Review both scripts before adapting them.

A final builder needs to pin each dependency, consume the intended local OpenOrbis source, use an isolated build directory, and produce a versioned install tree. Only then can the graphics stack and Unreal integration be tested against the same toolchain revision.

## Practical sequence

1. Preserve the upstream source layout within an owned fork for core changes.
2. Add a build recipe that takes local paths and pinned dependencies; verify it never replaces the source checkout.
3. Build a minimal OpenOrbis sample with the produced toolchain.
4. Validate graphics and runtime capabilities on PS4 hardware.
5. Integrate a selected Unreal source version after the earlier gates pass.

This document describes the build architecture; it does not claim a complete SDK build or working Unreal port.
