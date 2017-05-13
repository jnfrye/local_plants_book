"""Use this to directly download CPNWH data.

To prevent timeout errors with their server, the data is downloaded from each
herbaria separately.
"""

import argparse
import string

import requests

import PyFloraBook.input_output.data_coordinator as dc


# Globals
# These are URL queries
QUERIES = {
    "polygon": "&PolygonCount=1&Polygon1=",
    "herbaria": "&Herbaria=",
    "family": "&Family1=",
}

HERBARIA = [
    "ALA", "BABY", "BBLM", "BLMMD", "BOIS", "CIC", "CRMO", "EVE", "EWU", "FHL",
    "HJAEF", "HPSU", "HSC", "ID", "IDS", "LEA", "LINF", "MONT", "MONTU", "NY",
    "OSC", "PLU", "PNNL", "PSM", "REED", "RM", "SOC", "SRP", "UAAH", "UBC", "V",
    "VALE", "VIU", "WCW", "WS", "WSTC", "WTU", "WWB"
    ]

MAIN_URL = (
    "http://www.pnwherbaria.org/data/results.php?DisplayAs=Checklist"
    "&DisplayOption=Tab&ExcludeCultivated=Y&GroupBy=ungrouped"
    "&SortBy=ScientificName&SortOrder=ASC&QueryCount=1"
    "&Zoom=7&Lat=46.71797026962876&Lng=-123.013916015625"
    )

OUTPUT_FILE_PREFIX = "all_species"

# Parse arguments
PARSER = argparse.ArgumentParser(
    description='Download CPNWH data into multiple files')
PARSER.add_argument(
    "-r", "--region", type=str, choices=['OR', 'WA'], required=True,
    help="Region to use."
    )
args = PARSER.parse_args()
region = args.region

site_name = 'CPNWH_' + region
# Load polygon file
script_path = dc.locate_current_script_folder()
polygon_file_name = site_name + '_polygon.txt'
polygon_file_path = script_path / polygon_file_name
with polygon_file_path.open(mode='r') as polygon_file:
    polygon = polygon_file.read().strip()

# Gather components of URL
region_url = MAIN_URL + QUERIES["polygon"] + polygon

output_path = dc.locate_raw_data_folder()

unknown_error_herbaria = []
empty_herbaria = []
for i, herbarium in enumerate(HERBARIA):
    print(str(i) + ": \tRequesting herbarium: \t" + herbarium)
    herbarium_url = region_url + (QUERIES["herbaria"] + herbarium)
    response = requests.get(herbarium_url)
    if response.headers['Content-Type'] == 'text/html':
        print("*** No CSV returned!")
        empty_herbaria.append(herbarium)
        continue

    if (response.elapsed.seconds == 30 or
            '<' in response.text or '>' in response.text):
        print("*** HIGHLY LIKELY that this download timed out!")
    if "Fatal error" in response.text:
        if ("Maximum execution time of 30 seconds exceeded"
                not in response.text):
            print("\t!!! Unknown error; CSV not saved !!!")
            unknown_error_herbaria.append(herbarium)
            continue

        # TODO I need to redo the checks above for each of these new URLs
        # TODO Maybe add an "alphabet search mode" to the argparse
        print("*** Timeout confirmed.")
        print("*** Splitting requests by first letter of family name...")
        for letter in string.ascii_uppercase:
            alphabetical_query = QUERIES["family"] + letter + '%'
            alphabetical_url = herbarium_url + alphabetical_query
        continue

    file_name = OUTPUT_FILE_PREFIX + "_part" + str(i) + ".txt"
    file_path = output_path / site_name / file_name
    with file_path.open(mode='w') as output_file:
        output_file.write(response.text)

if len(empty_herbaria) > 0:
    print("\nSome herbaria did not return CSVs.")
    print("Here is a url to see why:\n")
    print(region_url + QUERIES["herbaria"] + ",".join(empty_herbaria))

if len(unknown_error_herbaria) > 0:
    print("\nSome herbaria had unknown errors. Deal with these manually:")
    print(unknown_error_herbaria)
