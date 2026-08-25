# Classification of supplied files

## Authoritative (this machine)

| File | Role |
| --- | --- |
| `ideamaker/conradfreeman_filament_orange.gcode` | Known-good Hyper Speed ideaMaker output, left nozzle, PLA |
| `ideamaker/conradfreeman_filament_orange.data` | ideaMaker metadata; inspect only, do not modify |
| `ideamaker/Multicolor.gcode` | Known-good Hyper Speed ideaMaker dual / two-color output, T0+T1, PLA |
| `ideamaker/Multicolor.data` | ideaMaker metadata; inspect only, do not modify |

## Community-derived (not Hyper Speed evidence)

From [Prusa Slicer Profile for Raise3D Pro2 dual head printer](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/).

| Zip | Author / date | What it is | Do not copy blindly |
| --- | --- | --- | --- |
| `Raise3D-PRO2-Plus.zip` | rmeister, Jan 2022 | PrusaSlicer 2.4 single config: left-only and dual-head, **0.6 mm**, PETG, `gcode_flavor = marlin`, `pause_print_gcode = M601`, printer_model leftover `MK3S` | Marlin, wrong nozzle, PETG, pre-Hyper Speed |
| `RaisePro2_v1_2202.02.18_PrusaSlicer_config_bundle.zip` | izumi5188, 2022-02-18 | Left-extruder Pro2 (300 mm Z) Marlin bundle | Pro2 not Plus; expanded bed; Marlin |
| `RaisePro2_v1.1_2202.02.25_PrusaSlicer_config-izumi5188.zip` | izumi5188, 2022-02-25 | Dual Pro2 Marlin bundle, `M2000` pause, `M1001`/`M1002` added | Dual/toolchange unverified on Hyper Speed Klipper |

Useful community facts (still not a substitute for ideaMaker):

- RaiseTouch may parse `;Dimension: … 0.400 0.400` for nozzle matching.
- `;Filament Name #1:` must match the name loaded on the printer.
- Hyper Speed firmware is Klipper; 2022 Marlin profiles are outdated for this conversion.
- `M600` is reported not to work; `M2000` is the community pause command.

## Missing evidence

- Short 20–30 minute PLA ideaMaker file
- ideaMaker printer/filament/template exports
- RaiseTouch version screenshot
- Right-nozzle-only ideaMaker G-code
- Pause / runout reference file
- Measured PLA flow, temp, and volumetric-speed results
