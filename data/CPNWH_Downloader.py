"""Use this to directly download CPNWH data.

To prevent timeout errors with their server, the data is downloaded from each
herbaria separately.
"""

import pandas as pd
import requests

import argparse


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
    region_url = text_file.read().strip()

herbaria = [
    "ALA", "BABY", "BBLM", "BLMMD", "BOIS", "CIC", "CRMO", "EVE", "EWU", "FHL",
    "HJAEF", "HPSU", "HSC", "ID", "IDS", "LEA", "LINF", "MONT", "MONTU", "NY",
    "OSC", "PLU", "PNNL", "PSM", "REED", "RM", "SOC", "SRP", "UAAH", "UBC", "V",
    "VALE", "VIU", "WCW", "WS", "WSTC", "WTU", "WWB"
    ]

# Loop through each herbarium
timed_out_herbaria = []
erroneous_herbaria = []
for i, herbarium in enumerate(herbaria):
    print(str(i) + ": \tRequesting herbarium: \t" + herbarium)
    url = main_url + herbarium + region_url
    response = requests.get(url)
    if response.headers['Content-Type'] == 'text/html':
        print("*** No CSV returned!")
        erroneous_herbaria.append(herbarium)
        continue

    if (response.elapsed.seconds == 30 or
            '<' in response.text or '>' in response.text):
        print("*** HIGHLY LIKELY that this download timed out!")
    if ("Fatal error" in response.text):
        if ("Maximum execution time of 30 seconds exceeded" in response.text):
            print("\t!!! DOWNLOAD DEFINITELY TIMED OUT !!!")
        print("*** CSV not saved!")
        timed_out_herbaria.append(herbarium)
        continue

    file_path = './' + folder + file_prefix + "_raw_data" + str(i) + ".txt"
    with open(file_path, 'w') as output_file:
        output_file.write(response.text)

if len(erroneous_herbaria) > 0:
    print("\nSome herbaria did not return CSVs.")
    print("Here is a url to see why:\n")
    print(main_url + ",".join(erroneous_herbaria) + region_url)

if len(timed_out_herbaria) > 0:
    print("\nSome herbaria timed out. Deal with these manually:")
    print(timed_out_herbaria)

