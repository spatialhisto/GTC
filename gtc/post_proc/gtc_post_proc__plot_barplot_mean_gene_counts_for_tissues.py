#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import math
import pandas as pd
import seaborn as sns
import gtc.mask as g_msk
import gtc.post_proc as g_post
import matplotlib.pyplot as plt
from typing import Tuple


def plot_barplot_mean_gene_counts_for_tissues(
    main_output_dir: str,
    fnames_gtc_param: list,
    genes: list,
    column_names: list,
    dfs_counts: dict,
    names_gtc_param_ranks: dict,
    plot_size: Tuple[float, float] = (29.0, 20.0),  # (width, height) subplot size
    img_dims_plots: Tuple[int, int] = (400, 400),
    pos_txt_box: Tuple[float, float] = (0.50, -0.04),
    num_rows_per_plot: int = 10,
    num_genes_per_row: int = 10,
    font_size_box: int = 9,
    save_res: int = 300
) -> None:

    """Perform bar plots for the
    mean gene counts in the tissues
    'neoplastic' and 'non-neoplastic',
    with one standard deviation as
    error bar and the count values as
    points."""

    DEBUG_PLOT_ONLY_1_SERIES = False

    ####

    path_out = main_output_dir + 'Summary_barplot_mean_gene_counts_for_tissues/'
    g_post.create_dir(path_out)

    empty_img = g_msk.new_white_color_image(list(img_dims_plots))  # empty black image

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    pre_mask_types, tissues, units = g_post.split_column_names_in_mask_types_and_tissues_and_units(column_names)
    num_tissues = len(tissues)

    num_genes_per_plot = num_rows_per_plot * num_genes_per_row
    num_plots = math.ceil(len(genes) / num_genes_per_plot)  # only 1 series of plots for debugging

    try:
        for name_gtc_param in names_gtc_param:
            counter = 1
            for pre_mask_type in pre_mask_types:
                for unit in units:
                    for num_plot in range(num_plots):
                        print('-Creating plot %d of %d for %s' %
                              (counter, len(pre_mask_types) * len(units) * num_plots, name_gtc_param))

                        fig, axs = plt.subplots(num_rows_per_plot, num_genes_per_row, figsize=plot_size)  # define subplot

                        genes_sub = genes[num_genes_per_plot * num_plot:num_genes_per_plot * (num_plot + 1)]
                        if len(genes_sub) < num_genes_per_plot:  # fill empty fields
                            genes_sub += ['empty' for _ in range(len(genes_sub), num_genes_per_plot)]

                        for count_gene_plot, gene_sub in enumerate(genes_sub):  # loop over every gene
                            row_plot = math.floor(count_gene_plot / num_genes_per_row)
                            col_plot = count_gene_plot - row_plot * num_genes_per_row
                            ax = axs[row_plot, col_plot]  # set axis

                            if gene_sub not in ['empty']:
                                data = {'tissues': [], 'counts': []}

                                for tissue in tissues:  # loop over every tissue
                                    column_name = pre_mask_type + tissue + unit

                                    index = g_post.get_row_index(dfs_counts[name_gtc_param][column_name], 'genes', gene_sub)
                                    gene_counts = dfs_counts[name_gtc_param][column_name].iloc[index, 1:]  # drop gene name (column 1) and read out count values

                                    data['tissues'] += [tissue for _ in range(len(gene_counts))]
                                    data['counts'] += list(gene_counts)

                                df_gene_counts = pd.DataFrame(data)

                                if df_gene_counts['counts'].size / num_tissues > 1:  # enough values for standard deviation
                                    sns.barplot(ax=ax, x='tissues', y='counts', hue='tissues', data=df_gene_counts,
                                                palette=['orangered', 'limegreen'],
                                                ci='sd', capsize=0.12, errwidth=1.0, errcolor='black', dodge=False)
                                else:
                                    sns.barplot(ax=ax, x='tissues', y='counts', hue='tissues', data=df_gene_counts,
                                                palette=['orangered', 'limegreen'])

                                sns.swarmplot(ax=ax, x='tissues', y='counts', data=df_gene_counts, color='royalblue', size=5)

                                ax.legend().set_visible(False)
                                handles, labels = ax.get_legend_handles_labels()
                                ax.axes.xaxis.set_visible(False)
                                ax.text(pos_txt_box[0], pos_txt_box[1], '%s' % gene_sub,
                                        transform=ax.transAxes, fontsize=font_size_box,
                                        verticalalignment='center', horizontalalignment='center',
                                        bbox=dict(boxstyle='round', facecolor='white', edgecolor='none', alpha=1.0))

                            else:
                                ax.imshow(empty_img, extent=[0, img_dims_plots[1], 0, img_dims_plots[0]], aspect='auto')
                                ax.axes.xaxis.set_ticks([])  # turn off ticks and tick labels
                                ax.axes.yaxis.set_ticks([])
                                ax.axis('off')

                        fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.99), ncol=num_tissues,
                                   bbox_transform=fig.transFigure, frameon=False)
                        plt.suptitle('Tissues', fontsize=20, x=0.5, y=1.0)

                        plt.subplots_adjust(hspace=0.1, wspace=0.1, bottom=0.0, top=0.9, left=0.0, right=1.0)  # spacing between subplots
                        fig.tight_layout()

                        plt.savefig(path_out + names_gtc_param_ranks[name_gtc_param] + '__' +
                                    name_gtc_param + '__' + pre_mask_type + unit + '__' +
                                    'image' + ('__%02d' % (num_plot + 1)) + '.png', dpi=save_res)
                        plt.close(fig)

                        counter += 1

                if DEBUG_PLOT_ONLY_1_SERIES: raise Exception  # stop after the run of 1 series to debug

    except Exception: pass

#################################
