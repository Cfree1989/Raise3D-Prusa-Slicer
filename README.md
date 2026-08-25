# Raise3D Pro2 Plus Hyper Speed — PrusaSlicer (experimental)

**This is not a production-ready profile.** It is a PrusaSlicer bundle derived from known-good ideaMaker G-code on this printer: left-only start/purge from `conradfreeman_filament_orange.gcode`, dual start/tool-change/end from `Multicolor.gcode`. Validate on the machine before any unattended print. Keep ideaMaker as the rollback slicer.

Printer workflow: slice on the PC → copy `.gcode` to USB → start from RaiseTouch. Third-party slicers do not write ideaMaker’s `.data` file, so touchscreen preview/layer metadata may be missing. ([Raise3D: Can I use another slicer?](https://support.raise3d.com/General-Question/can-i-use-another-slicer-14-398.html))

## What is in this pass

| Preset | Name |
| --- | --- |
| Printer | Raise3D Pro2 Plus Hyper Speed 0.4 Dual |
| Filament | Generic PLA |
| Print | XL-style 0.4 mm family: 0.10 FAST DETAIL, 0.15/0.20/0.25 SPEED and STRUCTURAL, 0.28 DRAFT (default 0.20mm SPEED) |

One printer, two 0.4 mm tools (T0 left, T1 right), like XL 2-tool. Assign filament to both slots. Print left-only, right-only, or both: unused tools are skipped via `is_extruder_used`. The printer firmware applies the ~25 mm X nozzle offset — PrusaSlicer offset is `0x0,0x0` so it is not applied twice. Wipe tower is on for dual-color: PrusaSlicer places and shapes it (relative E / `M83`). Do not copy ideaMaker tower coordinates.

Print layout follows Prusa XL IS 0.4 (SPEED / STRUCTURAL / DETAIL / DRAFT). Motion is clipped to Raise3D Pro2 **Hyper FFF L1**: 150 mm/s print, 5000 mm/s² accel, 15 mm³/s. Travel stays **150 mm/s** (this machine’s ideaMaker / `machine_max_feedrate`). XL values of 170–400 mm/s are not used. Generic PLA temps follow Prusa Templates (210/215 °C, 60 °C bed), volumetric 15 mm³/s.

## Install

### A. Configuration Wizard (vendor bundle)

1. Copy `vendor/Raise3D.ini` and `vendor/Raise3D.idx` to `%APPDATA%\PrusaSlicer\vendor\`
2. Restart PrusaSlicer
3. **Configuration Wizard** → Other FFF → enable **Raise3D (experimental)** → Pro2 Plus Hyper Speed Dual 0.4
4. Confirm Generic PLA and the XL-style print profiles appear with that printer selected

Tested against PrusaSlicer **2.9.6**.

### B. Import Config Bundle

1. **File → Import → Import Config Bundle**
2. Select `vendor/Raise3D.ini`
3. Select Dual, then Generic PLA and a print profile (0.20mm SPEED is default)

([PrusaSlicer: importing and exporting custom profiles](https://help.prusa3d.com/article/how-to-import-and-export-custom-profiles-in-prusaslicer_382766))

## Using both extruders

1. Select **Raise3D Pro2 Plus Hyper Speed 0.4 Dual**.
2. Load **Generic PLA** on filament slot 1 and slot 2 (or only the slot you will print with).
3. On the plater, set each object’s extruder (1 = left / T0, 2 = right / T1), or paint multi-material.
4. Slice a small test. Wipe tower is on; drag it on the plater (PrusaSlicer sets position/shape). Unused nozzle drops to 180 °C on tool change.
5. Confirm `;Filament Name #1:` / `#2:` is **`[Raise3D] PLA`** and matches the names loaded on the printer.

Right-only: assign the part to extruder 2. Start G-code still homes with T0, then purges and prints T1.

Keep dual-color (and right-extruder) parts off the leftmost ~25 mm of the bed. The right nozzle is offset in firmware and cannot reach the far left of the plate.

## Source of truth

Start/end G-code and Hyper Speed headers come from ideaMaker **5.4.2.8790** (`RAISE3D Pro2 Plus - Hyper Speed`, `;Firmware: Klipper`, nozzles `0.400 0.400`, bed `305 × 305 × 605`):

- `reference/ideamaker/conradfreeman_filament_orange.gcode` — left `T0` only (purge `X20 Y0`)
- `reference/ideamaker/Multicolor.gcode` — dual / two-color (`T0`+`T1` in-place prime, standby 180 °C). ideaMaker wipe-tower XY is reference only; PrusaSlicer owns the tower.

The 2022 forum zips in `reference/community/` are **community starting points** (Marlin, pre-Hyper Speed). They were not used for start/end G-code. Thread: [Prusa Slicer Profile for Raise3D Pro2 dual head printer](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/).

Command-by-command mapping: `docs/GCODE_MAPPING.md`  
Evidence labels: `docs/MACHINE_BEHAVIOR.md`

## Assumptions you must treat as untested

- Copying `M99123` from the ideaMaker file enables Hyper Speed on the touchscreen (forum reports are mixed).
- `;Filament Name #1: [Raise3D] PLA` (and `#2` on Dual) matches the name loaded on **this** printer. If a slot was renamed, change the G-code comment or the slot so they match exactly.
- PLA at 215/210 °C and 60 °C bed — Prusa Generic PLA, not ideaMaker [Raise3D] PLA 230 °C / 94% flow.
- `SET_VELOCITY_LIMIT ACCEL=5000` at start without ideaMaker’s later 2000/5000 switching.
- `M2000` pause (community; not in the ideaMaker file).
- Dual: electronic lift on `T0`/`T1`, firmware XY offset, in-place dual prime (`F200 E10` / `E-11`), tool-change standby 180 °C. Wipe tower position/shape is PrusaSlicer's (relative E). Mid-print next-tool preheat is not replicated; `M109` waits at the swap.
- Relative E (`M83`) instead of ideaMaker `M82`, required for PrusaSlicer's wipe tower. Left-only purge uses `E1` on the `X20 Y0` move (the extra 1 mm after the 29 mm blob).

## Before you print

1. Slice a small part (assign the tools you will use).
2. Run (the first script is required: PrusaSlicer always writes `; generated by …` before start G-code):

```text
python scripts\ensure_m99123_first.py path\to\sliced.gcode
python scripts\validate_gcode.py path\to\sliced.gcode
python scripts\compare_gcode.py reference\ideamaker\conradfreeman_filament_orange.gcode path\to\sliced.gcode
```

Optional: Print Settings → Output options → Post-processing scripts → `python` plus the full path to `scripts\ensure_m99123_first.py` in this repo, so Export runs the move automatically ([PrusaSlicer post-processing](https://help.prusa3d.com/article/post-processing-scripts_283913)). G-code thumbnails are off in this profile so a PNG block is not sitting in front of the header.

3. Read the first ~80 lines and the end sequence. Confirm `M99123` is line 1, `G28 X0 Y0` then `G28 Z0`, `M1001` / `M1002`, no `G29` / `M92` / `M218`. Left-only: purge `X20 Y0`. Dual: in-place `F200 E10` primes; tool-change standby `S180`; wipe tower is wherever you placed it in PrusaSlicer, not ideaMaker’s X96/X30.
4. Stage 3: supervised first layer (home, heat, purge, Z height, fan, shutdown). Dual: watch the unused nozzle lift, T1 first motion, and the park/prime at tool-change.
5. Do not leave a long job unattended until Stages 3–4 pass. Dual color is Stage 7.

## Rollback

Use ideaMaker with the printer’s Hyper Speed template and USB export as before. Nothing in this repo is written to the printer’s firmware.

## Tests

```text
python -m unittest discover -s tests -v
```
