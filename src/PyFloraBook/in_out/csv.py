import os
from typing import List

import pandas as pd


def write(
        folder: os.path,
        filename: str,
        dataframe: pd.DataFrame,
        columns: List[str]
        ) -> None:

    os.makedirs(folder)
    dataframe.to_csv(
        folder / filename,
        columns=columns, index=False
        )
