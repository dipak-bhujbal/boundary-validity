#!/usr/bin/env python3
"""Regenerate docs/pre-registration/manifest.md from the current git HEAD.

Run before OSF pre-registration submission to freeze the file list.
Idempotent: writes the same content given the same HEAD.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        out = subprocess.check_output(["git", "ls-tree", "-r", "HEAD"], text=True)
    except subprocess.CalledProcessError as e:
        print(f"git ls-tree failed: {e}", file=sys.stderr)
        return 1

    rows: list[tuple[str, str]] = []
    for line in out.strip().split("\n"):
        parts = line.split()
        if len(parts) < 4:
            continue
        blob = parts[2]
        path = " ".join(parts[3:])
        rows.append((path, blob))
    rows.sort()

    lines = [
        "# Full manifest (frozen at pre-registration)",
        "",
        "This file lists every tracked file at its blob hash as of the pinned commit.",
        "Auto-generated; regenerate before OSF submission with:",
        "",
        "```bash",
        "python3 scripts/gen-manifest.py > docs/pre-registration/manifest.md",
        "```",
        "",
        "**Pinned commit:** populate at submission time via `git rev-parse HEAD`.",
        "",
        "| Path | Blob SHA-1 |",
        "|:--|:--|",
    ]
    for path, blob in rows:
        lines.append(f"| `{path}` | `{blob}` |")
    lines.append("")
    lines.append(f"**Total files pinned:** {len(rows)}")

    Path("docs/pre-registration/manifest.md").write_text("\n".join(lines) + "\n")
    print(f"wrote docs/pre-registration/manifest.md with {len(rows)} files",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
