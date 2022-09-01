#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.mask as g_msk


def create_mask_from_df(
    orig_img_props: dict,
    df: pd.DataFrame,
    method: str,
    p: dict
) -> np.ndarray:

    """Create a mask by the gene/cell positions defined in a dataframe."""

    dot_radius_union = p['tissue_masks']['dot_radius']['union']
    dot_radius_threshold = p['tissue_masks']['dot_radius']['threshold']
    threshold_value = p['tissue_masks']['threshold_value']

    ####

    if method == 'union':
        img_tmp = g_msk.merge_masks_by_threshold(orig_img_props, df, dot_radius_union, 0.0, p)

    elif method == 'threshold':
        img_tmp = g_msk.merge_masks_by_threshold(orig_img_props, df, dot_radius_threshold, threshold_value, p)

    else:
        raise ValueError("The wrong value '%s' for 'method' - Check 'Gtc-Parameters' file!" % method)

    return img_tmp

#################################
