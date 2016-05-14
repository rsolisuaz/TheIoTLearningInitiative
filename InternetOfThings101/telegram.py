#!/usr/bin/python

import signal
import sys

import time
import pyupm_grove as grove
import pyupm_i2clcd as lcd
import ConfigParser
import telebot


def interruptHandler(signal, frame):
    sys.exit(0)

class TelegramBot():
    def __init__(self):
       self.configuration = ConfigParser.ConfigParser()
       self.configuration.read("configuration/services.config")
       self.token = self.configuration.get("telegram","token")
       self.mybot = telebot.TeleBot(self.token)

    def listener(self, message):
       for m in message:
           chatid = m.chat.id
           if m.content_type == "text":
              text = ascii.ignore(m.text)
              if m.text == "/date":
                 self.mybot.send_message(chatid,text)
                 self.mybot.send_message(chatid, "The date is ...")

    def execute(self):
       self.mybot.set_update_listener(self.listener)
       self.mybot.polling()
       while True:
           pass
  

if __name__ == '__main__':
   signal.signal(signal.SIGINT, interruptHandler)

   myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
   temperature = grove.GroveTemp(1)
   light = grove.GroveLight(3)

   myLcd.setColor(0,0,255)
   myLcd.setCursor(0,0)

   telegrambot = TelegramBot()
   telegrambot.execute()

   # Read the input and print, waiting one second between readings
   while 1:
      luz = light.value()
      tempval = temperature.value()
      myLcd.setCursor(0,0)
      myLcd.write('%6d'% tempval)
      myLcd.setCursor(1,0)
      myLcd.write('%6d'%luz)
      time.sleep(1)

   del light
   del temperature


