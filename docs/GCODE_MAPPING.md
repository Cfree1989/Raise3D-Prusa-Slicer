# Start / end G-code mapping

Required before treating any PrusaSlicer G-code as final.

Source: `conradfreeman_filament_orange.gcode` (ideaMaker 5.4.2.8790).
Proposed output lives in `vendor/Raise3D.ini` printer start/end G-code.

This mapping is **experimental**. Physical Stage 2–3 tests are still required.

## Start G-code

| ideaMaker (source) | PrusaSlicer equivalent | Action | Reason |
| --- | --- | --- | --- |
| `M99123 /RKIIyAfrg…` (line 1) | Same payload, copied from this file | Copied | Confirmed Hyper Speed header on this machine. Forum reports pasting it does not always produce a green checkmark — **physical test required**. |
| `;Sliced by ideaMaker 5.4.2.8790…` | Omitted | Omitted | Lying about the slicer did not clear warnings in [MackDan’s Hyper Speed notes](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/paged/2/). |
| `;Dimension: 305.000 305.000 605.000 0.400 0.400` | Same comment | Copied | Community: Raise3D Klipper reads this for nozzle-diameter check. Also matches this file. |
| `;Plate Shape: 0` / `;Origin Center: 0` / `;Extruder Offset #1: 0.000 0.000` | Same | Copied | Present in known-good header. |
| `;Filament Name #1: [Raise3D] PLA` | `;Filament Name #1: Overture PLA` (filament G-code) | Changed | This sample is Raise3D PLA. Target filament is Overture PLA. **Must exactly match the name loaded on the printer** or the touchscreen filament warning appears (community). |
| `;Filament Diameter/Type/#` comments | Emitted from filament start G-code with placeholders | Copied (values parameterized) | Header metadata used by RaiseTouch. |
| `;Printer Type: RAISE3D Pro2 Plus - Hyper Speed` | Same | Copied | Confirmed in this file. |
| `;Firmware: Klipper` | Same | Copied | Confirmed in this file. |
| `;Bounding Box:…` | Omitted | Omitted | Per-print metadata; PrusaSlicer cannot know it at start. |
| `M221 T0 S94.00` | `M221 T0 S{extrusion_multiplier[0]*100}` | Changed | 94% is Raise3D PLA compensation, not an Overture measurement. Default multiplier 1.00 until calibrated. |
| `M140 S60` / `M104 T0 S230` / `M109 T0 S230` / `T0` / `M190 S60` | Same commands with `{first_layer_bed_temperature[0]}` and `{first_layer_temperature[0]}` | Copied structure; temps parameterized | Heat **T0 only**, matching this left-only file. Do not heat T1 (MackDan community advice not used here because this file does not). |
| `G21` `G90` `M82` `M107` | Same | Copied | Units, absolute XYZ, absolute E, fan off. |
| `G28 X0 Y0` then `G28 Z0` | Same | Copied | Do not replace with `G28` or add `G29`. |
| `G1 Z15.0 F300` | Same | Copied | Clearance before purge. |
| `G92 E0` / `G1 F140 E29` / `G1 X20 Y0 F140 E30` / `G92 E0` | Same | Copied | Exact purge from this machine. Community X5 Y5 purge lines were **not** used. |
| `G1 F9000.0` / `M117 Printing...` / `M1001` | Same | Copied | Travel feed + start marker. |
| `SET_VELOCITY_LIMIT ACCEL=5000.00` and `SQUARE_CORNER_VELOCITY=10.00` | Same, once after `M1001` | Copied initial values | ideaMaker later switches ACCEL 2000/5000 during the print. Per-feature switching is **not replicated** (Assumption / physical test). |
| `G29`, `M92`, `M218`, `M600`, `PRINT_START` macros | — | Omitted | Not in this file. Generic Klipper macros are not authoritative. |

## End G-code

ideaMaker emits a slicer-generated retract/Z-hop (`G1 F2400 E…`, `G0 F300 Z…`) then custom end. PrusaSlicer will emit its own retract before custom end G-code. Custom end starts at `M221`:

| ideaMaker (source) | PrusaSlicer equivalent | Action | Reason |
| --- | --- | --- | --- |
| `M221 T0 S100` / `G92 E0` / `M1002` | Same | Copied | Reset flow + end marker. |
| `M104 T0 S0` / `M221 T0 S100` / `M104 S0` / `M140 S0` / `M107` | Same | Copied | Duplicate heater-off matches this file. |
| `G91` / `G1 E-1 F300` / `G1 Z+0.5 E-5 X-20 Y-20 F9000.00` | Same | Copied | Relative retract and wipe. |
| `G28 X0 Y0` / `M84` / `G90` | Same | Copied | Home XY, disable steppers, restore absolute. |
| Raise Z to `max_layer_z+5` (izumi) | Omitted | Omitted | Not in this ideaMaker end. Relative `Z+0.5` is what the machine file does. |

## Uncertain commands — required physical tests

| Uncertainty | Test |
| --- | --- |
| `M99123` payload copied from this file | Stage 2–3: note whether Hyper Speed checkmark appears; abort if the printer refuses the file. |
| `;Filament Name #1: Overture PLA` | Stage 2: confirm it matches the name on the touchscreen filament slot. |
| T0-only preheat (no T1) | Stage 3: confirm left nozzle lifts/prints without forcing a T1 heat. |
| Purge blob at homed origin then `X20 Y0` | Stage 3: watch first motion; confirm no bed crash and purge is on the plate, not on the clip. |
| `SET_VELOCITY_LIMIT ACCEL=5000` without later 2000 drops | Stage 4: compare ringing to the ideaMaker baseline. |
| `M2000` pause (community, not in this file) | Stage 5 only; do not use on a long print first. |
| Absolute E (`M82`) under PrusaSlicer Klipper flavor | Stage 2: inspect G-code for mixed relative/absolute E. |

## Commands remaining Not implemented

- Right-extruder start, `T1`, dual tool-change, nozzle lift
- Pause/filament-runout recovery beyond documenting `M2000` as community
- ideaMaker `;Data start` / recover comment block
- Hyper Speed PLA material profile
- `G29` mesh, `M92` steps, `M218` offsets
