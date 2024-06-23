import os
import random
import sys
import time

import telebot
from selenium.webdriver.chrome.options import Options

from searchers import ChancellorsSearcher, BreckonSearcher, PennySearcher, ScotSearcher, AllenSearcher, \
    NEW_APARTMENT_PHRASES, NO_NEW_APARTMENTS_PHRASES, CHECKING_FOR_APARTMENTS_PHRASES

BOT_TOKEN = os.environ.get('BOT_TOKEN')


timeout = int(sys.argv[1])

chrome_options = Options()
chrome_options.add_argument('chrome')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')


notification_bot = telebot.TeleBot(BOT_TOKEN)
searcher_chancellors = ChancellorsSearcher(chrome_options, notification_bot)
searcher_breckon = BreckonSearcher(chrome_options, notification_bot)
searcher_penny = PennySearcher(chrome_options, notification_bot)
searcher_scot = ScotSearcher(chrome_options, notification_bot)
searcher_allen = AllenSearcher(chrome_options, notification_bot)
print("All searchers are initialised. Ready to start chat bot.")


@notification_bot.message_handler(commands=['start'])
def wait_for_new_apartments(message):
    searcher_chancellors.message = message
    searcher_breckon.message = message
    searcher_penny.message = message
    searcher_scot.message = message
    searcher_allen.message = message
    new_apartments = []
    while True:
        print("Checking for new apartment")
        notification_bot.send_message(message.chat.id, random.choice(CHECKING_FOR_APARTMENTS_PHRASES))
        new_apartments.extend(searcher_chancellors.check_for_new_apartments())
        new_apartments.extend(searcher_breckon.check_for_new_apartments())
        new_apartments.extend(searcher_penny.check_for_new_apartments())
        new_apartments.extend(searcher_scot.check_for_new_apartments())
        new_apartments.extend(searcher_allen.check_for_new_apartments())
        if len(new_apartments) != 0:
            for apartment in new_apartments:
                notification_bot.send_message(message.chat.id, f"{random.choice(NEW_APARTMENT_PHRASES)}:\n{apartment}")
                time.sleep(1)
            new_apartments.clear()
        else:
            notification_bot.send_message(message.chat.id, random.choice(NO_NEW_APARTMENTS_PHRASES))
        print(f"Sleep for {timeout}s")
        time.sleep(timeout)


notification_bot.infinity_polling()
