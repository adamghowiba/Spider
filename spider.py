from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pyhunter import PyHunter
import writer

## Import webdriver(Browser you want to use)
# main = driver.find_element_by_class_name("placards")
websites = []


def run():
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # Opens website
    driver.get("https://www.loopnet.com")

    search = driver.find_element_by_name("geography")
    search.send_keys("Longwood,FL")
    search.send_keys(Keys.RETURN)

    ## Make sure to wait before trying to find elemtn, make sure it exists

    try:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placardSec")))

        elems = driver.find_elements_by_tag_name("a")
        max_count = -1
        elements = []
        list_number = 0
        should_restart = True
        final = []
        current_link = "None"
        for elem in elems:
            txt = elem.get_attribute("href")
            if str(txt).startswith("https://www.loopnet.com/Listing/") and txt not in final:
                final.append(txt)
                elements.append(elem)
                max_count += 1

        while should_restart:
            print("clicking ", list_number)
            driver.get(final[list_number])
            list_number += 1

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "contact-form-contacts")))
            link_wrapper = driver.find_element_by_class_name("contact-logo")
            link = link_wrapper.find_element_by_tag_name("a")
            websites.append(link.get_attribute("href"))

            driver.back()
            time.sleep(5)
            print(websites)

        # for link in final_list:
        #     websites.append(link)

    finally:
        print("Done")


# if not str(h).startswith(
#                       ("https://www.loopnet.com", "https://listingmanager", "https://images1.", "https://facebook",
#                        "https://linkedin.com", "https://twitter.com",
#                        "https://marketing", "https://secure", "javascript", "None", "mailto", "tel")) \
#                       and len(h) > 4 \
#                       and h not in final_list:

run()
