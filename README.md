# Raise3D Pro2 Plus Hyper Speed — PrusaSlicer (experimental)

**This is not a production-ready profile.** It is a PrusaSlicer bundle derived from known-good ideaMaker G-code on this printer: left-only from `LeftonlyExtruder.gcode`, right-only from `RightonlyExtruder.gcode`, dual start/tool-change/end from `MulticolorRaise3d.gcode`. Validate on the machine before any unattended print. Keep ideaMaker as the rollback slicer.

Printer workflow: slice on the PC → copy `.gcode` to USB → start from RaiseTouch. Third-party slicers do not write ideaMaker’s `.data` file, so touchscreen preview/layer metadata may be missing. ([Raise3D: Can I use another slicer?](https://support.raise3d.com/General-Question/can-i-use-another-slicer-14-398.html))

## What is in this pass

| Preset | Name |
| --- | --- |
| Printer | Raise3D Pro2 Plus Hyper Speed 0.4 Dual |
| Filament | PLA / PETG / TPU / ASA / PA-CF / ABS-GF Raise3D |
| Print | XL-style 0.4 mm family: 0.10 FAST DETAIL, 0.15/0.20/0.25 SPEED and STRUCTURAL, 0.28 DRAFT (default 0.20mm SPEED) |

One printer, two 0.4 mm tools (T0 left, T1 right), like XL 2-tool. Assign filament to both slots. Print left-only, right-only, or both: unused tools are skipped via `is_extruder_used`. The printer firmware applies the ~25 mm X nozzle offset — PrusaSlicer offset is `0x0,0x0` so it is not applied twice. Wipe tower is on for dual-color: PrusaSlicer places and shapes it (relative E / `M83`). Do not copy ideaMaker tower coordinates.

Print layout follows Prusa XL IS 0.4 (SPEED / STRUCTURAL / DETAIL / DRAFT). Motion is clipped to Raise3D Pro2 **Hyper FFF L1**: 150 mm/s print, 5000 mm/s² accel, 15 mm³/s. Travel stays **150 mm/s** (this machine’s ideaMaker / `machine_max_feedrate`). XL values of 170–400 mm/s are not used. PLA Raise3D nozzle is **215 °C first layer / 225 °C other layers**, multiplier **1.00**, bed **60 °C** (operator’s PLA XL / proven Prusa PLA). PETG, TPU, ASA, PA-CF, and ABS-GF Raise3D use the same first-layer/other-layer temps as the matching `* XL` user presets; TPU volumetric is 4 mm³/s. Dual unused-nozzle standby stays **180 °C** from ideaMaker. Filament presets are compatible only with this Dual 0.4 printer.

## Install

### Lab PC (required before slicing)

Print profiles call two post-processing scripts by **absolute path**. Put this repo at `C:\Repos\Raise3D-Prusa-Slicer` (clone or copy the whole tree). Then install:

1. **PrusaSlicer 2.9.6** (the version this bundle was tested against).
2. **Python 3** from [python.org](https://www.python.org/downloads/) — ordinary CPython, GIL on. 3.13 and 3.14 both work. Do not use the free-threaded (no-GIL) build. No pip packages: the scripts use only the standard library.
3. Confirm the Windows launcher: `py -3 --version` in a command prompt. Profiles run `C:\Windows\py.exe -3`, which picks the **newest Python 3** on the machine, not a pinned `C:\Python313\python.exe`.

Required scripts (already in the repo):

```text
C:\Repos\Raise3D-Prusa-Slicer\scripts\ensure_m99123_first.py
C:\Repos\Raise3D-Prusa-Slicer\scripts\validate_gcode.py
```

If the repo lives anywhere else, post-processing will fail until those two files are at that path. `compare_gcode.py` is optional and is not run by PrusaSlicer.

Then install the vendor profiles (A or B below). ideaMaker is rollback only; nothing here is written to printer firmware.

### A. Configuration Wizard (vendor bundle)

1. Copy `vendor/Raise3D.ini`, `vendor/Raise3D.idx`, and the `vendor/Raise3D/` folder (bed texture) to `%APPDATA%\PrusaSlicer\vendor\`
2. Restart PrusaSlicer
3. **Configuration Wizard** → Other FFF → enable **Raise3D (experimental)** → Pro2 Plus Hyper Speed Dual 0.4
4. Confirm PLA Raise3D (and the other Raise3D filaments if you want them) and the XL-style print profiles appear with that printer selected

If slicing fails on post-processing, check that `py -3 --version` works and that the two scripts exist at the path above.

### B. Import Config Bundle

1. **File → Import → Import Config Bundle**
2. Select `vendor/Raise3D.ini`
3. Select Dual, then PLA Raise3D and a print profile (0.20mm SPEED is default)

Import Config Bundle does not install `vendor/Raise3D/PRO2PLUS_HS_DUAL_texture.svg`. Copy that folder as in A if you want the orange T1 keep-out stripe on the plater. Default wipe tower X50 Y140 still applies.

([PrusaSlicer: importing and exporting custom profiles](https://help.prusa3d.com/article/how-to-import-and-export-custom-profiles-in-prusaslicer_382766))

## Using both extruders

1. Select **Raise3D Pro2 Plus Hyper Speed 0.4 Dual**.
2. Load **PLA Raise3D** (or PETG/TPU/ASA/PA-CF/ABS-GF Raise3D) on filament slot 1 and slot 2 (or only the slot you will print with). These presets are tied to this Dual printer only (Filament → Dependencies).
3. On the plater, set each object’s extruder (1 = left / T0, 2 = right / T1), or paint multi-material.
4. Slice a small test. Wipe tower is on; default is **X50 Y140** so T1 can reach it. Drag it on the plater if you want. Unused nozzle drops to 180 °C on tool change. The orange stripe on the bed is T1 keep-out (leftmost ~25 mm).
5. Confirm `;Filament Name #1:` / `#2:` is **`[Raise3D] `** plus the selected `filament_type` (PLA still emits `[Raise3D] PLA`) and matches the names loaded on the printer. Custom G-code writes `{"[Raise3D] "}` so PrusaSlicer does not parse `[Raise3D]` as a variable.

Right-only: assign the part to extruder 2. Start G-code heats T1 only, homes on T1, then uses the same `F140 E29` / `X80 Y0` wipe as left-only (from `RightonlyExtruder.gcode`, XY extended past ideaMaker `X20` so the fan clears the blob). Dual in-place `E10`/`E-11` is only when both tools are used; both modes then travel `G1 X80 Y0 F9000` at Z15.

Keep dual-color (and right-extruder) parts **and the wipe tower** off the leftmost ~25 mm of the bed. The right nozzle offset lives in firmware (`extruder_offset` stays `0x0,0x0`). PrusaSlicer 2.9.6 cannot clip T1’s printable polygon; the bed texture is a reminder, and `validate_gcode.py` errors on T1 moves with X < 25 mm after `M1001`. Start-sequence T1 purge at home (before `M1001`) is allowed.

## Source of truth

Start/end G-code and Hyper Speed headers come from ideaMaker **5.4.2.8790** (`RAISE3D Pro2 Plus - Hyper Speed`, `;Firmware: Klipper`, nozzles `0.400 0.400`, bed `305 × 305 × 605`):

- `reference/ideamaker/LeftonlyExtruder.gcode` — left `T0` only (purge `X20 Y0`)
- `reference/ideamaker/RightonlyExtruder.gcode` — right `T1` only (same `X20 Y0` wipe; home on T1)
- `reference/ideamaker/MulticolorRaise3d.gcode` — dual / two-color (`T0`+`T1` in-place prime, standby 180 °C). ideaMaker wipe-tower XY is reference only; PrusaSlicer owns the tower.

The 2022 forum zips in `reference/community/` are **community starting points** (Marlin, pre-Hyper Speed). They were not used for start/end G-code. Thread: [Prusa Slicer Profile for Raise3D Pro2 dual head printer](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/).

Command-by-command mapping: `docs/GCODE_MAPPING.md`  
Evidence labels: `docs/MACHINE_BEHAVIOR.md`

## Assumptions you must treat as untested

- Copying `M99123` from the ideaMaker file enables Hyper Speed on the touchscreen (forum reports are mixed).
- `;Filament Name #1: [Raise3D] PLA` (and `#2` on Dual) when slicing PLA matches the name loaded on **this** printer. Other materials emit `[Raise3D] PETG`, `[Raise3D] TPU`, `[Raise3D] ASA`, `[Raise3D] PA`, `[Raise3D] ABS`. If a slot was renamed, change the slot so it matches exactly.
- PLA at 215 °C first layer / 225 °C other layers, multiplier 1.00, 60 °C bed — operator’s PLA XL / proven Prusa PLA. PETG/TPU/ASA/PA-CF/ABS-GF temps are copied from the matching `* XL` user presets; cooling and retract are generic for type, not copied from XL. ideaMaker `[Raise3D] PLA` was 230 °C / 94%; dual standby stays 180 °C from Multicolor (filament idle is not used in Raise3D tool-change G-code).
- `SET_VELOCITY_LIMIT` print 2000 / travel 5000 / first layer 500 after converting PrusaSlicer `M204 S`. Cadence will not match ideaMaker’s ~10k switches exactly.
- SPEED print 150 mm/s vs STRUCTURAL (XL 80/45 walls). First layer is 40 mm/s on every profile. Hyper FFF L1 is 150 mm/s / 15 mm³/s; do not flatten SPEED to 75. ideaMaker files already print at 120 and 150.
- `M2000` pause (community; not in the ideaMaker file).
- Dual: electronic lift on `T0`/`T1`, firmware XY offset (~25 mm X; slicer offset 0), in-place dual prime (`F200 E10` / `E-11`) when both tools are used, then `G1 X80 Y0 F9000` at Z15 (ideaMaker dual has no XY wipe; X20 left the fan in the blob). Tool-change standby 180 °C. Right-only uses the same `X80 Y0` wipe as left, after homing on T1. Wipe tower default X50 Y140 (relative E); this ideaMaker dual file placed the octagon around ~X50 Y241. Next-tool `M104` is inserted ~400 lines before swap `M109` (ideaMaker gaps 64–2200, median 762). T1 in this dual file stays ≥ ~X27; validator keep-out is X < 25.
- Relative E (`M83`) instead of ideaMaker `M82`, required for PrusaSlicer's wipe tower. Left-only purge uses `E1` on the `X80 Y0` move (the extra 1 mm after the 29 mm blob).

## Before you print

1. Slice a small part (assign the tools you will use). Print profiles run `scripts\ensure_m99123_first.py` then `scripts\validate_gcode.py` as post-processing ([PrusaSlicer post-processing](https://help.prusa3d.com/article/post-processing-scripts_283913)): that moves `M99123` to line 1, converts `M204` to `SET_VELOCITY_LIMIT`, inserts next-tool preheat, writes RaiseTouch `;PRINTING_TIME:` / `;REMAINING_TIME:` immediately before each `;LAYER:N` (ideaMaker Tune clock) plus `;Print Time:` from PrusaSlicer `M73` and estimated-time comments, copies the slicer's `;HEIGHT:` to after `;LAYER:N` / `;Z:` (do **not** put `HEIGHT` in Before layer change G-code — PrusaSlicer reserved keyword), writes `;Bounding Box:` from print moves, then rejects unsafe G-code (a validator error aborts export). G-code thumbnails are off so a PNG block is not sitting in front of the header. On the printer, name the loaded slots `[Raise3D] PLA` (or `[Raise3D]` plus the material type) so Filament Status can go green. Hyper Speed may stay yellow: copying `;Sliced by ideaMaker` does not unlock that check.
2. Optional extra check vs ideaMaker:

```text
python scripts\compare_gcode.py reference\ideamaker\LeftonlyExtruder.gcode path\to\left-only.gcode
python scripts\compare_gcode.py reference\ideamaker\RightonlyExtruder.gcode path\to\right-only.gcode
python scripts\compare_gcode.py reference\ideamaker\MulticolorRaise3d.gcode path\to\dual.gcode
```

3. Read the first ~80 lines and the end sequence. Confirm `M99123` is line 1, `G28 X0 Y0` then `G28 Z0`, `M1001` / `M1002`, no `G29` / `M92` / `M218`. Left-only: heat T0, home T0, purge `X80 Y0`. Right-only: heat T1, home T1, same `X80 Y0` wipe. Dual: home T0, in-place `F200 E10` / `E-11`, then `G1 X80 Y0 F9000`. ideaMaker references still wipe to `X20`; the profile uses X80 so the fan clears the blob before Z drops. Single-tool end turns off only that tool plus bare `M104 S0`. Tool-change standby `S180`; wipe tower starts at X50 Y140 unless you moved it (this ideaMaker dual file used ~X50 Y241, not a slicer default). Validator rejects T1 print moves with X < 25 mm.
4. Stage 3: supervised first layer (home, heat, purge, Z height, fan, shutdown). Dual: watch the unused nozzle lift, T1 first motion, and the park/prime at tool-change.
5. Do not leave a long job unattended until Stages 3–4 pass. Dual color is Stage 7.

## Rollback

Use ideaMaker with the printer’s Hyper Speed template and USB export as before. Nothing in this repo is written to the printer’s firmware.

## Tests

```text
python -m unittest discover -s tests -v
```
