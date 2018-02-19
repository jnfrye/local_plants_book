from selenium import webdriver
import pandas as pd

import argparse
import os

import PyFloraBook.web.communication as scraping
import PyFloraBook.in_out.data_coordinator as dc


# ---------------- GLOBALS ----------------
SITE_NAME = "CalFlora"

# ---------------- INPUT ----------------
# Parse arguments
PARSER = argparse.ArgumentParser(
    description='Scrape CalFlora for species counts for given family'
    )
PARSER.add_argument(
    "-f", "--families", nargs='+',
    help="Names of the families to be analyzed."
    )
args = PARSER.parse_args()
families = args.families

# ---------------- SCRAPING ----------------
print("Opening browser...")
browser = webdriver.Firefox()
browser.set_window_size(500, 300)
browser.set_window_position(200, 200)

output_path = dc.locate_raw_counts_folder() / SITE_NAME

for family in families:
    # Load the webpage
    try:
        browser.get(
            "http://www.calflora.org/entry/wgh.html#srch=t&family="
            + family +
            "&group=none&fmt=simple&y=39.493&x=-119.6979&z=5&rid=rs940")
    except:
        pass  # lol

    scraping.wait_for_load(browser, "CLASS_NAME", "familyColumn")

    # Download the rows in the species data table
    # Next we skip the first three rows because they contain nonsense
    data_table = browser.find_element_by_id("resultSlot")
    data_rows = data_table.find_elements_by_tag_name("tr")[3:]

    # Extract the species counts
    species_list = [
        (row.find_element_by_class_name("column1Simple").text,
         int(row.find_element_by_class_name("observColumn").text.split()[0]))
        for row in data_rows
        ]

    # ---------------- ANALYSIS ----------------
    # Convert to friendly format for writing CSV
    family_results_path = str(output_path / (family + "_raw_data.csv"))
    all_species = pd.DataFrame(species_list, columns=["full_name", "count"])
    os.makedirs(output_path)
    all_species.to_csv(
        family_results_path,
        columns=['full_name', 'count'], index=False
        )

    # For whatever reason, it won't load the next page unless I do this
    browser.get("about:blank")

browser.quit()
