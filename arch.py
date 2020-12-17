from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from configutil import get_value, update_key
import exceltool
import txtutil
import ui

PATH = "C:\\Program Files (x86)\\chromedriver\\chromedriver.exe"


class Spider:
    def __init__(self, website, location, resume):
        self.website = website
        self.resume = resume
        self.location = location
        self.driver = None
        self.listing_links = []
        self.listing_elements = []
        self.scanned_companies = txtutil.generate_list_of_companies()
        self.first_list_title = None
        self.first = True

        # self.should_restart = True
        self.list_number = 0

        # Initialize the ExcelTool - used for saving data to excel file.
        self.excel = exceltool.ExcelTool()

    def run(self):
        self.driver = webdriver.Chrome(PATH)
        self.lookup_location_action()
        self.store_current_listings()
        self.scan_listings()

    def lookup_location_action(self):
        # Opens website
        self.driver.get("https://www.loopnet.com")

        print("Getting results for search location: " + self.location)

        # TODO - Add feature for type
        # for_lease_button = self.driver.find_element_by_xpath(
        #     '/html/body/section/main/section[1]/section[1]/div/div/div/form/div/div/ul/li[2]/h2/button')
        # for_lease_button.click()

        location_search_box = self.driver.find_element_by_name("geography")
        location_search_box.send_keys(self.location)
        location_search_box.send_keys(Keys.RETURN)

    def add_company_contact(self):
        try:
            self.driver.implicitly_wait(3)
            contact_form = self.driver.find_element_by_class_name("contact-logo")

            # Contact section <a> tag
            contact_a_wrapper = contact_form.find_element_by_tag_name("a")
            company_website = contact_a_wrapper.get_attribute("href")

            # TODO - Do we need to do 2 None checks
            if company_website is not None \
                    and company_website != "None" \
                    and not company_website.startswith("https://www.loopnet.com/"):
                if company_website not in self.scanned_companies:
                    # Print out grabbed website for testing purposes.
                    print(company_website)

                    # Appends the newest company scanned to the current local list
                    self.scanned_companies.append(company_website)

                    # Also adds the company to the text file for next time.
                    txtutil.append_company_safe(company_website)

                    # Adds company data to excel file based on recent row, and saves file.
                    self.excel.add_company_data(company_website)
                else:
                    print("Duplicate company ignored")
        except NoSuchElementException:
            print("Not Found")

    def get_listing_title(self):
        try:
            self.first_list_title = self.driver.find_element_by_xpath(
                '/html/body/section/main/section/div[2]/div/div[1]/section/div[2]/div/h1/span[1]')
        except NoSuchElementException:
            self.first_list_title = self.driver.find_element_by_xpath(
                '/html/body/section/main/section/div[2]/div/div[1]/section/div[2]/h1')
        return self.first_list_title

    def scan_listings(self, should_restart=True):
        if self.resume and get_value('excel', 'lastLink') != 'None':
            self.driver.get(str(get_value('excel', "lastLink")))
            print("Opening last link known")
        else:
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "placards")))
            self.driver.get(self.listing_links[0])

            self.driver.implicitly_wait(3)
            self.get_listing_title()

            print("Opening First Listing")
        while True:
            list_title = self.get_listing_title()

            # If spider scans all websites save and quit
            if self.first_list_title.text == list_title.text and self.list_number > 1:
                self.save_listing()
                print('Scanned all list for city')
                break

            print(self.listing_links[0])
            print("Opening Listing:", self.list_number, self.get_next_listing_page(link=True))

            # Appends company contact information to excel file.
            # Also checks for duplicates.
            self.add_company_contact()

            # Locates the next page button and clicks it
            self.get_next_listing_page()

            # Add one to move onto next list
            self.list_number += 1


    def get_next_listing_page(self, link=False):
        next_page_wrapper = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located(
            (By.XPATH, "/html/body/section/main/section/div[1]/nav/div[5]/a[2]")))

        # Should you return the link of the next listing, for printing purposes.
        if link:
            return next_page_wrapper.get_attribute("href")
        else:
            next_page_wrapper.click()

    def save_listing(self, end=True):
        if not end:
            update_key('excel', "lastLink", self.driver.current_url)
        update_key('home', 'listingsScanned', get_value('home', 'listingsScanned') + self.list_number)
        print("Quitting chrome driver, saving last location", self.driver.current_url)
        self.list_number = 0
        self.driver.quit()

    # TODO Don't need to store current listings anymore, only need first
    def store_current_listings(self):
        listings = WebDriverWait(self.driver, 10) \
            .until(ec.presence_of_element_located((By.CLASS_NAME, "placards")))

        # Gets all listings with link. Tag <a>
        listings_a_tag = listings.find_elements_by_tag_name("a")

        # Loop through listing tags to add link, and element
        for listing in listings_a_tag:

            # Gets the actual link
            listing_href_tag = listing.get_attribute("href")
            if listing_href_tag not in self.listing_links and str(listing_href_tag).startswith("https://www.loopnet"):
                self.listing_links.append(listing_href_tag)
                self.listing_elements.append(listing)
