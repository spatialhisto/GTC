#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.function as g_fct


def create_df_for_count_statistics(
    c: dict
) -> pd.DataFrame:

    """Create the dataframe for the
    cell and gene count statistic
    of the tissues."""

    df_counts = pd.DataFrame(0,
                             index=np.arange(len(['cells'] + c['gene_names_iss'])),
                             columns=g_fct.df_col_names(c['all_tissue_mask_names_calc'], c['units'][0]),
                             dtype=int)  # create columns

    df_counts.index = ['cells'] + c['gene_names_iss']  # create row indices

    return df_counts

#################################
