#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import gtc.mask as g_msk
from matplotlib.ticker import ScalarFormatter


def sci_notation_format() -> ScalarFormatter:

    """Drop the row 'cells' from the dataframe for the barplots."""

    class ScalarFormatterClass(ScalarFormatter):  # format ticks in scientific notation
        def _set_format(self):
            self.format = "%1.2f"

    y_scalar_formatter = ScalarFormatterClass(useMathText=True)
    y_scalar_formatter.set_powerlimits((0, 0))

    return y_scalar_formatter


####


def rgb_color_dict(
    k: int = 204
) -> dict:

    """Perform morphological opening manipulation on a mask
    (erosion followed by dilation to remove small dots)."""

    black = [0, 0, 0]
    blue = [0, 0, k]
    green = [0, k, 0]
    green_light = [150, k, 150]
    red = [k, 0, 0]
    red_light = [255, 50, 50]
    red_dark = [120, 0, 0],
    pink = [240, 0, 220],
    yellow = [k, k, 0]
    yellow_light = [255, 255, 0]

    rgb_colors = {
        "blend": yellow_light,
        "empty": blue,
        "outside": black,
        "tissue 'neoplastic'": red,
        "tissue 'neoplastic' boundary": red,
        "tissue 'neoplastic' center": red_light,
        "tissue 'non-neoplastic'": green,
        "tissue 'non-neoplastic' boundary": green,
        "tissue 'non-neoplastic' center": green_light,
        "tissue 'connective in tumor'": yellow,
        "tissue 'connective in tumor' boundary": yellow,
        "tissue 'connective in tumor' center": yellow_light,
        "mask_overlap": red_dark,
        "only_mask_A": red_light,
        "only_mask_B": pink}

    return rgb_colors


####


def save_resized_image(
    orig_img_props: dict,
    mask: np.ndarray,
    file_name: str,
    p: dict
):

    """Save a small version of image or mask as png-file."""

    img_tmp = g_msk.resize_img(mask, orig_img_props['dims_out'])  # resize for output

    cv2.imwrite(p['output'] + file_name + '.png', img_tmp)

#################################
