#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import math as m
import numpy as np


def create_virtual_he_image_method1(
    orig_img_props: dict,
    masks: dict
) -> np.ndarray:

    """Create H&E from DAPI and FITC image using formulas from the following paper:
    Creating virtual hematoxylin and eosin images using samples imaged on
      a commercial CODEX platform, P.D. Simonson, 2021

    R_i,j / 255 = c_R + (1 − c_R) * exp(− k_D * a_R * D_i,j – k_E * b_R * F_i,j)
    G_i,j / 255 = c_G + (1 – c_G) * exp(− k_D * a_G * D_i,j – k_E * b_G * F_i,j)
    B_i,j / 255 = c_B + (1 – c_B) * exp(− k_D * a_B * D_i,j – k_E * b_B * F_i,j)

    R_i,j, G_i,j, B_i,j ... red, green, and blue channels of H&E image
    D_i,j, F_i,j ... pixel indices of DAPI and FITC image
    a = [a_R, a_G, a_B] and b = [b_R, b_G, b_B] ... for DAPI (a) and
      FITC (b) expected decrease in bright field light intensity for
      increasing brightness seen by fluorescence microscopy
    c = [c_R, c_G, c_B] ... a postulated expected minimum amount of light
    k_D, k_E ... scalars that are added for convenience for adjusting
      impact on image output based on DAPI and eosin input images

    https://github.com/SimonsonLab/VirtualHE_examples/blob/main/VirtualHE.ipynb"""

    a = [0.2, 0.6, 1.0]  # dapi
    b = [0.3, 0.7, 0.1]  # eosin
    c = [0.15, 0.15, 0.15]  # minimun light
    k = [0.014, 0.006]

    img_dapi = masks['orig dapi image'][:, :, 0]
    img_fitc = masks['orig fitc image'][:, :, 0]

    ####

    img_tmp = np.empty([orig_img_props['rows'], orig_img_props['cols'], 3])  # empty black image with float

    for ii in range(3):  # [R_i,j, G_i,j, B_i,j], [red, green, blue]
        img_tmp[:, :, ii] = np.round(255 * (c[ii] + (1 - c[ii]) * np.exp(
                            - k[0] * a[ii] * img_dapi - k[1] * b[ii] * img_fitc)))

    img_tmp = img_tmp.astype(np.uint8)  # cast float to integer and convert to bgr

    # print('min: %d, max: %d' % (img_tmp.min(), img_tmp.max()))

    return img_tmp


####


def create_virtual_he_image_method2(
    orig_img_props: dict,
    masks: dict
) -> np.ndarray:

    """Create H&E from DAPI and FITC image using formulas from the following paper:
    Virtual Hematoxylin and Eosin Transillumination Microscopy Using
      Epi-Fluorescence Imaging, M.G. Giacomelli, 2016

    R_i,j / 255 = exp(− k * (a_R * D_i,j / 255 + b_R * E_i,j / 255))
    G_i,j / 255 = exp(− k * (a_G * D_i,j / 255 + b_G * E_i,j / 255))
    B_i,j / 255 = exp(− k * (a_B * D_i,j / 255 + b_B * E_i,j / 255))

    R_i,j, G_i,j, B_i,j ... red, green, and blue channels of H&E image
    D_i,j, F_i,j ... pixel indices of DAPI and FITC image
    k ... constant
    a = [a_R, a_G, a_B] and b = [b_R, b_G, b_B] ... for DAPI (a) and
      FITC (b) expected decrease in bright field light intensity for
      increasing brightness seen by fluorescence microscopy"""

    hemat = np.array([0.300, 1.000, 0.860])  # Hematoxylin (DAPI) from paper Giacomelli
    eosin = np.array([0.544, 1.000, 0.050])  # Eosin (FITC)
    min_rgb_value = 15  # the lower the value the higher the contrast

    ####

    img_tmp = np.empty([orig_img_props['rows'], orig_img_props['cols'], 3])  # empty black image with float

    def norm_image(img):
        img_scale = img - img[0, 0]
        img_scale[img < img[0, 0]] = 0  # set backround to zero so it occurs white
        img_scale = img_scale / 255  # values between 0 and 1
        return img_scale

    img1 = norm_image(masks['orig dapi image'][:, :, 0])
    img2 = norm_image(masks['orig fitc image'][:, :, 0])

    b_comb_max = max([(hemat[ii] * img1 + eosin[ii] * img2).max() for ii in range(3)])
    k = - m.log(min_rgb_value / 255) / b_comb_max  # log is here ln

    for ii in range(3):  # [blue, green, red]
        img_tmp[:, :, ii] = 255 * np.exp(- k * (hemat[ii] * img1 + eosin[ii] * img2))

    img_tmp = img_tmp.astype(np.uint8)  # cast float to integer

    return img_tmp

#################################
