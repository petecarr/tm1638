# tm1638
tm1638 driver module for the Onion Omega2.
  Ported by Pete Carr (petecarr <at> yahoo <dot> com) 4/2017
  Spec comes from www.titanmec.com/index.php/product/lists/typeid/59/p/3.html
  The device this software drives came from DealExtreme -
  8 7-segment led displays, 8 red-green leds and 8 buttons.

  ------------------------------------------------------------------------
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
   
   Strobe (ST0)  is connected to gpio 0
   Data IO (DIO) is connected to gpio 1
   Clock (CLK) is connected to gpio 18
 
