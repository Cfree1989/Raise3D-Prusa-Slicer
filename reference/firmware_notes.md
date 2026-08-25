# Firmware / slicer notes from supplied files

## Confirmed from ideaMaker G-code

- ideaMaker **5.4.2.8790**
- `;Printer Type: RAISE3D Pro2 Plus - Hyper Speed`
- `;Firmware: Klipper`
- Hyper Speed marker: `M99123` on line 1
- `;Dimension: 305.000 305.000 605.000 0.400 0.400`

## Dual (experimental)

- Two nozzles: `nozzle_diameter = 0.4,0.4`
- Slicer `extruder_offset = 0x0,0x0` (printer hardware holds ~25 mm X)
- Tool change: `T0` / `T1` (electronic lift in firmware) plus `M109` wait
- Do not emit `M218`, `M116`, or Marlin `T… P0`

## Not present in supplied files

- RaiseTouch version
- ideaMaker Hyper Speed template export
- Screenshots of the selected printer / filament / template
- PLA ideaMaker slice (present: `[Raise3D] PLA` at 230 °C / 94% flow). PrusaSlicer Generic PLA uses the operator’s proven 215/225 °C and 1.00 multiplier.

Add screenshots or notes here when available.
