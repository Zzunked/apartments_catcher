import sys
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from chance import ChanceFilter


def configure_webdriver(chrome: str) -> Options:
    options = Options()
    if chrome == 'headless':
        options.add_argument('headless')
    else:
        options.add_argument('chrome')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    return options


if __name__ == "__main__":
    chrome_type = sys.argv[1]
    chrome_options = configure_webdriver(chrome_type)

    driver = webdriver.Chrome(options=chrome_options)

    chance = ChanceFilter(driver)
    chance.scroll_to_the_bottom()
    time.sleep(20)
    chance.get_all_properties()
    time.sleep(30)
