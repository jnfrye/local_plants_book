"""Create a map from the input binomials to their ITIS accepted synonyms.
"""
import pandas as pd

from PyFloraBook.in_out.data_coordinator import locate_nomenclature_folder


# Globals
INPUT_FILE_NAME = "search_results.csv"

# Input
nomenclature_folder = locate_nomenclature_folder()
itis_results = pd.read_csv(
    str(nomenclature_folder / INPUT_FILE_NAME), encoding="ISO-8859-1")
