G91                 	;Set to Relative Positioning
G1 S1 Y-500 F2500	;Move Y rail to limit switch until pressed
G1 S2 Y3   F250   	;Back off Y rail from limit switch a small amount
G1 S1 Y-10 F150   	;Move Y rail to limit switch slowly
G90			;Absolute position