#!/usr/bin/env python3
"""One-command readiness report for the pinned OpenOrbis/OpenGNM workspace."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], cwd: Path) -> dict:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-host-tests", action="store_true", help="Also build and run pinned OpenGNM host tests.")
    parser.add_argument("--output", type=Path, default=PROJECT / "build" / "workspace-readiness.json")
    args = parser.parse_args()

    py = sys.executable
    checks = {
        "environment": run([py, "tools/validate_environment.py", "--root", str(PROJECT), "--json"], PROJECT),
        "graphics_preflight": run([py, "tools/bootstrap_graphics.py", "--preflight"], PROJECT),
        "graphics_lock": run([py, "tools/bootstrap_graphics.py", "--check"], PROJECT),
    }
    if args.with_host_tests:
        checks["host_graphics_tests"] = run([py, "tools/run_host_graphics_tests.py"], PROJECT)

    summary = {
        "all_requested_checks_passed": all(item["returncode"] == 0 for item in checks.values()),
        "ps4_hardware_validated": False,
        "oo_ps4_toolchain_set": bool(os.environ.get("OO_PS4_TOOLCHAIN")),
        "note": "Host readiness is not PS4 hardware validation.",
    }
    payload = {"schema": 1, "checks": checks, "summary": summary}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Readiness report: {args.output}")
    for name, result in checks.items():
        print(f"{name}: {'PASS' if result['returncode'] == 0 else 'FAIL'}")
    print("PS4 hardware validated: NO")
    return 0 if summary["all_requested_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
