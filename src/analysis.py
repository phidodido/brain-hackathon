import pandas as pd
import numpy as np


def get_numerical_columns(df: pd.DataFrame) -> list:
    number_cols = df.columns[df.dtypes.astype(str) == 'float64']
    # cat_cols = [x for x in dfi.columns if x not in number_cols]
    
    return number_cols

def get_bins(ss: pd.Series, how: str = 'center', bins: int = 10) -> pd.Series:
    cut = pd.cut(ss, bins=bins)

    left = np.array([x.right if pd.notnull(x) else np.nan for x in cut])
    if how == 'left':
        return left
    
    right = np.array([x.right if pd.notnull(x) else np.nan for x in cut])
    if how == 'right':
        return right
    
    center = (left + right)/2
    
    return center


def make_counts(df: pd.DataFrame, variable: str,
                 bins: int = 10, top: int = 10) -> pd.Series:
    number_cols = get_numerical_columns(df)
        
    if variable in number_cols:
        vals = get_bins(df[variable], how='center', bins=bins)
        ssv = pd.Series(vals, name=variable)
    else:
        ssv = df[variable]
    
    ss = ssv.value_counts()
    
    if len(ss) > top:
        ss = ss.sort_values(ascending=False)[:top]
    
    return ss


def make_groupby(df: pd.DataFrame, variable: str, groupby: str, 
                 bins: int = 10, top: int = 10) -> pd.Series:
    number_cols = get_numerical_columns(df)
    
    if variable in number_cols:
        agg_func = 'mean'
    else:
        agg_func = 'count'
    
    if groupby in number_cols:
        gr_col = get_bins(df[groupby], how='center', bins=bins)
    else:
        gr_col = groupby
    
    ss = df.groupby(gr_col)[variable].agg(agg_func)
    ss.name = variable
    ss.index.name = groupby
    
    if len(ss) > top:
        ss = ss.sort_values(ascending=False)[:top]

    return ss