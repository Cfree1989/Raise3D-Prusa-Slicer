# Raise3D Pro2 Plus Hyper Speed — PrusaSlicer (experimental)

**This is not a production-ready profile.** It is a first-pass, left-extruder-only PrusaSlicer bundle derived from known-good ideaMaker G-code on this printer. Validate on the machine before any unattended print. Keep ideaMaker as the rollback slicer.

Printer workflow: slice on the PC → copy `.gcode` to USB → start from RaiseTouch. Third-party slicers do not write ideaMaker’s `.data` file, so touchscreen preview/layer metadata may be missing. ([Raise3D: Can I use another slicer?](https://support.raise3d.com/General-Question/can-i-use-another-slicer-14-398.html))

## What is in this pass

| Preset | Name |
| --- | --- |
| Printer | Raise3D Pro2 Plus Hyper Speed 0.4 Left |
| Filament | Overture PLA |
| Print | 0.20mm L1 Conservative |

Right-extruder and dual-extrusion profiles are **not implemented**.

## Install

### A. Configuration Wizard (vendor bundle)

1. Copy `vendor/Raise3D.ini` and `vendor/Raise3D.idx` to `%APPDATA%\PrusaSlicer\vendor\`
2. Restart PrusaSlicer
3. **Configuration Wizard** → Other FFF → enable **Raise3D (experimental)** → Pro2 Plus Hyper Speed 0.4
4. Confirm Overture PLA and 0.20mm L1 Conservative appear only with that printer selected

Tested against PrusaSlicer **2.9.6**.

### B. Import Config Bundle

1. **File → Import → Import Config Bundle**
2. Select `vendor/Raise3D.ini`
3. Choose the imported Raise3D printer, then Overture PLA and the L1 print profile

([PrusaSlicer: importing and exporting custom profiles](https://help.prusa3d.com/article/how-to-import-and-export-custom-profiles-in-prusaslicer_382766))

## Source of truth

Start/end G-code and Hyper Speed headers come from:

`reference/ideamaker/conradfreeman_filament_orange.gcode`

sliced by **ideaMaker 5.4.2.8790** as `RAISE3D Pro2 Plus - Hyper Speed`, `;Firmware: Klipper`, left tool `T0` only, nozzles `0.400 0.400`, bed `305 × 305 × 605`.

The 2022 forum zips in `reference/community/` are **community starting points** (Marlin, pre-Hyper Speed). They were not used for start/end G-code. Thread: [Prusa Slicer Profile for Raise3D Pro2 dual head printer](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/).

Command-by-command mapping: `docs/GCODE_MAPPING.md`  
Evidence labels: `docs/MACHINE_BEHAVIOR.md`

## Assumptions you must treat as untested

- Copying `M99123` from the ideaMaker file enables Hyper Speed on the touchscreen (forum reports are mixed).
- `;Filament Name #1: Overture PLA` matches the name loaded on **this** printer. If the slot is still `[Raise3D] PLA`, change one of them so they match exactly.
- Overture PLA at 205/200 °C and 60 °C bed — **not** the 230 °C / 94% flow from the Raise3D PLA sample.
- `SET_VELOCITY_LIMIT ACCEL=5000` at start without ideaMaker’s later 2000/5000 switching.
- `M2000` pause (community; not in the ideaMaker file).

## Before you print

1. Slice a small left-only PLA part.
2. Run:

```text
python scripts\validate_gcode.py path\to\sliced.gcode
python scripts\compare_gcode.py reference\ideamaker\conradfreeman_filament_orange.gcode path\to\sliced.gcode
```

3. Read the first ~80 lines and the end sequence. Confirm `M99123` is line 1, `G28 X0 Y0` then `G28 Z0`, purge `X20 Y0`, `M1001` / `M1002`, no `G29` / `M92` / `M218`.
4. Stage 3: supervised first layer (home, heat, purge, Z height, fan, shutdown).
5. Do not leave a long job unattended until Stages 3–4 pass.

## Rollback

Use ideaMaker with the printer’s Hyper Speed template and USB export as before. Nothing in this repo is written to the printer’s firmware.

## Tests

```text
python -m unittest discover -s tests -v
```
