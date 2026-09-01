G91                 	;Set to Relative Positioning
G1 S1 X500 F2500	;Move X rail to limit switch until pressed
G1 S2 X-3   F250   	;Back off X rail from limit switch a small amount
G1 S1 X10 F150   	;Move x rail to limit switch slowly
G90			;Absolute position