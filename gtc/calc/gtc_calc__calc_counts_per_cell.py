#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import pandas as pd
import gtc.function as g_fct


def calc_counts_per_cell(
    df_counts: pd.DataFrame,
    c: dict
) -> None:

    """Calculate the frequency per cell for all gene types in the previously created masks."""

    for col_name, new_col_name in zip(g_fct.df_col_names(c['all_tissue_mask_names_calc'], c['units'][0]),
                                      g_fct.df_col_names(c['all_tissue_mask_names_calc'], c['units'][1])):

        df_counts[new_col_name] = df_counts[col_name] / df_counts.loc['cells', col_name]

#################################
