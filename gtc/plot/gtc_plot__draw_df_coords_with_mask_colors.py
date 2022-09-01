#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import pandas as pd
import gtc.mask as g_msk
import gtc.plot as g_plt
import gtc.function as g_fct


def draw_df_coords_with_mask_colors(
    orig_img_props: dict,
    masks: dict,
    mask_type: str,
    df: pd.DataFrame,
    file_name: str,
    c: dict,
    p: dict
):

    """Plot a picture of cells/genes true to their
    positions and with the mask colors they lie in."""

    dot_radius = p['plot_props']['dot_radius']

    ####

    rgb_colors = g_plt.rgb_color_dict()

    img_tmp = g_msk.new_white_color_image(orig_img_props['dims'])  # empty white image

    for mask_name in c['tissue_mask_names']:
        color_bgr = g_fct.rgb2bgr(rgb_colors[mask_name])

        for row, col in zip(df['row'], df['col']):
            if masks[mask_type + ' ' + mask_name][row, col] == 255:  # if cell within mask, values 0 and 255 for False and True
                cv2.circle(img_tmp, g_fct.switch_coordinates((row, col)), dot_radius, color_bgr, thickness=cv2.FILLED)  # create disc elements around cell/gene

    g_plt.save_resized_image(orig_img_props, img_tmp, 'Plot_colored_' + file_name, p)  # plot small image

#################################
