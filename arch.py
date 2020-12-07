import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import exceltool

PATH = "C:\Program Files (x86)\chromedriver.exe"


class Spider:
    def __init__(self, website, location):
        self.website = website
        self.location = location
        self.driver = webdriver.Chrome(PATH)
        self.listing_links = []
        self.listing_elements = []

        # self.should_restart = True
        self.list_number = 0

        self.excel = exceltool.ExcelTool()

    def lookup_location_action(self):
        # Opens website
        self.driver.get("https://www.loopnet.com")

        print("Getting results for search location: " + self.location)
        location_search_box = self.driver.find_element_by_name("geography")
        location_search_box.send_keys(self.location)
        location_search_box.send_keys(Keys.RETURN)

    def store_current_listings(self):
        listings = WebDriverWait(self.driver, 10) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "placards")))

        # Gets all listings with link. Tag <a>
        listings_a_tag = listings.find_elements_by_tag_name("a")

        # Loop through listing tags to add link, and element
        for listing in listings_a_tag:

            # Gets the actual link
            listing_href_tag = listing.get_attribute("href")
            if listing_href_tag not in self.listing_links and str(listing_href_tag).startswith("https://www.loopnet"):
                self.listing_links.append(listing_href_tag)
                self.listing_elements.append(listing)
        print("Added links to list:", len(self.listing_elements))

    def scan_listings(self, should_restart=True):
        first = False
        while should_restart:
            if not first:
                first = True
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "placards")))
                self.listing_elements[0].click()
                print("First listing")

            print("Opening Listing:", self.list_number, self.get_next_listing_page(link=True))
            # Opens(gets) each link from 'listing_links' variable and opens it.
            # self.driver.get(self.listing_links[self.list_number])
            try:
                self.driver.implicitly_wait(3)
                contact_form = self.driver.find_element_by_xpath(
                    "/html/body/section/main/section/div[2]/div/div[2]/div/div/div[2]/div/div[2]/ul/li[2]/a")

                # Print out grabbed website for testing purposes.
                company_website = contact_form.get_attribute("href")
                if company_website is not None and company_website != "None" and not(company_website.startswith("https://www.loopnet.com/")):
                    print(company_website)
                    self.excel.add_company_data(company_website)
                    self.excel.save_file()

            except NoSuchElementException:
                print("Not Found")

            self.get_next_listing_page()

            # Add one to move onto next list
            self.list_number += 1
            time.sleep(3)

    def get_next_listing_page(self, link=False):
        next_page_wrapper = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/main/section/div[1]/nav/div[5]/a[2]")))

        # Should you return the link of the next listing, for priting purposes.
        if link:
            return next_page_wrapper.get_attribute("href")
        else:
            next_page_wrapper.click()
