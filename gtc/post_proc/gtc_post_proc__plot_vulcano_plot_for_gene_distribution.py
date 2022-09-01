#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import math
import numpy as np
import pandas as pd
import gtc.post_proc as g_post
import matplotlib.pyplot as plt
from adjustText import adjust_text


def plot_vulcano_plot_for_gene_distribution(
    main_output_dir: str,
    fnames_gtc_param: list,
    column_names: list,
    dfs_stat: dict,
    names_gtc_param_ranks: dict,
    df_pathway_groups: pd.DataFrame,
    alpha2_ttest_rel: float = 0.05,
    alpha2_ttest_ind: float = 0.05,
    point_size: int = 16,
    ax_label_fontsize: int = 16,
    tick_fontsize: int = 14,
    gene_label_fontsize: int = 8,
    leg_fontsize: int = 6,
    exp_pts: float = 1.1,  # distance between line end and points
    exp_txt: float = 1.5,  # length of lines
    title_fontsize: int = 5,
    save_res: int = 300,
    SHOW_ANNOTATIONS: bool = False
) -> None:

    """Perform vulcano plots for the the significant genes:
     - x-axis: log2(fold change)
     - y-axis: - log10(p-value)
    in the gene distributions:
     - neoplastic / non-neoplastic tissue without relaps
       consideration
     - neoplastic tissue of relaps patients /
       neoplastic tissue of non-relaps patients."""

    DEBUG_PLOT_ONLY_1_SERIES = False

    ####

    path_out = main_output_dir + 'Summary_vulcano_plots_significant_genes/'
    g_post.create_dir(path_out)

    names_gtc_param = g_post.rm_ext(fnames_gtc_param)

    pre_mask_types, tissues, units = g_post.split_column_names_in_mask_types_and_tissues_and_units(column_names)

    try:
        for name_gtc_param in names_gtc_param:
            counter = 1
            for pre_mask_type in pre_mask_types:
                for unit in units:
                    for test_type in ['ttest_rel', 'ttest_ind']:
                        print('Creating plot %d of %d for %s' % (counter, len(pre_mask_types) * len(units) * 2, name_gtc_param))

                        alpha2_ttest = alpha2_ttest_rel if test_type == 'ttest_rel' else alpha2_ttest_ind

                        df = dfs_stat[name_gtc_param][pre_mask_type + unit]
                        df = df[['genes', test_type + '_pvalue', test_type + '_mean1', test_type + '_mean2']].copy()  # extract values - without copy error arrise
                        df.columns = ['genes', 'pvalues', 'mean1', 'mean2']  # rename columns

                        df = g_post.calc_miss_df_values_for_vulcano_plot(df, df_pathway_groups, test_type,
                                                                         alpha2_ttest, k=-1.3, d=5.0)

                        fig, ax = plt.subplots()  # define subplot

                        label_genes = []  # relevant genes get labels on plot
                        significant_genes = 'Significant genes\n'  # significant genes

                        for _, row in df.iterrows():  # loop over all genes
                            gene_name = row['genes']
                            label = row['group_names']
                            x = row['log2_fold_changes']
                            y = row['log10_pvalues']

                            if row['is_significant'] == 'yes':
                                ax.scatter(x, y, color=row['rgba_colors'], alpha=row['alphas_opacity'],
                                           marker=row['symbols'], s=point_size, edgecolor='none', label=label)
                            else:
                                ax.scatter(x, y, color=row['rgba_colors'], alpha=row['alphas_opacity'],
                                           marker=row['symbols'], s=point_size, edgecolor='none', label='not significant')

                            if row['is_labeled'] == 'yes':
                                label_genes.append(ax.text(x, y, gene_name, color='black', fontsize=gene_label_fontsize))
                            if row['is_significant'] == 'yes':
                                significant_genes += gene_name + '\n'

                        adjust_text(label_genes, arrowprops=dict(arrowstyle="-", color='grey', lw=0.8),  # move gene labels to avoid overlap
                                    expand_points=(exp_pts, exp_pts), force_points=0.8,
                                    expand_text=(exp_txt, exp_txt), force_text=0.5)

                        if SHOW_ANNOTATIONS:
                            if test_type == 'ttest_rel':
                                title = "Up-regulation of genes in 'neoplastic' tissue (compared to 'non-neoplastic' " \
                                        "tissue) - paired t-test with alpha/2 = %1.2f" % alpha2_ttest_rel
                            else:
                                title = "Up-regulation of genes in 'neoplastic' tissue of relaps patients " \
                                        "(compared to non-relaps patients) - independent t-test with " \
                                        "alpha/2 = %1.2f" % alpha2_ttest_ind
                            ax.set_title(title, loc='left', fontsize=title_fontsize)

                            ax.text(0.02, 0.02, significant_genes, transform=ax.transAxes, fontsize=2)  # summarize significant genes in textbox

                        max_abs_log2_fold_changes = math.ceil(np.max(np.abs(df['log2_fold_changes'])))
                        max_log10_pvalues = math.ceil(np.max(df['log10_pvalues']))

                        ax.axhline(y=-math.log10(alpha2_ttest), color='grey', linestyle='-.', linewidth=0.7)

                        if test_type == 'ttest_rel':
                            ax.set_xlim([-max_abs_log2_fold_changes, max_abs_log2_fold_changes+1])
                        else:
                            ax.set_xlim([-max_abs_log2_fold_changes, max_abs_log2_fold_changes])
                        ax.set_ylim([0, max_log10_pvalues])
                        ax.set_xlabel('log2(fold changes)', fontsize=ax_label_fontsize)
                        ax.set_ylabel('- log10(p-values)', fontsize=ax_label_fontsize)
                        ax.tick_params(axis='both', labelsize=tick_fontsize)

                        if not SHOW_ANNOTATIONS:
                            handles, labels = plt.gca().get_legend_handles_labels()  # remove duplicates from legend
                            by_label = dict(zip(labels, handles))
                            legend = plt.legend(by_label.values(), by_label.keys(), loc='upper left', frameon=False,
                                                title='Processes and cell types', fontsize=leg_fontsize)
                            plt.setp(legend.get_title(), fontsize=leg_fontsize+2)
                            legend._legend_box.align = 'left'
                            for lh in legend.legendHandles:  # set full alpha opacity
                                lh.set_alpha(1.0)

                        fig.tight_layout()
                        plt.savefig(path_out + names_gtc_param_ranks[name_gtc_param] + '__' +
                                    name_gtc_param + '__' + pre_mask_type + unit + '__' +
                                    test_type + str(SHOW_ANNOTATIONS) + '.png', dpi=save_res)
                        plt.close(fig)

                        counter += 1

            if DEBUG_PLOT_ONLY_1_SERIES: raise Exception  # stop after the run of 1 series to debug

    except Exception: pass

#################################
