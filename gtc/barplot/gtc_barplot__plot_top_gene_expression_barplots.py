#################################
# Michael Gruber, 21.10.2021    #
# Medizinische Universität Graz #
# Lehrstuhl für Histologie      #
#################################

import numpy as np
import pandas as pd
import gtc.plot as g_plt
import gtc.function as g_fct
import matplotlib.pyplot as plt


def plot_top_gene_expression_barplots(
    df_counts: pd.DataFrame,
    c: dict,
    p: dict,
    num_genes: int = 10,
    txt_size: int = 14
) -> None:

    """Plot the top expressed genes in each
    gene mask and tissue mask as a bar plot."""

    img_res_in_dpi = p['img_res_in_dpi']

    ####

    col_names = list(df_counts.columns)
    col_names.remove('genes')

    for mask_name in c['all_tissue_mask_names_calc']:
        print('-Plot top genes for %s' % mask_name)

        col_name = g_fct.df_col_names(mask_name, c['units'][0])

        df_col = df_counts[['genes'] + [col_name]].copy()  # genes + column
        df_col.sort_values(by=[col_name], ascending=False, inplace=True)
        df_col = df_col.head(num_genes)

        fig, ax = plt.subplots()  # new plot

        ax.barh(np.arange(num_genes), df_col[col_name].to_numpy(), align='center', edgecolor='black', linewidth=0.6)

        ax.set_xlabel('Counts', fontsize=txt_size+1)
        ax.tick_params(axis='x', labelsize=txt_size)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
        ax.xaxis.set_major_formatter(g_plt.sci_notation_format())

        ax.set_ylabel('Genes', fontsize=txt_size+1)
        ax.tick_params(axis='y', labelsize=txt_size)
        ax.set_yticks(range(num_genes))  # ensures one tick per gene, otherwise we get fewer
        ax.set_yticklabels(df_col['genes'].astype(str).values)
        ax.invert_yaxis()

        fig.subplots_adjust(left=0.30, right=0.90, top=0.80, bottom=0.20)

        plt.savefig(p['output'] + 'Plot_top_' + str(num_genes) + '_genes_' + col_name + '.png',
                    dpi=img_res_in_dpi)

#################################
