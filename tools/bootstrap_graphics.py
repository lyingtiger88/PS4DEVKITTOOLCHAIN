#!/usr/bin/env python3
"""Fetch or verify the pinned OpenGNM build layout without resetting local work."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PROJECT = Path(__file__).resolve().parent.parent
LOCK = json.loads((PROJECT / "graphics.lock.json").read_text())
DEFAULT_STACK = PROJECT / ".deps" / "graphics" / "opengnm-stack"


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.PIPE
    ).strip()


def ensure_checkout(path: Path, item: dict) -> None:
    url, commit = item["url"], item["commit"]
    if path.exists() and not (path / ".git").exists():
        raise RuntimeError(f"{path} exists but is not a Git checkout")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        git("clone", "--depth", "1", url, str(path))
    origin = git("remote", "get-url", "origin", cwd=path)
    if origin != url:
        raise RuntimeError(f"{path}: expected origin {url}, found {origin}")
    head = git("rev-parse", "HEAD", cwd=path)
    if head != commit:
        if git("status", "--porcelain", cwd=path):
            raise RuntimeError(f"{path}: local changes present; refusing to switch commits")
        git("fetch", "--depth", "1", "origin", commit, cwd=path)
        git("checkout", "--detach", commit, cwd=path)


def verify(stack: Path) -> list[str]:
    failures = []
    for name, item in LOCK["repositories"].items():
        path = stack if name == "opengnm-stack" else stack / name
        if not (path / ".git").exists():
            failures.append(f"missing checkout: {path}")
            continue
        head = git("rev-parse", "HEAD", cwd=path)
        if head != item["commit"]:
            failures.append(f"{name}: expected {item['commit']}, found {head}")
        origin = git("remote", "get-url", "origin", cwd=path)
        if origin != item["url"]:
            failures.append(f"{name}: unexpected origin {origin}")
    for name, expected in LOCK["stack_submodules"].items():
        path = stack / name
        if not path.is_dir() or not (path / ".git").exists():
            failures.append(f"missing submodule: {name}")
        else:
            head = git("rev-parse", "HEAD", cwd=path)
            if head != expected:
                failures.append(f"{name}: expected {expected}, found {head}")
    return failures


def preflight(stack: Path) -> dict:
    commands = {name: bool(shutil.which(name)) for name in (
        "git", "clang", "clang++", "ld.lld", "llvm-ar", "cmake", "make", "python3"
    )}
    try:
        import mako  # noqa: F401
        mako_found = True
    except ImportError:
        mako_found = False
    sdk_value = os.environ.get("OO_PS4_TOOLCHAIN")
    sdk = Path(sdk_value).expanduser() if sdk_value else None
    return {
        "stack": str(stack),
        "source_layout_ok": not verify(stack),
        "commands": commands,
        "python_mako": mako_found,
        "sdk_path": str(sdk) if sdk else None,
        "sdk_link_script": bool(sdk and (sdk / "link.x").is_file()),
        "sdk_crt": bool(sdk and (sdk / "lib" / "crt1.o").is_file()),
        "sdk_libc": bool(sdk and (sdk / "lib" / "libc.a").is_file()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack", type=Path, default=DEFAULT_STACK)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--fetch", action="store_true", help="Fetch exact revisions without overwriting local changes")
    actions.add_argument("--check", action="store_true", help="Verify pinned source layout")
    actions.add_argument("--preflight", action="store_true", help="Report source and build prerequisites")
    args = parser.parse_args()
    stack = args.stack.resolve()
    try:
        if args.fetch:
            ensure_checkout(stack, LOCK["repositories"]["opengnm-stack"])
            for name in LOCK["stack_submodules"]:
                path = stack / name
                if (path / ".git").exists() and git("status", "--porcelain", cwd=path):
                    raise RuntimeError(f"{name}: local changes present; refusing to update submodule")
            git("submodule", "update", "--init", "--recursive", "--depth", "1", cwd=stack)
            for name in ("Vulkan-Headers", "SPIRV-Headers"):
                ensure_checkout(stack / name, LOCK["repositories"][name])
        if args.preflight:
            print(json.dumps(preflight(stack), indent=2))
            return 0
        failures = verify(stack)
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print(f"Pinned OpenGNM source layout verified: {stack}")
        return 0
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"bootstrap failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
