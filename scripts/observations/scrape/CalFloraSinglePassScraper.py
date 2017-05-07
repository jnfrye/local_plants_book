"""Use this to scrape results of searching CalFlora for ALL species in the area.
"""

from bs4 import BeautifulSoup
import pandas as pd


soup = BeautifulSoup(open("./CalFlora/all_species_search.html"), "lxml")

results_table = soup.find(id="resultSlot")

# This is an iterator that covers all the data rows
data_rows = list(results_table.table.tbody.children)[1].td.table.tbody.children

extracted_data = []
for row in data_rows:
    species_name = row.find(title="plant details").div.contents[0]
    species_count = int(
        row.find(title="display points").div.contents[0].split()[0]
        )
    extracted_data.append((species_name, species_count))

all_species = pd.DataFrame(extracted_data, columns=["full_name", "count"])
all_species.to_csv(
    "./CalFlora/all_species_raw_data.csv", columns=['full_name', 'count'],
    index=False
    )
print("DONE!")
