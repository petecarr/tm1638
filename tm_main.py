#!/usr/bin/env python

""" 
    Drive the DealExtreme led display which is based on titanmec's tm1638 chip.
"""

import onionGpio
import time
from tm1638 import TM1638
from tm1638 import LED_COLOR_NONE, LED_COLOR_RED, LED_COLOR_GREEN, STROBE_0,DIO,CLK


# The 3 color LED on the expansion board
BLUE_LED = 15
GREEN_LED = 16
RED_LED = 17

onVal = 0
offVal = 1

def main():

    # Blue
    gpioObjBlue = onionGpio.OnionGpio(BLUE_LED)
    status  = gpioObjBlue.setOutputDirection(0)
    status  = gpioObjBlue.setValue(offVal)

    # Green
    gpioObjGreen = onionGpio.OnionGpio(GREEN_LED)
    status  = gpioObjGreen.setOutputDirection(0)
    status  = gpioObjGreen.setValue(offVal)

    # Red
    gpioObjRed = onionGpio.OnionGpio(RED_LED)
    status  = gpioObjRed.setOutputDirection(0)
    status  = gpioObjRed.setValue(offVal)


    #print("Call segmentDisplay")
    segmentDisplay = TM1638(CLK, DIO, STROBE_0, True, 7)


    buttons = 0
    while (True) :
        try:
            buttons = segmentDisplay.getButtons()
    	    print("buttons = ", buttons)
            if(buttons == 1):
                status = gpioObjRed.setValue(onVal)
                status = gpioObjGreen.setValue(offVal)
                status = gpioObjBlue.setValue(offVal)
    
                for i in range(0,8):
                    segmentDisplay.clearDisplay()
                    segmentDisplay.setDisplay("HELLO W", 0x00, i)
                    time.sleep(1.0)
    		i += 1
                
            elif (buttons != 0x00):
                status = gpioObjGreen.setValue(onVal)
                status = gpioObjRed.setValue(offVal)
                status = gpioObjBlue.setValue(offVal)
    
                segmentDisplay.clearDisplay()
    
                for i in range(0,8):
                    if(buttons & 1):
                        segmentDisplay.setLED(i, LED_COLOR_RED)
                        segmentDisplay.setDisplayDigit(i, i, 1)
                    else :
                        segmentDisplay.setLED(i, LED_COLOR_GREEN)
                    
    
                    #  go the the bit for the next button
                    buttons >>= 1
                
            else :
                status = gpioObjBlue.setValue(onVal)
                status = gpioObjGreen.setValue(offVal)
                status = gpioObjRed.setValue(offVal)
    
                segmentDisplay.setDisplay("ABCDEFGH", 0, 0)
                for i in range(0,8,2):
                    segmentDisplay.setLED(i, LED_COLOR_GREEN)
                for i in range(1,8,2):
                    segmentDisplay.setLED(i, LED_COLOR_RED)
        except KeyboardInterrupt:
            print("Keyboard interrupt, exiting")
            status = gpioObjBlue.setValue(offVal)
	    quit()
        

main()
