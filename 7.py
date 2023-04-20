from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json

class Dice:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.driver_path = data['chrome_driver_path']
        self.driver = None
        self.keywords = data['keywords']
        self.location = data['location']

    def start(self):
        """This function starts the Chrome webdriver"""

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-webrtc')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        self.driver = webdriver.Chrome(service_log_path='NUL', options=options)

    def login_dice(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the Dice login url
        self.driver.get("https://www.dice.com/dashboard/login")
        # wait for the page to load
        self.driver.implicitly_wait(4) # wait for 10 seconds

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'email')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)

         # wait for the page to load
        self.driver.implicitly_wait(4) # wait for 10 seconds

        #try:
            #popup = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'popup-class')))
            #popup.find_element_by_css_selector('.popup-close-button').click()
        #except:
            #pass

    def job_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""

        
        # go to Jobs
        jobs_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Jobs')
        jobs_link.click()

        # wait for the page to load
        self.driver.implicitly_wait(10) # wait for 10 seconds

        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.ID, "typeaheadInput")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_keywords.send_keys(Keys.RETURN)
        time.sleep(2) # wait for the page to load
        search_location = self.driver.find_element(By.ID, "google-location-search")
        search_location.clear()
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.RETURN)

        # apply the Contract filter
        self.filter_by_contract_and_today()

    def filter(self):

            """This function filters all the job results by 'Contract'"""
            time.sleep(2) # wait for the page to load
            # select the Contract filter and apply the filter
            contract_filter = self.driver.find_element(By.XPATH, "//button[@aria-label='Filter Search Results by Contract']")
            contract_filter.click()
            
    def main(self):
            """This function calls all other functions"""
            self.start()
            self.login_dice()
            self.job_search()  # Added function call to job_search() function
            input("Press any key to quit")

if __name__ == '__main__':
    with open('config2.json') as f:
        data = json.load(f)
    dice = Dice(data)
    dice.main()
