# Reference files

Known-good **ideaMaker** output lives in `ideamaker/`. PrusaSlicer start/end G-code, tool changes, and Hyper Speed behavior are derived from those files only. Do not replace them with generic Klipper or Prusa examples.

| Path | What it is |
| --- | --- |
| `ideamaker/` | Authoritative Hyper Speed ideaMaker jobs (left / right / dual) plus a later ideaMaker comparison slice |
| `prusaslicer/` | Exports from this experimental Dual profile — compare only, not a source of start/end G-code |
| `prusa-xl/` | Prusa XL IS slices of the same models — motion/wipe-tower reference, not machine evidence |
| `community/` | 2022 Prusa forum config zips; **not** Hyper Speed machine evidence (see `SOURCE_CLASSIFICATION.md`) |

`.data` files are binary metadata only and were not modified.

## ideaMaker (source of truth)

- `ideamaker/LeftonlyExtruder.gcode` + `.data` — Hyper Speed, left `T0`, `[Raise3D] PLA`
- `ideamaker/RightonlyExtruder.gcode` + `.data` — Hyper Speed, right `T1`, `[Raise3D] PLA`
- `ideamaker/MulticolorRaise3d.gcode` + `Multicolor.data` — Hyper Speed, dual / two-color `T0`+`T1`, `[Raise3D] PLA`
- `ideamaker/IdeaMakerTest.gcode` + `.data` — later ideaMaker slice of the same test model as `prusaslicer/Raise3DTest_…`

## PrusaSlicer (this profile)

- `prusaslicer/Raise3DTest_0.4n_0.2mm_PLA_PRO2PLUS_HS_DUAL_3h2m.gcode` — current Dual profile export
- `prusaslicer/proj_1_…`, `RaiseMulticolor_…`, `Dualcolorsupportj_…` — earlier Dual-profile exports (pre–Hyper Speed print preset)

## Prusa XL (comparison only)

- `prusa-xl/PrusaXLTest_0.4n_0.2mm_PLA_XLIS_2h29m.bgcode`
- `prusa-xl/PrusaMulticolor_1_0.4n_0.2mm_PLA,PLA_XLIS_4h0m.bgcode`

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
