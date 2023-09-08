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
            Individual=lambda x: x.index.get_level_values(0).astype(str).str.findall(r'\d+').str[0].astype(int)
        )
        .reset_index(drop=True)
        .set_index('Individual').reset_index()
    )
    
    return df


def read_invivo_gm() -> pd.DataFrame:
    """Variables gm"""
    df = (
        read_variables('./data/invivo/i_Variables_gm')
        .replace(np.inf, np.nan)
    )

    return df


def read_invivo_info() -> pd.DataFrame:
    """Individual information"""
    df = (
        pd.read_excel('./data/invivo/i_Individual_List/individual_information_invivo.xlsx')
        .dropna(axis=1, how='all')
        .assign(Individual = lambda x: x['In vivo Database Number'])
    )
    df.loc[df['Weight'] == '304,3', 'Weight'] = 304

    return df


def read_exvivo_gm() -> pd.DataFrame:
    """Variables gm"""
    df = (
        read_variables('./data/exvivo/e_Variables_gm')
        .replace('-', np.nan)
        .replace(np.inf, np.nan)
    )
    df['Volume (mm^3)'] = df['Volume (mm^3)'].astype(float)
    df.loc[df['Volume (mm^3)'] > 1_000, 'Volume (mm^3)'] = np.nan
    
    return df


def read_exvivo_info() -> pd.DataFrame:
    """Individual information"""
    df = (
        pd.read_excel('./data/exvivo/e_Individual_List/individual_information_exvivo.xlsx')
        .dropna(axis=1, how='all')
        .assign(Individual = lambda x: x['ex vivo Database Number'].str.replace('ex', '').astype(int))
        .drop(columns=['HR-T2WI Image'])
    )

    return df


def combine_data(df_gm: pd.DataFrame, df_info: pd.DataFrame) -> pd.DataFrame:
    """Combine ex vivo data."""
    df = (
        df_gm
        .merge(df_info, on='Individual', how='left')
    )
    
    return df


def store_data(dfi: pd.DataFrame, dfe: pd.DataFrame):
    os.makedirs('./data/store', exist_ok=True)

    dfi.to_feather('./data/store/invivo.feather')
    dfe.to_feather('./data/store/exvivo.feather')


def create_store():
    dfe_gm = read_exvivo_gm()
    dfe_info = read_exvivo_info()
    dfe = combine_data(dfe_gm, dfe_info)
    
    dfi_gm = read_invivo_gm()
    dfi_info = read_invivo_info()
    dfi = combine_data(dfi_gm, dfi_info)

    store_data(dfi, dfe)


def check_store() -> bool:
    fpi = './data/store/invivo.feather'
    fpe = './data/store/exvivo.feather'
    if not Path(fpi).exists() or not Path(fpe).exists():
        return False
    return True


def read_store() -> tuple:
    dfi = pd.read_feather('./data/store/invivo.feather')
    dfe = pd.read_feather('./data/store/exvivo.feather')

    return dfi, dfe
