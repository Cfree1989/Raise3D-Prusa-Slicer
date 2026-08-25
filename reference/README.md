# Reference files (source of truth)

Drop known-good **ideaMaker** output here. PrusaSlicer start/end G-code, tool changes, and Hyper Speed behavior will be derived from these files only. Do not replace them with generic Klipper or Prusa examples.

Currently present:

- `ideamaker/LeftonlyExtruder.gcode` + `.data` — Hyper Speed, left `T0`, `[Raise3D] PLA`
- `ideamaker/RightonlyExtruder.gcode` + `.data` — Hyper Speed, right `T1`, `[Raise3D] PLA`
- `ideamaker/MulticolorRaise3d.gcode` + `.data` — Hyper Speed, dual / two-color `T0`+`T1`, `[Raise3D] PLA`
- `community/` — 2022 Prusa forum config zips; **not** Hyper Speed machine evidence (see `SOURCE_CLASSIFICATION.md`)

`.data` files are binary metadata only and were not modified.

## Essential (needed before left-extruder G-code is written)

| What to add | Why |
| --- | --- |
| Short Hyper Speed ideaMaker `.gcode` using the **left nozzle** and **PLA** (about 20–30 minutes) | Start sequence, end sequence, headers, temperatures, motion |
| Matching `.data` file, if ideaMaker created one | Metadata only; it will not be modified |
| ideaMaker version and RaiseTouch / Hyper Speed firmware version (notes or screenshot) | Version lock for the profile |
| Screenshots of the selected printer, nozzle, filament, and Hyper Speed template | Confirm Hyper Speed mode and 0.4 mm nozzles |

## Strongly recommended

- Known-good ideaMaker file sliced for **regular PLA** (not Hyper Speed PLA unless that is what you actually print)
- Same **0.4 mm** nozzles currently installed
- Right-nozzle `.gcode` — **present** (`RightonlyExtruder.gcode`)
- Dual-extrusion `.gcode` — **present** (`MulticolorRaise3d.gcode`)
- A file that includes pause or filament change
- ideaMaker printer / filament / Hyper Speed template exports
- Notes or photos of the purge-line location and usable print area

## Do not include

Passwords, API keys, network credentials, serial numbers, or other private information.
