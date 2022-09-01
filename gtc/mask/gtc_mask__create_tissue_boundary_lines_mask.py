#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import gtc.mask as g_msk


def create_tissue_boundary_lines_mask(
    orig_img_props: dict,
    masks: dict,
    mask_type: str,
    c: dict,
    p: dict,
    scale_fac: float = 3000
) -> np.ndarray:

    """Create mask with the boundary lines of the tissues."""

    dot_radius = p['plot_props']['dot_radius']

    ####

    img_tmp = g_msk.new_black_color_image(orig_img_props['dims'])

    mask_names = [mask_type + ' ' + mask_name for mask_name in c['tissue_mask_names']]

    for mask_name in mask_names:
        mask_tmp = cv2.Laplacian(masks[mask_name], cv2.CV_64F)  # detect border line of tissue

        _, mask_tmp = cv2.threshold(mask_tmp, 0, 255, cv2.THRESH_BINARY)  # set limit of minima to 0 and limit of maxima to 255
        mask_tmp = mask_tmp.astype('uint8')

        def calc_radius(size):  # calculate appropriate thickness for boundary lines
            radius = dot_radius * max(1, int(float(size) / scale_fac))  # the higher the scale_fac value the thinner the lines
            return radius

        radii = (calc_radius(orig_img_props['rows']), calc_radius(orig_img_props['cols']))  # prevent to thin lines in matplotlib plots

        mask_tmp = cv2.dilate(mask_tmp, g_msk.disk_kernel(radii), iterations=1)  # thicken boundary line

        mask_tmp = cv2.cvtColor(mask_tmp, cv2.COLOR_GRAY2RGB)  # convert gray to color

        img_tmp = cv2.bitwise_or(img_tmp, mask_tmp)  # add tissue boundary line to mask

    return img_tmp

#################################
