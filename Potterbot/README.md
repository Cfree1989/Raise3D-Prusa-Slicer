# Potterbot 9

3D Potterbot 9, Duet 2 WiFi, RepRapFirmware **2.04RC1** (2019-07-14). Axis limits from the board: **420 × 360 × 400 mm**. Physical bat is **15×15″** (about 381 × 381 mm), which is smaller than X travel and a bit larger than Y travel.

No PrusaSlicer profile yet. This folder is the source material:

- `Slicer Settings/Cura/3D Potter Standard.3mf` — official Cura project for Model 9 / Pro 9 / Super 9
- `Test Vase Standard.gcode` / `Test Cylinder Standard.gcode` — known-good Simplify3D output
- `PRINT START LOCATION.gcode`, `PRIME.gcode`, `RETRACT.gcode` — Duet macros
- `Instructions.txt` — Cura / Simplify3D / DWC workflow

When a bundle is added it should live in `profiles/` and `vendor/` here, same pattern as [Raise3D](../Raise3D/README.md).
