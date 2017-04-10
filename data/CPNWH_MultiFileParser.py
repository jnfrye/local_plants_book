"""This is used when you download CSV files from CPNWH in multiple parts
"""

import pandas as pd
import numpy as np

import argparse

# Parse arguments
parser = argparse.ArgumentParser(
    description='Parse CPNWH multiple data files')
parser.add_argument(
    "-r", "--region", type=str, choices=['OR', 'WA'], required=True,
    help="Region to use."
    )
parser.add_argument(
    "-n", "--number_of_files", type=int, required=True,
    help="Number of files to parse"
    )
args = parser.parse_args()
region = args.region
num_files = args.number_of_files

# Read multiple search text files into datasets
folder = 'CPNWH_' + region + '/'
file_prefix = "all_species"
datasets = [
    pd.read_csv(
        './' + folder + 'raw_data/' + \
        file_prefix + "_raw_data" + str(i) + ".txt", sep="\t",
        usecols=["Genus", "Specific Epithet", "Specimen Count"]
        )
    for i in range(1, num_files)
    ]

# Combine the datasets
all_species = pd.concat(datasets, ignore_index=True)

# Some entries have no specific epithet
# (e.g. when the observer could not determine it)
# These show up as NaN; we replace these with a unique text to proceed
all_species = all_species.replace(np.nan, "NAN")
all_species['binomial'] = all_species['Genus'] + ' ' + all_species['Specific Epithet']

# The dataframe is degenerate; this combines those counts
species_counts = all_species.groupby('binomial')['Specimen Count'] \
                            .sum().to_frame()

species_counts.columns = ['count']

species_counts.to_csv('./' + folder + file_prefix + '_species.csv')

