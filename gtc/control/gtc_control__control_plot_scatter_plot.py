#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import cv2
import numpy as np
import pandas as pd
import gtc.plot as g_plt
import matplotlib.pyplot as plt


def control_plot_scatter_plot(
    masks: dict,
    df_cells: pd.DataFrame,
    c: dict,
    p: dict
):

    """Plot scatter plot of the cell positions colored by the tissue colors."""

    rgb_colors = g_plt.rgb_color_dict()

    fname = p['output'] + 'Control_scatter_plot_cells_in_tissues.png'

    for mask_name in c['tissue_mask_names']:
        within = [masks[mask_name][x, y] == 255 for x, y in zip(df_cells['row'], df_cells['col'])]  # count

        comb = np.column_stack((within, df_cells['row'], df_cells['col']))  # combine info
        coords = comb[comb[:, 0] > 0, 1:]

        color_rgb = np.array(rgb_colors[mask_name]) / 255
        plt.scatter(coords[:, 0], coords[:, 1], s=0.001, color=color_rgb)

    plt.xlabel('Number rows / pixles')
    plt.ylabel('Number columns / pixles')
    plt.savefig(fname, dpi=300)

    img_plt = cv2.imread(fname)  # rotate image 90 degree clockwise
    img_plt = cv2.rotate(img_plt, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(fname, img_plt)

#################################
