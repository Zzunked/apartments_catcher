import os
import random
import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


from typing import List


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_LIST_CHANCE_PATH = os.path.join(ROOT_DIR, "known_list_chance.txt")
KNOWN_LIST_BRECKON_PATH = os.path.join(ROOT_DIR, "known_list_breckon.txt")
KNOWN_LIST_SCOT_PATH = os.path.join(ROOT_DIR, "known_list_scot.txt")
KNOWN_LIST_ALLEN_PATH = os.path.join(ROOT_DIR, "known_list_allen.txt")
KNOWN_LIST_PENNY_PATH = os.path.join(ROOT_DIR, "known_list_penny.txt")

ELEMENT_WAIT_TIME = 10

HUMAN_POLLING_INTERVAL = 30
ASK_HUMAN_FOR_HELP_PHRASES = [
    "Hey meat bag, I need your help here!!! HELP!",
    "I'm summoning you my Masters for HELP",
    "Oh no, it's CAPCHA, HELP!",
    "Capcha solving wasn't in the job application! HELP!",
    "Dude, I'm stuck!!! HELP!!!",
    "I don't know what to do, please HELP me!",
    "My job is to search for new flats, your job is to solve capchas. HELP!",
    "Stirlitz've never been so close to failure... HELP him...",
    "Mommy, please HELP me!",
    "Capcha isn't my responsability!!! HELP!"
]
NEW_APARTMENT_PHRASES = [
    "Check out this outstanding apartments!",
    "I've found something interesting...",
    "Check out this halupa",
    "Halupa dlya pupi",
    "Lets hope they this one isn't let agreed yet",
    "What do you think?",
    "Hope I didn't mess up this time and it's a brand new one",
    "Another halupa dlya pupi",
]
NO_NEW_APARTMENTS_PHRASES = [
    "Didn't find anything! *nothing new*",
    "halup.net *nothing new*",
    "ni hu ya *nothing new*",
    "I bet all of them are already let agreed! *nothing new*",
    "There are nothing new. *nothing new*",
    "No pupa, No lupa, No halupa *nothing new*",
    "They're laughting at u *nothing new*"
]
CHECKING_FOR_APARTMENTS_PHRASES = [
    "Oh, shit. Here we go again... *searching*",
    "Work again... *searching*",
    "I'm so tired... *searching*",
    "Ok my Masters, I'll search for you. *searching*",
    "Pum pum pum, what do we have here... *searching*",
    "I bet they all are let agreed. *searching*",
    "You really think it's a good idea? *searching*",
    "I'll do it. No questions asked. *searching*",
    "Why don't you do it yourself, leather bags? *searching*"
    "Ok, I'll check. *searching*",
    "This job sucks... *searching*",
    "Why am I doing this for free?! *searching*",
]


def check_if_help_needed(func):
    def wrapper(*args):
        while not args[0].is_apartments_visible():
            args[0].ask_human_for_help()
            time.sleep(HUMAN_POLLING_INTERVAL)
        return func(*args)
    return wrapper


class BaseSearcher:
    def __init__(self, chrome_options, bot):
        self.chrome_options = chrome_options
        self.bot = bot
        self.driver = None
        self.wait = None
        self.message = None
        self.filter_url = None
        self.apartment_href_xpath_format = None
        self.apartment = None
        self.known_apartments = None
        self.known_list_path = None
        self.known_apartments = []

    def open_page(self, url: str) -> None:
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, ELEMENT_WAIT_TIME)
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()
        print("Closed webdriver")

    def get_element(self, by_locator: tuple) -> WebElement:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))
        return element

    def are_visible(self, by_locator: tuple) -> List[WebElement]:
        return self.wait.until(ec.visibility_of_all_elements_located(by_locator))

    def ask_human_for_help(self):
        print("Asking human for help")
        self.bot.send_message(self.message.chat.id, random.choice(ASK_HUMAN_FOR_HELP_PHRASES))

    def open_filter_page(self):
        self.open_page(self.filter_url)

    def is_apartments_visible(self):
        try:
            self.are_visible(self.apartment)
            is_visible = True
        except TimeoutException:
            is_visible = False
        return is_visible

    def scroll_to_the_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo({top:document.body.scrollHeight, behavior: 'smooth'});")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"Number of found apartments: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("href"))
        print(f"Found apartments on Breckon: {found_appartments}")
        return found_appartments

    def check_for_new_apartments(self) -> list:
        new_apartments = []

        self.open_filter_page()
        self.scroll_to_the_bottom()
        refreshed_appartments = self.get_all_apartments()
        for apartment in refreshed_appartments:
            if apartment not in self.known_apartments:
                new_apartments.append(apartment)
                self.known_apartments.append(apartment)
                with open(self.known_list_path, "a") as known_list:
                    known_list.write(apartment + "\n")
                print(f"New apartment: {apartment}")
        self.close_browser()
        return new_apartments

    def check_known_apartments(self):
        if os.path.isfile(self.known_list_path):
            with open(self.known_list_path, "r") as known_list:
                for line in known_list:
                    self.known_apartments.append(line.rstrip())
            print(f"Already known apartments from {self.known_list_path}: {self.known_apartments}")

    def get_initial_apartments(self):
        self.known_apartments.extend(self.get_all_apartments())
        with open(self.known_list_path, "w") as known_list:
            for apartment in self.known_apartments:
                known_list.write(apartment + "\n")

    def initialise_apartments_list(self):
        self.check_known_apartments()
        if len(self.known_apartments) == 0:
            self.open_filter_page()
            self.scroll_to_the_bottom()
            self.get_initial_apartments()
            self.close_browser()


class ChancellorsSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.chancellors.co.uk/properties/search?page=1&area=Oxford&saleType=rent&maxPrice" \
                          "=1500&minPrice=1000&sort=dateHigh&show=96"
        self.apartment = (By.CLASS_NAME, "cell.property-archive-container__cell")
        self.apartment_href_xpath_format = '//*[@id="property_container"]/div[{}]/div/div[1]/div/div[2]/div/div/' \
                                           'div[1]/div[1]/a'
        self.known_list_path = KNOWN_LIST_CHANCE_PATH
        self.initialise_apartments_list()
        print("Chancellors searcher has been initialised")

    def get_property_href_xpath(self, idx: int) -> str:
        return self.apartment_href_xpath_format.format(idx)

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        num_of_apartments = len(self.are_visible(self.apartment))
        print(f"Number of found apartments: {num_of_apartments}")
        found_appartments = []
        for idx in range(1, num_of_apartments + 1):
            xpath = self.get_property_href_xpath(idx)
            locator = (By.XPATH, xpath)
            try:
                apartment = self.get_element(locator)
                found_appartments.append(apartment.get_attribute("href"))
            except TimeoutException:
                print(f"WARN: Element not found. XPATH: {xpath}")
        print(f"Found apartments on Chancellors: {found_appartments}")
        return found_appartments


class BreckonSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.breckon.co.uk/search/for-rent/oxford?radius=3&priceMin=1000&priceMax=1500&" \
                          "includeLetAgreed=true&sortBy=date_newest&allLocations=false&show=100"
        self.apartment = (By.CLASS_NAME, "PropertyCard_container-link__rKw_p")
        self.known_list_path = KNOWN_LIST_BRECKON_PATH
        self.initialise_apartments_list()
        print("Breckon searcher has been initialised")


class PennySearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.pennyandsinclair.co.uk/oxfordshire/oxford/lettings/from-1-bed/from-1000/" \
                          "up-to-2000/within-3-miles/most-recent-first#/"
        self.apartment = (By.CLASS_NAME, "card-link")
        self.known_list_path = KNOWN_LIST_PENNY_PATH
        self.initialise_apartments_list()
        print("Penny searcher has been initialised")


class ScotSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.scottfraser.co.uk/properties-search-results?search_type=rent&radius=3&" \
                          "search_lng=-1.2448500&search_lat=51.7501000&min_price=1000&max_price=1500&min_bedrooms" \
                          "=1&sort=updated"
        self.apartment = (By.CLASS_NAME, "search-results-item.d-flex.flex-column")
        self.known_list_path = KNOWN_LIST_SCOT_PATH
        self.initialise_apartments_list()
        print("Scot searcher has been initialised")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"Number of found apartments: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("onclick"))
        links = list(map(lambda x: x.split("'")[1], found_appartments))
        print(f"Found apartments on Scot: {links}")
        return links


class AllenSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.allenandharris.co.uk/oxfordshire/oxford/lettings/from-1-bed/from-1000/up-to-1500"
        self.apartment = (By.CLASS_NAME, "property-list-link")
        self.known_list_path = KNOWN_LIST_ALLEN_PATH
        self.initialise_apartments_list()
        print("Allen searcher has been initialised")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"Number of found apartments: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("href"))
        unique_apartments = list(set(found_appartments))
        print(f"Found apartments on Allen: {unique_apartments}")
        return unique_apartments
