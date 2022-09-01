#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.mask as g_msk
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from math import ceil


def plot_custom_gene_sets_hist2d_and_contourf_with_boundary_lines(
    masks: dict,
    df_genes: pd.DataFrame,
    c: dict,
    p: dict,
    alpha_img: float = 0.6,
    alpha_plot: float = 1.0,
    pad_title_colorbar: int = 12,
    shrink_fac_colorbar: float = 0.6
):

    """Plot the number of genes of the defined gene sets as 2d-histogram
    with the tissue boundary lines."""

    gene_sets = p['custom_gene_sets']
    num_bins = p['plot_props']['num_hist2d_bins']
    img_res_in_dpi = p['img_res_in_dpi']

    ####

    mask_boundary_lines = g_msk.invert_binary_mask(masks['gene boundary lines tissues'])  # mask with inverted tissue border lines

    def setup_plot():
        fig, ax = plt.subplots()  # new plot
        ax.imshow(mask_boundary_lines, alpha=alpha_img, interpolation='gaussian')  # new background image to plot on

        return fig, ax

    def format_and_save(plot_type, y_axis_flipped):
        if y_axis_flipped: ax.invert_yaxis()  # otherwise the boundary lines are flipped
        ax.axis('off')
        fig.patch.set_visible(False)
        cmap = plt.colorbar(shrink=shrink_fac_colorbar)
        cmap.ax.set_title('Counts [-]', pad=pad_title_colorbar)

        plt.savefig(p['output'] + 'Plot_' + plot_type + '_of_gene_set_' + gene_set_name + '.png', dpi=img_res_in_dpi)
        plt.close('all')

    def adapt_colormap(counts):  # adapt range of white to avoid big yellow areas
        max_val = int(np.max(counts))
        num_white = ceil(max_val / 7)

        orig_cmap = plt.cm.get_cmap('hot_r', max_val)
        colors = orig_cmap(np.linspace(0, 1, max_val))
        colors[:num_white, :] = np.array([1, 1, 1, 1])  # white
        new_cmap = ListedColormap(colors)

        return new_cmap

    ####

    for gene_set_name in c['custom_gene_set_names']:
        df_gene = df_genes[df_genes['gene_iss'].isin(gene_sets[gene_set_name])]  # select gene of one type

        ####

        print("-Plot 2d-histogram of gene set '%s'" % gene_set_name)

        fig, ax = setup_plot()
        counts, ybins, xbins, _ = plt.hist2d(df_gene['col'], df_gene['row'], bins=num_bins,  # !!!NOTE: switched x- and y-coordinates
                                             cmap=plt.cm.get_cmap('hot_r'), alpha=alpha_plot, zorder=-1)  # put hist2d in background and boundary lines in front
        format_and_save('hist2d', True)

        ####

        print("-Plot contourf plot of gene set '%s'" % gene_set_name)

        fig, ax = setup_plot()
        plt.contourf(counts.T, extent=[xbins.min(), xbins.max(), ybins.min(), ybins.max()],
                     cmap=adapt_colormap(counts), alpha=alpha_plot, zorder=-1)  # put contourf in background and boundary lines in front
        format_and_save('contourf', False)

#################################
