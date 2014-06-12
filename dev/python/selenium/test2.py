###################################################################
### Using PyUnit (Python standart library, module unittest)     ###
### Created on 05/22/2014                                       ###
### Author: V. Kovrigin                                         ###
###################################################################

# you might need to install 'selenium' package by executing e.g.
# pip install selenium

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KapXLogin(unittest.TestCase):

    def setUp(self):
        # initialization
        self.driver = webdriver.Firefox()
        self.base_url = "https://kapx.kaplan.com"

    def test_kapx_login_and_logout(self):
        driver = self.driver
        # open home page
        driver.get(self.base_url + "/")
        # assert for the text "KAPx" in the title
        self.assertIn("KAPx", driver.title)
        #except AssertionError as e: self.verificationErrors.append(str(e))

        # login by clicking on "Login" button
        driver.find_element_by_class_name("nav-login").click()
        
        # wait for the frame to be available and switch to it
        wait = WebDriverWait(driver, 5)
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
        # wait for presence of text field Username
        driver.implicitly_wait(1)
        wait.until(EC.presence_of_element_located((By.NAME, "username")))

        # fill up the form on the frame
        # we can find element by id, xpath, name, link text, class, css etc...
        login_username = driver.find_element_by_name("username")
        login_username.clear()
        login_username.send_keys("TestUserName561")
        login_password = driver.find_element_by_xpath("//input[contains(@placeholder, 'Enter your Password')]")
        login_password.clear()
        login_password.send_keys("TestPassword1")
        driver.find_element_by_xpath("//button[contains(.,'Login')]").click()
        
        # return to main window
        driver.switch_to_default_content()
        # wait for page load and assert for text "Hello TestFirstName"
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//p"), "TestFirstName"))
        self.assertEqual("Hello TestFirstName", driver.find_element_by_xpath("//p").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))

        # logout by clicking on "Logout" button
        driver.find_element_by_class_name("nav-logout").click()

        # assert for text "You've signed out successfully" on the main page after logging out
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//article/div"), "signed out successfully"))
        self.assertIn("You've signed out successfully", driver.find_element_by_xpath("//article/div").text)
        #except AssertionError as e: self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        pass
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()