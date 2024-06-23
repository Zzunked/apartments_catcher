import os
import time

import telebot

from chance import ChanceSearcher

BOT_TOKEN = os.environ.get('BOT_TOKEN')


class NotificationBot:
    bot = telebot.TeleBot(BOT_TOKEN)

    def __init__(self, chrome_options):
        self.chrome_options = chrome_options
        self.chance_searcher = None

    @bot.message_handler(commands=['start'])
    def wait_for_new_apartments(self, message):
        self.chance_searcher = ChanceSearcher(self.chrome_options)
        time.sleep(30)

        while True:
            new_apartments = self.chance_searcher.check_for_new_apartments()
            if len(new_apartments) != 0:
                for apartment in new_apartments:
                    self.bot.send_message(message.chat.id, apartment)
                    time.sleep(1)
            time.sleep(30)
