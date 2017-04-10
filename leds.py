#!/usr/bin/env python

""" 
Drive the tm1638 leds and the 7 segment displays
"""

import onionGpio
import time
from tm1638 import TM1638
from tm1638 import LED_COLOR_NONE, LED_COLOR_RED, LED_COLOR_GREEN, STROBE_0,DIO,CLK

# The 3 color LED on the expansion board
BLUE_LED = 15
GREEN_LED = 16
RED_LED = 17

def main():

    onVal = 0
    offVal = 1

    # The omega2 expansion board rgb leds

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


    segmentDisplay = TM1638(CLK, DIO, STROBE_0, True, 7)
    segmentDisplay.clearDisplay()
    for i in range(0,8):
        segmentDisplay.setLED(i, LED_COLOR_NONE)

    led = 0
    while (True) :
        if led > 255:
	    led = 0
        try:
	    """ onionGpio.setValue is kind of slow so I commented these out
            status = gpioObjRed.setValue(offVal)
            status = gpioObjGreen.setValue(offVal)
            status = gpioObjBlue.setValue(offVal)
	    if led & 1:
                status = gpioObjRed.setValue(onVal)
	    if led&2:
                status = gpioObjGreen.setValue(onVal)
	    if led&4:
                status = gpioObjBlue.setValue(onVal)
            """

	    j = led&7
	    for i in range(7,-1,-1):
	        k = 7-i
	        if led & (1<<i):
		    #print(i," goes red")
                    segmentDisplay.setLED(k, LED_COLOR_RED)
                    segmentDisplay.setDisplayDigit(k, k, 0)
                else :
		    #print(i," goes green")
                    segmentDisplay.setLED(k, LED_COLOR_GREEN)
                    segmentDisplay.clearDisplayDigit(k, 0)
                
        except KeyboardInterrupt:
	    # I have a script to clear up any Resource Busy problems.
	    # It outputs error messages but appears to work
	    """
	    echo 18 > /sys/class/gpio/unexport
	    echo 0 > /sys/class/gpio/unexport
	    echo 1 > /sys/class/gpio/unexport
	    """
	    
            print("Keyboard interrupt, exiting")
            status = gpioObjBlue.setValue(offVal)
            quit()
        led += 1
        

main()
