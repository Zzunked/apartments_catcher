import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


from typing import List


HUMAN_POLLING_INTERVAL = 30


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

    def open_page(self, url: str) -> None:
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 25)
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()
        print("Closed webdriver")

    def get_element(self, by_locator: tuple) -> WebElement:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))
        return element

    def is_visible(self, by_locator: tuple) -> bool:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))
        return element

    def are_visible(self, by_locator: tuple) -> List[WebElement]:
        return self.wait.until(ec.visibility_of_all_elements_located(by_locator))

    def ask_human_for_help(self):
        print("Asking human for help")
        self.bot.send_message(self.message.chat.id, "Hay meat bag, I need your help here!!!")

    def open_filter_page(self):
        self.open_page(self.filter_url)

    def is_apartments_visible(self):
        try:
            self.are_visible(self.apartment)
            is_visible = True
        except TimeoutException:
            is_visible = False
        return is_visible

    def get_all_apartments(self):
        raise NotImplementedError

    def scroll_to_the_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo({top:document.body.scrollHeight, behavior: 'smooth'});")

    def check_for_new_apartments(self) -> list:
        new_apartments = []

        self.open_filter_page()
        self.scroll_to_the_bottom()
        refreshed_appartments = self.get_all_apartments()
        for apartment in refreshed_appartments:
            if apartment not in self.known_apartments:
                new_apartments.append(apartment)
                self.known_apartments.append(apartment)
                print(f"New apartment: {apartment}")
        self.close_browser()
        return new_apartments


class ChancellorsSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.chancellors.co.uk/properties/search?page=1&area=Oxford&saleType=rent&maxPrice" \
                          "=1500&minPrice=1000&sort=dateHigh&show=96"
        self.apartment = (By.CLASS_NAME, "cell.property-archive-container__cell")
        self.apartment_href_xpath_format = '//*[@id="property_container"]/div[{}]/div/div[1]/div/div[2]/div/div/' \
                                           'div[1]/div[1]/a'

        self.open_filter_page()
        time.sleep(5)
        self.scroll_to_the_bottom()
        time.sleep(5)
        self.known_apartments = self.get_all_apartments()
        self.known_apartments.pop()
        self.close_browser()
        print("Chancellors searcher has been initialised")

    def get_property_href_xpath(self, idx: int) -> str:
        return self.apartment_href_xpath_format.format(idx)

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        num_of_apartments = len(self.are_visible(self.apartment))
        print(f"len of items: {num_of_apartments}")
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

        self.open_filter_page()
        self.scroll_to_the_bottom()
        self.known_apartments = self.get_all_apartments()
        self.known_apartments.pop()
        self.close_browser()
        print("Breckon searcher has been initialised")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"len of items: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("href"))
        print(f"Found apartments on Breckon: {found_appartments}")
        return found_appartments


class PennySearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.pennyandsinclair.co.uk/oxfordshire/oxford/lettings/from-1-bed/from-1000/" \
                          "up-to-2000/within-3-miles/most-recent-first#/"
        self.apartment = (By.CLASS_NAME, "card-link")

        self.open_filter_page()
        self.scroll_to_the_bottom()
        self.known_apartments = self.get_all_apartments()
        self.known_apartments.pop()
        self.close_browser()
        print("Penny searcher has been initialised")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"len of items: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("href"))
        print(f"Found apartments on Breckon: {found_appartments}")
        return found_appartments


class ScotSearcher(BaseSearcher):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options, bot)
        self.filter_url = "https://www.scottfraser.co.uk/properties-search-results?search_type=rent&radius=3&" \
                          "search_lng=-1.2448500&search_lat=51.7501000&min_price=1000&max_price=1500&min_bedrooms" \
                          "=1&sort=updated"
        self.apartment = (By.CLASS_NAME, "search-results-item.d-flex.flex-column")

        self.open_filter_page()
        self.scroll_to_the_bottom()
        self.known_apartments = self.get_all_apartments()
        self.known_apartments.pop()
        self.close_browser()
        print("Scot searcher has been initialised")

    @check_if_help_needed
    def get_all_apartments(self) -> list:
        apartments = self.are_visible(self.apartment)
        print(f"len of items: {len(apartments)}")
        found_appartments = []
        for apartment in apartments:
            found_appartments.append(apartment.get_attribute("onclick"))
        links = list(map(lambda x: x.split("'")[1], found_appartments))
        print(f"Found apartments on Scot: {links}")
        return links
