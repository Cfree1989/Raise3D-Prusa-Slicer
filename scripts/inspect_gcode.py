"""Extract Raise3D / ideaMaker machine-behavior facts from a G-code file."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

INTERESTING = re.compile(
    r"^(M99123|M1001|M1002|M2000|M600|M92\b|M218\b|G28\b|G29\b|T0\b|T1\b|G10\b|G11\b|"
    r"SET_|M221\b|M104\b|M109\b|M140\b|M190\b|M106\b|M107\b|M84\b)",
    re.IGNORECASE,
)
HEADER_HINT = re.compile(
    r"(printer|nozzle|filament|dimension|template|firmware|hyper|sliced|slicer version|"
    r"bounding box|origin|plate shape|extruder offset)",
    re.IGNORECASE,
)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def inspect(path: Path) -> str:
    lines = read_lines(path)
    out: list[str] = []
    out.append(f"file: {path}")
    out.append(f"lines: {len(lines)}")
    out.append("")
    out.append("=== first 200 lines ===")
    out.extend(lines[:200])
    out.append("")
    out.append("=== header / machine comments ===")
    for i, line in enumerate(lines, 1):
        if line.startswith(";") and HEADER_HINT.search(line):
            out.append(f"{i}: {line}")
    out.append("")
    out.append("=== interesting commands (unique, with first line number) ===")
    seen: dict[str, int] = {}
    counts: Counter[str] = Counter()
    for i, line in enumerate(lines, 1):
        raw = line.split(";", 1)[0].strip()
        if not raw:
            continue
        if INTERESTING.match(raw):
            key = raw
            counts[key] += 1
            if key not in seen:
                seen[key] = i
    for cmd, first in seen.items():
        out.append(f"{first}: {cmd}  (x{counts[cmd]})")
    out.append("")
    out.append("=== last 40 executable-looking lines before ;Data start ===")
    tail = []
    for line in lines:
        if line.startswith(";Data start"):
            break
        tail.append(line)
    out.extend(tail[-40:])
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gcode", type=Path)
    args = parser.parse_args()
    if not args.gcode.is_file():
        print(f"not found: {args.gcode}", file=sys.stderr)
        return 1
    sys.stdout.write(inspect(args.gcode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
