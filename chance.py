import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from base_page import BasePage


class ChanceFilter(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.filter_url = "https://www.chancellors.co.uk/properties/search?page=1&area=Oxford&saleType=rent&maxPrice" \
                           "=1500&minPrice=1000&sort=dateHigh&show=96"
        self._driver.get(self.filter_url)
        self.property_container = (By.ID, "property_container")
        # self.property = (By.CLASS_NAME, "cell.small-10")
        self.property = (By.CLASS_NAME, "cell.property-archive-container__cell")
        self.property_link = (
            By.CSS_SELECTOR, '//*[@id="property_container"]/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/a'
        )
        self.property_title = (By.CLASS_NAME, "archive-property__title")
        self.number_of_properties = (By.XPATH, "/html/body/div[5]/section/div[2]/div/div[1]/div/div[2]/div[2]/strong")

    def scroll_to_the_bottom(self):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    @staticmethod
    def get_property_href_xpath(idx):
        return f'//*[@id="property_container"]/div[{idx}]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/a'

    def get_all_properties(self):
        # items = self.are_visible(self.property)
        # expected_num_of_properties = self.get_element(self.number_of_properties)
        num_of_properites = len(self.are_visible(self.property))
        # timeout = time.time() + 30
        # while num_of_properites < int(expected_num_of_properties.text) or time.time() < timeout:
        #     # self.scroll_to_the_bottom()
        #     print(num_of_properites)
        #     num_of_properites = len(self.are_visible(self.property))
        #     time.sleep(3)

        print(f"len of items: {num_of_properites}")
        found_appartments = []
        for idx in range(1, num_of_properites + 1):
            locator = (By.XPATH, self.get_property_href_xpath(idx))
            try:
                apartment = self.get_element(locator)
                found_appartments.append(apartment.get_attribute("href"))
                print(apartment.get_attribute("href"))
            except TimeoutException:
                pass

        print(f"Expected: {num_of_properites}, found: {len(found_appartments)}")
