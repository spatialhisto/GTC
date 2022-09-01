#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import os
import numpy as np
import pandas as pd
import pathlib as pth
import gtc.mask as g_msk
from math import floor, ceil


def extract_fpath_fname_fext(
    full_path: str
) -> (str, str, str):

    """Extract the file path, the file name and
    the file extension from full path string."""

    fpath, fname_ext = os.path.split(full_path)
    fname, fext = os.path.splitext(fname_ext)

    return fpath, fname, fext


####


def assemble_input_dirname(
    fname_gtc_param: str
) -> str:

    """Assemble the output directory name."""

    fpath, _, _ = extract_fpath_fname_fext(fname_gtc_param)

    fpath_input = fpath + '/Data/'

    return fpath_input


####


def assemble_output_dirname(
    fname_gtc_param: str
) -> str:

    """Assemble the output directory name."""

    fpath, fname, _ = extract_fpath_fname_fext(fname_gtc_param)

    fpath_output = fpath + '/Results/' + fname + '/'

    return fpath_output


####


def create_output_dir(
    fname_gtc_param: str
):

    """Create the output directory if it does not exist."""

    path_out = assemble_output_dirname(fname_gtc_param)

    pth.Path(path_out).mkdir(parents=True, exist_ok=True)  # create output folder


####


def scale_gtc_parameters_by_factor(
    p: dict
) -> dict:

    """Divide the parameters of the gtc file
    by img_scale_factor."""

    img_scale_factor = p['img_scale_factor']

    ####

    p['img_res_in_um_per_px'] = p['img_res_in_um_per_px'] * img_scale_factor
    p['move_in_secure_seal'] = floor(p['move_in_secure_seal'] / img_scale_factor)
    p['tissue_masks']['dot_radius']['union'] = floor(p['tissue_masks']['dot_radius']['union'] / img_scale_factor)
    p['tissue_masks']['dot_radius']['threshold'] = floor(p['tissue_masks']['dot_radius']['threshold'] / img_scale_factor)
    p['tissue_region_masks']['boundary_size'] = floor(p['tissue_region_masks']['boundary_size'] / img_scale_factor)
    p['plot_props']['dot_radius'] = floor(p['plot_props']['dot_radius'] / img_scale_factor)

    return p


####


def assemble_fname_scaled_tissue_image(
    full_path: str,
    img_scale_factor: int,
    p: dict
) -> str:

    """Assemble the file name of the scaled tissue image
    with img_scale_factor as extension, e.g. '_4' for
    img_scale_factor = 4."""

    _, fname, _ = extract_fpath_fname_fext(full_path)

    fpath_img_scaled = p['input'] + '/' + fname + ('_shrink_factor_%d.tif' % img_scale_factor)

    return fpath_img_scaled


####


def divide_df_coords_by_rescale_factor(
    df: pd.DataFrame,
    img_scale_factor: int
) -> pd.DataFrame:

    """Divide the coordinates of the cells/genes
    by img_scale_factor."""

    df['row'] = df['row'].apply(lambda x: int(float(x) / img_scale_factor))  # floor coordinates
    df['col'] = df['col'].apply(lambda x: int(float(x) / img_scale_factor))

    return df


###


def scale_original_tissue_image_file(
    img_orig: np.ndarray,
    img_scale_factor: int
):

    """Scale the original tissue image file"""

    height_orig, width_orig = img_orig.shape[0:2]

    height_debug = ceil(height_orig / img_scale_factor)  # calc dimensions for debug file
    width_debug = ceil(width_orig / img_scale_factor)
    dims_debug = (height_debug, width_debug)

    img_scaled = g_msk.resize_img(img_orig, dims_debug)  # resize orig img

    return img_scaled

#################################
