#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import pandas as pd
import gtc.mask as g_msk
import gtc.plot as g_plt


def create_tissue_composite_mask(
    orig_img_props: dict,
    masks: dict,
    df_cells: pd.DataFrame,
    df_genes: pd.DataFrame,
    p: dict,
    DEBUG: bool
) -> np.ndarray:

    """Create a mask for the composite (entire) tissue
    as intersection of the masks derived from the positions
    of the genes and cells."""

    method = p['tissue_masks']['composite']['method']

    ####

    mask_cells = g_msk.create_mask_from_df(orig_img_props, df_cells, method, p)  # create mask from cell/gene positions
    mask_genes = g_msk.create_mask_from_df(orig_img_props, df_genes, method, p)

    if DEBUG:
        g_plt.save_resized_image(orig_img_props, mask_cells, 'Control_plot_composite_cell part', p)  # plot small images of cells and genes
        g_plt.save_resized_image(orig_img_props, mask_genes, 'Control_plot_composite_gene part', p)

    mask = cv2.bitwise_and(mask_genes, mask_cells)  # entire tissue mask as intersection of gene and cell masks

    mask = g_msk.morph_operations_and_secure_seal_area(mask, masks['secure seal area'], p, method=method)  # perform blurring, closing, opening and restrict mask area to secure seal area

    return mask

#################################
