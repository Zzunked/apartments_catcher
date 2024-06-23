from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from typing import List


class BasePage:
    def __init__(self, chrome_options):
        self.chrome_options = chrome_options
        self.driver = None
        self.wait = None

    def open_page(self, url: str) -> None:
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 25)
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()
        print("Closed webdriver")

    def do_click(self, by_locator: tuple) -> None:
        if self.is_visible(by_locator):
            self.wait_until_clickable(by_locator).click()

    def do_click_by_webelement(self, webelement: WebElement) -> None:
        visible_webelement = self.wait.until(ec.visibility_of(webelement))
        self.wait.until(ec.element_to_be_clickable(visible_webelement)).click()

    def do_send_keys(self, by_locator: tuple, text: str) -> None:
        self.wait.until(ec.visibility_of_element_located(by_locator)).send_keys(text)

    def get_element_property(self, by_locator: tuple):
        return self.wait.until(ec.visibility_of_element_located(by_locator)).get_property('type')

    def get_element_text(self, by_locator: tuple) -> str:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))

        return element.text

    def get_element(self, by_locator: tuple) -> WebElement:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))
        return element

    def is_visible(self, by_locator: tuple) -> bool:
        element = self.wait.until(ec.visibility_of_element_located(by_locator))

        return element

    def wait_disappear(self, by_locator):
        self.wait.until(ec.invisibility_of_element_located(by_locator))

    def are_visible(self, by_locator: tuple) -> List[WebElement]:
        return self.wait.until(ec.visibility_of_all_elements_located(by_locator))

    def is_url_changed_to_expected(self, url: str) -> bool:
        return self.wait.until(ec.url_to_be(url))

    def go_back(self):
        self.driver.back()

    def wait_until_clickable(self, by_locator: tuple):
        return self.wait.until(ec.element_to_be_clickable(by_locator))

    def clear_field(self, by_locator):
        self.wait.until(ec.visibility_of_element_located(by_locator)).clear()
