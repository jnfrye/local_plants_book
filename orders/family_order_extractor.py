import pandas as pd

import string
import logging


with open("APG_IV_families_and_orders.txt", 'r') as input_file:
    family_info_lines = [l.strip().split(' = ') for l in input_file.readlines()]

logging.info("Extract all non-latin characters found in input")
all_characters = set()
for line in family_info_lines:
    text = "".join(line)
    characters = set(text)
    all_characters |= characters

logging.info("Check for any lines that have non-latin characters")
non_latin_characters = all_characters - set(string.ascii_letters)
if len(non_latin_characters) > 0:
    raise ValueError(
        "Non-latin characters [{}] found in input!".format(
            ", ".join(non_latin_characters)
            )
        )

logging.info("Assemble dictionary of synonyms and orders of accepted families")
orders_of_families = {}
family_synonyms = {}
for line in family_info_lines:
    family = line[0]

    # Perform some formatting checks
    if not family.istitle():
        raise ValueError(
            '(' + family + ') is not capitalized properly!'
            )
    if family[-5:] != 'aceae':
        raise ValueError(
            '(' + family + ') does not end in "aceae"!'
            )

    elif len(line) == 3:
        # This is a synonym of an accepted family
        synonym = line[1]
        family_synonyms[family] = synonym
    elif len(line) == 2:
        # This is an accepted family, so save its order
        order = line[1]

        # Perform some formatting checks
        if not order.istitle():
            raise ValueError(
                '(' + order + ') is not capitalized properly!'
                )
        if order[-4:] != 'ales':
            raise ValueError(
                '(' + order + ') does not end in "ales"!'
                )

        orders_of_families[family] = order
    else:
        raise ValueError(
            'Line in input file has incorrect number of items: ' + str(line))

with open("local_families.txt", 'r') as my_file:
    my_families = my_file.read().splitlines()

logging.info("For all accepted families, get their orders")
local_orders = {}
for family in my_families:
    try:
        local_orders[family] = orders_of_families[family]
    except KeyError:
        print(family + " is not an accepted family!")

logging.info("Save the local family orders")
local_orders_df = pd.DataFrame.from_dict(local_orders, orient='index')
local_orders_df.index.name = "family"
local_orders_df.columns = ["order"]
local_orders_df.to_csv("local_families_and_orders.csv")

