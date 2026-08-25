# Machine-behavior report

Sources of truth (ideaMaker 5.4.2.8790):

- `LeftonlyExtruder.gcode` — left `T0` only (2026-08-25)
- `RightonlyExtruder.gcode` — right `T1` only (2026-08-25)
- `MulticolorRaise3d.gcode` — dual / two-color `T0`+`T1` (2026-08-25)

Matching `.data` files are binary metadata only and were not modified.

Every item is labeled:

- **Confirmed** — present in this machine’s ideaMaker G-code
- **Supported by Raise3D documentation**
- **Community-derived starting point**
- **Assumption requiring physical testing**
- **Not implemented**

This profile is **experimental**. It is not production-ready.

## Printer and firmware

| Item | Value | Status |
| --- | --- | --- |
| Printer type comment | `RAISE3D Pro2 Plus - Hyper Speed` | Confirmed |
| Slicer | ideaMaker 5.4.2.8790 | Confirmed |
| Motion firmware comment | `Firmware: Klipper` | Confirmed |
| Hyper Speed mode marker | First line is `M99123` plus payload (same payload reported on the [Prusa forum Hyper Speed notes](https://forum.prusa3d.com/forum/prusaslicer/prusa-slicer-profile-for-raise3d-pro2-dual-head-printer/paged/2/)) | Confirmed in ideaMaker. PrusaSlicer profile disables G-code thumbnails and `scripts/ensure_m99123_first.py` moves `M99123` to line 1. **Green checkmark / touchscreen unlock is still Assumption requiring physical testing** |
| RaiseTouch version | Not present in G-code or `.data` text | Not implemented (unknown) |
| Files sliced in Hyper Speed mode | Yes: `M99123` present and printer type includes Hyper Speed | Confirmed |

## Tooling and filament in this file

| Item | Value | Status |
| --- | --- | --- |
| Nozzles in `;Dimension:` | `0.400 0.400` | Confirmed |
| Tools used | Left: `T0` only. Right: `T1` only. Dual: `T0` and `T1`, many swaps | Confirmed. Dual profile gates unused tools with `is_extruder_used` |
| Filament name | `[Raise3D] PLA` | Confirmed in ideaMaker. PrusaSlicer start G-code now emits the same `#1`/`#2` comments. Wizard preset remains Generic PLA. |
| Filament diameter | 1.75 mm | Confirmed |
| Filament compensation | 94% (`M221 T0 S94.00`) | Confirmed in ideaMaker. PrusaSlicer filament preset uses multiplier **1.00** (operator’s proven Prusa PLA). |
| First-layer nozzle / bed | `M109 T0 S230` / `M190 S60` | Confirmed in ideaMaker. PrusaSlicer preset is **215 °C first layer / 225 °C other / 60 °C bed** (operator’s proven Prusa PLA). |
| First layer height | 0.300 mm then 0.200 mm | Confirmed in ideaMaker. PrusaSlicer print family keeps **XL 0.20 mm** first layer (`skirts = 0`, first-layer speed 40 / infill 100). Start G-code already purges. |
| Copperhead hotends | Not mentioned in G-code | Assumption (operator-stated hardware) |
| PLA temps / flow / retract | ideaMaker 230 °C / 94% / 1.5 mm at F2400 | PrusaSlicer uses operator Prusa PLA: 215/225 °C, multiplier 1.00, retract still 1.5 mm / 40 mm/s. Dual standby remains 180 °C. |

## Geometry

| Item | Value | Status |
| --- | --- | --- |
| `;Dimension:` | `305.000 305.000 605.000 0.400 0.400` | Confirmed |
| Origin | `;Origin Center: 0` (corner origin) | Confirmed |
| Plate shape | `;Plate Shape: 0` | Confirmed |
| This print bounding box | Left: X 101.505–203.495, Y 91.316–213.451, Z 0–43.100. Dual: X 69.430–183.760, Y 49.015–308.595, Z 0–60.900 (wipe tower exceeds 305 mm Y) | Confirmed |
| Official Pro2 Plus volume | 305 × 305 × 605 mm | [Supported by Raise3D documentation](https://www.raise3d.com/pro2-series/) |
| T1 keep-out | Leftmost ~25 mm (factory right-nozzle X offset in firmware; slicer XY offset 0) | Assumption requiring physical testing. PrusaSlicer 2.9.6 has no per-tool printable polygon. Bundle uses bed texture + default wipe tower X50 Y140 + validator. |
| izumi 330 × 327.5 bed | Community Pro2 (not Plus), 2022 | Community-derived; **not used** |

## Special commands found

| Command | In this file | Notes |
| --- | --- | --- |
| `M99123` | Yes, line 1 | Hyper Speed header |
| `M1001` | Yes, after `M117 Printing...` | Start marker |
| `M1002` | Yes, in end sequence | End marker |
| `M2000` | No | Pause: community-derived only |
| `M600` | No | Community: does not work on this Klipper conversion |
| `M92` | No | Do not emit |
| `M218` | No | Do not emit |
| `G28` | `G28 X0 Y0` then `G28 Z0` at start; `G28 X0 Y0` at end | Confirmed |
| `G29` | No | Do not emit |
| `T0` | Left and dual files | Confirmed |
| `T1` | Right-only and dual files | Confirmed in `RightonlyExtruder.gcode` and `MulticolorRaise3d.gcode` |
| `G10` / `G11` | No | |
| `SET_VELOCITY_LIMIT` | `ACCEL=5000`, `ACCEL=2000`, `SQUARE_CORNER_VELOCITY=10` | Confirmed Klipper. `MulticolorRaise3d.gcode`: 5469×5000 and 5468×2000 (print vs travel). PrusaSlicer 2.9.6 emits `M204 S` instead; post-process converts to `SET_VELOCITY_LIMIT`. Print profiles: 2000 print / 5000 travel and first layer. |
| `M221` | Start `S94`, end `S100` | Confirmed |
| `M106` | `S0`, `S128`, `S255` | Confirmed; first layer fan off |

## Start sequence (complete, from this file)

See `tests/fixtures/ideamaker_left_start.gcode`, `tests/fixtures/ideamaker_right_start.gcode`, `tests/fixtures/ideamaker_dual_start.gcode`, and `docs/GCODE_MAPPING.md`.

Left file: heat **T0 only**, home X/Y then Z, raise Z to 15 mm, purge at origin → `X20 Y0`, `M1001`, then `SET_VELOCITY_LIMIT`.

Right file: heat **T1 only**, `T1` then the same home and `X20 Y0` wipe (not dual `E10`/`E-11`).

Dual file: heat **T0 and T1**, home on `T0`, then in-place prime (`T1` `E10`/`E-11` at `F200`, `T0` `E10` at `F200`), `M1001`, `M104 T1 S180`, then `SET_VELOCITY_LIMIT`. No `X20 Y0` wipe.

## End sequence (complete, from this file)

See `tests/fixtures/ideamaker_left_end.gcode`, `tests/fixtures/ideamaker_right_end.gcode`, and `tests/fixtures/ideamaker_dual_end.gcode`.

Left file: fan off, retract, Z hop, `M221 T0 S100`, `M1002`, heaters off (including bare `M104 S0`), relative retract/wipe, `G28 X0 Y0`, `M84`, `G90`.

Right file: same shape with `M221 T1` / `M104 T1 S0` / bare `M104 S0`.

Dual file: `M221` T0 and T1 `S100` twice around `M1002`, `M104 T0 S0` and `M104 T1 S0`, **no** bare `M104 S0`. Dual printer end G-code follows the matching ideaMaker file via `is_extruder_used`.

## Tool-change / pause / recovery

| Sequence | Status |
| --- | --- |
| Tool change | Confirmed in `MulticolorRaise3d.gcode`: park `X30 Y295`, retract 11 mm at `F1200`, standby `M104 T{prev} S180`, wait `M109 T{next} S230`, `T`, wipe-tower prime. Mid-print `M104 T{next} S230` before the swap (gaps 64–2200, median 762). No `M218`. Electronic lift is firmware. PrusaSlicer copies standby/`M109`; `ensure_m99123_first.py` inserts next-tool `M104` ~400 lines before `M109`. Wipe tower default X50 Y140; this ideaMaker file’s octagon is ~X50 Y241 |
| Pause / `M600` / `M2000` | Not present in this file |
| Recovery block | Present as **comments** after `;Data end` (`Recover start:29` … `Recover end`). Not executable G-code. **Not implemented** as PrusaSlicer custom G-code |

## Motion observed

| Item | Value | Status |
| --- | --- | --- |
| Travel | `F9000` (150 mm/s) | Confirmed. PrusaSlicer travel is 150 (XL IS uses 400; clipped to Hyper FFF L1 / this machine). |
| First-layer skirt | `F900` (15 mm/s) | Confirmed in ideaMaker. Print family does **not** copy this (XL first-layer 40/100, no skirt). |
| Later print moves | `F1500` 25 mm/s, `F2400` 40 mm/s, `F4500` 75 mm/s, `F6000` 100 mm/s, `F7200` 120 mm/s, `F9000` 150 mm/s (with E). Both ideaMaker files reach **150 mm/s** on print moves, not only 75. | Confirmed. PrusaSlicer SPEED is 150; STRUCTURAL is XL 80/45/120/140. Do not flatten SPEED to 75. |
| Retract | 1.5 mm at `F2400` (40 mm/s) | Confirmed |
| Absolute extruder | ideaMaker: `M82`. PrusaSlicer Dual profile: `M83` (wipe tower) | ideaMaker confirmed; PrusaSlicer **changed** |
| Print time comment | 8629 s (~2.4 h) | Confirmed — longer than the requested 20–30 min sample |

## Community zip files (not authoritative)

Stored under `reference/community/`. See `reference/SOURCE_CLASSIFICATION.md`.

These are 2022 **Marlin** PrusaSlicer profiles for pre-Hyper Speed Pro2/Pro2 Plus machines. They are starting points for bed comments and `M1001`/`M1002` only. Start/end G-code for this project is taken from the ideaMaker file, not from those zips.

## Uncertainties (do not silently resolve)

1. Whether copying `M99123` plus `;Printer Type: RAISE3D Pro2 Plus - Hyper Speed` produces the touchscreen Hyper Speed checkmark.
2. Printer slot names must still be `[Raise3D] PLA` (G-code now emits that; a renamed slot will still warn).
3. RaiseTouch firmware version.
4. Whether PrusaSlicer’s 2000/5000 `SET_VELOCITY_LIMIT` cadence (from converted `M204`) matches ideaMaker ringing. Klipper flavor cannot emit SET_VELOCITY_LIMIT natively.
5. Pause/resume (`M2000`) on this Hyper Speed firmware.
6. Right nozzle and dual-head lift: dual G-code confirmed; right-only G-code confirmed (`RightonlyExtruder.gcode`). Confirm firmware XY offset (do not also slice 25 mm). Dual purge is in-place `E10`/`E-11` at home. Right-only uses the same `X20 Y0` wipe as left after homing on T1. Keep T1 paths and the wipe tower off X < 25 mm; measure the real keep-out. Watch Stage 6–7 for collisions and ~25 mm shift.
7. Dual tool-change: PrusaSlicer wipe tower (default X50 Y140; you can drag) vs ideaMaker’s octagon at ~X50 Y241 in `MulticolorRaise3d.gcode`. Confirm the tower is where you put it and ooze does not hit the part.
8. Relative E (`M83`) vs ideaMaker `M82` — inspect first dual slice for mixed E mode.
9. Volumetric limit 15 mm³/s is Hyper FFF L1. Print temps are the operator’s Prusa PLA (215/225 °C, 1.00 flow). ideaMaker was 230 °C / 94%. Dual standby stays 180 °C; filament idle 70 °C is not emitted in tool-change G-code.
