# Implementation plan (first pass)

Status: **left-extruder-only experimental bundle**. Not production-ready.

## What this pass includes

1. Vendor bundle `vendor/Raise3D.ini` + `vendor/Raise3D.idx` for Configuration Wizard / local vendor drop-in.
2. Importable config bundle `profiles/Raise3D-Pro2Plus-HS-Left-0.4-bundle.ini` (`File → Import → Import Config Bundle`).
3. Printer: Raise3D Pro2 Plus Hyper Speed, 0.4 mm, **left only**.
4. Filament: Overture PLA 1.75 mm (temps conservative; not copied from Hyper Speed Raise3D PLA).
5. Print: 0.20 mm L1 conservative.
6. Start/end G-code derived from `conradfreeman_filament_orange.gcode` as mapped in `docs/GCODE_MAPPING.md`.
7. G-code inspect / validate / compare scripts and fixtures.
8. README with install, assumptions, validation stages, and ideaMaker rollback.

## What this pass does not include

- Right extruder
- Dual extrusion / electronically lifting tool-change
- Pause/runout recovery as a tested feature
- Hyper Speed PLA filament preset
- Claiming the Hyper Speed touchscreen checkmark works
- Expanding the bed beyond 305 × 305 × 605

## Source priority

1. This printer’s ideaMaker G-code (authoritative for start/end/headers/homing/purge).
2. Raise3D published specs (build volume).
3. [Prusa forum Pro2 thread](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/) and the 2022 zip profiles — **community starting points only**, especially `M1001`/`M1002` and `;Dimension:` nozzle comments.
4. Generic Klipper/Prusa/Bambu examples — **not used** for machine G-code.

## Validation (do not skip)

| Stage | Action |
| --- | --- |
| 1 | Import bundle; confirm printer / filament / print appear and are linked. |
| 2 | Slice a small left-only PLA test; run `scripts/validate_gcode.py` on the output; diff headers vs ideaMaker. |
| 3 | Supervised first-layer: homing, heat, purge, Z height, fan, shutdown. |
| 4 | Small calibration object vs ideaMaker baseline. |
| 5 | Pause / runout — only after 3–4 pass. |
| 6–7 | Right then dual — blocked until left passes and matching ideaMaker G-code is supplied. |
