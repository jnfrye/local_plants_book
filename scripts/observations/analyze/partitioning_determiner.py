import argparse
import pandas as pd


def partitions(n: int):
    """Generate partitions of the integer in lexicographic order.
    """
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return

    # modify partitions of n-1 to form partitions of n
    for p in partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]


def find_best_partitioning(
        dataframe: pd.DataFrame, value_column: str,
        partition_size: float, smallest_partition: float) -> pd.DataFrame:
    """Find the partitioning of the data that minimizes the error.

    Args:
        dataframe:
            Dataframe containing the data to be partitioned.
        value_column: 
            Header of the column containing the values
        partition_size:
            Total size of the partitioning
        smallest_partition: 
            All partitionings are multiples of this value

    Returns:
        Dataframe containing the best partitioning for each row
    """
    num_entries = len(dataframe)

    partition_table = pd.DataFrame({
        'partitioning': [0] * num_entries,
        'best_partitioning': [0] * num_entries
        }, index=dataframe.index)

    # Normalize and sort the values
    partition_table['values'] = \
        dataframe[value_column] / dataframe[value_column].sum()
    partition_table.sort_values('values', inplace=True)

    assert (-0.00005 < partition_table['values'].sum() - 1. < 0.00005), \
        "Normalization of partition table failed!"

    # Each partition is checked to see how much error it has against the ideal
    # partitioning, and the best is selected.
    best_error = float("inf")
    for partition in partitions(int(partition_size / smallest_partition)):
        # Fill the rest of the partition with zeros
        partitioning = pd.Series(
            [0] * (num_entries - len(partition)) + list(partition),
            index=partition_table.index)

        partition_table['partitioning'] = partitioning * smallest_partition
        error = sum(
            abs(partition_table['partitioning']
                - partition_table['values'] * partition_size))

        if error < best_error:
            best_error = error
            partition_table['best_partitioning'] = \
                partition_table['partitioning']

        print(error, best_error, " ... ", partition[len(partition) - 4:])

    del partition_table['partitioning']
    # Return only non-zero partitions
    return partition_table[partition_table["best_partitioning"] > 0]


# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Determine the optimal distribution of pages for each genus '
                'and species (for my plant drawing project).')
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

# Each species has a score of how important or common it is
species_table = pd.read_csv(
    './scores/' + family + '_scores.csv', index_col=['genus', 'species'])

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
        print("WARNING: Sum of pages for genus' species does not match target "
              "pages! Excess of", leftover_pages, "pages for genus", genus)

    temp_results.set_index([genus + " " + temp_results.index], inplace=True)
    species_results = species_results.append(temp_results)

# ---------------- OUTPUT ----------------
print("\nGENUS RESULTS\n--------------")
print(genus_results)
print("\nSPECIES RESULTS\n--------------")
print(species_results)

genus_results.to_csv('./partitions/' + family + '_genus_partitions.csv')
species_results.to_csv('./partitions/' + family + '_species_partitions.csv')

