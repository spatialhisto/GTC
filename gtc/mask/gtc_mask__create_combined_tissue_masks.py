#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.function as g_fct


def create_combined_tissue_masks(
    orig_img_props: dict,
    masks: dict,
    mask_type: str,
    c: dict,
) -> np.ndarray:

    """Combine all tissue masks in on mask and
    highlight inside/outside secure seal area."""

    rgb_colors = g_plt.rgb_color_dict()

    img_tmp = g_msk.new_black_color_image(orig_img_props['dims'])  # empty black image

    img_tmp[np.where(masks['secure seal area'] == 255)] = g_fct.rgb2bgr(rgb_colors['empty'])  # inside secure seal area color

    mask_seal_inv = g_msk.invert_binary_mask(masks['secure seal area'])  # invert secure seal area
    img_tmp[np.where(mask_seal_inv == 255)] = g_fct.rgb2bgr(rgb_colors['outside'])  # outside secure seal area color

    for mask_name in c['tissue_mask_names_calc']:
        if not mask_name + ' boundary' in c['tissue_mask_names_calc']:  # skip normal tissue mask if boundary+center masks exist for tissue
            img_tmp[np.where(masks[mask_type + ' ' + mask_name] == 255)] = g_fct.rgb2bgr(rgb_colors[mask_name])  # tissue mask colors

    return img_tmp

#################################
