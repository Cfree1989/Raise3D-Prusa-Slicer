# Raise3D Pro2 Plus Hyper Speed — PrusaSlicer (experimental)

**This is not a production-ready profile.** It is a PrusaSlicer bundle derived from known-good ideaMaker G-code on this printer (left tool) plus dual-head start/tool-change built from that sequence. Validate on the machine before any unattended print. Keep ideaMaker as the rollback slicer.

Printer workflow: slice on the PC → copy `.gcode` to USB → start from RaiseTouch. Third-party slicers do not write ideaMaker’s `.data` file, so touchscreen preview/layer metadata may be missing. ([Raise3D: Can I use another slicer?](https://support.raise3d.com/General-Question/can-i-use-another-slicer-14-398.html))

## What is in this pass

| Preset | Name |
| --- | --- |
| Printer | Raise3D Pro2 Plus Hyper Speed 0.4 Dual |
| Filament | PLA |
| Print | 0.20mm SPEED |

One printer, two 0.4 mm tools (T0 left, T1 right), like XL 2-tool. Assign filament to both slots. Print left-only, right-only, or both: unused tools are skipped via `is_extruder_used`. The printer firmware applies the ~25 mm X nozzle offset — PrusaSlicer offset is `0x0,0x0` so it is not applied twice. Wipe tower is off: PrusaSlicer only allows it with relative E, and this printer keeps ideaMaker’s `M82` / absolute E.

Print layout and speeds follow Prusa XL IS 0.20 SPEED, clipped to Raise3D Pro2 **Hyper FFF L1**: 150 mm/s print, 5000 mm/s² accel, 15 mm³/s. Travel stays **150 mm/s** (this machine’s ideaMaker / `machine_max_feedrate`). XL values of 170–400 mm/s are not used.

## Install

### A. Configuration Wizard (vendor bundle)

1. Copy `vendor/Raise3D.ini` and `vendor/Raise3D.idx` to `%APPDATA%\PrusaSlicer\vendor\`
2. Restart PrusaSlicer
3. **Configuration Wizard** → Other FFF → enable **Raise3D (experimental)** → Pro2 Plus Hyper Speed Dual 0.4
4. Confirm PLA and the matching L1 print profile appear with that printer selected

Tested against PrusaSlicer **2.9.6**.

### B. Import Config Bundle

1. **File → Import → Import Config Bundle**
2. Select `vendor/Raise3D.ini`
3. Select Dual, then PLA and 0.20mm SPEED

([PrusaSlicer: importing and exporting custom profiles](https://help.prusa3d.com/article/how-to-import-and-export-custom-profiles-in-prusaslicer_382766))

## Using both extruders

1. Select **Raise3D Pro2 Plus Hyper Speed 0.4 Dual**.
2. Load **PLA** on filament slot 1 and slot 2 (or only the slot you will print with).
3. On the plater, set each object’s extruder (1 = left / T0, 2 = right / T1), or paint multi-material.
4. Slice a small test. Wipe tower stays off (absolute E).
5. Confirm `;Filament Name #1:` / `#2:` is **PLA** and matches the names loaded on the printer.

Right-only: assign the part to extruder 2. Start G-code still homes with T0, then purges and prints T1.

Keep dual-color (and right-extruder) parts off the leftmost ~25 mm of the bed. The right nozzle is offset in firmware and cannot reach the far left of the plate.

## Source of truth

Start/end G-code and Hyper Speed headers come from:

`reference/ideamaker/conradfreeman_filament_orange.gcode`

sliced by **ideaMaker 5.4.2.8790** as `RAISE3D Pro2 Plus - Hyper Speed`, `;Firmware: Klipper`, left tool `T0` only, nozzles `0.400 0.400`, bed `305 × 305 × 605`.

Dual heat/purge/tool-change is that left sequence plus `T1` when the right tool is used. There is not yet a matching ideaMaker dual file. The 2022 forum zips in `reference/community/` are **community starting points** (Marlin, pre-Hyper Speed). They were not used for start/end G-code. Thread: [Prusa Slicer Profile for Raise3D Pro2 dual head printer](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/).

Command-by-command mapping: `docs/GCODE_MAPPING.md`  
Evidence labels: `docs/MACHINE_BEHAVIOR.md`

## Assumptions you must treat as untested

- Copying `M99123` from the ideaMaker file enables Hyper Speed on the touchscreen (forum reports are mixed).
- `;Filament Name #1: PLA` (and `#2` on Dual) matches the name loaded on **this** printer. If the slot is still `[Raise3D] PLA`, change one of them so they match exactly.
- PLA at 215/210 °C and 60 °C bed — Prusa generic PLA, not ideaMaker [Raise3D] PLA 230 °C / 94% flow.
- `SET_VELOCITY_LIMIT ACCEL=5000` at start without ideaMaker’s later 2000/5000 switching.
- `M2000` pause (community; not in the ideaMaker file).
- Dual: electronic lift on `T0`/`T1`, firmware XY offset, T1 purge at `X40 Y0`, and tool-change standby (`temperature-30` then `M109`) — no ideaMaker dual G-code yet.

## Before you print

1. Slice a small part (assign the tools you will use).
2. Run:

```text
python scripts\validate_gcode.py path\to\sliced.gcode
python scripts\compare_gcode.py reference\ideamaker\conradfreeman_filament_orange.gcode path\to\sliced.gcode
```

3. Read the first ~80 lines and the end sequence. Confirm `M99123` is line 1, `G28 X0 Y0` then `G28 Z0`, left purge `X20 Y0`, `M1001` / `M1002`, no `G29` / `M92` / `M218`. Dual: T1 heat/purge only if that tool is used; tool-change must not contain `M218`.
4. Stage 3: supervised first layer (home, heat, purge, Z height, fan, shutdown). Dual: watch the unused nozzle lift and T1 first motion.
5. Do not leave a long job unattended until Stages 3–4 pass. Dual color is Stage 7.

## Rollback

Use ideaMaker with the printer’s Hyper Speed template and USB export as before. Nothing in this repo is written to the printer’s firmware.

## Tests

```text
python -m unittest discover -s tests -v
```
