;3DP-9 4/16/2019 3D Potter
;Z-gear box = I20

M111 S0                            		; Debug off
M550 P3DP-D9					; Machine name and Netbios name (can be anything you like)
;M551 P12345678                   		; Machine password (used for FTP)

;*** If you have more than one Duet on your network, they must all have different MAC addresses, so change the last digits
;networking
M540 P0xBE:0xEF:0xDE:0xAD:0xFE:0xED		; MAC Address
M552 S2   					; start wifi S2 OR S1 network

;Settings
M555 P2						; Set output to look like Marlin
G21						; Work in mm
G90						; Set to Absolute Positioning
M83						; ...but relative extruder moves

;Motor Direction
M584 X5 Y6 Z2 E3			; Set drive mapping  Axis and motor configuration                                                
M569 P5 S0 R0 T4			; Drive 5 goes forwards X
M569 P6 S0 R0 T4			; Drive 6 goes forwards Y
M569 P2 S0 R0 T4 D2			; Drive 2 goes forwards Z
M569 P3 S1 R0 T4 D2			; Drive 3 goes forwards E

;Motor Ranges				        
M574 X2 Y1 Z2 S0 			; Endstop configuration				                         	
M208 X420 Y360 Z400			; set axis maxima and high homing switch positions (adjust to suit your machine)
M208 S1 X0 Y0 Z0 S1 			; set axis minima and low homing switch positions (adjust to make X=0 and Y=0 the edges of the bed)

;Motor Speeds
M92 X71 Y71 Z1458			; Steps/mm for X Y Z
M92 E70                   		; Steps/mm for E 
M350 X1 Y1 Z16 E16 I1			; Set 1x microstepping with interpolation
M906 X0 Y0 Z1500 E2500 I30		; Set motor currents (mA) and increase idle current to 30%
M201 X3000 Y3000 Z1000 E3000		; Accelerations (mm/s^2)                        
M203 X6000 Y6000 Z1000 E22000		; Maximum speeds (mm/min). E5000 = ~87mm/s. Maximum of 85mm/s in slicing program is recommended.
M566 X3000 Y3000 Z1000 E3000  		; Maximum instant speed changes mm/minute     

; Tool definitions
M563 P0 D0          			; Define or remove a tool
G10 P1         				; Set tool number 1
T0					; Select tool 0	
M140 H-1				; Bed Off

; Misc
M83 					; Set extruder to relative mode
M302 P1                  		; Allow cold extrusion