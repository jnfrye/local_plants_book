import os
from typing import List

import pandas as pd


def write(
        folder: os.path,
        filename: str,
        dataframe: pd.DataFrame,
        columns_to_write: List[str] = None,
        write_row_names: bool = True,
        ) -> None:

    os.makedirs(folder, exist_ok=True)
    dataframe.to_csv(
        folder / filename,
        columns=columns_to_write, index=write_row_names
        )
