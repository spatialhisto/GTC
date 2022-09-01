#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.mask as g_msk


def create_tissue_mask(
    orig_img_props: dict,
    masks: dict,
    df_genes: pd.DataFrame,
    tissue: str,
    p: dict
) -> np.ndarray:

    """Build the tissue masks through the defined gene mask sets."""

    method = p['tissue_masks'][tissue]['method']
    gene_set = p['tissue_masks'][tissue]['genes']

    ####

    df_gene = df_genes[df_genes['gene_iss'].isin(gene_set)]  # filter genes for mask

    mask = g_msk.create_mask_from_df(orig_img_props, df_gene, method, p)  # create mask from gene positions

    mask = g_msk.morph_operations_and_secure_seal_area(mask, masks['secure seal area'], p, method=method)  # perform blurring, closing, opening and restrict mask area to secure seal area

    return mask

#################################
