# Implementation plan (first pass)

Status: **experimental Dual bundle**. Dual start/tool-change/end now matched to `Multicolor.gcode`. Not production-ready. Physical Stage 6–7 still required.

## What this pass includes

1. Vendor bundle `vendor/Raise3D.ini` + `vendor/Raise3D.idx` for Configuration Wizard / local vendor drop-in. G-code thumbnails off; `scripts/ensure_m99123_first.py` puts `M99123` on line 1 after export.
2. Importable config bundle `profiles/Raise3D-Pro2Plus-HS-0.4-bundle.ini` (`File → Import → Import Config Bundle`).
3. Printer: Raise3D Pro2 Plus Hyper Speed 0.4 Dual. Unused tools skipped with `is_extruder_used`.
4. Filament: Generic PLA 1.75 mm. Temps from Prusa Generic PLA (210/215). Volumetric 15 mm³/s = Pro2 Hyper FFF L1. Assign to both slots.
5. Print: XL-style 0.4 mm family (0.10 FAST DETAIL, 0.15/0.20/0.25 SPEED and STRUCTURAL, 0.28 DRAFT). Default 0.20 mm SPEED. Motion clipped to Pro2 Hyper FFF L1 (150 mm/s, 5000 mm/s², 15 mm³/s). Travel 150 mm/s. Wipe tower on — PrusaSlicer places it; relative E / `M83` (ideaMaker used `M82`).
6. Left-only purge from `conradfreeman_filament_orange.gcode`. Dual start, standby tool-change, and end from `Multicolor.gcode`.
7. Tool-change standby 180 °C, `M109`, firmware XY offset (`extruder_offset = 0x0,0x0`). Wipe tower position/shape is not copied from ideaMaker.
8. G-code inspect / validate / compare scripts and fixtures.
9. README with install, Dual usage, assumptions, validation stages, and ideaMaker rollback.

## What this pass does not include

- ideaMaker right-only reference G-code
- Pause/runout recovery as a tested feature
- Hyper Speed PLA filament preset
- Claiming the Hyper Speed touchscreen checkmark works
- Expanding the bed beyond 305 × 305 × 605
- Slicer-applied 25 mm X offset (that lives in printer hardware)

## Source priority

1. This printer’s ideaMaker G-code (authoritative for start/end/headers/homing/purge).
2. Raise3D published specs (build volume, factory 25 mm right-nozzle X offset on the printer).
3. [Prusa forum Pro2 thread](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/) and the 2022 zip profiles — **community starting points only**, especially `M1001`/`M1002` and `;Dimension:` nozzle comments. Dual tool-change from those zips used Marlin `T… P0` / `M116` — **not copied**.
4. Generic Klipper/Prusa/Bambu examples — **not used** for machine G-code.

## Validation (do not skip)

| Stage | Action |
| --- | --- |
| 1 | Import bundle; confirm Dual printer / filament / print appear and are linked. |
| 2 | Slice a small left-only PLA test; run `scripts/validate_gcode.py` on the output; diff headers vs ideaMaker. |
| 3 | Supervised first-layer: homing, heat, purge, Z height, fan, shutdown. |
| 4 | Small calibration object vs ideaMaker baseline. |
| 5 | Pause / runout — only after 3–4 pass. |
| 6 | Right-only (object assigned to extruder 2): T0 home, T1 in-place `E10` prime, lift, first layer. |
| 7 | Dual color: 180 °C standby, lift, alignment (firmware offset), PrusaSlicer wipe tower where you placed it. Abort if nozzles collide, T1 is shifted ~25 mm, or purge lands on the part. |
