import os
import time

import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    while True:
        bot.send_message(message.chat.id, "kek")
        time.sleep(5)
