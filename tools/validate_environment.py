#!/usr/bin/env python3
"""Report the local prerequisites and pinned-input state for PS4 research.

This script is intentionally read-only. It never downloads dependencies and
never claims that a PS4 build is valid. Missing tools are reported explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


TOOLS = ("clang", "clang++", "ld.lld", "llvm-ar", "cmake", "make", "python3")


def run_version(executable: str) -> str | None:
    path = shutil.which(executable)
    if not path:
        return None
    try:
        proc = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "present (version probe failed)"
    line = (proc.stdout or proc.stderr).splitlines()
    return line[0].strip() if line else "present"


def git_rev(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    try:
        proc = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = proc.stdout.strip()
    return value or None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Research workspace containing the dependency checkouts.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    result = {
        "root": str(root),
        "tools": {tool: run_version(tool) for tool in TOOLS},
        "environment": {
            "OO_PS4_TOOLCHAIN": os.environ.get("OO_PS4_TOOLCHAIN"),
        },
        "checkouts": {
            name: git_rev(root / name)
            for name in (
                "opengnm",
                "opengnm-psbc",
                "vulkan-ps4",
                "OpenOrbis-PS4-Toolchain",
                "Vulkan-Headers",
                "SPIRV-Headers",
            )
        },
    }

    missing_tools = [name for name, version in result["tools"].items() if version is None]
    result["summary"] = {
        "missing_host_tools": missing_tools,
        "cross_toolchain_present": bool(result["environment"]["OO_PS4_TOOLCHAIN"]),
        "note": (
            "This is an environment report only. It is not evidence of PS4 "
            "hardware compatibility."
        ),
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Workspace: {root}")
        print("\nHost tools:")
        for name, version in result["tools"].items():
            print(f"  {name:10} {version or 'MISSING'}")
        print("\nOO_PS4_TOOLCHAIN:")
        print(f"  {result['environment']['OO_PS4_TOOLCHAIN'] or 'NOT SET'}")
        print("\nDependency revisions:")
        for name, revision in result["checkouts"].items():
            print(f"  {name:24} {revision or 'NOT FOUND'}")
        print("\nResult:")
        print(f"  missing host tools: {', '.join(missing_tools) or 'none'}")
        print(
            "  cross toolchain: "
            + ("configured" if result["summary"]["cross_toolchain_present"] else "not configured")
        )
        print("  NOTE: environment state is not PS4 hardware validation.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
