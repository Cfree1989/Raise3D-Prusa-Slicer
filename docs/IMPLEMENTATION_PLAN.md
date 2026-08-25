# Implementation plan (first pass)

Status: **experimental Dual bundle**. Not production-ready. Dual has no ideaMaker dual-file confirmation yet.

## What this pass includes

1. Vendor bundle `vendor/Raise3D.ini` + `vendor/Raise3D.idx` for Configuration Wizard / local vendor drop-in.
2. Importable config bundle `profiles/Raise3D-Pro2Plus-HS-0.4-bundle.ini` (`File → Import → Import Config Bundle`).
3. Printer: Raise3D Pro2 Plus Hyper Speed 0.4 Dual. Unused tools skipped with `is_extruder_used`.
4. Filament: PLA 1.75 mm. Temps from Prusa generic PLA (210/215). Volumetric 15 mm³/s = Pro2 Hyper FFF L1, not Hyper Speed PLA marketing. Assign to both slots.
5. Print: 0.20 mm SPEED. Prusa XL IS 0.20 SPEED layout, motion clipped to Pro2 Hyper FFF L1 (150 mm/s, 5000 mm/s², 15 mm³/s). Travel 150 mm/s. Wipe tower off — requires relative E; this printer uses ideaMaker M82.
6. Start/end G-code derived from `conradfreeman_filament_orange.gcode` as mapped in `docs/GCODE_MAPPING.md`, with T1 heat/purge gated.
7. Tool-change `M104` standby + `M109`, firmware XY offset (`extruder_offset = 0x0,0x0`).
8. G-code inspect / validate / compare scripts and fixtures.
9. README with install, Dual usage, assumptions, validation stages, and ideaMaker rollback.

## What this pass does not include

- ideaMaker dual / right-only reference G-code (still missing)
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
| 6 | Right-only (object assigned to extruder 2): T0 home, T1 purge at X40 Y0, lift, first layer. |
| 7 | Dual color: tool-change lift, standby temp, alignment (firmware offset). Abort if nozzles collide or T1 is shifted ~25 mm. |
