# cs-prog-1-traffic
Assignment for my programming class to create a two-way traffic stop using a Raspberry Pi 4.

## GPIO Pin Setup

Pin numbers are given using the board numbering.

### Traffic light 1 (cars) - TL1

PIN 9  - GROUND  
PIN 11 - RED  
PIN 13 - YELLOW  
PIN 15 - GREEN


### Traffic light 2 (pedestrian) - TL2

PIN 9  - GROUND (NEG RAILS CONNECTED)  
PIN 16 - RED  
PIN 18 - GREEN  
PIN 22 - YELLOW (INDICATOR)

### Button - BTN

PIN 1  - BUTTON POS (3V3)  
PIN 10 - BUTTON STATE (RXD)  


## Cycle Descriptions

### TL1 Cycle

RED       - X s  
RED + YEL - X s  
GRN       - X s  
BLINK GRN - 4x 1+1 s  
YEL       - X s  
END

### TL2 Cycle

RED (persistent)  
Interrupt BTN  
IND ON  
WAIT TL1 END  
IND OFF  
GREEN + TL1 RED  
END