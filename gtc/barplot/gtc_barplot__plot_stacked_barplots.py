#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.plot as g_plt
import gtc.barplot as g_bar
import gtc.function as g_fct
import matplotlib.pyplot as plt


def plot_stacked_barplots(
    masks_to_plot: list,
    df: pd.DataFrame,
    mask_type: str,
    unit: str,
    txt_tit: str,
    p: dict,
    txt_size: int = 14,
    bar_width: float = 0.2
):

    """Plot a stacked bar plot either of all genes or of a custom
    defined subset of the genes."""

    img_res_in_dpi = p['img_res_in_dpi']

    ####

    col_names = g_fct.df_col_names(masks_to_plot, unit)
    df_unit = df[['genes'] + col_names]  # subset dataframe
    df_unit = g_bar.sort_dataframe('stacked', df_unit, col_names, p)  # subset sorted

    df_col = df_unit[col_names].sum(axis=1)  # sum over each row
    df_unit[col_names] = df_unit[col_names].div(df_col, axis=0)  # normalize with sum for stacked bar plot
    # df_col = df_col.div(df_col.max())  # normalize line in stacked bar plot

    fig, axs, num_genes, num_genes_per_subplot, num_subplots = g_bar.calc_fig_dims(df, p)

    if num_subplots == 1:
        fig.subplots_adjust(left=0.15, right=0.65, top=0.80, bottom=0.20)
    else:
        fig.subplots_adjust(left=0.15, right=0.85, top=0.94, bottom=0.03, hspace=0.50, wspace=0)

    for num_ax in range(num_subplots):
        index_genes_subplot = range(num_ax * num_genes_per_subplot,
                                    min((num_ax + 1) * num_genes_per_subplot, num_genes))
        df_unit_sub = df_unit.iloc[index_genes_subplot]
        df_col_sub = df_col.iloc[index_genes_subplot]

        pos_group = np.arange(len(df_unit_sub))  # the x-positions of the bar groups

        df_unit_sub_cumsum = df_unit_sub[col_names].cumsum(axis=1)  # cumsum over each row

        for jj, col_name in enumerate(col_names):  # loop over all tissue masks
            bottom = None if jj == 0 else df_unit_sub_cumsum.iloc[:, jj - 1]
            axs[num_ax, 0].bar(pos_group, df_unit_sub[col_name], bar_width, bottom=bottom,  # add bar to plot
                               label=masks_to_plot[jj])

        axs[num_ax, 0] = g_bar.format_axes(axs[num_ax, 0], df_unit_sub, unit, pos_group,
                                           'Normalized counts', txt_size)  # format axes

        ax2 = axs[num_ax, 0].twinx()  # add 2nd y-axis
        ax2.plot(pos_group, df_col_sub, color='red', linestyle='-', linewidth=1.0,
                 marker='o', markersize=2.0, label='counts in all tissues')
        ax2.set_ylabel('Counts in all tissues ' + unit, color='red', size=txt_size+1)
        ax2.tick_params(axis='y', labelsize=txt_size)
        ax2.yaxis.set_major_formatter(g_plt.sci_notation_format())

    plt.xticks(fontsize=txt_size)  # tick labels
    plt.yticks(fontsize=txt_size)

    g_bar.format_title_and_legend(axs, num_subplots, txt_tit)  # plot title and legend

    plt.savefig(p['output'] + 'Barplot_stacked_' + txt_tit + '_Counts ' + mask_type + ' masks ' + unit + '.png',
                dpi=img_res_in_dpi)

#################################
