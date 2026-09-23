#!/usr/bin/env python3
"""Run OpenGNM generic-backend tests against the pinned graphics checkout."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

from bootstrap_graphics import DEFAULT_STACK, verify

TEST_SOURCES = (
    "test_main.c", "test_surface.c", "test_drawcmd.c", "test_validate.c",
    "test_api.c", "test_compat.c", "test_helpers.c", "test_pm4.c"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack", type=Path, default=DEFAULT_STACK)
    args = parser.parse_args()
    stack = args.stack.resolve()
    failures = verify(stack)
    if failures:
        parser.error("\n".join(failures))
    cc = shutil.which("cc")
    if not cc:
        parser.error("C compiler 'cc' not found")
    core = stack / "opengnm"
    config = core / "config.mak"
    generic = (core / "config.generic.mak").read_bytes()
    if config.exists() and config.read_bytes() != generic:
        parser.error(f"{config} differs from generic config; refusing to overwrite it")
    config.write_bytes(generic)

    # Upstream's Makefile puts -lm before its static archive during test linking.
    # Build the library normally and link the same upstream test sources in the
    # correct order here, without modifying upstream files.
    subprocess.run(["make", "lib", f"CC={cc}"], cwd=core, check=True)
    binary = core / "opengnm_tests"
    cmd = [cc, "-std=c11", "-Iinclude", "-Isrc", "-Itests"]
    cmd.extend(f"tests/{source}" for source in TEST_SOURCES)
    cmd.extend(["libopengnm.a", "-lm", "-o", str(binary)])
    subprocess.run(cmd, cwd=core, check=True)
    result = subprocess.run([str(binary)], cwd=core, text=True, capture_output=True)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode != 0 or "ALL TESTS PASSED" not in result.stdout:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
