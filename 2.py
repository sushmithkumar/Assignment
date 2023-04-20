from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from bs4 import BeautifulSoup
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
        self.index = data['index']
        self.page = data['page']

    def start(self):
        """This function starts the Chrome webdriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(service_log_path='NUL', options=options)

    def login_dice(self):
        """This function logs into your personal LinkedIn profile"""
        # go to the Dice login url
        self.driver.get("https://www.dice.com/dashboard/login")
        # wait for the page to load
        wait = WebDriverWait(self.driver, 10)
        print('Dice login page loaded')

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'email')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
        print('Logged in succesfully')

        # wait for the page to load
        self.driver.implicitly_wait(4) # wait for 4 seconds

    def job_search(self):
        """This function goes to the 'Jobs' section and looks for all the jobs that match the keywords and location"""
        # go to Jobs
        jobs_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Jobs')
        jobs_link.click()
        print('In Job search page')

        # wait for the page to load
        self.driver.implicitly_wait(10) # wait for 10 seconds

        time.sleep(2)

        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.ID, "typeaheadInput")
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_keywords.send_keys(Keys.RETURN)
        time.sleep(2)# wait for the page to load
        #search_location = self.driver.find_element(By.ID, "google-location-search")
        #search_location.clear()
        #search_location.send_keys(self.location)
        #search_location.send_keys(Keys.RETURN)

        #self.filter_by_contract_and_today()
        self.filter_by_contract_and_last_3_days()

    #def filter_by_contract_and_today(self):

    def filter_by_contract_and_last_3_days(self):
        """This function filters all the job results by 'Contract' and 'Today'"""
        time.sleep(2) # wait for the page to load

        # select the Contract filter and apply the filter
        contract_filter = self.driver.find_element(By.XPATH, "//button[@aria-label='Filter Search Results by Contract']")
        contract_filter.click()

        # Select the Today filter and apply the filter
        #wait = WebDriverWait(self.driver, 10)
        #today_filter = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-cy='posted-date-option' and contains(text(), 'Today') and @class='btn btn-md btn-light ng-star-inserted' and @aria-checked='false']")))
        #today_filter.click()

        
        # Select the Last 3 days filter and apply the filter     
        wait = WebDriverWait(self.driver, 10)
        last_3_days_filter = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-cy='posted-date-option' and contains(text(), 'Last 3 Days') and @class='btn btn-md btn-light ng-star-inserted' and @aria-checked='false']")))
        last_3_days_filter.click()
        print('Applied all filters')


        time.sleep(2)
    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results
        total_results = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='totalJobCount']")))
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", ""))
        
        # Print the total number of jobs
        print('total jobs ' + str(total_results_int))

        job_title_elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link.bold'))
        )

        # Get the number of job title elements
        jobs_per_page = len(job_title_elements)

        total_pages = (total_results_int // jobs_per_page) + 1
        print('No of pages ' + str(total_pages))
        print('No of jobs in current page ' + str(jobs_per_page))

        # Add a delay to allow enough time to enter the input
        time.sleep(5)

        page = int(self.page)

        # Click on the Next button for (start page - 1) times
        for i in range(page - 1):
            next_button = self.driver.find_element(By.XPATH, f"//a[@class='page-link' and @rel='nofollow' and contains(text(),'{page}')]")
            next_button.click()
            page += 1
            time.sleep(5)

        # Calculate starting index
        index = int(self.index)

        links = self.driver.find_elements(By.CSS_SELECTOR, 'a.card-title-link.bold')

        while index < len(links):

            # Get the current URL
            current_url = self.driver.current_url
            main_url = self.driver.current_url

            # Wait for all job title elements to be visible
            job_title_elements = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link.bold'))
            )

            # Get the number of job title elements
            jobs_per_page = len(job_title_elements)

            # Open Jobs
            job_title_element = job_title_elements[index % jobs_per_page]

            # Extract the job title text
            job_title = job_title_element.text

            # Print the job title
            print(index+1, job_title)


            # Open the job page
            job_url = job_title_element.get_attribute('href')
            self.driver.get(job_url)
            
            try:
                # Wait for the 'Easy apply' button to load
                easy_apply_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.apply-button")))
                easy_apply_div.click()
                print('checking for Easy apply')
            except NoSuchElementException:
                print('Easy apply not found')
                # Wait for the 'Application submitted' button to load
                pass

            try:
                next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-next")))
                # Click on the 'Next' button
                next_button.click()
                print('Found Easy apply, resume uploaded')
            except TimeoutException:
                print('No Easy apply')

            try:
                apply_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Apply']")))
                # Click on the element
                apply_button.click()
                print('Applied')
                try:
                    element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "profile-not-visible")))
                    element.click()
                    print('selected no need')
                    try:
                        # Locate the element using its class name
                        continue_button = self.driver.find_element_by_class_name("sc-dhi-candidates-button")

                        # Click on the element
                        continue_button.click()
                        print('confirming the last step')
                    except:
                        print('failed at last step')

                except:
                    print('not selected')
                
                try:
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                        print("Alert dismissed")
                    except NoAlertPresentException:
                        print("No alert found")

                    print('going Back to search')
                    # Navigate back to the page with the link
                    self.driver.get(current_url)
                    index += 1
                    # Wait for new job links to appear
                    links = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link.bold'))
                    )
                    if self.driver.current_url == current_url:
                        print("Successfully navigated to search page")
                    else:
                        print("Failed to navigate to search page")
                except:
                    print("Failed to apply")
                    pass

            except TimeoutException:
                try:
                    print('going Back to search')
                    # Navigate back to the page with the link
                    self.driver.get(main_url)
                    index += 1
                    # Wait for new job links to appear
                    links = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link.bold'))
                    )
                    if self.driver.current_url == main_url:
                        print("Successfully navigated to search page")
                    else:
                        print("Failed to navigate to search page")
                except:
                    print("Error occurred while going back to search page")
                    continue

            if ((index + 1) % jobs_per_page) - 1 == 0 and page < total_pages:
                page += 1
                next_button = self.driver.find_element(By.XPATH, f"//a[@class='page-link' and @rel='nofollow' and contains(text(),'{page}')]")
                next_button.click()
                index = 0
                links = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a.card-title-link.bold'))
                )
                print('page no' +str(page))
                print('No of jobs in current page ' + str(jobs_per_page))
            
                
        self.driver.quit()
    def main(self):
        """This function calls all other functions"""
        self.start()
        self.login_dice()
        self.job_search()
        self.find_offers()
        input("Press any key to quit")

if __name__ == '__main__':
    with open('config2.json') as f:
        data = json.load(f)
    dice = Dice(data)
    dice.main()