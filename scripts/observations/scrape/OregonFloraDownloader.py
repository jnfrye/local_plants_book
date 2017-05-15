"""Script for downloading observation data from OregonFlora
"""

import shutil
import argparse
import time
import os.path
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import PyFloraBook.web.communication as scraping
import PyFloraBook.input_output.data_coordinator as dc


# ---------------- GLOBALS ----------------
SITE_NAME = "OregonFlora"

# ---------------- INPUT ----------------
# Parse arguments
PARSER = argparse.ArgumentParser(
    description='Download family observation data from OregonFlora'
    )
PARSER.add_argument(
    "-f", "--families", nargs='+',
    help="Names of the families to be analyzed."
    )
args = PARSER.parse_args()
families = args.families

# ---------------- SETUP ----------------
download_dir = Path(os.getcwd())
print("Opening browser...")
# We have to set up the webdriver to automatically download files
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", str(download_dir))
fp.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/csv; charset=UTF-8"
    )

browser = webdriver.Firefox(firefox_profile=fp)
browser.set_window_size(500, 300)
browser.set_window_position(200, 200)

output_path = dc.locate_raw_observations_folder() / SITE_NAME

# ---------------- SCRAPING ----------------
# Load the search webpage
for family in families:
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

    # This is the default file name when you download from OregonFlora
    download_name = "results.csv"
    temp_file_path = download_dir / download_name

    # Check if the file already exists; rename if so
    if os.path.isfile(str(temp_file_path)):
        shutil.move(str(temp_file_path), str(temp_file_path) + ".bkp")

    # Click the download button
    time.sleep(.5)
    browser.find_element_by_id("downloadxls").click()

    i = 0
    while True:
        i += 1
        time.sleep(1)
        if i >= 10 or os.path.isfile(str(temp_file_path)):
            break
    time.sleep(.5)

    final_file_name = family + ".csv"
    final_file_path = output_path / final_file_name

    shutil.move(str(temp_file_path), str(final_file_path))
    print(family + " finished!")

browser.quit()
