"""Script for downloading observation data from OregonFlora
"""

import shutil
import argparse
import time
import os.path

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# TODO I've gotta learn how python imports work lol
import common as scraping

import pdb; pdb.set_trace()

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Download family observation data from OregonFlora')
parser.add_argument("-f", "--families", nargs='+',
                    help="Names of the families to be analyzed.")
ARGS = parser.parse_args()
FAMILIES = ARGS.families

FOLDER = './OregonFlora/'

# ---------------- SETUP ----------------
print("Opening browser...")
# We have to set up the webdriver to automatically download files
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/csv; charset=UTF-8")

browser = webdriver.Firefox(firefox_profile=fp)
browser.set_window_size(500, 300)
browser.set_window_position(200, 200)

# ---------------- SCRAPING ----------------
# Load the search webpage
for family in FAMILIES:
    print("Loading atlas...")
    browser.get("http://www.oregonflora.org/atlas.php")
    scraping.wait_for_load(browser, "ID", "btnInstructions")

    print("Selecting options for " + family + "...")
    family_select = Select(browser.find_element_by_id("familySelectionBox"))
    family_select.deselect_all()
    family_select.select_by_value(family)

    # Pick the right checkboxes
    browser.find_element_by_id("Observations").click()
    browser.find_element_by_id("OSU").click()

    # Open the advanced options menu
    browser.find_element_by_id("btnAdvanced").click()
    scraping.wait_for_load(browser, "ID", "startyear")

    # Type in correct start year
    start_year = browser.find_element_by_id("startyear")
    for i in range(6):
        # Delete whatever is already there
        start_year.send_keys(Keys.BACK_SPACE)

    start_year.send_keys("2002")

    # Submit form
    browser.find_element_by_id("atlasSearch").click()

    print("Downloading data for " + family + "...")
    scraping.wait_for_load(browser, "ID", "downloadxls")

    # Gotta check if there's a results.csv file already there
    if os.path.isfile("results.csv"):
        shutil.move("results.csv", "results.bkp.csv")

    # Click the download button
    time.sleep(.5)
    browser.find_element_by_id("downloadxls").click()

    i = 0
    while True:
        i += 1
        time.sleep(1)
        if i >= 10 or os.path.isfile("results.csv"):
            break
    time.sleep(.5)

    shutil.move("results.csv", FOLDER + family + ".csv")
    print(family + " finished!")
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

browser.quit()
