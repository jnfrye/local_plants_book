import pandas as pd

import argparse
from difflib import get_close_matches
import os

import PyFloraBook.in_out.data_coordinator as dc
from PyFloraBook.calculate import scalar


# ---------------- GLOBALS ----------------
# These are the weights used to create the final score (a weighted avg)
WEIGHTS = {
    "CalFlora":     1,
    "OregonFlora":  1,
    "CPNWH_OR":     1,
    "CPNWH_WA":     1,
    }
WEBSITES = WEIGHTS.keys()
INPUT_SUFFIX = "species"
OUTPUT_SUFFIX = "scores"

# ---------------- INPUT ----------------
# Parse arguments
parser = argparse.ArgumentParser(
    description='Gather species counts for given families and analyze'
    )
parser.add_argument(
    "-f", "--families", nargs='+',
    help="Names of the families to be analyzed."
    )
args = parser.parse_args()
families = args.families

# Normalize the weights
weights_df = pd.DataFrame.from_dict(WEIGHTS, orient="index")
weights_df.columns = ["weight"]
weights_df['normed'] = \
    weights_df['weight'] / weights_df['weight'].sum(axis=0)

weight_sum = weights_df['normed'].sum(axis=0)
assert scalar.is_normed(weight_sum)

weights_df.drop('weight', axis=1, inplace=True)

# Locate relevant folders
cleansed_data_folder = dc.locate_cleansed_data_folder()
scores_folder = dc.locate_scores_folder()
for family in families:
    # Read data from files
    data_frames = dict()
    for website in WEBSITES:
        website_folder = cleansed_data_folder / website
        website_data_file_name = family + "_" + INPUT_SUFFIX + ".csv"
        data_frames[website] = pd.read_csv(
            str(website_folder / website_data_file_name), index_col=0
            )

    # Normalize data and combine into a single dataframe
    normed_data = pd.DataFrame()
    for key, df in data_frames.items():
        df['normed'] = df['count'] / df['count'].sum(axis=0)

        normed_count_sum = df['normed'].sum(axis=0)
        assert scalar.is_normed(normed_count_sum)

        df.drop('count', axis=1, inplace=True)
        normed_data = pd.concat([normed_data] + [df], axis=1)
        normed_data.columns = list(normed_data.columns[:-1]) + [key]

    # Replace NaN entries with zeros
    normed_data = normed_data.fillna(0)

    # Try to find alternate spellings
    close_matches = []
    indices = list(normed_data.index.values)
    for index in indices:
        matched_pair = get_close_matches(index, indices, cutoff=0.83, n=2)
        if len(matched_pair) > 1 and matched_pair[::-1] not in close_matches:
            close_matches.append(matched_pair)

    # Since the two rows are possibly just different spellings or synonyms,
    # we can confirm this by seeing if the rows are "disjoint"; that is, if
    # no two columns are both nonzero.
    for match in close_matches:
        matched_rows = normed_data.loc[match]

        are_disjoint = not any(
            [all(matched_rows[col] != 0) for col in matched_rows]
            )
        # this code is ghetto but it's used below and I guess it works lol
        if are_disjoint:
            match.append(" *** ")
        else:
            match.append(" ")

    # Merge alternate spellings (if desired)
    while len(close_matches) > 0:
        print(
            "These pairs of species names look similar. "
            "Should any be merged? If prefixed by ***, the rows are 'disjoint'"
            )
        for index, match in enumerate(close_matches):
            print(match[2] + match[0] + "\n" +
                  match[2] + match[1] + " " + str(index) + "\n")

        choices = input(
            "Type index to merge, a space, then 'u'/'d' to merge up/down."
            "\nType -1 to quit.\n"
            ).split()
        index_choice = int(choices[0])
        if index_choice is -1:
            break

        merge_direction = choices[1]
        if merge_direction == 'd':
            sign = -1
        elif merge_direction == 'u':
            sign = +1
        else:
            raise Exception("THIS IS BAD")

        target, replacement = tuple(close_matches[index_choice][:2][::sign])
        del close_matches[index_choice]
        normed_data.loc[target] += normed_data.loc[replacement]
        normed_data.drop([replacement], inplace=True)

    # Create final score column
    normed_data['score'] = normed_data.dot(weights_df)

    normed_data_sum = normed_data['score'].sum(axis=0)
    assert scalar.is_normed(normed_data_sum)

    normed_data.index = pd.MultiIndex.from_tuples(
        list(map(tuple, normed_data.index.str.split())),
        names=("genus", "species")
        )
    print(normed_data["score"].sum(level="genus"))
    print(normed_data['score'])

    scores_file_name = family + '_' + OUTPUT_SUFFIX + ".csv"
    os.makedirs(scores_folder)
    normed_data.to_csv(
        str(scores_folder / scores_file_name), columns=["score"]
        )
