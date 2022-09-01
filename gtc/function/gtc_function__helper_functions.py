#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
from typing import Union


def df_col_names(
    mask_names: Union[list, str],
    unit: str = ''
) -> list:

    """Create dataframe column names from mask names."""

    def ensure_is_list(arg):  # if string and not list return string
        return arg if isinstance(arg, list) else [arg]

    if len(ensure_is_list(mask_names)) == 1:
        col_names = 'Counts in ' + mask_names + ' ' + unit
    else:
        col_names = ['Counts in ' + mask_name + ' ' + unit for mask_name in mask_names]

    return col_names


####


def prepare_df_for_plots(
    df_counts: pd.DataFrame
):

    """Drop the row 'cells' from the dataframe for the barplots."""

    df_counts.drop(['cells'], inplace=True)  # remove row 'cells from dataframe
    df_counts.index.name = 'genes'  # row index 'genes' as column
    df_counts.reset_index(inplace=True)  # reset row index


####


def switch_coordinates(
    coords: Union[list, tuple]
) -> Union[list, tuple]:

    """Switch coordinates (x,y) to (y,x) for opencv functions."""

    new_coords = coords[::-1]

    return new_coords


####


def merge_lists_no_duplicates(
    a: list,
    b: list
) -> list:

    """Combine two lists without duplicates."""

    c = list(set(a + b))

    return c

#################################
