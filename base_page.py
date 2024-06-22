from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from typing import List


class BasePage:
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 25)

    def do_click(self, by_locator: tuple) -> None:
        if self.is_visible(by_locator):
            self.wait_until_clickable(by_locator).click()

    def do_click_by_webelement(self, webelement: WebElement) -> None:
        visible_webelement = self._wait.until(EC.visibility_of(webelement))
        self._wait.until(EC.element_to_be_clickable(visible_webelement)).click()

    def do_send_keys(self, by_locator: tuple, text: str) -> None:
        self._wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def get_element_property(self, by_locator: tuple):
        return self._wait.until(EC.visibility_of_element_located(by_locator)).get_property('type')

    def get_element_text(self, by_locator: tuple) -> str:
        element = self._wait.until(EC.visibility_of_element_located(by_locator))

        return element.text

    def get_element(self, by_locator: tuple) -> WebElement:
        element = self._wait.until(EC.visibility_of_element_located(by_locator))
        return element

    def is_visible(self, by_locator: tuple) -> bool:
        element = self._wait.until(EC.visibility_of_element_located(by_locator))

        return element

    def wait_disappear(self, by_locator):
        self._wait.until(EC.invisibility_of_element_located(by_locator))

    def are_visible(self, by_locator: tuple) -> List[WebElement]:
        return self._wait.until(EC.visibility_of_all_elements_located(by_locator))

    def is_url_changed_to_expected(self, url: str) -> bool:
        return self._wait.until(EC.url_to_be(url))

    def go_back(self):
        self._driver.back()

    def wait_until_clickable(self, by_locator: tuple):
        return self._wait.until(EC.element_to_be_clickable(by_locator))

    def clear_field(self, by_locator):
        self._wait.until(EC.visibility_of_element_located(by_locator)).clear()
