# Classification of supplied files

## Authoritative (this machine)

| File | Role |
| --- | --- |
| `ideamaker/LeftonlyExtruder.gcode` | Known-good Hyper Speed ideaMaker output, left nozzle, PLA |
| `ideamaker/LeftonlyExtruder.data` | ideaMaker metadata; inspect only, do not modify |
| `ideamaker/RightonlyExtruder.gcode` | Known-good Hyper Speed ideaMaker output, right nozzle, PLA |
| `ideamaker/RightonlyExtruder.data` | ideaMaker metadata; inspect only, do not modify |
| `ideamaker/MulticolorRaise3d.gcode` | Known-good Hyper Speed ideaMaker dual / two-color output, T0+T1, PLA |
| `ideamaker/Multicolor.data` | ideaMaker metadata; inspect only, do not modify |

## Additional ideaMaker (not used for start/end)

| File | Role |
| --- | --- |
| `ideamaker/IdeaMakerTest.gcode` + `.data` | Later ideaMaker slice of the same test model as `prusaslicer/Raise3DTest_…` |

## This profile’s exports (not start/end evidence)

| File | Role |
| --- | --- |
| `prusaslicer/Raise3DTest_0.4n_0.2mm_PLA_PRO2PLUS_HS_DUAL_3h2m.gcode` | Current Dual profile export (2026-09-02) |
| `prusaslicer/proj_1_0.4n_0.2mm_PLA_PRO2PLUS_HS_DUAL_3h16m.gcode` | Earlier Dual-profile export |
| `prusaslicer/RaiseMulticolor_1_0.4n_0.2mm_PLA,PLA_PRO2PLUS_HS_DUAL_4h10m.gcode` | Earlier dual-color Dual-profile export |
| `prusaslicer/Dualcolorsupportj_1_0.4n_0.2mm_PLA,PLA_PRO2PLUS_HS_DUAL_4h8m.gcode` | Earlier dual-color + support Dual-profile export |

## Prusa XL comparison (not machine evidence)

| File | Role |
| --- | --- |
| `prusa-xl/PrusaXLTest_0.4n_0.2mm_PLA_XLIS_2h29m.bgcode` | Same test model on XL IS |
| `prusa-xl/PrusaMulticolor_1_0.4n_0.2mm_PLA,PLA_XLIS_4h0m.bgcode` | Dual-color XL IS comparison |

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
- Pause / runout reference file
- Measured PLA flow, temp, and volumetric-speed results
