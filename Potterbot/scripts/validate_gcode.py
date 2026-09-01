"""Reject Potterbot G-code that would heat the machine or skip the end retract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

BED_X = 381.0
BED_Y = 360.0
BED_Z = 400.0
END_RETRACT = 500
HEAT_RE = re.compile(r"\bM1(?:04|09|40|90)\b[^;\n]*\bS\s*([0-9]+(?:\.[0-9]+)?)", re.I)
MOVE_RE = re.compile(
    r"^\s*(?:G0|G1|G2|G3)\b(?P<body>[^;]*)",
    re.I,
)
AXIS_RE = re.compile(r"\b([XYZEF])\s*(-?[0-9]+(?:\.[0-9]+)?)", re.I)


class ValidationError(Exception):
    pass


def _heat_value(line: str) -> float | None:
    match = HEAT_RE.search(line)
    if not match:
        return None
    return float(match.group(1))


def validate(text: str) -> None:
    errors: list[str] = []
    if "G28" not in text.upper():
        errors.append("missing G28 (home)")

    trailing = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(";")]
    end = "\n".join(trailing[-40:])
    if not re.search(rf"\bE-?{END_RETRACT}\b", end, re.I):
        errors.append(f"end G-code must retract E-{END_RETRACT} to stop clay ooze")

    if not re.search(r"\bM83\b", text):
        errors.append("missing M83 (firmware and official Cura use relative E)")

    x = y = z = 0.0
    relative = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        heat = _heat_value(line)
        if heat is not None and heat > 0:
            errors.append(f"line {lineno}: heater command with S{heat:g} (clay is cold)")
        upper = line.upper()
        if upper.startswith("G90"):
            relative = False
        elif upper.startswith("G91"):
            relative = True
        move = MOVE_RE.match(line)
        if not move:
            continue
        axes = {m.group(1).upper(): float(m.group(2)) for m in AXIS_RE.finditer(move.group("body"))}
        if "X" in axes:
            x = x + axes["X"] if relative else axes["X"]
        if "Y" in axes:
            y = y + axes["Y"] if relative else axes["Y"]
        if "Z" in axes:
            z = z + axes["Z"] if relative else axes["Z"]
        if not relative:
            if x < -0.05 or x > BED_X + 0.05:
                errors.append(f"line {lineno}: X{x:g} outside bat {BED_X:g} mm")
            if y < -0.05 or y > BED_Y + 0.05:
                errors.append(f"line {lineno}: Y{y:g} outside printable Y {BED_Y:g} mm")
            if z < -0.05 or z > BED_Z + 0.05:
                errors.append(f"line {lineno}: Z{z:g} outside Z {BED_Z:g} mm")

    if errors:
        raise ValidationError("\n".join(errors))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: validate_gcode.py <file.gcode>", file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        validate(path.read_text(encoding="utf-8", errors="replace"))
    except ValidationError as exc:
        print(f"{path}:\n{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
