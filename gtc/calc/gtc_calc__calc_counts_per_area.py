#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.function as g_fct


def calc_counts_per_area(
    orig_img_props: dict,
    masks: dict,
    df_counts: pd.DataFrame,
    c: dict
) -> None:

    """Calculate the frequency per area for all gene types in the previously created masks."""

    mask_areas = dict()

    for mask_name in c['all_tissue_mask_names_calc']:
        mask_area_px = np.sum(masks[mask_name] == 255)  # sum up the number of pixels in the masks
        mask_area_rel = mask_area_px / orig_img_props['area_px2']
        mask_areas[mask_name] = mask_area_rel * orig_img_props['area_um2']

        print('-%s: relative area = %3.2f [-], absolute area = %3.2e [px] = %3.2e [um2]'
              % (mask_name, mask_area_rel, int(mask_area_px), mask_areas[mask_name]))

    for mask_name, col_name, new_col_name in zip(c['all_tissue_mask_names_calc'],
                                                 g_fct.df_col_names(c['all_tissue_mask_names_calc'], c['units'][0]),
                                                 g_fct.df_col_names(c['all_tissue_mask_names_calc'], c['units'][2])):

        df_counts[new_col_name] = df_counts[col_name] / mask_areas[mask_name]

#################################
