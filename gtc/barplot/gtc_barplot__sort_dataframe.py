#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd


def sort_dataframe(
    plot_type: str,
    df_unit: pd.DataFrame,
    col_names: list,
    p: dict,
) -> pd.DataFrame:

    """Re-arrange order of the dataframe either alphabetically by the gene
    names or descending by the gene count values."""

    sort_genes_by = p['barplot_props']['sort_genes_by']

    ####

    df_tmp = df_unit.copy(deep=True)

    if sort_genes_by == 'value':  # sort by index of reference column
        if plot_type == 'grouped':
            df_col = df_tmp[col_names].max(axis=1)  # max value over all columns of subset
        else:
            df_col = df_tmp[col_names].sum(axis=1)  # sum over all columns of subset

        df_col.sort_values(ascending=False, inplace=True)

        df_tmp = df_tmp.reindex(index=df_col.index)

    else:  # sort_genes_by == 'letter':
        df_tmp.sort_values(by=['genes'], inplace=True)  # sort alphabetically

    df_tmp.reset_index(drop=True, inplace=True)  # reset row index

    return df_tmp

#################################
