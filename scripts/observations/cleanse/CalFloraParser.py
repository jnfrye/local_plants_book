import pandas as pd

import argparse
import os

import PyFloraBook.in_out.data_coordinator as dc


# ---------------- GLOBALS ----------------
WEBSITE = "CalFlora"
INPUT_SUFFIX = "raw_data"
OUTPUT_SUFFIX = "species"

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Parse CalFlora datasets for given families species counts'
    )
parser.add_argument(
    "-f", "--families", nargs='+',
    help="Names of the families to be analyzed. "
         "Enter 'all_species' to do that file!"
    )
args = parser.parse_args()
families = args.families

subfolder = WEBSITE
raw_data_folder = dc.locate_raw_counts_folder() / subfolder
cleansed_data_folder = dc.locate_cleansed_data_folder() / subfolder
for family in families:
    # Remove the variety info
    raw_data_file = raw_data_folder / (family + "_" + INPUT_SUFFIX + ".csv")
    all_species = pd.read_csv(str(raw_data_file))

    # Strip the 'variety' and 'subspecies' nomenclature
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

    # Output
    print(family, '\t', species_counts['count'].sum(), '\t',
          len(species_counts))
    cleansed_data_file = \
        cleansed_data_folder / (family + '_' + OUTPUT_SUFFIX + '.csv')
    os.makedirs(cleansed_data_folder)
    species_counts.to_csv(str(cleansed_data_file))
