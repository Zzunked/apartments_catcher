import os
import sys
import time

import telebot
from selenium.webdriver.chrome.options import Options

from chance import ChanceSearcher


BOT_TOKEN = os.environ.get('BOT_TOKEN')
TIMEOUT = 30


chrome_type = sys.argv[1]

chrome_options = Options()
if chrome_type == 'headless':
    chrome_options.add_argument('headless')
else:
    chrome_options.add_argument('chrome')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')


notification_bot = telebot.TeleBot(BOT_TOKEN)
chance_searcher = ChanceSearcher(chrome_options, notification_bot)
time.sleep(TIMEOUT)


@notification_bot.message_handler(commands=['start'])
def wait_for_new_apartments(message):
    chance_searcher.message = message
    while True:
        print("Checking for new apartments")
        notification_bot.send_message(message.chat.id, "Checking for new apartments")
        new_apartments = chance_searcher.check_for_new_apartments()
        if len(new_apartments) != 0:
            for apartment in new_apartments:
                notification_bot.send_message(message.chat.id, f"New apartment:\n{apartment}")
                time.sleep(1)
        time.sleep(TIMEOUT)


notification_bot.infinity_polling()
