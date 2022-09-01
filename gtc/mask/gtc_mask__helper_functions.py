#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import pandas as pd
import gtc.mask as g_msk
import gtc.function as g_fct
import skimage.morphology as ski_mrph
from math import floor, log, sqrt
from typing import Union


def disk_kernel(
    radius: Union[int, tuple]
) -> np.ndarray:

    """Create disk-shaped kernel for binary image manipulation."""

    if type(radius) == int:
        s = 2 * radius + 1
        size = (s, s)
    else:
        s0 = 2 * radius[0] + 1
        s1 = 2 * radius[1] + 1
        size = (s0, s1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)

    return kernel


####


def gaussian_kernel(
    radius: int,
    ratio: float = 0.05
) -> np.ndarray:

    """Create a normal distributed kernel, whereat the
    function value decreases from the center to the boundary
    for ratio, with the normal distribution in 2d:
    N(r, s) = 1/(2pi*s^2) * exp(-1/2*(r/s)^2)"""

    s = 2 * radius + 1  # kernel size must be odd-numbered
    size = (s, s)

    sigma = radius / sqrt(-2 * log(ratio))  # sigma so that normal distribution decreases from center to boundary for ratio, NOTE: log is natural logarithm

    gauss_kernel = np.zeros(size)
    gauss_kernel[radius, radius] = 1
    gauss_kernel = cv2.GaussianBlur(gauss_kernel, size, sigma, borderType=cv2.BORDER_ISOLATED)

    return gauss_kernel


####


def new_black_binary_image(
    img_dims: list
) -> np.ndarray:

    """Create an empty black binary image."""

    img_tmp = np.zeros(img_dims, dtype=np.uint8)

    return img_tmp


####


def new_black_color_image(
    img_dims: list
) -> np.ndarray:

    """Create an empty black RGB image."""

    img_tmp = np.zeros((img_dims[0], img_dims[1], 3), dtype=np.uint8)

    return img_tmp


####


def new_white_color_image(
    img_dims: list
) -> np.ndarray:

    """Create an empty black RGB image with an alpha channel."""

    img_tmp = np.zeros((img_dims[0], img_dims[1], 3), dtype=np.uint8)
    img_tmp[:] = [255, 255, 255]

    return img_tmp


####


def new_black_color_image_with_alpha_channel(
    img_dims: list,
    alpha: int = 255
) -> np.ndarray:

    """Create an empty black RGB image with an alpha channel."""

    img_tmp = np.zeros((img_dims[0], img_dims[1], 4), dtype=np.uint8)
    img_tmp[:] = [0, 0, 0, alpha]

    return img_tmp


####


def new_white_color_image_with_alpha_channel(
    img_dims: list,
    alpha: int = 255
) -> np.ndarray:

    """Create an empty black RGB image with an alpha channel."""

    img_tmp = np.zeros((img_dims[0], img_dims[1], 4), dtype=np.uint8)
    img_tmp[:] = [255, 255, 255, alpha]

    return img_tmp


####


def new_tissue_background_image_rgb(
    masks: dict
) -> np.ndarray:

    """Create an tissue background image with rgba color scheme."""

    img_tmp = cv2.cvtColor(masks['orig_img_tissue_alpha'].copy(), cv2.COLOR_BGR2RGB)

    return img_tmp


####


def invert_binary_mask(
    img_tmp: np.ndarray,
) -> np.ndarray:

    """Invert the binary mask."""

    if img_tmp.dtype == np.uint8:
        img_tmp = 255 - img_tmp
    else:
        raise ValueError('Cannot convert image with dtype != uint8')

    return img_tmp


####


def resize_img(
    img_tmp: np.ndarray,
    dims: tuple
) -> np.ndarray:

    """Resize image to new dimensions by using the best method for
    scale-up and scale-down interpolation."""

    height_old = img_tmp.shape[0]
    width_old = img_tmp.shape[1]
    height_new = dims[0]
    width_new = dims[1]

    if (height_old < height_new) & (width_old < width_new):  # scale-up
        method = cv2.INTER_LINEAR
    elif (height_old > height_new) & (width_old > width_new):  # scale-down
        method = cv2.INTER_AREA
    else:  # something else
        method = cv2.INTER_NEAREST

    img_tmp = cv2.resize(img_tmp, g_fct.switch_coordinates(dims), interpolation=method)

    return img_tmp


####


def overlap_img_with_mask(
    img: np.ndarray,
    mask: np.ndarray,
    alpha_mask: float
) -> np.ndarray:

    """Overlap microscope image with colored mask."""

    img_tmp = cv2.addWeighted(img, 1.0, mask, alpha_mask, 0.0)

    return img_tmp


###


def erode_mask_by_size(
    mask: np.ndarray,
    size_to_erode: int,
    max_disk_radius: int
) -> np.ndarray:

    """Erode a binary image by a given size via a disk kernel."""

    num_iterations = size_to_erode // max_disk_radius
    disk_radius_res = size_to_erode % max_disk_radius  # remaining rest of boundary size

    mask_tmp = cv2.erode(mask, disk_kernel(max_disk_radius), iterations=num_iterations)  # move disk around mask boundary and remove mask parts within the disk

    if disk_radius_res > 0: img_tmp = cv2.erode(mask_tmp, disk_kernel(disk_radius_res), iterations=1)

    return mask_tmp


####


def blurring_mask(
    mask_tmp: np.ndarray,
    radius: int = None
) -> np.ndarray:

    """Perform morphological median blur manipulation on a mask
    (smear out dots for better overlapping)."""

    mask_tmp = cv2.medianBlur(mask_tmp, radius)

    return mask_tmp


####


def closing_mask(
    mask_tmp: np.ndarray,
    radius: int = None
) -> np.ndarray:

    """Perform morphological closing manipulation on a mask
    (dilation followed by erosion to remove small holes)."""

    mask_tmp = cv2.morphologyEx(mask_tmp, cv2.MORPH_CLOSE, disk_kernel(radius))

    return mask_tmp


####


def opening_mask(
    mask_tmp: np.ndarray,
    radius: int = None
) -> np.ndarray:

    """Perform morphological opening manipulation on a mask
    (erosion followed by dilation to remove small dots)."""

    mask_tmp = cv2.morphologyEx(mask_tmp, cv2.MORPH_OPEN, disk_kernel(radius))

    return mask_tmp


####


def morph_operations_and_secure_seal_area(
    mask_tmp: np.ndarray,
    mask_secure_seal_area: np.ndarray,
    p: dict,
    method: str = None,
    factor: float = 1.3
) -> np.ndarray:

    """Perform morphological manipulation operations
    (blurring, closing and opening) on a mask and restrict
    its area to the valid area of the secure seal."""

    dot_radius_union = p['tissue_masks']['dot_radius']['union']
    dot_radius_threshold = p['tissue_masks']['dot_radius']['threshold']

    morph_closing = p['tissue_masks']['morph_operations']['closing']
    morph_opening = p['tissue_masks']['morph_operations']['opening']
    morph_blurring = p['tissue_masks']['morph_operations']['blurring']

    ####

    radius = dot_radius_union if method == 'union' else dot_radius_threshold
    radius = floor(radius * factor)
    radius = radius + 1 if (radius % 2 == 0) else radius  # size must be even

    if morph_blurring:  # blur dots
        mask_tmp = blurring_mask(mask_tmp, radius)
    if morph_closing:  # remove small holes
        mask_tmp = closing_mask(mask_tmp, radius)
    if morph_opening:  # remove small dots
        mask_tmp = opening_mask(mask_tmp, radius)

    mask_tmp = cv2.bitwise_and(mask_tmp, mask_secure_seal_area)  # restrict valid area for gene/cell counting to secure seal area

    return mask_tmp


####


def merge_masks_by_union(
    orig_img_props: dict,
    df: pd.DataFrame,
    p: dict
) -> np.ndarray:

    """Create mask by merging the discs created
    by the disks of the gene/cell positions."""

    dot_radius = p['tissue_masks']['dot_radius']['union']

    ####

    mask_tmp = g_msk.new_black_binary_image(orig_img_props['dims'])  # empty black binary image

    for row_gene, col_gene in zip(df['row'], df['col']):
        cv2.circle(mask_tmp, g_fct.switch_coordinates((row_gene, col_gene)), dot_radius, 255, thickness=cv2.FILLED)  # values 0 and 255 for False and True

    return mask_tmp


####


def threshold(
    mask: np.ndarray,
    thresh_value_rel: float
) -> np.ndarray:

    """Perform thresholding technique on mask."""

    count_max = mask.max()
    thresh_value_abs = count_max * thresh_value_rel  # cut-off value for threshold as integer

    mask[mask <= thresh_value_abs] = 0
    mask[mask > thresh_value_abs] = 255
    mask = mask.astype('uint8')

    print('The threshold_value: thresh_value_rel = %1.2f, mask.max() = %4.5f, thresh_value_abs = %4.5f'
          % (thresh_value_rel, count_max, thresh_value_abs))

    return mask


####


def merge_masks_by_threshold(
    orig_img_props: dict,
    df: pd.DataFrame,
    dot_radius: int,
    thresh_value: float,
    p: dict
) -> np.ndarray:

    """Create mask by representing each cell/gene as disc
    of a certain size with the origin at the cell/gene
    position. The individual discs overlap and sum up, so
    that the thresholding technique is used afterwards to
    generate binary masks."""

    kernel_shape = p['tissue_masks']['kernel_shape']

    ####

    # mask_tmp = g_msk.new_black_binary_image(orig_img_props['dims'])  # empty black binary image
    mask_tmp = np.zeros(orig_img_props['dims'], dtype=np.float16)  # empty black binary image

    if kernel_shape == 'uniform':
        kernel = ski_mrph.disk(dot_radius)  # disk shape with uniform distribution and 2r+1 length
    elif kernel_shape == 'gaussian':
        kernel = gaussian_kernel(dot_radius)
    else:
        raise ValueError("The following kernel does not exist: %s "
                         "- Check the 'Gtc-Parameters'!" % kernel_shape)

    for row_gene, col_gene in zip(df['row'], df['col']):
        def calc_min_max(x):
            x_min = x - dot_radius
            x_max = x + dot_radius + 1
            return x_min, x_max

        row_min, row_max = calc_min_max(row_gene)
        col_min, col_max = calc_min_max(col_gene)

        if row_min > 0 and col_min > 0 and row_max < mask_tmp.shape[0] and col_max < mask_tmp.shape[1]:  # only add kernel if within mask boundaries
            mask_tmp[row_min:row_max, col_min:col_max] += kernel

    mask_tmp = threshold(mask_tmp, thresh_value)  # thresholding to generate binary mask

    return mask_tmp


####


def histogram_equalization_image(
    img_tmp: np.ndarray,
    clip_limit: float = 12.0,
    grid_size: int = 8
) -> np.ndarray:

    """Contrast Limited Adaptive Histogram Equalization (CLAHE) of image."""

    img_tmp_gray = cv2.cvtColor(img_tmp, cv2.COLOR_BGR2GRAY)  # bgr to gray

    clahe_grid = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))  # histo equalization
    img_tmp_gray = clahe_grid.apply(img_tmp_gray)

    img_tmp = cv2.cvtColor(img_tmp_gray, cv2.COLOR_GRAY2BGR)

    return img_tmp

#################################
