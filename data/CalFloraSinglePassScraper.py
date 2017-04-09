"""Use this to parse results of searching CalFlora for ALL species in the area.
"""

from bs4 import BeautifulSoup
import pandas as pd


soup = BeautifulSoup(open("./CalFlora/all_species_search.html"))

results_table = soup.find(id="resultSlot")

# This is an iterator that covers all the data rows
data_rows = list(results_table.table.tbody.children)[1].td.table.tbody.children

extracted_data = []
for row in data_rows:
    species_name = row.find(title="plant details").div.contents[0]
    species_count = int(
        row.find(title="display points").div.contents[0].split()[0]
        )
    extracted_data.append((species_name, [species_count]))

df = pd.DataFrame.from_items(extracted_data, orient='index', columns=["count"])
df.index.name = "name"

df.to_csv("./CalFlora/all_species_counts.csv")

