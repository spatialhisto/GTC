#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.function as g_fct


def create_overlap_neoplastic_tissue_masks_image(
    orig_img_props: dict,
    masks: dict
) -> np.ndarray:

    """Show overlap of neoplastic tissue masks created
    by drawing and by genes through an colored image:
    dark red: overlap of both masks (A and B)
    light red: non-overlap drawn mask (A \ B)
    pink: non-overlap gene based mask (B \ A)."""

    rgb_colors = g_plt.rgb_color_dict()

    A = masks["drawn tissue 'neoplastic'"] == 255
    B = masks["gene tissue 'neoplastic'"] == 255

    img_tmp = g_msk.new_black_color_image(orig_img_props['dims'])  # empty black image

    mask_tmp = 255 * np.logical_and(A, B)  # overlap
    img_tmp[np.where(mask_tmp == 255)] = g_fct.rgb2bgr(rgb_colors['mask_overlap'])

    mask_tmp = 255 * np.logical_and(A, np.logical_not(B))  # A \ B
    img_tmp[np.where(mask_tmp == 255)] = g_fct.rgb2bgr(rgb_colors['only_mask_A'])

    mask_tmp = 255 * np.logical_and(B, np.logical_not(A))  # B \ A
    img_tmp[np.where(mask_tmp == 255)] = g_fct.rgb2bgr(rgb_colors['only_mask_B'])

    return img_tmp

#################################
