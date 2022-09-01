#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.function as g_fct


def plot_blend_yellow_mask_over_orig_img(
    orig_img_props: dict,
    masks: dict,
    mask_type: str,
    c: dict,
    p: dict,
    alpha_mask: float = 0.6
):

    """Color and overlay each gene and tissue mask with the original
    microscope image and save the result as png-file."""

    rgb_colors = g_plt.rgb_color_dict()

    mask_names = [mask_type + ' ' + mask_name for mask_name in c['tissue_mask_names_calc']]
    if mask_type == 'gene': mask_names = mask_names + ["gene tissue 'composite'", 'secure seal area']

    for mask_name in mask_names:
        if mask_name in masks.keys():  # skip if boundary+center masks do not exist for tissue
            print("-Plot blending for %s" % mask_name)

            img_tmp = g_msk.new_black_color_image(orig_img_props['dims'])

            img_tmp[np.where(masks[mask_name] == 255)] = g_fct.rgb2bgr(rgb_colors['blend'])  # color mask

            img_tmp = g_msk.overlap_img_with_mask(masks['orig dapi image'], img_tmp, alpha_mask)  # alpha blend images

            g_plt.save_resized_image(orig_img_props, img_tmp, 'Plot_blend_yellow_' + mask_name, p)  # plot small image

#################################
