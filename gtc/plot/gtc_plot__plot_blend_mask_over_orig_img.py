#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import gtc.mask as g_msk
import gtc.plot as g_plt


def plot_blend_mask_over_orig_img(
    orig_img_props: dict,
    masks: dict,
    mask_name: str,
    p: dict,
    alpha_mask: float = 0.6
):

    """Plot a mask over the microscope image."""

    img_tmp = g_msk.overlap_img_with_mask(masks['orig dapi image'], masks[mask_name], alpha_mask)  # alpha blend images

    g_plt.save_resized_image(orig_img_props, img_tmp, 'Plot_blend_' + mask_name, p)  # plot small image

#################################
