import argparse
import pandas as pd

import PyFloraBook.input_output.data_coordinator as dc
from PyFloraBook.threshold.partition import find_best_partitioning


# ---------------- GLOBALS ----------------
INPUT_SUFFIX = "scores"
OUTPUT_SUFFIX = "partitions"

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Determine the optimal distribution of pages for each genus '
                'and species (for my plant drawing project).'
    )
parser.add_argument("family", help="Name of the family to be analyzed.")
parser.add_argument(
    "total_pages", type=int,
    help="Total number of pages devoted to this family."
    )
parser.add_argument(
    "-g", "--min_page_per_genus", type=float, default=1,
    help="Minimum portion of a page each genus should have."
         "This must be an integer fraction of 1! (like 1/2)"
    )
parser.add_argument(
    "-s", "--min_page_per_species", type=float, default=1,
    help="Minimum portion of a page each species should have."
         "This must be an integer fraction of 1! (like 1/2)"
    )
parser.add_argument(
    "-c", "--constant_species_pages", type=bool, default=True,
    help="If true, every species that scores high enough will get "
         "the same portion of pages devoted to it; specifically, "
         "whatever --min_page_per_species is set to."
    )
args = parser.parse_args()

total_pages = args.total_pages
min_page_per_genus = args.min_page_per_genus
min_page_per_species = args.min_page_per_species
family = args.family
constant_species_pages = args.constant_species_pages

# Locate input/output paths
scores_folder = dc.locate_scores_folder()
selections_folder = dc.locate_selections_folder()

# Each species has a score of how important or common it is
scores_file_name = family + '_' + INPUT_SUFFIX + '.csv'
species_table = pd.read_csv(
    str(scores_folder / scores_file_name),
    index_col=['genus', 'species']
    )

# ---------------- ANALYSIS ----------------
# If the pages were partitioned exactly in proportion, this would be the result
genus_scores_series = species_table['score'].sum(level='genus')
genus_scores = pd.DataFrame(  # XXX This is ghetto but it works
    data={'score': genus_scores_series.values},
    index=genus_scores_series.index)

genus_results = find_best_partitioning(
    genus_scores, 'score', total_pages, min_page_per_genus)

species_results = pd.DataFrame()
for genus in genus_results.index:
    pages_for_this_genus = genus_results.loc[genus]["best_partitioning"]

    if constant_species_pages:
        species_to_pick = int(pages_for_this_genus / min_page_per_species)
        temp_results = species_table.loc[genus].nlargest(
            species_to_pick, 'score'
            )
        temp_results["best_partitioning"] = min_page_per_species
    else:
        temp_results = find_best_partitioning(
            species_table, 'score', pages_for_this_genus, min_page_per_species
            )

    # Check if there's some unasigned portion of this genus' pages
    leftover_pages = pages_for_this_genus - \
        temp_results['best_partitioning'].sum()
    if leftover_pages != 0:
        print("WARNING: Sum of pages for genus' species does not match "
              "target pages! Excess of", leftover_pages, "pages for genus",
              genus)

    temp_results.set_index([genus + " " + temp_results.index], inplace=True)
    species_results = species_results.append(temp_results)

# ---------------- OUTPUT ----------------
print("\nGENUS RESULTS\n--------------")
print(genus_results)
print("\nSPECIES RESULTS\n--------------")
print(species_results)

genus_output_name = family + '_genus_' + OUTPUT_SUFFIX + '.csv'
species_output_name = family + '_species_' + OUTPUT_SUFFIX + '.csv'
genus_results.to_csv(str(selections_folder / genus_output_name))
species_results.to_csv(str(selections_folder / species_output_name))

