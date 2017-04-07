from selenium import webdriver
import pandas as pd

import argparse
import sys; sys.path.append("..")
import scraping

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Scrape CalFlora for species counts for given family')
parser.add_argument("-f", "--families", nargs='+',
    help="Names of the families to be analyzed.")
args = parser.parse_args()
families = args.families

# ---------------- SCRAPING ----------------
print("Opening browser...")
browser = webdriver.Firefox()
browser.set_window_size(500, 300)
browser.set_window_position(200, 200)
browser.set_page_load_timeout(8)

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
    all_species = pd.DataFrame(species_list, columns=["full_name", "count"])

    # Remove the variety info
    all_species = pd.concat(
        [all_species,
         all_species['full_name'].str.split(' ', expand=True, n=2)],
        axis=1
        )
    if len(all_species.columns) > 4:
        all_species.drop(2, axis=1, inplace=True)
    all_species['binomial'] = all_species[0] + ' ' + all_species[1]

    # Add up the counts for each species
    species_counts = all_species.groupby('binomial')['count'].sum().to_frame()

    print(family, '\t', species_counts['count'].sum(), '\t',
          len(species_counts))
    species_counts.to_csv('./CalFlora/' + family + '_species.csv')

    # For whatever reason, it won't load the next page unless I do this
    browser.get("about:blank")

browser.quit()

# ---------------- OUTPUT ----------------

