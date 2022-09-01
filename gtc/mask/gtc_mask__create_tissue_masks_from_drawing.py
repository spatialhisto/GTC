#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import gtc.mask as g_msk
import gtc.function as g_fct


def create_tissue_masks_from_drawing(
    orig_img_props: dict,
    masks: dict,
    tissue_type: str,
    p: dict,
    tol: int = 10
):

    """Create a mask for the composite (entire) tissue
    as intersection of the masks derived from the positions
    of the genes and cells."""

    color_bgr = g_fct.rgb2bgr(np.array(p['rgb_colors_drawn_masks'][tissue_type]))  # change color mode
    mask_tmp = cv2.inRange(masks['orig drawn tissue mask image'], color_bgr - tol, color_bgr + tol)  # threshold rgb color +/- tol, values 0 and 255 for False and True

    mask_tmp = g_msk.resize_img(mask_tmp, orig_img_props['dims'])  # enlarge tissue masks to microscope image sizes

    mask_tmp = cv2.bitwise_and(mask_tmp, masks['secure seal area'])  # restrict valid area for gene/cell counting to secure seal area

    return mask_tmp

#################################
