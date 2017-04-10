#!/usr/bin/env python
# For end=''
from __future__ import print_function


"""
  tm1638 driver module for the Onion Omega2.
  Ported by Pete Carr (petecarr <at> yahoo <dot> com) 4/2017
  Spec comes from www.titanmec.com/index.php/product/lists/typeid/59/p/3.html
  The device this software drives came from DealExtreme -
  8 7-segment led displays, 8 red-green leds and 8 buttons.


  The original of this software came from:
  "Copyright" (C) Oct 2012 Dan Oprescu (robotrandi <at> gmail <dot> com)
  It was written for the Stellaris Launchpad EK-LM4F120XL
  Now renamed the Tiva but nearly the same thing.
  Built with CCS Version 5.2.1

  Original was written in C++ and is under the following license
  -------------------------------------------------------------------------
  This program is free software: you can redistribute it and/or modify
  it under the terms of the version 3 GNU General Public License as
  published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  --------------------------------------------------------------------------
  On the other hand. On Arduino there is an obvious predecessor.
  https://github.com/rjbatista/tm1638-library/blob/master/TM16XX.cpp

  TM16XX.cpp - Library implementation for TM16XX.
  Copyright (C) 2011 Ricardo Batista (rjbatista <at> gmail <dot> com)
  Also on a GNU License.
  ---------------------------------------------------------------------------

  
  Looking at female connector at end of cable. Ground side has red dots.
     On tm1638 |  2 GND VCC 1 |
               |  4 DIO CLK 3 |
               |  6 ST1 ST0 5 |||  <-- Note protrusion on connector
               |  8 ST3 ST2 7 |
               | 10 ST5 ST4 9 |
   ST1 through ST5 are for daisy chaining further displays.
   3.3v appears to be adequate but the spec says the tm1638 chip wants 5.0+/-0.5 Volt.

"""
import time
import onionGpio
from tm1638_fonts import NUMBER_FONT, FONT_DEFAULT

ADDRSET = 0xC0                 # Command to set address 0x00
DATA_WRITE_INCR_ADDR = 0x40    # Command to switch TM1638 for automatic
                               # increment address mode
DATA_WRITE_FIX_ADDR = 0x44     # Command to switch TM1638 for fix address mode
DATA_READ_KEY_SCAN_MODE = 0x42 # Command for read key code from TM1638

LED_COLOR_NONE  = 0
LED_COLOR_GREEN = 1
LED_COLOR_RED   = 2

# Pins 0,1,18, VDD=5.0V, GND
STROBE_0 = 0
DIO      = 1
CLK      = 18

onVal = 1
offVal = 0


class TM1638:

    def __init__(self, clockPin, dataPin, strobePin, activateDisplay, intensity):
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.strobePin = strobePin
    
    
        #  all the pins are outputs
        self.gpioDataPin = onionGpio.OnionGpio(self.dataPin)
        status  = self.gpioDataPin.setOutputDirection(0)

        self.gpioClockPin = onionGpio.OnionGpio(self.clockPin)
        status  = self.gpioClockPin.setOutputDirection(0)

        self.gpioStrobePin = onionGpio.OnionGpio(self.strobePin)
        status  = self.gpioStrobePin.setOutputDirection(0)

        #  init them all in a known state
        status  = self.gpioClockPin.setValue(offVal)
        status  = self.gpioDataPin.setValue(offVal)
        status  = self.gpioStrobePin.setValue(offVal)
    
        #  send the init commands
        #print("send init")
        self.sendCommand(DATA_WRITE_INCR_ADDR)
        self.setupDisplay(activateDisplay, intensity)
    
        self.strobeSelect()
        self.send(ADDRSET)
        for i in range(0,16):
            self.send(0x00)
        
        self.strobeDeselect()
    
    
    
    def send(self, data):
        for i in range(0,8):
            status  = self.gpioClockPin.setValue(offVal)
            if data &1:
                dataBit = onVal
            else:
                dataBit = offVal
            status = self.gpioDataPin.setValue(dataBit)
            #time.sleep(0.00001)  # pc. I stuck these in to make the oscilloscope 
                                  # trace look less horrible
				  # however, python appears to be slow enough
            data >>= 1

            #time.sleep(0.00001)
	    # take data on rising edge of clock
            status  = self.gpioClockPin.setValue(onVal)
        
    
    def receive(self) :
        
        result = 0
    
        #  change the type of the data pin into an input
        status = self.gpioDataPin.setValue(onVal)
        status  = self.gpioDataPin.setInputDirection()
	#print("data input_value", status)
    
        #  start with the most significant bit
        for i in range(0,8):
        
            result >>= 1
            status = self.gpioClockPin.setValue(offVal)
            time.sleep(0.0001)  #  completely empirical value, but without a 
                        #  small break here it doesn't work. Probably 
                        #  the TM1638 chip needs some time after the 
                        #  clock edge to prepare the data...
    
            val = self.gpioDataPin.getValue()
            if val == 1:
                result |= 0x80
                print("received {0:s}".format(val))
    
            status = self.gpioClockPin.setValue(onVal)
            time.sleep(0.00001)

    
        #  put it back as output
        status = self.gpioDataPin.setOutputDirection(0)
        status = self.gpioDataPin.setValue(0x00)
    
        return result
    
    
    def sendCommand(self, cmd):
        self.strobeSelect()
        self.send(cmd)
        self.strobeDeselect()
    
    
    def sendData(self, address, data):
        self.sendCommand(DATA_WRITE_FIX_ADDR)
        self.strobeSelect()
        self.send(ADDRSET | address)
        self.send(data)
        self.strobeDeselect()
    
    
    def sendChar(self, pos, data, dot) :
        which_dot = 0
        if dot:
            which_dot = 0x80
        self.sendData(pos << 1, data | which_dot)
    
    
    def getButtons(self) :
        result = 0x00
    
        self.strobeSelect()
        self.send(DATA_READ_KEY_SCAN_MODE)
        #  we should wait to scan keys ready (see datasheet). 
        #  BUT it seems to work like this...
        time.sleep(0.000001)
        for i in range(0,4):
            result |= (self.receive() << i)
        self.strobeDeselect()
    
        return result
    
    
    
    def setupDisplay(self, active, intensity):
        if active : 
            activeBit = 8 
        else: 
            activeBit = 0
        self.sendCommand(0x80 | activeBit | min(7, intensity))
    
    
    def setDisplayDigit(self, digit, pos, dot):
        self.sendChar(pos, NUMBER_FONT[digit & 0xF], dot)
    
    
    def clearDisplayDigit(self, pos, dot) :
        self.sendChar(pos, 0, dot)
    
    
    def setDisplay(self, str, dots, pos):
        for i in range(0,8-pos):
            if (str[i] != '\0'):
                self.sendChar(i + pos, FONT_DEFAULT[ord(str[i]) - 32], 
    	                  (dots & (1 << (8 - i - 1))) != 0)
            else:
                break
            
    
    def clearDisplay(self) :
        for i in range(0,8):
            self.sendData(i << 1, 0x00)
        
    
    def setLED(self, pos, color) :
        self.sendData((pos << 1) + 1, color)
    
    
    
    def strobeSelect(self) :
        # strobe falls to indicate clk is driving data
        status = self.gpioStrobePin.setValue(0)
    
    
    def strobeDeselect(self) :
        # rises to tell chip to ignore clk
        status = self.gpioStrobePin.setValue(1)
    
    
