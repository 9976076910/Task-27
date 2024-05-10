from Data import data
from Locators import locator
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest

# Explicit Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
class TestOrangehrm:
    @pytest.fixture
    def boot(self):
        # Setup before testing
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.wait = WebDriverWait(self.driver, 10)
        yield
        # Teardown after testing
        self.driver.quit()

    def enterText(self, locator, textvalue):
        element = self.wait.until(ec.presence_of_element_located((By.NAME, locator)))
        element.clear()
        element.send_keys(textvalue)

        # Method to click Button

    def clickButton(self, locator):
        return self.wait.until(ec.presence_of_element_located((By.XPATH, locator))).click()

    def test_login(self,boot):
        try:
            # For loop for reading the data

            for row in range(2, data.WebData().rowCount() + 1):
                username = data.WebData().readData(row, 3)
                password = data.WebData().readData(row, 4)
                # Entering the data's
                self.enterText(locator.WebLocators().usernameLocator, username)
                self.enterText(locator.WebLocators().passLocator, password)
                self.clickButton(locator.WebLocators().subLocator)

                if self.driver.current_url == data.WebData().dashboardURL:
                    print("Successfully Loggedin")
                    data.WebData().writeData(row, 5, "PASSED")
                    # to print the name of the tester
                    data.WebData().writeData(row, 6, "NIVI")
                    curr = datetime.now().strftime("%H:%M:%S")
                    print(curr)
                    self.clickButton(locator.WebLocators().buttonLocator)
                    self.clickButton(locator.WebLocators().logoutButton)
                else:
                    print("Login unsuccessfull")
                    data.WebData().writeData(row, 5, "FAILED")
        except NoSuchElementException as e:
            print(e)
