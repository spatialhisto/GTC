#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.setup as g_set


def read_csv_data(
    fname: str,
    cols: list,
    drop_cols: list,
    img_scale_factor: int,
    sep: str = ','
) -> pd.DataFrame:

    """Read csv data file, rename columns, drop columns
    and divide the coordinates by img_scale_factor."""

    df_raw = pd.read_csv(fname, sep=sep, engine='python')
    df_raw.columns = cols
    df_raw.dropna(inplace=True)
    df_raw = df_raw.astype({'row': 'int', 'col': 'int'})  # cast to integer

    df_raw.drop(columns=drop_cols, inplace=True)  # drop columns

    df_raw = g_set.divide_df_coords_by_rescale_factor(df_raw, img_scale_factor)  # divide cell/gene coordinates by img_scale_factor

    return df_raw

#################################
