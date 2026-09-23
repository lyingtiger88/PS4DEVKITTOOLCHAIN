#!/usr/bin/env python3
"""Extract a cautious, reproducible source audit from a vulkan-ps4 checkout."""

import argparse
import collections
import json
from pathlib import Path
import re
import subprocess
import sys


def git_revision(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def audit(root: Path) -> dict:
    src = root / "src"
    header = root / "include" / "vk_ps4_internal.h"
    entry = src / "vk_ps4_entry.c"
    if not header.is_file() or not entry.is_file():
        raise ValueError("Expected a vulkan-ps4 checkout with src/ and include/")

    version_match = re.search(r"#define\s+VK_PS4_API_VERSION\s+VK_MAKE_VERSION\(([^)]+)\)", header.read_text())
    entry_text = entry.read_text()
    extensions_match = re.search(
        r"g_device_extensions\[\]\s*=\s*\{(.*?)\};", entry_text, re.S
    )
    if not version_match or not extensions_match:
        raise ValueError("Upstream layout changed; inspect the version or extension declaration")
    extensions = re.findall(r"\{(VK_[A-Z0-9_]+_EXTENSION_NAME)\s*,", extensions_match.group(1))
    counts = collections.Counter(extensions)
    explicit_unsupported = []
    for source in sorted(src.glob("*.c")):
        for number, line in enumerate(source.read_text(errors="replace").splitlines(), 1):
            if "VK_ERROR_FEATURE_NOT_PRESENT" in line or "VK_ERROR_FORMAT_NOT_SUPPORTED" in line:
                # A textual match may be a comment or a guarded path, not proof of failure.
                explicit_unsupported.append({"file": source.name, "line": number, "text": line.strip()[:180]})

    return {
        "upstream": "PS4-OpenGNM/vulkan-ps4",
        "revision": git_revision(root),
        "advertised_api_version_expression": version_match.group(1).replace(" ", ""),
        "advertised_device_extension_count": len(extensions),
        "duplicate_device_extensions": {k: v for k, v in counts.items() if v > 1},
        "explicit_unsupported_text_matches": explicit_unsupported,
        "interpretation": "Source inspection only; inspect guards and test on PS4 before treating a path as supported or broken.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Local vulkan-ps4 checkout")
    args = parser.parse_args()
    try:
        result = audit(args.checkout.resolve())
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
