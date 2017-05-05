"""Create a map from the input binomials to their ITIS accepted synonyms.
"""
import pandas as pd

itis_results = pd.read_csv("search_result.csv", encoding = "ISO-8859-1")
