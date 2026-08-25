"""Compare ideaMaker reference headers/start/end with a PrusaSlicer G-code file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKERS = (
    "M99123",
    ";Dimension:",
    ";Printer Type:",
    ";Firmware:",
    ";Filament Name #1:",
    "G28 X0 Y0",
    "G28 Z0",
    "G1 Z15.0 F300",
    "G1 F140 E29",
    "G1 X20 Y0",
    "M1001",
    "SET_VELOCITY_LIMIT ACCEL=5000.00",
    "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=10.00",
    "M1002",
    "M104 T0 S0",
    "M140 S0",
    "M84",
)


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def first_n_exec(text: str, n: int = 80) -> list[str]:
    lines = []
    for line in text.splitlines():
        if line.startswith(";Data start"):
            break
        lines.append(line)
        if len(lines) >= n:
            break
    return lines


def last_end(text: str, n: int = 30) -> list[str]:
    buf = []
    for line in text.splitlines():
        if line.startswith(";Data start"):
            break
        buf.append(line)
    return buf[-n:]


def compare(reference: Path, candidate: Path) -> int:
    ref = load(reference)
    cand = load(candidate)
    missing = [m for m in MARKERS if m not in cand]
    print(f"reference: {reference}")
    print(f"candidate: {candidate}")
    print()
    if missing:
        print("MISSING expected markers from ideaMaker mapping:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("All expected start/end markers are present.")
    print()
    print("=== candidate first 60 lines ===")
    print("\n".join(first_n_exec(cand, 60)))
    print()
    print("=== candidate end (before ;Data start / EOF) ===")
    print("\n".join(last_end(cand, 25)))
    print()
    print("=== reference start (first 45) ===")
    print("\n".join(first_n_exec(ref, 45)))
    return 1 if missing else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    for p in (args.reference, args.candidate):
        if not p.is_file():
            print(f"not found: {p}", file=sys.stderr)
            return 1
    return compare(args.reference, args.candidate)


if __name__ == "__main__":
    raise SystemExit(main())
