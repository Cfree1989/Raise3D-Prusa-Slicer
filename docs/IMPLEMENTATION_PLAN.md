# Implementation plan (first pass)

Status: **experimental Dual bundle**. Dual start/tool-change/end matched to `MulticolorRaise3d.gcode`. Not production-ready. Physical Stage 6–7 still required.

## What this pass includes

1. Vendor bundle `vendor/Raise3D.ini` + `vendor/Raise3D.idx` for Configuration Wizard / local vendor drop-in. G-code thumbnails off; print `post_process` runs `C:\Windows\py.exe -3` (latest Python 3) on `scripts/ensure_m99123_first.py` then `scripts/validate_gcode.py` (M99123 on line 1, `M204 S` → `SET_VELOCITY_LIMIT`, next-tool `M104` before swap `M109`).
2. Importable config bundle `profiles/Raise3D-Pro2Plus-HS-0.4-bundle.ini` (`File → Import → Import Config Bundle`).
3. Printer: Raise3D Pro2 Plus Hyper Speed 0.4 Dual. Unused tools skipped with `is_extruder_used`.
4. Filament: PLA / PETG / TPU / ASA / PA-CF / ABS-GF Raise3D (G-code name `[Raise3D] ` + `filament_type`). Temps from the operator’s matching `* XL` user presets. PLA also matches the proven Prusa PLA. Dual standby 180 °C. Volumetric 15 mm³/s except TPU 4. Compatible only with this Dual 0.4 printer.
5. Print: XL-style 0.4 mm family (0.10 FAST DETAIL, 0.15/0.20/0.25 SPEED and STRUCTURAL, 0.28 DRAFT). Default 0.20 mm SPEED. Motion clipped to Pro2 Hyper FFF L1 (150 mm/s, 5000 mm/s², 15 mm³/s). Travel 150 mm/s. Accel: print 2000 / travel and first layer 5000 (ideaMaker). `ensure_m99123_first.py` converts `M204 S` to `SET_VELOCITY_LIMIT`. Wipe tower on — default X50 Y140 (past T1 keep-out); relative E / `M83` (ideaMaker used `M82`).
6. Left-only from `LeftonlyExtruder.gcode`. Right-only from `RightonlyExtruder.gcode` (T1 home + same `X80 Y0` wipe). Dual start, standby tool-change, and dual end from `MulticolorRaise3d.gcode`; dual adds `G1 X80 Y0 F9000` at Z15 after in-place prime. Single-tool end matches the matching ideaMaker file.
7. Tool-change standby 180 °C, `M109`, firmware XY offset (`extruder_offset = 0x0,0x0`). T1 keep-out: bed texture + validator; not a slicer XY offset. Next-tool `M104` via `ensure_m99123_first.py` (~400 lines before swap).
8. G-code inspect / validate / compare scripts and fixtures.
9. README with install, Dual usage, assumptions, validation stages, and ideaMaker rollback.

## What this pass does not include

- Pause/runout recovery as a tested feature
- Hyper Speed PLA filament preset
- Claiming the Hyper Speed touchscreen checkmark works
- Expanding the bed beyond 305 × 305 × 605
- Slicer-applied 25 mm X offset (that lives in printer hardware)
- Per-tool printable area (`extruder_printable_area` is Orca/Bambu, not PrusaSlicer 2.9.6)
- ideaMaker first layer 0.30 mm, skirt, and 15 mm/s first-layer feed (print family stays XL: 0.20 mm, no skirt, 40/100 mm/s)
- Flattening SPEED to 75 mm/s (keep XL SPEED/STRUCTURAL split; Hyper FFF L1 is 150 mm/s and 15 mm³/s)

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
| 6 | Right-only (object assigned to extruder 2): heat T1 only, home on T1, same `X80 Y0` wipe as left (not dual `E10`). Lift, first layer, keep-out. |
| 7 | Dual color: 180 °C standby, lift, alignment (firmware offset), wipe tower (default X50 Y140). Abort if nozzles collide, T1 is shifted ~25 mm, or purge lands on the part. |
