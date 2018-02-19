import pandas as pd

import argparse
import os

import PyFloraBook.in_out.data_coordinator as dc


# ---------------- GLOBALS ----------------
WEBSITE = 'OregonFlora'
OUTPUT_SUFFIX = 'species'

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Count the observed species'
    )
parser.add_argument(
    "-f", "--families", nargs='+',
    help="Names of the families to be analyzed."
    )
args = parser.parse_args()
families = args.families

subfolder = WEBSITE
raw_data_folder = dc.locate_raw_observations_folder() / subfolder
cleansed_data_folder = dc.locate_cleansed_data_folder() / subfolder
for family in families:
    input_file_name = family + ".csv"
    input_file_path = raw_data_folder / input_file_name
    try:
        data = pd.read_csv(str(input_file_path), encoding="ISO-8859-1")
    except FileNotFoundError:
        print(family, "not found!")
        continue
    # Sanity check: make sure the file contains data for the right family
    if data['family'][0] != family:
        print(data['family'][0], "!=", family)
        continue

    # Get rid of the weird "image" rows
    data = data[data['data_type'] != 'image']
    # Get rid of any data from the wrong counties
    excluded_counties = [
        "Baker", "Crook", "Gilliam", "Grant", "Harney", "Lake", "Malheur",
        "Morrow", "Sherman", "Umatilla", "Union", "Wallowa", "Wheeler"
        ]
    for county in excluded_counties:
        data = data[data['county'] != county]

    all_observed = data['taxon'].to_frame()

    # ---------------- ANALYSIS ----------------
    # Fix troublesome hybrid symbols
    all_observed = all_observed['taxon'].str.replace('× ', '×').to_frame()
    # Split into columns to get rid of variety information
    all_observed = all_observed['taxon'].str.split(' ', expand=True, n=2)
    if len(all_observed.columns) > 2:
        all_observed.drop(2, axis=1, inplace=True)
    all_observed['binomial'] = all_observed[0] + ' ' + all_observed[1]

    # This is the number of observations of each species
    species_counts = all_observed['binomial'].value_counts().to_frame()
    species_counts.rename(columns={'binomial': 'count'}, inplace=True)
    species_counts.index.name = 'binomial'
    species_counts.sort_index(inplace=True)

    # ---------------- OUTPUT ----------------
    print(family, '\t', len(all_observed), '\t', len(species_counts))

    cleansed_data_file_name = family + '_' + OUTPUT_SUFFIX + '.csv'
    os.makedirs(cleansed_data_folder)
    species_counts.to_csv(str(cleansed_data_folder / cleansed_data_file_name))
