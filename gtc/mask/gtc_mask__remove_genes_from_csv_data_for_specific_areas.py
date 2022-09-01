#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import pandas as pd
import gtc.mask as g_msk
import gtc.function as g_fct


def remove_genes_from_csv_data_for_specific_areas(
    orig_img_props: dict,
    masks: dict,
    df_genes: pd.DataFrame,
    tol: int = 10
):

    """Remove genes from csv data in specific areas,
     because the number of genes are not representive
     due to microscoping problems."""

    rgb_color_to_remove = [30, 218, 230]  # color turquis in drawn masks

    ####

    color_bgr = g_fct.rgb2bgr(np.array(rgb_color_to_remove))  # change color mode
    mask_remove = cv2.inRange(masks['orig drawn tissue mask image'], color_bgr - tol, color_bgr + tol)  # threshold rgb color +/- tol, values 0 and 255 for False and True

    mask_remove = g_msk.resize_img(mask_remove, orig_img_props['dims'])  # enlarge masks to microscope image sizes

    within_remove_mask = [mask_remove[x, y] == 255 for x, y in zip(df_genes['row'], df_genes['col'])]

    print('Removed %d genes from dataset' % sum(within_remove_mask))

    genes_to_keep = [(not gene) for gene in within_remove_mask]
    df_genes = df_genes[genes_to_keep]

    return df_genes

#################################
