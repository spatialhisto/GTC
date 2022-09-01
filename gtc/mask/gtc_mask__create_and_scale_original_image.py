#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os
import cv2
import numpy as np
import gtc.mask as g_msk
import gtc.setup as g_set


def create_and_scale_original_image(
    image_name: str,
    p: dict
) -> np.ndarray:

    """Create image of the original microscope image."""

    fname_orig = p['files'][image_name]
    img_scale_factor = p['img_scale_factor']

    ####

    fname_scaled = g_set.assemble_fname_scaled_tissue_image(fname_orig, img_scale_factor, p)  # assemble file names of scaled image files

    if os.path.exists(fname_scaled):
        img_scaled = cv2.imread(fname_scaled)  # load the already scaled image from the input folder
    else:
        img_orig = cv2.imread(fname_orig)

        img_scaled = g_set.scale_original_tissue_image_file(img_orig, img_scale_factor)  # shrink and save debug tissue images if they do not exist in the input folder

        cv2.imwrite(fname_scaled, img_scaled)  # save scaled image in the input folder with img_scale_factor as extension, e.g. '_4' for img_scale_factor = 4."""

    img_tmp = g_msk.histogram_equalization_image(img_scaled)  # contrast limited histogram equalization

    return img_tmp

#################################
