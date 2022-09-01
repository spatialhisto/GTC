#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import gtc.mask as g_msk
import gtc.function as g_fct
from math import floor


def create_secure_seal_area_mask(
    orig_img_props: dict,
    p: dict
) -> np.ndarray:

    """The secure seal area for in-situ sequencing on the
    microscope slide has the shape of a disc. Here, a mask
    in form of a disc is created which defines the valid area
    for genes and cell counting."""

    move_in_secure_seal = p['move_in_secure_seal']

    ####

    mask = g_msk.new_black_binary_image(orig_img_props['dims'])  # empty black binary image

    row_center = floor(orig_img_props['rows'] / 2)  # center of the microscope image
    col_center = floor(orig_img_props['cols'] / 2)

    radius = min(row_center, col_center) - move_in_secure_seal  # circle radius

    cv2.circle(mask, g_fct.switch_coordinates((row_center, col_center)), radius, 255, thickness=cv2.FILLED)  # values 0 and 255 for False and True

    return mask

#################################
