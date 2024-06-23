import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from base_page import BasePage


class ChanceSearcher(BasePage):
    def __init__(self, chrome_options, bot):
        super().__init__(chrome_options)
        self.filter_url = "https://www.chancellors.co.uk/properties/search?page=1&area=Oxford&saleType=rent&maxPrice" \
                          "=1500&minPrice=1000&sort=dateHigh&show=96"
        self.property_container = (By.ID, "property_container")
        self.property = (By.CLASS_NAME, "cell.property-archive-container__cell")
        self.open_filter_page()
        self.scroll_to_the_bottom()
        self.known_apartments = self.get_all_apartments()
        self.close_browser()
        print("Chance searcher has been initialised")
        self.bot = bot
        self.message = None

    def open_filter_page(self):
        self.open_page(self.filter_url)

    def scroll_to_the_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @staticmethod
    def get_property_href_xpath(idx: int) -> str:
        return f'//*[@id="property_container"]/div[{idx}]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/a'

    def is_apartments_visible(self):
        try:
            self.are_visible(self.property)
            is_visible = True
        except TimeoutException:
            is_visible = False
        return is_visible

    def ask_human_for_help(self):
        print("Asking human for help")
        self.bot.send_message(self.message.chat.id, "Hay meat bag, I need your help here!!!")

    def get_all_apartments(self) -> list:
        while not self.is_apartments_visible():
            self.ask_human_for_help()
            time.sleep(30)
        num_of_properites = len(self.are_visible(self.property))
        print(f"len of items: {num_of_properites}")
        found_appartments = []
        for idx in range(1, num_of_properites + 1):
            xpath = self.get_property_href_xpath(idx)
            locator = (By.XPATH, xpath)
            try:
                apartment = self.get_element(locator)
                found_appartments.append(apartment.get_attribute("href"))
            except TimeoutException:
                print(f"WARN: Element not found. XPATH: {xpath}")
        return found_appartments

    def check_for_new_apartments(self) -> list:
        new_apartments = []

        self.open_filter_page()
        self.scroll_to_the_bottom()
        refreshed_appartments = self.get_all_apartments()
        refreshed_appartments.append(
            "https://www.chancellors.co.uk/properties/east-oxford-property/2-bedroom-purpose-built-to-rent/06042628"
            "/stockmore-street-east-oxford-ox4"
        )
        for apartment in refreshed_appartments:
            if apartment not in self.known_apartments:
                new_apartments.append(apartment)
                self.known_apartments.append(apartment)
                print(f"New apartment: {apartment}")
        self.close_browser()
        return new_apartments
