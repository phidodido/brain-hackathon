import os
import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Union, Dict


def read_dir_files(folder_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    """Read all Excel and CSV files in a folder."""
    folder_path = Path(folder_path)
    d = {}
    for fn in sorted(os.listdir(folder_path)):
        fp = folder_path/fn
        if fn.endswith('xlsx'):
            df = pd.read_excel(fp)
        elif fn.endswith('csv'):
            df = pd.read_csv(fp)
        d[fn] = df
    
    return d


def read_variables(folder_path: Union[str, Path]) -> pd.DataFrame:
    """Read and combine all files in the i/e_Variables_gm folder."""
    d = read_dir_files(folder_path)
    
    df = (
        pd.concat(d)
        .assign(
            Number=lambda x: x.index.get_level_values(0).astype(str).str.findall(r'\d+').str[0].astype(int)
        )
        .reset_index(drop=True)
        .set_index('Number').reset_index()
    )
    
    return df

