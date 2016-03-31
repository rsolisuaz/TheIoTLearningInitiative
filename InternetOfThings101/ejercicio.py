#!/usr/bin/python

import signal
import sys

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import pyupm_i2clcd as lcd

def interruptHandler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':
   signal.signal(signal.SIGINT, interruptHandler)

   touch = ttp223.TTP223(6)
   myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
   button = grove.GroveButton(8)

   count = 0
   myLcd.setColor(0,0,255)

   # Read the input and print, waiting one second between readings
   while 1:
      if button.value():
         count=count+1
      if touch.isPressed():
         count=count-1
      myLcd.setCursor(0,0)
      myLcd.write('%6d'% count)
      time.sleep(0.01)

   del button
   del touch


