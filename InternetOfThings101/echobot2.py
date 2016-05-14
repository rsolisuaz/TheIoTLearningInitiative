#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import pyupm_grove as grove
import pyupm_i2clcd as lcd

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
temperature = grove.GroveTemp(1)
light = grove.GroveLight(3)

myLcd.setColor(0,0,255)
myLcd.setCursor(0,0)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def obtentemp(bot, update):
    tempval = temperature.value()
    myLcd.setCursor(0,0)
    myLcd.write('Temp = %6d'% tempval)
    bot.sendMessage(update.message.chat_id, text='Temperatura es %6d grados centigrados'% 
tempval)

def obtenluz(bot, update):
    luz = light.value()
    myLcd.setCursor(1,0)
    myLcd.write('Luz = %6d'% luz)
    bot.sendMessage(update.message.chat_id, text='Luz es %6d'% luz)

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("181560082:AAHbTzTUj6_onF8p_iClYODVjFyreSvAEZg")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("temperatura", obtentemp))
    dp.add_handler(CommandHandler("luz", obtenluz))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
