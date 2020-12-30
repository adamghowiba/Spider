from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from configutil import get_value, update_key
import exceltool
import txtutil
from selenium.webdriver.chrome.options import Options

PATH = "C:\\Program Files (x86)\\chromedriver\\chromedriver.exe"


# TODO Error when website is offline.
class Spider:
    def __init__(self, website, location, resume):
        self.website = website
        self.resume = resume
        self.location = location
        self.driver = None
        self.listing_links = []
        self.listing_elements = []
        self.scanned_companies = txtutil.generate_list_of_companies()
        # self.first_list_title = None
        self.first = True

        # self.should_restart = True
        self.list_number = 0

        # Initialize the ExcelTool - used for saving data to excel file.
        self.excel = exceltool.ExcelTool()

    def run(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)
        self.lookup_location_action()
        self.store_current_listings()
        self.scan_listings()

    def lookup_location_action(self):
        # Opens website
        self.driver.get("https://www.loopnet.com")

        print("Getting results for search location: " + self.location)

        # TODO - Add feature for type
        for_lease_button = self.driver.find_element_by_xpath(
            '/html/body/section/main/section[1]/section[1]/div/div/div/form/div/div/ul/li[2]/h2/button')
        for_lease_button.click()

        location_search_box = self.driver.find_element_by_name("geography")
        location_search_box.send_keys(self.location)
        location_search_box.send_keys(Keys.RETURN)

    def add_company_contact(self):
        company_website = None
        try:
            contact_form = WebDriverWait(self.driver, 4).until(ec.presence_of_element_located((By.CLASS_NAME, "contact-logo")))

            # Contact section <a> tag
            contact_a_wrapper = contact_form.find_element_by_tag_name("a")
            company_website = contact_a_wrapper.get_attribute("href")
            print("Company Website:", company_website)

        except TimeoutException:
            print("Contact Logo Element Not Found: ", company_website)
            company_website = None

        # TODO - Do we need to do 2 None checks
        if company_website is not None and company_website != "None" \
                and not company_website.startswith("https://www.loopnet.com/"):
            if company_website not in self.scanned_companies:

                # Appends the newest company scanned to the current local list
                self.scanned_companies.append(company_website)

                # Also adds the company to the text file for next time.
                txtutil.append_company_safe(company_website)

                # Adds company data to excel file based on recent row, and saves file.
                # self.excel.add_company_data(company_website)
            else:
                print("Invalid or duplicate company")

    def get_listing_title(self):
        try:
            listing_title = self.driver.find_element_by_xpath(
                '/html/body/section/main/section/div[2]/div/div[1]/section/div[2]/div/h1/span[1]')
        except NoSuchElementException:
            listing_title = self.driver.find_element_by_xpath(
                '/html/body/section/main/section/div[2]/div/div[1]/section/div[2]/h1')
        return listing_title.text

    def scan_listings(self):
        # Check if a page was closed unexpectedly
        first_listing_title = None
        if self.resume and get_value('excel', 'lastLink') != 'None':
            self.driver.get(str(get_value('excel', "lastLink")))
            print("Opening last link known")
        else:
            # When spider first opens the listing poage, and needs to click on a listing not next.
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "placards")))

            print("Opening First Listing")
            self.driver.get(self.listing_links[0])

            self.driver.implicitly_wait(1)
            first_listing_title = self.get_listing_title()

        while True:
            # If spider scans all websites save and quit
            if first_listing_title == self.get_listing_title() and self.list_number > 1:
                self.save_listing()
                print('Scanned all list for city')
                break


            # Scans for company contact via Hunter, Appends company contact to excel. Checks duplicates
            self.add_company_contact()

            print("Opening Listing:", self.list_number, self.get_next_listing_page(link=True))
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

