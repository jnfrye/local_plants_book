from selenium import webdriver
import pandas as pd

import argparse
from observations.scrape.common import scraping

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Scrape CPNWH for species counts for given family and region')
parser.add_argument("-f", "--families", nargs='+',
    help="Names of the families to be analyzed.")
parser.add_argument("-r", "--region", type=str, choices=['OR', 'WA'],
    help="Region to use.")
args = parser.parse_args()
families = args.families
region = args.region

# ---------------- SCRAPING ----------------
print("Opening browser...")
browser = webdriver.Firefox()
browser.set_window_size(500, 300)
browser.set_window_position(200, 200)
browser.set_page_load_timeout(20)

main_url = (
    "http://www.pnwherbaria.org/data/results.php?DisplayAs=Checklist&"
    "DisplayOption=HTML&ExcludeCultivated=Y&GroupBy=ungrouped&"
    "SortBy=Year&SortOrder=DESC&SearchAllHerbaria=Y&QueryCount=1&Family1="
    )

with open('CPNWH_' + region + '_polygon.txt', 'r') as text_file:
    region_url = text_file.read().strip()

for family in families:
    # Load the webpage
    try:
        browser.get(main_url + family + region_url)

    scraping.wait_for_load(browser, "CLASS_NAME", "checklistnotes")

    # Download the rows in the species data table
    # Next we skip the first three rows because they contain nonsense
    data_rows = browser.find_elements_by_class_name("checklisttaxon")

    # Extract the species counts

    species_list = []
    for row in data_rows:
        italic_entries = row.find_elements_by_tag_name("i")
        # The first two italics entries are the genus and species name
        # If there is only one italic entry, it is just the genus and
        # should be discarded
        assert len(italic_entries) > 0
        if len(italic_entries) == 1:
            continue
        binomial = italic_entries[0].text + " " + italic_entries[1].text

        # Check for abnormalities in binomial
        if binomial[0].islower():
            print("WARNING: binomial started with a lowercase!: " + binomial)
            accept_entry = input("Accept entry? y/n: ")
            if accept_entry == 'n':
                continue
            elif accept_entry == 'y':
                pass
            else:
                raise Exception("Must respond 'y' or 'n'!")

        count = int(row.find_element_by_tag_name("b").text)
        species_list.append((binomial, count))

    # ---------------- ANALYSIS ----------------
    # Convert to friendly format for writing CSV
    all_species = pd.DataFrame(species_list, columns=["binomial", "count"])

    # Add up the counts for each species
    species_counts = all_species.groupby('binomial')['count'].sum().to_frame()

    print(
        family, '\t', species_counts['count'].sum(), '\t', len(species_counts)
        )
    species_counts.to_csv('./CPNWH_' + region + '/' + family + '_species.csv')

    # For whatever reason, it won't load the next page unless I do this
    browser.get("about:blank")

browser.quit()

