;Home All
G91                 	;Set to Relative Positioning
G1 S1 Z600 F1000	;Move Z rail to limit switch until pressed
G1 S2 Z-3 F250   	;Back off Z rail from limit switch a small amount
G1 S1 Z10 F150   	;Move Z rail to limit switch slowly
G90			;Absolute position

G91                 	;Set to Relative Positioning
G1 S1 X500 Y-500 F2500	;Move X and Y rail to limit switch until pressed
G1 S2 X-3 Y3 F250   	;Back off X and Y rail from limit switch a small amount
G1 S1 X10 Y-10 F150   	;Move X and Y rail to limit switch slowly
G90			;Absolute position


