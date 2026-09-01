Raise3D Pro2 Printer Profile for Prusa Slicer
Developed on Prusa Slicer 2.4.0
To upload, use the Import->Import Config

Last Release 2022.02.25
Caution::Use at your own risk. 
I expanded the print size beyond what Raise3D says the Pro2 fits from my own testing on my machine.
I TEST my full bed print to confirm using PrusaSlicer. 295x295 with a 5mm brim and 1 skirt loop that 
is 2mm offset from the brim and it ran literally down the left and right sides when using the 
extruders seperately.  Dual color would need to fit inside the two squares on the mat including 
using the primarys brim and skirt. Along with making sure all color extruder changes fit.

You'll need to update both the attached print settings and filament settings. These will need to be 
calibrated to your machines and filaments. They are currently set with dependencys to this profile.

Release 2022.02.22 - Dual Extruder 
Release Notes
Changed Gcode Flavor to Marlin (legacy)
Added Build Plate STL to plater view, confirmed the safe zones of the left(white) and right(gold) squares.
Added missing M1001 and M1002 commands to start up and end gcode
Added filalment flowrate/extrusion multiplier M221 commands

You'll need to manual adjust your extruder offsets on the extruder.
If you want your purge line to match with your offsets, you'll need to adjust your startup
gcode to match. There currently isn't a way to use the stored values with arthmatic. 

Added max layery z test to raise nozzle 5mm before moving to home at the end of the print

Added Gcode around Dual Extruders from @rmeister shared profile

Added Color Change (Template Custom Code)
Semi seems to work. It moves the extruder to 'home', and retracts filament for you to swap, and reload using
the Pro2s screen. However, upon restart, the extruder appears to miss a whole layer. Not sure what is going on.
M2000, in general appears to work. Not sure what I missed.


-----------------------------------------------------------------
Release 2022.02.18 - Single Left Extruder
Release Notes
I attempted to port over settings I used in Ideamaker for my Raise3D Pro2
Currently on configured for the left extruder.

Platter overlay has anticipated safezones for the left and right extruders.  Each square is 305x305mm.
Testing my bed with different sizes in Ideamaker I came to the conclusion that the full bed appears to 
have an opperational size of 330mm x 327.50mm
Outside of the safezone is an extra 5mm of space for brim, skirt and raft material. That way you can eye
up location of parts and still add these without having to rearrange. On top of that there is an additional
2.5mm of play because I use a megnatic WamBam plate and don't always get it perfectly back on.
The safe zones are also 13.75mm from Y0 to allow that 5mm of gap between the print and purge lines
in the start up Gcode.

Custom Gcode:
Starting Gcode Starts to heat bed to 100% and left nozzle to 80% initially.
Waits for left nozzle and then begins the homing sequence.
Proceeds to wait for temperatures to hit first layer values before printing a 75mm purge line at X5 Y5

Set Pause to M2000. According to the internt that is the correct value for Raise3D printers. This is untested.

Don't remove the following keywords! These keywords are used in the "compatible printer" condition of the print 
and filament profiles to link the particular print and filament profiles to this printer profile.
PRINTER_VENDOR_RAISE3D
PRINTER_MODEL_PRO2





