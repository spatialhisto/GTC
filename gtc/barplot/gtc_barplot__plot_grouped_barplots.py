#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.barplot as g_bar
import gtc.function as g_fct
import matplotlib.pyplot as plt


def plot_grouped_barplots(
    masks_to_plot: list,
    df: pd.DataFrame,
    mask_type: str,
    unit: str,
    txt_tit: str,
    p: dict,
    txt_size: int = 14,
    dist_bars_diff_genes: float = 0.4
):

    """Plot a grouped bar plot either of all genes or of a custom
    defined subset of the genes."""

    img_res_in_dpi = p['img_res_in_dpi']

    ####

    col_names = g_fct.df_col_names(masks_to_plot, unit)
    df_unit = df[['genes'] + col_names]  # subset dataframe
    df_unit = g_bar.sort_dataframe('grouped', df_unit, col_names, p)  # subset sorted

    num_bars_per_gene = len(col_names)
    bar_width = (1 - dist_bars_diff_genes) / num_bars_per_gene

    fig, axs, num_genes, num_genes_per_subplot, num_subplots = g_bar.calc_fig_dims(df, p)

    if num_subplots == 1:
        fig.subplots_adjust(left=0.15, right=0.65, top=0.80, bottom=0.20)
    else:
        fig.subplots_adjust(left=0.15, right=0.90, top=0.94, bottom=0.03, hspace=0.50, wspace=0)

    for num_ax in range(num_subplots):  # loop over all subplots
        index_genes_subplot = range(num_ax * num_genes_per_subplot,
                                    min((num_ax + 1) * num_genes_per_subplot, num_genes))
        df_unit_sub = df_unit.iloc[index_genes_subplot]

        pos_group = np.arange(len(df_unit_sub))  # the x-positions of the bar groups

        for jj, col_name in enumerate(col_names):  # loop over all masks
            pos_bar = pos_group - ((num_bars_per_gene - 1) - 2 * jj) * bar_width / 2  # x-position of a single bar
            axs[num_ax, 0].bar(pos_bar, df_unit_sub[col_name], bar_width, label=masks_to_plot[jj])  # add bar to plot

        axs[num_ax, 0] = g_bar.format_axes(axs[num_ax, 0], df_unit_sub, unit, pos_group, 'Counts', txt_size)  # format axes

    g_bar.format_title_and_legend(axs, num_subplots, txt_tit)  # plot title and legend

    plt.savefig(p['output'] + 'Barplot_grouped_' + txt_tit + '_Counts ' + mask_type + ' masks ' + unit + '.png',
                dpi=img_res_in_dpi)

#################################
