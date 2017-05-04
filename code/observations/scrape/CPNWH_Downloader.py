"""Use this to directly download CPNWH data.

To prevent timeout errors with their server, the data is downloaded from each
herbaria separately.
"""

import pandas as pd
import requests

import argparse
import string


# Parse arguments
parser = argparse.ArgumentParser(
    description='Download CPNWH data into multiple files')
parser.add_argument(
    "-r", "--region", type=str, choices=['OR', 'WA'], required=True,
    help="Region to use."
    )
args = parser.parse_args()
region = args.region

folder = 'CPNWH_' + region + '/raw_data/'
file_prefix = "all_species"

# Gather components of URL
main_url = (
    "http://www.pnwherbaria.org/data/results.php?DisplayAs=Checklist"
    "&DisplayOption=Tab&ExcludeCultivated=Y&GroupBy=ungrouped"
    "&SortBy=ScientificName&SortOrder=ASC&Herbaria="
    )

with open('CPNWH_' + region + '_polygon.txt', 'r') as text_file:
    region_query = text_file.read().strip()

family_url = "&QueryCount=1&Family1="

herbaria = [
    "ALA", "BABY", "BBLM", "BLMMD", "BOIS", "CIC", "CRMO", "EVE", "EWU", "FHL",
    "HJAEF", "HPSU", "HSC", "ID", "IDS", "LEA", "LINF", "MONT", "MONTU", "NY",
    "OSC", "PLU", "PNNL", "PSM", "REED", "RM", "SOC", "SRP", "UAAH", "UBC", "V",
    "VALE", "VIU", "WCW", "WS", "WSTC", "WTU", "WWB"
    ]

# Loop through each herbarium
unknown_error_herbaria = []
empty_herbaria = []
for i, herbarium in enumerate(herbaria):
    print(str(i) + ": \tRequesting herbarium: \t" + herbarium)
    url = main_url + herbarium + region_query
    response = requests.get(url)
    if response.headers['Content-Type'] == 'text/html':
        print("*** No CSV returned!")
        empty_herbaria.append(herbarium)
        continue

    if (response.elapsed.seconds == 30 or
            '<' in response.text or '>' in response.text):
        print("*** HIGHLY LIKELY that this download timed out!")
    if ("Fatal error" in response.text):
        if ("Maximum execution time of 30 seconds exceeded"
                not in response.text):
            print("\t!!! Unknown error; CSV not saved !!!")
            unknown_error_herbaria.append(herbarium)
            continue

        # TODO This code is getting messy, I gotta refactor it a little
        # TODO It's getting confusing because I need to redo the checks above 
        # TODO for each of these new URLs
        # TODO I think it might be easier to add an "alphabet search mode"
        # TODO to the argparse and have the user re-run the script
        print("*** Timeout confirmed.")
        print("*** Splitting requests by first letter of family name...")
        for letter in string.ascii_uppercase:
            family_query = family_url + letter + '%'
            url = main_url + herbarium + family_query + region_query
        continue

    file_path = './' + folder + file_prefix + "_raw_data" + str(i) + ".txt"
    with open(file_path, 'w') as output_file:
        output_file.write(response.text)

if len(empty_herbaria) > 0:
    print("\nSome herbaria did not return CSVs.")
    print("Here is a url to see why:\n")
    print(main_url + ",".join(empty_herbaria) + region_query)

if len(unknown_error_herbaria) > 0:
    print("\nSome herbaria had unknown errors. Deal with these manually:")
    print(unknown_error_herbaria)

