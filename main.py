import os
import sys
import time

import telebot
from selenium.webdriver.chrome.options import Options

from searchers import ChancellorsSearcher, BreckonSearcher, PennySearcher

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
searcher_chancellors = ChancellorsSearcher(chrome_options, notification_bot)
searcher_breckon = BreckonSearcher(chrome_options, notification_bot)
searcher_penny = PennySearcher(chrome_options, notification_bot)
print("All searchers are initialised. Ready to start chat bot.")


@notification_bot.message_handler(commands=['start'])
def wait_for_new_apartments(message):
    searcher_chancellors.message = message
    searcher_breckon.message = message
    searcher_penny.message = message
    new_apartments = []
    while True:
        print("Checking for new apartment")
        notification_bot.send_message(message.chat.id, "Checking for new apartment")
        new_apartments.extend(searcher_chancellors.check_for_new_apartments())
        new_apartments.extend(searcher_breckon.check_for_new_apartments())
        new_apartments.extend(searcher_penny.check_for_new_apartments())
        if len(new_apartments) != 0:
            for apartment in new_apartments:
                notification_bot.send_message(message.chat.id, f"New apartment:\n{apartment}")
                time.sleep(1)
            new_apartments.clear()
        else:
            notification_bot.send_message(message.chat.id, f"There are no new apartments")
        print(f"Sleep for {TIMEOUT}s")
        time.sleep(TIMEOUT)


notification_bot.infinity_polling()
