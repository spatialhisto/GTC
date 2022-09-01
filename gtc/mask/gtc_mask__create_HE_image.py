#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np


def create_virtual_he_image(
    orig_img_props: dict,
    masks: dict
) -> np.ndarray:

    """Create H&E from DAPI image using formulas from the following paper:
    Creating virtual hematoxylin and eosin images using samples imaged on
      a commercial CODEX platform, P.D. Simonson, 2021
    R_i,j = c_R + (1 − c_R) * exp(− k_D * a_R * D_i,j – k_E * b_R * E_i,j)
    G_i,j = c_G + (1 – c_G) * exp(− k_D * a_G * D_i,j – k_E * b_G * E_i,j)
    B_i,j = c_B + (1 – c_B) * exp(− k_D * a_B * D_i,j – k_E * b_B * E_i,j)

    R_i,j, G_i,j, B_i,j ... red, green, and blue channels of H&E image
    D_i,j, E_i,j ... pixel indices of DAPI and eosin image
    a = [a_R, a_G, a_B] and b = [b_R, b_G, b_B] ... for DAPI (a) and
      eosin (b) expected decrease in bright field light intensity for
      increasing brightness seen by fluorescence microscopy
    c = [c_R, c_G, c_B] ... a postulated expected minimum amount of light
    k_D, k_E ... scalars that are added for convenience for adjusting
      impact on image output based on DAPI and eosin input images

    https://github.com/SimonsonLab/VirtualHE_examples/blob/main/VirtualHE.ipynb"""

    a = [0.2, 0.6, 1.0]  # dapi
    b = [0.3, 0.7, 0.1]  # eosin
    c = [0.15, 0.15, 0.15]  # minimun light
    k = [0.014, 0.006]

    img_dapi = masks['orig dapi image']
    img_eosin = masks['orig fitc image']

    ####

    img_tmp = np.empty([orig_img_props['rows'], orig_img_props['cols'], 3])  # empty black image with float

    for ii in range(3):  # [R_i,j, G_i,j, B_i,j], [red, green, blue]
        img_tmp[:, :, ii] = np.round(255 * (c[ii] + (1 - c[ii]) * np.exp(
                            - k[0] * a[ii] * img_dapi[:, :, ii] - k[1] * b[ii] * img_eosin[:, :, ii])))

    img_tmp = img_tmp.astype(np.uint8)  # cast float to integer and convert to bgr

    # print('min: %d, max: %d' % (img_tmp.min(), img_tmp.max()))

    return img_tmp

#################################
