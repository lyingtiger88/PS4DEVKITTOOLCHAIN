# Upstream dependencies

| Component | Upstream | Revision examined | Role |
| --- | --- | --- | --- |
| OpenOrbis PS4 Toolchain | https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain | `0a1aaf9dd4a92695538bdeb09fb056d06dd11725` | PS4 homebrew compiler, headers, libraries, packaging tools |
| OpenGNM stack | https://github.com/PS4-OpenGNM/opengnm-stack | `2de9fc54ca33b39baa0ace59c6b0059e5de94a63` | Umbrella project for graphics experiments |
| vulkan-ps4 | https://github.com/PS4-OpenGNM/vulkan-ps4 | `f4d940b723771b3fe637e8ac0704bb5d6ab19622` | Candidate Vulkan driver to evaluate before Unreal integration |

OpenOrbis is included as a pinned Git submodule. The source at the pinned revision was also separately downloaded as an archive for this project. That archive is a source snapshot without Git history or prebuilt release binaries. To fetch the source through this repository:

```sh
git clone --recurse-submodules https://github.com/lyingtiger88/PS4DEVKITTOOLCHAIN.git
```

OpenOrbis's README recommends a release ZIP or installer when a ready-to-use toolchain is needed; a source checkout requires building missing binaries and libraries. Check licenses and build instructions in each upstream repository before integrating or redistributing components.
