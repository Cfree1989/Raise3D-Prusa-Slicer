# Potterbot 9 machine behavior

Evidence for the PrusaSlicer bundle. Labels are from files in `reference/`.

## Controller

- Duet 2 WiFi, RepRapFirmware **2.04RC1** (2019-07-14). DWC screenshots in `reference/dwc/`.
- `config.g` names the machine **3DP-D9**. Absolute XYZ, **relative E** (`M83`), cold extrusion (`M302 P1`), bed heater off (`M140 H-1`).
- Drive limits: X 0–420, Y 0–360, Z 0–400. Home: X max, Y min, Z max. After `G28` the head is at **X420 Y0 Z400**.
- Max feed (mm/s): XY 100, Z 16.67, E 366.67. Accel XY/E 3000, Z 1000. `config.g` comment: keep slicer speeds ≤ 85 mm/s.
- `config.g.bak` is the same file with Z max 200 (older short-column setup).

## Official slicer settings

From `reference/cura/3D Potter Standard.3mf` (Cura machine) and the Cura 5.12 jobs:

| Setting | Value |
| --- | --- |
| Start | `G28` |
| End | `G91` / `G0 Z10 E-500 F1000` / `G90` / `G28` |
| Nozzle / line width | 5 mm / 5 mm (`wall_thickness = 5`) |
| Layer | 1.5 mm |
| Speeds | print 40, travel 80, bottom 20 mm/s |
| Skirt | 3 loops, 8 mm gap |
| Spiral vase | on |
| Infill / top | 0 / 0 |
| Retract during print | off |
| Temps / fan | 0 / off |
| Filament diameter | 1.75 mm (volumetric model for the ram) |

`no_bottom__layers.gcode` has `bottom_layers = 0`. `Bottom_Layers.gcode` has `bottom_layers = 3`. Both spiralize after the base.

Lab `Instructions.txt` says to match **line width** to the nozzle on the machine. It does not scale layer height with the tip. 3D Potter does not publish a layer-height-to-nozzle percentage. This bundle keeps **1.5 mm layer** on 2–10 mm nozzles and sets line width equal to the selected nozzle. The 1 mm tip is **0.8 mm layer** because PrusaSlicer rejects `extrusion_width <= layer_height` and also rejects first-layer height greater than nozzle diameter. Print profile names omit the layer height. Sparse infill is **grid**, solid bottoms are **concentric** with **Arachne** (classic concentric and Archimedean chords leave growing gaps on wide tips), and solid tops are **rectilinear**. Infill overlap is **15%** so bottoms meet the wall.

## Retraction

Official Cura **3D Potter Standard** stores `retraction_amount = 1000` / `retraction_speed = 1000` but sets `retraction_enable = False`. Known-good jobs never retract mid-print.

The [3D Potter FAQ](https://3dpotter.com/faq/) mid-print recipe (1000 mm at 1000 mm/s) exceeds `config.g` `M203 E22000` (367 mm/s) and is what stalled the ram motor in Cura.

This bundle puts retract on the **printer** (every print profile): relative `E-80` at 17 mm/s, Z-hop 5 mm (FAQ lift, not FAQ speed), extra prime 10 mm, only if travel ≥ 15 mm. Spiral vase walls do not travel, so they do not fire it. Skirt, bottoms, infill, and hops between objects do. End G-code is still `G0 Z10 E-500 F1000`. Experimental.

## Bed vs bat

Official Cura machine is **420 × 360 × 400** (firmware travel). The physical bat is **15×15″ (381 × 381 mm)**. This bundle uses **381 × 360 × 400** so the plater matches the bat and does not ask for Y past firmware travel.

## Macros (do not paste blindly)

- `reference/duet-macros/PRIME.gcode` — `G1 E100000 F30000` (charge the ram).
- `reference/duet-macros/RETRACT.gcode` — `G1 E-100000 F20000`.
- `reference/duet-macros/PRINT START LOCATION.gcode` — center of firmware travel (`X210 Y180`).
- `reference/firmware/macros/pause.g` — **homes** (`G28`). Not used as slicer pause (`M25` instead).
