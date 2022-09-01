#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
from math import floor
from typing import Union


def rgb2bgr(
    rgb_color: Union[list, np.array],
) -> Union[list, np.array]:

    """Convert rgb- to bgr-color scheme (standard of opencv)."""

    if type(rgb_color) == list:
        bgr_color = list(reversed(rgb_color))
    else:  # numpy array
        bgr_color = np.flip(rgb_color)

    return bgr_color


####


def rgb2rgba(
    rgb_color: Union[list, np.array],
    alpha: int = 255
) -> Union[list, np.array]:

    """Convert rgb- to rgba-color scheme (with alpha channel)."""

    if type(rgb_color) == list:
        rgba_color = rgb_color + [alpha]
    else:  # numpy array
        rgba_color = np.append(rgb_color, alpha)

    return rgba_color


####


def rgb2bgra(
    rgb_color: Union[list, np.array],
    alpha=255
) -> Union[list, np.array]:

    """Convert rgb- to bgra-color scheme (standard of opencv with alpha channel)."""

    if type(rgb_color) == list:
        bgra_color = list(reversed(rgb_color)) + [alpha]
    else:  # numpy array
        bgra_color = np.append(np.flip(rgb_color), alpha)

    return bgra_color


####


def rgba2bgra(
    rgba_color: Union[list, np.array],
) -> Union[list, np.array]:

    """Convert rgba- to bgra-color scheme (standard of opencv with alpha channel)."""

    rgb_color = rgba_color[0:3]
    alpha = rgba_color[3]

    if type(rgb_color) == list:
        bgra_color = list(reversed(rgb_color)) + [alpha]
    else:  # numpy array
        bgra_color = np.append(np.flip(rgb_color), alpha)

    return bgra_color


####


def alpha_blending(
    color: Union[list, np.array],
    alpha: Union[int, float],
    background: str = 'white'
) -> Union[list, np.array]:

    """The png-image format has no alpha channel. Hence, the alpha channel
    is integrated into the RGB- or BGR-color values via convex combination
    (alpha blending): c = (1 - alpha) * a + alpha * b.
    Alpha values: 0...full transparent, 1 (255)...full visible."""

    alpha = alpha if type(alpha) == float else float(alpha / 255)  # 0.0 or 0...transparent, 1.0 or 255...opaque
    a = 255 if background == 'white' else 0  # 255...white, 0...black

    def conv_comb(b):
        c = (1 - alpha) * a + alpha * b
        return c

    if type(color) == list:
        new_color = [conv_comb(color[0]), conv_comb(color[1]), conv_comb(color[2])]
    else:  # numpy array
        new_color = np.array([conv_comb(color[0]), conv_comb(color[1]), conv_comb(color[2])])

    return new_color


####


def mod_rgb_color_by_value(
    rgb_color: Union[list, np.array],
    value_offset: int
) -> Union[list, np.array]:

    """Change each rgb-color by a value and limit minima and maxima values to 0 and 255."""

    new_rgb_color = [int(max(0, min(x + value_offset, 255))) for x in rgb_color]

    return new_rgb_color


####


def calc_values_to_change_rgb_colors_about(
    gene_set: list,
    delta: int = 20
) -> list:

    """Calculate an integer value for each gene type of a given gene type set to modify
    a single rgb color in order to highlight their difference."""

    num_genes = len(gene_set)
    width = num_genes // 2
    offset = 0.0 if num_genes % 2 == 1 else 0.5

    rgb_values = [floor((float(ii) - width + offset) * delta) for ii in range(num_genes)]

    return rgb_values

#################################
